# 빌드 스테이지
FROM python:3.11-slim as builder

WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 운영 스테이지
FROM python:3.11-slim

WORKDIR /app

# 빌드 스테이지에서 설치된 Python 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# 애플리케이션 복사
COPY app ./app

# 환경 변수 설정
ENV FLASK_APP=app/app.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# 80 포트 노출
EXPOSE 80

# Gunicorn으로 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "4", "--access-logfile", "-", "app.app:app"]