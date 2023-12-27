"""Module providing Redis connection handlers"""
from time import sleep
import datetime
import redis

class RedisClient:
    """Redis client to handle Redis read/write"""
    # pylint: disable=too-many-arguments
    def __init__(self,
                 host,
                 port,
                 topic,
                 consumer_group,
                 consumer_name,
                 logger=None):
        self.logger = logger
        self.host = host
        self.port = port
        self.topic = topic
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name

        self.client = redis.Redis(host=host, port=port, decode_responses=True)

        try:
            self.client.xgroup_create(self.topic, self.consumer_group, id=0, mkstream=True)
        except redis.ResponseError:
            self.logger.debug("Consumer group most likely already existing")

        self.logger.debug("Redis client initialised")
        start_time = datetime.datetime.now()
        while True:
            time = datetime.datetime.now()
            time_diff = time - start_time
            info = self.client.info()
            if info.get('loading', 1) == 1:
                sleep(1)
            else:
                break

            if time_diff.total_seconds() >= 60:
                logger.critical("Couldn't establish connection to redis")
                return

        self.logger.debug("Redis loaded")

    def read_messages(self, initial=False):
        """Read messages from stream that is part of topic"""
        _ = (initial) # use this later
        count = 1

        messages_ret = []
        messages = self.client.xreadgroup(self.consumer_group,
                                          self.consumer_name,
                                          {self.topic: '>'},
                                          count=count)
        for mes in messages:
            for mes_id, mes_data in mes[1]:
                messages_ret.append(mes_data)
                self.client.xack(mes[0], self.consumer_group, mes_id)

        return messages_ret

    def add_message(self, message):
        """Add message to redis stream"""
        self.client.xadd(self.topic, message)

    def close(self):
        """Close redis client connection"""
        self.client.close()
