import base64, json, os

media_root = os.path.join(os.path.dirname(__file__), '..', 'media')
images = {
    'neroli-imperial': ('shop/products/2026/06/mareefe-cosmetic-oil-3164684_1920.webp', 'shop.Product', 'main_image'),
    'ashwagandha-sombre': ('shop/products/2026/06/monicore-essential-oils-1851027_1920.webp', 'shop.Product', 'main_image'),
    'moringa-solaire': ('shop/products/2026/06/ninetechno-herbal-tea-7111625_1920.webp', 'shop.Product', 'main_image'),
    'songe-dosiris': ('shop/products/2026/06/nutriscanapp-moringa-9872407_1920.webp', 'shop.Product', 'main_image'),
    'quintessence-dhematite': ('shop/products/2026/06/u_ocknzmxfrt-essential-oils-8373959_1920.webp', 'shop.Product', 'main_image'),
}

hero_images = {
    'home': ('hero/2026/06/pexels-n-voitkevich-7526024.webp', 'core.HeroSlide'),
    'login': ('hero/2026/06/pexels-n-voitkevich-7526024.webp', 'core.HeroSlide'),
}

blog_images = {
    'le-pouvoir-adaptogene-de-lashwagandha': ('blog/featured/2026/06/Gemini_Generated_Image_rkmqb3rkmqb3rkmq.webp', 'blog.Article'),
    'protocoles-de-detoxification-hepatique-douce': ('blog/featured/2026/06/pexels-n-voitkevich-7615465.webp', 'blog.Article'),
    'microbiote-et-axe-intestin-cerveau': ('blog/featured/2026/06/wooden-spoons-with-plants-flat-lay.webp', 'blog.Article'),
    'les-5-piliers-dune-digestion-optimale': ('blog/featured/2026/06/woman-drinking-healthy-tea.webp', 'blog.Article'),
    'jeune-intermittent-mythes-et-realites-cliniques': ('blog/featured/2026/06/nutriscanapp-moringa-9872407_1920.webp', 'blog.Article'),
    'gemmotherapie-le-pouvoir-des-bourgeons': ('blog/featured/2026/06/pexels-n-voitkevich-7615465.webp', 'blog.Article'),
    'aromatherapie-scientifique': ('blog/featured/2026/06/pexels-n-voitkevich-7615465_ed1vFHL.webp', 'blog.Article'),
    'le-rituel-du-matin': ('blog/featured/2026/06/ninetechno-herbal-tea-7111625_1920.webp', 'blog.Article'),
}

entries = []

for slug, (rel_path, model, field) in images.items():
    full_path = os.path.join(media_root, rel_path)
    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        entries.append({'model': model, 'lookup': 'slug', 'value': slug, 'field': field, 'data': b64, 'ext': 'webp'})
        print(f'  Packed product {slug}: {len(b64)} bytes')
    else:
        print(f'  MISSING product image: {full_path}')

for slug, (rel_path, model) in hero_images.items():
    full_path = os.path.join(media_root, rel_path)
    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        entries.append({'model': model, 'lookup': 'page', 'value': slug, 'field': 'image', 'data': b64, 'ext': 'webp'})
        print(f'  Packed hero {slug}: {len(b64)} bytes')
    else:
        print(f'  MISSING hero image: {full_path}')

for slug, (rel_path, model) in blog_images.items():
    full_path = os.path.join(media_root, rel_path)
    if os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        entries.append({'model': model, 'lookup': 'slug', 'value': slug, 'field': 'featured_image', 'data': b64, 'ext': 'webp'})
        print(f'  Packed article {slug}: {len(b64)} bytes')
    else:
        print(f'  MISSING article image: {full_path}')

output_path = os.path.join(os.path.dirname(__file__), '..', 'railway_import_images.py')
with open(output_path, 'w') as f:
    f.write('import os, sys, base64\n')
    f.write("os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')\n")
    f.write('import django; django.setup()\n')
    f.write('from django.core.files.base import ContentFile\n')
    f.write('from django.apps import apps\n\n')
    f.write(f'entries = {json.dumps(entries)}\n\n')
    f.write('for entry in entries:\n')
    f.write('    try:\n')
    f.write('        model = apps.get_model(entry["model"])\n')
    f.write('        obj = model.objects.get(**{entry["lookup"]: entry["value"]})\n')
    f.write('        filename = f"{entry["value"]}_{entry["field"]}.{entry["ext"]}"\n')
    f.write('        getattr(obj, entry["field"]).save(\n')
    f.write('            filename,\n')
    f.write('            ContentFile(base64.b64decode(entry["data"]), name=filename),\n')
    f.write('            save=True,\n')
    f.write('        )\n')
    f.write('        print(f"OK: {entry["model"]}#{entry["value"]}")\n')
    f.write('    except Exception as e:\n')
    f.write('        print(f"FAIL: {entry["model"]}#{entry["value"]}: {e}")\n')
    f.write('print("All done!")\n')

size = os.path.getsize(output_path)
print(f'\nScript generated: {output_path}')
print(f'Script size: {size/1024:.1f} KB')
print(f'Total entries: {len(entries)}')
