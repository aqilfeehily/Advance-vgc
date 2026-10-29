#!/bin/bash
# Rebuild all media for the "vgc-9x16" Epic Style project from input/source.mov, then render.
# Run on the Mac (CoreML matte): bash projects/vgc-9x16/build_media.sh   (needs ffmpeg, node, python3 with numpy+opencv)
set -e
cd "$(dirname "$0")"
SK=../../.claude/skills/epic-style
mkdir -p work assets/clips assets/fonts && cp $SK/template/assets/fonts/* assets/fonts/
ffmpeg -v error -y -i ../../input/source.mov -vf "fps=30,format=yuv420p" -c:v libx264 -crf 14 -preset fast -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -c:a aac -b:a 192k -ar 48000 work/src30.mp4
python3 tools/cut.py            # -> work/edit.mov + work/timemap.json (4 repeats cut, snapped to audio dips)
(cd work && python3 ../tools/decap.py run)  # -> work/clean.mov (burned-in captions removed)
bash $SK/scripts/prep_media.sh presenter work/clean.mov 0.62   # CoreML matte -> assets/presenter.webm
enc="-c:v libx264 -crf 16 -preset fast -g 15 -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv -an -movflags +faststart"
ffmpeg -v error -y -ss 17.73 -t 6.4 -i work/clean.mov $enc assets/clips/insA.mp4
ffmpeg -v error -y -ss 83.4 -t 4.0 -i work/clean.mov $enc assets/clips/insB.mp4
bash $SK/scripts/make_sfx.sh work/sfx
ffmpeg -v error -y -i work/clean.mov -vn -ac 2 -ar 48000 -af "volume=1.3dB,alimiter=limit=0.9:level=disabled" work/vo.wav
python3 tools/mix_simple.py
npx --yes hyperframes@0.8.149 lint
mkdir -p renders ../../output
npx --yes hyperframes@0.8.149 render --quality looks --fps 30 --sdr -o renders/vgc-final.mp4 --quiet
cp renders/vgc-final.mp4 ../../output/vgc_epic_9x16.mp4
