#!/bin/bash
source venv/bin/activate

cd notificator.db || exit
docker volume create --name=notificator.db

docker-compose up -d
sleep 3

cd ..

cd notificator.mq || exit
docker volume create --name=notificator.mq
docker-compose up -d

sleep 3

cd ..

sudo systemctl start reminder.service
