"""Ahrefs Web Analytics (cookie-free visit counts) on every page. Safe to re-run: python3 scripts/analytics.py"""
import glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIPPET = '<script src="https://analytics.ahrefs.com/analytics.js" data-key="N9x0VuCqlgvZIo2XtLycvw" async></script>'

n = 0
for f in glob.glob(os.path.join(ROOT, "site", "**", "*.html"), recursive=True):
    rel = os.path.relpath(f, os.path.join(ROOT, "site"))
    if rel.startswith(("wp-", "_finance-preview")):
        continue
    s = open(f, encoding="utf-8").read()
    if "analytics.ahrefs.com/analytics.js" in s or "</head>" not in s:
        continue
    open(f, "w", encoding="utf-8").write(s.replace("</head>", SNIPPET + "\n</head>", 1))
    n += 1
print(n, "pages")
