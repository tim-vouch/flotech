#!/usr/bin/env python3
"""Daily Google update for Flotech: rating, review count and new reviews, then rebuilds the review sections.

Runs from .github/workflows/update-reviews.yml. Needs, in the GitHub repo settings:
  secret   GOOGLE_PLACES_API_KEY  (Google Cloud key with "Places API (New)" enabled)
  variable GOOGLE_PLACE_ID        (Flotech's Google Maps place ID)

Google only returns 5 reviews per call, so new ones are added on top of data/google-reviews.json and every
review saved before is kept (the first 214 came from the GHL export, Oct 2026). If someone deletes a review
on Google, remove it from the file by hand.
"""
import datetime, json, os, pathlib, re, subprocess, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from reviews_lib import service_for  # noqa: E402

key, place = os.environ.get("GOOGLE_PLACES_API_KEY"), os.environ.get("GOOGLE_PLACE_ID")
if not key or not place:
    sys.exit("GOOGLE_PLACES_API_KEY or GOOGLE_PLACE_ID is not set")


def get(url, headers=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=30))


data = get(f"https://places.googleapis.com/v1/places/{place}?languageCode=en-GB",
           {"X-Goog-Api-Key": key, "X-Goog-FieldMask": "displayName,rating,userRatingCount,reviews"})
name = data.get("displayName", {}).get("text", "")
if "flotech" not in name.lower():
    sys.exit(f"Refusing to update: GOOGLE_PLACE_ID points at '{name}', not Flotech.")

# Rating and count
rp = ROOT / "data" / "rating.json"
old = json.loads(rp.read_text())
rating, count = f'{data["rating"]:.1f}', str(data["userRatingCount"])
if int(count) < int(old["count"]) - 2:
    sys.exit(f"Refusing to update: Google returned {count} reviews but the site shows {old['count']}.")
rp.write_text(json.dumps({"rating": rating, "count": count}) + "\n")
print(f"Rating: {rating} from {count} reviews")

# Reviews: newest first via the legacy endpoint if the key allows it, plus the standard 5.
fetched = []
try:
    q = urllib.parse.urlencode({"place_id": place, "fields": "reviews", "reviews_sort": "newest", "language": "en-GB", "key": key})
    for r in get(f"https://maps.googleapis.com/maps/api/place/details/json?{q}").get("result", {}).get("reviews", []):
        fetched.append({"name": r.get("author_name", ""), "stars": int(r.get("rating", 0)), "text": r.get("text", ""),
                        "published": datetime.datetime.fromtimestamp(r.get("time", 0)).isoformat(timespec="minutes")})
except Exception as err:
    print("Newest-first reviews not available, using the standard 5:", err)
for r in data.get("reviews", []):
    fetched.append({"name": r.get("authorAttribution", {}).get("displayName", ""), "stars": int(r.get("rating", 0)),
                    "text": (r.get("originalText") or r.get("text") or {}).get("text", ""),
                    "published": (r.get("publishTime") or "")[:16]})

path = ROOT / "data" / "google-reviews.json"
saved = json.loads(path.read_text())
ident = lambda r: (r["name"].strip().lower(), " ".join(r["text"].split())[:80].lower())
known = {ident(r) for r in saved}
added = []
for r in fetched:
    r["text"] = " ".join(r["text"].split())
    if not r["name"] or not r["text"] or ident(r) in known:
        continue
    known.add(ident(r))
    r["service"] = service_for(r["text"])
    added.append(r)
if added:
    added.sort(key=lambda r: r.get("published", ""), reverse=True)
    path.write_text(json.dumps(added + saved, indent=2, ensure_ascii=False) + "\n")
print(f"Reviews: {len(added)} new, {len(added) + len(saved)} saved")
for r in added:
    print(f"  + {r['name']} ({r['stars']} stars){' - ' + r['service'] if r['service'] else ''}")

subprocess.run([sys.executable, str(ROOT / "scripts" / "build_reviews.py")], check=True)
