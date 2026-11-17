"""Flotech boiler care plan leaflets: A5, printed both sides (Tim, 17 Nov 2026).

    python3 brochures/build.py      -> brochures/out/*.html, *.pdf and *.png previews

Two leave-behind packs, each one A5 sheet:
  side 1: cover (logo, title, the 12-point service, "serviced on" box)
  side 2: the two plans side by side, why join, QR code to the care plans page
Homeowner pack = For Homeowners + Priority Plus. Landlord pack = Service & Certificate + Priority Plus.
Facts match site/boiler-care-plans/index.html; change both together.
"""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FONTS = os.path.join(os.path.dirname(HERE), "site", "fonts", "google", "urbanist.css")
PHONE, TEL, WEB, EMAIL = "01279 598 972", "+441279598972", "flotechheating.co.uk", "office@flotechheating.co.uk"
GAS_SAFE_NO = ""   # TODO: Flotech's Gas Safe registration number (from Darren). Blank shows a gap to fill in.

CHECKS = ["Visual inspection, inside and out", "Flue inspection", "Gas rate test", "Radiator check", "Filter clean",
          "System function check", "Boiler operating pressure test", "Pilot and burner check", "Flue gas analysis",
          "Seal check", "Water leak check", "Thermostat and heating controls check"]   # longest last, so it wraps on the bottom row

HOME = {"name": "For Homeowners", "price": 9, "year": 108,
        "items": ["12-point annual boiler service", "Priority booking when something goes wrong",
                  "A reminder when your service is due", "We deal with the manufacturer on warranty call-outs"],
        "same": "The same £108 as a yearly service booked separately, split into 12 payments."}
CERT = {"name": "Service &amp; Certificate", "price": 13, "year": 156,
        "items": ["12-point annual boiler service", "Gas safety certificate (boiler and hob)",
                  "Certificate emailed, ready for your tenants", "A reminder before it expires",
                  "Priority booking when something goes wrong"],
        "same": "The same £156 as a service and certificate booked separately, split into 12 payments."}
PLUS_EXTRAS = ["1 free call-out a year, first hour of labour included", "Inhibitor top-up to protect your heating",
               "Unvented cylinder check (if you have one)"]
PACKS = {
    "homeowner": {"for": "For homeowners", "base": HOME,
                  "plus_items": ["Gas safety check and certificate (boiler and hob)"] + PLUS_EXTRAS},
    "landlord": {"for": "For landlords", "base": CERT, "plus_items": PLUS_EXTRAS},
}

TICK = ('<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" fill="#1FA84F"/>'
        '<path d="M4.6 8.3l2.2 2.2 4.6-4.8" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')

