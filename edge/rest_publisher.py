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

        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }

        # clear redis consumer buffer from old junk
        # todo: push this to some api endpoint for debugging purposes?
        junk_read = 1000
        while True:
            junk_buffer = self.redis.read_messages(junk_read)
            if len(junk_buffer) < junk_read:
                break
            utils.sleep_ms(self.period)

        while not self.shutdown:
            api_available = False
            try:
                available_query = requests.get(f"{self.api_url}/version",
                                               headers=headers,
                                               timeout=10)
                if available_query.status_code == 200:
                    #self.logger.debug("Web API available")
                    api_available = True
                else:
                    # If server is completely out of order, previous call will
                    # throw an exception that is caught later (ConnectionError)
                    self.logger.critical(f"Web API not available ({available_query.status_code})")

                if api_available:
                    # This relies on NMEA device update rate of 1 second
                    # If connection to API is lost we don't consume data from Redis and when API is
                    # again available we will go through Redis stream in chunks of 10 messages
                    # sending only one of those to REST API to keep 10 seconds update period for
                    # web service
                    data = self.redis.read_messages(10, int(self.period/2))
                    current_time = utils.get_time()
                    time_delta = utils.timedelta_seconds(last_sent_pos.get('ts_epoch', 0),
                                                         current_time)

                    if time_delta >= self.update_rate_seconds or len(data) >= 5:
                        current_point = None
                        if len(data) > 0:
                            current_point = points_from_redis(data[-1])
                        else:
                            if last_sent_pos.get('ts_epoch'):
                                current_point = last_sent_pos.copy()
                                current_point.pop('ts_epoch')

                        if current_point and self.should_send(last_sent_pos,
                                                              current_point,
                                                              time_delta):
                            try:
                                payload = self.build_message_json(current_point)
                                response = requests.post(f"{self.api_url}/location",
                                                         data=payload,
                                                         headers=headers,
                                                         timeout=10)

                                if response.status_code == 200:
                                    last_sent_pos = current_point
                                    last_sent_pos['ts_epoch'] = current_time

                                else:
                                    self.logger.warning("API Response: %s", response.status_code)

                            except Exception as error:
                                self.logger.warning("Error connecting to API: %s", error)
            except requests.exceptions.ConnectionError as connection_error:
                self.logger.warning(f"API not available \n {connection_error}")

            if api_available:
                utils.sleep_ms(self.period)
            else:
                # No intention to bully API with extra traffic if version not available
                utils.sleep_ms(self.period * 10)
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
