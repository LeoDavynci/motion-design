import re
s = open('index.html', encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:100]
    s = s.replace(a, b, 1)


# 1. Introducing gets room above the wordmark
rep("words(['Introducing'], 96, 262, 64,", "words(['Introducing'], 96, 190, 60,")

# 2. callouts without a leader when the target is null
rep("  const lp = ease((t - t0 - 0.15) / 0.4); if (lp <= 0) return;", "  const lp = tgt ? ease((t - t0 - 0.15) / 0.4) : 0; if (lp <= 0) return;")
rep("scrPt(600, py, PS, pc, 300, 340 - scroll), 1010);", "null, 1010);")
rep("scrPt(600, py, PS, pc, 250, 1215 - scroll), 1010);", "null, 1010);")

# 3. one thumb at a time: short glide in, short lift out
rep("const u = t - t0; if (u < -0.9 || u > 0.9) continue;", "const u = t - t0; if (u < -0.45 || u > 0.5) continue;")
rep("m = ease((u + 0.9) / 0.9), fade = u < 0.45 ? 1 : 1 - clamp((u - 0.45) / 0.45);", "m = ease((u + 0.45) / 0.45), fade = u < 0.2 ? 1 : 1 - clamp((u - 0.2) / 0.3);")
rep("const ring2 = ease(u / 0.8);", "const ring2 = ease(u / 0.5);")
rep("Math.sin((u + 0.9) * 7)", "Math.sin((u + 0.45) * 9)")

# 4. status bar content removed (the space and the island stay)
rep("  PROF = await load('assets/figma/audio_ready_v2.png');",
    """  PROF = await load('assets/figma/audio_ready_v2.png');
  const clean = (im) => { const c = mk(im.width, im.height), g = c.getContext('2d'); g.drawImage(im, 0, 0);
    for (const [x0, x1] of [[26, 112], [266, im.width - 24]]) { g.save(); g.beginPath(); g.rect(x0, 12, x1 - x0, 44); g.clip(); g.filter = 'blur(3px)'; g.drawImage(im, x0 - 6, 10, x1 - x0 + 12, 2, x0 - 6, 6, x1 - x0 + 12, 56); g.restore(); }
    return c; };
  for (const k of Object.keys(FG)) if (FG[k]) FG[k] = clean(FG[k]);
  PROF = clean(PROF);""")

# 5/6. end: Figma map without initials, one colour for the tagline
rep("phone3([{ im: FG.map_in }], 1560,", "phone3([{ im: FG.mm_a }], 1560,")
rep("words([['Capture.', { c: LIME }]], 96, 640, 96,", "words(['Capture.'], 96, 640, 96,")
rep("words([['Ask.', { c: LIME }]], 96 + textWidth('Capture. ', 96, 400), 640, 96,", "words(['Ask.'], 96 + textWidth('Capture. ', 96, 400), 640, 96,")

# 7. screen(): slide offset, clipped region, dim for the page underneath
rep("    ctx.save(); ctx.globalAlpha *= aL; if (L.sc) ctx.scale(L.sc, L.sc);",
    "    ctx.save(); if (L.clipY0) { ctx.beginPath(); ctx.rect(-sw / 2, -sh / 2 + L.clipY0 * sh / 844, sw, sh); ctx.clip(); } ctx.translate(0, (L.oy || 0) * sh); ctx.globalAlpha *= aL; if (L.sc) ctx.scale(L.sc, L.sc);")
rep("L.ov(); ctx.restore(); }\n    ctx.restore();\n  }", "L.ov(); ctx.restore(); }\n    ctx.restore();\n    if (L.dim) { ctx.fillStyle = `rgba(14,10,22,${L.dim})`; ctx.fillRect(-sw / 2, -sh / 2, sw, sh); }\n  }")
rep("function stack(t, list, tr = 0.5) {", """function stack2(t, list, tr = 0.55) { // [[t, image, overlay, mode]]: 'up' = next page slides up over this one, 'part' = only the lower part changes, default = soft dissolve
  let i = 0; for (let j = 0; j < list.length; j++) if (t >= list[j][0]) i = j;
  const e = list[i], p = i > 0 ? ease((t - e[0]) / tr) : 1, L = [], mode = e[3] || 'fade';
  if (i > 0 && p < 1) { const o = list[i - 1]; L.push(mode === 'up' ? { im: o[1], ov: o[2], oy: -0.06 * p, dim: 0.3 * p } : { im: o[1], ov: o[2] }); }
  if (i > 0 && p < 1 && mode === 'up') L.push({ im: e[1], ov: e[2], oy: 1 - p });
  else if (i > 0 && p < 1 && mode === 'part') L.push({ im: e[1], ov: e[2], oy: (1 - p) * 0.07, clipY0: 440 });
  else L.push({ im: e[1], ov: e[2], a: p, sc: 1 + 0.045 * (1 - p), blur: (1 - p) * 9 });
  return L;
}
function stack(t, list, tr = 0.5) {""")

