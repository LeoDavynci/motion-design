s = open('index.html', encoding='utf-8').read()


def rep(a, b, cnt=1):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b, cnt)


# ---------- imports / assets: Figma frames instead of recorded flows ----------
rep("import LIVE from './assets/live/data.js';\n", "")
rep("const FR = {}, CARDS = [], PSC = mk(390, 844);", "const FG = {}, CARDS = [], PSC = mk(390, 844);")
a = s.index("  for (const [name, f] of Object.entries(LIVE))")
b = s.index("\n", a)
s = s[:a] + """  const FRAMES = { mm_a: 'mm_a', mm_b: 'mm_b', map_in: 'map_in', add_voice: 'v7/add_voice', add_voice_live: 'v7/add_voice_live', add_processing: 'v7/add_processing', add_preview: 'v7/add_preview',
    find_suggest: 'v7/find_suggest', find_query: 'v7/find_query', match1: 'v7/match1', match2: 'v7/match2', match3: 'v7/match3' };
  await Promise.all(Object.entries(FRAMES).map(async ([k, p]) => { FG[k] = await load(`assets/figma/${p}.png`); }));""" + s[b:]

# ---------- replace the recorded-flow time maps with a morph helper ----------
a = s.index("// ---------- time maps")
b = s.index("// ---------- backgrounds")
s = s[:a] + """// ---------- screen morphs: a new state dissolves in from a soft blur while the old one eases back ----------
function stack(t, list, tr = 0.5) { // list = [[t, image, overlayFn], ...]
  let i = 0; for (let j = 0; j < list.length; j++) if (t >= list[j][0]) i = j;
  const p = i > 0 ? ease((t - list[i][0]) / tr) : 1, L = [];
  if (i > 0 && p < 1) L.push({ im: list[i - 1][1], ov: list[i - 1][2] });
  L.push({ im: list[i][1], ov: list[i][2], a: p, sc: 1 + 0.045 * (1 - p), blur: (1 - p) * 9 });
  return L;
}

""" + s[b:]

# ---------- screen(): layer alpha / scale / blur / overlay ----------
a = s.index("    const draw = (im, a) =>")
b = s.index("\n", a)
s = s[:a] + "    const aL = L.a === undefined ? 1 : L.a;" + s[b:]
rep("    draw(L.im, 1); if (L.im2) draw(L.im2, L.mix);\n  }",
    """    ctx.save(); ctx.globalAlpha *= aL; if (L.sc) ctx.scale(L.sc, L.sc); if (L.blur > 0.3) ctx.filter = `blur(${L.blur.toFixed(1)}px)`;
    if (L.im) ctx.drawImage(L.im, 4, 4, L.im.width - 8, L.im.height - 8, -sw / 2, -sh / 2, sw, sh);
    if (L.ov) { ctx.filter = 'none'; ctx.save(); ctx.translate(-sw / 2, -sh / 2); ctx.scale(sw / 390, sh / 844); L.ov(); ctx.restore(); }
    ctx.restore();
  }""")

