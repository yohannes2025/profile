import os
import django

# Updated from 'your_project_name.settings' to 'config.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

# Guard clause: If you forgot to set the password in Render, don't try to create a broken user
if not password:
    print("ERROR: DJANGO_SUPERUSER_PASSWORD environment variable is missing!")
    exit(0) # exit(0) prevents Render from crashing the build if the variable is missing

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully!")
else:
    print(f"Superuser '{username}' already exists. Skipping.")