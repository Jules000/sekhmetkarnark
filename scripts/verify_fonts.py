"""Verify all font files referenced in fonts.css exist."""
import re
from pathlib import Path

CSS_PATH = Path(__file__).resolve().parent.parent / "static" / "css" / "fonts.css"
FONTS_DIR = Path(__file__).resolve().parent.parent / "static" / "fonts"

css = CSS_PATH.read_text("utf-8")
files = re.findall(r"\.\./fonts/([^)']+)+", css)
# Clean trailing quotes
files = [f.strip().strip("'").strip('"') for f in files]

existing = [f for f in files if (FONTS_DIR / f).exists()]
missing = [f for f in files if not (FONTS_DIR / f).exists()]

print(f"fonts.css : {len(files)} fichiers references")
print(f"Presents : {len(existing)}")
if missing:
    print(f"MANQUANTS ({len(missing)}) :")
    for m in missing:
        print(f"  - {m}")
else:
    print("TOUS LES FICHIERS SONT PRESENTS !")