# ---------- live-input helpers (typing, words, waveform) ----------
rep("// ---------- talking:", """// ---------- live input drawn over the Figma frames (390x844 screen units) ----------
const BOX = '#fbfaf9', TXT = '#5f5b66', TXT2 = '#a8a3ae';
function bars(t, x0, x1, yc) {
  ctx.fillStyle = BOX; ctx.fillRect(x0 - 8, yc - 16, x1 - x0 + 16, 32); ctx.fillStyle = '#2f4fd0';
  for (let x = x0, i = 0; x <= x1; x += 6, i++) {
    const env = 0.3 + 0.7 * Math.abs(Math.sin(t * 4.1 + i * 0.6)) * (0.55 + 0.45 * Math.sin(t * 2.3 + i * 1.7));
    const h = 3 + 22 * env * (0.35 + 0.65 * hash(i + 7)); ctx.fillRect(x, yc - h / 2, 2.4, h);
  }
}
function liveText(str, x, base, maxW, lh, pending, caret, t) {
  const font = `400 14px ${F}`; ctx.font = font; ctx.letterSpacing = '-0.1px';
  const ls = wrap(str, maxW, font); let lx = x, ly = base;
  ls.forEach((l, i) => {
    ly = base + i * lh;
    if (pending && i === ls.length - 1 && l.includes(' ')) { const k = l.lastIndexOf(' '), head = l.slice(0, k + 1); ctx.fillStyle = TXT; ctx.fillText(head, x, ly); ctx.fillStyle = TXT2; ctx.fillText(l.slice(k + 1), x + ctx.measureText(head).width, ly); }
    else { ctx.fillStyle = pending && i === ls.length - 1 ? TXT2 : TXT; ctx.fillText(l, x, ly); }
    lx = x + ctx.measureText(l).width;
  });
  if (caret && Math.floor(t * 2.4) % 2 === 0) { ctx.fillStyle = INK; ctx.fillRect(lx + 1.5, ly - 12, 1.4, 16); }
}
// iOS keyboard key rectangles measured from the Figma frame (x, y, w, h)
const KEYROWS = [['qwertyuiop', [7, 45, 84, 122, 160, 198, 237, 275, 313, 351], 563], ['asdfghjkl', [27, 65, 103, 141, 179, 217, 255, 293, 332], 617], ['zxcvbnm', [65, 103, 141, 179, 217, 255, 293], 671]];
function keyRect(ch) { if (ch === ' ') return [105, 725, 180, 43]; for (const [row, xs, y] of KEYROWS) { const i = row.indexOf(ch.toLowerCase()); if (i >= 0) return [xs[i], y, 32, 43]; } return null; }
function keyPop(ch, upper) { // the pressed key darkens and its magnified letter bubble rises above it, like iOS
  const k = keyRect(ch); if (!k) return;
  ctx.save(); ctx.fillStyle = 'rgba(150,152,172,0.5)'; ctx.beginPath(); ctx.roundRect(k[0], k[1], k[2], k[3], 8); ctx.fill();
  if (ch !== ' ') { ctx.shadowColor = 'rgba(10,6,20,0.25)'; ctx.shadowBlur = 8; ctx.shadowOffsetY = 3; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.roundRect(k[0] - 8, k[1] - 56, k[2] + 16, 60, 12); ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.fillStyle = '#16121c'; ctx.font = `400 30px ${F}`; ctx.letterSpacing = '0px'; const g = upper ? ch.toUpperCase() : ch; ctx.fillText(g, k[0] + k[2] / 2 - ctx.measureText(g).width / 2, k[1] - 14); }
  ctx.restore();
}

// ---------- talking:""")

# ---------- reveal + capture ----------
a = s.index("function liveAt(")
b = s.index("const FIELD = [")
s = s[:a] + """function reveal(t) { // 5.0 - 8.6: wordmark, 3D phone, the Figma mind map: tap a person, View, the profile slides up as a sheet
  words([...'Peepl'], 96, 520, 360, t, 5.3, 8.6, { mode: 'arc', gap: 0.07, dur: 0.9 });
  words(['Remember the people you meet'], 96, 650, 56, t, 5.8, 7.0, { mode: 'zoom', gap: 0.07 }); words(['and their ', ['story.', { hl: true }]], 96, 650, 56, t, 7.0, 8.6, { mode: 'arc', gap: 0.09, hlDelay: 0.3 });
  const r = rig(t, 5.1, 8.6), tView = 7.35, sheet = sp(t - (tView + 0.05), 90, 16);
  const layers = t < tView + 0.04 ? stack(t, [[5.0, FG.mm_a], [6.25, FG.mm_b]], 0.55) : [{ im: FG.mm_b }, { cv: profileScreen(0, null), ty: lerp(844, 170, sheet), scrim: 0.3 * sheet }];
  phone3(layers, 1360, 560, 930, { t, island: true, ry: lerp(-40, 0, sp(t - 5.1, 70, 15)) + Math.sin(t * 0.9) * 2, rx: lerp(-8, 0, sp(t - 5.1, 60, 14)), dy: r.dy + Math.sin(t * 1.2) * 6, rot: lerp(4, 0, sp(t - 5.2, 90, 16)), taps: [[6.05, 0.324, 0.317], [tView, 0.52, 0.255]] });
}
const NOTE_S = 'Jordan Lee, met at Demo Day. Founder at [Startup], battery recycling for e-bikes. From Seattle, lives in Brooklyn now. Climbs Tuesdays. Owe them a hardware engineer intro.';
function capture(t) { // 8.6 - 14.0: the voice flow from the Figma frames: words arrive over a moving waveform, 20 s timer, check + confetti
  const tStart = 8.95, tStop = 12.2, nw = clamp((t - tStart) / 0.1, 0, NOTE.length);
  eyebrow('01 · Capture', 96, 230, t, 8.8, 14.0);
  words(['Talk for'], 96, 400, 140, t, 8.85, 14.0, { mode: 'arc', gap: 0.12 }); words([['20 seconds.', { hl: true }]], 96, 540, 140, t, 9.1, 14.0, { mode: 'track', hlDelay: 0.4 });
  const ce = sp(t - 9.0, 150, 18), cx = ease((t - 13.3) / 0.3);
  if (t > 8.9 && cx < 1) voiceCard(t, 96 - cx * 900, 640 + (1 - ce) * 400, 780, 330, nw, t > tStart && t < tStop);
  timer(t, 1040, 800, 84, tStart, tStop);
  const ovTalk = () => { ctx.fillStyle = BOX; ctx.fillRect(24, 636, 348, 86); bars(t, 54, 231, 749); if (nw > 0) liveText(NOTE.slice(0, Math.max(1, Math.floor(nw))).join(' '), 31, 656, 336, 19, nw < NOTE.length, false, t); };
  const r = rig(t, 8.7, 14.0);
  const layers = stack(t, [[8.6, FG.add_voice], [8.85, FG.add_voice_live, ovTalk], [12.4, FG.add_processing], [13.0, FG.add_preview]], 0.5);
  phone3(layers, 1500, 560, 920, { t, island: true, dy: r.dy, ry: lerp(34, 10, sp(t - 8.7, 80, 15)) + Math.sin(t) * 2, rx: lerp(-6, 0, sp(t - 8.7, 60, 14)), rot: lerp(-4, 0, sp(t - 8.7, 90, 16)), taps: [[tStop, 0.742, 0.886]] });
}
""" + s[b:]

