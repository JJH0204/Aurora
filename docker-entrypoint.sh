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

# Apply database migrations first
python3 manage.py makemigrations
python3 manage.py migrate

# Now run the initialization script
mysql -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE < /docker-entrypoint-initdb.d/deploy_db.sql

# Create media directory
mkdir -p /app/Aurora/Data/media

# Copy original media files from host to container (if they exist)
if [ -d "/app/Aurora/Data/original_media" ]; then
    echo "Copying original media files..."
    cp -r /app/Aurora/Data/original_media/* /app/Aurora/Data/media/
    chmod -R 777 /app/Aurora/Data/media
    ls -la /app/Aurora/Data/media  # 파일 복사 확인
    echo "Media files setup completed successfully!"
fi

# Collect static files
cd /app
python3 manage.py collectstatic --noinput

# Start Django development server
python3 manage.py runserver 0.0.0.0:80
