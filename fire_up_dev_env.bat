@echo off
docker-compose.exe up -d
docker.exe exec -it apache-container bash -c "docker-php-ext-install mysqli && apachectl restart"
docker.exe cp .\testdata.sql mysql-container:/tmp
echo "Waiting for mysql to start..."
timeout /t 5 /nobreak >nul
docker.exe exec -it mysql-container bash -c "mysql -u root --password=root < /tmp/testdata.sql"
bash -c "./apitest.sh"