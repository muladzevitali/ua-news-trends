#!/bin/bash

python manage.py makemigrations
python manage.py migrate

echo "Starting app in DEBUG=$DEBUG"
celery -A config worker -B -S django -l info
