#!/usr/bin/env bash
# assemble.sh — normalize, grade, and concat Higgsfield shots into one cut.
#
# Higgsfield has no concat tool, and generated shots vary in resolution, fps, and audio
# presence (e.g. a 720p motion_control shot among 1080p Seedance shots). Concatenating those
# directly produces glitches or fails. This script re-encodes every input to a common spec,
# applies ONE unified teal-orange grade so shots from different generations read as a single
# scene, loudness-normalizes audio (keeping each shot's generated SFX at an even level), then
# concats via the demuxer.
#
# Usage:
#   assemble.sh [options] OUTPUT.mp4 SHOT1 SHOT2 [SHOT3 ...]
#
# Options:
#   --no-audio          Drop audio entirely (pure video concat). Use if any shot is silent and
#                       you don't want to mix silence with SFX.
#   --res WxH           Target resolution (default 1920x1080).
#   --fps N             Target fps (default 30).
#   --grade "FILTER"    Override the default ffmpeg color grade filter chain.
#   --no-grade          Skip color grading (just normalize + concat).
#
# Requires: ffmpeg, ffprobe.
set -euo pipefail

RES="1920x1080"; FPS="30"; AUDIO=1; DO_GRADE=1
GRADE='eq=contrast=1.07:saturation=1.13:gamma=0.98,colorbalance=rs=-0.05:gs=-0.01:bs=0.06:rm=0.01:bm=-0.02:rh=0.06:gh=0.02:bh=-0.06'

args=()
while [ $# -gt 0 ]; do
  case "$1" in
    --no-audio) AUDIO=0; shift;;
    --no-grade) DO_GRADE=0; shift;;
    --res) RES="$2"; shift 2;;
    --fps) FPS="$2"; shift 2;;
    --grade) GRADE="$2"; shift 2;;
    *) args+=("$1"); shift;;
  esac
done

[ "${#args[@]}" -ge 2 ] || { echo "usage: assemble.sh [opts] OUTPUT.mp4 SHOT1 SHOT2 ..." >&2; exit 1; }
OUT="${args[0]}"; SHOTS=("${args[@]:1}")
W="${RES%x*}"; H="${RES#*x}"

SCALE="scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:-1:-1:color=black,fps=${FPS},setsar=1,format=yuv420p"
if [ "$DO_GRADE" = 1 ]; then VF="${GRADE},${SCALE}"; else VF="$SCALE"; fi

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
LIST="$TMP/concat.txt"; : > "$LIST"

i=0
for s in "${SHOTS[@]}"; do
  [ -f "$s" ] || { echo "missing input: $s" >&2; exit 1; }
  n="$TMP/n_$i.mp4"
  if [ "$AUDIO" = 1 ]; then
    # Keep audio; if a shot has none, synthesize silence so concat audio params stay uniform.
    if ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$s" | grep -q .; then
      ffmpeg -nostdin -loglevel error -y -i "$s" -vf "$VF" -c:v libx264 -preset veryfast -crf 20 \
        -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:a aac -ar 48000 -ac 2 "$n"
    else
      ffmpeg -nostdin -loglevel error -y -i "$s" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
        -vf "$VF" -c:v libx264 -preset veryfast -crf 20 -c:a aac -ar 48000 -ac 2 -shortest "$n"
    fi
  else
    ffmpeg -nostdin -loglevel error -y -i "$s" -an -vf "$VF" -c:v libx264 -preset veryfast -crf 20 "$n"
  fi
  echo "file '$n'" >> "$LIST"
  i=$((i+1))
done

ffmpeg -nostdin -loglevel error -y -f concat -safe 0 -i "$LIST" -c copy "$OUT"
echo "wrote $OUT"
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,width,height -of default=noprint_wrappers=1 "$OUT" 2>/dev/null | sed 's/^/  /'
