import json

meta = json.load(open('assets/figma/profile_meta.json'))
bars = [b for b in meta['bars'] if b['x'] > 68]
open('assets/figma/profile_meta.js', 'w', encoding='utf-8').write('export const BARS = ' + json.dumps(bars) + ';\n')
print('bars', len(bars))

s = open('index.html', encoding='utf-8').read()


def rep(a, b, cnt=1):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, cnt)


# --- imports + assets
rep("import LIVE, { PEOPLE } from './assets/live/data.js';", "import LIVE from './assets/live/data.js';\nimport { BARS } from './assets/figma/profile_meta.js';")
rep("const FR = {}, PIMG = {}; let dotGrid;", "const FR = {}, CARDS = [], PSC = mk(390, 844); let dotGrid, PROF = null;")
rep("  await Promise.all(PEOPLE.map(async (p) => { PIMG[p.id] = await load(`assets/people/${p.id}.png`); }));",
    "  await Promise.all(Array.from({ length: 11 }, async (_, i) => { CARDS[i] = await load(`assets/figma/cards/c${String(i).padStart(2, '0')}.png`); }));\n  PROF = await load('assets/figma/audio_ready_v2.png');")

# --- hero cards -> new Figma people cards (radius measured 20px at 1x, +1 to drop the antialiased edge)
a = s.index("// a person's hero card cut from")
b = s.index("// ---------- product:")
s = s[:a] + """// the new Figma people cards (358x106, corner radius 20 at 1x)
function personCard(i, scale) {
  const w = 358 * scale, h = 106 * scale;
  return bake(`pc${i}@${scale}`, w, h, 60, () => { cardShadow(w, h, 21 * scale, '#222'); ctx.save(); rr(0, 0, w, h, 21 * scale); ctx.clip(); ctx.drawImage(CARDS[i], 0, 0, w, h); ctx.restore(); });
}

""" + s[b:]

# --- phone(): canvas layers (Figma-built screens) as sheets, island option, white thumb dot
rep("  const { t = 0, rot = 0, sc = 1, dx = 0, dy = 0, shadow = 0.4, taps = [] } = o;", "  const { t = 0, rot = 0, sc = 1, dx = 0, dy = 0, shadow = 0.4, taps = [], island = false } = o;")
rep("""    draw(L.im, 1); if (L.im2) draw(L.im2, L.mix);
  }""", """    if (L.cv) { // a Figma-built screen, optionally as a sheet sliding up over what is behind it
      const k = sw / 390, ty = (L.ty || 0) * k, rad = ty > 1 ? 46 * k : 0;
      if (L.scrim) { ctx.fillStyle = `rgba(14,10,22,${L.scrim})`; ctx.fillRect(-sw / 2, -sh / 2, sw, sh); }
      ctx.save(); ctx.beginPath(); ctx.roundRect(-sw / 2, -sh / 2 + ty, sw, sh - ty + 2, [rad, rad, 0, 0]); ctx.clip();
      ctx.drawImage(L.cv, 0, 0, 390, 844, -sw / 2, -sh / 2 + ty, sw, sh); ctx.restore();
      if (ty > 1) { ctx.fillStyle = 'rgba(255,255,255,0.55)'; ctx.beginPath(); ctx.roundRect(-sw * 0.045, -sh / 2 + ty + 8 * k, sw * 0.09, 4 * k, 2 * k); ctx.fill(); }
      continue;
    }
    draw(L.im, 1); if (L.im2) draw(L.im2, L.mix);
  }
  if (island) { ctx.fillStyle = '#000'; rr(-sw * 0.1575, -sh / 2 + sw * 0.028, sw * 0.315, sw * 0.092, sw * 0.046); ctx.fill(); }""")

