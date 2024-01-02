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
from threading import Event
import queue
import gitversion

from nmea_redis_connection import NMEAStreamReader, RedisPublisher
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
    shutdown_event = Event()

    logger.info("Starting Snowdog %s", gitversion.git_revision)
    redis_topic = "snowdog:location"

    mqtt_topic = f"telemetry/{secrets.MY_TENANT}/{secrets.MY_DEVICE}"

    io_queue = queue.Queue(maxsize=100)

    mqtt_client = MqttClient(secrets.HTTP_ADAPTER_IP,
                              secrets.MQTT_PORT,
                              None,
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
                                        "redis_iot_group",
                                        "redis_iot",
                                        logger=logger)

    redis_rest_consumer = RedisConsumer(redis_client,
                                        redis_topic,
                                        "redis_rest_group",
                                        "redis_rest",
                                        logger=logger)

    nmeareader_thread = NMEAStreamReader('NMEAStreamReader',
                                         '/dev/EG25.NMEA',
                                         io_queue,
                                         logger)

    redis_publisher_thread = RedisPublisher('RedisPublisher',
                                            redis_client,
                                            io_queue,
                                            logger)

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
