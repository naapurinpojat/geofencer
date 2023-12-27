import datetime
import redis
from time import sleep

class RedisClient:
    def __init__(self, host, port, topic, consumer_group, consumer_name, logger=None):
        self.logger = logger
        self.host = host
        self.port = port
        self.topic = topic
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name

        self.client = redis.Redis(host=host, port=port, decode_responses=True)

        try:
            self.client.xgroup_create(self.topic, self.consumer_group, id=0, mkstream=True)
        except:
            self.logger.debug("Consumer group most likely already existing")
            pass

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
                self.shutdown_event.set()
                break         

        self.logger.debug("Redis loaded")

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