a = s.index("  for (const [t0, tfx, tfy] of taps) {")
b = s.index("  ctx.restore();\n}\nfunction phone3")
s = s[:a] + """  for (const [t0, tfx, tfy] of taps) { // the thumb: a soft white dot that glides in, presses, ripples and lifts away
    const u = t - t0; if (u < -0.9 || u > 0.9) continue;
    const px = (tfx - 0.5) * sw, py = (tfy - 0.5) * sh, m = ease((u + 0.9) / 0.9), fade = u < 0.45 ? 1 : 1 - clamp((u - 0.45) / 0.45);
    if (u >= 0) {
      const ring2 = ease(u / 0.8);
      ctx.strokeStyle = `rgba(255,255,255,${0.9 * (1 - ring2)})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(px, py, sw * (0.05 + 0.15 * ring2), 0, 7); ctx.stroke();
      ctx.strokeStyle = `rgba(22,18,28,${0.18 * (1 - ring2)})`; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.arc(px, py, sw * (0.056 + 0.15 * ring2), 0, 7); ctx.stroke();
    }
    const bob = Math.sin((u + 0.9) * 7) * (1 - m) * sw * 0.012, ax = px + (1 - m) * sw * 0.34, ay = py + (1 - m) * sh * 0.2 + bob, press = clamp(u / 0.1) * (1 - clamp((u - 0.22) / 0.22)), R = sw * 0.05 * (1 - 0.2 * press);
    ctx.save(); ctx.globalAlpha = fade; ctx.shadowColor = 'rgba(10,6,20,0.32)'; ctx.shadowBlur = sw * 0.04; ctx.shadowOffsetY = sw * 0.012;
    ctx.fillStyle = 'rgba(255,255,255,0.96)'; ctx.beginPath(); ctx.arc(ax, ay, R, 0, 7); ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.strokeStyle = 'rgba(22,18,28,0.14)'; ctx.lineWidth = 1.5; ctx.stroke(); ctx.restore();
  }
""" + s[b:]

# --- profile screen built from the updated Figma frame
rep("// ---------- talking:", """// ---------- profile screen built from the updated Figma frame (108:5579): scroll, compact header, fixed composer, live playback overlay ----------
const WORDS = ['Came across Jordan on my way home and he', 'said how much he hates his job search and that', 'the job market is cooked. He hates his current', 'job and wants out'].map((l) => l.split(' '));
const NWORDS = WORDS.flat().length;
function profileScreen(scroll, pl) { // pl = { p: 0..1 progress, on: playing } or null
  const prev = ctx; ctx = PSC.getContext('2d'); const oy = -scroll;
  ctx.clearRect(0, 0, 390, 844); ctx.fillStyle = '#f4f2ef'; ctx.fillRect(0, 0, 390, 844);
  ctx.drawImage(PROF, 0, scroll, 390, 844, 0, 0, 390, 844);
  if (pl) { // the moment card, redrawn live
    const BG = '#fbfbfb';
    ctx.fillStyle = BG; ctx.fillRect(22, 1090 + oy, 346, 94);
    ctx.font = `400 15px ${F}`; ctx.letterSpacing = '-0.1px'; const fit = 302 / ctx.measureText(WORDS[0].join(' ')).width; ctx.font = `400 ${(15 * fit).toFixed(2)}px ${F}`;
    let wi = 0; WORDS.forEach((line, li) => { let x = 31; line.forEach((w) => { const lit = clamp(pl.p * NWORDS * 1.04 - wi + 0.6); ctx.fillStyle = lit > 0.5 ? '#16121c' : '#9a979f'; ctx.fillText(w, x, 1107 + li * 22 + oy); x += ctx.measureText(w + ' ').width; wi++; }); });
    ctx.fillStyle = BG; ctx.fillRect(66, 1198 + oy, 214, 38);
    BARS.forEach((b, i) => { const done = i / BARS.length < pl.p; ctx.globalAlpha = pl.on ? (done ? 1 : 0.28) : 1; ctx.fillStyle = b.c; ctx.beginPath(); ctx.roundRect(b.x - b.w / 2, b.y0 + oy, b.w, b.y1 - b.y0 + 1, b.w / 2); ctx.fill(); }); ctx.globalAlpha = 1;
    ctx.fillStyle = BG; ctx.fillRect(28, 1196 + oy, 40, 38); ctx.fillStyle = '#16121c'; ctx.beginPath(); ctx.arc(47, 1215 + oy, 15.5, 0, 7); ctx.fill(); ctx.fillStyle = '#fff';
    if (pl.on) { ctx.fillRect(43, 1210 + oy, 3.4, 10); ctx.fillRect(48.6, 1210 + oy, 3.4, 10); } else { ctx.beginPath(); ctx.moveTo(44.5, 1209.5 + oy); ctx.lineTo(53, 1215 + oy); ctx.lineTo(44.5, 1220.5 + oy); ctx.closePath(); ctx.fill(); }
    ctx.fillStyle = BG; ctx.fillRect(324, 1204 + oy, 40, 22); ctx.fillStyle = '#5b5361'; ctx.font = `400 11px ${M}`; ctx.letterSpacing = '0px';
    const el = pl.on ? Math.round(pl.p * 34) : 34, lab = pl.on ? `0:${String(el).padStart(2, '0')}` : '0:34'; ctx.fillText(lab, 356 - ctx.measureText(lab).width, 1219 + oy);
  }
  const ha = clamp((scroll - 70) / 110); // compact blue header once the hero scrolls away, as in the app
  if (ha > 0) { ctx.save(); ctx.globalAlpha = ha; ctx.beginPath(); ctx.roundRect(0, 0, 390, 112, [0, 0, 26, 26]); ctx.clip(); ctx.drawImage(PROF, 0, 0, 390, 112, 0, 0, 390, 112); ctx.fillStyle = '#fff'; ctx.font = `500 18px ${F}`; ctx.letterSpacing = '-0.3px'; ctx.fillText('Jordan Lee', 195 - ctx.measureText('Jordan Lee').width / 2, 91); ctx.restore(); }
  ctx.drawImage(PROF, 0, 1331, 390, 100, 0, 744, 390, 100); // fixed composer
  ctx = prev; return PSC;
}

// ---------- talking:""")