CSS = """
@page { size: 148mm 210mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { font-family: 'Urbanist', sans-serif; color: #14121c; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 148mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; background: #fff; }
.grad { background: linear-gradient(100deg, #9B51FF 0%, #1BA5FF 100%); }
.gtext { background: linear-gradient(100deg, #8a3ff5, #1592e6); -webkit-background-clip: text; background-clip: text; color: transparent; }

/* cover */
.cover { display: flex; flex-direction: column; align-items: center; text-align: center; padding: 10mm 12mm 0; }
.cover .logo { width: 44mm; height: auto; }
.cover .for { margin-top: 5.5mm; font-size: 10pt; font-weight: 800; letter-spacing: 2.4px; text-transform: uppercase; color: #7a3fe0; }
.cover h1 { margin-top: 2mm; font-size: 30pt; line-height: 1.02; font-weight: 800; }
.cover .sub { margin-top: 4mm; font-size: 11pt; line-height: 1.42; color: #3b3848; max-width: 116mm; }
.cover .sub b { color: #14121c; font-weight: 700; }
.checks { margin-top: 5.5mm; width: 100%; border: 1px solid #e7e3f1; border-radius: 4mm; padding: 4.5mm 5mm 4mm; text-align: left; background: #fbfaff; }
.checks h2 { font-size: 10.5pt; font-weight: 800; margin-bottom: 2.6mm; text-align: center; }
.checks ul { list-style: none; display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm 5mm; }
.checks li { display: flex; gap: 1.8mm; align-items: flex-start; font-size: 8.6pt; line-height: 1.25; font-weight: 600; }
.checks li svg, .plan li svg { width: 3.4mm; height: 3.4mm; flex: none; margin-top: .3mm; }
.serviced { margin-top: 4mm; width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }
.serviced div { border: 1.4px dashed #b9a6e8; border-radius: 3mm; padding: 2.4mm 3.2mm 6.5mm; text-align: left; font-size: 8pt; font-weight: 700; color: #5b5470; }
.band { position: absolute; left: 0; right: 0; bottom: 0; height: 22mm; color: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 10mm; }
.band .call { font-size: 8.5pt; font-weight: 700; opacity: .92; }
.band .num { font-size: 17pt; font-weight: 800; letter-spacing: .3px; line-height: 1.1; }
.band .web { text-align: right; font-size: 9pt; font-weight: 700; line-height: 1.45; }
.band .gs { display: flex; align-items: center; gap: 2mm; background: #fff; border-radius: 2mm; padding: 1.3mm 2.2mm 1.3mm 1.5mm; color: #14121c; }
.band .gs img { height: 11mm; width: auto; }
.band .gs span { font-size: 6.8pt; font-weight: 700; line-height: 1.25; }
.band .gs b { display: block; font-size: 8.6pt; font-weight: 800; letter-spacing: .3px; }

/* plans side */
.plans-side { padding: 7.5mm 9mm 0; }
.top { display: flex; align-items: center; justify-content: space-between; }
.top img { height: 10mm; width: auto; }
.top .t { text-align: right; }
.top .t b { display: block; font-size: 15pt; font-weight: 800; line-height: 1.05; }
.top .t span { font-size: 8.5pt; font-weight: 700; color: #6b6680; letter-spacing: .3px; }
.cards { margin-top: 5.5mm; display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; align-items: stretch; }
.plan { border: 1px solid #e3def0; border-radius: 4mm; padding: 4.5mm 4mm 4mm; position: relative; background: #fff; }
.plan.pop { border: 2px solid transparent; background: linear-gradient(#fff, #fff) padding-box, linear-gradient(120deg, #9B51FF, #1BA5FF) border-box; }
.tag { position: absolute; top: -3mm; left: 50%; transform: translateX(-50%); white-space: nowrap; font-size: 7.2pt; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; color: #fff; padding: 1mm 3mm; border-radius: 99px; }
.plan h3 { font-size: 12.5pt; font-weight: 800; line-height: 1.1; }
.price { margin-top: 2mm; display: flex; align-items: baseline; gap: 1mm; }
.price b { font-size: 25pt; font-weight: 800; line-height: 1; }
.price span { font-size: 9pt; font-weight: 700; color: #4b465c; }
.vat { margin-top: 1mm; font-size: 7.4pt; font-weight: 600; color: #6b6680; }
.plan ul { list-style: none; margin-top: 3mm; display: grid; gap: 1.8mm; }
.plan li { display: flex; gap: 1.8mm; font-size: 8.6pt; line-height: 1.25; font-weight: 600; }
.plan .every { margin-top: 3.2mm; font-size: 8.4pt; font-weight: 800; line-height: 1.3; color: #14121c; padding: 2mm 2.6mm; border-radius: 2.4mm; background: #f3eeff; }
.plan .every + ul { margin-top: 2.6mm; }
.same { margin-top: 3mm; font-size: 7.6pt; line-height: 1.35; color: #4b465c; font-weight: 600; }
.why { margin-top: 4.5mm; }
.why h4 { font-size: 11pt; font-weight: 800; margin-bottom: 2.4mm; }
.why .cols { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; }
.why .b { border-radius: 3.5mm; background: #f6f3fd; padding: 3mm 3mm 2.6mm; }
.why .ic { width: 8mm; height: 8mm; border-radius: 50%; display: grid; place-items: center; color: #fff; margin-bottom: 1.8mm; }
.why .ic svg { width: 4.6mm; height: 4.6mm; }
.why b { display: block; font-size: 9.6pt; font-weight: 800; line-height: 1.15; margin-bottom: 1mm; }
.why p { font-size: 7.7pt; line-height: 1.33; color: #3b3848; font-weight: 600; }
.join { margin-top: 3.5mm; display: flex; align-items: center; gap: 4.5mm; }
.join img { width: 17mm; height: 17mm; flex: none; }
.join .j b { display: block; font-size: 12pt; font-weight: 800; line-height: 1.15; }
.join .j p { margin-top: 1mm; font-size: 9pt; font-weight: 700; color: #3b3848; }
.small { margin-top: 3mm; font-size: 6.2pt !important; font-size: 6.6pt; line-height: 1.4; color: #6b6680; font-weight: 600; }
"""


def band():
    no = GAS_SAFE_NO or "______"
    return (f'<div class="band grad"><div><div class="call">Call us</div><div class="num">{PHONE}</div></div>'
            f'<div class="web">{WEB}<br>{EMAIL}</div>'
            f'<div class="gs"><img src="gas-safe-yellow.png" alt="Gas Safe Register"><span>Gas Safe<br>registered<b>No. {no}</b></span></div></div>')


