# 빌드 스테이지
FROM python:3.11-slim AS builder

WORKDIR /app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 운영 스테이지
FROM python:3.11-slim

WORKDIR /app

# MySQL 클라이언트 라이브러리 설치
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 빌드 스테이지에서 설치된 Python 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# 프로젝트 파일 복사
COPY . .

# 시작 스크립트 생성
RUN echo '#!/bin/sh' > /app/docker-entrypoint.sh && \
    echo 'echo "Running migrations..."' >> /app/docker-entrypoint.sh && \
    echo 'python manage.py migrate' >> /app/docker-entrypoint.sh && \
    echo 'echo "Collecting static files..."' >> /app/docker-entrypoint.sh && \
    echo 'python manage.py collectstatic --noinput' >> /app/docker-entrypoint.sh && \
    echo 'echo "Starting Gunicorn..."' >> /app/docker-entrypoint.sh && \
    echo 'exec gunicorn aurora.wsgi:application --bind 0.0.0.0:80 --timeout 120 --workers 3 --threads 3 --worker-class gthread' >> /app/docker-entrypoint.sh && \
    chmod +x /app/docker-entrypoint.sh

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=aurora.settings

# 80 포트 노출
EXPOSE 80

# 시작 스크립트 실행
CMD ["sh", "/app/docker-entrypoint.sh"]