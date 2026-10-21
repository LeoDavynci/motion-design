// node hook-150/render_segment.mjs --page <html, from the studio root, may end in ?query> --from 2.6 --to 4.6 --out <mp4> [--fps 60 --sub 8 --speed 1]
// --speed 0.8 plays the film at 80% speed (the output is 1/0.8 as long).
// Like render.mjs, but renders any [from, to] of a film (render.mjs always starts at 0), and captures each sub-frame as a
// quality-100 JPEG of the page instead of a PNG of #c: with a grainy background a 1080p PNG takes ~400ms to encode, the
// JPEG ~30ms (about 13x faster), and the difference disappears in the sub-frame blend and the H.264 encode.
// Run from ~/motion-design. The film must fill the 1920 x 1080 page from its top-left corner (both films do).
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const PAGE = arg('page'), OUT = arg('out'), FROM = Number(arg('from', 0)), TO = Number(arg('to'));
const FPS = Number(arg('fps', 60)), SUB = Number(arg('sub', 8)), SPEED = Number(arg('speed', 1));
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
const [FILE, QS] = PAGE.split('?');
await page.goto(pathToFileURL(process.cwd() + '/' + FILE).href + (QS ? '?' + QS : ''));
await page.evaluate(() => window.ready);
const vf = `tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/${FPS}/TB`;
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(FPS * SUB), '-i', '-',
  '-vf', vf, '-r', String(FPS), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });
const total = Math.round(((TO - FROM) / SPEED) * FPS * SUB);
for (let i = 0; i < total; i++) {
  await page.evaluate((t) => window.seek(t), FROM + (i / (FPS * SUB)) * SPEED);
  const jpg = await page.screenshot({ type: 'jpeg', quality: 100, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  if (!ff.stdin.write(jpg)) await new Promise((r) => ff.stdin.once('drain', r));
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
await browser.close();
console.log('rendered', PAGE, FROM, '->', TO, 'to', OUT);
