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

# Sync modeltranslation fallback data checking for empty strings
echo "Syncing modeltranslation fallback data..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from api.models import Project

for p in Project.objects.all():
    # Fetch raw fallback values from database layout dictionary
    raw_title = p.__dict__.get('title', '')
    raw_desc = p.__dict__.get('description', '')
    raw_content = p.__dict__.get('content', '')

    # If the language-specific field is missing, empty, or just spaces, copy the raw data
    if not p.title_en or str(p.title_en).strip() == '':
        p.title_en = raw_title
    if not p.title_de or str(p.title_de).strip() == '':
        p.title_de = raw_title

    if not p.description_en or str(p.description_en).strip() == '':
        p.description_en = raw_desc
    if not p.description_de or str(p.description_de).strip() == '':
        p.description_de = raw_desc

    if not p.content_en or str(p.content_en).strip() == '':
        p.content_en = raw_content
    if not p.content_de or str(p.content_de).strip() == '':
        p.content_de = raw_content

    p.save()
print('Production language mappings successfully overwritten!')
"

echo "Creating/updating admin..."
python create_admin.py

echo "Build completed successfully."