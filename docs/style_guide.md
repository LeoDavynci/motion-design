# Peepl launch film: style guide (v2)

**Format:** 16:9, 1920x1080, 60 fps, 30 s, H.264 yuv420p CRF 16, synthesized sound at 120 BPM (1 beat = 0.5 s, 60 beats), -14 LUFS.
**Sources (all real):** Figma file bV6DQFxu5SHuF6hE5NIDeb (V1 flows), localhost:5173/?mock=100 (updated build), case study PDF (copy + deck look).

## Concept
A startup launch film, not a screen recording. The product is the hero: phones glide, rotate and parallax on top of branded color fields, kinetic type names each idea, and UI details are pulled out of the screen as floating callouts. Story: **150 people you can remember → hundreds you can't → Peepl → talk for 20 seconds → it keeps the story → ask your own notes → show the network → remember the story.**

## Two moods (from the deck)
- **Night** `#1c1522`: huge blurred blue `#2f4fd0` and coral `#ec5a32` blobs (plus a little magenta `#d6347f`) drifting slowly. Used for hook, story, ask, CTA.
- **Day** `#f4efe7`: pastel washes (`#dde3fb` blue, `#fde0d4` coral, `#fadbe8` pink, `#fbf0c4` yellow) plus the app's dotted grid. Used for reveal and capture.
Transitions between moods are colour wipes that travel on a beat, never a fade.

## Colour meaning (kept from the product)
Dots, avatars and nodes use the relationship hues only where the product does: work blue, social coral, community yellow, family magenta, unsorted grey. Depth of hue = how well you know them.
**One UI accent: lime `#c6f04a`** (the app's "live" colour). It is used for the highlighter swipe behind one key word per shot, recording indicators, and the CTA. No second accent.

## Type
- **Geist 300** for display, very large (160-300 px), -4% tracking. Key words in Geist 600.
- **Geist Mono 400** for tiny uppercase eyebrow labels with an index ("01 · CAPTURE"), as in the deck. They sit inside the layout above a headline, never in corners.
- No serif.

## Product framing
- Phone: 390x844 screens in a black bezel with a dynamic island on Night, thin white bezel on Day; soft contact shadow, no glow.
- Screens come from Figma exports (designed flows) and from the live app at 2x (mindmap, list, profile). No screen is invented. Jordan Lee is a real scenario from the case study.
- Callouts: UI fragments cropped from the same screens, scaled up, floated beside the phone on frosted white cards (`rgba(255,255,255,.6)`, 24 px radius), connected by a thin line that draws on.

## Motion vocabulary (varied on purpose)
1. Kinetic type: words rise out of masks, swap in place on beats, and a lime highlighter swipes behind one word.
2. Dot field: the Dunbar grid, 150 lit dots versus the rest.
3. Phone choreography: slide-in with spring overshoot, 3D-feeling tilt (rotate + skew), parallax between two or three phones at different speeds.
4. Camera pushes and pull-backs to a detail, with a whip-pan between shots.
5. Typing and transcript reveal synced to the voice bar.
6. Counters and number slams (150).
7. Node pop on the mindmap, with edges drawing in.
8. Loop diagram: Log → Ask → Act → Close, one node lit per beat.
9. Mask wipes and shape-driven cuts on beats.
Every 2-4 seconds something new happens.

## Banned (project defaults + mine)
Centered title on a gradient, everything fading in, corner labels, frame borders, glow on UI, generic particle bursts, invented screens, invented metrics, Math.random, CSS transitions, timers.

## Sound
Synthesized, no sample packs. Warm sub + mallet arp over a soft kick, 120 BPM. Hits on the measured grid (beats.json): dot pops (hook), whooshes on each cut, key ticks on the transcript, riser into the reveal, four card hits on the Ask results, final chord. Master -14 LUFS.

## Render contract
`window.seek(t)` paints frame t from `t` only. 60 fps with 2 sub-frames for motion blur (3600 captures). No state between frames, seeded noise only, Geist loaded before first frame.
