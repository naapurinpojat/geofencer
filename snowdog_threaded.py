from pynmeagps import NMEAReader 
from datetime import date, datetime
import json
import queue
from threading import Thread, Event
from time import sleep
import requests

import secrets

def produce_values(nmr: NMEAReader, que: queue.Queue, shutdown: Event):
  for (raw_data, parsed_data) in nmr:
    try:
      if parsed_data.identity == 'GPGGA':
        if parsed_data.quality == 1:
            data = {}

            ts_date = str(date.today())
            ts_time = str(parsed_data.time)
            ts_raw = f"{ts_date} {ts_time}"
            data['ts'] = datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S').isoformat()
            data['lat'] = parsed_data.lat
            data['lon'] = parsed_data.lon
            data['alt'] = parsed_data.alt
            #print(json.dumps(data))

            que.put_nowait(data)
    except queue.Full:
      print("Previous value not sent yet")
    except:
      pass

    # Check if program is interrupted
    if shutdown.is_set():
      break

def send_values(que: queue.Queue, shutdown: Event):
  print("Sending values...")

  while not shutdown.is_set():
    if que.empty is False:
      data = que.get()

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

      print(json.dumps(t_set))

      que.task_done()


if __name__ == "__main__":
  que = queue.Queue(maxsize=1)
  shutdown_signal = Event()

  stream = open('/dev/EG25.NMEA', 'rb')
  nmr = NMEAReader(stream, nmeaonly=True)

  produce_values_thread = Thread(target=produce_values,
                                  args=(nmr,
                                        que,
                                        shutdown_signal))

  send_values_thread = Thread(target=send_values,
                                  args=(que,
                                        shutdown_signal))
  
  produce_values_thread.start()
  send_values_thread.start()


  while not shutdown_signal.is_set():
    try:
      sleep(1)
    except KeyboardInterrupt:
      print("Terminated by keyboard... Shutting down")
      shutdown_signal.set()

  produce_values_thread.join()
  send_values_thread.join()
