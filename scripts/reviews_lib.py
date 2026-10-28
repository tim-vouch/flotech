"""Shared review helpers: job labels from review text, and the homepage carousel selection."""
import re

# Job labels, checked in order: the first match wins. Boiler installation first, because it's Flotech's lead service.
SERVICES = [
    ("Boiler installation", r"new boiler|replacement boiler|boiler (?:installation|install|replacement|replaced|swap|upgrade)|"
                            r"(?:install|installed|fitted|fit|replaced|changed|supplied) (?:a |the |our |my |us a )?(?:new |replacement )?(?:combi |system |gas )?boiler|"
                            r"boiler (?:and|&) (?:hot )?(?:tank|cylinder) installed|boiler needed to be replaced|fitted boilers"),
    ("Bathroom", r"bathroom (?:upgrade|install|fit|refurb|renovat|work)|new bathroom|shower room|bathroom total"),
    ("Underfloor heating", r"underfloor|under-floor"),
    ("Hot water cylinder", r"cylinder|hot tank|water tank|immersion"),
    ("Power flush", r"power ?flush|system flush|flush of (?:our|the)"),
    ("Radiators", r"radiator"),
    ("Boiler service", r"boiler serv|servic(?:e|ed|ing) (?:our|my|the) (?:gas )?(?:central heating )?boiler|annual (?:boiler )?service|gas (?:safety )?certificate|boiler checks"),
    ("Boiler repair", r"boiler (?:repair|fault|breakdown|issue|problem)|fix(?:ed)? (?:my|our|the) boiler|boiler (?:was|stopped|broke)"),
    ("Central heating", r"central heating|heating system"),
    ("Water softener", r"water softener"),
    ("Shower", r"\bshower"),
    ("Leak repair", r"\bleak"),
    ("Taps and sinks", r"\btap\b|\bsink\b"),
    ("Toilet", r"toilet|cistern"),
]


def service_for(text):
    t = (text or "").lower()
    return next((label for label, rx in SERVICES if re.search(rx, t)), "")


def carousel(reviews, size=15):
    """Five-star reviews that name a job and read well on a card; boiler installations get two of every three slots."""
    ok = [r for r in reviews if r["stars"] == 5 and r.get("service") and 50 <= len(r["text"]) <= 420]
    ok.sort(key=lambda r: r.get("published", ""), reverse=True)
    installs = [r for r in ok if r["service"] == "Boiler installation"]
    others = [r for r in ok if r["service"] != "Boiler installation"]
    picked = []
    while len(picked) < size and (installs or others):
        for src in (installs, installs, others):
            if src and len(picked) < size:
                picked.append(src.pop(0))
        if not installs and not others:
            break
    return picked
