"""Phone header that stays on screen while scrolling (like MJ Services): logo, call button, menu and Get Quote.

Run: python3 scripts/mobile_header.py   (safe to re-run; edits every site/**/index.html)
The thin top bar (Call us today + socials) scrolls away; the main row sticks to the top.
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """<style id="ft-sticky-m">
@media (max-width:767px){
header.elementor-location-header{position:-webkit-sticky;position:sticky;top:-60px;z-index:9990}
.elementor-element-48963d4{--padding-top:8px !important;--padding-bottom:8px !important;box-shadow:0 6px 18px rgba(15,10,40,.08)}
.elementor-element-48963d4 .elementor-element-5ca6e8a img{width:64px !important;height:auto !important;max-width:none}
.elementor-element-48963d4 .elementor-element-2f259d3 .elementor-widget-container,.elementor-element-48963d4 .elementor-element-08aa765{display:flex;align-items:center;justify-content:center;gap:10px}
.ftm-call{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:12px;border:2px solid #9B51FF;color:#7A3FE0 !important;background:#fff;flex:none}
.ftm-call svg{width:20px;height:20px}
}
</style>"""

CALL = ('<a href="tel:+441279598972" class="ftm-call" aria-label="Call 01279 598 972"><svg viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 '
        '19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 '
        '2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg></a>')
BURGER = '<button type="button" class="ftm-burger"'


def update(t):
    t = re.sub(r'<style id="ft-sticky-m">.*?</style>\n', "", t, flags=re.S)
    t = t.replace(CALL, "")
    if "elementor-element-48963d4" not in t:
        return t
    t = t.replace(BURGER, CALL + BURGER, 1)
    return t.replace("</head>", CSS + "\n</head>", 1)


def main():
    n = 0
    for f in glob.glob(os.path.join(ROOT, "site", "**", "index.html"), recursive=True):
        if "/wp-" in f or "_finance-preview" in f:
            continue
        s = open(f, encoding="utf-8").read()
        u = update(s)
        if u != s:
            open(f, "w", encoding="utf-8").write(u)
            n += 1
    print(n, "pages")


if __name__ == "__main__":
    main()
