// node capture2.mjs [flow ...]  -> assets/live/<flow>/u#####.jpg (distinct frames, 1.5x) + assets/live/<flow>.json (60fps map + taps)
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
const URL = 'http://localhost:5173/', FPS = 60; let CLIP = null;
const want = process.argv.slice(2);
const b = await chromium.launch();
const wait = (p, s) => p.waitForTimeout(s * 1000);

async function record(name, setup, run, opts = {}) {
  if (want.length && !want.includes(name)) return;
  const ctx = await b.newContext({ viewport: { width: 800, height: 1500 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  await p.goto(URL, { waitUntil: 'networkidle' }); await p.addStyleTag({ content: '.device{--device-scale:1.5 !important}' }); await wait(p, 1.4);
  { const bb = await p.locator('.phone').boundingBox(); CLIP = { x: Math.round(bb.x), y: Math.round(bb.y), width: 2 * Math.floor(bb.width / 2), height: 2 * Math.floor(bb.height / 2) }; }
  await setup(p);
  const cdp = await ctx.newCDPSession(p), frames = [], taps = []; let shooting = false, shooter = null;
  if (opts.shots) { shooting = true; shooter = (async () => { while (shooting) { const buf = await p.screenshot({ type: 'jpeg', quality: 88, clip: CLIP }); frames.push({ ts: Date.now() / 1000, d: buf.toString('base64') }); } })(); }
  else { cdp.on('Page.screencastFrame', (f) => { frames.push({ ts: f.metadata.timestamp, d: f.data }); cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {}); });
  await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 90, maxWidth: 800, maxHeight: 1500, everyNthFrame: 1 }); }
  await wait(p, 0.25);
  const tap = async (loc, note = '') => {
    const bb = await loc.boundingBox(); if (!bb) { console.log('  tap miss', note); return; }
    const cx = bb.x + bb.width / 2, cy = bb.y + bb.height / 2;
    taps.push({ t: Date.now() / 1000, fx: (cx - CLIP.x) / CLIP.width, fy: (cy - CLIP.y) / CLIP.height, note });
    await p.mouse.click(cx, cy);
  };
  try { await run(p, tap); } catch (e) { console.log('  flow error', name, e.message.slice(0, 200)); }
  await wait(p, 0.3);
  if (opts.shots) { shooting = false; await shooter; } else await cdp.send('Page.stopScreencast');
  const t0 = frames[0].ts, dur = frames[frames.length - 1].ts - t0, n = Math.floor(dur * FPS), map = [];
  const raw = `tmp/${name}`, out = `assets/live/${name}`;
  rmSync(raw, { recursive: true, force: true }); rmSync(out, { recursive: true, force: true }); mkdirSync(raw, { recursive: true }); mkdirSync(out, { recursive: true });
  let j = 0;
  for (let i = 0; i < n; i++) { while (j + 1 < frames.length && frames[j + 1].ts - t0 <= i / FPS) j++; map.push(j); }
  const used = [...new Set(map)].sort((a, c) => a - c), remap = new Map(used.map((u, k) => [u, k]));
  used.forEach((u, k) => writeFileSync(`${raw}/u${String(k).padStart(5, '0')}.jpg`, Buffer.from(frames[u].d, 'base64')));
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', `${raw}/u%05d.jpg`, '-vf', opts.shots ? 'scale=590:-2' : `crop=${CLIP.width}:${CLIP.height}:${CLIP.x}:${CLIP.y},scale=590:-2`, '-q:v', '3', `${out}/u%05d.jpg`]);
  if (r.status) console.log('  ffmpeg fail', String(r.stderr).slice(0, 200));
  const mm = map.map((u) => remap.get(u)), starts = used.map((u, k) => mm.indexOf(k));
  writeFileSync(`assets/live/${name}.json`, JSON.stringify({ fps: FPS, n, dur, map: mm, starts, taps: taps.map((x) => ({ ...x, t: x.t - t0 })) }));
  console.log(name, 'dur', dur.toFixed(1) + 's', 'ticks', n, 'distinct', used.length, 'taps', taps.map((x) => (x.t - t0).toFixed(1) + ':' + x.note).join(' '));
  rmSync(raw, { recursive: true, force: true });
  await ctx.close();
}
const scroll = async (p, steps, dy) => { await p.mouse.move(400, 750); for (let i = 0; i < steps; i++) { await p.mouse.wheel(0, dy); await wait(p, 0.05); } };
const openJordan = async (p) => { await p.getByRole('button', { name: 'Connections list' }).click(); await wait(p, 0.7); await p.locator('.person-row', { hasText: 'Jordan Lee' }).first().click(); await wait(p, 1.4); };

