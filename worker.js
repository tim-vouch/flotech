// Flotech enquiry form handler (Cloudflare Worker).
// The website itself is hosted on GitHub Pages (flotechheating.co.uk); this Worker also serves a preview copy
// of the site on workers.dev. The contact form on both posts here: POST /api/enquiry -> spam checks -> GHL webhook.
// GHL_WEBHOOK_URL is a Cloudflare Secret (Settings > Variables and Secrets). Never commit it: this repo is public.

const ALLOWED = ["https://flotechheating.co.uk", "https://www.flotechheating.co.uk", "https://flotech-live.vouchdigital.co.uk"];
const cors = (origin) => ({
  "access-control-allow-origin": ALLOWED.includes(origin) || /\.workers\.dev$|^https:\/\/flotech\.vouchdigital\.co\.uk$/.test(origin) ? origin : ALLOWED[0],
  "access-control-allow-methods": "POST, OPTIONS",
  "access-control-allow-headers": "content-type",
  "vary": "origin",
});
const json = (body, status, origin) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", ...cors(origin) } });

// Sales pitches (SEO, marketing agencies): 3+ matches = dropped with a normal thank-you and logged.
const PITCH = [
  /\bseo\b/i, /\bmarketing\b/i, /\bbacklinks?\b/i, /\bguest post/i, /first page of google/i,
  /google (ranking|rankings|maps ranking|business profile)/i, /\b(more|new|extra) (leads|reviews|customers)\b/i,
  /\breviews? (vs|versus)\b/i, /\bcompetitors?\b/i, /monthly report/i, /\bour (setup|service|agency|team|platform)\b/i,
  /(per|a) month\b/i, /\+ ?vat\b/i, /no contract/i, /pay (nothing|a penny)/i, /free trial/i,
  /reply ["'“]?(yes|no|stop)/i, /not for you/i, /unsubscribe/i, /book a (call|demo)/i,
  /website (design|redesign)/i, /\b(we|i) (can|will|'ll) (help you|get you|grow)/i,
  /(appointment setting|lead generation|virtual assistant|outsourc)/i, /https?:\/\/|www\./i,
  /\byour (website|site|online|business|google)\b/i, /\bvisibility\b/i, /\b(ai|ai-powered) search|chatgpt/i,
  /\bi (noticed|came across|put together)\b/i, /\bsuggestions\b/i, /free (to review|audit|report|analysis)/i,
  /(would it be (ok|okay|alright)|is it (ok|okay)) (if|to)|send (them|it) over/i,
];
const pitchScore = (text) => PITCH.filter((re) => re.test(text)).length;

async function handleEnquiry(request, env) {
  const origin = request.headers.get("origin") || "";
  if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(origin) });
  if (request.method !== "POST") return json({ ok: false, error: "method" }, 405, origin);
  let data = {};
  try { data = await request.json(); } catch { return json({ ok: false, error: "bad_request" }, 400, origin); }

  const clean = (v, max) => String(v || "").replace(/\s+/g, " ").trim().slice(0, max);
  const name = clean(data.name, 80), phone = clean(data.phone, 30), email = clean(data.email, 120);
  const message = String(data.message || "").trim().slice(0, 2000);

  const tooFast = Date.now() - Number(data.started || 0) < 3000;
  if (clean(data.company, 200) || tooFast) return json({ ok: true }, 200, origin);   // bots
  if (pitchScore(`${name} ${message}`) >= 3) {
    console.log("Blocked sales pitch", JSON.stringify({ name, phone, email, message }));
    return json({ ok: true }, 200, origin);
  }
  if (name.length < 2 || phone.replace(/\D/g, "").length < 10) return json({ ok: false, error: "validation" }, 422, origin);
  if (!env.GHL_WEBHOOK_URL) return json({ ok: false, error: "not_configured" }, 500, origin);

  const [first_name, ...rest] = name.split(" ");
  const payload = { first_name, last_name: rest.join(" "), full_name: name, phone, email, message,
    source: "Website enquiry", page: clean(data.page, 300), submitted_at: new Date().toISOString() };
  const res = await fetch(env.GHL_WEBHOOK_URL, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) });
  return res.ok ? json({ ok: true }, 200, origin) : json({ ok: false, error: "upstream" }, 502, origin);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/enquiry") return handleEnquiry(request, env);
    // This Worker only serves preview copies (flotech.vouchdigital.co.uk, workers.dev). Keep them out of Google
    // so they never compete with the real site: block crawlers and send noindex on every response.
    if (url.pathname === "/robots.txt") {
      return new Response("User-agent: *\nDisallow: /\n", { headers: { "content-type": "text/plain", "x-robots-tag": "noindex" } });
    }
    // Finance compliance preview (Phoenix, Nov 2026): fixed copies of pages live in site/_finance-preview/ and are shown
    // here first, for Louise to approve. pages.yml strips that folder from the live site. Approve with
    // `python3 scripts/finance_fix.py apply` and delete site/_finance-preview.
    // Demo-only pages (site/_preview/, built by scripts/preview_build.py, e.g. Darren's postcode areas, Nov 2026)
    // are served first in the same way; pages.yml strips that folder from the live site too.
    let res = null;
    if (request.method === "GET" && url.pathname.endsWith("/") && !/^\/_(finance-)?preview\//.test(url.pathname)) {
      for (const dir of ["/_preview", "/_finance-preview"]) {
        const alt = await env.ASSETS.fetch(new Request(new URL(dir + url.pathname, url), request));
        if (alt.ok && (alt.headers.get("content-type") || "").includes("text/html")) { res = alt; break; }
      }
    }
    if (!res) res = await env.ASSETS.fetch(request);
    let out = new Response(res.body, res);
    out.headers.set("x-robots-tag", "noindex, nofollow");
    if ((out.headers.get("content-type") || "").includes("text/html")) {
      const html = previewOverlay(await out.text(), url.pathname);
      const headers = new Headers(out.headers);
      headers.delete("content-length");
      out = new Response(html, { status: out.status, headers });
    }
    return out;
  },
};

