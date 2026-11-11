"""Build demo-only changes into site/_preview/, leaving the live pages in site/ untouched.

    python3 scripts/preview_build.py          # rebuild the demo copies (safe to re-run)
    python3 scripts/preview_build.py apply    # make them live: write the changes into site/ and delete site/_preview/

How it works: the area scripts run on site/ as usual, then every page they changed or created is moved into
site/_preview/<same path> and the live original is put back. worker.js serves site/_preview/<path> first on
the demo (flotech.vouchdigital.co.uk); pages.yml deletes site/_preview before publishing to GitHub Pages, so
flotechheating.co.uk never sees it. Before `apply`, set PREVIEW_ONLY = False in scripts/area_content.py.

Now in the demo: Darren's postcode areas (11 Nov 2026), 25 town pages, the postcode checker on /areas/,
the new Areas menu, footer column and schema areaServed.
The daily reviews job (build_reviews.py) refreshes the copies in _preview too, so they stay current.
"""
import os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PREVIEW = os.path.join(SITE, "_preview")
STEPS = ["build_areas.py", "areas.py", "mobile_header.py", "analytics.py"]
SKIP = ("_preview", "_finance-preview", "wp-", "boiler-care-plans")   # boiler-care-plans is already demo-only
KEEP_LIVE = ("sitemap.xml", "llms.txt")                               # live files the build also touches


def pages():
    out = {}
    for d, _, files in os.walk(SITE):
        rel_d = os.path.relpath(d, SITE)
        if rel_d != "." and rel_d.startswith(SKIP):
            continue
        for name in files:
            if name.endswith(".html"):
                rel = os.path.normpath(os.path.join(rel_d, name))
                out[rel] = open(os.path.join(SITE, rel), encoding="utf-8").read()
    return out


def run(env):
    for s in STEPS:
        subprocess.run([sys.executable, os.path.join(ROOT, "scripts", s)], check=True, env=env)


def main():
    env = dict(os.environ, FLOTECH_PREVIEW_BUILD="1")
    if sys.argv[1:] == ["apply"]:
        import area_content
        if area_content.PREVIEW_ONLY:
            sys.exit("Set PREVIEW_ONLY = False in scripts/area_content.py first.")
        shutil.rmtree(PREVIEW, ignore_errors=True)
        run(env)
        print("Applied to site/. Commit and push to publish to flotechheating.co.uk.")
        return
    shutil.rmtree(PREVIEW, ignore_errors=True)
    before = pages()
    keep = {f: open(os.path.join(SITE, f), encoding="utf-8").read() for f in KEEP_LIVE if os.path.exists(os.path.join(SITE, f))}
    run(env)
    after = pages()
    moved = 0
    for rel, text in after.items():
        if before.get(rel) == text:
            continue
        dest = os.path.join(PREVIEW, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(text)
        src = os.path.join(SITE, rel)
        if rel in before:
            open(src, "w", encoding="utf-8").write(before[rel])
        else:
            os.remove(src)
            try:
                os.removedirs(os.path.dirname(src))
            except OSError:
                pass
        moved += 1
    for f, text in keep.items():
        open(os.path.join(SITE, f), "w", encoding="utf-8").write(text)
    print(moved, "pages in site/_preview (demo only); live pages unchanged")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
