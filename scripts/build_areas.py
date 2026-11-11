"""Builds the area pages: /areas/ (hub) and /areas/<slug>/ for each town in scripts/area_content.py.

Run: python3 scripts/build_areas.py && python3 scripts/areas.py
The page shell (head, header, footer, styles) is copied from the combi boiler page, so the menus and
footer stay identical to the rest of the site. Safe to re-run: pages are rebuilt from scratch.
"""
import html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from area_content import TOWNS, GROUPS, PREVIEW_ONLY  # noqa: E402
from finance_fix import STRIP, balanced_div  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
BASE = "https://flotechheating.co.uk"
TEMPLATE = os.path.join(SITE, "combi-boiler-installation", "index.html")
OLD_URL = BASE + "/combi-boiler-installation/"
BY_SLUG = {t["slug"]: t for t in TOWNS}
HEROES = {"combi": ("hero-combi-1600", "hero-combi-800"), "system": ("hero-system-1354", "hero-system-800"),
          "regular": ("hero-regular-1600", "hero-regular-800"), "conversion": ("hero-conversion-1280", "hero-conversion-800")}
REVIEWS = {r["name"]: r for r in json.load(open(os.path.join(ROOT, "data", "google-reviews.json")))}

PIN = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
       'stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>')
PHONE = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 '
         '19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6'
         'l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>')

CSS = """<style id="fx-area">
.fx-nonum .fx-step::before{display:none}
.fx-quote{max-width:780px;margin:28px auto 0;display:grid;gap:18px}
.fx-quote blockquote{margin:0;background:#fff;border:1px solid #EAEAF0;border-radius:18px;padding:28px 30px;text-align:left}
.fx-quote blockquote p{margin:0 0 14px;font-size:17px;line-height:1.65;color:#1A1A1A}
.fx-quote .fx-stars{color:#F5B301;letter-spacing:2px;font-size:18px;margin-bottom:10px}
.fx-quote cite{font-style:normal;font-weight:700;font-size:14.5px;color:#4A4A4A}
.fx-areas.fx-near{justify-content:center}
.fx-areas.fx-near li{padding:0;background:none;border:0}
.fx-areas.fx-near a{display:inline-flex;align-items:center;gap:6px;padding:10px 16px;border-radius:999px;background:#fff;border:1px solid #E6E6EE;font-size:15px;font-weight:600;color:#1A1A1A;text-decoration:none;transition:border-color .2s}
.fx-areas.fx-near a:hover{border-color:#9B51FF}
.fx-areas.fx-near svg{color:#7B35E0}
.fx-group-h{margin:44px 0 0 !important;font-size:22px;font-weight:800;scroll-margin-top:120px}
.fx-group-h:first-of-type{margin-top:28px !important}
.fx-codes{display:grid;gap:18px;max-width:980px;margin:26px auto 0;text-align:left}
.fx-codes h3{margin:0 0 8px;font-size:15px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#4A4A4A}
.fx-codes ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.fx-codes a{display:inline-block;padding:7px 12px;border-radius:999px;background:#fff;border:1px solid #E6E6EE;font-size:14.5px;font-weight:700;color:#1A1A1A;text-decoration:none}
.fx-codes a:hover{border-color:#9B51FF;color:#7A3FE0}
</style>"""

SERVICES = [("/gas-boiler-installations/", "Boiler Installation", "Ideal and Vaillant boilers, professionally fitted"),
            ("/boiler-servicing-repairs/", "Servicing &amp; Repairs", "Annual servicing by Gas Safe engineers"),
            ("/powerflush/", "Power Flushing", "Remove sludge, restore efficiency"),
            ("/unvented-cylinders/", "Unvented Cylinders", "High-pressure mains-fed hot water")]


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def btns():
    return (f'<div class="fx-btns"><a href="/contact/" class="fx-btn fx-btn--primary">Get a Free Quote {ARROW}</a>'
            f'<a href="tel:+441279598972" class="fx-btn fx-btn--ghost">{PHONE} 01279 598 972</a></div>')


