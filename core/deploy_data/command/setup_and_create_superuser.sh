#!/bin/bash

# Install Python packages from requirements.txt
cd ..
cd ..
pip install -r ./requirements/base.txt

# Create staticfiles directory
mkdir staticfiles

# Collect static files
python manage.py collectstatic --noinput

# Upgrade setuptools
pip install --upgrade setuptools

# Apply database migrations
python manage.py migrate

# Create a superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('sherzamon', '', 'sherzAmon2001A')" | python manage.py shell

cd deploy/command