# ---------- field: cards fly in from the top, right and bottom edges ----------
a = s.index("const FIELD = [")
b = s.index("function moments(t)")
s = s[:a] + """const FIELD = [ // [card, x, y, ry, rz, scale]: eleven people, each card has its own colours and clay avatar
  [0, 1530, 560, -8, -2, 1.05], [1, 1130, 230, 24, -4, 0.95], [2, 1560, 120, -18, 2, 0.9], [3, 1890, 280, -26, 3, 0.95], [4, 1120, 520, 20, 2, 1.0], [5, 1900, 610, -24, -3, 0.92],
  [6, 1170, 810, 22, -2, 0.95], [7, 1560, 860, -16, 3, 1.0], [8, 1900, 940, -22, 2, 0.9], [9, 1300, 1040, 18, -3, 0.85], [10, 1700, 1040, -20, 2, 0.88]];
const ENTRY = ['top', 'right', 'bottom'];
function field(t) { // 14.0 - 16.1: people arrive from the top, the right and the bottom of the frame
  words(['Every person.'], 96, 560, 130, t, 14.3, 15.2, { mode: 'drift', gap: 0.11 });
  words(['Every ', ['story.', { hl: true }]], 96, 560, 130, t, 15.2, 16.1, { mode: 'arc', gap: 0.11, hlDelay: 0.3 });
  const out = ease((t - 16.0) / 0.3); if (out >= 1) return;
  FIELD.forEach(([ci, X, Y, ry, rz, s], i) => {
    const edge = ENTRY[i % 3], t0 = 14.1 + i * 0.1, e = sp(t - t0, 95, 12.5); if (t < t0 - 0.01) return;
    const flip = i % 2 ? 1 : -1, sx = edge === 'top' ? X + 140 * flip : edge === 'right' ? W + 480 : X + 160 * flip, sy = edge === 'top' ? -300 : edge === 'right' ? Y + 110 * flip : H + 300;
    const spin = (edge === 'top' ? -22 : edge === 'right' ? 16 : 20) * (1 - e), yaw = (edge === 'right' ? -60 : 0) * (1 - e);
    ctx.save(); ctx.globalAlpha = 1 - out; proj(personCard(ci, 1.3), lerp(sx, X, e), lerp(sy, Y, e) + Math.sin(t * 1.3 + i * 1.7) * 10 * e, ry * (0.5 + 0.5 * e) + yaw + Math.sin(t * 0.9 + i) * 4, rz + spin, 1, s * (1 + 0.1 * out)); ctx.restore();
  });
}
""" + s[b:]

# ---------- moments: backdrop is the Figma map frame ----------
rep("const layers = [liveAt('map', srcAt('map', tapT('map', 'view') ?? 7.35)), { cv: profileScreen(scroll, pl), ty, scrim: 0.3 * (1 - grow) * slide }];",
    "const layers = [{ im: FG.mm_b }, { cv: profileScreen(scroll, pl), ty, scrim: 0.3 * (1 - grow) * slide }];")

