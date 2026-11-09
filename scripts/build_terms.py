"""Builds /terms-and-conditions/ from Flotech's own Boiler Terms and Conditions (sent by Louise, 9 Nov 2026).

The wording is Flotech's, copied as supplied (only the numbering is tidied). Change it here only if Flotech
send a new version. Run: python3 scripts/build_terms.py && python3 scripts/areas.py
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_areas import page, TEMPLATE, BASE, SITE  # noqa: E402
from finance_fix import balanced_div  # noqa: E402

SECTIONS = [
    ("1. Definitions", [
        "<p><strong>1.1</strong> &ldquo;Company&rdquo; refers to Flotech Heating &amp; Plumbing Ltd.</p>",
        "<p><strong>1.2</strong> &ldquo;Customer&rdquo; refers to any individual or entity purchasing boiler installation, servicing, or heating system upgrades from the Company.</p>",
        "<p><strong>1.3</strong> &ldquo;Services&rdquo; refers to the installation, servicing, and upgrades of boilers, central heating systems, and related components.</p>",
        "<p><strong>1.4</strong> &ldquo;Equipment&rdquo; refers to all materials and products supplied by the Company, including boilers, pipework, controls, radiators, and accessories.</p>"]),
    ("2. Scope of Services", [
        "<p><strong>2.1</strong> The Company provides the following services:</p><ul><li>Installation of new boilers and central heating systems.</li>"
        "<li>Servicing and maintenance of boilers to ensure efficiency and safety.</li><li>Upgrades and replacements of heating system components.</li></ul>",
        "<p><strong>2.2</strong> The Company supplies all necessary equipment but may reuse existing controls where suitable.</p>",
        "<p><strong>2.3</strong> All work is carried out by the Company&rsquo;s employees or subcontractors.</p>",
        "<p><strong>2.4 Free services.</strong> Service must be booked by yourself; we will not contact you for any free services given. Service must be booked between month 11 and month 13 of the boiler install. Any bookings outside of this time frame will forfeit the first-year service.</p>",
        "<p><strong>2.5 Comparing and Matching Competitor Quotations</strong></p><ul>"
        "<li>Where the Customer asks the Company to consider matching a quotation from another contractor, the Customer must provide a complete, current and itemised written quotation.</li>"
        "<li>The quotation must clearly show all relevant products and services included, such as the boiler make and model, controls, materials, labour, system cleaning or flushing, warranties, disposal of existing equipment, additional works and VAT.</li>"
        "<li>The Company can only consider matching a quotation where the products, specification, standard of installation, scope of work, warranties and other inclusions are genuinely equivalent to those included in the Company&rsquo;s quotation.</li>"
        "<li>If the competitor&rsquo;s quotation is incomplete or does not provide enough detail, the Company will be unable to confirm that it is a like-for-like quotation or agree to match the price.</li>"
        "<li>Any price match is subject to review and written confirmation by the Company. A price match is not automatic and may be declined where there are material differences between the quotations.</li></ul>"]),
    ("3. Guarantees and Warranties", [
        "<p><strong>3.1</strong> The Company provides a one-year workmanship guarantee on all installations from the date of completion.</p>",
        "<p><strong>3.2</strong> The boiler and heating system components are covered by the manufacturer&rsquo;s warranty, subject to their specific terms and conditions.</p>",
        "<p><strong>3.3</strong> To maintain the validity of the manufacturer&rsquo;s boiler warranty, the Customer must arrange for annual servicing by a qualified professional (this does not have to be the Company).</p>",
        "<p><strong>3.4</strong> We offer free aftercare support for 48 hours following the installation of your new boiler, to resolve any initial issues.</p>"
        "<p><strong>Inclusions:</strong></p><ul><li>Free phone support for troubleshooting.</li><li>On-site visit if the issue can&rsquo;t be resolved over the phone.</li></ul>"
        "<p><strong>Exclusions:</strong></p><ul><li>Damage caused by misuse or neglect. Issues from third-party alterations or work.</li></ul>"
        "<p><strong>How to contact us:</strong></p><ul><li>Reach us by phone or email within 48 hours for assistance. After this period, services will be charged at standard rates.</li></ul>"]),
    ("4. Payment Terms", [
        "<p><strong>4.1</strong> A deposit is required upon acceptance of the quotation. Payment of this deposit constitutes acceptance of these terms and conditions.</p>",
        "<p><strong>4.2</strong> The final balance is due upon completion of the work.</p>",
        "<p><strong>4.3</strong> If payment is not received within two weeks of invoicing, a late payment fee of 2% per week will apply to the outstanding balance.</p>"]),
    ("5. Cancellation Policy", [
        "<p><strong>5.1</strong> The Customer may cancel the service at least 48 hours before work is scheduled to begin for a full refund.</p>",
        "<p><strong>5.2</strong> Cancellations made within 48 hours of the scheduled start date will incur a 20% restocking charge for materials.</p>"]),
    ("6. Customer Responsibilities", [
        "<p><strong>6.1</strong> The Customer must ensure the work area is clear and safe before installation or servicing begins.</p>",
        "<p><strong>6.2</strong> If unforeseen issues arise, such as hidden pipework defects, structural problems, or outdated system incompatibilities, work will pause until a revised price is agreed upon.</p>",
        "<p><strong>6.3</strong> The Company is not responsible for faults in existing pipework that occur after a power flush or system upgrade to higher pressure.</p>"]),
    ("7. Liability and Indemnity", [
        "<p><strong>7.1</strong> The Company takes reasonable precautions to prevent damage to the Customer&rsquo;s property during installation or servicing.</p>",
        "<p><strong>7.2</strong> The Company shall not be liable for:</p><ul><li>Pre-existing defects in the heating system.</li><li>Undersized gas pipework unless previously discussed.</li>"
        "<li>Damage resulting from old or deteriorating pipework when upgrading to a pressurised system.</li>"
        "<li>Loss of heating or hot water due to issues beyond the Company&rsquo;s control, such as gas supply interruptions.</li></ul>",
        "<p><strong>7.3</strong> The Customer agrees to indemnify the Company against any claims arising from improper use or maintenance of installed equipment.</p>",
        "<p><strong>7.4</strong> Whilst all reasonable care will be taken during the execution of the works, no responsibility can be accepted for any faults or failures that may occur to existing pipework, fittings, equipment, etc., due to disturbance caused by the proposed works.</p>"]),
    ("8. Issues and Complaints", [
        "<p><strong>8.1</strong> If the Customer identifies an issue with the installation or service, the Company will make reasonable efforts to address and resolve the problem.</p>",
        "<p><strong>8.2</strong> In the event of an unresolved issue, the Customer may withhold up to 10% of the final payment until the issue is resolved. The Customer may not withhold more than 10% under any circumstances.</p>"]),
    ("9. Compliance and Data Protection", [
        "<p><strong>9.1</strong> The Company complies with UK data protection laws in handling customer information.</p>",
        "<p><strong>9.2</strong> The Company follows Environmental Agency regulations concerning waste disposal and environmental safety.</p>"]),
    ("10. Applicability to Residential and Commercial Customers", [
        "<p><strong>10.1</strong> These terms and conditions apply equally to residential and commercial properties requiring boiler installation, servicing, or heating system upgrades.</p>"]),
]

CSS = """<style id="fx-terms">
.fx-terms{max-width:820px;margin:0 auto}
.fx-terms h2{font-size:24px;margin:40px 0 14px}
.fx-terms h2:first-of-type{margin-top:0}
.fx-terms p,.fx-terms li{font-size:16px;line-height:1.7;color:#333}
.fx-terms p{margin:0 0 12px}
.fx-terms ul{margin:0 0 14px;padding-left:22px}
.fx-terms li{margin:0 0 6px}
.fx-terms .fx-terms-note{background:#F6F4FC;border:1px solid #E6E0F7;border-radius:14px;padding:18px 20px;margin-top:36px}
.fx-terms .fx-terms-note p{margin:0}
</style>"""


def main():
    tpl = open(TEMPLATE, encoding="utf-8").read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', tpl, re.S)
    business = next(g for g in json.loads(m.group(1))["@graph"] if g.get("@type") == "HVACBusiness")
    url = BASE + "/terms-and-conditions/"
    title = "Terms & Conditions | Flotech Heating and Plumbing"
    desc = ("Flotech Heating & Plumbing Ltd terms and conditions for boiler installation, servicing and heating upgrades: "
            "guarantees, payment, cancellation and more.")
    body = "".join(f"<h2>{h}</h2>" + "".join(ps) for h, ps in SECTIONS)
    note = ('<div class="fx-terms-note"><p>Questions about these terms? Call us on <a href="tel:+441279598972">01279 598 972</a> '
            'or email <a href="mailto:office@flotechheating.co.uk">office@flotechheating.co.uk</a>.</p></div>')
    main_html = ('<div class="fx">' + CSS + '<section class="fx-sec"><div class="fx-wrap"><div class="fx-terms">'
                 + body + note + "</div></div></section></div>")
    graph = [{"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-GB",
              "breadcrumb": {"@id": url + "#breadcrumb"}},
             {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Terms & Conditions", "item": url}]}, business]
    schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}) + "</script>"
    out = page(tpl, url, title, desc, "Flotech Heating &amp; Plumbing Ltd", "Terms &amp;", "Conditions",
               "Our terms and conditions for boiler installation, servicing and heating system upgrades.", "regular", main_html, schema)
    # No stats block on a legal page
    i = out.find("The numbers speak for themselves")
    if i > 0:
        s = out.rfind('<div class="elementor-element', 0, out.rfind('e-parent', 0, i))
        s = out.rfind('<div class="elementor-element', 0, out.rfind('e-parent', 0, i) + 1)
        out = out[:s] + out[balanced_div(out, s):]
    os.makedirs(os.path.join(SITE, "terms-and-conditions"), exist_ok=True)
    open(os.path.join(SITE, "terms-and-conditions", "index.html"), "w", encoding="utf-8").write(out)
    sm = os.path.join(SITE, "sitemap.xml")
    s = open(sm, encoding="utf-8").read()
    if url not in s:
        s = s.replace("\n</urlset>", f"\n  <url><loc>{url}</loc></url>\n</urlset>")
        open(sm, "w", encoding="utf-8").write(s)
    print("terms page built", len(title), len(desc))


if __name__ == "__main__":
    main()