# --- reveal: freeze the map at the View tap, then the new profile slides up as a sheet
a = s.index("function reveal(t)")
b = s.index("function capture(t)")
s = s[:a] + """function liveAt(name, srcT) { const f = LIVE[name], fr = FR[name], u = f.map[clamp(Math.floor(srcT * f.fps), 0, f.n - 1)]; return { im: fr[u] }; }
function reveal(t) { // 5.0 - 8.6: wordmark, 3D phone, the real map: tap a person, View, the profile slides up as a sheet
  words([...'Peepl'], 96, 520, 360, t, 5.3, 8.6, { mode: 'arc', gap: 0.07, dur: 0.9 });
  words(['Remember the people you meet'], 96, 650, 56, t, 5.8, 7.0, { mode: 'zoom', gap: 0.07 }); words(['and their ', ['story.', { hl: true }]], 96, 650, 56, t, 7.0, 8.6, { mode: 'arc', gap: 0.09, hlDelay: 0.3 });
  const r = rig(t, 5.1, 8.6), tView = tapT('map', 'view') ?? 7.35, sheet = sp(t - (tView + 0.05), 90, 16);
  const layers = [t < tView + 0.02 ? live('map', t) : liveAt('map', srcAt('map', tView))];
  if (t > tView + 0.04) layers.push({ cv: profileScreen(0, null), ty: lerp(844, 170, sheet), scrim: 0.3 * sheet });
  phone3(layers, 1360, 560, 930, { t, island: true, ry: lerp(-40, 0, sp(t - 5.1, 70, 15)) + Math.sin(t * 0.9) * 2, dy: r.dy + Math.sin(t * 1.2) * 6, rot: lerp(4, 0, sp(t - 5.2, 90, 16)), taps: tapsOf('map') });
}
""" + s[b:]

# --- capture: stop before the old-design card, drop the card tap
rep("const r = rig(t, 8.7, 14.0);\n  phone3([live('add', t)], 1500, 560, 920, { t, dy: r.dy, ry: lerp(34, 10, sp(t - 8.7, 80, 15)) + Math.sin(t) * 2, rot: lerp(-4, 0, sp(t - 8.7, 90, 16)), taps: tapsOf('add') });",
    "const r = rig(t, 8.7, 13.4);\n  phone3([live('add', Math.min(t, 13.35))], 1500, 560, 920, { t, dy: r.dy, ry: lerp(34, 10, sp(t - 8.7, 80, 15)) + Math.sin(t) * 2, rot: lerp(-4, 0, sp(t - 8.7, 90, 16)), taps: tapsOf('add').filter((k) => k[3] !== 'card' && k[3] !== 'add') });")

