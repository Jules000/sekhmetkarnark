"""Check seeded data in the database."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.local"

import django
django.setup()

from apps.shop.models import Product, Category as ShopCategory
from apps.blog.models import Article, Category as BlogCategory, Tag

print("=== SHOP CATEGORIES ===")
for c in ShopCategory.objects.all():
    print(f"  - {c.name}")

print("\n=== PRODUCTS ===")
for p in Product.objects.filter(is_active=True):
    print(f"  - {p.name}: {p.price} EUR (stock: {p.stock_quantity})")
    print(f"    Categorie: {p.category.name if p.category else 'Aucune'}")

print("\n=== BLOG CATEGORIES ===")
for c in BlogCategory.objects.all():
    print(f"  - {c.name}")

print("\n=== TAGS ===")
for t in Tag.objects.all():
    print(f"  - {t.name}")

print("\n=== ARTICLES ===")
for a in Article.objects.filter(status="published"):
    tags = ", ".join(t.name for t in a.tags.all())
    print(f"  - {a.title}")
    print(f"    Categorie: {a.category.name if a.category else 'Aucune'}, Tags: [{tags}], {a.reading_time} min")

print("\nDone!")
