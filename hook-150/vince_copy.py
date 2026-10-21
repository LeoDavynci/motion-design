# python3 hook-150/vince_copy.py problem|story < vince.html > copy.html
# Makes the temporary copies of Vince's film that make_cut.sh renders shots from. His files are never changed: the
# copy is written next to his index.html (so its assets and lib/ resolve) and deleted after the render. Each edit is
# checked, so a change in his film stops the cut instead of rendering something else.
#   problem: his first version (commit 964dee0), only "Meeting people is easy / Remembering them is hard", on its night
#            background; the text and cards stay 0.35s longer after the "hard." highlight (exit 5.05s, not 4.7s).
#   story:   v17, only "Every person. Every story." and "Remember the connection. Not just their name.":
#            the headline comes in before the cards (it came after), the night background is already there (no curtain
#            wipe in; the cut crossfades into it), the page-turn wipe between the two becomes a crossfade, and the
#            "Remember the connection" beat holds instead of leaving (the cut ends on it).
import sys

mode, s = sys.argv[1], sys.stdin.read()


def rep(a, b, n=1):
    global s
    if s.count(a) != n:
        sys.exit(f'vince_copy.py {mode}: expected {n} of {a!r}, found {s.count(a)}')
    s = s.replace(a, b)


if mode == 'problem':
    lines = s.split('\n')
    s = '\n'.join('const SHOTS = [[2.8, 5.35, problem]];' if l.startswith('const SHOTS = ') else l for l in lines)
    rep("[4.6, 'dA', 'diag'], ", '')
    rep("t, 3.8, 4.7, { mode: 'zoom'", "t, 3.8, 5.05, { mode: 'zoom'")
    rep("t, 3.95, 4.7, { mode: 'zoom'", "t, 3.95, 5.05, { mode: 'zoom'")
    rep('(t - 4.7 - i * 0.06)', '(t - 5.05 - i * 0.06)')
elif mode == 'story':
    # A background that crossfades in (his others wipe in with a clip)
    rep("    if (p >= 1) { paint(key, t); continue; }\n",
        "    if (p >= 1) { paint(key, t); continue; }\n"
        "    if (style === 'fade') { ctx.save(); ctx.globalAlpha = ease(p); paint(key, t); ctx.restore(); continue; }\n")
    rep("[BGT.field - 0.4, 'nW', 'curtain']", "[BGT.field - 1.6, 'nW', 'fade']")
    rep("[BGT.moments - 0.9, 'nB', 'diagR']", "[BGT.moments - 0.9, 'nB', 'fade']")
    # Text first, then the cards
    rep("const t0 = 14.1 + i * 0.1, e = sp(t - t0, 95, 12.5);", "const t0 = 14.95 + i * 0.1, e = sp(t - t0, 95, 12.5);")
    rep("t, 15.6, 16.5, { mode: 'drift', gap: 0.11 });", "t, 14.15, 15.6, { mode: 'drift', gap: 0.11 });")
    rep("t, 16.5, 18.6, { mode: 'arc', gap: 0.11, hlDelay: 0.3 });", "t, 15.6, 18.6, { mode: 'arc', gap: 0.11, hlDelay: 0.3 });")
    # Hold "Remember the connection. Not just their name." to the end of the cut
    rep("TX = 18.1;", "TX = 99;")
    # Only these two shots
    rep("const TOTAL = SEG.reduce(", "SHOTS.splice(0, SHOTS.length, ...SHOTS.filter((x) => x[2] === field || x[2] === moments));\nconst TOTAL = SEG.reduce(")
    # Film time for a film-internal time, for make_cut.sh
    rep("window.seek = (T) => {", "window.filmTime = (t) => { let T0 = 0; for (const [u0, u1, d] of SEG) { if (t <= u1) return T0 + d * (t - u0) / (u1 - u0); T0 += d; } return T0; };\nwindow.BGT = BGT;\nwindow.seek = (T) => {")
else:
    sys.exit('usage: vince_copy.py problem|story')
sys.stdout.write(s)
