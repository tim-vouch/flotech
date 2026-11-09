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
.elementor-element-48963d4 > .e-con-inner{display:flex !important;flex-wrap:nowrap !important;align-items:center !important;gap:8px !important}
.elementor-element-48963d4 .elementor-element-47db4ff{order:1;--width:auto !important;width:auto !important;margin-right:auto !important}
.elementor-element-48963d4 .elementor-element-2f259d3,.elementor-element-48963d4 .elementor-element-08aa765{display:contents !important}
.elementor-element-48963d4 .ftm-call{order:2}
.elementor-element-48963d4 .elementor-element-4a79251{order:3;--width:auto !important;width:auto !important;flex:none !important}
.elementor-element-48963d4 .ftm-burger{order:4;flex:none}
.elementor-element-48963d4 .ft-book-btn .elementor-button{padding:0 14px !important;height:46px;display:inline-flex !important;align-items:center;font-size:15px !important;white-space:nowrap}
.elementor-element-48963d4 .ft-book-btn .elementor-button-icon{display:none !important}
.ftm-call{display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:12px;border:2px solid #9B51FF;color:#7A3FE0 !important;background:#fff;flex:none}
.ftm-call svg{width:20px;height:20px}
}
@media (max-width:400px){
.elementor-element-48963d4 > .e-con-inner{gap:6px !important}
.elementor-element-48963d4 .elementor-element-5ca6e8a img{width:56px !important}
.elementor-element-48963d4 .ftm-call,.elementor-element-48963d4 .ftm-burger{width:42px !important;height:42px !important}
.elementor-element-48963d4 .ft-book-btn .elementor-button{height:42px;padding:0 12px !important;font-size:14px !important}
}
@media (max-width:359px){
.elementor-element-c8b0c78 .elementor-element-d0c918a{display:none !important}
.elementor-element-48963d4 .elementor-element-5ca6e8a img{width:48px !important}
.elementor-element-48963d4 .ftm-call,.elementor-element-48963d4 .ftm-burger{width:40px !important;height:40px !important}
.elementor-element-48963d4 .ft-book-btn .elementor-button{height:40px;padding:0 10px !important;font-size:13px !important}
}
a[x-apple-data-detectors]{color:inherit !important;text-decoration:none !important}
.ft-phone-box .elementor-icon-box-description a{color:inherit !important;text-decoration:none !important}
</style>"""
META = '<meta name="format-detection" content="telephone=no">'
NUM_OLD = """<p class="elementor-icon-box-description">
						01279 598 972					</p>"""
NUM_NEW = """<p class="elementor-icon-box-description"><a href="tel:+441279598972">01279 598 972</a></p>"""

CALL = ('<a href="tel:+441279598972" class="ftm-call" aria-label="Call 01279 598 972"><svg viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 '
        '19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 '
        '2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg></a>')
BURGER = '<button type="button" class="ftm-burger"'


def put_css(t, css):
    """Insert or replace a <style id=...> block in place, so re-running keeps the head order stable."""
    sid = re.search(r'<style id="([^"]+)"', css).group(1)
    m = re.search(r'<style id="' + re.escape(sid) + r'">.*?</style>\n?', t, re.S)
    if m:
        return t[:m.start()] + css + "\n" + t[m.end():]
    return t.replace("</head>", css + "\n</head>", 1)


def update(t):
    t = t.replace(CALL, "")
    if "elementor-element-48963d4" not in t:
        return t
    t = t.replace(BURGER, CALL + BURGER, 1)
    t = t.replace(NUM_OLD, NUM_NEW)
    # Phone header button reads "Get Free Quote" (the desktop one already does)
    i = t.find('elementor-element-4a79251')
    if i > 0:
        j = t.find('<span class="elementor-button-text">Get Quote</span>', i, i + 2000)
        if j > 0:
            t = t[:j] + '<span class="elementor-button-text">Get Free Quote</span>' + t[j + len('<span class="elementor-button-text">Get Quote</span>'):]
    if META not in t:
        t = t.replace('<meta name="viewport"', META + "\n" + '<meta name="viewport"', 1)
    return put_css(t, CSS)


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
