#!/bin/sh
CURRENTDATE=`date +"%Y-%m-%d-%T"`

pip install -r /home/snowdog/requirements.txt

nohup socat pty,raw,echo=0,link=/dev/EG27.NMEA pty,raw,echo=0,link=/dev/EG25.NMEA > /dev/null &

nohup redis-server --bind 0.0.0.0 &

curl http://apache-container:80/snowdog/map.geojson > /home/snowdog/map.geojson
nohup python /home/snowdog/nmea_testdata/emulator.py "/home/snowdog/nmea_testdata/snowdog-1.gpx" &
# test different NMEA data delays
#nohup python /home/snowdog/nmea_testdata/emulator.py "/home/snowdog/nmea_testdata/snowdog-1.gpx" delay_test &

python /home/snowdog/snowdog.py