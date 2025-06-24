#!/bin/bash

# Update system
sudo yum update -y
sudo yum install -y docker
sudo amazon-linux-extras enable docker
sudo service docker start
sudo systemctl start docker
sudo systemctl enable docker

# Download DockerHub's image
docker pull asasgroup/garantias_ia:latest

# Network and Container creation without the compose
docker network create gpt_parsing_default
docker run -d --name redis --network gpt_parsing_default -p 6379:6379 redis:7
docker run -d --name listener --network gpt_parsing_default -p 5000:5000 asasgroup/garantias_ia:latest
docker run -d --name celery_worker1 --network gpt_parsing_default asasgroup/garantias_ia:latest celery -A controller worker --loglevel=info

