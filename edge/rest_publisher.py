"""
Module to handle data sending to rest API endpoint
"""
import json
from threading import Thread

import requests

from redis_client import RedisConsumer
from utils import Utils as utils
from utils import Fences as fences

def points_from_redis(redis_data) -> dict:
    """Convert data from redis stream to rest API compatible format"""
    return {'lat': float(redis_data.get('lat')),
            'lon': float(redis_data.get('lon')),
            'alt': float(redis_data.get('alt')),
            'speed': float(0),
            'ts': redis_data.get('ts')}

class RestPublisher(Thread):
    """
    Publish gps location to HTTP api endpoint if location has changed 5 m or last update is
    older than three minutes. Keeps track which geofences are passed.

    Args:
        name (str): Name of thread
        api_url (str): API endpoint
        api_key (str): Authentication key
        shutdown_event (Event): Follow programs shutdown event
    """
    def __init__(self,
                 name:str,
                 geojson_file:str,
                 api_url:str,
                 api_key:str,
                 redis_consumer:RedisConsumer,
                 period:int=100,
                 logger=None):
        super().__init__(name=name)
        self.api_url = api_url
        self.api_key = api_key
        self.fences = fences(filepath=geojson_file)
        self.redis = redis_consumer
        self.period = period
        self.logger = logger

        self.shutdown = False

        # Constants
        self.update_rate_seconds = 10
        self.update_rate_meters = 5
        self.update_rate_idle_minutes = 3


    def stop(self):
        """Stop thread"""
        self.shutdown = True
        self.join()

    def run(self):
        self.logger.info("Starting REST publisher")
        last_sent_pos = {}

        # clear redis consumer buffer from old junk
        # todo: push this to some api endpoint for debugging purposes?
        junk_read = 1000
        while True:
            junk_buffer = self.redis.read_messages(junk_read)
            if len(junk_buffer) < junk_read:
                break
            utils.sleep_ms(self.period)

        while not self.shutdown:
            current_time = utils.get_time()
            data = self.redis.read_messages()
            time_delta = utils.timedelta_seconds(last_sent_pos.get('ts', 0), current_time)

            if time_delta >= self.update_rate_seconds:
                current_point = None
                if len(data) > 0:
                    current_point = points_from_redis(data[0])
                if current_point and self.should_send(last_sent_pos, current_point, time_delta):
                    try:
                        payload = self.build_message_json(current_point)
                        headers = {
                            'Content-Type': 'application/json',
                            'Authorization': self.api_key
                        }
                        response = requests.post(self.api_url, data=payload, headers=headers)

                        if response.status_code == 200:
                            last_sent_pos = current_point
                            last_sent_pos['ts'] = current_time # overwrite ts with nanos

                        else:
                            self.logger.warning("API Response: %s", response.status_code)

                    except Exception as error:
                        self.logger.warning("Error connecting to API: %s", error)
            utils.sleep_ms(self.period)
        self.logger.info("Rest publisher shutting down")

    def build_message_json(self, location) -> str:
        """Format data to rest API compatible json str"""
        data = location.copy()
        data['in_area'] = ""
        in_area_data = self.fences.in_area(data)
        if in_area_data:
            data['in_area'] = in_area_data
        self.logger.debug(json.dumps(data))

        return json.dumps(data)

    def should_send(self, last_sent_pos, new_point, time_delta) -> bool:
        """Check if requirements to send new data to rest API fulfills"""
        if not last_sent_pos.get("lat"):
            return True

        point_xy = new_point.get("lat"), new_point.get("lon")
        last_sent_point = last_sent_pos.get("lat", 0), last_sent_pos.get("lon", 0)

        distance_between = utils.haversine_distance_meters(point_xy,
                                                    last_sent_point)

        if distance_between >= self.update_rate_meters:
            return True

        if  time_delta >= self.update_rate_idle_minutes * 60:
            return True

        return False
