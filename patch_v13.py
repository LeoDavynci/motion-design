p = 'index.html'
s = open(p, encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:70])
    s = s.replace(a, b)


# labels + ghost text removed everywhere
rep("const eyebrow = (s, x, y, t, t0, t1) => words(", "const eyebrow = () => {}; const eyebrow_ = (s, x, y, t, t0, t1) => words(")
rep("function ghost(str, t, t0, t1, y, dir = 1) {\n", "function ghost(str, t, t0, t1, y, dir = 1) {\n  return; // background words compete with the product: removed\n")
# phone exit must clear the frame completely
rep("x * x * H * 0.8 }", "x * x * H * 1.2 }")
# callout: card grows with its text so nothing touches the bottom edge
rep("""  const e = sp(t - t0, 170, 18), x = ease((t - t1) / 0.35); if (t < t0 - 0.01 || x >= 1) return;
  const cx = bx + (1 - e) * 460 + x * 600, cy = y + (1 - e) * 40;""", """  const e = sp(t - t0, 170, 18), x = ease((t - t1) / 0.35); if (t < t0 - 0.01 || x >= 1) return;
  h = Math.max(h, 88 + (wrap(body, 320, `300 26px ${F}`).length - 1) * 34 + 64);
  const cx = bx + (1 - e) * 460 + x * 600, cy = y + (1 - e) * 40;""")
