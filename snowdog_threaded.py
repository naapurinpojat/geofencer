from pynmeagps import NMEAReader 
from datetime import date, datetime
import json
import queue
from threading import Thread, Event
from time import sleep
import redis
import asyncio
from gmqtt import Client as MQTTClient
import requests
import ssl
import logging

import secrets

USE_MQTT = True

logger = None
g_log_level = logging.INFO

def set_logger(level: int, name=None):
  global logger

  logger = logging.getLogger(name)
  logger.addHandler(logging.StreamHandler())
  logger.setLevel(level)

async def publish_mqtt(client: MQTTClient, topic: str, data: str):
  client.publish(topic, data)

def publish_http(topic: str, data: str):
  url = f'https://{secrets.HTTP_ADAPTER_IP}/http-adapter'
  response = requests.put(f'{url}/{topic}', auth=(f'{secrets.MY_DEVICE}@{secrets.MY_TENANT}', secrets.MY_PWD), data=data)
  logger.debug(response)

def format_ts(raw_ts):
  ts_raw = f"{date.today()} {raw_ts}"
  return f"{datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S').isoformat()}.000Z"

def extract_data(raw_data):
  data = {}
  try:
    if raw_data.identity == 'GPVTG':
      if raw_data.quality == 1:
        data['ts'] = format_ts(raw_data.time)
        data['identity'] = raw_data.identity
        data['speed'] = raw_data.sogk
        logger.debug(data)

    if raw_data.identity == 'GPGGA':
      if raw_data.quality == 1:
        data['ts'] = format_ts(raw_data.time)
        data['identity'] = raw_data.identity
        data['lat'] = raw_data.lat
        data['lon'] = raw_data.lon
        data['alt'] = raw_data.alt
        logger.debug(data)
  except Exception as e:
    data = None
    logger.debug(e)

  return data

def format_iot_ticket(data):
  iot_json = {}

  if data.get('identity') == 'GPGGA':
    t_set = {}
    
    lat_data = {'n':'lat','dt':'double'}
    lon_data = {'n':'lon','dt':'double'}
    alt_data = {'n':'alt','dt':'double'}

    lat_data['value'] = data.get('lat')
    lon_data['value'] = data.get('lon')
    alt_data['value'] = data.get('alt')

    t = [lat_data, lon_data, alt_data]

    t_set['t'] = t
    t_set['id'] = secrets.TELEMETRY_ID
    t_set['ts'] = data.get('ts')

    iot_json = {'t_set':[t_set]}

  if data.get('identity') == 'GPVTG':
    speed_data = {'n':'speed', 'dt':'double'}
    speed_data['data':[{data.get('ts'): data.get('speed')}]]
    iot_json = {'t':[speed_data]}

  return iot_json

def add_data_to_stream(stream_name, data):
  redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

  # Add data to the stream
  redis_client.xadd(stream_name, data)

def read_values_from_device(nmr: NMEAReader, raw_que: queue.Queue, shutdown: Event):
  logger.info("Starting reading data from device ...")

  data_to_process = ['GPGGA', 'GPVTG']

  for (raw_data, parsed_data) in nmr:
    try:
      if parsed_data.quality == 1:
        if parsed_data.identity in data_to_process:
          logger.debug(parsed_data)
          raw_que.put_nowait(parsed_data)
    except queue.Full:
      logger.warning("Previous values not processed yet")
    except:
      pass

    # Check if program is interrupted
    if shutdown.is_set():
      break

  logger.info("Ending read from device")

def process_values(raw_que: queue.Queue, send_que: queue.Queue, shutdown: Event):
  logger.info("Start data processing ...")

  while not shutdown.is_set():
    sleep(0.1)
    if raw_que.empty() is False:
      iot_json = {}
      data_raw = raw_que.get()
      
      # do data formatting for visualisation
      data = extract_data(data_raw)

      raw_que.task_done()

      if data:
        iot_json = format_iot_ticket(data)

        if data.get('identity') == 'GPGGA':
          add_data_to_stream('snowdog:location', data)
        elif data.get('identity') == 'GPVTG':
          add_data_to_stream('snowdog:speed', data)

      if iot_json:
        try:
          send_que.put_nowait(iot_json)
        except queue.Full:
          pass

  logger.info("Ending data processing")

def send_values(que: queue.Queue, shutdown: Event):
  logger.info("Sending values ...")

  client = None
  async_loop = None

  context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  context.load_verify_locations(secrets.CERT_FILE)

  if USE_MQTT:
    # Init MQTT client
    async_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(async_loop)

    client = MQTTClient("py_snowdog")
    client.set_auth_credentials(username=f"{secrets.MY_DEVICE}@{secrets.MY_TENANT}", password=secrets.MY_PWD)

    try:
      async_loop.run_until_complete(client.connect(secrets.HTTP_ADAPTER_IP, secrets.MQTT_PORT, ssl=context))
    except Exception as e:
      logger.critical(f"couldn't connect client to mqtt broker \n {e}")
      shutdown_signal.set()

  topic = f"telemetry/{secrets.MY_TENANT}/{secrets.MY_DEVICE}"

  while not shutdown.is_set():
    sleep(0.1)
    if que.empty() is False:
      data = que.get()

      data = json.dumps(data, ensure_ascii=False)

      if USE_MQTT:
        async_loop.run_until_complete(publish_mqtt(client, topic, data))
      else:
        publish_http(topic, data)

      que.task_done()

  if USE_MQTT:
    async_loop.run_until_complete(client.disconnect())
    async_loop.close()

  logger.info("Ending send values thread")

if __name__ == "__main__":
  set_logger(g_log_level, "py_snowdog")

  send_que = queue.Queue(maxsize=1)
  process_que = queue.Queue(maxsize=10)
  shutdown_signal = Event()

  stream = open('/dev/EG25.NMEA', 'rb')
  nmr = NMEAReader(stream, nmeaonly=True)


  produce_values_thread = Thread(target=read_values_from_device,
                                  args=(nmr,
                                        process_que,
                                        shutdown_signal))
  
  process_values_thread = Thread(target=process_values,
                                 args=(process_que,
                                 send_que,
                                 shutdown_signal))

  send_values_thread = Thread(target=send_values,
                                  args=(send_que,
                                        shutdown_signal))
  
  logger.debug('Starting program ...')
  
  produce_values_thread.start()
  process_values_thread.start()
  send_values_thread.start()


  while not shutdown_signal.is_set():
    try:
      sleep(1)
    except KeyboardInterrupt:
      logger.info("\nTerminated by keyboard... Shutting down")
      shutdown_signal.set()

  produce_values_thread.join()
  process_values_thread.join()
  send_values_thread.join()
