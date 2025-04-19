#!/bin/bash

# Run DB migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create a superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model;
import os;
User = get_user_model();
username = os.environ.get('DJANGO_SU_NAME', 'admin');
email = os.environ.get('DJANGO_SU_EMAIL', 'admin@example.com');
password = os.environ.get('DJANGO_SU_PASSWORD', 'adminpassword');
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password);
    print('✅ Superuser created');
else:
    print('ℹ️ Superuser already exists');
"

# Start the Daphne server
daphne -b 0.0.0.0 -p 8000 chat_room.asgi:application
 
