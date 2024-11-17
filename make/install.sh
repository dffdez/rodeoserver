#! /bin/bash

docker image load -i dockerImages/engine &&
docker image load -i dockerImages/server

docker compose up -d