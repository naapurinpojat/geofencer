#!/bin/sh
wget -N https://juhaviitanen.com/snowdog/map.geojson -P /home/snowdog/
nohup python /home/snowdog/snowdog.py > snowdog.log &
ps|grep "python /home/snowdog/snowdog.py"
