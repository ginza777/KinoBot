#!/bin/sh

python manage.py migrate
gunicorn core.wsgi:application --bind 0.0.0.0:${WEB_PORT} --workers=9
