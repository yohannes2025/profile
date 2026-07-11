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

echo "--- DIAGNOSTIC: Checking Live Database Rows ---"
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from api.models import Project

projects = Project.objects.all()
print(f'Total projects found: {len(projects)}')

for i, p in enumerate(projects):
    print(f'--- Project Row {i+1} ---')
    print(f'Raw Dict Keys: {list(p.__dict__.keys())}')
    print(f'Raw title field value: {repr(p.__dict__.get(\"title\"))}')
    print(f'Title_en value: {repr(p.title_en)}')
    print(f'Title_de value: {repr(p.title_de)}')
"
echo "-----------------------------------------------"

echo "Creating/updating admin..."
python create_admin.py

echo "Build completed successfully."