# hook-150: alternate opening (Emily)

An experimental hook for the Peepl launch film, kept in its own folder so it doesn't touch the main film (`../index.html`).

**What it shows:** "150" is typed and snaps down into "150 people. Dunbar's number.", then "That's how many your brain
can handle." with a 152-dot colorful grid, then "But what about the rest?" cuts into a zoom while the grid opens up
and a white grid fills the screen. The text slides off, the dots fade out from the middle, and it crossfades into the
main film's "Meeting people is easy" shot (2.8s in `../index.html`), which wipes into "Introducing Peepl" on a light
background: the discs from the prototype's mindmap slide in, gather into a cluster, and the camera zooms into Jordan
Lee, whose initials and profile pill pop up. The view then zooms out into the screen of a phone (the prototype's device
frame) on a pale background, a thumb taps Jordan's pill, and his profile slides up.

**Designs:** Figma file `bV6DQFxu5SHuF6hE5NIDeb`, page "Video Edits": Frames 1-3 and 16-19 (hook), 25, 22, 23, 26, 27,
28 (Introducing Peepl), then the phone frames 427:6972 / 427:6981 and "2.6 Person profile / View details" (427:7102,
saved as `assets/phone/profile-jordan.png`). The typing motion follows a
screen recording reference (letters fade and sharpen in, the caret jumps after each one, the line re-centers).

**Files**
- `index.html`: the hook, `window.seek(t)` like the main film (same render contract, uses `../lib/motion.js`).
- `intro.html`: "Introducing Peepl" (same contract). Its two backgrounds (the scene's, and the pale one around the
  phone) are drawn once into `assets/intro/bg.png` and `assets/phone/pale.png` by `make_intro_bg.mjs` from the Figma
  shapes in `assets/intro/` and `assets/phone/` (redrawing them every frame was ~10x slower). Rerun it after changing
  the shapes.
- `typing.js`: the typed lines both films use (typing, caret, re-centering, cut-zooms, exits).
- `dots.js`: the colorful grid's dot positions and colors, from Figma Frame 17.
- `assets/bg.png`: the background image from the Figma frames (grain included).
- `render_segment.mjs`: renders just `[from, to]` of a film (`render.mjs` always starts at 0).
- `make_cut.sh`: renders the hook, the main film's problem shot (2.4s-5.5s at 80% speed, from a temporary copy with the opening
  dot-field shot switched off) and the intro, and joins them: a 0.4s crossfade, then a 0.6s soft wipe from the left.
  `../index.html` itself is never changed.

**Render:** `zsh hook-150/make_cut.sh` renders the hook into the main film as a quick draft (30fps, 2 sub-frames,
~2 min); `zsh hook-150/make_cut.sh final` renders the full-quality version (60fps, 8 sub-frames of motion blur,
~15 min). Hook only: `cd hook-150 && node ../render.mjs --fps 60 --dur 17.6 --sub 8`. Output (`hook-150/out/peepl-film-draft.mp4`) goes to `hook-150/out/`
(ignored by git). No sound yet.
