#!/bin/sh
set -e

echo "Waiting for database..."
sleep 5

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Celery worker..."
exec celery -A config worker --loglevel=info
