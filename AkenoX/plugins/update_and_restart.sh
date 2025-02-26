#!/bin/bash

# Navigate to the bot's directory
cd ~/home/ubuntu/drag-inline

# Pull latest changes
git pull

# Stop and remove the old container
docker stop akenox-inline
docker rm akenox-inline

# Rebuild and restart the container
docker build -t akenox-inline .
docker run -d --restart always --name akenox-inline akenox-inline
