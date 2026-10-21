s = open('index.html', encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b, 1)


# oversized, cropped word drifting behind the phone (references: "SmartOps" / "STREAMLINE" behind devices)
rep("function sparkle(", """function ghost(str, t, t0, t1, y, dir = 1) {
  const a = ease((t - t0) / 0.6) * (1 - ease((t - t1) / 0.4)); if (a <= 0.003) return;
  ctx.save(); ctx.globalAlpha = a * (isDay(t) ? 0.06 : 0.07); ctx.fillStyle = isDay(t) ? INK : '#fff'; ctx.font = `600 560px ${F}`; ctx.letterSpacing = '-22px';
  const w = ctx.measureText(str).width; ctx.fillText(str, 960 - w / 2 + dir * (t - t0) * 46, y); ctx.restore();
}
function sparkle(""")
rep("  const r = rig(t, 5.55, 8.6), tView = 7.35", "  ghost('PEOPLE', t, 5.4, 8.6, 880, -1);\n  const r = rig(t, 5.55, 8.6), tView = 7.35")
rep("  const r = rig(t, 8.7, 14.0);", "  ghost('SPEAK', t, 8.8, 14.0, 880, 1);\n  const r = rig(t, 8.7, 14.0);")
rep("  const r = rig(t, 16.1, 22.4), tPlay", "  ghost('STORY', t, 16.3, 22.4, 880, -1);\n  const r = rig(t, 16.1, 22.4), tPlay")
rep("  const r = rig(t, 22.1, 26.5);", "  ghost('ASK', t, 22.5, 26.5, 880, 1);\n  const r = rig(t, 22.1, 26.5);")
open('index.html', 'w', encoding='utf-8').write(s)
print('ok')
