#!/bin/sh
CURRENTDATE=`date +"%Y-%m-%d-%T"`

nohup socat pty,raw,echo=0,link=/dev/EG27.NMEA pty,raw,echo=0,link=/dev/EG25.NMEA > /dev/null &

nohup redis-server --bind 0.0.0.0 &
. /home/snowdog/venv/bin/activate

curl http://apache-container:80/snowdog/map.geojson > /home/snowdog/map.geojson
nohup python /home/snowdog/nmea_testdata/emulator.py "/home/snowdog/nmea_testdata/snowdog-1.gpx" &
python /home/snowdog/snowdog.py
#ps|grep "python /home/snowdog/snowdog.py" > "snowdog-thread.info"