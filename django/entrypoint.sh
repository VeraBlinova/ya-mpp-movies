#!/bin/sh

python manage.py compilemessages -l en -l ru

python manage.py migrate --no-input
python manage.py collectstatic --no-input


gunicorn config.wsgi:application --bind 0.0.0.0:8000 -p 8000 --reload --log-level 'info'

exec "$@" 
