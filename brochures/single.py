"""One PDF per care plan, A5 pages, emailed to customers (Tim, 17 Nov 2026). Draft for Darren to check.

    python3 brochures/single.py [priority-homeowner ...]   -> out/Flotech-Care-Plans-Priority-*.pdf

  page 1: the plan's name, why it matters (warranty or the law), three reasons to join
  page 2: the plan box, what's included, the 12-point service, QR code / link to join
  page 3 (Certificate and Plus only): the plan's own feature: the gas safety certificate, or the free call-out
  last page: the full plan terms, written out (nothing points to the website)
Phone, website, email and join link are clickable. Shares the look, band and plan facts with build.py (the
printed two-plan leaflets). Facts and terms should match site/boiler-care-plans/index.html.
"""
import os, subprocess, sys
import build as B
from title_svg import title_svg

HOME_SUB = B.PACKS["homeowner"]["sub"]
LAND_SUB = B.PACKS["landlord"]["sub"]

# What every plan includes (title, one line of detail)
SERVICE = ("12-point annual boiler service", "By our Gas Safe engineers, to your boiler manufacturer&rsquo;s instructions.")
PRIORITY = ("Priority booking", "When something goes wrong, you go to the front of our queue in normal working hours. We can&rsquo;t promise a set response time.")
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
        "terms": "", "roomy": True, "v2": True,
        "terms_full": [
            ("Paying for your plan", [
                ("Paying", "&pound;9 a month by Direct Debit, including VAT."),
                ("Your price", "Fixed for 12 months, even if our service price goes up during that time."),
                ("Renewing", "Your plan renews each year. At renewal your price only changes if our standard service price has changed, and we tell you at least 28 days before. You can choose not to renew."),
                ("Cancelling", "You can cancel within 14 days of getting your agreement, and you only pay for work already done. After that, your plan runs to the end of its 12 months."),
                ("Missed payments", "If a payment is missed, we let you know and take it again. If it&rsquo;s still unpaid after 14 days, priority booking is paused until you&rsquo;re up to date. If two payments are missed, we may end your plan. If we&rsquo;ve already done your service, you then pay the rest of its normal price, less what you&rsquo;ve paid."),
                ("Moving home", "Moving within our area? Your plan moves with you, and we check the boiler at your new home is in good working order at its first visit. If you move outside our area, your plan ends and you only pay for work already done."),
            ]),
            ("Your yearly service", [
                ("Booking your service", "We send you one reminder a year. Call or message us and we&rsquo;ll book a time that suits you."),
                ("Your boiler warranty", "Most manufacturers only keep the warranty valid if the boiler is serviced every year. Your plan includes that service, so please book it when we remind you."),
                ("Your first service", "We also check your boiler is in good working order and can be serviced safely. If it needs a repair, we give you the price first."),
                ("Older boilers", "Boilers over 5 years old may need new burner seals at the service. This costs &pound;40, and we always tell you before we fit them."),
                ("In winter", "We sometimes move service appointments, because our priority is getting people without heating or hot water warm and safe again."),
                ("Access", "Please be in at the appointment time and keep the area around the boiler clear. If we can&rsquo;t get in twice in a row, we may charge for the extra visit."),
                ("Your safety comes first", "If an appliance is unsafe and can&rsquo;t be made safe straight away, we label it with a warning notice and it mustn&rsquo;t be used until the fault is fixed."),
            ]),
            ("Repairs and priority booking", [
                ("Priority booking", "You go to the front of our queue in normal working hours. We always get to you as soon as we can, but we can&rsquo;t promise a set response time."),
                ("Repairs and parts", "Not included. If something needs fixing, we give you the price first and only start once you&rsquo;re happy."),
                ("Gas safety certificate", "Not included. If you need one, Priority Certificate is &pound;13 a month."),
            ]),
            ("Your agreement with us", [
                ("Who can join", "Homes in our area with one natural gas or oil boiler designed for home use, up to 70kW."),
                ("Not insurance", "This is a service and maintenance agreement provided directly by Flotech Heating and Plumbing Ltd. All work is carried out by our own Gas Safe registered engineers."),
                ("Our responsibility", "We carry out all work with reasonable care and skill, and we&rsquo;re responsible for any damage our work causes. We&rsquo;re not responsible for faults that were already there, normal wear and tear, or parts and appliances we didn&rsquo;t fit or work on. Nothing here affects your legal rights."),
                ("Your details", "We only use your details to run your plan: bookings, reminders and payments. We never sell them. See <a href=\"https://flotechheating.co.uk/privacy-policy/\">flotechheating.co.uk/privacy-policy</a>."),
                ("Questions or complaints", "Just call us on <a href=\"tel:+441279598972\">01279 598 972</a> or email <a href=\"mailto:office@flotechheating.co.uk\">office@flotechheating.co.uk</a> and we&rsquo;ll sort it out."),
            ]),
        ],
    },
    "priority-certificate": {
        "base": B.CERT, "for": "For landlords", "lines": ("Priority", "Certificate"), "sub": LAND_SUB,
        "why": [("pound", "Spread the cost", "&pound;13 a month instead of &pound;156 in one go. The same price, with no big bill to plan for.")],
        "intro": "The same &pound;156 as a service and gas safety certificate booked separately, split into 12 payments, with priority booking and the admin done for you.",
        "items": [SERVICE, CERT, CERT_REMIND, ("Priority booking", "Front of our queue when something goes wrong, in normal working hours."), REMINDER, WARRANTY],
        "box": "gas",
        "not": ["Call-outs, repairs and parts (normal rates, and we always tell you the price first)",
                "Other gas appliances, such as a gas fire (tell us and we&rsquo;ll quote to add them)",
                "More than one property (each property needs its own plan)"],
        "terms": " You must give your tenants a copy of the certificate within 28 days of the check, and keep your records.",
        "v2": True, "page2_box": "gas", "join": False, "terms_split": 2,
        "terms_full": [
            ("Paying for your plan", [
                ("Paying", "&pound;13 a month by Direct Debit, including VAT."),
                ("Your price", "Fixed for 12 months, even if our service or certificate prices go up during that time."),
                ("Renewing", "Your plan renews each year. At renewal your price only changes if our standard service or certificate prices have changed, and we tell you at least 28 days before. You can choose not to renew."),
                ("Cancelling", "You can cancel within 14 days of getting your agreement, and you only pay for work already done. After that, your plan runs to the end of its 12 months."),
                ("Missed payments", "If a payment is missed, we let you know and take it again. If it&rsquo;s still unpaid after 14 days, priority booking is paused until you&rsquo;re up to date. If two payments are missed, we may end your plan. If we&rsquo;ve already done your service and certificate, you then pay the rest of their normal price, less what you&rsquo;ve paid."),
                ("Changing property", "Selling or no longer renting out the property? Your plan can move to another property of yours in our area, and we check that boiler is in good working order at its first visit. Otherwise your plan ends and you only pay for work already done."),
            ]),
            ("Your gas safety certificate", [
                ("What it covers", "Your boiler and gas hob. A landlord&rsquo;s certificate must cover every gas appliance and flue you provide, so if there are others, such as a gas fire, tell us when you join and we&rsquo;ll quote to include them."),
                ("Your tenants&rsquo; own appliances", "Not covered. Your legal duty is for the appliances and flues you provide."),
                ("Giving tenants a copy", "Your certificate is emailed to you. By law, you must give existing tenants a copy within 28 days of the check, and new tenants a copy before they move in."),
                ("Keeping records", "You must keep each certificate for at least 2 years. We keep a copy too, so just ask if you need another."),
                ("Before it runs out", "We remind you before your certificate expires. The check can be done up to 2 months early and your renewal date stays the same, so nothing is lost by booking in good time."),
                ("If something fails the check", "We tell you what&rsquo;s needed and give you the price first. If an appliance is unsafe, we label it with a warning notice and it mustn&rsquo;t be used until it&rsquo;s fixed."),
                ("One plan per property", "Each rented property needs its own plan and its own certificate."),
            ]),
            ("Your yearly service", [
                ("Booking", "We send you a reminder when your service and certificate are due. Call or message us and we&rsquo;ll book a time that suits you."),
                ("Your boiler warranty", "Most manufacturers only keep the warranty valid if the boiler is serviced every year. Your plan includes that service, so please book it when we remind you."),
                ("Your first service", "We also check your boiler is in good working order and can be serviced safely. If it needs a repair, we give you the price first."),
                ("Older boilers", "Boilers over 5 years old may need new burner seals at the service. This costs &pound;40, and we always tell you before we fit them."),
                ("In winter", "We sometimes move service appointments, because our priority is getting people without heating or hot water warm and safe again."),
                ("Access", "Please make sure we can get in at the appointment time (arranging it with your tenants) and that the area around the boiler is clear. If we can&rsquo;t get in twice in a row, we may charge for the extra visit."),
            ]),
            ("Repairs and priority booking", [
                ("Priority booking", "You go to the front of our queue in normal working hours. We always get to you as soon as we can, but we can&rsquo;t promise a set response time."),
                ("Repairs and parts", "Not included. If something needs fixing, we give you the price first and only start once you&rsquo;re happy."),
            ]),
            ("Your agreement with us", [
                ("Who can join", "Properties in our area with one natural gas or oil boiler designed for home use, up to 70kW. Each property needs its own plan."),
                ("Not insurance", "This is a service and maintenance agreement provided directly by Flotech Heating and Plumbing Ltd. All work is carried out by our own Gas Safe registered engineers."),
                ("Our responsibility", "We carry out all work with reasonable care and skill, and we&rsquo;re responsible for any damage our work causes. We&rsquo;re not responsible for faults that were already there, normal wear and tear, or parts and appliances we didn&rsquo;t fit or work on. Nothing here affects your legal rights."),
                ("Your details", "We only use your details to run your plan: bookings, reminders and payments. We never sell them. See <a href=\"https://flotechheating.co.uk/privacy-policy/\">flotechheating.co.uk/privacy-policy</a>."),
                ("Questions or complaints", "Just call us on <a href=\"tel:+441279598972\">01279 598 972</a> or email <a href=\"mailto:office@flotechheating.co.uk\">office@flotechheating.co.uk</a> and we&rsquo;ll sort it out."),
            ]),
        ],
    },
    "priority-plus": {
        "base": None, "for": "For homeowners and landlords", "lines": ("Priority", "Plus"),
        "sub": ("Miss your yearly service and most manufacturers can refuse a warranty claim. Priority Plus covers your service, "
                "gas safety certificate and a free call-out every year, for <b>&pound;28 a month</b>."),
        "why": [("tool", "A free call-out every year", "If something stops working, your first call-out each year is free, with the first hour of labour included.")],
        "intro": "Everything in Priority Certificate, plus a free call-out every year, an inhibitor top-up and your unvented cylinder checked.",
        "items": [SERVICE, CERT, CALLOUT, INHIBITOR, UNVENTED,
                  ("Priority booking", "Front of our queue when something goes wrong, in normal working hours."),
                  ("Reminders", "When your service is due and before your certificate runs out."),
                  ("Warranty call-outs handled", "We arrange warranty visits with the manufacturer and follow them up for you.")],
        "box": "callout",
        "not": ["Parts, on any job (normal rates, and we always tell you the price first)",
                "Labour after the first hour, and call-outs after your free one each year"],
        "terms": (" The free call-out is in normal working hours, can be used once your plan has been running for 30 days, doesn&rsquo;t carry "
                  "over, and doesn&rsquo;t cover faults that were already there when you joined."),
        "v2": True, "terms_split": 2, "page2_box": "gas", "join": False, "feature": {
            "title": "Your free call-out", "box": "callout", "layout": "callout",
            "intro": "If something stops working, your first call-out each plan year is free, including the first hour of labour. Fixed within that hour? You only pay for any parts.",
            "sections": [("How it works", [
                ("Longer jobs", "If a fix takes more than an hour, we give you a price for the rest before we carry on. You decide."),
                ("When you can use it", "Once your plan has been running for 30 days, in normal working hours. It doesn&rsquo;t carry over if you don&rsquo;t use it."),
                ("What it doesn&rsquo;t cover", "Parts, on any job, and faults that were already there when you joined. Other call-outs are charged at our normal rate."),
            ]), ("Also on Priority Plus", [
                ("Inhibitor top-up", "Inhibitor is a liquid in your heating that stops radiators, pipes and your boiler rusting and filling with sludge. It weakens over the year, so we test it at your service and top it up."),
                ("Unvented cylinder check", "If you have an unvented hot water cylinder, we check it and its safety valves at the same visit."),
            ])]},
        "terms_full": [
            ("Paying for your plan", [
                ("Paying", "&pound;28 a month by Direct Debit, including VAT."),
                ("Your price", "Fixed for 12 months, even if our prices go up during that time."),
                ("Renewing", "Your plan renews each year. At renewal your price only changes if our standard prices have changed, and we tell you at least 28 days before. You can choose not to renew."),
                ("Cancelling", "You can cancel within 14 days of getting your agreement, and you only pay for work already done. After that, your plan runs to the end of its 12 months."),
                ("Missed payments", "If a payment is missed, we let you know and take it again. If it&rsquo;s still unpaid after 14 days, priority booking and your free call-out are paused until you&rsquo;re up to date. If two payments are missed, we may end your plan, and you pay the normal price of any work already done, less what you&rsquo;ve paid."),
                ("Moving home", "Moving within our area? Your plan moves with you, and we check the boiler at your new home is in good working order at its first visit. If you move outside our area, your plan ends and you only pay for work already done."),
            ]),
            ("Your gas safety certificate", [
                ("What it covers", "Your boiler and gas hob, emailed to you after the check. A landlord&rsquo;s certificate must cover every gas appliance and flue you provide, so if there are others, such as a gas fire, tell us when you join and we&rsquo;ll quote to include them."),
                ("Landlords", "Your tenants&rsquo; own appliances aren&rsquo;t covered. By law, you must give existing tenants a copy within 28 days of the check and new tenants a copy before they move in, and keep each certificate for at least 2 years. We keep a copy too, so just ask if you need another."),
                ("Before it runs out", "We remind you before your certificate expires. The check can be done up to 2 months early and your renewal date stays the same, so nothing is lost by booking in good time."),
                ("If something fails the check", "We tell you what&rsquo;s needed and give you the price first. If an appliance is unsafe, we label it with a warning notice and it mustn&rsquo;t be used until it&rsquo;s fixed."),
            ]),
            ("Your yearly service", [
                ("Booking", "We send you a reminder when your service and certificate are due. Call or message us and we&rsquo;ll book a time that suits you."),
                ("Your boiler warranty", "Most manufacturers only keep the warranty valid if the boiler is serviced every year. Your plan includes that service, so please book it when we remind you."),
                ("Your first service", "We also check your boiler is in good working order and can be serviced safely. If it needs a repair, we give you the price first."),
                ("Older boilers", "Boilers over 5 years old may need new burner seals at the service. This costs &pound;40, and we always tell you before we fit them."),
                ("In winter", "We sometimes move service appointments, because our priority is getting people without heating or hot water warm and safe again."),
                ("Access", "Please be in at the appointment time and keep the area around the boiler clear. If we can&rsquo;t get in twice in a row, we may charge for the extra visit."),
            ]),
            ("Repairs and priority booking", [
                ("Priority booking", "You go to the front of our queue in normal working hours. We can&rsquo;t promise a set response time."),
                ("Repairs and parts", "Parts are never included. Other repairs are charged at our normal rates, and we always give you the price first."),
            ]),
            ("Your agreement with us", [
                ("Who can join", "Properties in our area with one natural gas or oil boiler designed for home use, up to 70kW. Landlords need one plan per property."),
                ("Not insurance", "This is a service and maintenance agreement provided directly by Flotech Heating and Plumbing Ltd. All work is carried out by our own Gas Safe registered engineers."),
                ("Our responsibility", "We carry out all work with reasonable care and skill, and we&rsquo;re responsible for any damage our work causes. We&rsquo;re not responsible for faults that were already there, normal wear and tear, or parts and appliances we didn&rsquo;t fit or work on. Nothing here affects your legal rights."),
                ("Your details", "We only use your details to run your plan: bookings, reminders and payments. We never sell them. See <a href=\"https://flotechheating.co.uk/privacy-policy/\">flotechheating.co.uk/privacy-policy</a>."),
                ("Questions or complaints", "Just call us on <a href=\"tel:+441279598972\">01279 598 972</a> or email <a href=\"mailto:office@flotechheating.co.uk\">office@flotechheating.co.uk</a> and we&rsquo;ll sort it out."),
            ]),
        ],
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
/* v2 layout (Priority Homeowner first; Tim, 17 Nov 2026): emailed, so no "serviced on" boxes, links clickable */
a { color: inherit; text-decoration: none; }
.cover.v2 .why { margin-top: 7mm; gap: 3.6mm; }
.cover.v2 .why .b { padding: 4.4mm 5mm; }
.cover.v2 .join { margin-top: 3mm; width: 100%; text-align: left; justify-content: center; }
.cover.v2 .join img { width: 17mm; height: 17mm; }
.cover.v2 .join .j p a { color: #6a2fe0; text-decoration: underline; text-underline-offset: 1.5px; }
.v2b { padding: 7mm 9mm 0; }
.v2b { height: 210mm; display: flex; flex-direction: column; justify-content: space-between; gap: 3.5mm; padding-bottom: 30mm; }   /* spread the four blocks evenly down to the band */
.v2b .logo-row { display: flex; align-items: center; justify-content: space-between; }
.v2b .logo-row img { height: 8.5mm; width: auto; }
.v2b .logo-row span { font-size: 8pt; font-weight: 800; letter-spacing: 1.6px; text-transform: uppercase; color: #7a3fe0; }
.hero-card { margin-top: 0; border-radius: 4mm; padding: 3.8mm 5.5mm; color: #fff; display: flex; align-items: center; justify-content: space-between; }
.hero-card .ey { font-size: 7.4pt; font-weight: 800; letter-spacing: 1.6px; text-transform: uppercase; opacity: .92; }
.hero-card .nm { margin-top: .8mm; font-size: 21pt; font-weight: 800; line-height: 1.02; }
.hero-card .pr { text-align: right; }
.hero-card .pr b { font-size: 27pt; font-weight: 800; line-height: 1; }
.hero-card .pr b small { font-size: 10pt; font-weight: 700; }
.hero-card .pr p { margin-top: .8mm; font-size: 7.6pt; font-weight: 700; opacity: .92; }
.bx { margin-top: 2.7mm; border: 1px solid #e7e3f1; border-radius: 3.5mm; padding: 3.2mm 4.2mm 3.4mm; background: #fbfaff; }
.bx h4 { font-size: 10pt; font-weight: 800; margin-bottom: 2.4mm; }
.inc { display: grid; grid-template-columns: 1fr 1fr; gap: 2.2mm 4.5mm; }
.inc > div { display: flex; gap: 1.8mm; }
.inc svg { width: 3.8mm; height: 3.8mm; flex: none; margin-top: .1mm; }
.inc b { display: block; font-size: 9pt; font-weight: 800; line-height: 1.2; }
.inc p { margin-top: .4mm; font-size: 7.5pt; line-height: 1.3; font-weight: 600; color: #4b465c; }
.bx.checks { margin-top: 2.7mm; padding: 3.2mm 4.2mm 3.4mm; }
.bx.checks h4 { font-size: 10pt; }
.how { display: grid; grid-template-columns: 1fr 1fr; gap: 2.2mm 4.5mm; }
.how b { display: block; font-size: 8pt; font-weight: 800; line-height: 1.2; }
.how p { margin-top: .3mm; font-size: 7.2pt; line-height: 1.32; font-weight: 600; color: #3b3848; }
.v2b .join { margin-top: 3.2mm; gap: 4mm; }
.v2b .join img { width: 17mm; height: 17mm; }
.v2b .join .j b { font-size: 12pt; }
.v2b .join .j p { font-size: 9pt; }
.v2b .join .j p a { color: #6a2fe0; text-decoration: underline; text-underline-offset: 1.5px; }
.co { margin-top: 2.6mm; font-size: 6.4pt; font-weight: 600; color: #6b6680; }
/* page 2 with room to breathe, and the terms page */
.v2b .bx { margin-top: 0; padding: 4mm 4.8mm; }
.v2b .bx h4 { font-size: 11pt; margin-bottom: 3mm; }
.v2b .inc { gap: 3.4mm 5mm; }
.v2b .inc b { font-size: 10pt; }
.v2b .inc p { font-size: 8.2pt; margin-top: .6mm; }
.v2b .inc svg { width: 4.2mm; height: 4.2mm; }
.v2b .checks ul { gap: 2.2mm 3mm; }
.v2b .checks li { font-size: 8pt; }
.v2b .checks li svg { width: 3.3mm; height: 3.3mm; }
.v2b .join { margin-top: 0; gap: 5mm; }
.v2b .join img { width: 24mm; height: 24mm; }
.v2b .join .j b { font-size: 13.5pt; }
.v2b .join .j p { font-size: 9.6pt; }
.v2t { padding: 7mm 9mm 0; }
.thead { display: flex; align-items: center; justify-content: space-between; }
.thead .ey { font-size: 7.6pt; font-weight: 800; letter-spacing: 1.4px; text-transform: uppercase; color: #7a3fe0; }
.thead h2 { margin-top: .6mm; font-size: 17pt; font-weight: 800; line-height: 1.05; }
.thead img { height: 8.5mm; width: auto; }
.tcols { margin-top: 3.4mm; column-count: 2; column-gap: 5mm; }
.tsec { margin-bottom: 2.6mm; }
.tsec h4 { break-after: avoid; font-size: 8.6pt; font-weight: 800; color: #6a2fe0; padding-bottom: .9mm; margin-bottom: 1.2mm; border-bottom: 1px solid #e3dcf5; }
.tsec p { font-size: 7.2pt; line-height: 1.36; font-weight: 600; color: #3b3848; margin-bottom: 1.1mm; break-inside: avoid; }
.tsec p b { color: #14121c; font-weight: 800; }
.tsec a { color: #6a2fe0; }
.v2t .co { position: absolute; left: 9mm; bottom: 28mm; margin: 0; }
.v2t.dense .tsec p { line-height: 1.32; margin-bottom: .8mm; }
.v2t.dense .tsec { margin-bottom: 2.2mm; }
.v2b.dense { gap: 2.6mm; }
.v2b.dense .inc p { font-size: 7.9pt; }
.v2b.dense .checks ul { gap: 1.8mm 3mm; }
.v2b.dense .inc { gap: 2.2mm 5mm; }
.v2b.dense .bx { padding: 3.4mm 4.8mm; }
.v2b.dense .bx h4 { margin-bottom: 2.4mm; }
.v2t.roomy .tsec p { font-size: 8.4pt; line-height: 1.45; margin-bottom: 1.8mm; }
.v2t.roomy .tsec h4 { font-size: 10pt; margin-bottom: 1.8mm; }
.v2t.roomy .tsec { margin-bottom: 4mm; }

/* Priority Plus call-out page */
.v2c { padding: 7mm 9mm 33mm; height: 210mm; display: flex; flex-direction: column; justify-content: space-between; gap: 4mm; }
.v2c .bx { margin-top: 0; padding: 4.4mm 5mm; }
.v2c .bx h4 { font-size: 10.6pt; margin-bottom: 2.6mm; }
.stats { border-radius: 4mm; color: #fff; display: grid; grid-template-columns: repeat(3, 1fr); padding: 3.4mm 2mm; }
.stats div { text-align: center; padding: 0 2mm; }
.stats div + div { border-left: 1px solid rgba(255,255,255,.35); }
.stats b { display: block; font-size: 19pt; font-weight: 800; line-height: 1; }
.stats span { display: block; margin-top: 1mm; font-size: 7.8pt; font-weight: 700; line-height: 1.25; opacity: .95; }
.ric { width: 8mm; height: 8mm; border-radius: 50%; display: grid; place-items: center; flex: none; }
.ric svg { width: 4.6mm; height: 4.6mm; }
.cvs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }
.cv b { display: block; margin: 1.8mm 0 1.4mm; font-size: 9.2pt; font-weight: 800; }
.cv ul { list-style: none; display: grid; gap: 1.1mm; }
.cv li { display: flex; gap: 1.3mm; font-size: 7.6pt; line-height: 1.28; font-weight: 600; color: #3b3848; }
.cv li svg { width: 2.9mm; height: 2.9mm; flex: none; margin-top: .2mm; }
.sts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; }
.st .n { width: 6mm; height: 6mm; border-radius: 50%; display: grid; place-items: center; color: #fff; font-size: 9pt; font-weight: 800; }
.st b { display: block; margin-top: 1.6mm; font-size: 9.2pt; font-weight: 800; }
.st p { margin-top: .6mm; font-size: 7.6pt; line-height: 1.32; font-weight: 600; color: #3b3848; }
.good { list-style: none; margin-top: 2.6mm; padding-top: 2.2mm; border-top: 1px solid #e7e3f1; display: grid; grid-template-columns: 1fr 1fr; gap: 1.4mm 4mm; }
.good li { display: flex; gap: 1.6mm; font-size: 7.6pt; line-height: 1.3; font-weight: 600; color: #3b3848; }
.good i { width: 1.6mm; height: 1.6mm; border-radius: 50%; background: #9B51FF; flex: none; margin-top: 1.1mm; }
.als { display: grid; grid-template-columns: 1fr 1fr; gap: 3.4mm; }
.al { display: flex; gap: 2.6mm; border: 1px solid #e7e3f1; border-radius: 3.5mm; padding: 3.4mm 3.8mm; background: #fbfaff; }
.al b { display: block; font-size: 9.2pt; font-weight: 800; }
.al p { margin-top: .6mm; font-size: 7.6pt; line-height: 1.32; font-weight: 600; color: #3b3848; }
.v2c .join { margin-top: 0; gap: 5mm; }
.v2c .join img { width: 20mm; height: 20mm; }
.v2c .join .j b { font-size: 12.5pt; }
.v2c .join .j p { font-size: 9.4pt; }
.v2c .join .j p a { color: #6a2fe0; text-decoration: underline; text-underline-offset: 1.5px; }

/* Priority Plus extras page */
.v2x { padding: 7mm 9mm 30mm; height: 210mm; display: flex; flex-direction: column; justify-content: space-between; gap: 3mm; }
.xc { border: 1px solid #e7e3f1; border-radius: 4mm; background: #fbfaff; padding: 3.8mm 5mm 4mm; }
.xh { display: flex; align-items: center; gap: 3mm; }
.xh .ric { width: 10mm; height: 10mm; }
.xh .ric svg { width: 5.6mm; height: 5.6mm; }
.xh b { font-size: 13pt; font-weight: 800; }
.xg { margin-top: 2.6mm; display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.xc h5 { font-size: 8.4pt; font-weight: 800; color: #6a2fe0; text-transform: uppercase; letter-spacing: .8px; margin-bottom: 1mm; }
.xc p { font-size: 8pt; line-height: 1.4; font-weight: 600; color: #3b3848; }
.xc > h5 { margin-top: 2.8mm; }
.xc ul { list-style: none; display: grid; gap: 1.4mm; }
.xc li { display: flex; gap: 1.8mm; font-size: 8pt; line-height: 1.3; font-weight: 600; color: #14121c; }
.xc li svg { width: 3.5mm; height: 3.5mm; flex: none; margin-top: .1mm; }
.v2x .join { margin-top: 0; gap: 5mm; }
.v2x .join img { width: 20mm; height: 20mm; }
.v2x .join .j b { font-size: 13pt; }
.v2x .join .j p { font-size: 9.6pt; }
.v2x .join .j p a { color: #6a2fe0; text-decoration: underline; text-underline-offset: 1.5px; }
/* feature page (Priority Certificate: the certificate; Priority Plus: the free call-out) */
.v2f { padding: 7mm 9mm 33mm; height: 210mm; display: flex; flex-direction: column; justify-content: space-between; }
.v2f .bx { margin-top: 0; padding: 4mm 4.8mm; }
.v2f .bx h4 { font-size: 11pt; margin-bottom: 2.8mm; }
.fintro { font-size: 10pt; line-height: 1.45; font-weight: 600; color: #3b3848; }
.v2f .checks ul { gap: 2.4mm 4mm; }
.v2f .checks li { font-size: 8.6pt; }
.v2f .checks li svg { width: 3.5mm; height: 3.5mm; }
.v2f .cov { gap: 4mm; }
.v2f .cov b { font-size: 9.4pt; margin-bottom: 1mm; }
.v2f .cov p { font-size: 8.2pt; line-height: 1.4; }
.fsec p { font-size: 8.4pt; line-height: 1.42; font-weight: 600; color: #3b3848; margin-bottom: 1.8mm; }
.fsec p:last-child { margin-bottom: 0; }
.fsec p b { color: #14121c; font-weight: 800; }
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


def band_links():
    """The shared band, with the phone, website and email clickable (these PDFs are emailed)."""
    return (B.band().replace(f'<div class="num">{B.PHONE}</div>', f'<div class="num"><a href="tel:{B.TEL}">{B.PHONE}</a></div>')
            .replace(f'{B.WEB}<br>{B.EMAIL}', f'<a href="https://{B.WEB}/">{B.WEB}</a><br><a href="mailto:{B.EMAIL}">{B.EMAIL}</a>'))


def box2(kind):
    """The plan's own second box on page 2: what the gas safety check covers, or what the free call-out covers."""
    if kind == "gas":
        order = list(GAS_CHECKS)   # the one item that wraps goes to the bottom of its column
        i, j = order.index("Flue flow test, so fumes are removed safely"), order.index("Flame failure devices working properly")
        order[i], order[j] = order[j], order[i]
        items = "".join(f"<li>{B.TICK}<span>{x}</span></li>" for x in order)
        return f'<div class="bx checks two"><h4>What your gas safety check covers</h4><ul>{items}</ul></div>'
    if kind == "callout":
        cols = "".join(f"<div><b>{t}</b><p>{d}</p></div>" for t, d in CALLOUT_COVERS)
        return f'<div class="bx"><h4>What your free call-out covers</h4><div class="cov">{cols}</div></div>'
    return ""


LINE_ICONS = {   # simple 24px line icons, drawn in the brand gradient circle like the cover icons
    "boiler": '<rect x="6" y="3.5" width="12" height="17" rx="2"/><path d="M9 8h6M12 17.5c-1.6 0-2.6-1-2.6-2.4 0-1.6 1.4-2.3 1.7-3.8 1.9 1 3.5 2.4 3.5 3.9 0 1.3-1 2.3-2.6 2.3z"/>',
    "radiator": '<path d="M5 6v12M9.5 6v12M14.5 6v12M19 6v12M3 9h18M3 15h18"/>',
    "tap": '<path d="M4 8.5h8.5a3.5 3.5 0 0 1 3.5 3.5v1.5M8 8.5V5.5M5.5 5.5h5"/><path d="M16 16.5c.9 1.2 1.4 2 1.4 2.6a1.4 1.4 0 0 1-2.8 0c0-.6.5-1.4 1.4-2.6z"/>',
    "drop": '<path d="M12 3.5c3 4 5.5 6.6 5.5 10a5.5 5.5 0 0 1-11 0c0-3.4 2.5-6 5.5-10z"/><path d="M9.5 14a2.5 2.5 0 0 0 2.5 2.5"/>',
    "cylinder": '<rect x="7" y="3" width="10" height="18" rx="5"/><path d="M12 7v3M10.5 14h3"/>',
}


def ricon(n):
    return (f'<span class="ric grad"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{LINE_ICONS[n]}</svg></span>')


def callout_page(name, price, url):
    covers = [("boiler", "Boiler and controls", ["Your boiler and flue", "Programmer and thermostats", "Zone valves and pump"]),
              ("radiator", "Central heating", ["Radiators and their valves", "Expansion tank and air vents", "Heating pipework", "Hot water cylinder and immersion"]),
              ("tap", "Plumbing", ["Leaking pipes and joints", "Overflows, soil and vent pipes", "Water tanks", "Pipes from your stopcock to your taps and showers"])]
    cov = "".join(f'<div class="cv">{ricon(i)}<b>{t}</b><ul>' + "".join(f"<li>{B.TICK}<span>{x}</span></li>" for x in items) + "</ul></div>"
                  for i, t, items in covers)
    steps = [("Call us", "Ring us in normal working hours and we&rsquo;ll book you in as a priority."),
             ("First hour free", "Fixed within the hour? You only pay for any parts."),
             ("Longer job?", "We give you a price for the rest before we carry on. You decide.")]
    st = "".join(f'<div class="st"><span class="n grad">{k}</span><b>{t}</b><p>{d}</p></div>' for k, (t, d) in enumerate(steps, 1))
    good = ["One free call-out each plan year. It doesn&rsquo;t carry over",
            "Other call-outs are charged at our normal rate",
            "Parts aren&rsquo;t included, on any job",
            "Faults that were already there when you joined aren&rsquo;t covered"]
    gd = "".join(f"<li><i></i><span>{g}</span></li>" for g in good)
    return f"""<section class="page v2c">
  <div class="thead"><div><p class="ey">{name} &middot; &pound;{price} a month</p><h2>Your free call-out</h2></div>
    <img src="logo-noslogan-centred.png" alt="Flotech"></div>
  <div class="stats grad"><div><b>1</b><span>free call-out<br>every plan year</span></div><div><b>1 hour</b><span>of labour<br>included</span></div><div><b>30 days</b><span>and it&rsquo;s ready<br>to use</span></div></div>
  <div class="bx"><h4>What it covers</h4><div class="cvs">{cov}</div></div>
  <div class="bx"><h4>How it works</h4><div class="sts">{st}</div><ul class="good">{gd}</ul></div>
  {band_links()}
</section>"""


def extras_page(name, price, url):
    """Priority Plus: the two extra checks at the yearly service, with the QR code to join."""
    cards = [("drop", "Inhibitor top-up",
              "Inhibitor is a liquid in your central heating water. It protects the inside of your radiators, pipes and boiler from rust and sludge.",
              "It gets weaker over the year. When it&rsquo;s low, sludge can build up, leading to cold spots on radiators, a noisy boiler and breakdowns.",
              ["We test the inhibitor level at your yearly service", "We top it up if it&rsquo;s low, as part of your plan"]),
             ("cylinder", "Unvented cylinder check",
              "An unvented hot water cylinder stores hot water at mains pressure, so it has safety valves that release pressure and heat if something goes wrong.",
              "Cylinder manufacturers recommend a check every year to keep those safety devices working, and many need it to keep the cylinder&rsquo;s warranty valid.",
              ["We check the pressure and temperature relief valves", "We check the expansion vessel and the discharge pipe",
               "All at the same visit as your boiler service. No unvented cylinder? Nothing to do."])]
    html = ""
    for i, t, what, why, do in cards:
        dl = "".join(f"<li>{B.TICK}<span>{x}</span></li>" for x in do)
        html += (f'<div class="xc"><div class="xh">{ricon(i)}<b>{t}</b></div>'
                 f'<div class="xg"><div><h5>What it is</h5><p>{what}</p></div><div><h5>Why it matters</h5><p>{why}</p></div></div>'
                 f'<h5>What we do</h5><ul>{dl}</ul></div>')
    return f"""<section class="page v2x">
  <div class="thead"><div><p class="ey">{name} &middot; &pound;{price} a month</p><h2>Also included in your plan</h2></div>
    <img src="logo-noslogan-centred.png" alt="Flotech"></div>
  <p class="fintro">Two extra checks at your yearly service, to keep your heating healthy.</p>
  {html}
  <div class="join"><a href="{url}"><img src="qr-care-plans.svg" alt="QR code to the care plans page"></a>
    <div class="j"><b>Join online, or give us a call</b><p><a href="{url}">{B.WEB}/boiler-care-plans</a></p></div></div>
  {band_links()}
</section>"""


def leaflet_v2(key):
    p = PLANS[key]
    title, top = title_svg(lines=p["lines"])
    why = p["why"] + [("clock", "Save time", "We remind you when your service is due and deal with the manufacturer if you need a warranty call-out."),
                      ("bolt", "Seen first", "If something goes wrong, plan members are booked in before customers who aren&rsquo;t on a plan.")]
    why_html = "".join(f'<div class="b">{B.icon(i)}<div><b>{t}</b><p>{d}</p></div></div>' for i, t, d in why)
    url = f"https://{B.WEB}/boiler-care-plans/"
    cover = f"""<section class="page cover v2">
  <img class="logo" src="logo-centred.png" alt="Flotech Heating and Plumbing">
  <p class="for">{p['for']}</p>
  <h1>{title}</h1>
  <p class="sub">{p['sub']}</p>
  <div class="why">{why_html}</div>
  {band_links()}
</section>"""
    name = " ".join(p["lines"])
    inc = "".join(f"<div>{B.TICK}<div><b>{t}</b><p>{d}</p></div></div>" for t, d in p["items"])
    order = list(B.CHECKS)   # at this width "Boiler operating pressure test" wraps: give it the bottom of column 2
    a, b = order.index("Boiler operating pressure test"), order.index("Water leak check")
    order[a], order[b] = order[b], order[a]
    checks = "".join(f"<li>{B.TICK}<span>{x}</span></li>" for x in order)
    def secs_html(secs):
        return "".join(f'<div class="tsec"><h4>{h}</h4>' + "".join(f"<p><b>{t}.</b> {d}</p>" for t, d in items) + "</div>"
                       for h, items in secs)
    split = p.get("terms_split")   # number of sections on the first terms page, when the terms need two pages
    term_pages = [p["terms_full"][:split], p["terms_full"][split:]] if split else [p["terms_full"]]
    join = (f'<div class="join"><a href="{url}"><img src="qr-care-plans.svg" alt="QR code to the care plans page"></a>'
            f'<div class="j"><b>Join online, or give us a call</b><p><a href="{url}">{B.WEB}/boiler-care-plans</a></p></div></div>')
    back = f"""<section class="page v2b{' dense' if len(p['items']) > 6 or p.get('page2_box') else ''}">
  <div class="hero-card grad"><div><p class="ey">Your boiler care plan</p><p class="nm">{name}</p></div>
    <div class="pr"><b>&pound;{PRICE[key]}<small> /month</small></b><p>Including VAT · 12-month plan</p></div></div>
  <div class="bx"><h4>What&rsquo;s included</h4><div class="inc">{inc}</div></div>
  <div class="bx checks"><h4>What&rsquo;s in your 12-point annual boiler service</h4><ul>{checks}</ul></div>
  {box2(p.get("page2_box"))}
  {join if p.get("join", True) else ""}
  {band_links()}
</section>"""
    f = p.get("feature")
    feature_page = ""
    if f and f.get("layout") == "callout":
        feature_page = extras_page(name, PRICE[key], url) + callout_page(name, PRICE[key], url)
    elif f:
        secs = "".join(f'<div class="bx fsec"><h4>{h}</h4>' + "".join(f"<p><b>{t}.</b> {d}</p>" for t, d in items) + "</div>"
                       for h, items in f["sections"])
        feature_page = f"""<section class="page v2f">
  <div class="thead"><div><p class="ey">{name} &middot; &pound;{PRICE[key]} a month</p><h2>{f['title']}</h2></div>
    <img src="logo-noslogan-centred.png" alt="Flotech"></div>
  <p class="fintro">{f['intro']}</p>
  {box2(f['box'])}
  {secs}
  {band_links()}
</section>"""
    terms_page = ""
    for n, secs in enumerate(term_pages):
        last = n == len(term_pages) - 1
        heading = "Your plan terms" if n == 0 else "Your plan terms, continued"
        co = ('<p class="co">Flotech Heating &amp; Plumbing Ltd, company no. 08739272. These terms apply from the day your plan starts.</p>'
              if last else '<p class="co">Continued on the next page.</p>')
        terms_page += f"""<section class="page v2t{' roomy' if split else ''}">
  <div class="thead"><div><p class="ey">{name} &middot; &pound;{PRICE[key]} a month</p><h2>{heading}</h2></div>
    <img src="logo-noslogan-centred.png" alt="Flotech"></div>
  <div class="tcols">{secs_html(secs)}</div>
  {co}
  {band_links()}
</section>"""
    css = B.CSS + CSS.replace("{TOP:.2f}", f"{top:.2f}")
    return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Flotech {name}</title>
<link rel="stylesheet" href="file://{B.FONTS}"><style>{css}</style></head><body>{cover}{back}{feature_page}{terms_page}</body></html>"""


def main():
    os.makedirs(B.OUT, exist_ok=True)
    for f in ("logo-centred.png", "logo-noslogan-centred.png", "gas-safe-mst.png", "qr-care-plans.svg"):
        src, dst = os.path.join(B.HERE, f), os.path.join(B.OUT, f)
        if not os.path.exists(dst):
            os.symlink(src, dst)
    keys = sys.argv[1:] or list(PLANS)   # e.g. python3 single.py priority-homeowner
    for key in keys:
        html = (leaflet_v2 if PLANS[key].get("v2") else leaflet)(key)
        open(os.path.join(B.OUT, f"flotech-care-plans-{key}.html"), "w", encoding="utf-8").write(html)
    subprocess.run(["node", os.path.join(B.HERE, "render.js"), B.OUT] + keys, check=True)


if __name__ == "__main__":
    main()
