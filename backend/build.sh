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

# Sync modeltranslation fallback data using raw database values
echo "Syncing modeltranslation fallback data..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from api.models import Project
for p in Project.objects.all():
    # p.__dict__['title'] bypasses modeltranslation proxy to get the real original data
    original_title = p.__dict__.get('title')
    original_description = p.__dict__.get('description')
    original_content = p.__dict__.get('content')
    
    if original_title:
        if not p.title_en: p.title_en = original_title
        if not p.title_de: p.title_de = original_title
        
    if original_description:
        if not p.description_en: p.description_en = original_description
        if not p.description_de: p.description_de = original_description

    if original_content:
        if not p.content_en: p.content_en = original_content
        if not p.content_de: p.content_de = original_content
        
    p.save()
print('Production project data successfully synchronized from raw values!')
"

echo "Creating/updating admin..."
python create_admin.py

echo "Build completed successfully."