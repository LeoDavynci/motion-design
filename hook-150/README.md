# hook-150: alternate opening (Emily)

An experimental hook for the Peepl launch film, kept in its own folder so it doesn't touch the main film (`../index.html`).

**What it shows:** "150" is typed and snaps down into "150 people. Dunbar's number.", then "That's how many your brain
can handle." with a 152-dot colorful grid, then "But what about the rest?" cuts into a zoom while the grid opens up
and a white grid fills the screen. The text slides off, the dots fade out from the middle, and it crossfades into the
main film's "Meeting people is easy" shot (2.8s in `../index.html`), which wipes into "Introducing Peepl" on a light
background: the discs from the prototype's mindmap slide in, gather into a cluster, and the camera zooms into Jordan
Lee, whose initials and profile pill pop up. The camera then pulls back: it was the screen of a phone all along (a dark iPhone, like the one in the main film), seen whole on a pale background. A thumb taps Jordan's pill, and his profile slides up; then the phone fades away.
"Speak into the mic" is typed, a waveform streams in from the right and gathers into the voice box (already part-way
through the transcript), the camera pulls back to the phone around the box, a thumb taps send, and Jordan's new profile
is created (skeleton card, then the profile card). It crossfades into the main film's (v17) "Every person. Every
story." and "Remember the connection. Not just their name." (headline before the cards, crossfades instead of wipes),
then, once that line has faded out, a moment plays back (`moment.html?v=card`; `?v=button` is the unused other
version): the collapsed card widens into "First meeting" and opens, each with a slight bounce; a thumb taps play, the words darken and the waveform fills
in, and at 3/4 the camera pulls back to the phone (Jordan's profile, scrolled to Moments).

**Designs:** Figma file `bV6DQFxu5SHuF6hE5NIDeb`, page "Video Edits": Frames 1-3 and 16-19 (hook), 25, 22, 23, 26, 27,
28 (Introducing Peepl), then the phone frames 427:6972 / 427:6981 and "2.6 Person profile / View details" (427:7102,
saved as `assets/phone/profile-jordan.png`, its dark header stretched 2px out to the edges), then 430:7792-8352 and the
prototype screens 2.3-2.5 "Add person / Create profile" (`create.html`). The typing motion follows a
screen recording reference (letters fade and sharpen in, the caret jumps after each one, the line re-centers).

**Files**
- `index.html`: the hook, `window.seek(t)` like the main film (same render contract, uses `../lib/motion.js`).
- `intro.html`: "Introducing Peepl" (same contract). Its two backgrounds (the scene's, and the pale one around the
  phone) are drawn once into `assets/intro/bg.png` and `assets/phone/pale.png` by `make_intro_bg.mjs` from the Figma
  shapes in `assets/intro/` and `assets/phone/` (redrawing them every frame was ~10x slower). Rerun it after changing
  the shapes.
- `moment.html`: the moment playback (`?v=button` or `?v=card`), Figma 437:9943-10293, assets in `assets/moment/`.
- `create.html`: "Speak into the mic" to Jordan's new profile (same contract), assets in `assets/create/`.
- `vince_copy.py`: the edits make_cut.sh makes to temporary copies of the main film to render its shots.
- `typing.js`: the typed lines all three use (typing, caret, re-centering, cut-zooms, exits, Vince-style highlights).
- `dots.js`: the colorful grid's dot positions and colors, from Figma Frame 17.
- `assets/bg.png`: the background image from the Figma frames (grain included).
- `render_segment.mjs`: renders just `[from, to]` of a film (`render.mjs` always starts at 0).
- `make_cut.sh`: renders the hook, the main film's problem shot (2.4s-5.5s at 65% speed, from a temporary copy with the opening
  dot-field shot switched off) and the intro, and joins them: a 0.4s crossfade, then a 0.6s soft wipe from the left.
  `../index.html` itself is never changed. `create.html` follows the intro with a 0.3s crossfade on the pale background.

**Render:** `zsh hook-150/make_cut.sh` renders the hook into the main film as a quick draft (30fps, 2 sub-frames,
~2 min); `zsh hook-150/make_cut.sh final` renders the full-quality version (60fps, 8 sub-frames of motion blur,
~15 min). Hook only: `cd hook-150 && node ../render.mjs --fps 60 --dur 17.6 --sub 8`. Output (`hook-150/out/peepl-film-draft.mp4`) goes to `hook-150/out/`
(ignored by git). No sound yet.
