@echo off

:: Stop and remove existing aurora container if it exists
docker stop aurora 2>nul
docker rm aurora 2>nul

:: Build the Docker image with the specified tag
docker build -t krjaeh0/aurora:latest .

:: Run the container
docker run -d --name aurora -p 80:80 -v "%cd%/Aurora:/app/Aurora" krjaeh0/aurora:latest

:: Show container status
docker ps
