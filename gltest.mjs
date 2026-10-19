import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
for (const args of [[], ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist']]) {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files', ...args] });
  const p = await b.newPage({ viewport: { width: 800, height: 800 } });
  p.on('pageerror', (e) => console.log('pageerror', e.message.slice(0, 120)));
  await p.goto(pathToFileURL(process.cwd() + '/gltest.html').href);
  const t0 = Date.now();
  try { await p.waitForFunction(() => window.done, null, { timeout: 25000 }); console.log(args.join(' ') || '(default)', 'OK', JSON.stringify(await p.evaluate(() => window.info)), (Date.now() - t0) + 'ms'); await p.screenshot({ path: 'tmp/gltest.png' }); }
  catch (e) { console.log(args.join(' ') || '(default)', 'FAILED', e.message.slice(0, 80)); }
  await b.close();
}
