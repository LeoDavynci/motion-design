import re
p = 'index.html'
s = open(p, encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)


# ---- head: profile coordinates of the updated page
rep('<script type="importmap">', '<script src="assets/figma/v13/profile_meta.js"></script>\n<script type="importmap">')
rep("import { BARS } from './assets/figma/profile_meta.js';\n", "")
rep("const W = 1920, H = 1080,", "const BARS = window.PROFILE_META_V13.bars;\nconst W = 1920, H = 1080,")

# ---- assets: updated frames, no status-bar blur
rep("const FG = {}, CARDS = [], AV = [], PSC = mk(390, 844);", "const FG = {}, CARDS = [], AV = [], SEQ = [], PSC = mk(390, 844); let COMP, HDR, BGC = '#fbf9f8';")
rep("add_voice: 'v7/add_voice', add_voice_live: 'v7/add_voice_live', add_processing: 'v7/add_processing', add_preview: 'v7/add_preview',",
    "add_voice: 'v7/add_voice', add_voice_live: 'v7/add_voice_live', add_processing: 'v13/processing', add_skeleton: 'v13/skeleton', add_preview: 'v13/preview', home_map: 'v13/home_map',")
rep("  patchFrame('add_preview', [[67, 480, 63, 1]]);\n", "")
a = s.index("  PROF = await load('assets/figma/audio_ready_v2.png');")
b = s.index("  dotGrid = mk(W, H);")
s = s[:a] + """  PROF = await load('assets/figma/v13/profile_full.png'); COMP = await load('assets/figma/v13/profile_composer.png'); HDR = await load('assets/figma/v13/profile_header_compact.png');
  { const c = mk(780, 40), g = c.getContext('2d'); g.drawImage(PROF, 0, 2380, 780, 40, 0, 0, 780, 40); const d = g.getImageData(700, 10, 1, 1).data; BGC = `rgb(${d[0]},${d[1]},${d[2]})`; } // the moment card's own fill
  await Promise.all(Array.from({ length: 73 }, async (_, i) => { SEQ[i] = await load(`assets/figma/v13/ask_seq/f${String(i).padStart(3, '0')}.png`); }));
""" + s[b:]

# ---- profile screen from the updated page
a = s.index("function profileScreen(scroll, pl) {")
b = s.index("// ---------- live input drawn over the Figma frames")
s = s[:a] + """const PMAX = 571; // page is 1415 tall: the last scroll position puts the composer exactly where it is pinned
function profileScreen(scroll, pl) { // pl = { p: 0..1 progress, on: playing } or null
  const prev = ctx; ctx = PSC.getContext('2d'); const oy = -scroll;
  ctx.clearRect(0, 0, 390, 844); ctx.fillStyle = '#f4f2ef'; ctx.fillRect(0, 0, 390, 844);
  ctx.drawImage(PROF, 0, scroll * 2, 780, 1688, 0, 0, 390, 844);
  if (pl) { // the moment card, redrawn live
    ctx.fillStyle = BGC; ctx.fillRect(26, 1100 + oy, 338, 96);
    ctx.font = `400 15px ${F}`; ctx.letterSpacing = '-0.1px'; const fit = 302 / ctx.measureText(WORDS[0].join(' ')).width; ctx.font = `400 ${(15 * fit).toFixed(2)}px ${F}`;
    let wi = 0; WORDS.forEach((line, li) => { let x = 31; line.forEach((w) => { const lit = clamp(pl.p * NWORDS * 1.04 - wi + 0.6); ctx.fillStyle = lit > 0.5 ? '#16121c' : '#9a979f'; ctx.fillText(w, x, 1119 + li * 22 + oy); x += ctx.measureText(w + ' ').width; wi++; }); });
    ctx.fillStyle = BGC; ctx.fillRect(66, 1206 + oy, 214, 42);
    BARS.forEach((b, i) => { const done = i / BARS.length < pl.p; ctx.globalAlpha = pl.on ? (done ? 1 : 0.28) : 1; ctx.fillStyle = b.c; ctx.beginPath(); ctx.roundRect(b.x, b.y0 + oy, b.w, b.y1 - b.y0 + 1, b.w / 2); ctx.fill(); }); ctx.globalAlpha = 1;
    ctx.fillStyle = BGC; ctx.fillRect(28, 1208 + oy, 38, 38); ctx.fillStyle = '#16121c'; ctx.beginPath(); ctx.arc(46, 1227 + oy, 17, 0, 7); ctx.fill(); ctx.fillStyle = '#fff';
    if (pl.on) { ctx.fillRect(41.5, 1221 + oy, 3.4, 12); ctx.fillRect(47.6, 1221 + oy, 3.4, 12); } else { ctx.beginPath(); ctx.moveTo(43, 1220.5 + oy); ctx.lineTo(52.5, 1227 + oy); ctx.lineTo(43, 1233.5 + oy); ctx.closePath(); ctx.fill(); }
    ctx.fillStyle = BGC; ctx.fillRect(322, 1216 + oy, 44, 24); ctx.fillStyle = '#5b5361'; ctx.font = `400 11px ${M}`; ctx.letterSpacing = '0px';
    const el = pl.on ? Math.round(pl.p * 34) : 34, lab = pl.on ? `0:${String(el).padStart(2, '0')}` : '0:34'; ctx.fillText(lab, 357 - ctx.measureText(lab).width, 1231 + oy);
  }
  const ha = clamp((scroll - 70) / 110); // compact blue header once the hero scrolls away, as in the app
  if (ha > 0) { ctx.save(); ctx.globalAlpha = ha; ctx.drawImage(HDR, 0, 0, 390, 130); ctx.restore(); }
  ctx.drawImage(COMP, 0, 745, 390, 99); // fixed composer
  ctx = prev; return PSC;
}

""" + s[b:]

