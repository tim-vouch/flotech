"""Service areas: one list, used everywhere on the site.

Run: python3 scripts/areas.py   (safe to re-run; edits site/ in place)
Updates the homepage/About/Power Flushing area list, the area chips on the boiler
pages, the schema areaServed, the "Areas" dropdown in the desktop menu, the "Areas"
group in the mobile menu, and the "Areas we cover" band in the footer.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

AREAS = ["Bishop's Stortford", "Sawbridgeworth", "Dunmow", "Takeley", "Stansted", "Saffron Walden",
         "Harlow", "Chelmsford", "Cambridge", "Hertfordshire", "Essex"]

SLUGS = {"Bishop's Stortford": "bishops-stortford", "Sawbridgeworth": "sawbridgeworth", "Dunmow": "dunmow", "Takeley": "takeley",
         "Stansted": "stansted", "Saffron Walden": "saffron-walden", "Harlow": "harlow", "Chelmsford": "chelmsford",
         "Cambridge": "cambridge", "Hertfordshire": "#hertfordshire", "Essex": "#essex"}


def href(a):
    s = SLUGS[a]
    return "/areas/" + (s if s.startswith("#") else s + "/")


def link(a, inner):
    return f'<a href="{href(a)}">{inner}</a>'


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIN = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>'
       '<circle cx="12" cy="10" r="3"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>')

CSS = """<style id="ft-areas-css">
.ft-nav .ft-mega.ft-mega--areas{width:660px}
.ft-areas-mega{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:4px 12px}
.ft-areas-mega a{display:flex;align-items:center;gap:8px;padding:10px 12px;border-radius:10px;font-family:'Urbanist',sans-serif;font-size:15px;font-weight:600;color:#0A0A0A;text-decoration:none;transition:background .2s}
.ft-areas-mega a:hover{background:#F4F4F4;color:#9B51FF}
.ft-areas-mega li svg{color:#9B51FF;flex-shrink:0}
.ft-mobile__sub.ft-mobile__areas{display:grid;grid-template-columns:1fr 1fr;column-gap:12px}
.ftm-areas{list-style:none;margin:0;padding:4px 0 8px;display:grid;grid-template-columns:1fr 1fr;gap:4px 10px}
.ftm-areas a{display:flex;align-items:center;gap:8px;padding:9px 4px;font-family:'Urbanist',sans-serif;font-size:15px;font-weight:500;color:#4A4A4A !important;text-decoration:none !important}
.ftm-areas li svg{color:#9B51FF;flex-shrink:0}
.ft-footer-areas{background:#FAFAFA;padding:0 32px 36px}
.ft-footer-areas__inner{max-width:1280px;margin:0 auto;padding-top:28px;border-top:1px solid #E5E5E5;text-align:center}
.ft-footer-areas h2{margin:0 0 14px;font-family:'Urbanist',sans-serif;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:#0A0A0A}
.ft-footer-areas ul{list-style:none;margin:0 auto;max-width:980px;padding:0;display:flex;flex-wrap:wrap;justify-content:center;gap:8px 22px}
.ft-footer-areas li a{display:flex;align-items:center;gap:6px;font-family:'Urbanist',sans-serif;font-size:15px;color:#4A4A4A;text-decoration:none}
.ft-footer-areas li a:hover{color:#9B51FF}
.ft-areas-list a{color:inherit;text-decoration:none}
.ft-areas-list a:hover{text-decoration:underline;text-underline-offset:3px}
.fx-areas li a{color:inherit;text-decoration:none;display:inline-flex;align-items:center;gap:6px}
.fx-areas li:hover{border-color:#9B51FF}
.ft-footer-areas li svg{color:#9B51FF}
.ft-mega__btns{display:flex;gap:10px;flex-wrap:nowrap;flex-shrink:0}
.ft-mega--areas .ft-mega__footer-text{flex:1;min-width:0}
.ft-nav .ft-mega__cta.ft-mega__cta--ghost{background:#fff;color:#7A3FE0;box-shadow:inset 0 0 0 2px #9B51FF}
.ft-nav .ft-mega__cta.ft-mega__cta--ghost:hover{background:#F4EEFF}
.ft-mega--areas .ft-mega__cta{display:inline-flex;align-items:center;gap:6px;white-space:nowrap}
.ft-mobile__sub.ft-mobile__areas .ft-areas-all{grid-column:1/-1}
.ft-mobile__sub.ft-mobile__areas .ft-areas-all a{display:inline-flex !important;align-items:center;gap:6px;color:#7A3FE0 !important;font-weight:700 !important}
.ftm-areas-all{display:flex !important;align-items:center;justify-content:center;gap:6px;margin:4px 0 10px;padding:13px 16px;border-radius:12px;border:2px solid #9B51FF;color:#7A3FE0 !important;font-family:'Urbanist',sans-serif;font-weight:700;font-size:15px;text-decoration:none !important}
.ft-footer-areas .ft-footer-areas__all{display:inline-flex;align-items:center;gap:6px;margin-top:16px;font-family:'Urbanist',sans-serif;font-weight:700;font-size:15px;color:#7A3FE0 !important;text-decoration:none}
.ft-footer-areas__all:hover{text-decoration:underline;text-underline-offset:3px}
@media (max-width:767px){.ft-footer-areas{padding:0 20px 28px}}
</style>"""


def desktop_item():
    items = "".join(f"<li>{link(a, PIN + a)}</li>" for a in AREAS)
    return (
        '\n    <li class="ft-nav__item ft-nav__item--mega ft-nav__item--areas">\n'
        '      <a href="/areas/" class="ft-nav__link ft-nav__link--has-mega" aria-haspopup="true" aria-expanded="false">\n'
        '        Areas\n        CHEV\n      </a>\n'
        '      <div class="ft-mega ft-mega--areas">\n'
        f'        <ul class="ft-areas-mega">{items}</ul>\n'
        '        <div class="ft-mega__footer">\n'
        '          <div class="ft-mega__footer-text"><strong>Not sure if we cover you?</strong><span>Call 01279 598 972 or ask for a free quote.</span></div>\n'
        '          <div class="ft-mega__btns">'
        f'<a href="/areas/" class="ft-mega__cta ft-mega__cta--ghost">All Areas We Cover {ARROW}</a>'
        f'<a href="/contact/" class="ft-mega__cta">Get a Quote {ARROW}</a></div>\n'
        '        </div>\n      </div>\n    </li>')


def mobile_group():
    items = "".join(f"<li>{link(a, a)}</li>" for a in AREAS)
    return (
        '\n      <li class="ft-mobile__group">\n'
        '        <button type="button" class="ft-mobile__toggle" aria-expanded="false">Areas\n          CHEV\n        </button>\n'
        f'        <ul class="ft-mobile__sub ft-mobile__areas">{items}<li class="ft-areas-all"><a href="/areas/">All Areas We Cover {ARROW}</a></li></ul>\n      </li>')


def phone_group():
    items = "".join(f"<li>{link(a, PIN + a)}</li>" for a in AREAS)
    return (
        '\n      <li class="ftm-group ftm-group--areas">\n'
        '        <button type="button" class="ftm-toggle" aria-expanded="false">Areas\n          CHEV\n        </button>\n'
        f'        <div class="ftm-sub"><div class="ftm-sub__inner"><ul class="ftm-areas">{items}</ul><a href="/areas/" class="ftm-areas-all">All Areas We Cover {ARROW}</a></div></div>\n      </li>')


TOWNS_ONLY = [a for a in AREAS if not SLUGS[a].startswith("#")]
FOOT_CSS = """<style id="ft-footcol-css">
@media (min-width:1025px){
.elementor-element-1c1907bf{--width:22% !important}
.elementor-element-393059ae{--width:18% !important}
.elementor-element-5990f8be{--width:14% !important}
.elementor-element-5990f8be.ft-col-areas{--width:15% !important}
.elementor-element-1f64f320{--width:20% !important}
}
@media (min-width:768px) and (max-width:1024px){
.elementor-element-393059ae,.elementor-element-5990f8be,.elementor-element-5990f8be.ft-col-areas,.elementor-element-1f64f320{--width:45% !important}
}
</style>"""


def footer_li(href, text, icon):
    return (f'<li class="elementor-icon-list-item"><a href="{href}"><span class="elementor-icon-list-icon">{icon}</span>'
            f'<span class="elementor-icon-list-text">{text}</span></a></li>')


def footer_column(icon):
    items = "".join(footer_li(href(a), a, icon) for a in TOWNS_ONLY) + footer_li("/areas/", "All areas we cover", icon)
    return ('<div class="elementor-element elementor-element-5990f8be ft-col-areas e-con-full e-flex e-con e-child">'
            '<div class="elementor-element elementor-element-20ed6dd1 elementor-widget elementor-widget-heading">'
            '<div class="elementor-heading-title elementor-size-default">AREAS WE COVER</div></div>'
            '<div class="elementor-element elementor-element-94c94b1 elementor-align-start elementor-mobile-align-start '
            'elementor-icon-list--layout-traditional elementor-list-item-link-full_width elementor-widget elementor-widget-icon-list">'
            f'<ul class="elementor-icon-list-items">{items}</ul></div></div>')


def footer_band():
    items = "".join(f"<li>{link(a, PIN + a)}</li>" for a in AREAS)
    return (f'<div class="ft-footer-areas"><div class="ft-footer-areas__inner"><h2>Areas we cover</h2>'
            f'<ul>{items}</ul><a class="ft-footer-areas__all" href="/areas/">All areas we cover {ARROW}</a></div></div>\n')


def update(t, rel):
    # Area lists already on the pages
    def pins(m):
        pin = re.search(r'<span class="ft-area-pin">.*?</span>', m.group(0), re.S).group(0)
        return '<ul class="ft-areas-list">\n' + "".join(f"  <li>{pin}{link(a, a)}</li>\n" for a in AREAS) + "</ul>"
    t = re.sub(r'<ul class="ft-areas-list">.*?</ul>', pins, t, flags=re.S)

    def chips(m):
        pin = re.search(r"<svg.*?</svg>", m.group(2), re.S)
        pin = pin.group(0) if pin else ""
        return m.group(1) + "".join(f"<li>{link(a, pin + a)}</li>" for a in AREAS) + "</ul>"
    t = re.sub(r'(<ul class="fx-areas"[^>]*>)((?:(?!</ul>).)*?)</ul>', chips, t, flags=re.S)
    t = re.sub(r'"areaServed":\s*\[[^\]]*\]',
               lambda m: '"areaServed": ' + json.dumps([{"@type": "Place", "name": a} for a in AREAS]), t)

    # Anchor for the menu link (homepage areas section)
    t = t.replace('data-id="301a73a7" data-element_type="widget"', 'id="areas" data-id="301a73a7" data-element_type="widget"', 1) \
        if 'id="areas"' not in t else t

    # Rebuild menus and footer band from scratch each run
    t = re.sub(r'\n    <li class="ft-nav__item ft-nav__item--mega ft-nav__item--areas">.*?\n    </li>', "", t, flags=re.S)
    t = re.sub(r'\n      <li class="ft-mobile__group">\n        <button type="button" class="ft-mobile__toggle" aria-expanded="false">Areas.*?\n      </li>', "", t, flags=re.S)
    t = re.sub(r'\n      <li class="ftm-group ftm-group--areas">.*?\n      </li>', "", t, flags=re.S)
    t = re.sub(r'<div class="ft-footer-areas">.*?</div></div>\n\t\t', "", t, flags=re.S)
    t = re.sub(r'<style id="ft-areas-css">.*?</style>\n', "", t, flags=re.S)

    chev = re.search(r'Services\s*(<svg.*?</svg>)', t, re.S)
    if chev and '<nav class="ft-nav"' in t:
        c = chev.group(1)
        anchor = '\n    <li><a href="/reviews/" class="ft-nav__link">Testimonials</a></li>'
        if anchor in t:
            t = t.replace(anchor, desktop_item().replace("CHEV", c) + anchor, 1)
        manchor = '\n      <li><a href="/reviews/" class="ft-mobile__link">Testimonials</a></li>'
        mc = re.search(r'ft-mobile__toggle" aria-expanded="false">Services\s*(<svg.*?</svg>)', t, re.S)
        if manchor in t and mc:
            t = t.replace(manchor, mobile_group().replace("CHEV", mc.group(1)) + manchor, 1)
    panchor = '\n      <li><a href="/reviews/" class="ftm-link">Testimonials</a></li>'
    pc = re.search(r'class="ftm-toggle" aria-expanded="false">Services\s*(<svg.*?</svg>)', t, re.S)
    if panchor in t and pc:
        t = t.replace(panchor, phone_group().replace("CHEV", pc.group(1)) + panchor, 1)
    # Footer: an "Areas we cover" column after Quick Links, and Terms & Conditions in Quick Links
    t = re.sub(r'<div class="elementor-element elementor-element-5990f8be ft-col-areas .*?</ul></div></div>', "", t, flags=re.S)
    t = re.sub(r'<style id="ft-footcol-css">.*?</style>\n', "", t, flags=re.S)
    q = t.find('<div class="elementor-element elementor-element-5990f8be e-con-full')
    if q >= 0:
        from finance_fix import balanced_div
        e = balanced_div(t, q)
        col = t[q:e]
        icon = re.search(r'<span class="elementor-icon-list-icon">\s*(<svg.*?</svg>)', col, re.S).group(1)
        if 'href="/terms-and-conditions/"' not in col:
            col2 = re.sub(r'(<a href="/contact/">(?:(?!</li>).)*?</li>)', lambda m: m.group(1) + footer_li("/terms-and-conditions/", "Terms &amp; Conditions", icon), col, count=1, flags=re.S)
            t = t[:q] + col2 + t[e:]
            e = q + len(col2)
        t = t[:e] + footer_column(icon) + t[e:]
        t = t.replace("</head>", FOOT_CSS + "\n</head>", 1)
    if "</head>" in t and ("ft-nav__item--areas" in t or "ft-footer-areas" in t):
        t = t.replace("</head>", CSS + "\n</head>", 1)
    return t


def main():
    changed = []
    for f in sorted(glob.glob(os.path.join(ROOT, "site", "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, os.path.join(ROOT, "site"))
        if rel.startswith(("_finance-preview", "wp-")):
            continue
        t = open(f, encoding="utf-8").read()
        n = update(t, rel)
        if n != t:
            open(f, "w", encoding="utf-8").write(n)
            changed.append(rel)
    print(len(changed), "pages:", ", ".join(changed))


if __name__ == "__main__":
    main()
