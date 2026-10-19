// node contact.mjs [step=0.5] [dur=15]  -> out/contact.png (frames via seek, no video encode)
import { chromium } from 'playwright';
import { spawnSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const step = Number(process.argv[2] || 0.5), dur = Number(process.argv[3] || 15);
mkdirSync('out/frames', { recursive: true });
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto(pathToFileURL(process.cwd() + '/index.html').href);
await page.evaluate(() => window.ready);
let n = 0;
for (let t = 0; t < dur + 1e-6; t += step, n++) {
  await page.evaluate((x) => window.seek(x), t);
  await page.locator('#c').screenshot({ path: `out/frames/f${String(n).padStart(3, '0')}.png` });
}
await browser.close();
const cols = 4, rows = Math.ceil(n / cols);
spawnSync('ffmpeg', ['-y', '-i', 'out/frames/f%03d.png', '-vf', `scale=480:-1,tile=${cols}x${rows}`, '-frames:v', '1', 'out/contact.png'], { stdio: 'inherit' });
