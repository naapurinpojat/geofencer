#!/bin/sh
CURRENTDATE=`date +"%Y-%m-%d-%T"`
filename="/tmp/connok"
inotifywait -e create "$(dirname "$filename")" && [ -e "$filename" ] && echo "Connection OK!"

curl http://juhaviitanen.com/snowdog/map.geojson > /home/snowdog/map.geojson
nohup python /home/snowdog/snowdog.py > "snowdog-${CURRENTDATE}.log" &
ps|grep "python /home/snowdog/snowdog.py" > "snowdog-thread.info"