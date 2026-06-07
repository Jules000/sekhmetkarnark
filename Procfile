release: python manage.py migrate --noinput --settings=config.settings.production
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --worker-class gthread --threads 2 --timeout 120 --max-requests 1000 --max-requests-jitter 50
worker: celery -A config worker -l info --concurrency 2
beat: celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
