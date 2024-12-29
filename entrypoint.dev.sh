#!/bin/sh

# To update run
pip install --upgrade pip

# Install required packages (change this if needed)
pip install -r requirements/develop.txt

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn core.wsgi:application --bind 0.0.0.0:${WEB_PORT} --workers=9
