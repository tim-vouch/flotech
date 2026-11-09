"""Phoenix finance compliance (Nov 2026).

Flotech is an Introducer Appointed Representative (IAR) of Phoenix Financial Consultants Ltd. The site may only show:
the status disclosure, Phoenix's own banner and calculator, and a simple line such as
"Boiler installation finance available through Phoenix Financial Consultants Ltd". Nothing else about finance.

    python3 scripts/finance_fix.py preview   # writes fixed copies to site/_finance-preview/ (shown only on the Worker preview)
    python3 scripts/finance_fix.py apply     # writes the fixes into site/ itself (goes live on the next push)
"""
import re, sys, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPROVED = "Boiler installation finance available through Phoenix Financial Consultants Ltd."

STRIP = ('<div class="ffs" style="max-width:1200px;margin:0 auto;padding:0 20px 10px">'
         '<a href="/boiler-finance/" style="display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;'
         'font-family:Urbanist,sans-serif;font-weight:700;font-size:17px;color:#0A0A0A;text-decoration:none;'
         'background:#F4F2FB;border:1px solid #E4DEF7;border-radius:14px;padding:18px 22px;text-align:center">'
         '<span style="width:10px;height:10px;border-radius:50%;background:linear-gradient(90deg,#9B51FF,#1BA5FF);flex:none"></span>'
         f'{APPROVED}</a></div>')
WHY_LINE = (f'<p style="margin:18px 0 0;font-size:15px;font-weight:600"><a href="/boiler-finance/" style="color:#FFFFFF;text-decoration:underline;text-underline-offset:3px">{APPROVED}</a></p>')


def balanced_div(t, start):
    """End index of the <div> that opens at `start`."""
    depth, i = 0, start
    for m in re.compile(r"<div\b|</div>").finditer(t, start):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return m.end()
    raise ValueError("unbalanced div")


def sub(t, pat, rep, flags=re.S, count=0):
    return re.sub(pat, rep, t, count=count, flags=flags)


def fix(t, rel):
    # 1. Menus: drop the Boiler Finance item (desktop mega menu, mobile list, mobile cards)
    t = sub(t, r'<a href="/boiler-finance/" class="ft-mega__item"[^>]*>.*?</a>', "")
    t = sub(t, r'<a href="/boiler-finance/" class="ftm-card">.*?</a>', "")
    t = t.replace('<li><a href="/boiler-finance/">Boiler Finance</a></li>', "")
    # 2. Footer services list
    t = sub(t, r'(<li class="elementor-icon-list-item">\s*<a href="/boiler-finance/">(?:(?!</li>).)*?)Boiler Finance(</span>\s*</a>\s*</li>)', r"\1Finance available through Phoenix\2")
    # 3. Approved line above the status disclosure (footer, every page)
    t = t.replace("<p>Flotech Heating and Plumbing ltd is an Introducer Appointed Representative",
                  f"<p><strong>{APPROVED}</strong></p><p>Flotech Heating and Plumbing ltd is an Introducer Appointed Representative")
    # 4. Homepage
    t = t.replace("from new installations and annual servicing to finance plans and ongoing care.",
                  "from new installations and annual servicing to repairs and ongoing care.")
    t = t.replace("Flexible boiler finance available</li>", "Free quotes</li>")
    if rel == "index.html" or rel == "home/index.html":
        t = re.sub(r'(<ul class="ft-why-list">.*?</ul>)', lambda m: m.group(1) + WHY_LINE, t, count=1, flags=re.S)
    m = re.search(r'<div class="elementor-element elementor-element-724c26b5 ', t)
    if m:  # Boiler Finance card becomes Boiler Conversions
        e = balanced_div(t, m.start())
        card = t[m.start():e]
        card = card.replace(">Boiler Finance</h3>", ">Boiler Conversions</h3>")
        card = card.replace('aria-label="Boiler Finance"', 'aria-label="Boiler Conversions"').replace("<title>Boiler Finance</title>", "<title>Boiler Conversions</title>")
        card = card.replace('href="/boiler-finance/"', 'href="/boiler-conversions/"')
        card = sub(card, r'<g class="price-tag">.*?</g>', "")
        card = sub(card, r'<path d="M 122 52 Q 128 56 132 60"[^>]*></path>', "")
        t = t[:m.start()] + card + t[e:]
    # 5. "Boiler Finance Available" section on the boiler pages: remove the whole section
    i = t.find("elementor-element-581068c")
    if i > -1:
        s = t.rfind('<div class="elementor-element', 0, t.rfind("e-parent", 0, i) + 20)
        while "e-parent" not in t[s:s + 200]:
            s = t.rfind('<div class="elementor-element', 0, s)
        t = t[:s] + STRIP + t[balanced_div(t, s):]
    # 6. Servicing page: "Learn more" in the warning-signs section pointed at the finance page
    if rel.startswith("boiler-servicing"):
        t = sub(t, r'href="/boiler-finance/">(\s*<span class="elementor-button-content-wrapper">)', r'href="/contact/">\1')
        t = t.replace('<span class="elementor-screen-only"> about boiler finance</span>', '<span class="elementor-screen-only"> about booking a repair</span>')
    # Care plans (preview only): "pay monthly", not "spread the cost", so it can't be mistaken for finance
    if rel.startswith("boiler-care-plans"):
        for a, b in [("booked for you and spread into small monthly payments.", "booked for you, with a small monthly payment."),
                     ("Our plans book it for you and spread the cost,", "Our plans book it for you, with a small monthly payment,"),
                     ("<b>Spread the cost</b><p>A small monthly payment instead of one bill for your service.</p>", "<b>Pay monthly</b><p>A small monthly payment instead of one bill for your service.</p>")]:
            t = t.replace(a, b)
    # 7. FAQs: drop "Can I spread the cost" questions (visible and in the FAQ schema)
    t = sub(t, r'<details><summary>Can I spread the cost of a new [a-z ]+boiler\?</summary>.*?</details>', "")
    t = sub(t, r',?\s*\{"@type": "Question", "name": "Can I spread the cost of a new [a-z ]+boiler\?".*?\}\}', "")
    t = t.replace('so there are no surprises, and <a href="/boiler-finance/">finance</a> is available to spread the cost.', "so there are no surprises.")
    t = t.replace("so there are no surprises, and finance is available to spread the cost.", "so there are no surprises.")
    # 8. Page descriptions
    for a, b in [(" Finance available.", ""), (", finance available.", "."), (" and finance available.", "."),
                 ("repairs, finance and reliable plumbing", "repairs and reliable plumbing")]:
        t = t.replace(a, b)
    return t


