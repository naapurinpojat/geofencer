""""
Module to handle data sending to MQTT broker
"""
import json
from threading import Thread

from utils import Utils as utils
from redis_client import RedisConsumer
from mqtt_client import MqttClient
import secrets


def iot_ticket_formatter(data):
    """
    Format position data to telemetry set and speed to telemetry data that could be sent to
    IOT-TICKET (https://iot-ticket.com)
    """
    iot_json = {}

    if data.get('identity') == 'GPGGA':
        telemetry_set = {}

        lat_data = {'n':'lat','dt':'double'}
        lon_data = {'n':'lon','dt':'double'}
        alt_data = {'n':'alt','dt':'double'}

        lat_data['value'] = data.get('lat')
        lon_data['value'] = data.get('lon')
        alt_data['value'] = data.get('alt')

        telemetry = [lat_data, lon_data, alt_data]

        telemetry_set['t'] = telemetry
        telemetry_set['id'] = secrets.TELEMETRY_ID
        telemetry_set['ts'] = data.get('ts')

        iot_json = 'location', telemetry_set

    elif data.get('identity') == 'GPVTG':
        speed_data = {'n':'speed', 'dt':'double'}
        data = {data.get('ts'),data.get('speed')}
        speed_data["data"] = [data]

        iot_json = 'speed', speed_data

    return iot_json

class MQTTPublisher(Thread):
    """
    Thread to publish gps positions to MQTT broker
    """
    def __init__(self,
                 name: str,
                 client: MqttClient,
                 mqtt_topic: str,
                 redis_client:RedisConsumer,
                 period:int=100,
                 logger=None):
        super().__init__(name=name)
        self.client = client
        self.mqtt_topic = mqtt_topic
        self.redis_client = redis_client
        self.period = period
        self.logger = logger

        self.shutdown = False

    def stop(self):
        """Stop thread"""
        self.shutdown = True
        self.join()

    def run(self):
        self.logger.info("MQTTPublisher starting")
        last_connection_check = utils.get_time()

        self.client.connect()

        while not self.shutdown:
            try:
                if self.client.is_connected():
                    last_connection_check = utils.get_time()
                    messages = self.redis_client.read_messages()

                    ts_buffer = []

                    for redis_data in messages:
                        topic, data = iot_ticket_formatter(redis_data)
                        if topic == 'location':
                            ts_buffer.append(data)

                    if len(ts_buffer) > 0:
                        ts_json = json.dumps({'t_set': ts_buffer}, ensure_ascii=False)

                        try:
                            mqtt_message_info = self.client.publish(self.mqtt_topic, ts_json)
                            if not mqtt_message_info.is_published():
                                self.logger.warning("Data not published %d", mqtt_message_info.rc)
                        except RuntimeError as rterr:
                            self.logger.critical(rterr)

                elif utils.timedelta_seconds(last_connection_check, utils.get_time()) >= 10:
                    last_connection_check = utils.get_time()
                    self.logger.critical("MQTT client not connected, trying to reconnect")

                    if self.client.get_connection_retries() < 10:
                        self.client.keep_connected()
                    else:
                        raise
            except Exception as error:
                self.logger.critical("MQTT connection failed. Trying manual reconnect")
                self.client.disconnect()
                utils.sleep_ms(10 * 1000)
                self.client.connect()

            utils.sleep_ms(self.period)

        self.logger.info("MQTTPublisher shutting down")
