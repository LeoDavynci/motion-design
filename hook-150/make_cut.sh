#!/bin/zsh
# The hook, Vince's "Meeting people is easy / Remembering them is hard" shot, and "Introducing Peepl":
#   1. the hook (index.html)
#   2. Vince's whole problem shot, at 65% speed (his index.html, 2.4s-5.85s, from a temporary copy that plays only
#      that shot and keeps his night background, which in his film wipes to day at 4.6s; his file is never changed).
#      In the copy, "Remembering them is hard." and the cards stay 0.35s longer (exit at 5.05s instead of 4.7s), a beat
#      after the "hard." highlight before they leave (user's call).
#      His night background is close to the hook's, so a 0.4s crossfade reads as one continuous background.
#   3. "Introducing Peepl" (intro.html), on the light background, brought in by a 0.6s soft wipe from the left, like the
#      wipes Vince's film uses between its night and day scenes. It ends on the pale background once the phone fades.
#   4. "Speak into the mic" and the new profile (create.html), which starts on the same pale background (0.3s crossfade).
#   5. Vince's "Every person. Every story." and "Remember the connection. Not just their name." (his v17 film, from a
#      temporary copy: headline before the cards, crossfades instead of his wipes, see vince_copy.py), brought in by a
#      0.8s crossfade from the new profile, ending on "Not just their name." held for a beat.
# The "Meeting people is easy" shot stays the one from his first version (commit 964dee0), which this cut was timed on.
# Run from anywhere:  zsh ~/motion-design/hook-150/make_cut.sh [draft|final]
#   draft (default): 30fps, 2 sub-frames of motion blur. For checking timing while iterating.
#   final: 60fps, 8 sub-frames. For versions to share.
# Both parts go through render_segment.mjs (fast JPEG capture); the studio's render.mjs is left as it is.
# Output: hook-150/out/peepl-film-draft.mp4
set -e
MODE=${1:-draft}
case "$MODE" in
  draft) FPS=30; SUB=2 ;;
  final) FPS=60; SUB=8 ;;
  *) echo "usage: make_cut.sh [draft|final]"; exit 1 ;;
esac
echo "$MODE: ${FPS}fps, $SUB sub-frames"
cd "$HOME/motion-design"
export PATH="$HOME/motion-design/bin:$PATH"

dur() { node -e "import('playwright').then(async({chromium})=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage();await p.goto('file://'+process.cwd()+'/$1');await p.evaluate(()=>window.ready);console.log(await p.evaluate(()=>window.DURATION));await b.close()})"; }
HOOK_DUR=$(dur hook-150/index.html)
INTRO_DUR=$(dur hook-150/intro.html)
CREATE_DUR=$(dur hook-150/create.html)
echo "hook: ${HOOK_DUR}s, intro: ${INTRO_DUR}s, create: ${CREATE_DUR}s"
mkdir -p hook-150/out
node hook-150/render_segment.mjs --page hook-150/index.html --from 0 --to "$HOOK_DUR" --fps "$FPS" --sub "$SUB" --out hook-150/out/silent.mp4

# Vince's film with only the problem shot, on its night background (his file is not changed)
TMP=.cut-problem.tmp.html
git show 964dee0:index.html | python3 hook-150/vince_copy.py problem > "$TMP" || { rm -f "$TMP"; exit 1; }
VINCE_SPEED=0.65  # Vince's shot plays at 65% speed (user's call: it read too fast)
VFROM=2.4; VTO=5.85
node hook-150/render_segment.mjs --page "$TMP" --from "$VFROM" --to "$VTO" --speed "$VINCE_SPEED" --fps "$FPS" --sub "$SUB" --out hook-150/out/vince-problem.mp4
rm -f "$TMP"
node hook-150/render_segment.mjs --page hook-150/intro.html --from 0 --to "$INTRO_DUR" --fps "$FPS" --sub "$SUB" --out hook-150/out/intro.mp4
node hook-150/render_segment.mjs --page hook-150/create.html --from 0 --to "$CREATE_DUR" --fps "$FPS" --sub "$SUB" --out hook-150/out/create.mp4

# Vince's v17 "Every person" + "Remember the connection" (his file is not changed): from just before the field shot (his
# night background alone) to just before his phone comes up under "Not just their name."
TMP=.cut-story.tmp.html
python3 hook-150/vince_copy.py story < index.html > "$TMP" || { rm -f "$TMP"; exit 1; }
RANGE=$(node -e "import('playwright').then(async({chromium})=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage();await p.goto('file://'+process.cwd()+'/$TMP');await p.evaluate(()=>window.ready);console.log(await p.evaluate(()=>[window.filmTime(window.BGT.field)-0.9,window.filmTime(window.BGT.moments+2.45)].map((x)=>x.toFixed(3)).join(' ')));await b.close()})")
SFROM=${RANGE% *}; STO=${RANGE#* }
node hook-150/render_segment.mjs --page "$TMP" --from "$SFROM" --to "$STO" --fps "$FPS" --sub "$SUB" --out hook-150/out/story-raw.mp4
rm -f "$TMP"
HOLD=0.8   # "Not just their name." holds a beat at the end
ffmpeg -y -loglevel error -i hook-150/out/story-raw.mp4 -vf "tpad=stop_mode=clone:stop_duration=${HOLD}" -c:v libx264 -crf 16 -pix_fmt yuv420p hook-150/out/story.mp4

FADE=0.4; WIPE=0.6; PALE=0.3; STORY=0.8; VINCE=$(node -e "console.log(((${VTO} - ${VFROM}) / ${VINCE_SPEED}).toFixed(3))")
O1=$(node -e "console.log((${HOOK_DUR} - ${FADE}).toFixed(3))")
O2=$(node -e "console.log((${HOOK_DUR} - ${FADE} + ${VINCE} - ${WIPE}).toFixed(3))")
O3=$(node -e "console.log((${HOOK_DUR} - ${FADE} + ${VINCE} - ${WIPE} + ${INTRO_DUR} - ${PALE}).toFixed(3))")
O4=$(node -e "console.log((${HOOK_DUR} - ${FADE} + ${VINCE} - ${WIPE} + ${INTRO_DUR} - ${PALE} + ${CREATE_DUR} - ${STORY}).toFixed(3))")
ffmpeg -y -loglevel error -i hook-150/out/silent.mp4 -i hook-150/out/vince-problem.mp4 -i hook-150/out/intro.mp4 -i hook-150/out/create.mp4 -i hook-150/out/story.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=${FADE}:offset=${O1}[a];[a][2:v]xfade=transition=smoothright:duration=${WIPE}:offset=${O2}[b];[b][3:v]xfade=transition=fade:duration=${PALE}:offset=${O3}[c];[c][4:v]xfade=transition=fade:duration=${STORY}:offset=${O4},format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -crf 16 -r "$FPS" hook-150/out/peepl-film-draft.mp4
cp hook-150/out/silent.mp4 hook-150/out/peepl-hook-150.mp4
echo done
