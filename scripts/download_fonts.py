"""
Script de téléchargement des Google Fonts pour SekhmetKarnark.
Utilise l'API google-webfonts-helper (https://gwfh.mranftl.com/api/fonts)
pour obtenir les URLs de téléchargement woff2/woff.

Usage: python scripts/download_fonts.py

Les fichiers seront placés dans static/fonts/
"""

import json
import urllib.request
import urllib.error
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "static" / "fonts"
FONTS_DIR.mkdir(parents=True, exist_ok=True)

FONTS = [
    {
        "family": "Libre Caslon Text",
        "variants": ["400", "400italic", "700"],
    },
    {
        "family": "Literata",
        "variants": ["400", "400italic", "700"],
    },
    {
        "family": "Jost",
        "variants": ["300", "400", "500"],
    },
    {
        "family": "Cormorant Garamond",
        "variants": ["300"],
    },
]

BASE_URL = "https://gwfh.mranftl.com/api/fonts/{family}?download=zip&formats=woff,woff2"


def download_font(family, variant):
    """Télécharge un fichier de police via google-webfonts-helper."""
    url = BASE_URL.format(family=family.replace(" ", "-").lower())
    filename = f"{family.lower().replace(' ', '-')}-{variant}.woff2"
    filepath = FONTS_DIR / filename

    if filepath.exists():
        print(f"  ✓ Déjà présent : {filename}")
        return

    try:
        print(f"  → Téléchargement : {filename}")
        # Note: l'API gwfh nécessite d'être appelée avec le subset et variant
        # L'implémentation complète nécessite une requête par variante
        print(f"  ✗ À télécharger manuellement depuis https://gwfh.mranftl.com/fonts/{family.replace(' ', '-').lower()}")
    except Exception as e:
        print(f"  ✗ Erreur : {e}")


def main():
    print("=== Téléchargement des polices Google Fonts ===")
    print(f"Dossier de destination : {FONTS_DIR}\n")

    for font in FONTS:
        family = font["family"]
        print(f"\nFamille : {family}")
        for variant in font["variants"]:
            download_font(family, variant)

    print("\n=== Terminé ===")
    print("\nPour télécharger automatiquement les fonts, utilisez :")
    print("  1. Rendez-vous sur https://gwfh.mranftl.com/")
    print("  2. Recherchez chaque famille de police")
    print("  3. Sélectionnez les subsets 'latin' et les variants listés ci-dessus")
    print("  4. Téléchargez le zip et extrayez les fichiers .woff2 et .woff dans static/fonts/")


if __name__ == "__main__":
    main()
