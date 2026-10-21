import { open, OUT } from './lib.mjs';
import { mkdirSync, rmSync, writeFileSync } from 'node:fs';
const { b, p, clip, shot } = await open();
const QS = 'I want to find someone to go climbing with me';
mkdirSync(OUT + 'ask_seq', { recursive: true });
await p.getByRole('button', { name: 'Ask me about people' }).click(); await p.waitForTimeout(1200);
await shot('ask_dev_suggest.png');
for (const ch of QS) {
  const key = ch === ' ' ? p.locator('.kb-key.is-space') : p.locator('.kb-keys button').filter({ hasText: new RegExp('^' + ch + '$', 'i') });
  const bb = await key.first().boundingBox(); await p.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2);
}
await p.waitForTimeout(500); await shot('ask_dev_query.png');
const frames = []; let go = true;
const loop = (async () => { while (go) { const t = Date.now(); const buf = await p.screenshot({ type: 'png', clip }); frames.push({ t, buf }); } })();
await p.waitForTimeout(150);
const t0 = Date.now(); await p.getByRole('button', { name: 'Send' }).click();
await p.waitForTimeout(6500); go = false; await loop;
// resample at 12fps from click time
const dur = (frames.at(-1).t - t0) / 1000; const n = Math.floor(dur * 12); let j = 0; const used = new Set(); const map = [];
for (let i = 0; i < n; i++) { while (j + 1 < frames.length && frames[j + 1].t - t0 <= i / 12 * 1000) j++; map.push(j); }
map.forEach((fi, i) => writeFileSync(`${OUT}ask_seq/f${String(i).padStart(3, '0')}.png`, frames[fi].buf));
console.log('raw', frames.length, 'dur', dur, 'out', n, 'distinct', new Set(map).size);
await shot('ask_dev_results.png');
await p.getByRole('button', { name: 'Draft a message' }).first().click(); await p.waitForTimeout(1500); await shot('ask_dev_draft.png');
await b.close();
