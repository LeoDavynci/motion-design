s = open('index.html', encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b, 1)


def cut(a_marker, b_marker, new):  # replace from a_marker up to (not incl.) b_marker
    global s
    a = s.index(a_marker); b = s.index(b_marker)
    s = s[:a] + new + s[b:]


# ---- assets: new hero cards (9) + zoomed avatars, avatars patched onto the Figma app frames
rep("const FG = {}, CARDS = [], PSC", "const FG = {}, CARDS = [], AV = [], PSC")
rep("await Promise.all(Array.from({ length: 11 }, async (_, i) => { CARDS[i] = await load(`assets/figma/cards/c${String(i).padStart(2, '0')}.png`); }));",
    """await Promise.all(Array.from({ length: 9 }, async (_, i) => { CARDS[i] = await load(`assets/figma/cards2/n0${i}.png`); AV[i] = await load(`assets/figma/av/z${i}.png`); }));
  const patchFrame = (key, spots) => { const im = FG[key], c = mk(im.width, im.height), g = c.getContext('2d'); g.drawImage(im, 0, 0); for (const [x, y, d, a] of spots) g.drawImage(AV[a], x - d / 2, y - d / 2, d, d); FG[key] = c; };
  patchFrame('match1', [[73, 329, 74, 1], [73, 550, 62, 6]]); patchFrame('match2', [[73, 329, 74, 1], [73, 597, 62, 6]]); patchFrame('match3', [[73, 329, 74, 1], [73, 597, 62, 6]]);
  patchFrame('add_preview', [[60, 479, 64, 1]]);""")

# ---- profile hero + mutuals use the zoomed avatars
rep("  const ha = clamp((scroll - 70) / 110);",
    """  ctx.drawImage(AV[1], 61 - 41, 171.5 - 41 + oy, 82, 82); // hero avatar
  [[111, 2], [186, 3], [253, 4], [321, 5], [388, 6]].forEach(([x, a]) => ctx.drawImage(AV[a], x - 27, 927 - 27 + oy, 54, 54));
  const ha = clamp((scroll - 70) / 110);""")

# ---- callouts that point at a real spot on the phone screen
rep("function sparkle(", """function scrPt(cx, cy, sh, sc, u, v) { return [cx + (u / 390 - 0.5) * sh * sc * 393 / 852, cy + (v / 844 - 0.5) * sh * sc]; }
function calloutAt(label, body, t, t0, t1, y, h, tgt) { // card on the right, lime leader ends on the exact UI element it describes
  const e = sp(t - t0, 170, 18), x = ease((t - t1) / 0.35); if (t < t0 - 0.01 || x >= 1) return;
  const cx = 1500 + (1 - e) * 460 + x * 600, cy = y + (1 - e) * 40;
  card(cx, cy, 380, h, { dark: true, r: 26 });
  ctx.fillStyle = LIME; ctx.font = `500 18px ${M}`; ctx.letterSpacing = '2.4px'; ctx.fillText(label.toUpperCase(), cx + 28, cy + 42);
  ctx.fillStyle = '#fff'; ctx.font = `300 26px ${F}`; ctx.letterSpacing = '-0.4px';
  wrap(body, 320, `300 26px ${F}`).forEach((l, i) => ctx.fillText(l, cx + 28, cy + 88 + i * 34));
  const lp = ease((t - t0 - 0.15) / 0.4); if (lp <= 0) return;
  const [tx, ty] = tgt, x0 = cx, y0 = cy + h / 2;
  ctx.save(); ctx.strokeStyle = LIME; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(lerp(x0, tx, lp), lerp(y0, ty, lp)); ctx.stroke();
  ctx.fillStyle = LIME; ctx.beginPath(); ctx.arc(lerp(x0, tx, lp), lerp(y0, ty, lp), 8, 0, 7); ctx.fill(); ctx.strokeStyle = 'rgba(22,18,28,0.55)'; ctx.lineWidth = 2; ctx.stroke(); ctx.restore();
}
function sparkle(""")

