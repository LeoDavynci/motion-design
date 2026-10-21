import { open, OUT } from './lib.mjs';
import { mkdirSync, rmSync, writeFileSync } from 'node:fs';
const { b, p, clip } = await open();
const QS = 'I want to find someone to go climbing with me';
rmSync(OUT + 'ask_seq', { recursive: true, force: true }); mkdirSync(OUT + 'ask_seq', { recursive: true });
await p.getByRole('button', { name: 'Ask me about people' }).click(); await p.waitForTimeout(1200);
for (const ch of QS) {
  const key = ch === ' ' ? p.locator('.kb-key.is-space') : p.locator('.kb-keys button').filter({ hasText: new RegExp('^' + ch + '$', 'i') });
  const bb = await key.first().boundingBox(); await p.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2);
}
await p.waitForTimeout(600);
const cdp = await p.context().newCDPSession(p); const frames = [];
cdp.on('Page.screencastFrame', (f) => { frames.push({ ts: f.metadata.timestamp, d: f.data }); cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {}); });
await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 95, maxWidth: 900, maxHeight: 1800, everyNthFrame: 1 });
await p.waitForTimeout(300);
const tClick = Date.now() / 1000; await p.getByRole('button', { name: 'Send' }).click();
await p.waitForTimeout(6000); await cdp.send('Page.stopScreencast');
const t0 = frames.find((f) => f.ts >= tClick - 0.3)?.ts ?? frames[0].ts; // approx: first frame near click
const start = Math.max(0, frames.findIndex((f) => f.ts >= tClick - 0.25));
const fr = frames.slice(start); const T = fr[0].ts; const dur = fr.at(-1).ts - T; const n = Math.floor(dur * 12); let j = 0; const map = [];
for (let i = 0; i < n; i++) { while (j + 1 < fr.length && fr[j + 1].ts - T <= i / 12) j++; map.push(j); }
mkdirSync('assets/figma/v13/tools/raw', { recursive: true });
map.forEach((fi, i) => writeFileSync(`assets/figma/v13/tools/raw/f${String(i).padStart(3, '0')}.jpg`, Buffer.from(fr[fi].d, 'base64')));
writeFileSync(OUT + 'ask_seq/clip.json', JSON.stringify({ clip, n, dur, map, rawFrames: frames.length }));
console.log('raw', frames.length, 'used', fr.length, 'dur', dur, 'n', n, 'distinct', new Set(map).size, clip);
await b.close();
