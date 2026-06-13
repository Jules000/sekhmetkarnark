#!/usr/bin/env bash
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput --clear

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

echo "==> Seeding initial data..."
python manage.py seed_data 2>/dev/null || echo "  → Seed skipped"

echo "==> Importing product images..."
python manage.py import_media --model shop.Product --field main_image --lookup slug --value neroli-imperial --path /app/media/shop/products/2026/06/mareefe-cosmetic-oil-3164684_1920.webp 2>&1 || true
python manage.py import_media --model shop.Product --field main_image --lookup slug --value ashwagandha-sombre --path /app/media/shop/products/2026/06/monicore-essential-oils-1851027_1920.webp 2>&1 || true
python manage.py import_media --model shop.Product --field main_image --lookup slug --value moringa-solaire --path /app/media/shop/products/2026/06/ninetechno-herbal-tea-7111625_1920.webp 2>&1 || true
python manage.py import_media --model shop.Product --field main_image --lookup slug --value songe-dosiris --path /app/media/shop/products/2026/06/nutriscanapp-moringa-9872407_1920.webp 2>&1 || true
python manage.py import_media --model shop.Product --field main_image --lookup slug --value quintessence-dhematite --path /app/media/shop/products/2026/06/u_ocknzmxfrt-essential-oils-8373959_1920.webp 2>&1 || true

echo "==> Starting Gunicorn..."
exec "$@"
