// node hook-150/make_intro_bg.mjs (from ~/motion-design): draws the "Introducing Peepl" backgrounds from the Figma shapes
// and saves them as images, which intro.html shows instead of redrawing the huge blurred shapes each frame:
// intro.html?bg -> hook-150/assets/intro/bg.png (the scene), intro.html?pale -> hook-150/assets/phone/pale.png (around the phone),
// moment.html?bg -> hook-150/assets/moment/bg.png
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
for (const [page, mode, out] of [['intro', 'bg', 'hook-150/assets/intro/bg.png'], ['intro', 'pale', 'hook-150/assets/phone/pale.png'], ['moment', 'bg', 'hook-150/assets/moment/bg.png']]) {
  await p.goto(pathToFileURL(process.cwd() + `/hook-150/${page}.html`).href + '?' + mode);
  await p.evaluate((m) => Promise.all([...document.querySelectorAll(`#${m} img`)].map((im) => im.decode())), mode);
  await p.waitForTimeout(300);
  await p.screenshot({ path: out, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  console.log('saved', out);
}
await b.close();
