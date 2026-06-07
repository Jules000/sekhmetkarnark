#!/bin/bash
set -e

PORT="${PORT:-8000}"
echo "Starting gunicorn on port $PORT..."

python manage.py migrate --noinput --settings=config.settings.production

python manage.py collectstatic --noinput --settings=config.settings.production || true

exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --worker-class gthread \
    --threads 2 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile -
