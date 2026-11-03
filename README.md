# Flotech Heating and Plumbing website

Managed by Vouch Digital. Public repo: never commit secrets, client documents or notes.

- `site/`: the website (static copy of the old WordPress site). Edit pages here.
- Live site: GitHub Pages (`.github/workflows/pages.yml` publishes `site/` on every push to `main`).
  DNS stays with Carl (Experts Computer Services) at 20i: apex A records to GitHub Pages
  (185.199.108.153, .109.153, .110.153, .111.153), `www` CNAME to tim-vouch.github.io. Email records untouched (Microsoft 365).
- Live-site preview (Nov 2026, until switch day): GitHub Pages custom domain set to flotech-live.vouchdigital.co.uk (Cloudflare DNS: CNAME flotech-live -> tim-vouch.github.io, DNS only), showing exactly what goes live. On switch day change the Pages custom domain to flotechheating.co.uk.
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
- `site/blog/` (Nov 2026): preview-only blog built from Flotech's Google Business Profile posts (images in `site/blog/img/`). Also removed by `pages.yml` before publishing. To make it live: remove that step, wire the form to `/api/enquiry`, add it to the nav and sitemap, and have the plan terms checked.
