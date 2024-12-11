# 빌드 스테이지
FROM ubuntu:latest

# 기본 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    dos2unix \
    mariadb-server \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# MariaDB 초기 설정
RUN mkdir -p /var/run/mysqld && \
    chown -R mysql:mysql /var/run/mysqld && \
    chmod 777 /var/run/mysqld

# MariaDB 데이터베이스 초기화
RUN mysql_install_db --user=mysql --datadir=/var/lib/mysql

# requirements.txt 먼저 복사
COPY requirements.txt .

# 가상 환경 생성 및 활성화
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# pip 설정 업데이트 및 패키지 설치
RUN pip install --upgrade pip && \
    pip config set global.timeout 1000 && \
    pip config set global.retries 10 && \
    pip install --no-cache-dir -r requirements.txt

# 나머지 프로젝트 파일 복사
COPY . .

# 시작 스크립트 설정
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN dos2unix /app/docker-entrypoint.sh && \
    chmod +x /app/docker-entrypoint.sh

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=aurora.settings \
    MYSQL_DATABASE=aurora_db \
    MYSQL_USER=aurora_user \
    MYSQL_PASSWORD=aurora_password \
    MYSQL_HOST=localhost

# 80 포트 노출
EXPOSE 80 3306

# 컨테이너 이름 설정
LABEL name="krjaeh0/aurora"

# 시작 스크립트 실행
CMD ["sh", "/app/docker-entrypoint.sh"]