# ---- hook: 150 coloured dots in a block, then zoom out into a huge grid while the number counts up
cut("function hook(t) {", "function problem(t) {", """function hook(t) { // 0 - 3.4: 150 people you can keep, then the rest of the people you've met: same 150 coloured, grid zooms out, number counts up
  const cx0 = 1290, cy0 = 560, BASE = 56, zt = ease((t - 1.5) / 1.9), sz = Math.exp(Math.log(0.24) * zt), g = BASE * sz, ex = 1 - ease((t - 3.0) / 0.4);
  if (ex > 0.003) {
    const c0 = Math.ceil((740 - cx0) / g + 6), c1 = Math.floor((1900 - cx0) / g + 6), r0 = Math.ceil((-10 - cy0) / g + 5.5), r1 = Math.floor((1090 - cy0) / g + 5.5);
    for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) {
      const x = cx0 + (c - 6) * g, y = cy0 + (r - 5.5) * g, idx = r * 13 + c, inBlock = r >= 0 && r < 12 && c >= 0 && c < 13 && idx < 150, fade = clamp((x - 740) / 70) * ex;
      if (inBlock) { const p = sp(t - idx / 170 - 0.05, 260, 14); if (p <= 0.02) continue; ctx.globalAlpha = fade; ctx.fillStyle = HUES[Math.floor(hash(idx) * 4.99)]; ctx.beginPath(); ctx.arc(x, y, 0.25 * g * Math.max(0, p), 0, 7); ctx.fill(); }
      else { const d = Math.hypot(c - 6, r - 5.5), p = clamp((t - 1.7 - d * 0.022) / 0.35); if (p <= 0) continue; ctx.globalAlpha = fade * (0.14 + 0.3 * p); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, 0.2 * g * ease(p), 0, 7); ctx.fill(); }
    }
    ctx.globalAlpha = 1;
  }
  eyebrow('The Dunbar number', 96, 190, t, -0.2, 3.0);
  if (t < 1.65) {
    const s = 1 + 0.45 * (1 - sp(t + 0.18, 230, 15));
    ctx.save(); ctx.translate(96, 540); ctx.scale(s, s); ctx.translate(-96, -540); words(['150'], 96, 540, 400, t, -0.22, 99, { mode: 'zoom', dur: 0.5 }); ctx.restore();
  } else { // the same 150, now counting up while the grid keeps growing
    const v = Math.round(150 * Math.pow(60, ease((t - 1.65) / 1.9))), str = v.toLocaleString('en-US'), size = Math.min(400, 400 * 640 / textWidth(str, 400)), a = 1 - ease((t - 3.0) / 0.4);
    if (a > 0.003) { ctx.save(); ctx.globalAlpha = a; if (a < 1) ctx.filter = `blur(${((1 - a) * 18).toFixed(1)}px)`; ctx.fillStyle = isDay(t) ? INK : '#fff'; ctx.font = `300 ${size}px ${F}`; ctx.letterSpacing = `${-0.04 * size}px`; ctx.fillText(str, 96, 540 - (1 - a) * 40); ctx.restore(); }
  }
  words(['people you can keep'], 96, 650, 58, t, 0.35, 1.55, { mode: 'arc', gap: 0.08 }); words(['in your head.'], 96, 724, 58, t, 0.6, 1.55, { mode: 'arc', gap: 0.08 });
  words(['The ', ['rest', { hl: true }], ' of the'], 96, 650, 58, t, 1.65, 3.05, { mode: 'drift', gap: 0.07, hlDelay: 0.3 }); words(["people you've met."], 96, 724, 58, t, 1.85, 3.05, { mode: 'drift', gap: 0.07 });
}
""")

# problem words wait for the counter to fade
rep("words(['Meeting people'], 96, 440, 150, t, 2.8, 3.8,", "words(['Meeting people'], 96, 440, 150, t, 3.15, 3.8,")
rep("words(['is easy.'], 96, 590, 150, t, 2.95, 3.8,", "words(['is easy.'], 96, 590, 150, t, 3.3, 3.8,")

# ---- reveal: say what is being introduced before the phone shows up
rep("words([...'Peepl'], 96, 520, 360, t, 5.3, 8.6,", "words(['Introducing'], 96, 262, 64, t, 5.05, 8.6, { mode: 'drift', gap: 0.1 });\n  words([...'Peepl'], 96, 520, 360, t, 5.45, 8.6,")
rep("const r = rig(t, 5.1, 8.6), tView = 7.35", "const r = rig(t, 5.55, 8.6), tView = 7.35")
rep("ry: lerp(-40, 0, sp(t - 5.1, 70, 15))", "ry: lerp(-40, 0, sp(t - 5.55, 70, 15))")
rep("rx: lerp(-8, 0, sp(t - 5.1, 60, 14))", "rx: lerp(-8, 0, sp(t - 5.55, 60, 14))")
rep("rot: lerp(4, 0, sp(t - 5.2, 90, 16)), taps: [[6.05", "rot: lerp(4, 0, sp(t - 5.6, 90, 16)), taps: [[6.05")

