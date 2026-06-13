#!/usr/bin/env bash
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "==> Seeding initial data..."
python manage.py seed_data --noinput 2>/dev/null || echo "  → Seed data skipped (already exists or not needed)"

echo "==> Creating superuser (if DJANGO_SUPERUSER_PASSWORD is set)..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@sekhmetkarnak.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser \"{username}\" created successfully.')
"

echo "==> Importing media files..."
if [ -f railway_import_images.py ]; then
    python railway_import_images.py 2>/dev/null && echo "  → Media imported" || echo "  → Media import skipped"
fi

echo "==> Starting Gunicorn..."
exec "$@"
