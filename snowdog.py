from pynmeagps import NMEAReader
import json
import paho.mqtt.client as pahomqtt
import redis
from time import sleep
import ssl
import logging
from threading import Thread, Event, Lock
import queue
import datetime

import secrets

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

g_time = None
g_date = None

MS_10 = 0.01
MS_100 = 0.1
MS_1000 = 1

class MQTTClient:
    def __init__(self, broker_address, broker_port, client_id, username=None, password=None, ssl_file=None):
        self.logger = logging.getLogger(__name__)
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client_id = client_id
        self.context = None
        self.connection_retries = 0

        self.client = pahomqtt.Client(self.client_id, protocol=pahomqtt.MQTTv5)

        if ssl_file:
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_verify_locations(ssl_file)
            self.client.tls_set_context(self.context)

        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc, properties):
        self.logger.info(f'Connected to MQTT broker {self.broker_address}:{self.broker_port}')
        self.connection_retries = 0
        
    def on_disconnect(self, client, userdata, rc, properties):
        self.logger.warning(f'Disconnected from MQTT broker ({rc}) {properties}')

    def keep_connected(self):
        if not self.client.is_connected():
            self.connection_retries += 1
            self.client.reconnect()

    def is_connected(self):
        return self.client.is_connected()

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_start()

    def publish(self, topic, data):
        return self.client.publish(topic, data)

    def get_connection_retries(self):
        return self.connection_retries
    
class RedisClient:
    def __init__(self, host, port, topic, consumer_group, consumer_name):
        self.host = host
        self.port = port
        self.topic = topic
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name

        self.client = redis.Redis(host=host, port=port, decode_responses=True)

        try:
            self.client.xgroup_create(self.topic, self.consumer_group, id=0, mkstream=True)
        except:
            logger.debug("Consumer group most likely already existing")
            pass

        logger.debug("Redis client initialised")

    def read_messages(self, initial=False):
        count = 1

        messages_ret = []
        messages = self.client.xreadgroup(self.consumer_group, self.consumer_name, {self.topic: '>'}, count=count)
        for mes in messages:
            for mes_id, mes_data in mes[1]:
                messages_ret.append(mes_data)
                self.client.xack(mes[0], self.consumer_group, mes_id)

        return messages_ret
    
    def add_message(self, message):
        self.client.xadd(self.topic, message)

    def close(self):
        self.client.close()

class MQTTPublisher(Thread):
    def __init__(self, client: MQTTClient, topic: str, redis_client, shutdown_event: Event):
        super().__init__()
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

        while not self.shutdown_event.is_set():
            if self.client.is_connected():
                messages = self.redis_client.read_messages()

                ts_buffer = []

                for data in messages:
                    topic, d = format_iot_ticket(data)
                    if topic == 'location':
                        ts_buffer.append(d)

                if len(ts_buffer) > 0:
                    ts_json = json.dumps({'t_set': ts_buffer}, ensure_ascii=False)

                    try:
                        self.client.publish(self.topic, ts_json)
                    except Exception as e:
                        logger.critical(f"Couldn't send data \n {e} \n")

            else:
                logger.critical("MQTT client not connected")

                if not self.client.keep_connected():
                    self.shutdown_event.set()
                else:
                    logger.info("Reconnected succesfully")

            sleep(MS_100)
        logger.info("MQTTPublisher shutting down")


class NMEAStreamReader(Thread):
    def __init__(self, path: str, data_que: queue.Queue, shutdown_event: Event):
        super().__init__()
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
    def __init__(self, client: RedisClient, data_que: queue.Queue, shutdown_event: Event):
        super().__init__()
        self.client = client
        self.queue = data_que
        self.shutdown_event = shutdown_event

    def run(self):
        def extract_data(raw_data):
            def format_ts(raw_ts):
                ts_raw = f"{g_date} {raw_ts}"
                return f"{datetime.datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S').isoformat()}.000Z"
            
            data = {}
            try:
                if raw_data.identity == 'GPVTG':
                    data['ts'] = format_ts(raw_data.time)
                    data['identity'] = raw_data.identity
                    data['speed'] = raw_data.sogk

                if raw_data.identity == 'GPGGA':
                    data['ts'] = format_ts(raw_data.time)
                    data['identity'] = raw_data.identity
                    data['lat'] = raw_data.lat
                    data['lon'] = raw_data.lon
                    data['alt'] = raw_data.alt 
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


def main():
    global g_time
    global g_date
    g_time = datetime.datetime.now()
    g_date = datetime.date.today()
    shutdown_event = Event()

    redis_consumer_name = "redis_iot"
    redis_consumer_group = "redis_iot_group"
    redis_topic = "snowdog:location"

    mqtt_client_name = "py_snowdog"
    mqtt_topic = f"telemetry/{secrets.MY_TENANT}/{secrets.MY_DEVICE}"

    io_queue = queue.Queue(maxsize=100)

    mqtt_client = MQTTClient(secrets.HTTP_ADAPTER_IP, secrets.MQTT_PORT, mqtt_client_name, f"{secrets.MY_DEVICE}@{secrets.MY_TENANT}", secrets.MY_PWD, ssl_file=secrets.CERT_FILE)
    redis_client = RedisClient('localhost', 6379, redis_topic, redis_consumer_group, redis_consumer_name)

    nmeareader_thread = NMEAStreamReader('/dev/EG25.NMEA', io_queue, shutdown_event)
    redis_publisher_thread = RedisPublisher(redis_client, io_queue, shutdown_event)
    mqtt_publisher_thread = MQTTPublisher(mqtt_client, mqtt_topic, redis_client, shutdown_event)

    nmeareader_thread.start()
    redis_publisher_thread.start()
    mqtt_publisher_thread.start()

    while not shutdown_event.is_set():
        try:
            # Update time in main thread so no need to get that on every thread
            g_time = datetime.datetime.now()
            g_date = datetime.date.today()
            sleep(1)
        except KeyboardInterrupt:
            logger.info("Terminated by keyboard... Shutting down")
            shutdown_event.set()
            
    nmeareader_thread.join()
    redis_publisher_thread.join()
    mqtt_publisher_thread.join()

    mqtt_client.disconnect()
    redis_client.close()


if __name__ == "__main__":
    main()
