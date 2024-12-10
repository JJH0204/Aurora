#!/bin/sh
set -e

echo "Running migrations..."
python manage.py makemigrations accounts posts core
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn aurora.wsgi:application --bind 0.0.0.0:80
