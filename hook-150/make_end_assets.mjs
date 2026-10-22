// node hook-150/make_end_assets.mjs (from ~/motion-design): two stills for the end of the cut.
// 1. hook-150/assets/end/home_jl.png: the phone's screen from intro.html (the updated mindmap: the new discs and
//    controls, "JL" for Jordan Lee), 786 x 1704 like the main film's screens, without the status bar (his phone draws
//    its own), the pill or the thumb. The main film's last scene shows it (vince_copy.py end).
// 2. hook-150/assets/find/dark.png: the main film's night background as it is at the start of its last scene, for
//    find.html to settle on before it hands over to that scene.
import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { writeFileSync, rmSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });

const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
await p.goto(pathToFileURL(process.cwd() + '/hook-150/intro.html').href);
await p.evaluate(() => window.ready);
await p.evaluate(() => {
  window.seek(window.PHONE_AT + 0.2);
  for (const sel of ['#pill', '#thumb', '.ripple', '#ui .time', '#ui .status', '#island', '#glare']) document.querySelectorAll(sel).forEach((el) => { el.style.visibility = 'hidden'; });
});
await p.screenshot({ path: 'hook-150/assets/end/home_jl.png', clip: { x: 763.5, y: 114, width: 393, height: 852 } });
await p.close();
console.log('saved hook-150/assets/end/home_jl.png');

const tmp = '.cut-bg.tmp.html';
writeFileSync(tmp, execFileSync('python3', ['hook-150/vince_copy.py', 'bg'], { input: execFileSync('cat', ['index.html']) }));
const q = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await q.goto(pathToFileURL(process.cwd() + '/' + tmp).href);
await q.evaluate(() => window.ready);
await q.evaluate(() => window.seek(window.filmTime(window.BGT.end + 0.5)));   // once his wipe into it has finished
await q.screenshot({ path: 'hook-150/assets/find/dark.png', clip: { x: 0, y: 0, width: 1920, height: 1080 } });
rmSync(tmp);
console.log('saved hook-150/assets/find/dark.png');
await b.close();
