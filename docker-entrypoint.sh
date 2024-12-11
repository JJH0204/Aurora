#!/bin/bash

# Start MariaDB service
service mariadb start

# Wait for MariaDB to be ready
while ! mysqladmin ping -h "localhost" --silent; do
    echo "Waiting for database to be ready..."
    sleep 2
done

# Create database and user if they don't exist
mysql -u root -p${MYSQL_ROOT_PASSWORD} << EOF
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

# 초기화 스크립트 실행
mysql -u root -p$MYSQL_ROOT_PASSWORD < /docker-entrypoint-initdb.d/deploy_db.sql

# Apply database migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

# Start Django development server
python3 manage.py runserver 0.0.0.0:80
