#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate

echo "Creating/updating superuser..."
python create_admin.py

echo "Build completed successfully."