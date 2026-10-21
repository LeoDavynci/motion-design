# hook-150: alternate opening (Emily)

An experimental hook for the Peepl launch film, kept in its own folder so it doesn't touch the main film (`../index.html`).

**What it shows:** "150" is typed and snaps down into "150 people. Dunbar's number.", then "That's how many your brain
can handle." with a 152-dot colorful grid, then "But what about the rest?" cuts into a zoom while the grid opens up
and a white grid fills the screen. The text slides off, the dots fade out from the middle, and it crossfades into the
main film's "Meeting people is easy" shot (2.8s in `../index.html`).

**Designs:** Figma file `bV6DQFxu5SHuF6hE5NIDeb`, page "Video Edits": Frames 1-3 and 16-19. The typing motion follows a
screen recording reference (letters fade and sharpen in, the caret jumps after each one, the line re-centers).

**Files**
- `index.html`: the hook, `window.seek(t)` like the main film (same render contract, uses `../lib/motion.js`).
- `dots.js`: the colorful grid's dot positions and colors, from Figma Frame 17.
- `assets/bg.png`: the background image from the Figma frames (grain included).
- `render_segment.mjs`: renders just `[from, to]` of a film (`render.mjs` always starts at 0).
- `make_cut.sh`: renders the hook, renders the main film's problem shot (2.6s-4.6s) from a temporary copy with the
  opening dot-field shot switched off, and joins them with a 0.4s crossfade. `../index.html` itself is never changed.

**Render:** `cd hook-150 && node ../render.mjs --fps 60 --dur 17.6 --sub 8` (hook only), or `zsh hook-150/make_cut.sh`
(hook into the main film). Output goes to `hook-150/out/` (ignored by git). No sound yet.
