"""Builds /privacy-policy/ for Flotech and links it in the footer's Quick Links.

Run: python3 scripts/build_privacy.py && python3 scripts/areas.py && python3 scripts/mobile_header.py
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_areas import page, TEMPLATE, BASE, SITE  # noqa: E402
from build_terms import CSS  # noqa: E402
from finance_fix import balanced_div  # noqa: E402

CO = "Flotech Heating &amp; Plumbing Ltd"
SECTIONS = [
    ("Who we are", f"<p>{CO} (company number 08739272), 62 Burgattes Road, Little Canfield, Dunmow, Essex, CM6 1FW, is the data controller "
     "for personal information collected through this website. You can contact us at "
     '<a href="mailto:office@flotechheating.co.uk">office@flotechheating.co.uk</a> or on <a href="tel:+441279598972">01279 598 972</a>.</p>'),
    ("What we collect", "<p>When you send an enquiry through our website we collect your name, phone number, email address and anything you write "
     "in your message. If you call or email us, we keep a record of that contact.</p>"),
    ("How we use it", "<p>We use your details to reply to your enquiry, arrange visits, provide quotes and carry out work. Our lawful basis is "
     "taking steps at your request before entering into a contract, and performing that contract. We may also contact you after a job, for "
     "example to ask for a review, based on our legitimate interest in running our business. You can ask us to stop at any time.</p>"),
    ("Website analytics", "<p>We use Ahrefs Web Analytics to count visits to this website and see which pages are useful. It does not use "
     "cookies and does not identify you personally; it only gives us totals, such as the number of visits to each page.</p>"),
    ("Cookies", "<p>Our cookie banner lets you choose which optional cookies you accept. Cookies that are needed for the website to work "
     "are always on. You can change your choice at any time from the cookie banner.</p>"),
    ("Finance", "<p>Boiler installation finance is provided through Phoenix Financial Consultants Ltd. If you follow our link to Phoenix, "
     "any information you give them is handled under Phoenix&rsquo;s own privacy policy.</p>"),
    ("Who we share it with", "<p>We use trusted service providers to host this website and to manage enquiries and customer records. They "
     "only process your information on our instructions. We do not sell your information.</p>"),
    ("How long we keep it", "<p>We keep enquiry details for as long as needed to deal with your enquiry and any work that follows, and "
     "customer and job records for as long as required for accounting and legal purposes.</p>"),
    ("Your rights", "<p>Under UK GDPR you can ask to see the information we hold about you, ask us to correct or delete it, object to how we "
     "use it or ask us to restrict it. Contact us at <a href=\"mailto:office@flotechheating.co.uk\">office@flotechheating.co.uk</a>. If you "
     "are unhappy with how we handle your information, you can complain to the Information Commissioner&rsquo;s Office at "
     '<a href="https://ico.org.uk" target="_blank" rel="noopener">ico.org.uk</a>.</p>'),
]


def main():
    tpl = open(TEMPLATE, encoding="utf-8").read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', tpl, re.S)
    business = next(g for g in json.loads(m.group(1))["@graph"] if g.get("@type") == "HVACBusiness")
    url = BASE + "/privacy-policy/"
    title = "Privacy Policy | Flotech Heating and Plumbing"
    desc = ("How Flotech Heating & Plumbing Ltd collects, uses and protects the personal information you give us through this website, "
            "under UK GDPR, and your rights.")
    body = '<p><em>Last updated: November 2026</em></p>' + "".join(f"<h2>{h}</h2>{p}" for h, p in SECTIONS)
    main_html = '<div class="fx">' + CSS + '<section class="fx-sec"><div class="fx-wrap"><div class="fx-terms">' + body + "</div></div></section></div>"
    graph = [{"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-GB"}, business]
    schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}) + "</script>"
    out = page(tpl, url, title, desc, "Flotech Heating &amp; Plumbing Ltd", "Privacy", "Policy",
               "How we use the personal information you give us.", "regular", main_html, schema)
    i = out.find("The numbers speak for themselves")
    if i > 0:
        s = out.rfind('<div class="elementor-element', 0, out.rfind('e-parent', 0, i) + 1)
        out = out[:s] + out[balanced_div(out, s):]
    os.makedirs(os.path.join(SITE, "privacy-policy"), exist_ok=True)
    open(os.path.join(SITE, "privacy-policy", "index.html"), "w", encoding="utf-8").write(out)
    sm = os.path.join(SITE, "sitemap.xml")
    s = open(sm, encoding="utf-8").read()
    if url not in s:
        open(sm, "w", encoding="utf-8").write(s.replace("\n</urlset>", f"\n  <url><loc>{url}</loc></url>\n</urlset>"))
    print("privacy page built", len(title), len(desc))


if __name__ == "__main__":
    main()
