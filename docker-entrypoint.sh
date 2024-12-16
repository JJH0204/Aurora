#!/bin/bash
set -e

# Start MariaDB service
service mariadb start

# Wait for MariaDB to be ready (최대 30초)
max_tries=30
counter=0
while ! mysqladmin ping -h "localhost" --silent; do
    counter=$((counter + 1))
    if [ $counter -gt $max_tries ]; then
        echo "Failed to connect to MariaDB after $max_tries attempts"
        exit 1
    fi
    echo "Waiting for database to be ready... (Attempt $counter/$max_tries)"
    sleep 2
done

echo "MariaDB is ready"

# Create database and user if they don't exist
mysql -u root -p${MYSQL_ROOT_PASSWORD} << EOF
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "Database and user created successfully"

# Apply database migrations
echo "Running Django migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Initialize database with test data
echo "Initializing database with test data..."
mysql -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE < /docker-entrypoint-initdb.d/deploy_db.sql

# Create and setup media directory
echo "Setting up media directory..."
mkdir -p /app/Aurora/Data/media
chmod -R 777 /app/Aurora/Data/media

# Copy original media files from host to container (if they exist)
if [ -d "/app/Aurora/Data/original_media" ]; then
    echo "Copying original media files..."
    cp -r /app/Aurora/Data/original_media/* /app/Aurora/Data/media/
    chmod -R 777 /app/Aurora/Data/media
    ls -la /app/Aurora/Data/media
    echo "Media files setup completed successfully!"
fi

# Collect static files
echo "Collecting static files..."
cd /app
python3 manage.py collectstatic --noinput

# Start Django in background
echo "Starting Django development server..."
python3 manage.py runserver 0.0.0.0:8000 &

# Wait for Django to start
echo "Waiting for Django to start..."
sleep 5

# Start Nginx in foreground
echo "Starting Nginx..."
nginx -g 'daemon off;'