ICONS = {"pound": '<path d="M16 6.5a4 4 0 0 0-7.2 2.4V12H6m2.8 0v2.6c0 1.6-.9 3-2.3 3.9H17M6 12h7.5"/>',
         "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
         "bolt": '<path d="M12 3l7.5 3v5.5c0 4.6-3.2 8.2-7.5 9.5-4.3-1.3-7.5-4.9-7.5-9.5V6L12 3z"/><path d="M9 12l2.2 2.2L15.5 10"/>'}


def icon(n):
    return (f'<span class="ic grad"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg></span>')


def ul(items):
    return "<ul>" + "".join(f"<li>{TICK}<span>{i}</span></li>" for i in items) + "</ul>"


def leaflet(key):
    p = PACKS[key]
    base = p["base"]
    checks = "".join(f"<li>{TICK}<span>{c}</span></li>" for c in CHECKS)
    cover = f"""<section class="page cover">
  <img class="logo" src="logo.webp" alt="Flotech Heating and Plumbing">
  <p class="for">{p['for']}</p>
  <h1><span class="gtext">Boiler<br>Care Plans</span></h1>
  <p class="sub">Your yearly boiler service for a small monthly payment. <b>We handle the reminders and the warranty paperwork, so you save time,</b> and you&rsquo;re seen first if something goes wrong.</p>
  <div class="checks"><h2>Your 12-point annual boiler service</h2><ul>{checks}</ul></div>
  <div class="serviced"><div>Serviced on</div><div>Engineer</div></div>
  {band()}
</section>"""
    plans = f"""<section class="page plans-side">
  <div class="top"><img src="logo-noslogan.png" alt="Flotech"><div class="t"><b>Choose your plan</b><span>{p['for']}</span></div></div>
  <div class="cards">
    <div class="plan">
      <h3>{base['name']}</h3>
      <div class="price"><b>£{base['price']}</b><span>/month</span></div>
      <p class="vat">Including VAT · 12-month plan</p>
      {ul(base['items'])}
      <p class="same">{base['same']}</p>
    </div>
    <div class="plan pop"><span class="tag grad">Most cover</span>
      <h3>Priority Plus</h3>
      <div class="price"><b>£28</b><span>/month</span></div>
      <p class="vat">Including VAT · 12-month plan</p>
      <p class="every">Everything in {base['name']}, plus:</p>
      {ul(p['plus_items'])}
    </div>
  </div>
  <div class="why"><h4>Why join a care plan?</h4><div class="cols">
    <div class="b">{icon("pound")}<b>Spread the cost</b><p>£{base['price']} a month instead of £{base['year']} in one go. Same price, no big bill.</p></div>
    <div class="b">{icon("clock")}<b>Save time</b><p>We remind you when it&rsquo;s due and deal with the manufacturer on warranty call-outs.</p></div>
    <div class="b">{icon("bolt")}<b>Seen first</b><p>If something goes wrong, plan members get priority over customers without a plan.</p></div>
  </div></div>
  <div class="join"><img src="qr-care-plans.svg" alt="QR code to the care plans page">
    <div class="j"><b>Scan to join, or ask your engineer</b><p>{WEB}/boiler-care-plans</p></div></div>
  <p class="small">Monthly payments by Direct Debit. Plans run for 12 months and renew each year. Parts and repairs are charged at our normal rates and we
    always tell you the price first. The Priority Plus free call-out can be used once your plan has been running for 30 days and doesn&rsquo;t cover faults that
    were already there when you joined. Boilers over 5 years old may need new burner seals at the service, at an extra £40. Full terms at {WEB}/boiler-care-plans.
    Flotech Heating &amp; Plumbing Ltd, company no. 08739272.</p>
  {band()}
</section>"""
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Flotech Boiler Care Plans: {p['for']}</title>
<link rel="stylesheet" href="file://{FONTS}"><style>{CSS}</style></head><body>{cover}{plans}</body></html>"""


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in ("logo.webp", "logo-noslogan.png", "gas-safe-yellow.png", "qr-care-plans.svg"):
        src, dst = os.path.join(HERE, f), os.path.join(OUT, f)
        if not os.path.exists(dst):
            os.symlink(src, dst)
    for key in PACKS:
        open(os.path.join(OUT, f"flotech-care-plans-{key}.html"), "w", encoding="utf-8").write(leaflet(key))
    subprocess.run(["node", os.path.join(HERE, "render.js"), OUT] + list(PACKS), check=True)


if __name__ == "__main__":
    main()
