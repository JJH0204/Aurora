#!/bin/bash

# Stop and remove existing aurora container if it exists
docker stop aurora 2>/dev/null
docker rm aurora 2>/dev/null

# Create Docker volume for database persistence if it doesn't exist
docker volume create aurora_db_data

# Build the Docker image with the specified tag
docker build -t krjaeh0/aurora:latest .

# Run the container with volume mount for database
docker run -d --name aurora \
    -p 80:80 \
    -v "$(pwd)/Aurora:/app/Aurora" \
    -v aurora_db_data:/var/lib/mysql \
    krjaeh0/aurora:latest

# Show container status
docker ps | grep aurora