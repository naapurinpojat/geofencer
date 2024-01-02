"""
Redis Client Module

This module provides a RedisClient class for establishing and managing
a connection to a Redis server.

Usage:
1. Create an instance of the RedisClient class.
2. Perform Redis operations using methods like `add_message`, `read_messages`.
3. Disconnect from the Redis server using the `close` method when done.

Example:
    # Create an instance of the RedisClient
    redis_client = RedisClient()

    # Disconnect from the Redis server
    redis_client.close()

Classes:
- RedisClient: Main class for establishing and managing a connection to a Redis server.
- RedisConsumer: Class used to consume data from redis streams

Methods:
- close: Disconnect from the Redis server.
- read_messages: Retrieve the value associated with a key.
- add_message: Set the value associated with a key.

Dependencies:
- redis: Required for interacting with the Redis server.

Note: Make sure to install the required dependencies before using this module.
"""

from threading import Event
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
    # pylint: disable=too-many-arguments, too-few-public-methods
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
        except redis.ResponseError as redis_error: # pylint: disable=unused-variable
            self.logger.debug("Consumer group most likely already existing")

    def read_messages(self, count=1, block=None):
        """Read messages from stream that is part of topic"""

        messages_ret = []
        messages = self.client.redis.xreadgroup(self.consumer_group,
                                          self.consumer_name,
                                          {self.topic: '>'},
                                          count=count,
                                          block=block)
        for mes in messages:
            for mes_id, mes_data in mes[1]:
                messages_ret.append(mes_data)
                self.client.redis.xack(mes[0], self.consumer_group, mes_id)

        return messages_ret
    