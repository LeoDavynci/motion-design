# v13 assets (updated Figma + dev build). All paths relative to assets/figma/v13/

Status bar: every Figma frame contains the REAL status bar (9:41, signal/wifi/battery, y 0-~44 at 1x) and NO dynamic island.
Dev-build frames (ask_seq) were captured with the dev build's island hidden (visibility:hidden) so the status bar is real and the area is empty.
=> Use all images as-is, delete the old `clean()` blur: the 3D phone's own island (centered, ~y 11-48 at 1x, x ~135-255) sits in the empty middle of the bar; time (left) and icons (right) are untouched. Never box over it.
Frame corners: Figma frames had baked rounded corners (r~40, grey 245 fill + 1px border). tools/build.py repaints them by smearing interior pixels, so the images are effectively square-cornered; still let the phone clip them.

## Files (780x1688 = 2x of 390x844 unless noted)
| file | what | source | replaces |
|---|---|---|---|
| profile_top.png | updated profile top (hero, SUMMARY card, tags, things to do, WHERE) | Figma 2.6 177:21620 | PROF / audio_ready_v2.png top, FG.mm_b profile |
| profile_scrolled.png | profile scrolled with compact header | Figma 2.7 177:25472 | - |
| profile_full.png (780x2830) | whole scrollable profile as ONE tall page, expanded hero at top, ends w/ moment card + composer | stitched: 2.6 rows 0-750, then 5.4 (294:31110) rows 149+ (offset +601). Seam at page y=750 (10px blend, in empty gap above WHERE) | audio_ready_v2.png (390x1431) |
| profile_header_compact.png (780x260) | pinned compact header (back, "Jordan Lee", ...) | 2.7 rows 0-130 | draw it over profile_full once scrolled past ~120px |
| profile_composer.png (780x198) | "Who did you meet?" composer band | 5.4 rows 745-844 | - |
| profile_meta.json / profile_meta.js | coordinates (1x CSS px of profile_full, x2 for pixels): avatar, summary, moment card, play button, 40 waveform bars (x,y0,y1,color), composer. JS exposes `window.PROFILE_META_V13` | measured from 5.4 | profile_meta.js (old coords no longer valid: moment card moved to y 1062-1258, waveform y~1227-1260) |
| processing.png | "Creating a new profile for Jordan Lee..." | Figma 2.3 294:22950 | FG.add_processing |
| skeleton.png | same + white skeleton card | 2.4 294:23017 | - |
| preview.png | same + updated blue/orange profile card (glasses avatar, chevron) | 2.5 294:23081 | FG.add_preview (no avatar patch needed, avatar is already baked in) |
| home_map.png | updated home mindmap: big gradient nodes OH/TK/AK/MC/HC/ZA, connections, Filters pill, "Jordan" back pill, Ask bar | Figma 5.5 183:4842 | FG.map_in / mm_a for closing scene |
| ask_1_suggest.png | Search for someone by... + keyboard | 6.1a 294:31691 | FG.find_suggest |
| ask_2_query.png | query typed, send button | 6.2a 294:31833 | FG.find_query |
| ask_3_thinking.png | thinking: "Reading your notes..." + skeleton cards | 6.3 294:32257 | (new) |
| ask_4_results.png | results, Jordan + Zarah cards, white "Draft a message" CTA | 6.4 294:32745 | FG.match1 |
| ask_4b_results_draft.png | results with Jordan's draft expanded (Copy Text / Share) | 6.4 294:32790 | FG.match2/3 |
| ask_5_copied.png | "Message copied to clipboard" toast | 6.5 294:32870 | - |
| ask_seq/f000..f072.png | 73 frames, 12 fps (6.1 s), 786x1704 (phone texture size, matches SCR canvas), REAL dev-build behaviour: keyboard+typed query -> Send -> thinking ("Reading your notes..." -> "Looking through your people..." -> "Picking the best matches...", skeleton cards) -> results with white Draft CTAs. Frame i = t*12. Results settle at ~f040 (3.3 s); f000-f003 still show keyboard. Pure function of time: pick floor(t*12). | localhost:5173 (no mock), tools/ask2.mjs | the static sheet that slid up from the bottom |
| fig1x/ | raw 390x844 Figma exports | | |
| tools/ | build.py (upscale/stitch/corner repair), ask2.mjs + lib.mjs (playwright capture) | | |

## Caveats
- Figma screenshot tool does not render above 1x (maxDimension is a cap, not a scale): all Figma-derived images are LANCZOS 2x upscales of 390x844 exports (slightly soft text). The dev-build ask_seq is native 2x and crisp. If sharper Figma is needed, export 2x from the Figma UI.
- ask_seq uses the dev-build mock data (Jordan avatar = teal blob, copy "Climbs Tuesdays, wants a climbing buddy"); Figma 6.4 uses glasses avatar and slightly different card copy. The previous avatar patching (AV z*.png, patchFrame) still applies if matching Figma avatars is wanted; this is a visible mismatch if you cut between ask_seq and ask_4_results.
- profile_full: mutuals row comes from Figma 5.4 (5 avatars incl. "An..." cut) not 2.6 (2 avatars). Composer is baked at the bottom (really pinned in app). Page ends at y=1415 (1x).
- 6.3 thinking in Figma is a single frame; use ask_seq for the real animation.
- Hero in profile_top has a light beige strip behind its rounded bottom corners: that is the design.
