"""Module providing Redis connection handlers"""
from threading import Event
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
                 logger=None):
        self.logger = logger
        self.topic = topic
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

        start_time = datetime.datetime.now()
        while True:
            time_diff = datetime.datetime.now() - start_time
            info = self.redis.info()
            if info.get('loading', 1) == 1:
                # Block execution until redis connection is loaded
                Event.wait(1)
            else:
                break

            if time_diff.total_seconds() >= 60:
                logger.critical("Couldn't establish connection to redis")
                return None

        self.logger.debug("Redis client initialised")

    def add_message(self, message):
        """Add message to redis stream"""
        self.redis.xadd(self.topic, message)

    def close(self):
        """Close redis client connection"""
        self.redis.close()

class RedisConsumer:
    """Store redis stream consumer group details"""
    def __init__(self,
                 client: RedisClient,
                 topic: str,
                 consumer_group: str,
                 consumer_name: str,
                 logger=None):
        self.client = client
        self.topic = topic
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name
        self.logger = logger

        try:
            self.client.redis.xgroup_create(self.topic, self.consumer_group, id=0, mkstream=True)
        except redis.ResponseError as e:
            print(e)
            self.logger.debug("Consumer group most likely already existing")

    def read_messages(self, count=1):
        """Read messages from stream that is part of topic"""

        messages_ret = []
        messages = self.client.redis.xreadgroup(self.consumer_group,
                                          self.consumer_name,
                                          {self.topic: '>'},
                                          count=count)
        for mes in messages:
            for mes_id, mes_data in mes[1]:
                messages_ret.append(mes_data)
                self.client.redis.xack(mes[0], self.consumer_group, mes_id)

        return messages_ret
