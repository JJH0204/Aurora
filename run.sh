#!/bin/bash

# MariaDB 데이터를 위한 볼륨 생성
docker volume create aurora_db_data

# 기존 컨테이너 중지 및 제거
docker stop aurora 2>/dev/null
docker rm aurora 2>/dev/null

# Docker 이미지 빌드
docker build -t krjaeh0/aurora:latest .

# 컨테이너 실행 (볼륨 마운트 추가)
docker run -d --name aurora \
    -p 80:80 \
    -v "$(pwd)/Aurora:/app/Aurora" \
    -v aurora_db_data:/var/lib/mysql \
    krjaeh0/aurora:latest

# 컨테이너 상태 확인
docker ps | grep aurora