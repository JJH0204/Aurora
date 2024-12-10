#!/bin/sh
echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn aurora.wsgi:application --bind 0.0.0.0:80 --timeout 120 --workers 3 --threads 3 --worker-class gthread
