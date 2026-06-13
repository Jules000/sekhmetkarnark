import os, requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.apps import apps

GITHUB_RAW = "https://raw.githubusercontent.com/Jules000/sekhmetkarnark/master/media"

IMAGES = {
    "shop.Product:slug:neroli-imperial:main_image": f"{GITHUB_RAW}/shop/products/2026/06/mareefe-cosmetic-oil-3164684_1920.webp",
    "shop.Product:slug:ashwagandha-sombre:main_image": f"{GITHUB_RAW}/shop/products/2026/06/monicore-essential-oils-1851027_1920.webp",
    "shop.Product:slug:moringa-solaire:main_image": f"{GITHUB_RAW}/shop/products/2026/06/ninetechno-herbal-tea-7111625_1920.webp",
    "shop.Product:slug:songe-dosiris:main_image": f"{GITHUB_RAW}/shop/products/2026/06/nutriscanapp-moringa-9872407_1920.webp",
    "shop.Product:slug:quintessence-dhematite:main_image": f"{GITHUB_RAW}/shop/products/2026/06/u_ocknzmxfrt-essential-oils-8373959_1920.webp",
    "core.HeroSlide:page:home:image": f"{GITHUB_RAW}/hero/2026/06/pexels-n-voitkevich-7526024.webp",
    "core.HeroSlide:page:login:image": f"{GITHUB_RAW}/hero/2026/06/pexels-n-voitkevich-7526024.webp",
    "blog.Article:slug:le-pouvoir-adaptogene-de-lashwagandha:featured_image": f"{GITHUB_RAW}/blog/featured/2026/06/Gemini_Generated_Image_rkmqb3rkmqb3rkmq.webp",
    "blog.Article:slug:protocoles-de-detoxification-hepatique-douce:featured_image": f"{GITHUB_RAW}/blog/featured/2026/06/pexels-n-voitkevich-7615465.webp",
    "blog.Article:slug:microbiote-et-axe-intestin-cerveau:featured_image": f"{GITHUB_RAW}/blog/featured/2026/06/wooden-spoons-with-plants-flat-lay.webp",
    "blog.Article:slug:les-5-piliers-dune-digestion-optimale:featured_image": f"{GITHUB_RAW}/blog/featured/2026/06/woman-drinking-healthy-tea.webp",
    "blog.Article:slug:jeune-intermittent-mythes-et-realites-cliniques:featured_image": f"{GITHUB_RAW}/blog/featured/2026/06/nutriscanapp-moringa-9872407_1920.webp",
    "blog.Article:slug:gemmotherapie-le-pouvoir-des-bourgeons:featured_image": f"{GITHUB_RAW}/blog/featured/2026/06/pexels-n-voitkevich-7615465.webp",
    "blog.Article:slug:aromatherapie-scientifique:featured_image": f"{GITHUB_RAW}/blog/featured/2026/06/pexels-n-voitkevich-7615465_ed1vFHL.webp",
    "blog.Article:slug:le-rituel-du-matin:featured_image": f"{GITHUB_RAW}/blog/featured/2026/06/ninetechno-herbal-tea-7111625_1920.webp",
}

class Command(BaseCommand):
    help = "Download images from GitHub raw and import into models"

    def handle(self, *args, **options):
        for key, url in IMAGES.items():
            parts = key.split(":")
            model_path, lookup, value, field = parts[0], parts[1], parts[2], parts[3]
            try:
                model = apps.get_model(model_path)
                obj = model.objects.get(**{lookup: value})
                if getattr(obj, field):
                    self.stdout.write(f"  - {model_path}#{value}: already has image")
                    continue
                r = requests.get(url, timeout=30)
                if r.status_code == 200:
                    ext = url.split(".")[-1]
                    filename = f"{value}_{field}.{ext}"
                    getattr(obj, field).save(filename, ContentFile(r.content, name=filename), save=True)
                    self.stdout.write(self.style.SUCCESS(f"  OK: {model_path}#{value}"))
                else:
                    self.stdout.write(self.style.WARNING(f"  HTTP {r.status_code}: {url}"))
            except model.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  SKIP: {model_path}#{value} not found"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  FAIL: {model_path}#{value}: {e}"))
