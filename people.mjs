import { chromium } from 'playwright';
const b = await chromium.launch();
const picks = [0, 2, 5, 9, 14, 20, 27, 35, 44, 52, 61, 73, 85, 97];
for (const i of picks) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  await p.goto('http://localhost:5173/?mock=100', { waitUntil: 'networkidle' });
  await p.click('button[aria-label="Connections list"]'); await p.waitForTimeout(500);
  const name = await p.locator('.person-row').nth(i).innerText().catch(() => '');
  await p.locator('.person-row').nth(i).scrollIntoViewIfNeeded().catch(() => {});
  await p.locator('.person-row').nth(i).click(); await p.waitForTimeout(1500);
  await p.screenshot({ path: `assets/people/p${String(i).padStart(2, '0')}.png` });
  console.log(i, name.replace(/\n/g, ' | '));
  await ctx.close();
}
await b.close();
