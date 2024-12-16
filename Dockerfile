# 빌드 스테이지
FROM ubuntu:latest

# 기본 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-venv \
    python3-pip \
    python3-full \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    dos2unix \
    mariadb-server \
    mariadb-client \
    imagemagick \
    nginx \
    wget \
    git \
    bison \
    flex \
    libgeoip-dev \
    liblmdb-dev \
    libpcre3-dev \
    libyajl-dev \
    automake \
    autoconf \
    libtool \
    libcurl4-openssl-dev \
    libxml2-dev \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Nginx 및 ModSecurity 디렉토리 설정
RUN mkdir -p /etc/nginx/modules /etc/nginx/modsecurity

# ModSecurity 소스 빌드
RUN cd /opt && \
    git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity && \
    cd ModSecurity && \
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make && \
    make install && \
    cp modsecurity.conf-recommended /etc/nginx/modsecurity/modsecurity.conf && \
    sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/nginx/modsecurity/modsecurity.conf

# Nginx 커넥터 설치
RUN cd /opt && \
    git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git && \
    wget http://nginx.org/download/nginx-1.24.0.tar.gz && \
    tar zxvf nginx-1.24.0.tar.gz && \
    cd nginx-1.24.0 && \
    ./configure --with-compat --add-dynamic-module=/opt/ModSecurity-nginx && \
    make modules && \
    cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/

COPY nginx-modsecurity/nginx.conf /etc/nginx/nginx.conf
COPY nginx-modsecurity/modsecurity.conf /etc/nginx/modsecurity/modsecurity.conf

# MariaDB 데이터 디렉토리 설정
RUN mkdir -p /var/run/mysqld && \
    chown -R mysql:mysql /var/run/mysqld && \
    chmod 777 /var/run/mysqld

# MariaDB 초기화
RUN mysql_install_db --user=mysql --datadir=/var/lib/mysql

# 작업 디렉토리 설정
WORKDIR /app

# 정적 파일 및 미디어 디렉토리 생성
RUN mkdir -p /app/staticfiles /app/Aurora/Data/media && \
    chmod -R 755 /app/staticfiles /app/Aurora/Data/media

# Assets 디렉토리 생성 (볼륨 마운트 포인트)
RUN mkdir -p /app/Aurora/Assets && \
    chmod -R 755 /app/Aurora/Assets

# 가상 환경 생성 및 활성화
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# bcrypt 패키지 설치
RUN pip3 install --no-cache-dir bcrypt

# MariaDB 초기화 스크립트 복사
COPY Maria/deploy_db.sql /docker-entrypoint-initdb.d/
RUN chmod 644 /docker-entrypoint-initdb.d/deploy_db.sql && \
    dos2unix /docker-entrypoint-initdb.d/deploy_db.sql

# MariaDB 문자셋 설정
COPY Maria/my.cnf /etc/mysql/conf.d/
RUN chmod 644 /etc/mysql/conf.d/my.cnf

# 나머지 프로젝트 파일 복사
COPY . .

# 실행 스크립트 설정
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN dos2unix /app/docker-entrypoint.sh && \
    chmod +x /app/docker-entrypoint.sh

# 모든 스크립트 파일의 줄바꿈 문자 변환
RUN find /app -type f -name "*.sh" -exec dos2unix {} \;
RUN find /app -type f -name "*.py" -exec dos2unix {} \;
RUN find /app -type f -name "*.sql" -exec dos2unix {} \;

# 디렉토리 권한 설정
RUN chown -R mysql:mysql /var/lib/mysql /var/run/mysqld && \
    chmod -R 755 /app/Aurora/Assets /app/staticfiles /app/Aurora/Data/media

# MariaDB 환경 변수 설정
ENV MYSQL_DATABASE=aurora_db \
    MYSQL_USER=Aurora \
    MYSQL_PASSWORD=AuroraRootPassword \
    MYSQL_ROOT_PASSWORD=qwer

# Django 환경 변수 설정
ENV DJANGO_SETTINGS_MODULE=Django.settings \
    DJANGO_DEBUG=True \
    DJANGO_ALLOWED_HOSTS=* \
    DATABASE_URL=mysql://Aurora:AuroraRootPassword@localhost:3306/aurora_db

# 볼륨 설정
VOLUME ["/app/Aurora"]

# 포트 설정
EXPOSE 80

# 시작 스크립트 실행
ENTRYPOINT ["/app/docker-entrypoint.sh"]