import { chromium } from 'playwright';
export const OUT = 'assets/figma/v13/';
export async function open(url = 'http://localhost:5173/', hideIsland = true) {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 900, height: 1800 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: '.device{--device-scale:2 !important}' + (hideIsland ? ' .dynamic-island{visibility:hidden !important}' : '') });
  await p.waitForTimeout(1500);
  const clip = await p.locator('.phone').boundingBox();
  return { b, p, clip, shot: (f, c) => p.screenshot({ path: OUT + f, clip: c || clip }) };
}