# ---- field: text centred, nine new cards all around it
cut("const FIELD = [", "function moments(t) {", """const FIELD = [ // [card, x, y, ry, rz, scale, edge]: nine people ring the centred headline and fly in from the top, right and bottom
  [0, 300, 120, 12, -3, 0.9, 'top'], [1, 960, 90, 0, 1, 0.9, 'top'], [2, 1620, 125, -12, 3, 0.9, 'top'], [3, 225, 345, 14, -2, 0.9, 'top'], [4, 1700, 355, -14, 2, 0.9, 'right'],
  [5, 255, 750, 14, 2, 0.9, 'bottom'], [6, 1680, 740, -14, -2, 0.9, 'right'], [7, 640, 975, 8, -2, 0.9, 'bottom'], [8, 1330, 985, -8, 2, 0.9, 'bottom']];
function field(t) { // 14.0 - 16.1
  const out = ease((t - 16.0) / 0.3); if (out >= 1) return;
  FIELD.forEach(([ci, X, Y, ry, rz, s, edge], i) => {
    const t0 = 14.1 + i * 0.1, e = sp(t - t0, 95, 12.5); if (t < t0 - 0.01) return;
    const flip = i % 2 ? 1 : -1, sx = edge === 'top' ? X + 140 * flip : edge === 'right' ? W + 480 : X + 160 * flip, sy = edge === 'top' ? -300 : edge === 'right' ? Y + 110 * flip : H + 300;
    const spin = (edge === 'top' ? -22 : edge === 'right' ? 16 : 20) * (1 - e), yaw = (edge === 'right' ? -60 : 0) * (1 - e);
    ctx.save(); ctx.globalAlpha = 1 - out; proj(personCard(ci, 1.3), lerp(sx, X, e), lerp(sy, Y, e) + Math.sin(t * 1.3 + i * 1.7) * 10 * e, ry * (0.5 + 0.5 * e) + yaw + Math.sin(t * 0.9 + i) * 4, rz + spin, 1, s * (1 + 0.1 * out)); ctx.restore();
  });
  const w1 = textWidth('Every person.', 130), w2 = textWidth('Every story.', 130);
  words(['Every person.'], 960 - w1 / 2, 575, 130, t, 14.3, 15.2, { mode: 'drift', gap: 0.11 });
  words(['Every ', ['story.', { hl: true }]], 960 - w2 / 2, 575, 130, t, 15.2, 16.1, { mode: 'arc', gap: 0.11, hlDelay: 0.3 });
}
""")

# ---- moments: scroll later so the summary is on screen when it is called out; callouts end on the real elements
rep("const scroll = ease((t - 17.1) / 2.2) * 587", "const scroll = ease((t - 18.0) / 1.3) * 587")
rep("  callout('Summary', 'Building battery recycling for e-bikes. Grew up in Seattle, just moved to Brooklyn.', t, 17.3, 18.8, 230);\n  callout('Play it back', 'Tap a moment. The waveform fills and the transcript lights up as it plays.', t, 20.0, 22.4, 420, 220);",
    """  const PS = 920, pc = 1 + 0.07 * ease((t - 19.6) / 2.5), py = 560 + r.dy;
  calloutAt('Summary', 'Building battery recycling for e-bikes. Grew up in Seattle, just moved to Brooklyn.', t, 17.55, 18.0, 330, 200, scrPt(1180, py, PS, pc, 300, 340 - scroll));
  calloutAt('Play it back', 'Tap a moment. The waveform fills and the transcript lights up as it plays.', t, 20.0, 22.4, 660, 220, scrPt(1180, py, PS, pc, 250, 1215 - scroll));""")

# ---- ask: Why Jordan -> Jordan's row, Draft a message -> the drafted message
rep("  callout('Why Jordan', 'Mentioned in July that he climbs on Tuesdays and wants a climbing buddy.', t, 24.95, 26.3, 220, 230);\n  callout('Draft a message', 'Hi Jordan! Are you still climbing on Tuesdays? Wanna go sometime soon?', t, 25.7, 26.3, 490, 230);",
    """  const ay = 560 + r.dy;
  calloutAt('Why Jordan', 'Mentioned in July that he climbs on Tuesdays and wants a climbing buddy.', t, 24.95, 26.3, 270, 215, scrPt(1180, ay, 920, 1, 215, 322));
  calloutAt('Draft a message', 'Hi Jordan! Are you still climbing on Tuesdays? Wanna go sometime soon?', t, 25.7, 26.3, 520, 215, scrPt(1180, ay, 920, 1, 300, 482));""")
open('index.html', 'w', encoding='utf-8').write(s)
print('patched')
