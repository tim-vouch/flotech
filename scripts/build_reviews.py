#!/usr/bin/env python3
"""Builds the review sections of the site from data/google-reviews.json and data/rating.json.

1. Every page: the reviews band at the top of the footer (replaces the old Trustindex widget). Rating summary,
   a carousel of five-star reviews that name a job (boiler installations get two of every three slots), and a
   "See all reviews" link.
2. /reviews/: every review with text, newest first, with its real star count.
3. sitemap.xml gets /reviews/.

Run after any change to the data: python3 scripts/build_reviews.py. The daily GitHub Action runs it for you.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
sys.path.insert(0, str(ROOT / "scripts"))
from reviews_lib import carousel  # noqa: E402

REVIEWS = json.loads((ROOT / "data" / "google-reviews.json").read_text())
RATING = json.loads((ROOT / "data" / "rating.json").read_text())
GOOGLE_URL = "https://www.google.com/search?q=Flotech+Heating+and+Plumbing+Ltd+reviews"
START, END = "<!--flotech-reviews:start-->", "<!--flotech-reviews:end-->"
COLOURS = ["#7b4dff", "#4f6bff", "#1fa2ff", "#a24bff", "#2f80ed", "#6a5af9"]

esc = lambda s: html.escape(s or "", quote=True)
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.5l2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 14.9l-5.2 2.8 1-5.9L1.5 7.7l5.9-.8z"/></svg>'
G_LOGO = ('<svg class="fr-g" viewBox="0 0 48 48" aria-hidden="true"><path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h11.8c-.5 2.8-2.1 5.1-4.4 6.7v5.5h7.1c4.2-3.8 6.6-9.5 6.6-16.2z"/>'
          '<path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.5-5.3l-7.1-5.5c-2 1.3-4.5 2.1-7.4 2.1-5.7 0-10.5-3.8-12.2-9H4.5v5.7C8.1 41.1 15.5 46 24 46z"/>'
          '<path fill="#FBBC05" d="M11.8 28.3c-.4-1.3-.7-2.7-.7-4.3s.3-3 .7-4.3V14H4.5C3 17 2 20.4 2 24s1 7 2.5 10l7.3-5.7z"/>'
          '<path fill="#EA4335" d="M24 10.7c3.2 0 6.1 1.1 8.4 3.3l6.3-6.3C34.9 4.2 29.9 2 24 2 15.5 2 8.1 6.9 4.5 14l7.3 5.7c1.7-5.2 6.5-9 12.2-9z"/></svg>')


def stars(n):
    return f'<span class="fr-stars" role="img" aria-label="{n} out of 5 stars">' + "".join(
        f'<i class="{"on" if i < n else "off"}">{STAR}</i>' for i in range(5)) + "</span>"


def card(r, i, clamp=True):
    initial = (r["name"].strip()[:1] or "?").upper()
    tag = f'<span class="fr-tag">{esc(r["service"])}</span>' if r.get("service") else ""
    more = '<button type="button" class="fr-more" hidden>Read more</button>' if clamp else ""
    return (f'<article class="fr-card"><div class="fr-head"><span class="fr-av" style="background:{COLOURS[i % len(COLOURS)]}">{esc(initial)}</span>'
            f'<div><div class="fr-name">{esc(r["name"])}</div><time class="fr-date" datetime="{esc(r.get("published", ""))}"></time></div>{G_LOGO}</div>'
            f'{stars(r["stars"])}{tag}<p class="fr-text{" fr-clamp" if clamp else ""}">{esc(r["text"])}</p>{more}</article>')


CSS = """<style>
.fr{--fr-a:#7b4dff;--fr-b:#1fa2ff;padding:72px 0 64px;background:#fff;font-family:inherit;width:100%;min-width:0;box-sizing:border-box;overflow-x:clip}
.fr *{box-sizing:border-box}
.fr-wrap{width:min(1280px,100% - 40px);margin:0 auto;display:grid;grid-template-columns:230px minmax(0,1fr);gap:32px;align-items:center}
.fr-sum{text-align:center;display:grid;gap:8px;justify-items:center}
.fr-sum strong{font-size:22px;letter-spacing:.04em;color:#111}
.fr-sum .fr-stars svg{width:30px;height:30px}
.fr-sum p{margin:0;color:#222;font-size:15px}
.fr-sum .fr-glogo{font:600 30px/1 Arial,sans-serif;letter-spacing:-.5px}
.fr-all{display:inline-flex;align-items:center;gap:8px;margin-top:10px;padding:11px 20px;border-radius:8px;color:#fff;text-decoration:none;font-weight:600;font-size:14px;background:linear-gradient(90deg,var(--fr-a),var(--fr-b))}
.fr-all:hover{opacity:.92;color:#fff}
.fr-car{position:relative}
.fr-track{display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 32px)/3);gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:4px}
.fr-track::-webkit-scrollbar{display:none}
.fr-card{scroll-snap-align:start;background:#f4f4f6;border-radius:12px;padding:20px;display:flex;flex-direction:column;gap:10px;text-align:left}
.fr-head{display:flex;align-items:center;gap:12px}
.fr-head>div{flex:1;min-width:0}
.fr-av{width:42px;height:42px;border-radius:50%;color:#fff;display:grid;place-items:center;font-weight:600;font-size:18px;flex:none}
.fr-name{font-weight:600;color:#111;font-size:15.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fr-date{color:#777;font-size:13px}
.fr-g{width:22px;height:22px;flex:none}
.fr-stars{display:inline-flex;gap:2px}
.fr-stars svg{width:19px;height:19px;display:block}
.fr-stars .on svg{fill:#fbbc04}.fr-stars .off svg{fill:#d6d6dc}
.fr-tag{align-self:flex-start;font-size:12px;font-weight:600;color:#5b3fd6;background:#ece7ff;border-radius:999px;padding:3px 10px}
.fr-text{margin:0;color:#222;font-size:15px;line-height:1.55}
.fr-clamp{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.fr-open .fr-clamp{-webkit-line-clamp:unset;display:block}
.fr-more{align-self:flex-start;background:none;border:0;padding:0;color:#777;font:inherit;font-size:14px;cursor:pointer}
.fr-more:hover{color:#111;background:none}
.fr-more[hidden]{display:none!important}
.fr-arrow{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;border:0;background:#fff;box-shadow:0 2px 10px rgba(0,0,0,.16);cursor:pointer;display:grid;place-items:center;color:#333;z-index:2}
.fr-arrow svg{width:18px;height:18px}
.fr-prev{left:-14px}.fr-next{right:-14px}
.fr-arrow[disabled]{opacity:0;pointer-events:none}
@media (max-width:1024px){.fr-track{grid-auto-columns:calc((100% - 16px)/2)}}
@media (max-width:767px){.fr{padding:48px 0}.fr-wrap{grid-template-columns:minmax(0,1fr);gap:20px}.fr-track{grid-auto-columns:86%}.fr-prev{left:-6px}.fr-next{right:-6px}}
.fr-page{padding:56px 0 80px}
.fr-page .fr-wrap{display:block}
.fr-page h1{font-size:clamp(32px,4vw,46px);margin:0 0 12px;color:#111}
.fr-page .fr-intro{display:flex;flex-wrap:wrap;align-items:center;gap:14px 22px;margin-bottom:36px;color:#333}
.fr-page .fr-intro a{color:#5b3fd6}
.fr-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.fr-grid .fr-card.fr-hide{display:none}
.fr-load{display:block;margin:32px auto 0;border:0;cursor:pointer;font:inherit}
@media (max-width:1024px){.fr-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.fr-grid{grid-template-columns:1fr}}
</style>"""

JS = """<script>
(function(){
  function ago(iso){if(!iso)return'';var d=(Date.now()-new Date(iso))/864e5;
    if(d<1)return'today';if(d<2)return'yesterday';if(d<7)return Math.floor(d)+' days ago';
    if(d<30){var w=Math.floor(d/7);return w+(w>1?' weeks':' week')+' ago';}
    if(d<365){var m=Math.floor(d/30.4);return m+(m>1?' months':' month')+' ago';}
    var y=Math.floor(d/365);return y+(y>1?' years':' year')+' ago';}
  document.querySelectorAll('.fr-date').forEach(function(t){t.textContent=ago(t.getAttribute('datetime'));});
  function clampCheck(){document.querySelectorAll('.fr-card').forEach(function(c){var p=c.querySelector('.fr-clamp'),b=c.querySelector('.fr-more');
    if(p&&b&&!c.classList.contains('fr-open'))b.hidden=p.scrollHeight<=p.clientHeight+2;});}
  document.addEventListener('click',function(e){var b=e.target.closest('.fr-more');if(!b)return;var c=b.closest('.fr-card');
    c.classList.toggle('fr-open');b.textContent=c.classList.contains('fr-open')?'Show less':'Read more';});
  document.querySelectorAll('.fr-car').forEach(function(car){var t=car.querySelector('.fr-track'),p=car.querySelector('.fr-prev'),n=car.querySelector('.fr-next');
    function step(){var c=t.querySelector('.fr-card');return c?c.getBoundingClientRect().width+16:300;}
    function upd(){p.disabled=t.scrollLeft<4;n.disabled=t.scrollLeft+t.clientWidth>=t.scrollWidth-4;}
    p.addEventListener('click',function(){t.scrollBy({left:-step(),behavior:'smooth'});});
    n.addEventListener('click',function(){t.scrollBy({left:step(),behavior:'smooth'});});
    t.addEventListener('scroll',upd,{passive:true});upd();});
  var load=document.querySelector('.fr-load');if(load)load.addEventListener('click',function(){
    var h=document.querySelectorAll('.fr-grid .fr-hide');for(var i=0;i<24&&i<h.length;i++)h[i].classList.remove('fr-hide');
    if(h.length<=24)load.remove();clampCheck();});
  clampCheck();window.addEventListener('resize',clampCheck);
})();
</script>"""

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>'


def summary(link=True):
    btn = '<a class="fr-all" href="/reviews/">See all reviews <span aria-hidden="true">&rarr;</span></a>' if link else ""
    return (f'<div class="fr-sum"><strong>EXCELLENT</strong>{stars(5)}<p>Based on <b>{esc(RATING["count"])} reviews</b></p>'
            f'<div class="fr-glogo" aria-label="Google"><span style="color:#4285F4">G</span><span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span>'
            f'<span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span></div>{btn}</div>')


def band():
    cards = "".join(card(r, i) for i, r in enumerate(carousel(REVIEWS)))
    return (f'{START}<section class="fr" aria-label="Customer reviews"><div class="fr-wrap">{summary()}'
            f'<div class="fr-car"><button type="button" class="fr-arrow fr-prev" aria-label="Previous reviews">{ARROW.format(d="M15 18l-6-6 6-6")}</button>'
            f'<div class="fr-track">{cards}</div>'
            f'<button type="button" class="fr-arrow fr-next" aria-label="Next reviews">{ARROW.format(d="M9 18l6-6-6-6")}</button></div>'
            f'</div></section>{CSS}{JS}{END}')


def reviews_page_main():
    shown = [r for r in REVIEWS if r.get("text")]
    shown.sort(key=lambda r: r.get("published", ""), reverse=True)
    cards = "".join(card(r, i).replace('class="fr-card"', 'class="fr-card fr-hide"', 1) if i >= 24 else card(r, i)
                    for i, r in enumerate(shown))
    load = '<button type="button" class="fr-all fr-load">Show more reviews</button>' if len(shown) > 24 else ""
    return (f'<section class="fr fr-page"><div class="fr-wrap"><h1>Customer reviews</h1>'
            f'<div class="fr-intro">{stars(5)}<span><b>{esc(RATING["rating"])}</b> from <b>{esc(RATING["count"])}</b> Google reviews.</span>'
            f'<a href="{GOOGLE_URL}" target="_blank" rel="noopener">Read them on Google</a></div>'
            f'<div class="fr-grid">{cards}</div>{load}</div></section>{END}')


def replace_block(page, new):
    if START in page:
        return re.sub(re.escape(START) + ".*?" + re.escape(END), lambda m: new, page, flags=re.S)
    # First run: swap the Trustindex widget (an Elementor HTML widget at the top of the footer) for our band.
    i = page.find('<pre class="ti-widget"')
    if i < 0:
        return page
    start = page.rfind('<div class="elementor-element', 0, i)
    depth, j = 0, start
    for m in re.finditer(r"<div\b|</div>", page[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            j = start + m.end()
            break
    return page[:start] + new + page[j:]


def main():
    b = band()
    pages = [p for p in SITE.rglob("index.html") if p.parent.name != "reviews"]
    for p in pages:
        s = p.read_text()
        t = replace_block(s, b)
        # Trustindex loader script, no longer needed
        t = re.sub(r'<script[^>]*cdn\.trustindex\.io[^>]*>\s*</script>', "", t)
        if t != s:
            p.write_text(t)

    # /reviews/ page, built from the About page's header and footer
    src = (SITE / "about-us" / "index.html").read_text()
    head_title = "Customer Reviews | Flotech Heating and Plumbing"
    desc = (f"Read {RATING['count']} Google reviews of Flotech Heating and Plumbing: boiler installations, servicing, "
            f"repairs and bathrooms across Bishop's Stortford and the surrounding areas.")
    s = re.sub(r"<title>.*?</title>", f"<title>{esc(head_title)}</title>", src, flags=re.S)
    s = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*"', lambda m: m.group(1) + esc(desc) + '"', s)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*"', lambda m: m.group(1) + esc(head_title) + '"', s)
    s = s.replace("https://flotechheating.co.uk/about-us/", "https://flotechheating.co.uk/reviews/")
    s = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>', "", s, flags=re.S)
    s = re.sub(r"(<main\b[^>]*>).*?(</main>)", lambda m: m.group(1) + reviews_page_main() + m.group(2), s, flags=re.S)
    s = replace_block(s, START + CSS + JS + END)   # no carousel on the page that already lists every review
    (SITE / "reviews").mkdir(exist_ok=True)
    (SITE / "reviews" / "index.html").write_text(s)

    sm = SITE / "sitemap.xml"
    x = sm.read_text()
    if "/reviews/" not in x:
        sm.write_text(x.replace("</urlset>", "  <url><loc>https://flotechheating.co.uk/reviews/</loc></url>\n</urlset>"))
    print(f"Built: {len(pages)} pages, carousel {len(carousel(REVIEWS))} reviews, /reviews/ {sum(1 for r in REVIEWS if r.get('text'))} reviews")


if __name__ == "__main__":
    main()
