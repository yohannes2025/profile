#!/usr/bin/env bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Applying migrations..."
python manage.py migrate

echo "Creating/updating admin..."
python create_admin.py

echo "Build completed successfully."

# 👇 ADD THIS TEMPORARY SNIPPET HERE TO REPAIR YOUR PRODUCTION DATA
echo "Syncing modeltranslation fallback data..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from api.models import Project
for p in Project.objects.all():
    if not p.title_en or p.title_en == '':
        p.title_en = p.title
    if not p.title_de or p.title_de == '':
        p.title_de = p.title
    p.save()
print('Production project data successfully synced!')
"

echo "Creating/updating admin..."
python create_admin.py

echo "Build completed successfully."