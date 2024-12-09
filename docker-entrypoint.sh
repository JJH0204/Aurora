#!/bin/sh

# 마이그레이션 파일 생성
python manage.py makemigrations accounts posts core

# 데이터베이스 마이그레이션
python manage.py migrate

# 정적 파일 수집
python manage.py collectstatic --noinput

# 개발 서버 실행
gunicorn aurora.wsgi:application --bind 0.0.0.0:80
