#! /bin/bash

rm -rf ../exports
mkdir -p ../exports/
mkdir -p ../exports/dockerImages

docker build -t "rodeo_server" -f "Docker/Server/Dockerfile" ../
docker build -t "rodeo_engine" -f "Docker/Engine/Dockerfile" ../

docker save -o "../exports/dockerImages/server" "rodeo_server"
docker save -o "../exports/dockerImages/engine" "rodeo_engine"

cp -r ../code/Database ../exports
cp install.sh ../exports/
cp docker-compose.yml ../exports/


mkdir -p ../install/
tar -cvzf ../install/rodeoserver.tar.gz ../exports/*