// 1. mind map: tap a person, pill with View, sheet slides up
await record('map', async () => {}, async (p, tap) => {
  await wait(p, 0.9); await tap(p.locator('.mm-node', { hasText: 'JL' }).first(), 'node'); await wait(p, 1.5);
  await tap(p.getByRole('button', { name: 'View' }).first(), 'view'); await wait(p, 1.9);
});
// 2. group by city
await record('group', async () => {}, async (p, tap) => {
  await wait(p, 0.6); await tap(p.getByRole('button', { name: 'Filters' }), 'filters'); await wait(p, 0.9);
  await tap(p.locator('.phone').getByText('City', { exact: true }).first(), 'city'); await wait(p, 2.2);
});
// 3. add a person by talking
await record('add', async () => {}, async (p, tap) => {
  await wait(p, 0.5); await tap(p.getByRole('button', { name: 'Add a person or moment' }), 'add'); await wait(p, 1.1);
  await tap(p.getByRole('button', { name: 'Record by voice' }), 'mic'); await wait(p, 5.0);
  await tap(p.getByRole('button', { name: 'Stop recording' }), 'stop'); await wait(p, 0.6);
  await tap(p.getByRole('button', { name: 'Send' }), 'send'); await wait(p, 2.4);
  await tap(p.locator('.phone').getByText('Met Oct 2026').first(), 'card'); await wait(p, 1.8);
});
// 4. profile: sheet, scroll, open a moment, play it
await record('profile', async (p) => { await p.getByRole('button', { name: 'Connections list' }).click(); await wait(p, 0.8); }, async (p, tap) => {
  await wait(p, 0.3); await tap(p.locator('.person-row', { hasText: 'Jordan Lee' }).first(), 'row'); await wait(p, 1.5);
  await scroll(p, 12, 60); await wait(p, 0.5); await scroll(p, 14, 70); await wait(p, 0.6);
  await tap(p.locator('.moment-head').first(), 'moment'); await wait(p, 1.0);
  await scroll(p, 10, 55); await wait(p, 0.8);
  await tap(p.getByRole('button', { name: 'Play voice note' }).first(), 'play'); await wait(p, 1.0);
});
// 5. add a moment by talking (from a profile)
await record('moment', openJordan, async (p, tap) => {
  await scroll(p, 8, 60); await wait(p, 0.6);
  await tap(p.getByRole('button', { name: 'Record by voice' }), 'mic'); await wait(p, 5.0);
  await tap(p.getByRole('button', { name: 'Stop recording' }), 'stop'); await wait(p, 0.5);
  await tap(p.getByRole('button', { name: 'Send' }), 'send'); await wait(p, 2.4);
});
// 5b. real playback of a voice note (screenshot loop: the screencast stalls while the player animates)
await record('play', async (p) => { await openJordan(p); await scroll(p, 26, 65); await wait(p, 0.6); await p.locator('.moment-head').first().click(); await wait(p, 1.0); await scroll(p, 10, 55); await wait(p, 0.8); }, async (p, tap) => {
  await wait(p, 0.2); await tap(p.getByRole('button', { name: 'Play voice note' }).first(), 'play'); await wait(p, 8.5);
}, { shots: true });
// 6. ask: type on the iOS keyboard, send, thinking, results, draft
const QS = 'I want to find someone to go climbing with me';
await record('ask', async () => {}, async (p, tap) => {
  await wait(p, 0.4); await tap(p.getByRole('button', { name: 'Ask me about people' }), 'pill'); await wait(p, 1.0);
  for (const ch of QS) {
    const key = ch === ' ' ? p.locator('.kb-key.is-space') : p.locator('.kb-keys button').filter({ hasText: new RegExp('^' + ch + '$', 'i') });
    try { const bb = await key.first().boundingBox({ timeout: 1500 }); if (bb) await p.mouse.click(bb.x + bb.width / 2, bb.y + bb.height / 2); } catch (e) { console.log('  key miss', ch); }
    await wait(p, 0.02);
  }
  await wait(p, 0.4); await tap(p.getByRole('button', { name: 'Send' }), 'send'); await wait(p, 3.2);
  await tap(p.getByRole('button', { name: 'Draft a message' }).first(), 'draft'); await wait(p, 2.0);
});
// 7. different people: one still of each profile sheet
if (!want.length || want.includes('people')) {
  const ctx = await b.newContext({ viewport: { width: 800, height: 1500 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage(); mkdirSync('assets/people', { recursive: true });
  await p.goto(URL, { waitUntil: 'networkidle' }); await p.addStyleTag({ content: '.device{--device-scale:1.5 !important}' }); await wait(p, 1.2);
  { const bb = await p.locator('.phone').boundingBox(); CLIP = { x: Math.round(bb.x), y: Math.round(bb.y), width: 2 * Math.floor(bb.width / 2), height: 2 * Math.floor(bb.height / 2) }; }
  await p.getByRole('button', { name: 'Connections list' }).click(); await wait(p, 0.8);
  const n = await p.locator('.person-row').count();
  for (let i = 0; i < n; i++) {
    await p.goto(URL, { waitUntil: 'networkidle' }); await p.addStyleTag({ content: '.device{--device-scale:1.5 !important}' }); await wait(p, 0.8);
    await p.getByRole('button', { name: 'Connections list' }).click(); await wait(p, 0.7);
    const row = p.locator('.person-row').nth(i); const nm = (await row.innerText()).trim().replace(/\s+/g, '_').slice(0, 24);
    await row.scrollIntoViewIfNeeded(); await row.click(); await wait(p, 1.5);
    await p.screenshot({ path: `assets/people/${String(i).padStart(2, '0')}_${nm}.png`, clip: CLIP });
  }
  console.log('people stills', n); await ctx.close();
}
await b.close();