# --- field: the new people cards
a = s.index("const FIELD = [")
b = s.index("function moments(t)")
s = s[:a] + """const FIELD = [ // [card, x, y, ry, rz, scale]: ten more people, each card has its own colours and clay avatar
  [1, 1130, 230, 24, -4, 0.95], [2, 1560, 120, -18, 2, 0.9], [3, 1890, 280, -26, 3, 0.95], [4, 1120, 520, 20, 2, 1.0], [5, 1900, 610, -24, -3, 0.92],
  [6, 1170, 810, 22, -2, 0.95], [7, 1560, 860, -16, 3, 1.0], [8, 1900, 940, -22, 2, 0.9], [9, 1300, 1040, 18, -3, 0.85], [10, 1700, 1040, -20, 2, 0.88]];
function field(t) { // 14.0 - 16.1: one card multiplies into different people
  words(['Every person.'], 96, 560, 130, t, 14.3, 15.2, { mode: 'drift', gap: 0.11 });
  words(['Every ', ['story.', { hl: true }]], 96, 560, 130, t, 15.2, 16.1, { mode: 'arc', gap: 0.11, hlDelay: 0.3 });
  const out = ease((t - 16.0) / 0.3); if (out >= 1) return;
  const e0 = sp(t - 14.3, 110, 14);
  if (t > 14.25) { ctx.save(); ctx.globalAlpha = 1 - out; proj(personCard(0, 1.3), lerp(1450, 1530, e0), lerp(1100, 520, e0) + Math.sin(t * 1.3) * 8, lerp(36, -10, e0), -2, 1, 1.0 * (1 + 0.1 * out)); ctx.restore(); }
  FIELD.forEach(([ci, X, Y, ry, rz, s], i) => {
    const t0 = 14.7 + i * 0.08, e = sp(t - t0, 110, 14); if (t < t0 - 0.01) return;
    ctx.save(); ctx.globalAlpha = 1 - out; proj(personCard(ci, 1.3), lerp(1530, X, e), lerp(520, Y, e) + Math.sin(t * 1.3 + i * 1.7) * 10, ry * (0.35 + 0.65 * e) + Math.sin(t * 0.9 + i) * 4, rz, 1, lerp(0.4, s, e) * (1 + 0.1 * out)); ctx.restore();
  });
}
""" + s[b:]

# --- moments: the updated Figma profile, scrolled, then the voice note playing
a = s.index("function moments(t)")
b = s.index("function ask(t)")
s = s[:a] + """function moments(t) { // 16.0 - 22.4: the updated profile slides up, grows full screen, scrolls to the moment; the voice note plays
  eyebrow('02 · The story', 96, 230, t, 16.2, 22.4);
  words(['It keeps the'], 96, 400, 120, t, 16.25, 18.9, { mode: 'swing', gap: 0.12 }); words([['story,', { hl: true }]], 96, 520, 120, t, 16.45, 18.9, { mode: 'zoom' });
  words(['not just the title.'], 96, 640, 120, t, 16.6, 18.9, { mode: 'drift', gap: 0.1 });
  words(['Play it ', ['back.', { hl: true }]], 96, 400, 130, t, 19.0, 22.4, { mode: 'arc', gap: 0.14, hlDelay: 0.3 });
  words(['Every moment keeps'], 96, 540, 60, t, 19.3, 22.4, { mode: 'zoom', gap: 0.08 }); words(['your voice and its words.'], 96, 614, 60, t, 19.5, 22.4, { mode: 'zoom', gap: 0.08 });
  const r = rig(t, 16.1, 22.4), tPlay = 19.65, on = t >= tPlay + 0.05;
  const slide = sp(t - 16.15, 90, 16), grow = ease((t - 16.9) / 0.6), ty = lerp(844, 170, slide) * (1 - grow);
  const scroll = ease((t - 17.1) / 2.2) * 587, pl = t >= tPlay ? { p: clamp((t - tPlay - 0.05) / 4.6) * 0.62, on } : null;
  const layers = [liveAt('map', srcAt('map', tapT('map', 'view') ?? 7.35)), { cv: profileScreen(scroll, pl), ty, scrim: 0.3 * (1 - grow) * slide }];
  phone3(layers, 1180, 560, 920, { t, island: true, dy: r.dy, ry: lerp(-24, 0, sp(t - 16.1, 80, 15)), rot: lerp(-3, 0, sp(t - 16.1, 90, 16)), sc: 1 + 0.07 * ease((t - 19.6) / 2.5), taps: [[tPlay, 47 / 390, (1215 - 587) / 844]] });
  callout('Summary', 'Building battery recycling for e-bikes. Grew up in Seattle, just moved to Brooklyn.', t, 17.3, 18.8, 230);
  callout('Play it back', 'Tap a moment. The waveform fills and the transcript lights up as it plays.', t, 20.0, 22.4, 420, 220);
}
""" + s[b:]

# SEG: drop retired flows
s = s.replace("  profile: [[16.0, 1.6, 1.7]],\n  play: [[19.5, 0.25, 1.5]],\n", "")
open('index.html', 'w', encoding='utf-8').write(s)
print('patched')
