"""
Ultimate snowdog tracker software that uses Redis datastream as local cache
and sends data over HTTP api and also to MQTT broker

Copyright (c) <2023> <Juha Viitanen(https://github.com/bittikettu) &
Matti Wenell(https://github.com/Mattti0)>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from time import sleep
import logging
from threading import Thread, Event
import queue
import datetime
from pynmeagps import NMEAReader
import gitversion

from mqtt_client import MqttClient
from redis_client import RedisClient, RedisConsumer
from mqtt_publisher import MQTTPublisher
from rest_publisher import RestPublisher

import secrets

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

G_TIME = None
G_DATE = None

MS_10 = 0.01
MS_100 = 0.1
MS_1000 = 1

class NMEAStreamReader(Thread):
    """
    Thread class to read NMEA input

    Args:
        name (str): Name of thread
        path (str): NMEA device path
        data_que (Queue): Queue where data is stored for processing
        shutdown_event (Event): Follow programs shutdown event
    """
    def __init__(self, name, path: str, data_que: queue.Queue):
        super().__init__(name=name)
        self.queue = data_que
        self.path = path
        self.running = True

    def stop(self):
        self.running = False
        self.join()

    def run(self):
        logger.info("NMEAStreamReader starting")
        data_to_process = ['GPGGA', 'GPVTG', 'GNGGA']

        with open(self.path, 'rb') as stream:
            nmr = NMEAReader(stream, nmeaonly=True)

            for (raw_data, parsed_data) in nmr:
                _ = (raw_data) # not used
                try:
                    if parsed_data.quality == 1:
                        if parsed_data.identity in data_to_process:
                            logger.debug(parsed_data)
                            self.queue.put_nowait(parsed_data)
                except NMEAReader.NMEAParseError:
                    pass

                if self.running is False:
                    break

        logger.info("NMEAStreamReader shutting down")

def nmea_data_to_redis_format(raw_data):
    """Format data from nmea stream to be compliance with Redis data structure"""
    def format_ts(raw_ts):
        ts_raw = f"{G_DATE} {raw_ts}"
        return f"{datetime.datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S').isoformat()}.000Z"

    data = {}

    try:
        if raw_data.identity == 'GPVTG':
            data['ts'] = format_ts(raw_data.time)
            data['identity'] = raw_data.identity
            data['speed'] = raw_data.sogk

        if raw_data.identity == 'GPGGA' or raw_data.identity == 'GNGGA':
            data['ts'] = format_ts(raw_data.time)
            data['identity'] = raw_data.identity
            data['lat'] = raw_data.lat
            data['lon'] = raw_data.lon
            data['alt'] = raw_data.alt
    except KeyError as error:
        data = None
        logger.debug(error)

    return data

class RedisPublisher(Thread):
    """
    Thread class to publish data to Redis stream

    Args:
        name (str): Name of thread
        client (RedisClient): Initialized client for Redis connection
        data_que (Queue): queue where data is read
        shutdown_event (Event): Follow programs shutdown event
    """
    def __init__(self, name, client: RedisClient, data_que: queue.Queue):
        super().__init__(name=name)
        self.client = client
        self.queue = data_que
        self.running = True

    def stop(self):
        self.running = False
        self.join()

    def run(self):
        logger.info("RedisPublisher running")
        while self.running:
            if not self.queue.empty():
                data = self.queue.get()
                redis_data = nmea_data_to_redis_format(data)
                self.queue.task_done()

                if redis_data:
                    self.client.add_message(redis_data)
            sleep(MS_100)
        logger.info("RedisPublisher shutting down")

def main():
    """
    Main thread to handle producers, consumers and data formatting threads

    - Initialize clients
    - Create threads where connections is handled
    - Update global time
    - If thread fails, try to restart it

    Returns:
        None
    """
    # pylint: disable=global-statement
    global G_TIME
    global G_DATE
    G_TIME = datetime.datetime.now()
    G_DATE = datetime.date.today()
    shutdown_event = Event()

    logger.info("Starting Snowdog %s", gitversion.git_revision)
    redis_consumer_name_mqtt = "redis_iot"
    redis_consumer_group_mqtt = "redis_iot_group"
    redis_consumer_name_rest = "redis_rest"
    redis_consumer_group_rest = "redis_rest_group"
    redis_topic = "snowdog:location"

    mqtt_client_name = None
    mqtt_topic = f"telemetry/{secrets.MY_TENANT}/{secrets.MY_DEVICE}"

    io_queue = queue.Queue(maxsize=100)

    mqtt_client = MqttClient(secrets.HTTP_ADAPTER_IP,
                              secrets.MQTT_PORT,
                              mqtt_client_name,
                              f"{secrets.MY_DEVICE}@{secrets.MY_TENANT}",
                              secrets.MY_PWD,
                              ssl_file=secrets.CERT_FILE,
                              logger=logger)

    redis_client = RedisClient('localhost',
                               6379,
                               redis_topic,
                               logger=logger)

    redis_mqtt_consumer = RedisConsumer(redis_client,
                                        redis_topic,
                                        redis_consumer_group_mqtt,
                                        redis_consumer_name_mqtt,
                                        logger=logger)

    redis_rest_consumer = RedisConsumer(redis_client,
                                        redis_topic,
                                        redis_consumer_group_rest,
                                        redis_consumer_name_rest,
                                        logger=logger)

    nmeareader_thread = NMEAStreamReader('NMEAStreamReader',
                                         '/dev/EG25.NMEA',
                                         io_queue)

    redis_publisher_thread = RedisPublisher('RedisPublisher',
                                            redis_client,
                                            io_queue)

    mqtt_publisher_thread = MQTTPublisher('MQTTPublisher',
                                          mqtt_client,
                                          mqtt_topic,
                                          redis_mqtt_consumer,
                                          logger=logger)

    rest_publisher_thread = RestPublisher('RestPublisher',
                                          '/home/snowdog/map.geojson',
                                          secrets.WEB_API,
                                          secrets.API_KEY,
                                          redis_rest_consumer,
                                          logger=logger)

    nmeareader_thread.start()
    redis_publisher_thread.start()
    mqtt_publisher_thread.start()
    rest_publisher_thread.start()

    threadslist = [nmeareader_thread,
                   redis_publisher_thread,
                   mqtt_publisher_thread,
                   rest_publisher_thread
                   ]

    while not shutdown_event.is_set():
        try:
            # Update time in main thread so no need to get that on every thread
            G_TIME = datetime.datetime.now()
            G_DATE = datetime.date.today()

            for thread in threadslist:
                if not thread.is_alive():
                    logger.critical("%s is not running", thread.name)
            sleep(1)
        except KeyboardInterrupt:
            logger.info("Terminated by keyboard... Shutting down")
            shutdown_event.set()

    for thread in threadslist:
        thread.stop()

    mqtt_client.disconnect()
    redis_client.close()


if __name__ == "__main__":
    main()
