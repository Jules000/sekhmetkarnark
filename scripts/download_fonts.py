"""
Télécharge les Google Fonts pour SekhmetKarnark depuis Google Fonts API CSS2.
Usage: python scripts/download_fonts.py
"""

import re
import urllib.request
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "static" / "fonts"
FONTS_DIR.mkdir(parents=True, exist_ok=True)

FONTS_CSS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Jost:wght@300;400;500&"
    "family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&"
    "family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,700;1,7..72,400&"
    "family=Cormorant+Garamond:wght@300&"
    "family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&"
    "display=swap"
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def download_file(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as r:
        data = r.read()
    dest.write_bytes(data)
    return len(data)


def main():
    print("=== Téléchargement des polices Google Fonts ===\n")

    req = urllib.request.Request(FONTS_CSS_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as r:
        css_content = r.read().decode("utf-8")

    urls = re.findall(r"url\((https://[^)]+)\)", css_content)
    print(f"  Trouvé {len(urls)} fichiers font\n")

    for url in urls:
        woff2_match = re.search(r"/([^/]+\.woff2)", url)
        if woff2_match:
            filename = woff2_match.group(1)
        else:
            filename = url.split("/")[-1].split("?")[0]

        dest = FONTS_DIR / filename
        if dest.exists():
            print(f"  ✓ Déjà présent : {filename}")
            continue

        try:
            size = download_file(url, dest)
            print(f"  ✓ Téléchargé : {filename} ({size // 1024} KB)")
        except Exception as e:
            print(f"  ✗ Échec : {filename} — {e}")

    print(f"\n✓ Terminé ! {len(urls)} fichiers dans {FONTS_DIR}")


if __name__ == "__main__":
    main()
