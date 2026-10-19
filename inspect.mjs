import { chromium } from 'playwright';
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 700, height: 922 }, deviceScaleFactor: 2 });
const p = await ctx.newPage();
const btns = () => p.$$eval('.phone button', (n) => n.filter((e) => e.offsetParent && !/kb-key/.test(e.className)).map((e) => e.getAttribute('aria-label') || e.innerText.trim().slice(0, 20)).filter(Boolean).join(','));
const val = () => p.$$eval('.phone textarea', (n) => n.map((e) => e.value.slice(-34)));
const clip = { x: 153.5, y: 35, width: 393, height: 852 };
await p.goto('http://localhost:5173/', { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
await p.getByRole('button', { name: 'Add a person or moment' }).click(); await p.waitForTimeout(1200);
await p.getByRole('button', { name: 'Record by voice' }).click(); const t0 = Date.now();
for (let i = 0; i < 14; i++) { await p.waitForTimeout(600); console.log(((Date.now() - t0) / 1000).toFixed(1), JSON.stringify(await val()), await btns()); }
await p.screenshot({ path: 'assets/insp_add.png', clip });
await b.close();
