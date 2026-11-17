"""One A5 leaflet per care plan, printed both sides (Tim, 17 Nov 2026). Draft for Darren to check.

    python3 brochures/single.py     -> out/Flotech-Care-Plans-Priority-Homeowner.pdf, -Priority-Certificate.pdf, -Priority-Plus.pdf

  side 1: the plan's name, why it matters (warranty or the law), three reasons to join, "serviced on" box
  side 2: everything the plan includes, the detail box for that plan, what isn't included, QR code, terms
Shares the look, band, 12-point list and plan facts with build.py (the two-plan packs). Facts match
site/boiler-care-plans/index.html; change all three together.
"""
import os, subprocess
import build as B
from title_svg import title_svg

HOME_SUB = B.PACKS["homeowner"]["sub"]
LAND_SUB = B.PACKS["landlord"]["sub"]

# What every plan includes (title, one line of detail)
SERVICE = ("12-point annual boiler service", "By our Gas Safe engineers, to your boiler manufacturer&rsquo;s instructions.")
PRIORITY = ("Priority booking", "When something goes wrong, you go to the front of our queue in normal working hours.")
REMINDER = ("A yearly reminder", "We remind you when your service is due. Then just call or message us to book.")
WARRANTY = ("Warranty call-outs handled", "If the manufacturer&rsquo;s warranty covers a fault, we arrange the visit and follow it up for you.")
CERT = ("Gas safety certificate", "For your boiler and gas hob, emailed to you, ready for your tenants.")
CERT_REMIND = ("A reminder before it runs out", "So you can book the check in good time and stay legal.")
CALLOUT = ("1 free call-out a year", "First hour of labour included. Fixed in that hour? You only pay for parts.")
INHIBITOR = ("Inhibitor top-up", "Tested at your service and topped up, to stop rust and sludge in your heating.")
UNVENTED = ("Unvented cylinder check", "If you have one, we check it and its safety valves at the same visit.")

GAS_CHECKS = ["Gas tightness test (checking for leaks)", "Standing and working pressure", "Ventilation for your boiler and hob",
              "Flue flow test, so fumes are removed safely", "Flame picture on your hob or cooker", "Carbon monoxide check on your boiler",
              "Electrical bonding at the gas meter", "Flame failure devices working properly"]
CALLOUT_COVERS = [("Boiler and controls", "Your boiler and flue, programmer, thermostats, zone valves and pump"),
                  ("Central heating", "Radiators and their valves, expansion tank, air vents, pipework, hot water cylinder and immersion"),
                  ("Plumbing", "Leaking pipes and joints, overflows, soil and vent pipes, tanks, and pipes from your stopcock to your taps and showers")]

TERMS_ALL = ("Monthly payments by Direct Debit, price fixed for 12 months. Plans run for 12 months and renew each year; we write to you at least 28 days "
             "before. You can cancel within 14 days of receiving your agreement (you pay for any work already done). Priority booking is in normal "
             "working hours; we can&rsquo;t promise a set response time. In winter we sometimes move service appointments to get people without "
             "heating back up and running. At your first service we check your boiler is in good working order. Boilers over 5 years old may need "
             "new burner seals at the service, at an extra &pound;40, and we tell you first.")
TERMS_END = (f" Our plans are service agreements, not insurance. Full terms at {B.WEB}/boiler-care-plans. "
             "Flotech Heating &amp; Plumbing Ltd, company no. 08739272.")

PLANS = {
    "priority-homeowner": {
        "base": B.HOME, "for": "For homeowners", "lines": ("Priority", "Homeowner"), "sub": HOME_SUB,
        "why": [("pound", "Spread the cost", "&pound;9 a month instead of &pound;108 in one go. The same price, with no big bill to plan for.")],
        "intro": "The same &pound;108 as a yearly service booked separately, split into 12 payments, with priority booking and the admin done for you.",
        "items": [SERVICE, PRIORITY, REMINDER, WARRANTY],
        "box": "checks",
        "not": ["Call-outs, repairs and parts (normal rates, and we always tell you the price first)",
                "A gas safety certificate (that&rsquo;s Priority Certificate, &pound;13 a month)"],
        "terms": "", "roomy": True,
    },
    "priority-certificate": {
        "base": B.CERT, "for": "For landlords", "lines": ("Priority", "Certificate"), "sub": LAND_SUB,
        "why": [("pound", "Spread the cost", "&pound;13 a month instead of &pound;156 in one go. The same price, with no big bill to plan for.")],
        "intro": "The same &pound;156 as a service and gas safety certificate booked separately, split into 12 payments, with priority booking and the admin done for you.",
        "items": [SERVICE, CERT, CERT_REMIND, PRIORITY, REMINDER, WARRANTY],
        "box": "gas",
        "not": ["Call-outs, repairs and parts (normal rates, and we always tell you the price first)",
                "Other gas appliances, such as a gas fire (tell us and we&rsquo;ll quote to add them)",
                "More than one property (each property needs its own plan)"],
        "terms": " You must give your tenants a copy of the certificate within 28 days of the check, and keep your records.",
    },
    "priority-plus": {
        "base": None, "for": "For homeowners and landlords", "lines": ("Priority", "Plus"),
        "sub": ("Miss your yearly service and most manufacturers can refuse a warranty claim. Priority Plus covers your service, "
                "gas safety certificate and a free call-out every year, for <b>&pound;28 a month</b>."),
        "why": [("tool", "A free call-out every year", "If something stops working, your first call-out each year is free, with the first hour of labour included.")],
        "intro": "Everything in Priority Certificate, plus a free call-out every year, an inhibitor top-up and your unvented cylinder checked.",
        "items": [SERVICE, CERT, CALLOUT, INHIBITOR, UNVENTED, PRIORITY, ("Reminders", "When your service is due and before your certificate runs out."), WARRANTY],
        "box": "callout",
        "not": ["Parts, on any job (normal rates, and we always tell you the price first)",
                "Labour after the first hour, and call-outs after your free one each year"],
        "terms": (" The free call-out is in normal working hours, can be used once your plan has been running for 30 days, doesn&rsquo;t carry "
                  "over, and doesn&rsquo;t cover faults that were already there when you joined."),
    },
}
PRICE = {"priority-homeowner": 9, "priority-certificate": 13, "priority-plus": 28}