FIN_MAIN = f"""<main id="content" class="site-main">
<style>
.ffp{{font-family:'Urbanist',sans-serif;max-width:760px;margin:0 auto;padding:110px 24px 90px;text-align:center;color:#0A0A0A}}
.ffp h1{{font-size:clamp(34px,5vw,54px);font-weight:800;letter-spacing:-1.2px;line-height:1.1;margin:0 0 22px}}
.ffp h1 span{{background:linear-gradient(90deg,#9B51FF,#1BA5FF);-webkit-background-clip:text;background-clip:text;color:transparent}}
.ffp .lead{{font-size:20px;font-weight:600;line-height:1.5;margin:0 0 22px}}
.ffp .disc{{font-size:14px;line-height:1.6;color:#4A4A4A;margin:0 auto 34px;max-width:640px}}
.ffp a.btn{{display:inline-block;padding:15px 28px;border-radius:10px;font-weight:700;text-decoration:none;color:#fff;background:linear-gradient(90deg,#9B51FF,#1BA5FF)}}
</style>
<section class="ffp">
<h1>Boiler <span>Finance</span></h1>
<p class="lead">{APPROVED}</p>
<p class="disc">Flotech Heating and Plumbing ltd is an Introducer Appointed Representative (Financial Services Register No. 1042219) of Phoenix Financial Consultants Limited (Phoenix). Phoenix is a credit broker, not a lender. Phoenix is authorised and regulated by the Financial Conduct Authority (FRN: 539195), and offers finance from its panel of lenders. All finance subject to status and credit checks.</p>
<a class="btn" href="/gas-boiler-installations/">See our boiler installations</a>
</section>
</main>"""


def fix_finance_page(t):
    t = t[:t.find("<main")] + FIN_MAIN + t[t.find("</main>") + len("</main>"):]
    t = t.replace("Boiler Finance in Bishop&#039;s Stortford | Flexible Payments | Flotech", "Boiler Finance | Flotech Heating and Plumbing")
    t = t.replace("Boiler Finance in Bishop's Stortford | Flexible Payments | Flotech", "Boiler Finance | Flotech Heating and Plumbing")
    t = sub(t, r'(<meta name="description" content=")[^"]*', r"\1" + APPROVED)
    t = sub(t, r'(<meta property="og:description" content=")[^"]*', r"\1" + APPROVED)
    t = sub(t, r'("description":")Boiler finance in Bishop[^"]*', r"\1" + APPROVED)
    return t


def main(mode):
    out_root = os.path.join(ROOT, "site", "_finance-preview") if mode == "preview" else os.path.join(ROOT, "site")
    changed = []
    for f in sorted(glob.glob(os.path.join(ROOT, "site", "**", "index.html"), recursive=True)):
        rel = os.path.relpath(f, os.path.join(ROOT, "site"))
        if rel.startswith(("_finance-preview", "wp-")):
            continue
        t = open(f, encoding="utf-8").read()
        n = fix(t, rel)
        if rel == "boiler-finance/index.html":
            n = fix_finance_page(n)
        if n != t:
            dst = os.path.join(out_root, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, "w", encoding="utf-8").write(n)
            changed.append(rel)
    print(mode, len(changed), "pages:", ", ".join(changed))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "preview")
