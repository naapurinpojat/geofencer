import queue
from threading import Thread
import datetime
from pynmeagps import NMEAReader

from utils import Utils as utils
from redis_client import RedisClient


class NMEAStreamReader(Thread):
    """
    Thread class to read NMEA input

    Args:
        name (str): Name of thread
        path (str): NMEA device path
        data_que (Queue): Queue where data is stored for processing
        shutdown_event (Event): Follow programs shutdown event
    """
    def __init__(self, name, path: str, data_que: queue.Queue, logger):
        super().__init__(name=name)
        self.queue = data_que
        self.path = path
        self.logger = logger
        self.running = True

    def stop(self):
        self.running = False
        self.join()

    def run(self):
        self.logger.info("NMEAStreamReader starting")
        data_to_process = ['GPGGA', 'GPVTG']

        with open(self.path, 'rb') as stream:
            nmr = NMEAReader(stream, nmeaonly=True)

            for (raw_data, parsed_data) in nmr:
                _ = (raw_data) # not used
                try:
                    if parsed_data.quality == 1:
                        if parsed_data.identity in data_to_process:
                            self.logger.debug(parsed_data)
                            self.queue.put_nowait(parsed_data)
                except NMEAReader.NMEAParseError:
                    pass

                if self.running is False:
                    break

        self.logger.info("NMEAStreamReader shutting down")

class RedisPublisher(Thread):
    """
    Thread class to publish data to Redis stream

    Args:
        name (str): Name of thread
        client (RedisClient): Initialized client for Redis connection
        data_que (Queue): queue where data is read
        shutdown_event (Event): Follow programs shutdown event
    """
    def __init__(self, name, client: RedisClient, data_que: queue.Queue, logger):
        super().__init__(name=name)
        self.client = client
        self.queue = data_que
        self.logged = logger
        self.running = True

    def stop(self):
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

        return data