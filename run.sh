#!/bin/bash

# Stop and remove existing aurora container if it exists
docker stop aurora 2>/dev/null
docker rm aurora 2>/dev/null

# Build the Docker image with the specified tag
docker build -t krjaeh0/aurora:latest .

# Run the container
docker run -d --name aurora -p 80:80 -v "$(pwd)/Aurora:/app/Aurora" krjaeh0/aurora:latest

# Show container status
docker ps | grep aurora
