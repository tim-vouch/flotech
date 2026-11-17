// Renders brochures/out/flotech-care-plans-<key>.html to an A5 PDF plus a PNG preview of each side.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [out, ...keys] = process.argv.slice(2);
  const b = await chromium.launch();
  for (const k of keys) {
    const p = await b.newPage({ viewport: { width: 560, height: 794 }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.join(out, `flotech-care-plans-${k}.html`), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(out, `Flotech-Care-Plans-${k.split('-').map(w => w[0].toUpperCase() + w.slice(1)).join('-')}.pdf`), width: '560px', height: '210mm', printBackground: true, preferCSSPageSize: true });
    const pages = await p.locator('.page').all();
    for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: path.join(out, `${k}-side${i + 1}.png`) });
    // flag anything that spills off the page
    const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map(pg => {
      const r = pg.getBoundingClientRect(); let worst = 0; const band = pg.querySelector('.band'); const lim = band ? band.getBoundingClientRect().top : r.bottom;
      pg.querySelectorAll('*').forEach(el => { if (band && band.contains(el)) return; const b = el.getBoundingClientRect(); if (b.height && b.bottom > lim + 0.5) worst = Math.max(worst, b.bottom - lim); });
      return Math.round(worst);
    }));
    console.log(k, 'overflow px per side:', over);
  }
  await b.close();
})();
