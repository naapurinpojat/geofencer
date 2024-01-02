"""Module providing MQTT client functionalities"""
import os
import socket
import ssl
import paho.mqtt.client as pahomqtt

from utils import Utils as utils

class MqttClient:
    """
    Class to handle MQTT client connections
    """
    # pylint: disable=too-many-arguments
    def __init__(self,
                 broker_address,
                 broker_port,
                 client_id,
                 username=None,
                 password=None,
                 ssl_file=None,
                 logger=None):
        self.logger = logger
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client_id = client_id
        self.context = None
        self.connection_retries = 0

        self.client = pahomqtt.Client(self.client_id, protocol=pahomqtt.MQTTv5)

        if int(os.getenv("VIRTUAL_SNOWDOG", '0')) == 0:
            if ssl_file:
                self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                self.context.load_verify_locations(ssl_file)
                self.client.tls_set_context(self.context)

            if username and password:
                self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        self.connected = False

    def on_connect(self, client, userdata, flags, result_code, properties):
        """on_connect callback"""
        # pylint: disable=too-many-arguments
        _ = (client, userdata, flags, properties) # unused
        if result_code == 0:
            self.logger.info(f'Connected to MQTT broker {self.broker_address}:{self.broker_port}')
            self.connection_retries = 0
            self.connected = True
        else:
            self.logger \
                .critical(f"Failed to connect to the MQTT broker with result code {result_code}")
            raise Exception(f"Connection failed with result code {result_code}")


    def on_disconnect(self, client, userdata, result_code, properties):
        """on_disconnect callback"""
        _ = (client, userdata, properties) # unused
        self.connected = False

        if result_code != 0:
            self.logger.warning(f'Disconnected suddenly from MQTT broker ({result_code})')
        else:
            self.logger.info("Disconnected from MQTT broker succesfully")
            self.client.loop_stop()

    def keep_connected(self):
        """"method to keep client connected"""
        if not self.is_connected():
            self.connection_retries += 1
            try:
                self.client.reconnect()
            except socket.gaierror as connection_error:
                self.logger.critical(f"MQTT broker not available {connection_error}")

    def is_connected(self):
        """method to check is client connected"""
        return self.connected

    def connect(self):
        connection_timeout_s = 60 * 5 # 5 minutes
        """method to connect client to broker"""
        time_beginning = utils.get_time()
        while not self.connected:
            try:
                self.client.connect(self.broker_address, self.broker_port)
                self.client.loop_start()

            except socket.gaierror as connection_error:
                time_delta = utils.timedelta_seconds(time_beginning)
                self.logger.debug(f"Have tried to connect for {time_delta} seconds")

                if time_delta > connection_timeout_s:
                    raise ConnectionError("Timeout, couldn't connect MQTT broker")
                self.logger.critical(f"Trying to connect, but MQTT broker not available \
                                     {connection_error}")

                utils.sleep_ms(1000)

    def disconnect(self):
        """method to disconnect client"""
        self.client.disconnect()

    def publish(self, topic, data):
        """method to publish new message to broker"""
        return self.client.publish(topic, data)

    def get_connection_retries(self):
        """check current count of reconnection retries"""
        return self.connection_retries
 