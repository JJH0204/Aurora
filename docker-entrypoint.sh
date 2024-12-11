#!/bin/sh

# MariaDB 서비스 시작
echo "Starting MariaDB service..."
service mariadb start

# MariaDB 초기 설정
echo "Configuring MariaDB..."
mysql -u root << EOF
CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;
CREATE USER IF NOT EXISTS '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';
GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn aurora.wsgi:application \
    --bind 0.0.0.0:80 \
    --timeout 120 \
    --workers 3 \
    --threads 3 \
    --worker-class gthread \
    --log-level debug \
    --access-logfile - \
    --error-logfile - \
    --capture-output
