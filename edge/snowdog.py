import requests
from pynmeagps import NMEAReader
import json
from time import sleep
import logging
from threading import Thread, Event
import queue
import datetime
from math import radians, sin, cos, sqrt, atan2
import gitversion

from edge.mqtt_client import MqttClient
from RedisClient import RedisClient

import secrets

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

g_time = None
g_date = None

g_last_known_pos = {'lat': 0, 'lon': 0, 'alt': 0, 'speed': 0, 'ts': None}

MS_10 = 0.01
MS_100 = 0.1
MS_1000 = 1

class MQTTPublisher(Thread):
    def __init__(self, name, client: MqttClient, topic: str, redis_client, shutdown_event: Event):
        super().__init__(name=name)
        self.client = client
        self.topic = topic
        self.shutdown_event = shutdown_event
        self.redis_client = redis_client

    def run(self): 
        def format_iot_ticket(data):
            iot_json = {}

            if data.get('identity') == 'GPGGA':
                t_set = {}
                
                lat_data = {'n':'lat','dt':'double'}
                lon_data = {'n':'lon','dt':'double'}
                alt_data = {'n':'alt','dt':'double'}

                lat_data['value'] = data.get('lat')
                lon_data['value'] = data.get('lon')
                alt_data['value'] = data.get('alt')

                t = [lat_data, lon_data, alt_data]

                t_set['t'] = t
                t_set['id'] = secrets.TELEMETRY_ID
                t_set['ts'] = data.get('ts')

                iot_json = 'location', t_set

            if data.get('identity') == 'GPVTG':
                speed_data = {'n':'speed', 'dt':'double'}
                speed_data['data':[{data.get('ts'): data.get('speed')}]]

                iot_json = 'speed', speed_data

            return iot_json
        
        logger.info("MQTTPublisher starting")
        last_connection_check = g_time

        self.client.connect()

        # wait a while to get client connected
        retries = 0
        while not self.client.is_connected():
            connection_check_delta = g_time - last_connection_check
            if connection_check_delta.total_seconds() >= 1:
                retries += 1

                self.client.connect()

                if retries > 10:
                    logger.critical("Couldn't connect MQTT broker")
                    return

            sleep(MS_100)

        if self.client.is_connected():
            logger.info("MQTT client connected")

        while not self.shutdown_event.is_set():
            if self.client.is_connected():
                last_connection_check = g_time
                messages = self.redis_client.read_messages()

                ts_buffer = []

                for data in messages:
                    topic, d = format_iot_ticket(data)
                    if topic == 'location':
                        ts_buffer.append(d)

                if len(ts_buffer) > 0:
                    ts_json = json.dumps({'t_set': ts_buffer}, ensure_ascii=False)

                    try:
                        mqtt_message_info = self.client.publish(self.topic, ts_json)
                        if not mqtt_message_info.is_published():
                            logger.warning(f"Data not published {mqtt_message_info.rc}")
                    except RuntimeError as rterr:
                        logger.critical(rterr)

            else:
                connection_check_delta = g_time - last_connection_check
                if connection_check_delta.total_seconds() >= 10:
                    last_connection_check = g_time
                    logger.critical("MQTT client not connected, trying to reconnect")

                    if self.client.get_connection_retries() < 10:
                        self.client.keep_connected()
                    else:
                        break

            sleep(MS_10)

        logger.info("MQTTPublisher shutting down")

class NMEAStreamReader(Thread):
    def __init__(self, name, path: str, data_que: queue.Queue, shutdown_event: Event):
        super().__init__(name=name)
        self.shutdown_event = shutdown_event
        self.queue = data_que
        self.path = path

    def run(self):
        logger.info("NMEAStreamReader starting")
        data_to_process = ['GPGGA', 'GPVTG']

        stream = open(self.path, 'rb')
        self.nmr = NMEAReader(stream, nmeaonly=True)

        for (raw_data, parsed_data) in self.nmr:
            try:
                if parsed_data.quality == 1:
                    if parsed_data.identity in data_to_process:
                        logger.debug(parsed_data)
                        self.queue.put_nowait(parsed_data)
            except:
                pass

            if self.shutdown_event.is_set():
                break

        logger.info("NMEAStreamReader shutting down")
        stream.close()