# ---- capture: the updated processing -> skeleton -> profile card frames replace the drawn card
a = s.index("  const ovCard = () => {")
b = s.index("  const layers = stack2(t, [[8.6, FG.add_voice]")
c = s.index("\n", b)
s = s[:a] + "  const layers = stack2(t, [[8.6, FG.add_voice], [8.85, FG.add_voice_live, ovTalk], [12.4, FG.add_processing, null, 'up'], [12.9, FG.add_skeleton], [13.15, FG.add_preview]], 0.55);" + s[c:]

# ---- moments
rep("ease((t - 18.6) / 1.3) * 587", "ease((t - 18.6) / 1.3) * PMAX")
rep("taps: [[tPlay, 47 / 390, (1215 - 587) / 844]]", "taps: [[tPlay, 46 / 390, (1227 - PMAX) / 844]]")

# ---- ask: text first, then the phone; real dev-build thinking -> result
a = s.index("function ask(t) {")
b = s.index("function end(t) {")
s = s[:a] + """function ask(t) { const tx = t; t -= PHS.ask; // 22.0 - 29.95: text and prompts first, then the phone types, sends, thinks and answers (frames recorded from the dev build)
  const QS = 'I want to find someone to go climbing with me', tType = 23.0, dt = 0.031, nq = clamp(Math.floor((t - tType) / dt), 0, QS.length), tSend = 24.5, TE = 29.5 + PHS.ask;
  words(['Ask your'], 96, 400, 130, tx, 22.65, TE, { mode: 'drift', gap: 0.12 }); words(['own ', ['notes.', { hl: true }]], 96, 535, 130, tx, 22.9, TE, { mode: 'arc', gap: 0.12, hlDelay: 0.3 });
  ['I want a climbing buddy.', "I'm in SF next month.", 'I just met a founder.'].forEach((q, i) => {
    const t0 = 23.0 + i * 0.25, e = sp(tx - t0, 170, 18), x = ease((tx - TE) / 0.3); if (tx < t0 - 0.01 || x >= 1) return;
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
  const r = rig(t, 22.1, 29.5);
  const fr = SEQ[clamp(Math.floor((t - tSend) * 12), 0, SEQ.length - 1)];
  const layers = t < tSend ? stack2(t, [[22.4, FG.find_suggest], [22.9, FG.find_query, ovType]], 0.55) : [{ im: FG.find_query, ov: ovType }, { im: fr, a: ease((t - tSend) / 0.2) }];
  phone3(layers, 1010, 560, 920, { t, island: true, dy: r.dy, ry: lerp(26, 0, sp(t - 22.1, 80, 15)), rx: lerp(-6, 0, sp(t - 22.1, 60, 14)), rot: lerp(3, 0, sp(t - 22.1, 90, 16)), taps: [[22.7, 0.5, 0.556], [tSend, 0.862, 0.553]] });
  calloutAt('Why Jordan', 'Climbs Tuesdays and wants a climbing buddy.', t, 28.1, 29.4, 270, 215, scrPt(1010, 560 + r.dy, 920, 1, 215, 270), 1430);
}
""" + s[b:]

# ---- end: updated home mindmap, no star
rep("phone3([{ im: FG.mm_a }], 1560,", "phone3([{ im: FG.home_map }], 1560,")
open(p, 'w', encoding='utf8').write(s)
print('ok')
