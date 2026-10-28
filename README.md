# Flotech Heating and Plumbing website

Managed by Vouch Digital. Public repo: never commit secrets, client documents or notes.

- `site/`: the website (static copy of the old WordPress site). Edit pages here.
- Live site: GitHub Pages (`.github/workflows/pages.yml` publishes `site/` on every push to `main`).
  DNS stays with Carl (Experts Computer Services) at 20i: apex A records to GitHub Pages
  (185.199.108.153, .109.153, .110.153, .111.153), `www` CNAME to tim-vouch.github.io. Email records untouched (Microsoft 365).
- Preview and contact form: Cloudflare Worker `flotech` (`worker.js`, `wrangler.jsonc`) on flotech.tim-268.workers.dev and flotech.vouchdigital.co.uk (noindex, robots.txt blocks crawlers).
  The form on /contact/ posts to its `/api/enquiry`, which filters spam and forwards to Flotech's GHL inbound webhook
  (Cloudflare Secret `GHL_WEBHOOK_URL`). If the secret is missing, visitors are asked to call 01279 598972.
