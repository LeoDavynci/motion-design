// node sheet.mjs [step] [from] [to] -> out/sheet_*.png (contact sheet) ; also prints TOTAL
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { mkdirSync, writeFileSync } from 'node:fs';
const step = Number(process.argv[2] || 1.5), from = Number(process.argv[3] || 0);
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('pageerror', (e) => console.log('PAGEERROR', e.message)); page.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
await page.goto(pathToFileURL(process.cwd() + '/index.html').href);
await page.evaluate(() => window.ready);
const total = await page.evaluate(() => window.TOTAL); console.log('TOTAL', total);
const to = Number(process.argv[4] || total);
mkdirSync('out/sheet', { recursive: true });
let n = 0;
for (let T = from; T < to; T += step) {
  await page.evaluate((t) => window.seek(t), T);
  await page.locator('#c').screenshot({ path: `out/sheet/f${String(n).padStart(3, '0')}_${T.toFixed(2)}.png`, type: 'png' }); n++;
}
console.log('frames', n);
await browser.close();