# timeline
rep("import { createPhone3D } from './lib/iphone3d.js';", "import { createPhone3D } from './lib/iphone3d.js';\nimport { SPEC } from './lib/timeline.js';")
rep("const BGS = [[0, 'nA', null], [4.6, 'dA', 'diag'], [8.1, 'dB', 'circle'], [13.6, 'nW', 'curtain'], [15.6, 'nB', 'diagR'], [22.0, 'nC', 'circle'], [26.1, 'nA', 'diag']];", "let BGS = [[0, 'nA', null]]; // filled from the timeline below\nconst PHS = { reveal: 1.8, capture: 1.6, moments: 1.7, ask: 1.8 }; // text plays alone first, then the phone arrives")
# ---- hook: hold the text, then count
rep("zt = ease((t - 1.5) / 1.9)", "zt = ease((t - 3.2) / 1.6)")
rep("ex = 1 - ease((t - 3.0) / 0.4);", "ex = 1 - ease((t - 5.9) / 0.4);")
rep("Math.pow(60, ease((t - 1.65) / 1.9))", "Math.pow(60, ease((t - 3.2) / 1.6))")
rep("a = 1 - ease((t - 3.0) / 0.4);\n    if (a > 0.003)", "a = 1 - ease((t - 5.9) / 0.4);\n    if (a > 0.003)")
rep("t, 1.65, 3.05, { mode: 'drift', gap: 0.07, hlDelay: 0.3 })", "t, 1.65, 6.0, { mode: 'drift', gap: 0.07, hlDelay: 0.3 })")
rep("t, 1.85, 3.05, { mode: 'drift', gap: 0.07 })", "t, 1.85, 6.0, { mode: 'drift', gap: 0.07 })")
# ---- problem: finish each fade, then cards, then swap
rep("t, 3.15, 3.8, { mode: 'swing', gap: 0.1 })", "t, 3.15, 5.6, { mode: 'swing', gap: 0.1 })")
rep("t, 3.3, 3.8, { mode: 'swing', gap: 0.1 })", "t, 3.3, 5.6, { mode: 'swing', gap: 0.1 })")
rep("t, 3.8, 4.7, { mode: 'zoom', gap: 0.1 })", "t, 6.05, 7.4, { mode: 'zoom', gap: 0.1 })")
rep("t, 3.95, 4.7, { mode: 'zoom', gap: 0.1, hlDelay: 0.2 })", "t, 6.2, 7.4, { mode: 'zoom', gap: 0.1, hlDelay: 0.2 })")
rep("const t0 = 3.0 + i * 0.3, e = sp(t - t0, 150, 17), x = ease((t - 4.7 - i * 0.06) / 0.35)", "const t0 = 4.4 + i * 0.3, e = sp(t - t0, 150, 17), x = ease((t - 5.6 - i * 0.06) / 0.35)")
# ---- reveal: text first
rep("function reveal(t) {", "function reveal(t) { const tx = t; t -= PHS.reveal;")
rep("words(['Introducing'], 96, 190, 60, t, 5.05, 8.6,", "words(['Introducing'], 96, 190, 60, tx, 5.05, 8.6 + PHS.reveal,")
rep("words([...'Peepl'], 96, 520, 360, t, 5.45, 8.6,", "words([...'Peepl'], 96, 520, 360, tx, 5.45, 8.6 + PHS.reveal,")
rep("  words(['Remember the people you meet'], 96, 650, 56, t, 5.8, 7.0, { mode: 'zoom', gap: 0.07 }); words(['and their ', ['story.', { hl: true }]], 96, 650, 56, t, 7.0, 8.6,", "  words(['and their ', ['story.', { hl: true }]], 96, 650, 56, tx, 5.9, 8.6 + PHS.reveal,")
# ---- capture
rep("function capture(t) {", "function capture(t) { const tx = t; t -= PHS.capture;")
rep("  eyebrow('01 · Capture', 1000, 230, t, 8.8, 14.0);\n", "")
rep("words(['Talk for'], 1000, 400, 140, t, 8.85, 14.0,", "words(['Talk for'], 1000, 400, 140, tx, 8.85, 14.0 + PHS.capture,")
rep("140, t, 9.1, 14.0, { mode: 'track'", "140, tx, 9.1, 14.0 + PHS.capture, { mode: 'track'")
# ---- field
a = s.index("function field(t) {")
b = s.index("function moments(t)")
s = s[:a] + """function field(t) { // 14.0 - 19.0: the cards arrive, then the headline, then a long hold; the colour wipe waits for it
  const out = ease((t - 18.0) / 0.3); if (out >= 1) return;
  FIELD.forEach(([ci, X, Y, ry, rz, s, edge], i) => {
    const t0 = 14.1 + i * 0.1, e = sp(t - t0, 95, 12.5); if (t < t0 - 0.01) return;
    const flip = i % 2 ? 1 : -1, sx = edge === 'top' ? X + 140 * flip : edge === 'right' ? W + 480 : X + 160 * flip, sy = edge === 'top' ? -300 : edge === 'right' ? Y + 110 * flip : H + 300;
    const spin = (edge === 'top' ? -22 : edge === 'right' ? 16 : 20) * (1 - e), yaw = (edge === 'right' ? -60 : 0) * (1 - e);
    ctx.save(); ctx.globalAlpha = 1 - out; proj(personCard(ci, 1.3), lerp(sx, X, e), lerp(sy, Y, e) + Math.sin(t * 1.3 + i * 1.7) * 10 * e, ry * (0.5 + 0.5 * e) + yaw + Math.sin(t * 0.9 + i) * 4, rz + spin, 1, s * (1 + 0.1 * out)); ctx.restore();
  });
  const w1 = textWidth('Every person.', 130), w2 = textWidth('Every story.', 130);
  words(['Every person.'], 960 - w1 / 2, 575, 130, t, 15.6, 16.5, { mode: 'drift', gap: 0.11 });
  words(['Every ', ['story.', { hl: true }]], 960 - w2 / 2, 575, 130, t, 16.5, 18.6, { mode: 'arc', gap: 0.11, hlDelay: 0.3 });
}
""" + s[b:]
# ---- moments
rep("function moments(t) {", "function moments(t) { const tx = t; t -= PHS.moments; const TE = 19.9 + PHS.moments;")
rep("  eyebrow('02 · The story', 1010, 230, t, 16.2, 22.4);\n", "")
a = s.index("  words(['It keeps the']")
b = s.index("  ghost('STORY'")
s = s[:a] + """  const L1 = 'Not just their name.', fs = Math.min(104, 104 * 860 / textWidth(L1, 104)), y0 = 400;
  words(['Remember the'], 1010, y0, fs, tx, 16.25, TE, { mode: 'swing', gap: 0.12 }); words([['connection.', { hl: true }]], 1010, y0 + fs * 1.08, fs, tx, 16.45, TE, { mode: 'zoom', hlDelay: 0.3 });
  words([L1], 1010, y0 + fs * 2.16, fs, tx, 16.7, TE, { mode: 'drift', gap: 0.1 });
  words(['Play it ', ['back.', { hl: true }]], 1010, 400, 120, t, 19.9, 23.0, { mode: 'arc', gap: 0.14, hlDelay: 0.3 });
  words(['Every moment keeps'], 1010, 520, 56, t, 20.2, 23.0, { mode: 'zoom', gap: 0.08 }); words(['your voice and its words.'], 1010, 592, 56, t, 20.35, 23.0, { mode: 'zoom', gap: 0.08 });
""" + s[b:]
rep("tPlay = 19.65,", "tPlay = 20.6,")
rep("ease((t - 18.0) / 1.3) * 587", "ease((t - 18.6) / 1.3) * 587")
rep("rig(t, 16.1, 22.4)", "rig(t, 16.1, 23.0)")
rep("ease((t - 19.6) / 2.5)", "ease((t - 20.6) / 2.5)", 2)
rep("t, 17.55, 18.0, 760, 200, null, 1010)", "t, 17.5, 18.5, 780, 200, null, 1010)")
a = s.index("  calloutAt('Play it back'")
b = s.index("\n", a)
s = s[:a] + s[b + 1:]
# ---- end
a = s.index("function end(t) {")
b = s.index("const SHOTS = ")
s = s[:a] + """function end(t) { // 26.5 - 31.2: the phone arrives first, then the wordmark and the line
  const tx = t - 0.6;
  words(['Peepl'], 96, 470, 380, tx, 27.4, 99, { mode: 'zoom', w: 300, dur: 0.8 });
  words(['Capture.'], 96, 640, 96, tx, 28.0, 99, { mode: 'arc', w: 400 });
  words(['Search.'], 96 + textWidth('Capture. ', 96, 400), 640, 96, tx, 28.4, 99, { mode: 'drift', w: 400 });
  words(['Reconnect.'], 96 + textWidth('Capture. Search. ', 96, 400), 640, 96, tx, 28.8, 99, { mode: 'zoom', w: 400 });
  words(['Remember the ', ['stories', { hl: true }], ' of the people you meet'], 96, 760, 52, tx, 29.2, 99, { mode: 'arc', gap: 0.09, hlDelay: 0.3 });
  const r = sp(t - 26.9, 90, 15);
  phone3([{ im: FG.mm_a }], 1560, 700 + (1 - r) * 1150, 960, { t, island: true, ry: -18 + 12 * Math.sin(t * 0.9), rx: -4 + 3 * Math.sin(t * 0.7), rot: -4, taps: [[28.6, 0.54, 0.55]] });
}
""" + s[b:]
# ---- shots / timeline
a = s.index("const SHOTS = ")
b = s.rindex("</script>")
s = s[:a] + """const FN = { hook, problem, reveal, capture, field, moments, ask, end };
const SHOTS = [], SEG = [], BGT = {}; let cur = 0;
for (const [name, a, b, ph, fph, segs] of SPEC) { // each scene runs in its own time; sh = shift into film-internal time
  const sh = cur - a; SHOTS.push([cur, cur + ph + (b - a), FN[name], sh]); BGT[name] = cur;
  if (ph) SEG.push([cur, cur + ph, fph]);
  for (const [u0, u1, d] of segs) SEG.push([u0 + sh + ph, u1 + sh + ph, d]);
  cur += ph + (b - a);
}
const TOTAL = SEG.reduce((q, x) => q + x[2], 0); window.TOTAL = TOTAL;
BGS = [[0, 'nA', null], [BGT.reveal - 0.4, 'dA', 'diag'], [BGT.capture - 0.5, 'dB', 'circle'], [BGT.field - 0.4, 'nW', 'curtain'], [BGT.moments - 0.9, 'nB', 'diagR'], [BGT.ask - 0.4, 'nC', 'circle'], [BGT.end - 0.4, 'nA', 'diag']];
function warp(T) { let T0 = 0; for (const [u0, u1, d] of SEG) { if (T <= T0 + d) return u0 + (u1 - u0) * (T - T0) / d; T0 += d; } return cur; }
window.seek = (T) => {
  const t = warp(T);
  ctx = MAIN; background(t);
  for (const [a, b, fn, sh] of SHOTS) if (t >= a - 0.01 && t <= b + 0.6) {
    const z = 1 + 0.03 * ease((t - a) / (b - a)); ctx.save(); ctx.translate(960, 540); ctx.scale(z, z); ctx.translate(-960, -540); fn(t - sh); ctx.restore();
  }
};
""" + s[b:]
open(p, 'w', encoding='utf8').write(s)
print('ok')
