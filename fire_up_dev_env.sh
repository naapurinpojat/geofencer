#!/bin/bash
docker-compose up -d
docker exec -it apache-container bash -c 'docker-php-ext-install mysqli && apachectl restart'
docker cp testdata.sql mysql-container:/tmp
sleep 5
docker exec -it mysql-container bash -c 'mysql -u root --password=root -h localhost < /tmp/testdata.sql'
./apitest.sh