# 8. capture: one screen builds the profile card (skeleton, then the real card), no crossfade between two screens
rep("  const layers = stack(t, [[8.6, FG.add_voice], [8.85, FG.add_voice_live, ovTalk], [12.4, FG.add_processing], [13.0, FG.add_preview]], 0.5);",
    """  const ovCard = () => { // the card builds in place: a shimmering skeleton, then the finished card settles over it
    const sk = clamp((t - 12.9) / 0.3), rev = ease((t - 13.15) / 0.45); if (sk <= 0) return;
    const X = 25, Y = 427, Wc = 340, Hc = 106, sh_ = ((t * 1.1) % 1) * (Wc + 160) - 80;
    ctx.save(); ctx.globalAlpha = sk * (1 - rev);
    ctx.fillStyle = 'rgba(40,34,80,0.10)'; rr(X, Y, Wc, Hc, 20); ctx.fill();
    ctx.save(); rr(X, Y, Wc, Hc, 20); ctx.clip(); const g = ctx.createLinearGradient(X + sh_ - 70, 0, X + sh_ + 70, 0); g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(0.5, 'rgba(255,255,255,0.55)'); g.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = g; ctx.fillRect(X, Y, Wc, Hc); ctx.restore();
    ctx.fillStyle = 'rgba(40,34,80,0.14)'; ctx.beginPath(); ctx.arc(67, 480, 30, 0, 7); ctx.fill(); rr(112, 460, 120, 12, 6); ctx.fill(); rr(112, 484, 170, 9, 4.5); ctx.fill(); rr(112, 502, 90, 9, 4.5); ctx.fill();
    ctx.restore();
    if (rev > 0) { const k = 0.97 + 0.03 * rev; ctx.save(); ctx.globalAlpha = rev; ctx.translate(X + Wc / 2, Y + Hc / 2 + (1 - rev) * 10); ctx.scale(k, k); ctx.beginPath(); ctx.roundRect(-Wc / 2, -Hc / 2, Wc, Hc, 20); ctx.clip(); ctx.drawImage(FG.add_preview, X + 4, Y + 4, Wc - 8, Hc - 8, -Wc / 2 + 4, -Hc / 2 + 4, Wc - 8, Hc - 8); ctx.restore(); }
  };
  const layers = stack2(t, [[8.6, FG.add_voice], [8.85, FG.add_voice_live, ovTalk], [12.4, FG.add_processing, ovCard, 'up']], 0.55);""")

# 9. ask: pages slide, nothing dissolves over text
rep("  const layers = stack(t, [[22.4, FG.find_suggest], [22.9, FG.find_query, ovType], [24.7, FG.match1], [25.5, FG.match2]], 0.5);",
    "  const layers = stack2(t, [[22.4, FG.find_suggest], [22.9, FG.find_query, ovType], [24.7, FG.match1, null, 'up'], [25.5, FG.match2, null, 'part']], 0.55);")

# 10. 50 s timing
a = s.index("const SEG = ["); b = s.index("function warp(T)")
new_seg = """const SEG = [ // [internal start, internal end, film seconds]
  [0, 1.2, 1.2], [1.2, 1.45, 1.4], [1.45, 2.8, 2.2], [2.8, 3.6, 1.0], [3.6, 3.75, 1.0], [3.75, 4.45, 0.9], [4.45, 4.65, 1.2], [4.65, 5.0, 0.4],
  [5.0, 5.9, 1.0], [5.9, 6.5, 0.8], [6.5, 6.9, 1.3], [6.9, 7.4, 0.7], [7.4, 8.1, 1.0], [8.1, 8.3, 1.3], [8.3, 8.6, 0.4],
  [8.6, 9.5, 1.0], [9.5, 12.2, 3.0], [12.2, 12.9, 0.7], [12.9, 13.15, 1.4], [13.15, 13.6, 0.6], [13.6, 14.0, 0.8],
  [14.0, 15.0, 1.2], [15.0, 15.25, 1.0], [15.25, 15.9, 0.8], [15.9, 16.0, 1.2], [16.0, 16.1, 0.2],
  [16.1, 17.5, 1.5], [17.5, 17.9, 0.5], [17.9, 18.0, 1.4], [18.0, 19.3, 1.3], [19.3, 19.65, 0.4], [19.65, 20.6, 1.2], [20.6, 20.8, 1.4], [20.8, 22.0, 1.3],
  [22.0, 22.9, 0.9], [22.9, 24.4, 2.0], [24.4, 24.95, 0.7], [24.95, 25.2, 1.6], [25.2, 25.7, 0.8], [25.7, 26.0, 1.7], [26.0, 26.5, 0.5],
  [26.5, 27.4, 1.0], [27.4, 28.0, 0.7], [28.0, 29.2, 1.7], [29.2, 30.0, 1.7]];
"""
s = s[:a] + new_seg + s[b:]
open('index.html', 'w', encoding='utf-8').write(s)

snd = open('sound.py', encoding='utf-8').read()
snd = snd.replace("SR, DUR, BEAT = 44100, 60.0, 0.5", "SR, DUR, BEAT = 44100, 50.0, 0.5")
seg = re.search(r"const SEG = \[[^\n]*\n(.*?)\];", s, re.S).group(1)
snd = re.sub(r"SEG = \[.*?\]\]\n", "SEG = [" + seg.replace("\n", " ").strip() + "]\n", snd, count=1, flags=re.S)
snd = snd.replace("putw(13.0, thock(210, 0.18), 0.35); putw(13.0, bloom(329.63, 1.4), 0.25)", "putw(13.2, thock(210, 0.18), 0.35); putw(13.25, bloom(329.63, 1.4), 0.25)")
open('sound.py', 'w', encoding='utf-8').write(snd)
print('ok')
