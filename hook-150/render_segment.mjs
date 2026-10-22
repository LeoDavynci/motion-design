// node hook-150/render_segment.mjs --page <html, from the studio root, may end in ?query> --from 2.6 --to 4.6 --out <mp4>
//   [--fps 60 --sub 8] [--speed 1.4 | --speedmap "0:1.4,9.2:1.4,9.8:1"] [--map <json>]
// --speed 1.4 plays the film 1.4x faster (the output is 1/1.4 as long). --speedmap gives the speed at points in the
// film's own time and eases between them (smoothstep), so a shot can slow down without a visible change of pace; before
// the first point and after the last it holds. --map writes the film time at each output frame (for placing sounds).
// Like render.mjs, but renders any [from, to] of a film (render.mjs always starts at 0), and captures each sub-frame as a
// quality-100 JPEG of the page instead of a PNG of #c: with a grainy background a 1080p PNG takes ~400ms to encode, the
// JPEG ~30ms (about 13x faster), and the difference disappears in the sub-frame blend and the H.264 encode.
// Run from ~/motion-design. The film must fill the 1920 x 1080 page from its top-left corner (all the films do).
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const PAGE = arg('page'), OUT = arg('out'), FROM = Number(arg('from', 0)), TO = Number(arg('to'));
const FPS = Number(arg('fps', 60)), SUB = Number(arg('sub', 8)), MAP = arg('map');
const POINTS = (arg('speedmap') || `0:${arg('speed', 1)}`).split(',').map((p) => p.split(':').map(Number));
const speedAt = (t) => {
  if (t <= POINTS[0][0]) return POINTS[0][1];
  for (let i = 1; i < POINTS.length; i++) {
    const [t0, s0] = POINTS[i - 1], [t1, s1] = POINTS[i];
    if (t <= t1) { const x = (t - t0) / (t1 - t0); return s0 + (s1 - s0) * x * x * (3 - 2 * x); }
  }
  return POINTS[POINTS.length - 1][1];
};
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const [FILE, QS] = PAGE.split('?');
await page.goto(pathToFileURL(process.cwd() + '/' + FILE).href + (QS ? '?' + QS : ''));
await page.evaluate(() => window.ready);
const vf = `tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/${FPS}/TB`;
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS * SUB), '-i', '-',
  '-vf', vf, '-r', String(FPS), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });
// Step through the film: each sub-frame advances it by 1/(FPS*SUB) of output time times the speed there; render whole
// output frames only
const dt = 1 / (FPS * SUB), times = [];
for (let t = FROM, i = 0; t < TO || i % SUB !== 0; i++) {
  if (i % SUB === 0) times.push(+t.toFixed(5));
  await page.evaluate((x) => window.seek(x), Math.min(t, TO));
  const jpg = await page.screenshot({ type: 'jpeg', quality: 100, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  if (!ff.stdin.write(jpg)) await new Promise((r) => ff.stdin.once('drain', r));
  t += dt * speedAt(t);
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
if (MAP) writeFileSync(MAP, JSON.stringify({ page: PAGE, fps: FPS, from: FROM, to: TO, times,
  keys: await page.evaluate(() => window.KEYS || []), cues: await page.evaluate(() => window.CUES || {}) }));
await browser.close();
console.log('rendered', PAGE, FROM, '->', TO, 'to', OUT, `(${(times.length / FPS).toFixed(2)}s)`);