class RedisPublisher(Thread):
    def __init__(self, name, client: RedisClient, data_que: queue.Queue, shutdown_event: Event):
        super().__init__(name=name)
        self.client = client
        self.queue = data_que
        self.shutdown_event = shutdown_event

    def run(self):
        def extract_data(raw_data):
            def format_ts(raw_ts):
                ts_raw = f"{g_date} {raw_ts}"
                return f"{datetime.datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S').isoformat()}.000Z"
            
            global g_last_known_pos
            data = {}

            try:
                if raw_data.identity == 'GPVTG':
                    data['ts'] = format_ts(raw_data.time)
                    data['identity'] = raw_data.identity
                    data['speed'] = raw_data.sogk

                    g_last_known_pos['speed'] = data['speed']

                if raw_data.identity == 'GPGGA':
                    data['ts'] = format_ts(raw_data.time)
                    data['identity'] = raw_data.identity
                    data['lat'] = raw_data.lat
                    data['lon'] = raw_data.lon
                    data['alt'] = raw_data.alt

                    g_last_known_pos['lat'] = round(data['lat'], 6)
                    g_last_known_pos['lon'] = round(data['lon'], 6)
                    g_last_known_pos['alt'] = data['alt']

                g_last_known_pos['ts'] = data['ts']
            except Exception as e:
                data = None
                logger.debug(e)

            return data
        
        logger.info("RedisPublisher running")
        while not self.shutdown_event.is_set():
            if not self.queue.empty():
                data = self.queue.get()
                redis_data = extract_data(data)
                self.queue.task_done()

                if redis_data:
                    self.client.add_message(redis_data)
            sleep(MS_100)
        logger.info("RedisPublisher shutting down")

