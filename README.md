# Flotech Heating and Plumbing website

Managed by Vouch Digital. Public repo: never commit secrets, client documents or notes.

- `site/`: the website (static copy of the old WordPress site). Edit pages here.
- Live site: GitHub Pages (`.github/workflows/pages.yml` publishes `site/` on every push to `main`).
  DNS stays with Carl (Experts Computer Services) at 20i: apex A records to GitHub Pages
  (185.199.108.153, .109.153, .110.153, .111.153), `www` CNAME to tim-vouch.github.io. Email records untouched (Microsoft 365).
- Live since 4 Nov 2026 on flotechheating.co.uk (GitHub Pages custom domain, Enforce HTTPS on; DNS at 20i: four A records 185.199.108-111.153, www CNAME tim-vouch.github.io, TXT _github-pages-challenge-tim-vouch for the verified domain; email records untouched). The flotech-live.vouchdigital.co.uk preview CNAME in Cloudflare can be deleted.
- Preview and contact form: Cloudflare Worker `flotech` (`worker.js`, `wrangler.jsonc`) on flotech.tim-268.workers.dev and flotech.vouchdigital.co.uk (noindex, robots.txt blocks crawlers).
  The form on /contact/ posts to https://flotech.vouchdigital.co.uk/api/enquiry (same-origin on the Worker previews), which filters spam and forwards to Flotech's GHL inbound webhook
  (Cloudflare Secret `GHL_WEBHOOK_URL`). If the secret is missing, visitors are asked to call 01279 598972.

## Google reviews
- `data/google-reviews.json`: every review (first 214 from the GHL export, Oct 2026; new ones added daily). `data/rating.json`: rating and count.
- `scripts/build_reviews.py` builds the reviews band at the top of every page's footer (replaced Trustindex) and the /reviews/ page.
  Service pages show reviews of their own job first (`PAGE_SERVICES` in build_reviews.py), topped up with the general carousel.
  Carousel = five-star reviews that name a job, newest first, boiler installations in two of every three slots (`scripts/reviews_lib.py`).
- `.github/workflows/update-reviews.yml` runs `scripts/update_reviews.py` every morning (needs repo secret `GOOGLE_PLACES_API_KEY`
  and variable `GOOGLE_PLACE_ID`), commits any change, and the Pages workflow republishes.
- A deleted Google review must be removed from `data/google-reviews.json` by hand, then run `python3 scripts/build_reviews.py`.

## Preview-only pages
- `site/boiler-care-plans/` (Nov 2026): boiler care plan demo for Darren. Served only on the preview (flotech.vouchdigital.co.uk); `pages.yml` deletes it before publishing to GitHub Pages, so it never reaches flotechheating.co.uk. Its sign-up form is a demo (shows a thank-you, sends nothing). Content (plan details, annual service, terms) adapted from the care plan brochure template Darren was sent; Darren must confirm prices, cancellation charges and terms, and have them checked. On the preview only, `previewOverlay()` in `worker.js` rewrites pages on the fly: the care plan menu items and homepage card link here, "Testimonials" (/reviews/, with service filter buttons) and "Blog" are added to the menus. The live site is untouched.
- `site/blog/` (Nov 2026): preview-only blog built from Flotech's Google Business Profile posts (images in `site/blog/img/`). Live since 3 Nov 2026, with "Testimonials" (/reviews/, with service filter buttons from `scripts/review_filter.html`) and "Blog" in all menus, added by `add_menus()` in `scripts/build_reviews.py`.

## Finance (Phoenix) compliance, Nov 2026
Flotech is an Introducer Appointed Representative (IAR) of Phoenix Financial Consultants Ltd. Phoenix allow ONLY: the status disclosure, Phoenix's own banner and calculator, and a simple line such as "Boiler installation finance available through Phoenix Financial Consultants Ltd". Never add finance wording such as "flexible finance", "spread the cost", "affordable monthly payments", "0% finance", "contact us to discuss finance", representative examples, calculators or eligibility checklists. Care plan pages say "pay monthly", not "spread the cost".
- Applied to the live site on 9 Nov 2026 (menu label "Boiler Finance via Phoenix", approved line on the homepage, boiler pages and footer, /boiler-finance/ with a "Continue to Phoenix" button to Flotech's Phoenix referral link). The script now skips pages that are already fixed.
- `scripts/finance_fix.py preview` writes fixed copies to `site/_finance-preview/`; the Worker shows them on the preview only (pages.yml deletes the folder before publishing). `scripts/finance_fix.py apply` writes the fixes into `site/` (live on push); then delete `site/_finance-preview/`.
- While the fixed copies sit in `_finance-preview`, the daily reviews update only refreshes the originals, so re-run `preview` if the preview needs today's reviews.

## Service areas
Area pages: `/areas/` (hub, grouped Hertfordshire, Essex, Cambridgeshire) and `/areas/<slug>/` for each town. Wording in `scripts/area_content.py` (real districts, housing and postcodes only; reviews quoted word for word by reviewer name). Build with `python3 scripts/build_areas.py && python3 scripts/areas.py` (the shell is copied from the combi boiler page; also adds the pages to sitemap.xml).
One list in `scripts/areas.py` (`AREAS`, from Darren via Tim, 9 Nov 2026). Run `python3 scripts/areas.py` after changing it: it updates the area lists and chips on the pages, the schema `areaServed`, the Areas dropdown (desktop), the Areas group (tablet and phone menus) and the Areas we cover band in the footer. Safe to re-run.

## Terms and conditions
`/terms-and-conditions/` is Flotech's own Boiler Terms and Conditions (Louise, 9 Nov 2026), copied word for word in `scripts/build_terms.py` (numbering tidied only). Linked from Quick Links in the footer. Rebuild: `python3 scripts/build_terms.py && python3 scripts/areas.py`.

Footer: `scripts/areas.py` adds the Areas We Cover column (after Quick Links) and the Terms & Conditions link, and sets the five column widths.

## Phone header
`scripts/mobile_header.py` keeps the phone header on screen while scrolling (the thin Call us bar scrolls away; logo, call button, menu and Get Quote stay), like MJ Services. Safe to re-run; run it after `build_areas.py` or `build_terms.py`.

## SEO fixes (9 Nov 2026)
`scripts/seo_fixes.py`: home links go to `/` (not the duplicate `/home/`), alt text on logos and images, titles under 60 and descriptions 140 to 160 where they were off, stock images over 150KB resized and recompressed. `site/llms.txt` added. Safe to re-run.
