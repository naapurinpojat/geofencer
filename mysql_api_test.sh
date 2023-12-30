#!/bin/bash
# this can be run when docker containers are up and running

docker cp testdata.sql mysql-container:/tmp
sleep 5
docker exec -it mysql-container bash -c 'mysql -u root --password=root -h localhost < /tmp/testdata.sql'
./apitest.sh