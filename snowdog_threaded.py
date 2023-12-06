from pynmeagps import NMEAReader 
from datetime import date, datetime
import json
import queue
from threading import Thread, Event
from time import sleep
import requests
import redis

import secrets

def add_data_to_stream(stream_name, data):
    redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    # Add data to the stream
    redis_client.xadd(stream_name, data)

def produce_values(nmr: NMEAReader, raw_que: queue.Queue, shutdown: Event):
  for (raw_data, parsed_data) in nmr:
    try:
      if parsed_data.identity == 'GPGGA':
        if parsed_data.quality == 1:
            data = {}

            ts_date = str(date.today())
            ts_time = str(parsed_data.time)
            ts_raw = f"{ts_date} {ts_time}"
            data['ts'] = f"{datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S').isoformat()}.000Z"
            data['lat'] = parsed_data.lat
            data['lon'] = parsed_data.lon
            data['alt'] = parsed_data.alt
#            print(json.dumps(data))

            raw_que.put_nowait(data)
    except queue.Full:
      print("Previous value not sent yet")
    except:
      pass
    # Check if program is interrupted
    if shutdown.is_set():
      break
#   sleep(0.5)

def process_values(raw_que: queue.Queue, send_que: queue.Queue, shutdown: Event):
  print("Start data processing ...")

  stream_name = "loc:snowdog"

  while not shutdown.is_set():
    if raw_que.empty() is False:
      data = raw_que.get()
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

#      try:
#        res = add_data_to_stream(stream_name, {'t_set':[t_set]})
#        print(res)
#      except:
#        pass
      try:
        send_que.put_nowait({'t_set':[t_set]})
      except queue.Full:
        pass

      raw_que.task_done()
#    sleep(0.5)

def send_values(que: queue.Queue, shutdown: Event):
  print("Sending values...")

  while not shutdown.is_set():
    if que.empty() is False:
      data = que.get()

      data = json.dumps(data, ensure_ascii=False)
      response = requests.put(f'https://{secrets.HTTP_ADAPTER_IP}/http-adapter/telemetry/{secrets.MY_TENANT}/{secrets.MY_DEVICE}', auth=(f'{secrets.MY_DEVICE}@{secrets.MY_TENANT}', secrets.MY_PWD), data=data)
      que.task_done()
#    sleep(0.5)

if __name__ == "__main__":
  send_que = queue.Queue(maxsize=1)
  process_que = queue.Queue(maxsize=10)
  shutdown_signal = Event()

  stream = open('/dev/EG25.NMEA', 'rb')
  nmr = NMEAReader(stream, nmeaonly=True)


  produce_values_thread = Thread(target=produce_values,
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
  
  produce_values_thread.start()
  process_values_thread.start()
  send_values_thread.start()


  while not shutdown_signal.is_set():
    try:
      sleep(1)
    except KeyboardInterrupt:
      print("Terminated by keyboard... Shutting down")
      shutdown_signal.set()

  produce_values_thread.join()
  process_values_thread.join()
  send_values_thread.join()
