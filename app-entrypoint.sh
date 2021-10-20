#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --clear

echo "Starting app in DEBUG=$DEBUG"
gunicorn -b 0.0.0.0 -p 8000 config.wsgi:application
