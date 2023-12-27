import paho.mqtt.client as pahomqtt
import ssl

class MQTTClient:
    def __init__(self, broker_address, broker_port, client_id, username=None, password=None, ssl_file=None, logger=None):
        self.logger = logger
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client_id = client_id
        self.context = None
        self.connection_retries = 0

        self.client = pahomqtt.Client(self.client_id, protocol=pahomqtt.MQTTv5)

        if ssl_file:
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_verify_locations(ssl_file)
            self.client.tls_set_context(self.context)

        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc, properties):
        self.logger.info(f'Connected to MQTT broker {self.broker_address}:{self.broker_port}')
        self.connection_retries = 0
        
    def on_disconnect(self, client, userdata, rc, properties):
        self.logger.warning(f'Disconnected from MQTT broker ({rc}) {properties}')

    def keep_connected(self):
        if not self.client.is_connected():
            self.connection_retries += 1
            self.client.reconnect()

    def is_connected(self):
        return self.client.is_connected()

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_start()

    def publish(self, topic, data):
        return self.client.publish(topic, data)

    def get_connection_retries(self):
        return self.connection_retries
 