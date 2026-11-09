"""Small SEO fixes from the 9 Nov 2026 audit. Safe to re-run.

- Home links point at / (the canonical homepage), not the duplicate /home/ copy.
- Logo images get alt text.
- Shorter titles (under 60 characters) and fuller meta descriptions (140 to 160) where they were off.
- Stock images over 150KB are recompressed.
Run: python3 scripts/seo_fixes.py
"""
import glob, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

TITLES = {
    "boiler-conversions/index.html": "Boiler Conversions in Bishop's Stortford | Flotech",
    "boiler-servicing-repairs/index.html": "Boiler Servicing & Repairs in Bishop's Stortford | Flotech",
}
DESCS = {
    "blog/index.html": "News, tips and advice from Flotech Heating and Plumbing: boiler servicing, new boilers, water softeners and bathrooms in Bishop's Stortford and Dunmow.",
    "gas-boiler-installations/index.html": "Gas boiler installation in Bishop's Stortford by Gas Safe engineers. Ideal and Vaillant combi, system and regular boilers, honest advice and free quotes.",
}
ALTS = {
    "Untitled-design-2026-05-18T132711.077": "Flotech engineer servicing a wall-mounted gas boiler",
    "images-7-2": "Ideal Heating logo",
    "whbc20_309414_02": "Modern fitted kitchen",
    "Untitled-design-2026-07-23T214212.121": "Flotech engineer power flushing a radiator",
    "Untitled-design-2026-07-23T214341.962": "Flotech engineer checking an unvented hot water cylinder",
    "elegant-minimalist-table-with-pampas-grass-and-rad": "Column radiator in a dining room",
    "Logic_MAX_Combi2_FO": "Ideal Logic Max combi boiler",
    "Vogue_MAX_Combi_FO": "Ideal Vogue Max combi boiler",
}
LOGOS = ["Flotech-Logo-04-scaled-e1778596830187-1", "Untitled-design-2026-05-12T160838.413-e1784812198268"]


def set_meta(t, title=None, desc=None):
    if title:
        e = html.escape(title, quote=True)
        t = re.sub(r"<title>.*?</title>", f"<title>{e}</title>", t, count=1, flags=re.S)
        t = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e, t)
        t = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + e, t)
    if desc:
        d = html.escape(desc, quote=True)
        for k in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            t = re.sub(r'(<meta ' + k + r' content=")[^"]*', lambda m: m.group(1) + d, t)
    return t


def main():
    n = 0
    for f in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
        rel = os.path.relpath(f, SITE)
        if rel.startswith(("wp-", "_finance-preview")):
            continue
        s = open(f, encoding="utf-8").read()
        t = s.replace('href="/home/"', 'href="/"')
        for logo in LOGOS:
            t = re.sub(r'(<img\b[^>]*' + re.escape(logo) + r'[^>]*?)\salt=""', r'\1 alt="Flotech Heating and Plumbing"', t)
        for key, alt in ALTS.items():
            t = re.sub(r'(<img\b[^>]*' + re.escape(key) + r'[^>]*?)\salt=""', lambda m: m.group(1) + f' alt="{alt}"', t)
        t = set_meta(t, TITLES.get(rel), DESCS.get(rel))
        if t != s:
            open(f, "w", encoding="utf-8").write(t)
            n += 1
    print(n, "pages")
    try:
        from PIL import Image
    except ImportError:
        return
    for f in glob.glob(os.path.join(SITE, "wp-content", "uploads", "**", "*.webp"), recursive=True):
        if os.path.getsize(f) > 150 * 1024:
            im = Image.open(f)
            if im.width > 1920:
                im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
            for q in (80, 74, 68):
                im.save(f + ".tmp", "WEBP", quality=q, method=6)
                if os.path.getsize(f + ".tmp") <= 150 * 1024:
                    break
            os.replace(f + ".tmp", f)
            print("compressed", os.path.relpath(f, SITE), os.path.getsize(f) // 1024, "KB")

if __name__ == "__main__":
    main()
