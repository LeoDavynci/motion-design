# python3 hook-150/vince_copy.py problem|story|ask|end|bg < vince.html > copy.html
# Makes the temporary copies of Vince's film that make_cut.sh renders shots from. His files are never changed: the
# copy is written next to his index.html (so its assets and lib/ resolve) and deleted after the render. Each edit is
# checked, so a change in his film stops the cut instead of rendering something else.
#   problem: his first version (commit 964dee0), only "Meeting people is easy / Remembering them is hard", on its night
#            background; each line fully finishes, then holds ~0.45s before moving on (user's call): "Meeting people is
#            easy." until 4.35s (was 3.8s, before it had even settled), "Remembering them is hard." and the cards from
#            4.35s / 4.5s until 6.0s (were 3.8s / 3.95s until 4.7s).
#   story:   v17, only "Every person. Every story." and "Remember the connection. Not just their name.":
#            the headline comes in before the cards (it came after), the night background is already there (no curtain
#            wipe in; the cut crossfades into it), the page-turn wipe between the two becomes a crossfade, and the
#            "Remember the connection" beat holds a little longer, then fades out with his usual text exit, and his phone
#            after it is switched off (the cut crossfades to the next part on the empty background). "Every story." fades out with
#            the cards (his shot stopped drawing it the moment the cards were gone, so it vanished).
#   ask:     v17, only "Ask your own notes." and its three prompt pills: the pills come in only once the headline (and its
#            highlight) is complete, everything holds a beat, then fades out; his phone after it is switched off. His
#            night background is already there (the cut crossfades into it).
#   end:     v17, only the last scene ("Peepl. Capture. Search. Reconnect." and the phone): the phone shows the updated
#            mindmap (our intro's phone screen, assets/end/home_jl.png: the new discs and controls, "JL" for Jordan Lee;
#            his showed an older screen with "MC"), and his night background is already there (the cut crossfades into it).
#   bg:      v17 with no shots at all: just his backgrounds (to draw the last scene's night background into a still).
#   story, ask, end: a highlighted word's text turns from white to ink smoothly as the lime box sweeps under it (it
#            switched at once, which looked rough).
import sys

mode, s = sys.argv[1], sys.stdin.read()


def rep(a, b, n=1):
    global s
    if s.count(a) != n:
        sys.exit(f'vince_copy.py {mode}: expected {n} of {a!r}, found {s.count(a)}')
    s = s.replace(a, b)


if mode == 'problem':
    lines = s.split('\n')
    s = '\n'.join('const SHOTS = [[2.8, 6.0, problem]];' if l.startswith('const SHOTS = ') else l for l in lines)
    rep("[4.6, 'dA', 'diag'], ", '')
    rep("t, 2.8, 3.8, { mode: 'swing'", "t, 2.8, 4.35, { mode: 'swing'")
    rep("t, 2.95, 3.8, { mode: 'swing'", "t, 2.95, 4.35, { mode: 'swing'")
    rep("t, 3.8, 4.7, { mode: 'zoom'", "t, 4.35, 6.0, { mode: 'zoom'")
    rep("t, 3.95, 4.7, { mode: 'zoom'", "t, 4.5, 6.0, { mode: 'zoom'")
    rep('(t - 4.7 - i * 0.06)', '(t - 6.0 - i * 0.06)')
elif mode in ('story', 'ask', 'end', 'bg'):
    # A background that crossfades in (his others wipe in with a clip)
    rep("    if (p >= 1) { paint(key, t); continue; }\n",
        "    if (p >= 1) { paint(key, t); continue; }\n"
        "    if (style === 'fade') { ctx.save(); ctx.globalAlpha = ease(p); paint(key, t); ctx.restore(); continue; }\n")
    # A highlighted word's colour blends to ink as the box passes (it flipped at 35%)
    rep("ctx.fillStyle = (k.st.hl && hp > 0.35) ? INK : (k.st.c || c0);",
        "ctx.fillStyle = k.st.hl ? mixHex(k.st.c || c0, INK, Math.min(1, Math.max(0, (hp - 0.1) / 0.6))) : (k.st.c || c0);")
    rep("function words(parts, x, base, size, t, t0, t1, o = {}) {",
        "function mixHex(a, b, x) { const p = (h) => h.length === 4 ? [1, 2, 3].map((i) => parseInt(h[i] + h[i], 16)) : [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16)); const A = p(a), B = p(b); x = x * x * (3 - 2 * x); return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * x)).join(',')})`; }\nfunction words(parts, x, base, size, t, t0, t1, o = {}) {")
    # Film time for a film-internal time, for make_cut.sh
    rep("window.seek = (T) => {", "window.filmTime = (t) => { let T0 = 0; for (const [u0, u1, d] of SEG) { if (t <= u1) return T0 + d * (t - u0) / (u1 - u0); T0 += d; } return T0; };\nwindow.BGT = BGT;\nwindow.seek = (T) => {")
