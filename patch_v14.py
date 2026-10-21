import re
p = 'index.html'
s = open(p, encoding='utf8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


# ---- head: v14 profile coordinates + keyboard keys
rep('<script src="assets/figma/v13/profile_meta.js"></script>', '<script src="assets/figma/v14/profile_meta.js"></script>\n<script src="assets/figma/v14/keyboard.js"></script>')
rep("const BARS = window.PROFILE_META_V13.bars;", "const PM = window.PROFILE_META_V14, BARS = PM.waveform.bars, KBJ = window.KEYS_V14;")

# ---- frames: only the newest Figma exports, no status bar, no keyboard
a = s.index("  const FRAMES = {")
b = s.index("  PROF = await load(")
s = s[:a] + """  const FRAMES = { home_out: 'v14/home_zoomed_out', home_in: 'v14/home_zoomed_in', home_tap: 'v14/home_tap', add_voice: 'v14/add_1_recording', add_voice_live: 'v14/add_2_live',
    add_processing: 'v14/add_3_processing', add_skeleton: 'v14/add_4_skeleton', add_preview: 'v14/add_5_preview', find_suggest: 'v14/ask_1_suggest', find_query: 'v14/ask_2_query' };
  await Promise.all(Object.entries(FRAMES).map(async ([k, p]) => { FG[k] = await load(`assets/figma/${p}.png`); }));
  await Promise.all(Array.from({ length: 9 }, async (_, i) => { CARDS[i] = await load(`assets/figma/cards2/n0${i}.png`); AV[i] = await load(`assets/figma/av/z${i}.png`); }));
  SB.light = await load('assets/figma/v14/status_light.png'); SB.dark = await load('assets/figma/v14/status_dark.png'); KB = await load('assets/figma/v14/keyboard.png');
  { const c = mk(1, 1), g = c.getContext('2d'); g.drawImage(FG.home_tap, 540, 1000, 1, 1, 0, 0, 1, 1); const d = g.getImageData(0, 0, 1, 1).data; PILLC = `rgb(${d[0]},${d[1]},${d[2]})`; } // pill fill, to swap the demo name
""" + s[b:]
rep("let COMP, HDR, BGC = '#fbf9f8';", "let COMP, HDR, KB, PILLC = '#f1eef6', BGC = '#fbf9f8';")
rep("assets/figma/v13/profile_full.png", "assets/figma/v14/profile_full.png")
rep("assets/figma/v13/profile_composer.png", "assets/figma/v14/profile_composer.png")
rep("assets/figma/v13/profile_header_compact.png", "assets/figma/v14/profile_header_compact.png")
rep("Array.from({ length: 73 }", "Array.from({ length: 65 }")
rep("assets/figma/v13/ask_seq/", "assets/figma/v14/ask_seq/")

# ---- profile screen from the new components (hero + body + pinned composer; status bar is an overlay)
a = s.index("const PMAX = ")
b = s.index("// ---------- live input drawn over the Figma frames")
s = s[:a] + """const PMAX = PM.page.h - 844; // last scroll position: the moment card sits just above the pinned composer
const PCARD = PM.moment_card, PPLAY = PCARD.play;
function profileScreen(scroll, pl) { // pl = { p: 0..1 progress, on: playing } or null
  const prev = ctx; ctx = PSC.getContext('2d'); const oy = -scroll;
  ctx.clearRect(0, 0, 390, 844); ctx.fillStyle = '#f4f2ef'; ctx.fillRect(0, 0, 390, 844);
  ctx.drawImage(PROF, 0, scroll * 2, 780, 1688, 0, 0, 390, 844);
  if (pl) { // the moment card, redrawn live: words light up, bars fill, button flips to pause
    const t0 = PCARD.body_text, ty0 = t0.y + oy;
    ctx.fillStyle = BGC; ctx.fillRect(PCARD.x + 6, ty0 - 4, PCARD.w - 12, t0.h + 6);
    ctx.font = `400 15px ${F}`; ctx.letterSpacing = '-0.1px'; const fit = (t0.w - 24) / ctx.measureText(WORDS[0].join(' ')).width; ctx.font = `400 ${(15 * fit).toFixed(2)}px ${F}`;
    let wi = 0; WORDS.forEach((line, li) => { let x = t0.x; line.forEach((w) => { const lit = clamp(pl.p * NWORDS * 1.04 - wi + 0.6); ctx.fillStyle = lit > 0.5 ? '#16121c' : '#8d8590'; ctx.fillText(w, x, t0.y + 16.5 + li * t0.lineH + oy); x += ctx.measureText(w + ' ').width; wi++; }); });
    const wf = PM.waveform; ctx.fillStyle = BGC; ctx.fillRect(wf.x - 4, wf.y - 6 + oy, wf.w + 8, wf.h + 12);
    BARS.forEach((b, i) => { const done = i / BARS.length < pl.p; ctx.fillStyle = pl.on && !done ? '#d8d8d8' : b.color; ctx.beginPath(); ctx.roundRect(b.x, b.y0 + oy, b.w, b.y1 - b.y0, 1); ctx.fill(); });
    ctx.fillStyle = BGC; ctx.fillRect(PPLAY.x - 3, PPLAY.y - 3 + oy, PPLAY.w + 6, PPLAY.h + 6); ctx.fillStyle = '#16121c'; ctx.beginPath(); ctx.arc(PPLAY.cx, PPLAY.cy + oy, 16, 0, 7); ctx.fill(); ctx.fillStyle = '#fff';
    if (pl.on) { ctx.fillRect(PPLAY.cx - 5.5, PPLAY.cy - 6 + oy, 3.4, 12); ctx.fillRect(PPLAY.cx + 0.6, PPLAY.cy - 6 + oy, 3.4, 12); } else { ctx.beginPath(); ctx.moveTo(PPLAY.cx - 3.5, PPLAY.cy - 6 + oy); ctx.lineTo(PPLAY.cx + 6, PPLAY.cy + oy); ctx.lineTo(PPLAY.cx - 3.5, PPLAY.cy + 6 + oy); ctx.closePath(); ctx.fill(); }
    const d = PCARD.duration; ctx.fillStyle = BGC; ctx.fillRect(d.x - 4, d.y - 3 + oy, d.w + 8, d.h + 6); ctx.fillStyle = '#5b5361'; ctx.font = `400 11px ${M}`; ctx.letterSpacing = '0px';
    const el = pl.on ? Math.round(pl.p * 34) : 34, lab = pl.on ? `0:${String(el).padStart(2, '0')}` : '0:34'; ctx.fillText(lab, d.x + d.w - ctx.measureText(lab).width, d.y + 11.5 + oy);
  }
  const ha = clamp((scroll - 70) / 110); // compact blue header once the hero scrolls away, as in the app
  if (ha > 0) { ctx.save(); ctx.globalAlpha = ha; ctx.drawImage(HDR, 0, 0, 390, 126); ctx.restore(); }
  ctx.drawImage(COMP, 0, 744, 390, 100); // pinned composer
  ctx = prev; return PSC;
}
// the demo name in the home pill is swapped for the film's person (same pill, same fill)
const ovPill = () => {
  const mx = (x) => (x - 4) * 390 / 385, my = (y) => y - 4;
  ctx.fillStyle = PILLC; ctx.fillRect(mx(156), my(493), 112 * 390 / 385, 42);
  ctx.fillStyle = '#16121c'; ctx.font = `500 14px ${F}`; ctx.letterSpacing = '-0.2px'; ctx.fillText('Jordan Lee', mx(158.5), my(510));
  ctx.fillStyle = '#5b5361'; ctx.font = `400 12px ${F}`; ctx.letterSpacing = '-0.1px'; ctx.fillText('Founder @ [Startup]', mx(158.5), my(526));
};

""" + s[b:]

# ---- overlays for the new add / ask layouts
rep("const BOX = '#fbfaf9',", "const BOX = '#fdfcfc',")
rep("const font = `400 14px ${F}`; ctx.font = font; ctx.letterSpacing = '-0.1px';", "const font = `400 14.5px ${F}`; ctx.font = font; ctx.letterSpacing = '-0.1px';")
rep("ctx.fillRect(24, 636, 348, 86); bars(t, 54, 231, 749); if (nw > 0) liveText(NOTE.slice(0, Math.max(1, Math.floor(nw))).join(' '), 31, 656, 336, 19, nw < NOTE.length, false, t); };",
    "ctx.fillRect(22, 662, 346, 88); bars(t, 55, 230, 782.5); if (nw > 0) liveText(NOTE.slice(0, Math.max(1, Math.floor(nw))).join(' '), 29.5, 685, 332, 18.5, nw < NOTE.length, false, t); };")

# ---- reveal
rep("const layers = t < tView + 0.04 ? stack(t, [[5.0, FG.mm_a], [6.25, FG.mm_b]], 0.55) : [{ im: FG.mm_b }, { cv: profileScreen(0, null), ty: lerp(844, 170, sheet), scrim: 0.3 * sheet }];",
    "const layers = t < tView + 0.04 ? stack(t, [[5.0, FG.home_out], [6.25, FG.home_tap, ovPill]], 0.55) : [{ im: FG.home_tap, ov: ovPill }, { cv: profileScreen(0, null), ty: lerp(844, 170, sheet), scrim: 0.3 * sheet }];")
rep("phone3(layers, 1360, 560, 930, { t, island: true,", "phone3(layers, 1360, 560, 930, { t, sb: 0, island: true,")
rep("taps: [[6.05, 0.324, 0.317], [tView, 0.52, 0.255]] });", "taps: [[6.05, 0.5, 0.5], [tView, 0.745, 0.6]] });")

# ---- capture
rep("phone3(layers, 470, 560, 920, { t, island: true,", "phone3(layers, 470, 560, 920, { t, sb: 0, island: true,")
rep("taps: [[tStop, 0.742, 0.886]] });", "taps: [[tStop, 0.75, 0.927]] });")

# ---- moments
rep("const layers = [{ im: FG.mm_b }, { cv: profileScreen(scroll, pl), ty, scrim: 0.3 * (1 - grow) * slide }];", "const layers = [{ im: FG.home_tap, ov: ovPill }, { cv: profileScreen(scroll, pl), ty, scrim: 0.3 * (1 - grow) * slide }];")
rep("phone3(layers, 600, 560, 920, { t, island: true,", "phone3(layers, 600, 560, 920, { t, sb: clamp((70 - ty) / 40), island: true,")
rep("taps: [[tPlay, 46 / 390, (1227 - PMAX) / 844]] });", "taps: [[tPlay, PPLAY.cx / 390, (PPLAY.cy - PMAX) / 844]] });")

# ---- ask: suggestion sheet + the keyboard component + the query box, typed live; then the dev build thinks and answers
a = s.index("// iOS keyboard key rectangles measured from the Figma frame")
b = s.index("// ---------- talking:")
s = s[:a] + """// Figma keyboard component (assets/figma/v14/keyboard.png): key rects come from keyboard.json
function keyPop(ch, upper, ktop) { // the pressed key darkens and its magnified letter bubble rises above it, like iOS
  const k = KBJ.keys[ch === ' ' ? 'space' : ch.toLowerCase()]; if (!k) return; const y = ktop + k.y;
  ctx.save(); ctx.fillStyle = 'rgba(150,152,172,0.5)'; ctx.beginPath(); ctx.roundRect(k.x, y, k.w, k.h, 8); ctx.fill();
  if (ch !== ' ') { ctx.shadowColor = 'rgba(10,6,20,0.25)'; ctx.shadowBlur = 8; ctx.shadowOffsetY = 3; ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.roundRect(k.x - 8, y - 56, k.w + 16, 60, 12); ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.fillStyle = '#16121c'; ctx.font = `400 30px ${F}`; ctx.letterSpacing = '0px'; const g = upper ? ch.toUpperCase() : ch; ctx.fillText(g, k.x + k.w / 2 - ctx.measureText(g).width / 2, y - 14); }
  ctx.restore();
}
const ASC = mk(390, 844);
function askScreen(kbp, str, t, caret, pop) { // suggestion sheet; tap the bar -> keyboard rises with the query box above it; text typed live
  const prev = ctx; ctx = ASC.getContext('2d');
  ctx.clearRect(0, 0, 390, 844); ctx.drawImage(FG.find_suggest, 0, 0, 390, 844);
  const ktop = lerp(844, 512, ease(kbp));
  if (kbp > 0.001) {
    const by = ktop - 8 - 93;
    ctx.drawImage(FG.find_query, 32, 1498, 716, 186, 16, by, 358, 93); // the query box component, its sample text blanked next
    ctx.fillStyle = BOX; ctx.fillRect(22, by + 7, 296, 32);
    ctx.font = `400 15px ${F}`; ctx.letterSpacing = '-0.1px'; const fs = 15 * 317 / ctx.measureText('I want to find someone to go climbing with me').width; ctx.font = `400 ${fs.toFixed(2)}px ${F}`;
    ctx.fillStyle = TXT; ctx.fillText(str, 29.5, by + 27); const tw = ctx.measureText(str).width;
    if (caret && Math.floor(t * 2.4) % 2 === 0) { ctx.fillStyle = INK; ctx.fillRect(29.5 + tw + 1.5, by + 13, 1.4, 17); }
    ctx.drawImage(KB, 0, ktop, 390, 332);
    if (pop) keyPop(pop.ch, pop.upper, ktop);
  }
  ctx = prev; return ASC;
}

""" + s[b:]
a = s.index("function ask(t) {")
b = s.index("function end(t) {")
body = s[a:b]
# replace ovType + layers + phone3 inside ask
i0 = body.index("  const ovType = () => {")
i1 = body.index("  calloutAt('Why Jordan'")
body = body[:i0] + """  const kbp = clamp((t - 22.72) / 0.4), pe = t - (tType + (nq - 1) * dt), pop = nq > 0 && nq < QS.length && pe < 0.11 ? { ch: QS[nq - 1], upper: nq === 1 } : null;
  const r = rig(t, 22.1, 29.5);
  const fr = SEQ[clamp(Math.floor((t - tSend) * 12), 0, SEQ.length - 1)], scr = { cv: askScreen(kbp, QS.slice(0, nq), t, t < tSend, pop), ty: 0 };
  const layers = t < tSend ? [scr] : [scr, { im: fr, a: ease((t - tSend) / 0.2) }];
  phone3(layers, 1010, 560, 920, { t, sb: 0, island: true, dy: r.dy, ry: lerp(26, 0, sp(t - 22.1, 80, 15)), rx: lerp(-6, 0, sp(t - 22.1, 60, 14)), rot: lerp(3, 0, sp(t - 22.1, 90, 16)), taps: [[22.55, 0.5, 0.93], [tSend, 0.915, 0.925]] });
""" + body[i1:]
body = body.replace("tType = 23.0,", "tType = 23.1,")
s = s[:a] + body + s[b:]

# ---- end: the updated mind map, dark status bar
rep("phone3([{ im: FG.home_map }], 1560, 700 + (1 - r) * 1150, 960, { t, island: true,", "phone3([{ im: FG.home_in }], 1560, 700 + (1 - r) * 1150, 960, { t, sb: 0, island: true,")
open(p, 'w', encoding='utf8').write(s)
print('ok')