def services(town):
    cards = "".join(f'<a href="{u}" class="fx-type"><strong>{n}</strong><span>{d}</span><em>Learn more {ARROW}</em></a>' for u, n, d in SERVICES)
    return (f'<section class="fx-sec fx-sec--tint"><div class="fx-wrap"><p class="fx-eyebrow">Our services</p>'
            f'<h2>What we do in <span class="fx-hl">{town}</span></h2><p class="fx-lead">Gas Safe registered engineers and Ideal and Vaillant '
            f'accredited installers, for every part of your heating and hot water.</p><div class="fx-types">{cards}</div></div></section>')


def review_block(names):
    rs = [REVIEWS[n] for n in names if n and n in REVIEWS]
    if not rs:
        return ""
    q = "".join(f'<blockquote><div class="fx-stars" aria-label="{r["stars"]} out of 5 stars">{"★" * r["stars"]}</div>'
                f'<p>{html.escape(r["text"])}</p><cite>{html.escape(r["name"])}, Google review</cite></blockquote>' for r in rs)
    return (f'<section class="fx-sec"><div class="fx-wrap fx-center"><p class="fx-eyebrow">From our customers</p>'
            f'<h2>What local customers <span class="fx-hl">say</span></h2><div class="fx-quote">{q}</div>'
            f'<p style="margin-top:22px"><a href="/reviews/">Read all our Google reviews</a></p></div></section>')


def faq_block(title, faqs):
    d = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)
    return (f'<section class="fx-sec"><div class="fx-wrap fx-center"><p class="fx-eyebrow">FAQs</p><h2>{title}</h2>'
            f'<div class="fx-faq" style="text-align:left">{d}</div></div></section>')


def near_block(slugs, heading):
    items = "".join(f'<li><a href="/areas/{s}/">{PIN}{BY_SLUG[s]["name"]}</a></li>' for s in slugs)
    return (f'<section class="fx-sec fx-sec--tint"><div class="fx-wrap fx-center"><p class="fx-eyebrow">Nearby</p><h2>{heading}</h2>'
            f'<ul class="fx-areas fx-near">{items}</ul><p style="margin-top:22px"><a href="/areas/">See all the areas we cover</a></p></div></section>')


def town_main(t):
    homes = "".join(f'<div class="fx-step"><h3>{h}</h3><p>{p}</p></div>' for h, p in t["homes"])
    intro = "".join(f"<p>{p}</p>" for p in t["intro"])
    return ('<div class="fx">' + CSS +
            f'<section class="fx-sec"><div class="fx-wrap"><p class="fx-eyebrow">{t["name"]}, {t["county"]}</p>'
            f'<h2>Local Gas Safe engineers in <span class="fx-hl">{t["name"]}</span></h2>{intro}{btns()}</div></section>'
            f'<section class="fx-sec" style="padding-top:0"><div class="fx-wrap"><div class="fx-dark"><p class="fx-eyebrow">Local homes</p>'
            f'<h2>Homes in {t["name"]} and what they usually need</h2><div class="fx-steps fx-nonum">{homes}</div></div></div></section>'
            + services(t["name"]) + review_block([t.get("review"), t.get("review2")])
            + faq_block(f'{t["name"]}: <span class="fx-hl">your questions answered</span>', t["faqs"])
            + near_block(t["nearby"], "We also cover") + "</div>")


AREA_NAMES = [("CM", "Chelmsford"), ("CB", "Cambridge"), ("CO", "Colchester"), ("SS", "Southend"), ("RM", "Romford"),
              ("IG", "Ilford"), ("EN", "Enfield"), ("SG", "Stevenage"), ("IP", "Ipswich")]
def code_key(code):
    m = re.match(r"([A-Z]+)(\d+)", code)
    return (m.group(1), int(m.group(2)))


