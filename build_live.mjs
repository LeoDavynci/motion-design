// node build_live.mjs -> assets/live/data.js (timing maps for every recorded flow) + assets/people/pNN.png (safe names)
import { readdirSync, readFileSync, writeFileSync, copyFileSync } from 'node:fs';
const out = {};
for (const f of readdirSync('assets/live').filter((n) => n.endsWith('.json'))) {
  const d = JSON.parse(readFileSync(`assets/live/${f}`, 'utf8'));
  out[f.replace('.json', '')] = { fps: d.fps, n: d.n, dur: d.dur, map: d.map, starts: d.starts, taps: d.taps };
}
const people = [];
for (const f of readdirSync('assets/people').filter((n) => /^\d\d_.+\.png$/.test(n)).sort()) {
  const i = f.slice(0, 2); copyFileSync(`assets/people/${f}`, `assets/people/p${i}.png`);
  people.push({ id: `p${i}`, name: f.slice(3, -4).replace(/_/g, ' ') });
}
writeFileSync('assets/live/data.js', `export default ${JSON.stringify(out)};\nexport const PEOPLE = ${JSON.stringify(people)};\n`);
console.log('flows', Object.keys(out).join(', '), '| people', people.length);
