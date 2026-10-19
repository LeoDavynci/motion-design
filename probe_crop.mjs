import { chromium } from 'playwright';
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 800, height: 1500 }, deviceScaleFactor: 1 });
const p = await ctx.newPage(); await p.goto('http://localhost:5173/', { waitUntil: 'networkidle' });
await p.addStyleTag({ content: '.device{--device-scale:1.5 !important}' }); await p.waitForTimeout(1200);
await p.getByRole('button', { name: 'Connections list' }).click(); await p.waitForTimeout(700);
await p.locator('.person-row', { hasText: 'Jordan Lee' }).first().click(); await p.waitForTimeout(1500);
await p.mouse.move(400, 750); for (let i = 0; i < 26; i++) { await p.mouse.wheel(0, 65); await p.waitForTimeout(50); } await p.waitForTimeout(600);
await p.locator('.moment-head').first().click(); await p.waitForTimeout(1000);
const cdp = await ctx.newCDPSession(p); let n = 0, last = 0;
cdp.on('Page.screencastFrame', (f) => { n++; last = f.metadata.timestamp; cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {}); });
await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 90, maxWidth: 800, maxHeight: 1500, everyNthFrame: 1 });
await p.waitForTimeout(400);
const t0 = Date.now(); console.log('before play frames', n);
const play = p.getByRole('button', { name: 'Play voice note' }).first(); const bb = await play.boundingBox();
await p.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2);
for (let i = 0; i < 8; i++) { await p.waitForTimeout(700); console.log(((Date.now() - t0) / 1000).toFixed(1), 'frames', n); }
await b.close();
