import base64, json, os, sys
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.models import FileField, ImageField


class Command(BaseCommand):
    help = "Importer des images depuis des fichiers locaux vers les modeles"

    def add_arguments(self, parser):
        parser.add_argument("manifest", nargs="?", help="Fichier JSON contenant le mapping images-modeles")
        parser.add_argument("--model", help="Modele cible (ex: shop.Product, blog.Article, core.HeroSlide)")
        parser.add_argument("--field", default="main_image", help="Champ image du modele")
        parser.add_argument("--lookup", default="slug", help="Champ de recherche (slug, id, name)")
        parser.add_argument("--value", help="Valeur du champ lookup")
        parser.add_argument("--path", help="Chemin du fichier image local")
        parser.add_argument("--inline", help="Donnees image en base64 inline (data:image/...;base64,...)")

    def handle(self, *args, **options):
        if options.get("inline") and options.get("model") and options.get("value"):
            return self._import_inline(options)
        if options.get("manifest"):
            return self._import_manifest(options["manifest"])
        self.print_help("manage.py", "import_media")
        self.stdout.write(self.style.ERROR("Utilisez --manifest ou --model --value --path --field"))

    def _import_inline(self, options):
        model_path = options["model"]
        field_name = options["field"]
        lookup_field = options.get("lookup", "slug")
        lookup_value = options["value"]
        image_data = options["inline"]

        model = self._get_model(model_path)
        if not model:
            return
        try:
            obj = model.objects.get(**{lookup_field: lookup_value})
        except model.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Objet {lookup_field}={lookup_value} introuvable dans {model_path}"))
            return

        if image_data.startswith("data:"):
            fmt, data = image_data.split(";base64,", 1)
            ext = fmt.split("/")[-1] if "/" in fmt else "webp"
            fmt = ext
        else:
            data = image_data
            ext = "webp"

        filename = f"{lookup_value}_{field_name}.{ext}"
        file_content = ContentFile(base64.b64decode(data), name=filename)
        getattr(obj, field_name).save(filename, file_content, save=True)
        self.stdout.write(self.style.SUCCESS(f"Image importee: {model_path}#{obj.pk} ({filename})"))

    def _import_manifest(self, manifest_path):
        if not os.path.exists(manifest_path):
            self.stdout.write(self.style.ERROR(f"Fichier manifeste introuvable: {manifest_path}"))
            return
        with open(manifest_path) as f:
            manifest = json.load(f)
        for entry in manifest:
            self._import_entry(entry)

    def _import_entry(self, entry):
        model = self._get_model(entry["model"])
        if not model:
            return
        try:
            obj = model.objects.get(**{entry.get("lookup", "slug"): entry["value"]})
        except model.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"  - {entry['model']} {entry.get('lookup','slug')}={entry['value']}: introuvable"))
            return
        path = entry["path"]
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f"  - {entry['model']}#{obj.pk}: fichier {path} introuvable"))
            return
        field_name = entry.get("field", "main_image")
        with open(path, "rb") as f:
            filename = os.path.basename(path)
            getattr(obj, field_name).save(filename, ContentFile(f.read()), save=True)
        self.stdout.write(self.style.SUCCESS(f"  - {entry['model']}#{obj.pk}: {path} -> {field_name}"))

    def _get_model(self, model_path):
        from django.apps import apps
        try:
            return apps.get_model(model_path)
        except LookupError:
            self.stdout.write(self.style.ERROR(f"Modele introuvable: {model_path}"))
            return None
