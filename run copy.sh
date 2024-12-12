#!/bin/bash

# Stop and remove existing aurora container if it exists
docker stop aurora 2>/dev/null
docker rm aurora 2>/dev/null

docker image rm krjaeh0/aurora:latest

docker run -d --name aurora -p 80:80 -v "$(pwd)/Aurora:/app/Aurora" krjaeh0/aurora:latest
