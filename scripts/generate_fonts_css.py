"""Generate fonts.css from Google Fonts — handles ttf and woff2."""
import re
import urllib.request
from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "static" / "fonts"
OUTPUT = Path(__file__).resolve().parent.parent / "static" / "css" / "fonts.css"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

FONT_URLS = {
    "Jost": "https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500&display=swap",
    "Libre Caslon Text": "https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&display=swap",
    "Literata": "https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,700;1,7..72,400&display=swap",
    "Cormorant Garamond": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300&display=swap",
    "Material Symbols Outlined": "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined&display=swap",
}


def parse_css(css):
    """Parse @font-face blocks from CSS."""
    blocks = re.findall(r"@font-face\s*\{([^}]*)\}", css)
    results = []
    for block in blocks:
        props = {}
        for line in block.split(";"):
            line = line.strip()
            if ":" in line:
                parts = line.split(":", 1)
                props[parts[0].strip()] = parts[1].strip()
        if "font-family" in props and "src" in props:
            results.append(props)
    return results


def find_local_file(font_url, font_dir):
    """Find the local file matching a Google Fonts URL."""
    fname = font_url.split("/")[-1].split("?")[0]
    path = font_dir / fname
    if path.exists():
        return fname
    # Try with .woff2 extension instead of .ttf
    if fname.endswith(".ttf"):
        alt = fname.replace(".ttf", ".woff2")
        if (font_dir / alt).exists():
            return alt
    return None


def main():
    lines = []
    lines.append("/* ============================================================")
    lines.append("   Fonts Locales — SekhmetKarnark")
    lines.append("   Servies localement, aucune dependance externe")
    lines.append("   ============================================================ */")
    lines.append("")

    local_files = list(FONTS_DIR.glob("*"))
    print(f"Fichiers dans static/fonts/ : {len(local_files)}")

    count = 0
    missing = []

    for family, css_url in FONT_URLS.items():
        try:
            req = urllib.request.Request(css_url, headers=HEADERS)
            with urllib.request.urlopen(req) as r:
                css = r.read().decode("utf-8")
        except Exception as e:
            lines.append(f"/* Error: {e} */")
            continue

        # Also try with format=woff2
        try:
            url2 = css_url.replace("css2?", "css?") + "&format=woff2"
            req2 = urllib.request.Request(url2, headers=HEADERS)
            with urllib.request.urlopen(req2) as r2:
                css2 = r2.read().decode("utf-8")
        except Exception:
            css2 = ""

        all_css = css + "\n" + css2
        blocks = parse_css(all_css)

        # Deduplicate by (family, style, weight, unicode)
        seen = set()
        unique_blocks = []
        for b in blocks:
            key = (
                b.get("font-family", ""),
                b.get("font-style", ""),
                b.get("font-weight", ""),
                b.get("unicode-range", ""),
            )
            if key not in seen:
                seen.add(key)
                unique_blocks.append(b)

        for props in unique_blocks:
            family_name = props.get("font-family", "").strip().strip("'").strip('"')
            style = props.get("font-style", "normal")
            weight = props.get("font-weight", "400")
            src = props.get("src", "")
            unicode_range = props.get("unicode-range", "U+0000-00FF")

            url_match = re.search(r"url\(([^)]+)\)", src)
            if not url_match:
                continue

            font_url = url_match.group(1)
            local_fname = find_local_file(font_url, FONTS_DIR)

            if local_fname:
                fmt = "woff2" if local_fname.endswith(".woff2") else "truetype"
                lines.append(f"/* {family_name} {style} {weight} */")
                lines.append("@font-face {")
                lines.append(f'  font-family: "{family_name}";')
                lines.append(f"  font-style: {style};")
                lines.append(f"  font-weight: {weight};")
                lines.append(f'  src: url("../fonts/{local_fname}") format("{fmt}");')
                lines.append(f"  unicode-range: {unicode_range};")
                lines.append("  font-display: swap;")
                lines.append("}")
                lines.append("")
                count += 1
            else:
                missing.append(f"{family_name} {weight} {font_url.split('/')[-1]}")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"fonts.css genere : {count} @font-face regles")
    if missing:
        print(f"\nFichiers manquants ({len(missing)}) :")
        for m in missing:
            print(f"  - {m}")
        print("\nAstuce : telechargez les fichiers manquants depuis Google Fonts")
        print("et placez-les dans static/fonts/")


if __name__ == "__main__":
    main()
