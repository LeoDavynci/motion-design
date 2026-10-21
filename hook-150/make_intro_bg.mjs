// node hook-150/make_intro_bg.mjs (from ~/motion-design): draws the "Introducing Peepl" background from the Figma shapes
// (intro.html?bg) and saves it as hook-150/assets/intro/bg.png, which intro.html shows instead of redrawing it each frame.
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto(pathToFileURL(process.cwd() + '/hook-150/intro.html').href + '?bg');
await p.evaluate(() => Promise.all([...document.querySelectorAll('#bg img')].map((im) => im.decode())));
await p.waitForTimeout(300);
await p.screenshot({ path: 'hook-150/assets/intro/bg.png', clip: { x: 0, y: 0, width: 1920, height: 1080 } });
await b.close();
console.log('saved hook-150/assets/intro/bg.png');