B.ICONS["tool"] = '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L4 16.8V20h3.2l5.3-5.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4 2.6-2.6z"/>'

CSS = """
.cover h1 .htitle.p { margin-top: {TOP:.2f}pt; }
.cover .price-pill { margin-top: 3mm; display: inline-flex; align-items: baseline; gap: 1mm; padding: 1.4mm 4.5mm; border-radius: 99px; background: #f3eeff; }
.cover .price-pill b { font-size: 15pt; font-weight: 800; line-height: 1; }
.cover .price-pill span { font-size: 9pt; font-weight: 700; color: #4b465c; }

.one { padding: 7mm 9mm 0; }
.one .head { display: flex; align-items: center; justify-content: space-between; gap: 4mm; }
.one .head img { height: 9mm; width: auto; }
.one .head .nm { text-align: right; }
.one .head .nm b { display: block; font-size: 16pt; font-weight: 800; line-height: 1.05; }
.one .head .nm span { font-size: 9pt; font-weight: 700; color: #4b465c; }
.one .head .nm span strong { font-size: 13pt; font-weight: 800; color: #14121c; }
.one .intro { margin-top: 3.2mm; font-size: 8.8pt; line-height: 1.4; font-weight: 600; color: #3b3848; }
.feat { margin-top: 3.2mm; display: grid; grid-template-columns: 1fr 1fr; gap: 2.4mm 4mm; }
.feat > div { display: flex; gap: 1.8mm; }
.feat svg { width: 3.6mm; height: 3.6mm; flex: none; margin-top: .2mm; }
.feat b { display: block; font-size: 9pt; font-weight: 800; line-height: 1.2; }
.feat p { margin-top: .4mm; font-size: 7.4pt; line-height: 1.3; font-weight: 600; color: #4b465c; }
.one .checks { margin-top: 3.6mm; }
.checks.two ul { grid-template-columns: repeat(2, 1fr); }
.cov { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; }
.cov b { display: block; font-size: 7.8pt; font-weight: 800; margin-bottom: .6mm; }
.cov p { font-size: 7pt; line-height: 1.3; font-weight: 600; color: #4b465c; }
.not { margin-top: 3mm; }
.not h4 { font-size: 9pt; font-weight: 800; }
.not ul { list-style: none; margin-top: 1.2mm; display: grid; gap: .9mm; }
.not li { display: flex; gap: 1.6mm; font-size: 7.6pt; line-height: 1.3; font-weight: 600; color: #3b3848; }
.not li svg { width: 3mm; height: 3mm; flex: none; margin-top: .2mm; }
.one .join { margin-top: 3.2mm; }
.one .join img { width: 19mm; height: 19mm; }
.one .join .j b { font-size: 12pt; }
/* more room on the plan with the least to say (homeowner) */
.one.roomy .intro { margin-top: 4mm; font-size: 9.8pt; }
.one.roomy .feat { margin-top: 4.2mm; gap: 3.6mm 5mm; }
.one.roomy .feat svg { width: 4.2mm; height: 4.2mm; }
.one.roomy .feat b { font-size: 10.4pt; }
.one.roomy .feat p { margin-top: .6mm; font-size: 8.3pt; }
.one.roomy .checks { margin-top: 5mm; padding: 3.6mm 4.2mm 3.4mm; }
.one.roomy .checks h4 { font-size: 10.4pt; margin-bottom: 2.6mm; }
.one.roomy .checks ul { gap: 2mm 3mm; }
.one.roomy .checks li { font-size: 8pt; }
.one.roomy .checks li svg { width: 3.3mm; height: 3.3mm; }
.one.roomy .not { margin-top: 4.4mm; }
.one.roomy .not h4 { font-size: 10pt; }
.one.roomy .not ul { margin-top: 1.8mm; gap: 1.4mm; }
.one.roomy .not li { font-size: 8.4pt; }
.one.roomy .not li svg { width: 3.4mm; height: 3.4mm; }
.one.roomy .join { margin-top: 4.4mm; }
.one.roomy .join img { width: 23mm; height: 23mm; }
.one.roomy .join .j b { font-size: 13pt; }
.one.roomy .small { margin-top: 3mm; font-size: 6.4pt; }
"""
CROSS = ('<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="#e6e1ef"/>'
         '<path d="M5.4 5.4l5.2 5.2M10.6 5.4l-5.2 5.2" stroke="#6b6680" stroke-width="1.7" stroke-linecap="round"/></svg>')


