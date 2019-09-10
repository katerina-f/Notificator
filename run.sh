#!/bin/bash

docker volume create --name=notificator.mq
docker volume create --name=notificator.db
docker volume create --name=app_container

docker-compose up -d --build