// ---------- Preview-only changes (Nov 2026, for showing Darren) ----------
// This Worker only serves the preview (flotech.vouchdigital.co.uk). The live site on GitHub Pages is untouched,
// so these edits are made here on the fly instead of in site/ (whose pages also go live).
//  - Boiler care plans: menu items and the homepage card link to /boiler-care-plans/ instead of "Coming soon"
// (Testimonials, Blog and the review filter moved into site/ on 3 Nov 2026, so they are live too.)
const CARE = "/boiler-care-plans/";
function previewOverlay(html, path) {
  html = html
    // desktop mega menu
    .replace(/<div class="ft-mega__item ft-mega__item--soon" aria-disabled="true">([\s\S]*?)<\/div>(<a href="\/boiler-finance\/")/,
      '<a href="' + CARE + '" class="ft-mega__item" role="menuitem">$1</a>$2')
    // second menu variant (cards)
    .replace(/<div class="ftm-card ftm-card--soon" aria-disabled="true">([\s\S]*?)<\/div>(\s*<a href="\/boiler-finance\/" class="ftm-card">)/,
      '<a href="' + CARE + '" class="ftm-card">$1</a>$2')
    .replaceAll("<strong>Boiler Care Plans</strong><span>Coming soon</span>", "<strong>Boiler Care Plans</strong><span>From &pound;9 a month</span>")
    // mobile menu
    .replace('<span class="ft-mobile__soon" aria-disabled="true">Boiler Care Plans <em>Coming soon</em></span>', '<a href="' + CARE + '">Boiler Care Plans</a>')
    // homepage card
    .replace('href="/contact/" class="fti-care" aria-label="Ask about boiler care plans (coming soon)"', 'href="' + CARE + '" class="fti-care" aria-label="See our boiler care plans"')
    .replace('<h3 class="elementor-heading-title elementor-size-default">Care Plans</h3>',
      '<h3 class="elementor-heading-title elementor-size-default"><a href="' + CARE + '" style="color:inherit;text-decoration:none">Care Plans</a></h3>');
  return html;
}