# ---------- ask + end ----------
a = s.index("function ask(t)")
b = s.index("const SHOTS")
s = s[:a] + """function ask(t) { // 22.4 - 26.5: tap the bar, type on the iOS keyboard (key pops), send, results, draft - all the Figma frames
  const QS = 'I want to find someone to go climbing with me', tType = 23.0, dt = 0.031, nq = clamp(Math.floor((t - tType) / dt), 0, QS.length), tSend = 24.5;
  eyebrow('03 · Ask', 96, 230, t, 22.6, 26.5);
  words(['Ask your'], 96, 400, 130, t, 22.65, 26.5, { mode: 'drift', gap: 0.12 }); words(['own ', ['notes.', { hl: true }]], 96, 535, 130, t, 22.9, 26.5, { mode: 'arc', gap: 0.12, hlDelay: 0.3 });
  ['I want a climbing buddy.', "I'm in SF next month.", 'I just met a founder.'].forEach((q, i) => {
    const t0 = 23.0 + i * 0.25, e = sp(t - t0, 170, 18), x = ease((t - 26.2) / 0.3); if (t < t0 - 0.01 || x >= 1) return;
    const act = i === 0 && t > tSend, y = 660 + i * 92;
    ctx.save(); ctx.translate(-(1 - e) * 700 - x * 800, 0);
    ctx.fillStyle = act ? LIME : 'rgba(255,255,255,0.09)'; rr(96, y, 640, 70, 35); ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,0.22)'; ctx.lineWidth = 2; rr(96, y, 640, 70, 35); ctx.stroke();
    ctx.fillStyle = act ? INK : '#fff'; ctx.font = `400 30px ${F}`; ctx.letterSpacing = '-0.5px'; ctx.fillText(q, 134, y + 45); ctx.restore();
  });
  const ovType = () => {
    ctx.fillStyle = '#fbfbf8'; ctx.fillRect(28, 394, 306, 52); liveText(QS.slice(0, nq), 36, 414, 296, 19, false, t < tSend, t);
    const i = nq - 1, age = t - (tType + i * dt); if (i >= 0 && nq < QS.length && age < 0.11) keyPop(QS[i], i === 0);
  };
  const r = rig(t, 22.1, 26.5);
  const layers = stack(t, [[22.4, FG.find_suggest], [22.9, FG.find_query, ovType], [24.7, FG.match1], [25.5, FG.match2]], 0.5);
  phone3(layers, 1180, 560, 920, { t, island: true, dy: r.dy, ry: lerp(26, 0, sp(t - 22.1, 80, 15)), rx: lerp(-6, 0, sp(t - 22.1, 60, 14)), rot: lerp(3, 0, sp(t - 22.1, 90, 16)), taps: [[22.7, 0.5, 0.556], [tSend, 0.862, 0.553], [25.3, 0.254, 0.545]] });
  callout('Why Jordan', 'Mentioned in July that he climbs on Tuesdays and wants a climbing buddy.', t, 24.95, 26.3, 220, 230);
  callout('Draft a message', 'Hi Jordan! Are you still climbing on Tuesdays? Wanna go sometime soon?', t, 25.7, 26.3, 490, 230);
}
function end(t) { // 26.5 - 30: sparkle -> wordmark -> Capture. Ask. Act.
  const wmW = textWidth('Peepl', 380), e = sp(t - 26.7, 110, 12), rot = (t - 26.7) * 2.4;
  const settle = ease((t - 27.3) / 0.5), px = lerp(960, 96 + wmW + 40, settle), py = lerp(540, 330, settle), R = lerp(150 * e, 34, settle);
  if (t > 26.65) sparkle(px, py, Math.max(0, R), rot, LIME);
  words(['Peepl'], 96, 470, 380, t, 27.4, 99, { mode: 'zoom', w: 300, dur: 0.8 });
  words([['Capture.', { c: LIME }]], 96, 640, 96, t, 28.0, 99, { mode: 'arc', w: 400 });
  words([['Ask.', { c: LIME }]], 96 + textWidth('Capture. ', 96, 400), 640, 96, t, 28.4, 99, { mode: 'drift', w: 400 });
  words(['Act.'], 96 + textWidth('Capture. Ask. ', 96, 400), 640, 96, t, 28.8, 99, { mode: 'zoom', w: 400 });
  words(['Remember the ', ['story.', { hl: true }]], 96, 760, 56, t, 29.2, 99, { mode: 'arc', gap: 0.09, hlDelay: 0.3 });
  const r = sp(t - 26.9, 90, 15);
  phone3([{ im: FG.map_in }], 1560, 700 + (1 - r) * 800, 960, { t, island: true, ry: -18 + 12 * Math.sin(t * 0.9), rx: -4 + 3 * Math.sin(t * 0.7), rot: -4, taps: [[28.2, 0.54, 0.55]] });
}
""" + s[b:]
s = s.replace("// Peepl launch film v7:", "// Peepl launch film v8:")
open('index.html', 'w', encoding='utf-8').write(s)
print('patched v8')
