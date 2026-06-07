#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput --settings=config.settings.production

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=config.settings.production || true

PORT="${PORT:-${RAILWAY_TCP_APPLICATION_PORT:-8000}}"
echo "Starting gunicorn on port $PORT..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 4 \
    --worker-class gthread \
    --threads 2 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile -
