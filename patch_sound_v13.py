import re
s = open('sound.py', encoding='utf8').read()
# timeline parsed from lib/timeline.js (single source of truth)
hdr = '''import json
SPEC = json.loads(re.search(r"export const SPEC = (\[.*\]);", open('lib/timeline.js', encoding='utf8').read(), re.S).group(1))
SEG, SH, PH, BT = [], {}, {}, {}
_cur = 0.0
for name, a, b, ph, fph, segs in SPEC:
    sh = _cur - a; SH[name] = sh; PH[name] = ph; BT[name] = _cur
    if ph: SEG.append([_cur, _cur + ph, fph])
    for u0, u1, d in segs: SEG.append([u0 + sh + ph, u1 + sh + ph, d])
    _cur += ph + (b - a)
TOTAL = sum(x[2] for x in SEG)
'''
s = s.replace("import numpy as np, soundfile as sf", "import re\nimport numpy as np, soundfile as sf", 1)
s = s.replace("SR, DUR, BEAT = 44100, 50.0, 0.5", hdr + "SR, DUR, BEAT = 44100, float(int(TOTAL) + 2), 0.5", 1)
a = s.index("SEG = [[0, 1.2, 1.2]")
b = s.index("out = out[:int(SR * DUR)]")
new = '''def inv(u):
    T0 = 0.0
    for u0, u1, d in SEG:
        if u <= u1: return T0 + (u - u0) / (u1 - u0) * d
        T0 += d
    return T0
def X(sc, t): return inv(t + SH[sc])               # text-time cue
def Pp(sc, t): return inv(t + SH[sc] + PH[sc])     # phone-time cue
def at(T, x, g=1.0): put(T, x, g)
# hook
at(X('hook', 0.0), boom(), 0.9); at(X('hook', 0.0), swell(0.9, 700), 0.35)
for b in range(1, 3): at(X('hook', b * BEAT), thock(150 + b * 25), 0.4)
at(X('hook', 3.15), whoosh(1.0, 900), 0.5); at(X('hook', 3.3), swell(1.8, 800), 0.3)          # grid zooms out, number counts up
# scene cuts and colour wipes
for sc in ('problem', 'reveal', 'capture', 'field', 'moments', 'ask', 'end'):
    at(inv(BT[sc]) - 0.3, whoosh(0.5, 1000), 0.45); at(inv(BT[sc]), thock(130, 0.3), 0.55)
for sc, off in (('reveal', 0.4), ('capture', 0.5), ('field', 0.4), ('moments', 0.9), ('ask', 0.4), ('end', 0.4)): at(inv(BT[sc] - off), whoosh(0.8, 1300), 0.55)
# problem
for k, t in enumerate((4.4, 4.7, 5.0)): at(X('problem', t), thock(170 + k * 30), 0.5)
at(X('problem', 6.05), whoosh(0.4, 1100), 0.3)
# reveal
at(X('reveal', 5.0) - 0.6, swell(0.6, 1200), 0.5); at(X('reveal', 5.4), boom(), 0.8)
at(X('reveal', 5.0), pad((130.81, 196, 261.63, 329.63), 3.0, a=0.15, fc=900), 0.7)
at(Pp('reveal', 6.05), thock(240, 0.15), 0.45); at(Pp('reveal', 6.25), thock(200, 0.2), 0.35)
at(Pp('reveal', 7.35), thock(240, 0.15), 0.45); at(Pp('reveal', 7.45), swell(0.5, 1000), 0.25)
# capture
at(Pp('capture', 8.95), swell(0.5, 900), 0.2)
at(Pp('capture', 12.2), thock(240, 0.15), 0.45); at(Pp('capture', 12.2), bloom(392, 1.3), 0.3); at(Pp('capture', 12.25), swell(0.5, 1500), 0.18)
at(Pp('capture', 12.4), thock(210, 0.18), 0.3); at(Pp('capture', 13.2), thock(210, 0.18), 0.35); at(Pp('capture', 13.25), bloom(329.63, 1.4), 0.25)
# field: cards fly in from the edges
for i in range(11): at(X('field', 14.1 + i * 0.1), whoosh(0.35, 1100), 0.16); at(X('field', 14.38 + i * 0.1), thock(170 + i * 10, 0.18), 0.22)
at(X('field', 16.5), bloom(392, 1.2), 0.22)
# moments
at(X('moments', 16.2), swell(0.6, 1000), 0.3); at(Pp('moments', 16.9), thock(170, 0.25), 0.4)
at(Pp('moments', 18.6), swell(1.6, 900), 0.22)
at(Pp('moments', 20.6), thock(240, 0.15), 0.45); at(Pp('moments', 20.7), bloom(392, 1.4), 0.25)
# ask
at(Pp('ask', 22.7), thock(240, 0.15), 0.45); at(Pp('ask', 22.9), thock(200, 0.2), 0.3)
for i in range(0, 45, 2): at(Pp('ask', 23.0 + i * 0.031), thock(300 + (i % 3) * 20, 0.05), 0.06)
at(Pp('ask', 24.5), thock(240, 0.15), 0.45); at(Pp('ask', 24.6), swell(0.8, 900), 0.28)
for k in range(3): at(Pp('ask', 25.2 + k * 0.9), thock(220, 0.1), 0.12)                       # thinking steps
at(Pp('ask', 27.8), thock(180, 0.25), 0.5); at(Pp('ask', 27.85), bloom(329.63, 1.2), 0.22)    # results settle
# end
at(X('end', 26.5), boom(), 0.9); at(X('end', 26.5), pad((130.81, 196, 261.63, 329.63), 3.8, a=0.3, fc=1000), 0.75); at(X('end', 26.5), sub(65.41, 3.4), 0.5)
at(X('end', 26.9), swell(0.8, 1300), 0.3); at(X('end', 28.6), thock(240, 0.15), 0.4)
for k, t in enumerate((28.6, 29.0, 29.4)): at(X('end', t), thock(160 + k * 28, 0.22), 0.45)
at(X('end', 29.8), bloom(392, 1.2), 0.22)
print('film length', round(TOTAL, 2))
'''
s = s[:a] + new + s[b:]
open('sound.py', 'w', encoding='utf8').write(s)
