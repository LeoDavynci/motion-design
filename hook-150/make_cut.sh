#!/bin/zsh
# The hook + the start of Vince's film: renders the hook (index.html), renders Vince's "Meeting people is easy /
# Remembering them is hard" shot (his index.html, 2.6s-4.6s, from a temporary copy with his opening dot-field shot
# turned off so nothing of it lingers), and joins them with a 0.4s crossfade. His night background (blue top right,
# orange bottom left) is close to the hook's, so the crossfade reads as one continuous background.
# Run from anywhere:  zsh ~/motion-design/hook-150/make_cut.sh [draft|final]
#   draft (default): 30fps, 2 sub-frames of motion blur. For checking timing while iterating.
#   final: 60fps, 8 sub-frames. For versions to share.
# Both parts go through render_segment.mjs (fast JPEG capture); the studio's render.mjs is left as it is.
# Output: hook-150/out/peepl-hook-150-into-problem.mp4
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

HOOK_DUR=$(node -e "import('playwright').then(async({chromium})=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage();await p.goto('file://'+process.cwd()+'/hook-150/index.html');await p.evaluate(()=>window.ready);console.log(await p.evaluate(()=>window.DURATION));await b.close()})")
echo "hook: ${HOOK_DUR}s"
mkdir -p hook-150/out
node hook-150/render_segment.mjs --page hook-150/index.html --from 0 --to "$HOOK_DUR" --fps "$FPS" --sub "$SUB" --out hook-150/out/silent.mp4

# Vince's film with only the problem shot (his file is not changed)
TMP=.cut-problem.tmp.html
sed 's/^const SHOTS = \[\[0, 2.8, hook\], /const SHOTS = [/' index.html > "$TMP"
grep -q '^const SHOTS = \[\[2.8, 5.0, problem\]' "$TMP" || { echo "could not isolate the problem shot"; rm -f "$TMP"; exit 1; }
node hook-150/render_segment.mjs --page "$TMP" --from 2.6 --to 4.6 --fps "$FPS" --sub "$SUB" --out hook-150/out/vince-problem.mp4
rm -f "$TMP"

FADE=0.4
OFFSET=$(node -e "console.log((${HOOK_DUR} - ${FADE}).toFixed(3))")
ffmpeg -y -loglevel error -i hook-150/out/silent.mp4 -i hook-150/out/vince-problem.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=${FADE}:offset=${OFFSET},format=yuv420p[v]" \
  -map "[v]" -c:v libx264 -crf 16 -r "$FPS" hook-150/out/peepl-hook-150-into-problem.mp4
cp hook-150/out/silent.mp4 hook-150/out/peepl-hook-150.mp4
echo done