def all_codes():
    by_area = {}
    for t in TOWNS:
        for code in t["codes"]:
            by_area.setdefault(code_key(code)[0], []).append((code, t))
    rows = ""
    for prefix, label in AREA_NAMES:
        items = "".join(f'<li><a href="/areas/{t["slug"]}/" title="{html.escape(t["name"])}">{code}</a></li>'
                        for code, t in sorted(by_area.get(prefix, []), key=lambda x: code_key(x[0])))
        if items:
            rows += f'<div><h3>{prefix} ({label} area)</h3><ul>{items}</ul></div>'
    n = sum(len(t["codes"]) for t in TOWNS)
    return (f'<section class="fx-sec fx-sec--tint"><div class="fx-wrap fx-center"><p class="fx-eyebrow">Postcodes</p>'
            f'<h2>Every postcode <span class="fx-hl">we cover</span></h2><p class="fx-lead">All {n} postcode districts we cover. '
            f'Tap one to see the local page.</p><div class="fx-codes">{rows}</div></div></section>')


def hub_main():
    groups = ""
    for gid, gname, slugs in GROUPS:
        cards = "".join(f'<a href="/areas/{s}/" class="fx-type"><strong>{BY_SLUG[s]["name"]}</strong>'
                        f'<span>{BY_SLUG[s]["postcode"]}</span><em>See {BY_SLUG[s]["name"]} {ARROW}</em></a>' for s in slugs)
        groups += f'<h3 class="fx-group-h" id="{gid}">{gname}</h3><div class="fx-types">{cards}</div>'
    n = sum(len(t["codes"]) for t in TOWNS)
    faqs = [("Do you cover my area?",
             f"We cover {n} postcode districts across Essex, Hertfordshire, Cambridgeshire and Suffolk, from Harlow and Brentwood to "
             "Cambridge, Ely and Bury St Edmunds. You can see every postcode we cover on this page, or call us on "
             "<a href=\"tel:+441279598972\">01279 598 972</a> and we'll tell you."),
            ("Where are you based?",
             "Our registered office is in Little Canfield, between Takeley and Great Dunmow, which puts Bishop's Stortford, Stansted and Great Dunmow close by."),
            ("Do you charge for quotes?",
             "No, our quotes are free and there's no pressure to go ahead. Call us or send the <a href=\"/contact/\">quote form</a> to arrange one.")]
    return ('<div class="fx">' + CSS +
            '<section class="fx-sec"><div class="fx-wrap"><p class="fx-eyebrow">Areas we cover</p>'
            '<h2>Local heating engineers across <span class="fx-hl">Essex, Hertfordshire, Cambridgeshire &amp; Suffolk</span></h2>'
            '<p class="fx-lead">From our registered office in Little Canfield, our Gas Safe engineers install, service and repair boilers across '
            'Essex and Hertfordshire, and into Cambridgeshire and Suffolk. Choose your area below, or see every postcode we cover.</p>'
            + groups + '<div style="margin-top:32px">' + btns() + '</div></div></section>'
            + all_codes() + services("your area") + review_block(["Hems"])
            + faq_block('Areas we cover: <span class="fx-hl">your questions answered</span>', faqs) + "</div>")


def schema(url, title, desc, crumbs, service_area, faqs, business):
    graph = [{"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-GB",
              "breadcrumb": {"@id": url + "#breadcrumb"}},
             {"@type": "Service", "@id": url + "#service", "name": "Heating and boiler services", "serviceType": "Boiler installation, servicing and repairs",
              "provider": {"@id": BASE + "/#business"}, "areaServed": service_area, "url": url},
             {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
                 {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs]},
             {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                 {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
             business]
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}) + "</script>"


