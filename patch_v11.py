import re
s = open('index.html', encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert a in s, a[:90]
    s = s.replace(a, b, n)


# ---- single clean avatar (cover the original exactly)
rep("patchFrame('match1', [[73, 329, 74, 1], [73, 550, 62, 6]]); patchFrame('match2', [[73, 329, 74, 1], [73, 597, 62, 6]]); patchFrame('match3', [[73, 329, 74, 1], [73, 597, 62, 6]]);",
    "patchFrame('match1', [[67, 329, 63, 1], [73, 549.5, 63, 6]]); patchFrame('match2', [[67, 329, 63, 1], [73, 597, 63, 6]]); patchFrame('match3', [[67, 329, 63, 1], [73, 597, 63, 6]]);")
rep("patchFrame('add_preview', [[60, 479, 64, 1]]);", "patchFrame('add_preview', [[67, 480, 63, 1]]);")

# ---- calloutAt: configurable card x
rep("function calloutAt(label, body, t, t0, t1, y, h, tgt) {", "function calloutAt(label, body, t, t0, t1, y, h, tgt, bx = 1500) {")
rep("  const cx = 1500 + (1 - e) * 460 + x * 600, cy = y + (1 - e) * 40;\n  card(cx, cy, 380, h, { dark: true, r: 26 });\n  ctx.fillStyle = LIME; ctx.font = `500 18px ${M}`; ctx.letterSpacing = '2.4px'; ctx.fillText(label.toUpperCase(), cx + 28, cy + 42);\n  ctx.fillStyle = '#fff'; ctx.font = `300 26px ${F}`; ctx.letterSpacing = '-0.4px';\n  wrap(body, 320, `300 26px ${F}`).forEach((l, i) => ctx.fillText(l, cx + 28, cy + 88 + i * 34));\n  const lp",
    "  const cx = bx + (1 - e) * 460 + x * 600, cy = y + (1 - e) * 40;\n  card(cx, cy, 380, h, { dark: true, r: 26 });\n  ctx.fillStyle = LIME; ctx.font = `500 18px ${M}`; ctx.letterSpacing = '2.4px'; ctx.fillText(label.toUpperCase(), cx + 28, cy + 42);\n  ctx.fillStyle = '#fff'; ctx.font = `300 26px ${F}`; ctx.letterSpacing = '-0.4px';\n  wrap(body, 320, `300 26px ${F}`).forEach((l, i) => ctx.fillText(l, cx + 28, cy + 88 + i * 34));\n  const lp")

# ---- capture: phone on the left, words + voice card on the right
a = s.index("function capture(t) {"); b = s.index("const FIELD = [")
c = s[a:b]
c = c.replace("eyebrow('01 · Capture', 96, 230", "eyebrow('01 · Capture', 1000, 230")
c = c.replace("words(['Talk for'], 96, 400", "words(['Talk for'], 1000, 400").replace("words([['20 seconds.', { hl: true }]], 96, 540", "words([['20 seconds.', { hl: true }]], 1000, 540")
c = c.replace("voiceCard(t, 96 - cx * 900,", "voiceCard(t, 1000 + cx * 900,")
c = c.replace("timer(t, 1040, 800, 84,", "timer(t, 850, 820, 84,")
c = c.replace("phone3(layers, 1500, 560, 920, { t, island: true, dy: r.dy, ry: lerp(34, 10, sp(t - 8.7, 80, 15)) + Math.sin(t) * 2, rx: lerp(-6, 0, sp(t - 8.7, 60, 14)), rot: lerp(-4, 0, sp(t - 8.7, 90, 16)),",
              "phone3(layers, 470, 560, 920, { t, island: true, dy: r.dy, ry: lerp(-34, -10, sp(t - 8.7, 80, 15)) + Math.sin(t) * 2, rx: lerp(-6, 0, sp(t - 8.7, 60, 14)), rot: lerp(4, 0, sp(t - 8.7, 90, 16)),")
assert "470, 560" in c and "1000 + cx" in c
s = s[:a] + c + s[b:]

# ---- moments: phone on the left, headline on the right, callouts under it
a = s.index("function moments(t) {"); b = s.index("function ask(t) {")
c = s[a:b]
for old, new in [("eyebrow('02 · The story', 96, 230", "eyebrow('02 · The story', 1010, 230"),
                 ("words(['It keeps the'], 96, 400, 120", "words(['It keeps the'], 1010, 380, 108"),
                 ("words([['story,', { hl: true }]], 96, 520, 120", "words([['story,', { hl: true }]], 1010, 495, 108"),
                 ("words(['not just the title.'], 96, 640, 120", "words(['not just the title.'], 1010, 610, 108"),
                 ("words(['Play it ', ['back.', { hl: true }]], 96, 400, 130", "words(['Play it ', ['back.', { hl: true }]], 1010, 400, 120"),
                 ("words(['Every moment keeps'], 96, 540, 60", "words(['Every moment keeps'], 1010, 520, 56"),
                 ("words(['your voice and its words.'], 96, 614, 60", "words(['your voice and its words.'], 1010, 592, 56"),
                 ("phone3(layers, 1180, 560, 920,", "phone3(layers, 600, 560, 920,"),
                 ("ry: lerp(-24, 0, sp(t - 16.1, 80, 15)), rot: lerp(-3, 0, sp(t - 16.1, 90, 16))", "ry: lerp(24, 0, sp(t - 16.1, 80, 15)), rot: lerp(3, 0, sp(t - 16.1, 90, 16))"),
                 ("scrPt(1180, py, PS, pc, 300, 340 - scroll));", "scrPt(600, py, PS, pc, 300, 340 - scroll), 1010);"),
                 ("scrPt(1180, py, PS, pc, 250, 1215 - scroll));", "scrPt(600, py, PS, pc, 250, 1215 - scroll), 1010);"),
                 ("t, 17.55, 18.0, 330, 200,", "t, 17.55, 18.0, 760, 200,"),
                 ("t, 20.0, 22.4, 660, 220,", "t, 20.0, 22.4, 740, 220,")]:
    assert old in c, old
    c = c.replace(old, new)
s = s[:a] + c + s[b:]

# ---- ask: phone in the middle, callouts on the right
a = s.index("function ask(t) {"); b = s.index("function end(t) {")
c = s[a:b]
for old, new in [("phone3(layers, 1180, 560, 920,", "phone3(layers, 1010, 560, 920,"),
                 ("scrPt(1180, ay, 920, 1, 215, 322));", "scrPt(1010, ay, 920, 1, 215, 322), 1430);"),
                 ("scrPt(1180, ay, 920, 1, 300, 482));", "scrPt(1010, ay, 920, 1, 300, 482), 1430);")]:
    assert old in c, old
    c = c.replace(old, new)
s = s[:a] + c + s[b:]

# ---- 60 s: film time -> internal time. Slow reading holds are inserted where text has just landed; everything else keeps its pace.
rep("window.seek = (t) => {", """const SEG = [ // [internal start, internal end, film seconds]
  [0, 1.2, 1.4], [1.2, 1.45, 1.8], [1.45, 2.8, 2.6], [2.8, 3.6, 1.2], [3.6, 3.75, 1.2], [3.75, 4.45, 1.0], [4.45, 4.65, 1.5], [4.65, 5.0, 0.5],
  [5.0, 5.9, 1.1], [5.9, 6.5, 1.0], [6.5, 6.9, 1.6], [6.9, 7.4, 0.8], [7.4, 8.1, 1.1], [8.1, 8.3, 1.6], [8.3, 8.6, 0.4],
  [8.6, 9.5, 1.1], [9.5, 12.2, 3.6], [12.2, 12.95, 0.9], [12.95, 13.15, 2.0], [13.15, 14.0, 1.0],
  [14.0, 15.0, 1.4], [15.0, 15.25, 1.2], [15.25, 15.9, 1.0], [15.9, 16.0, 1.4], [16.0, 16.1, 0.2],
  [16.1, 17.5, 1.7], [17.5, 17.9, 0.6], [17.9, 18.0, 1.6], [18.0, 19.3, 1.6], [19.3, 19.65, 0.5], [19.65, 20.6, 1.4], [20.6, 20.8, 1.6], [20.8, 22.0, 1.6],
  [22.0, 22.9, 1.0], [22.9, 24.4, 2.4], [24.4, 24.95, 0.8], [24.95, 25.2, 1.8], [25.2, 25.7, 0.9], [25.7, 26.0, 2.0], [26.0, 26.5, 0.6],
  [26.5, 27.4, 1.2], [27.4, 28.0, 0.8], [28.0, 29.2, 2.0], [29.2, 30.0, 3.3]];
function warp(T) { let T0 = 0; for (const [u0, u1, d] of SEG) { if (T <= T0 + d) return u0 + (u1 - u0) * (T - T0) / d; T0 += d; } return 30; }
window.seek = (T) => {
  const t = warp(T);""")
open('index.html', 'w', encoding='utf-8').write(s)

# ---- sound: same warp, 60 s bed
snd = open('sound.py', encoding='utf-8').read()
snd = snd.replace("SR, DUR, BEAT = 44100, 30.0, 0.5", "SR, DUR, BEAT = 44100, 60.0, 0.5")
seg = re.search(r"const SEG = \[(.*?)\];", s, re.S).group(1)
segpy = "SEG = [" + seg.replace("\n", " ") + "]\n"
helper = segpy + """def inv(u):
    T0 = 0.0
    for u0, u1, d in SEG:
        if u <= u1: return T0 + (u - u0) / (u1 - u0) * d
        T0 += d
    return T0
def putw(t, x, g=1.0): put(inv(t), x, g)
"""
i = snd.index("# cues")
head, tail = snd[:i], snd[i:]
tail = tail.replace("put(", "putw(")
tail = tail.replace("out = out[:int(SR * DUR)]", "out = out[:int(SR * DUR)]")
open('sound.py', 'w', encoding='utf-8').write(head + helper + tail)

r = open('render.mjs', encoding='utf-8').read()
r = r.replace("const FPS = arg('fps', 60), DUR = arg('dur', 15), SUB = arg('sub', 4);", "const FPS = arg('fps', 60), DUR = arg('dur', 15), SUB = arg('sub', 4), FROM = arg('from', 0), TO = arg('to', DUR), PART = arg('part', -1);\nconst OUT = PART >= 0 ? `out/part_${PART}.mp4` : 'out/silent.mp4';")
r = r.replace("'out/silent.mp4'],", "OUT],")
r = r.replace("const total = Math.round(DUR * FPS * SUB);\nfor (let i = 0; i < total; i++) {", "const total = Math.round(TO * FPS * SUB);\nfor (let i = Math.round(FROM * FPS * SUB); i < total; i++) {")
open('render.mjs', 'w', encoding='utf-8').write(r)
print('ok')