class RestPublisher(Thread):
    def __init__(self, name, api_url, api_key, shutdown_event):
        super().__init__(name=name)
        self.api_url = api_url
        self.api_key = api_key
        self.shutdown_event = shutdown_event
        self.fences = None
        self.areas = {}
        self.last_sent_pos = None
        self.last_sent_pos_ts = None

        with open("areas.json") as f:
            self.fences = json.load(f)

        for i in self.fences.get("features"):
            self.areas[i.get("properties").get("name")] = i.get("geometry").get('coordinates')[0]

    def run(self):
        def haversine_distance_meters(point1, point2):
            """
            Calculate the haversine distance between two points in meters.

            Parameters:
            - point1, point2: Tuple of (latitude, longitude) for each point.

            Returns:
            Distance in meters.
            """
            # Radius of the Earth in meters
            R = 6371000.0

            # Convert latitude and longitude from degrees to radians
            lat1, lon1 = map(radians, point1)
            lat2, lon2 = map(radians, point2)

            # Calculate the differences in coordinates
            dlat = lat2 - lat1
            dlon = lon2 - lon1

            # Haversine formula
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            # Distance in meters
            distance = R * c

            return distance
        
        # Wait until first location is read 
        while g_last_known_pos['lat'] == 0:
            sleep(MS_1000)

        while not self.shutdown_event.is_set():
            data = g_last_known_pos.copy()
            distance_between = None
            if self.last_sent_pos:
                distance_between = haversine_distance_meters((data.get("lat"), data.get("lon")),(self.last_sent_pos.get("lat"), self.last_sent_pos.get("lon")))
                time_diff = g_time - self.last_sent_pos_ts

            if distance_between == None or distance_between > 5 or time_diff.total_seconds() >= 3 * 60:
                try:
                    #data = g_last_known_pos
                    data['api_key'] = self.api_key
                    data['in_area'] = ""
                    in_area_data = self.in_area(data)
                    if in_area_data:
                        data['in_area'] = in_area_data
                    logger.debug(data)
                    response = requests.post(self.api_url, data=json.dumps(data))

                    if response.status_code == 200:
                        self.last_sent_pos = data
                        self.last_sent_pos_ts = g_time

                    logger.debug(f"API Response: {response.status_code}")
                    
                except Exception as e:
                    logger.warning(f"Error connecting to API: {e}")
            sleep(10 * MS_1000)

    def in_area(self, point):
        def point_in_polygon(x, y, polygon):
            """
            Check if a point (x, y) is inside a polygon.

            Parameters:
            - x, y: Coordinates of the point.
            - polygon: List of tuples representing the vertices of the polygon.

            Returns:
            True if the point is inside the polygon, False otherwise.
            """
            n = len(polygon)
            inside = False

            # Ray casting algorithm
            for i in range(n):
                x1, y1 = polygon[i]
                x2, y2 = polygon[(i + 1) % n]

                if ((y1 <= y < y2) or (y2 <= y < y1)) and \
                (x > (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                    inside = not inside

            return inside
        for k, v in self.areas.items():
            if point_in_polygon(point.get('lon'), point.get('lat'), v):
                return k

        return None

def main():
    global g_time
    global g_date
    g_time = datetime.datetime.now()
    g_date = datetime.date.today()
    shutdown_event = Event()

    logger.info(f"Starting Snowdog {gitversion.git_revision}")
    redis_consumer_name = "redis_iot"
    redis_consumer_group = "redis_iot_group"
    redis_topic = "snowdog:location"

    mqtt_client_name = None
    mqtt_topic = f"telemetry/{secrets.MY_TENANT}/{secrets.MY_DEVICE}"

    io_queue = queue.Queue(maxsize=100)

    mqtt_client = mqtt_client(secrets.HTTP_ADAPTER_IP, secrets.MQTT_PORT, mqtt_client_name, f"{secrets.MY_DEVICE}@{secrets.MY_TENANT}", secrets.MY_PWD, ssl_file=secrets.CERT_FILE, logger=logger)
    redis_client = RedisClient('localhost', 6379, redis_topic, redis_consumer_group, redis_consumer_name, logger=logger)

    nmeareader_thread = NMEAStreamReader('NMEAStreamReader', '/dev/EG25.NMEA', io_queue, shutdown_event)
    redis_publisher_thread = RedisPublisher('RedisPublisher', redis_client, io_queue, shutdown_event)
    mqtt_publisher_thread = MQTTPublisher('MQTTPublisher', mqtt_client, mqtt_topic, redis_client, shutdown_event)
    rest_publisher_thread = RestPublisher('RestPublisher', secrets.WEB_API, secrets.API_KEY, shutdown_event)

    nmeareader_thread.start()
    redis_publisher_thread.start()
    mqtt_publisher_thread.start()
    rest_publisher_thread.start()

    threadslist = [nmeareader_thread, redis_publisher_thread, mqtt_publisher_thread, rest_publisher_thread]

    while not shutdown_event.is_set():
        try:
            # Update time in main thread so no need to get that on every thread
            g_time = datetime.datetime.now()
            g_date = datetime.date.today()

            if not shutdown_event.is_set():
                for thread in threadslist:
                    if not thread.is_alive():
                        logger.critical(f"{thread.name} is not running, trying to restart")
                        thread.start()

            sleep(1)
        except KeyboardInterrupt:
            logger.info("Terminated by keyboard... Shutting down")
            shutdown_event.set()
            
    nmeareader_thread.join()
    redis_publisher_thread.join()
    mqtt_publisher_thread.join()
    rest_publisher_thread.join()

    mqtt_client.disconnect()
    redis_client.close()


if __name__ == "__main__":
    main()
