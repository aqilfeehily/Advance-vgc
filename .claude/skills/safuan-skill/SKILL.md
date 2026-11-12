---
name: safuan-skill
description: >-
  "Safuan Skill": Aqil's saved TikTok 9:16 talking-head edit for the owner BroSafuan, in the "Caption Cutaway" look taken from a
  Drive reference video: full-frame footage (grade untouched), white rounded hook box at the start, small black-box captions with
  yellow keywords, and cutaway cards that slide into a top strip. No music, light SFX, BroSafuan circle photo on the end card.
  Use whenever the user says "safuan skill", "style safuan", "macam video engagement safuan tu", or wants Safuan's footage edited
  in the same way again, even without a link. Built with HyperFrames; renders the real MP4.
---

# Safuan Skill (Caption Cutaway)

First built Nov 2026 for "Engagement yang kita tak nampak" (89.6 s). Reply in casual Malaysian BM (aku/kau). Render straight away
(Aqil's standing rule): no storyboard gate, no questions; state assumptions in the final note. Owner = **BroSafuan** (one word;
Whisper hears "Bruce Afwan"/"Bruce Afan": fix it). The brand logo is only his photo (`content-safuan/assets/brosafuan_logo_circle.png`).
Never another brand/logo. Reference videos from other people give the style only, never their logos, names or scripts.

## Look (numbers)
- 1080×1920, 30 fps. Footage full frame in `#cam` (origin 45% 42%), slow push 1.00→1.06 per stint plus a punch (1.10–1.12) on
  beats like "Nombor satu/dua". No colour overlay on the face; only the end card dims the picture (rgba 6,10,20,.78).
- Hook: white box, Inter 900 62 px, radius 26, y 335, 0–2 s, back.out pop.
- Captions: black rounded box rgba(8,8,8,.88), Inter 800 54 px, y 1040 (inside the TikTok safe zone), chunks of ≤5 words, ≤28 chars,
  broken at every Whisper segment and at gaps >0.45 s; keywords #FFD84A via the `KEY` regex.
- Cutaway cards: top strip y 290–630 (h 340), navy gradient with yellow bottom border, slide down 0.28 s expo.out / up 0.2 s;
  contents drawn in HTML/SVG (numbered badge + pause icon, tick, STAY, 2× chip, scrubber bar). Scrubber knobs move with `x`,
  fills with `scaleX` (lint rejects animating `left`/`width`). Cards only visualise what is SAID; never invent numbers.
- End card: 300 px circular photo (white 4 px border, cyan glow), "BroSafuan", "Content Strategist" (yellow), white pill CTA.
  Starts right after the last word, holds ≥2.6 s over the frozen last frame (`tpad stop_mode=clone`).
- Audio: voice only (highpass 70, light compressor) + light synth SFX (soft whoosh+pop per card, ding on tick, click on drags,
  soft impact on the end card), `loudnorm I=-14 TP=-1.5`. No music.

## Workflow
1. Footage: Drive folder → `mcp__Google_Drive__search_files` (`parentId = '<id>'`), then download with
   `curl -sSL -o input/footage.mov "https://drive.usercontent.google.com/download?id=<fileId>&export=download&confirm=t"`
   and check the size against `fileSize`. Probe with ffprobe (HDR or SDR, fps).
2. `pip install --break-system-packages -q scipy opencv-python-headless soundfile faster-whisper` (slow, run in background).
3. `python3 .claude/skills/safuan-skill/setup_project.py <name>`, then from `work/<name>/`:
   ```
   ffmpeg -i ../../input/footage.mov -vn -ac 1 -ar 16000 analysis/foot16k.wav
   ASR_PROMPT="BroSafuan, TikTok, <key terms>" python3 scripts/transcribe.py analysis/foot16k.wav analysis/words.json | tee analysis/tx.log
   ffmpeg -i ../../input/footage.mov -vf "fps=30,tpad=stop_mode=clone:stop_duration=2.6" -c:v libx264 -preset medium -crf 16 \
     -pix_fmt yuv420p -g 10 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -an hf/assets/video/main.mp4
   ffmpeg -i ../../input/footage.mov -vn -ac 2 -ar 48000 -af "apad=pad_dur=2.7,atrim=0:<DUR+2.6>" analysis/voice48.wav
   ```
   (HDR source: tone-map to SDR BT.709 first; see `pip-explainer-style/template/scripts/prep_footage.py`.)
4. Edit PER VIDEO in `scripts/build.py`: `SPEECH_END`, `TOTAL` (= footage + 2.6), `END`, the `KEY` regex, the `CARDS` list
   (id, start, end, inner HTML) with their GSAP lines in `extra`, the hook text/duration, the camera `beats`, and the end-card
   texts. In `scripts/audio.py` set the SFX times to match the cards. Fresh card metaphors every video (don't repeat last video's
   pause / tick / STAY / 2× / scrubber cards; try counters, stacks, maps, funnels, photo cards of named people or places).
5. `python3 scripts/audio.py && python3 scripts/build.py`, then in `hf/`:
   `npx --yes hyperframes@0.8.212 lint .` and `check .` (0 errors; `nested_structure_needs_subcomposition` warnings are fine),
   `snapshot . --at <beats> --no-end -o ../qc/snap` and LOOK at the sheets (heads hidden by the strip, captions, wrong words).
6. Render as a background task: `npx --yes hyperframes@0.8.212 render hf --quality standard --fps 30 --sdr -o renders/_raw.mp4`
   (about 15 min for 90 s), mux the exact master (`-map 1:a:0 mix_master.wav`, libx264 crf 18, aac 256k, +faststart) to
   `output/<Name>_9x16.mp4`. QC: ffprobe 1080×1920/30 fps, `ebur128` ≈ −14 LUFS, TP ≤ −1.4. Also make a small preview
   (`scale=540:960 -crf 27`, ~6 MB) when he wants a low-res download. Send with `SendUserFile` (`display: "attach"`).
7. Never commit videos, audio or `work/`.

## Video log
- **Engagement tak nampak** (Nov 2026, 89.6 s): hook "Engagement yang kita tak nampak"; cards PAUSE(1), pause-bubble, tick, STAY,
  SPEED 2×(2), drag timeline, "tunjuk sekejap je". Next video: new card metaphors.