if mode == 'story':
    rep("[BGT.field - 0.4, 'nW', 'curtain']", "[BGT.field - 1.6, 'nW', 'fade']")
    rep("[BGT.moments - 0.9, 'nB', 'diagR']", "[BGT.moments - 0.9, 'nB', 'fade']")
    # Text first, then the cards
    rep("const t0 = 14.1 + i * 0.1, e = sp(t - t0, 95, 12.5);", "const t0 = 14.95 + i * 0.1, e = sp(t - t0, 95, 12.5);")
    rep("t, 15.6, 16.5, { mode: 'drift', gap: 0.11 });", "t, 14.15, 15.6, { mode: 'drift', gap: 0.11 });")
    rep("t, 16.5, 18.6, { mode: 'arc', gap: 0.11, hlDelay: 0.3 });", "t, 15.6, 18.0, { mode: 'arc', gap: 0.11, hlDelay: 0.3 });")
    rep("const out = ease((t - 18.0) / 0.3); if (out >= 1) return;\n  FIELD.forEach(([ci, X, Y, ry, rz, s, edge], i) => {",
        "const out = ease((t - 18.0) / 0.3);\n  FIELD.forEach(([ci, X, Y, ry, rz, s, edge], i) => { if (out >= 1) return;")
    # "Remember the connection. Not just their name." holds ~0.5s longer, then fades out (his words() exit); no phone after it
    rep("TX = 18.1;", "TX = 18.6;")
    rep("  ghost('STORY', t, 16.3, 22.4, 880, -1);\n", "  ghost('STORY', t, 16.3, 22.4, 880, -1);\n  return;\n")
    # Only these two shots
    rep("const TOTAL = SEG.reduce(", "SHOTS.splice(0, SHOTS.length, ...SHOTS.filter((x) => x[2] === field || x[2] === moments));\nconst TOTAL = SEG.reduce(")
elif mode == 'ask':
    rep("[BGT.ask - 0.4, 'nC', 'circle']", "[BGT.ask - 1.6, 'nC', 'fade']")
    # The pills once "Ask your own notes." is complete (~23.5); everything holds, then leaves at 25.3 (was 24.25)
    rep("const t0 = 23.0 + i * 0.3, e = sp(tx - t0, 170, 18)", "const t0 = 23.65 + i * 0.3, e = sp(tx - t0, 170, 18)")
    rep("tSend = 24.5, TE = 24.25;", "tSend = 24.5, TE = 25.3;")
    # No phone after it
    rep("  const kbp = clamp((t - 22.72) / 0.4), pe = t - (tType + (nq - 1) * dt)", "  return;\n  const kbp = clamp((t - 22.72) / 0.4), pe = t - (tType + (nq - 1) * dt)")
    rep("const TOTAL = SEG.reduce(", "SHOTS.splice(0, SHOTS.length, ...SHOTS.filter((x) => x[2] === ask));\nconst TOTAL = SEG.reduce(")
elif mode == 'end':
    rep("home_in: 'v14/home_zoomed_in'", "home_in: '../../hook-150/assets/end/home_jl'")
    rep("[BGT.end - 0.4, 'nA', 'diag']", "[BGT.end - 1.6, 'nA', 'fade']")
    rep("const TOTAL = SEG.reduce(", "SHOTS.splice(0, SHOTS.length, ...SHOTS.filter((x) => x[2] === end));\nconst TOTAL = SEG.reduce(")
elif mode == 'bg':
    rep("const TOTAL = SEG.reduce(", "SHOTS.splice(0, SHOTS.length);\nconst TOTAL = SEG.reduce(")
if mode not in ('problem', 'story', 'ask', 'end', 'bg'):
    sys.exit('usage: vince_copy.py problem|story|ask|end|bg')
sys.stdout.write(s)
