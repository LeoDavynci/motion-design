#!/bin/zsh
# The hook, Vince's "Meeting people is easy / Remembering them is hard" shot, and "Introducing Peepl":
#   1. the hook (index.html)
#   2. Vince's whole problem shot, at 65% speed (his index.html, 2.4s-5.5s, from a temporary copy that plays only
#      that shot and keeps his night background, which in his film wipes to day at 4.6s; his file is never changed).
#      His night background is close to the hook's, so a 0.4s crossfade reads as one continuous background.
#   3. "Introducing Peepl" (intro.html), on the light background, brought in by a 0.6s soft wipe from the left, like the
#      wipes Vince's film uses between its night and day scenes.
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
echo "hook: ${HOOK_DUR}s, intro: ${INTRO_DUR}s"
mkdir -p hook-150/out
node hook-150/render_segment.mjs --page hook-150/index.html --from 0 --to "$HOOK_DUR" --fps "$FPS" --sub "$SUB" --out hook-150/out/silent.mp4

# Vince's film with only the problem shot, on its night background (his file is not changed)
TMP=.cut-problem.tmp.html
sed -e 's/^const SHOTS = .*/const SHOTS = [[2.8, 5.0, problem]];/' -e "s/\[4.6, 'dA', 'diag'\], //" index.html > "$TMP"
grep -q '^const SHOTS = \[\[2.8, 5.0, problem\]\];' "$TMP" && ! grep -q "\[4.6, 'dA'" "$TMP" || { echo "could not isolate the problem shot"; rm -f "$TMP"; exit 1; }
VINCE_SPEED=0.65  # Vince's shot plays at 65% speed (user's call: it read too fast)
node hook-150/render_segment.mjs --page "$TMP" --from 2.4 --to 5.5 --speed "$VINCE_SPEED" --fps "$FPS" --sub "$SUB" --out hook-150/out/vince-problem.mp4
rm -f "$TMP"
node hook-150/render_segment.mjs --page hook-150/intro.html --from 0 --to "$INTRO_DUR" --fps "$FPS" --sub "$SUB" --out hook-150/out/intro.mp4

FADE=0.4; WIPE=0.6; VINCE=$(node -e "console.log((3.1 / ${VINCE_SPEED}).toFixed(3))")
O1=$(node -e "console.log((${HOOK_DUR} - ${FADE}).toFixed(3))")
O2=$(node -e "console.log((${HOOK_DUR} - ${FADE} + ${VINCE} - ${WIPE}).toFixed(3))")
ffmpeg -y -loglevel error -i hook-150/out/silent.mp4 -i hook-150/out/vince-problem.mp4 -i hook-150/out/intro.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=${FADE}:offset=${O1}[a];[a][2:v]xfade=transition=smoothright:duration=${WIPE}:offset=${O2},format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -crf 16 -r "$FPS" hook-150/out/peepl-film-draft.mp4
cp hook-150/out/silent.mp4 hook-150/out/peepl-hook-150.mp4
echo done
