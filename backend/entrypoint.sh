#!/bin/sh
set -e

echo "Waiting for database..."
sleep 5

echo "Running migrations..."
python manage.py migrate --noinput

echo "Compiling translations..."
python manage.py compilemessages --ignore=venv 2>/dev/null || true

echo "Starting server..."
# Use runserver for now (we can switch to gunicorn later)
python manage.py runserver 0.0.0.0:8000
