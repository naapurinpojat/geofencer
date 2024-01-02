"""
NMEA Module

This module provides functionality for parsing NMEA (National Marine Electronics Association)
data and adding it to a Redis stream. It supports both virtual and hardware interfaces.

Usage:
1. Create an instance of the NMEAStreamReader class.
2. Configure the parser with the desired interface type (virtual or hw).
3. Start parsing NMEA data by running this class in thread
4. Parsed data is added to the specified Redis stream using the RedisPublisher class.

Example:
    # Create an instance of the NMEAParser
    nmea_reader = NMEAStreamReader()

    # Configure the parser for the virtual interface
    set environmental variable VIRTUAL_SNOWDOG=1 if running im docker

    # Start parsing NMEA data
    nmea_reader.start()

    # Add parsed data to Redis stream
    redis_publisher = RedisPublisher()
    redis_publisher.start()


Classes:
- NMEAStreamReader: Main class for NMEA reading/parsing and Redis stream integration.
- RedisPublisher: Class supporting parser to cache data to redis

Interfaces:
- VirtualInterface: Simulate NMEA data for testing purposes.
- HardwareInterface: Connect to a hardware device for real-time NMEA data.

Dependencies:
- RedisClient: Required for interacting with Redis.
- NMEAReader: Required for parsing NMEA data.

Note: Make sure to install the required dependencies before using this module.
"""
import os
import queue
from threading import Thread
import datetime
from pynmeagps import NMEAReader
from pynmeagps import exceptions as nmea_exceptions

from utils import Utils as utils
from redis_client import RedisClient

if int(os.getenv("VIRTUAL_SNOWDOG", '0')) == 1:
    import serial # pylint: disable=import-error


def process_data(que, data, logger):
    """Check NMEA data quality and put it to queue for RedisPublisher"""
    _ = (logger) # unused
    data_to_process = ['GPGGA', 'GPVTG']
    #logger.debug(data)
    if data.quality == 1:
        if data.identity in data_to_process:
            #logger.debug(data)
            que.put_nowait(data)


class NMEAStreamReader(Thread):
    """
    Thread class to read NMEA input

    Args:
        name (str): Name of thread
        path (str): NMEA device path
        data_que (Queue): Queue where data is stored for processing
        logger (Logger): Used for logging
    """
    def __init__(self, name, path: str, data_que: queue.Queue, logger):
        super().__init__(name=name)
        self.queue = data_que
        self.path = path
        self.logger = logger
        self.running = True

    def stop(self):
        """Stop thread execution"""
        self.running = False
        self.join()

    def nmea_handler_virt(self):
        """Handle reading from virtual serial port"""
        with serial.Serial(self.path, 38400, timeout=0.1) as stream:
            while True:
                nmr = NMEAReader(stream, nmeaonly=False)

                if stream.in_waiting:
                    line = stream.readline()
                    parsed_data = nmr.parse(line, validate=2)
                    if parsed_data:
                        process_data(self.queue, parsed_data, self.logger)

                if self.running is False:
                    break

                utils.sleep_ms(100)

    def nmea_handler(self):
        """Handle reading from real NMEA stream"""
        with open(self.path, 'rb') as stream:
            nmr = NMEAReader(stream, nmeaonly=True)
            for (raw_data, parsed_data) in nmr:
                _ = (raw_data) # not used
                try:
                    process_data(self.queue, parsed_data, self.logger)
                except nmea_exceptions.NMEAParseError:
                    pass

                if self.running is False:
                    break

    def run(self):
        self.logger.info("NMEAStreamReader starting")

        if int(os.getenv("VIRTUAL_SNOWDOG", '0')) == 1:
            self.logger.info("NMEAStreamReader running in virtual env")
            self.nmea_handler_virt()
        else:
            self.logger.debug("NMEAStreamReader running in hardware")
            self.nmea_handler()

        self.logger.info("NMEAStreamReader shutting down")

class RedisPublisher(Thread):
    """
    Thread class to publish data to Redis stream

    Args:
        name (str): Name of thread
        client (RedisClient): Initialized client for Redis connection
        data_que (Queue): queue where data is read
        logger (Logger): Used for logging
    """
    def __init__(self, name, client: RedisClient, data_que: queue.Queue, logger):
        super().__init__(name=name)
        self.client = client
        self.queue = data_que
        self.logger = logger
        self.running = True

    def stop(self):
        """Stop thread execution"""
        self.running = False
        self.join()

    def run(self):
        self.logger.info("RedisPublisher running")
        while self.running:
            if not self.queue.empty():
                data = self.queue.get()
                redis_data = self.nmea_data_to_redis_format(data)
                self.queue.task_done()

                if redis_data:
                    self.client.add_message(redis_data)
            utils.sleep_ms(100)
        self.logger.info("RedisPublisher shutting down")

    def nmea_data_to_redis_format(self, raw_data):
        """Format data from nmea stream to be compliance with Redis data structure"""
        def format_ts(raw_ts):
            ts_raw = f"{datetime.date.today()} {raw_ts}"
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
        except KeyError as error:
            data = None
            self.logger.debug(error)

        self.logger.debug(data)

        return data
