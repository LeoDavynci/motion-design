import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
const t = process.argv.slice(2).map(Number);
const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('pageerror', (e) => console.log('PAGEERROR', e.message.slice(0, 200)));
p.on('console', (m) => m.type() === 'error' && console.log('CONSOLE', m.text().slice(0, 160)));
await p.goto(pathToFileURL(process.cwd() + '/index.html').href);
await p.evaluate(() => window.ready);
for (const x of t) { const t0 = Date.now(); await p.evaluate((v) => window.seek(v), x); const ms = Date.now() - t0; await p.locator('#c').screenshot({ path: `tmp/f_${x}.png` }); console.log('seek', x, ms + 'ms'); }
await b.close();
