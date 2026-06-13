import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

import django
django.setup()

from django.core.files import File
from apps.shop.models import Product

media_root = '/app/media'
files = {
    'neroli-imperial': 'shop/products/2026/06/mareefe-cosmetic-oil-3164684_1920.webp',
    'ashwagandha-sombre': 'shop/products/2026/06/monicore-essential-oils-1851027_1920.webp',
    'moringa-solaire': 'shop/products/2026/06/ninetechno-herbal-tea-7111625_1920.webp',
    'songe-dosiris': 'shop/products/2026/06/nutriscanapp-moringa-9872407_1920.webp',
    'quintessence-dhematite': 'shop/products/2026/06/u_ocknzmxfrt-essential-oils-8373959_1920.webp',
}

for slug, rel_path in files.items():
    full_path = os.path.join(media_root, rel_path)
    try:
        product = Product.objects.get(slug=slug)
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                product.main_image.save(os.path.basename(rel_path), File(f), save=True)
            print(f'OK: {slug}')
        else:
            print(f'MISSING: {full_path}')
    except Product.DoesNotExist:
        print(f'NOT FOUND: {slug}')
print('Done!')
# deployed 2026-06-13 09:36
