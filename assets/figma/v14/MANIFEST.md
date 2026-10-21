# v14 assets: latest Figma (file bV6DQFxu5SHuF6hE5NIDeb, canvas "V1 flow - detailed" 161:2)

All images are TRUE 2x (vector re-render, not upscaled) and have NO status bar, NO keyboard (ask flow) and SQUARE corners (no baked rounded grey/border).
The area where the status bar was shows the frame's own background; overlay status_light.png / status_dark.png yourself.

## How
In a temporary scratch page, each source frame was cloned; Status bar instance hidden (visible=false), keyboard container hidden, cornerRadius=0, strokes cleared; clone.rescale(2); rendered with get_screenshot (1:1 of the 2x node). Originals untouched. Scratch page deleted and verified (page list = the original 8 pages).
Alpha for status bars: rendered over black and white backing and recovered (screenshots are opaque).

## Files
| file | size | source node(s) | replaces |
|---|---|---|---|
| status_light.png | 780x108 (390x54 @2x), transparent | Status bar component, variant `Property 1=white` (294:10354); content bbox 2x px x69-718, y57-82 (1x: x34.5-359, y28.5-41) | new overlay for dark/colorful screens (profile hero etc.) |
| status_dark.png | 780x108, transparent | variant `Property 1=black` (94:94, instance 294:33879); same geometry | overlay for light screens (home, add, ask) |
| home_zoomed_out.png | 786x1704 (393x852 @2x) | 1.1 294:33858 | mm_a.png / v13 home_map |
| home_zoomed_in.png | 786x1704 | 1.2 294:33981 | mm_b.png |
| home_tap.png | 786x1704 | 1.3 294:34554 (Maya Chen pill with chevron "View", MC node, connections lit; a small white finger/touch circle is baked near the Ask bar mic, it is in the design) | - |
| home_filters.png | 786x1704 | 1.4 294:34132 (Group by menu) | - |
| home_list.png | 786x1704 | 1.6 294:34447 (Connections list) | - |
| home_skeleton.png | 786x1704 | 1.0 294:33607 | - |
| profile_top.png | 780x1688 | 2.6 177:21620 (hero Expanded + body, whole frame) | v13/profile_top.png |
| profile_full.png | 780x2722 (390x1361) | 2.6 frame with body swapped for 5.4 body (294:31111, "Finish moment", playback complete); composer hidden | v13/profile_full.png |
| profile_full_ready.png / profile_full_playing.png | 780x2722 | same with 5.2 body 294:28998 (ready) / 5.3 body 294:30648 (playing: 7/40 bars played, pause icon, text half grey) | - |
| profile_composer.png | 780x200 | bottom 100px of 5.4 294:31110 ("Who did you meet?" + mic) | v13/profile_composer.png |
| profile_header_compact.png | 780x252 (390x126) | Profile Top `Collapsed` (237:3687) from 2.7 177:25472 | v13/profile_header_compact.png |
| profile_meta.json / .js (`window.PROFILE_META_V14`) | | measured from the clones, 1x px of profile_full (avatar, hero texts, summary, mutuals, moment card, play, 40 waveform bars x/w/y0/y1/color, text boxes + estimated baselines) | v13/profile_meta |
| add_1_recording.png | 780x1688 | 2.1 294:23253 (also older 177:17598 "Talking" variant exists) | FG.add_* |
| add_2_live.png | 780x1688 | 2.2 294:22850 | |
| add_3_processing.png | 780x1688 | 2.3 294:22950 | v13/processing.png |
| add_4_skeleton.png | 780x1688 | 2.4 294:23017 | v13/skeleton.png |
| add_5_preview.png | 780x1688 | 2.5 294:23081 (blue/orange card, glasses avatar) | v13/preview.png |
| ask_1_suggest.png | 780x1688 | 6.1a 294:31691, keyboard container (Frame 1 at y496, 390x346) hidden | v13/ask_1_suggest.png |
| ask_2_query.png | 780x1688 | 6.2a 294:31833, keyboard hidden; query + send arrow in the composer at bottom | v13/ask_2_query.png |
| ask_3_thinking.png | 780x1688 | 6.3 294:32257 | |
| ask_4_results.png | 780x1688 | 6.4 294:32745 (white "Draft a message") | |
| ask_4b_draft.png | 780x1688 | 6.4 294:32790 (draft open, Copy Text / Share) | |
| ask_5_copied.png | 780x1688 | 6.5 294:32870 (toast at top) | |
| keyboard.png | 780x664 (390x332) | component "Actully good Keyboard" 294:23489, with its background (top corners rounded, grey) | |
| keyboard.json | | key rects x,y,w,h in 1x keyboard-local px (a-z, shift, delete, 123, space, return) + autocorrection row, emoji, mic | |

## Status bar variants
Component set "Status bar", property `Property 1` = `white` (light content, use on dark/colored screens) / `black` (dark content, use on light screens). 390x54, time at 1x (34,25 32x21), icons at (294,29 66x12). No dynamic island in the component.

## Caveats
- Hidden status bar leaves empty background (home: gradient continues; ask/add: pale gradient; profile: hero blobs). Nothing is repainted.
- Keyboard keys are plain frames in Figma: NO pressed variant exists. Fake pressed state in the film (lighten rect from keyboard.json).
- Home 1.1-1.3 frames are 393x852 (not 390x844): 786x1704 images. Home "5.5 Home view connections" (183:4842) no longer exists in the file (getNodeById null); use home_tap / home_zoomed_in.
- profile_full is built (hero from 2.6 + body from 5.x), page height 1361 because composer is removed; the body's Aura background only spans the first ~844px (as in the design), rest is the plain frame fill. Hero has its beige strip behind rounded bottom corners (design).
- In 5.2 and 5.4 the waveform/play look identical (both full gradient, play icon); only 5.3 differs. Playing bars colors: played = gradient, unplayed #d8d8d8.
- profile_meta.json bars: pitch 5px, w 2, centered y 1225.5, gradient #2f4fd0 -> #ec5a32.
- ask_seq/ in this folder belongs to another agent.