def detail_box(kind):
    if kind == "checks":
        items = "".join(f"<li>{B.TICK}<span>{c}</span></li>" for c in B.CHECKS)
        return f'<div class="checks"><h4>What&rsquo;s in your 12-point annual boiler service</h4><ul>{items}</ul></div>'
    if kind == "gas":
        items = "".join(f"<li>{B.TICK}<span>{c}</span></li>" for c in GAS_CHECKS)
        return f'<div class="checks two"><h4>What your gas safety check covers</h4><ul>{items}</ul></div>'
    cols = "".join(f"<div><b>{t}</b><p>{d}</p></div>" for t, d in CALLOUT_COVERS)
    return f'<div class="checks"><h4>What your free call-out covers</h4><div class="cov">{cols}</div></div>'


def leaflet(key):
    p = PLANS[key]
    title, top = title_svg(lines=p["lines"])
    title = title.replace('class="htitle"', 'class="htitle p"').replace('id="hg"', 'id="hg1"').replace("url(#hg)", "url(#hg1)")
    why = p["why"] + [("clock", "Save time", "We remind you when your service is due and deal with the manufacturer if you need a warranty call-out."),
                      ("bolt", "Seen first", "If something goes wrong, plan members are booked in before customers who aren&rsquo;t on a plan.")]
    why_html = "".join(f'<div class="b">{B.icon(i)}<div><b>{t}</b><p>{d}</p></div></div>' for i, t, d in why)
    cover = f"""<section class="page cover">
  <img class="logo" src="logo-centred.png" alt="Flotech Heating and Plumbing">
  <p class="for">{p['for']}</p>
  <h1>{title}</h1>
  <p class="sub">{p['sub']}</p>
  <div class="why">{why_html}</div>
  <div class="serviced"><div>Serviced on</div><div>Engineer</div></div>
  {B.band()}
</section>"""
    name = " ".join(p["lines"])
    feats = "".join(f"<div>{B.TICK}<div><b>{t}</b><p>{d}</p></div></div>" for t, d in p["items"])
    nots = "".join(f"<li>{CROSS}<span>{n}</span></li>" for n in p["not"])
    back = f"""<section class="page one{' roomy' if p.get('roomy') else ''}">
  <div class="head"><img src="logo-noslogan-centred.png" alt="Flotech">
    <div class="nm"><b>{name}</b><span><strong>&pound;{PRICE[key]}</strong> /month · including VAT · 12-month plan</span></div></div>
  <p class="intro">{p['intro']}</p>
  <div class="feat">{feats}</div>
  {detail_box(p['box'])}
  <div class="not"><h4>Not included</h4><ul>{nots}</ul></div>
  <div class="join"><img src="qr-care-plans.svg" alt="QR code to the care plans page">
    <div class="j"><b>Scan to join, or ask your engineer</b><p>{B.WEB}/boiler-care-plans</p></div></div>
  <p class="small">{TERMS_ALL}{p['terms']}{TERMS_END}</p>
  {B.band()}
</section>"""
    css = B.CSS + CSS.replace("{TOP:.2f}", f"{top:.2f}")
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Flotech {name}</title>
<link rel="stylesheet" href="file://{B.FONTS}"><style>{css}</style></head><body>{cover}{back}</body></html>"""


def main():
    os.makedirs(B.OUT, exist_ok=True)
    for f in ("logo-centred.png", "logo-noslogan-centred.png", "gas-safe-mst.png", "qr-care-plans.svg"):
        src, dst = os.path.join(B.HERE, f), os.path.join(B.OUT, f)
        if not os.path.exists(dst):
            os.symlink(src, dst)
    for key in PLANS:
        open(os.path.join(B.OUT, f"flotech-care-plans-{key}.html"), "w", encoding="utf-8").write(leaflet(key))
    subprocess.run(["node", os.path.join(B.HERE, "render.js"), B.OUT] + list(PLANS), check=True)


if __name__ == "__main__":
    main()
