// node capture.mjs -> assets/seq/<flow>/0000.jpg ... at 30fps (real app, real timing, CDP screencast)
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
const URL = 'http://localhost:5173/?mock=100', FPS = 30;
const b = await chromium.launch();
async function flow(name, fn) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  const cdp = await ctx.newCDPSession(p);
  await p.goto(URL, { waitUntil: 'networkidle' });
  await p.waitForTimeout(500);
  const frames = [];
  cdp.on('Page.screencastFrame', async f => { frames.push({ ts: f.metadata.timestamp, d: f.data }); cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(()=>{}); });
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 88, maxWidth: 780, maxHeight: 1688, everyNthFrame: 1 });
  await p.waitForTimeout(200);
  await fn(p);
  await p.waitForTimeout(300);
  await cdp.send('Page.stopScreencast');
  const dir = `assets/seq/${name}`; rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  const t0 = frames[0].ts, n = Math.floor((frames.at(-1).ts - t0) * FPS);
  let j = 0;
  for (let i = 0; i < n; i++) {
    while (j + 1 < frames.length && frames[j + 1].ts - t0 <= i / FPS) j++;
    writeFileSync(`${dir}/${String(i).padStart(4, '0')}.jpg`, Buffer.from(frames[j].d, 'base64'));
  }
  console.log(name, n, 'frames', (n / FPS).toFixed(1) + 's');
  await ctx.close();
}
// A: mindmap, a slow drag-free hold so the force layout settles on screen
await flow('map', async p => { await p.reload({ waitUntil: 'domcontentloaded' }); await p.waitForTimeout(3500); });
// B: list view
await flow('list', async p => { await p.click('button[aria-label="Connections list"]'); await p.waitForTimeout(1200); await p.mouse.wheel(0, 500); await p.waitForTimeout(900); });
// C: add / capture, typed note
await flow('add', async p => {
  await p.click('button[aria-label="Add a person or moment"]'); await p.waitForTimeout(900);
  await p.keyboard.type('Just met Jordan Lee at Climate Demo Day. Founder, battery recycling for e-bikes.', { delay: 45 });
  await p.waitForTimeout(800);
});
// D: profile
await flow('profile', async p => {
  await p.click('button[aria-label="Connections list"]'); await p.waitForTimeout(600);
  await p.click('.person-row >> nth=0'); await p.waitForTimeout(1400);
  await p.mouse.move(195, 500); await p.mouse.wheel(0, 450); await p.waitForTimeout(1200);
});
// E: ask
await flow('ask', async p => {
  await p.click('text=Ask me about people'); await p.waitForTimeout(500);
  await p.keyboard.type('hiking', { delay: 110 }); await p.keyboard.press('Enter'); await p.waitForTimeout(2500);
});
await b.close();