def page(tpl, url, title, desc, eyebrow, h1_pre, h1_hl, lead, hero, main_html, schema_html):
    t = tpl
    head_end = t.find("</head>")
    head, body = t[:head_end], t[head_end:]
    e = html.escape(title, quote=True)
    d = html.escape(desc, quote=True)
    head = re.sub(r"<title>.*?</title>", f"<title>{e}</title>", head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + d, head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + d, head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + e, head)
    head = re.sub(r'<meta name="twitter:label1"[^>]*>\s*<meta name="twitter:data1"[^>]*>', "", head)
    head = head.replace(OLD_URL, url)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: schema_html, head, count=1, flags=re.S)
    big, small = HEROES[hero]
    head = head.replace("hero-combi-1600", big).replace("hero-combi-800", small)
    t = head + body
    t = t.replace("<span>Combi boilers</span>", f"<span>{eyebrow}</span>", 1)
    t = re.sub(r'(<h1 class="jexi-dhp__heading">).*?(<span class="jexi-dhp__highlight"[^>]*>).*?(</span></h1>)',
               lambda m: m.group(1) + h1_pre + " " + m.group(2) + html.escape(h1_hl) + m.group(3), t, count=1, flags=re.S)
    t = re.sub(r'(<div class="elementor-element elementor-element-a834167 [^>]*>\s*)<p>.*?</p>', lambda m: m.group(1) + f"<p>{lead}</p>", t, count=1, flags=re.S)
    i = t.find('<div class="fx">')
    t = t[:i] + main_html + t[balanced_div(t, i):]
    t = t.replace(STRIP, "")
    # The template sits one folder deep and links assets as ../wp-content/...; area pages are deeper, so make them absolute
    t = re.sub(r'(?<![\w/.])\.\./(?=[\w-])', "/", t)
    return t


def main():
    if PREVIEW_ONLY and not os.environ.get("FLOTECH_PREVIEW_BUILD"):
        sys.exit("The area pages are demo-only for now (PREVIEW_ONLY in area_content.py). Run: python3 scripts/preview_build.py")
    tpl = open(TEMPLATE, encoding="utf-8").read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', tpl, re.S)
    business = next(g for g in json.loads(m.group(1))["@graph"] if g.get("@type") == "HVACBusiness")
    hub = BASE + "/areas/"
    urls = [hub]
    for t in TOWNS:
        url = f'{hub}{t["slug"]}/'
        title = f'Heating Engineers in {t["name"]} | Flotech'
        assert len(title) < 60 and 140 <= len(t["desc"]) <= 160, (t["slug"], len(title), len(t["desc"]))
        # A single Place (not a list), so scripts/areas.py doesn't swap it for the site-wide list
        area = {"@type": "Place", "name": f'{t["name"]}, {t["county"]}'}
        crumbs = [("Home", BASE + "/"), ("Areas We Cover", hub), (t["name"], url)]
        out = page(tpl, url, title, t["desc"], t["county"], "Heating Engineers in", t["name"], t["lead"], t["hero"],
                   town_main(t), schema(url, title, t["desc"], crumbs, area, t["faqs"], business))
        os.makedirs(os.path.join(SITE, "areas", t["slug"]), exist_ok=True)
        open(os.path.join(SITE, "areas", t["slug"], "index.html"), "w", encoding="utf-8").write(out)
        urls.append(url)
    desc = ("Flotech's Gas Safe engineers cover Essex, Hertfordshire, Cambridgeshire and Suffolk, from Bishop's Stortford and Chelmsford to Ely and Bury St Edmunds.")
    assert 140 <= len(desc) <= 160, len(desc)
    title = "Areas We Cover | Flotech Heating and Plumbing"
    area = [{"@type": "Place", "name": f'{t["name"]}, {t["county"]}'} for t in TOWNS]
    hub_faqs_src = hub_main()
    faqs = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", hub_faqs_src)
    out = page(tpl, hub, title, desc, "Essex, Herts, Cambs &amp; Suffolk", "Areas", "We Cover",
               "Gas Safe heating engineers for boiler installation, servicing and repairs across Essex, Hertfordshire, Cambridgeshire and Suffolk.", "system",
               hub_faqs_src, schema(hub, title, desc, [("Home", BASE + "/"), ("Areas We Cover", hub)], area, faqs, business))
    os.makedirs(os.path.join(SITE, "areas"), exist_ok=True)
    open(os.path.join(SITE, "areas", "index.html"), "w", encoding="utf-8").write(out)

    sm = os.path.join(SITE, "sitemap.xml")
    s = open(sm, encoding="utf-8").read()
    s = re.sub(r"\s*<url><loc>https://flotechheating\.co\.uk/areas/[^<]*</loc></url>", "", s)
    add = "".join(f"\n  <url><loc>{u}</loc></url>" for u in urls)
    s = s.replace("\n</urlset>", add + "\n</urlset>")
    open(sm, "w", encoding="utf-8").write(s)
    print(len(urls), "area pages")


if __name__ == "__main__":
    main()
