// node hook-150/render_segment.mjs --page <html, from the studio root> --from 2.6 --to 4.6 --out <mp4> [--fps 60 --sub 8]
// Like render.mjs, but renders only [from, to] of a film (render.mjs always starts at 0). Run from ~/motion-design.
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const PAGE = arg('page'), OUT = arg('out'), FROM = Number(arg('from', 0)), TO = Number(arg('to'));
const FPS = Number(arg('fps', 60)), SUB = Number(arg('sub', 8));
const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(process.cwd() + '/' + PAGE).href);
await page.evaluate(() => window.ready);
const vf = `tmix=frames=${SUB},select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/${FPS}/TB`;
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS * SUB), '-i', '-',
  '-vf', vf, '-r', String(FPS), '-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p', OUT], { stdio: ['pipe', 'inherit', 'inherit'] });
const total = Math.round((TO - FROM) * FPS * SUB);
for (let i = 0; i < total; i++) {
  await page.evaluate((t) => window.seek(t), FROM + i / (FPS * SUB));
  const png = await page.locator('#c').screenshot({ type: 'png' });
  if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
}
ff.stdin.end();
await new Promise((r) => ff.on('close', r));
await browser.close();
console.log('rendered', PAGE, FROM, '->', TO, 'to', OUT);
