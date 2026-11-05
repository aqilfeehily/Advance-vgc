---
name: content-aqil
description: >-
  "Content Aqil": Aqil's one-shot talking-head edit. When he says "content aqil" (optionally with a Google Drive
  folder link or footage in input/), do the whole job without asking: fetch the footage, transcribe, and build +
  render a fast-paced 9:16 PiP Explainer MP4 (TikTok safe zones, hook title at the start, text only, no logo, no
  music), then QC it and send the MP4 for download. Built on pip-explainer-style. Use whenever the user says
  "content aqil", "buat content aqil", or "macam video freelancer tadi", even without a link.
---

# Content Aqil

A saved workflow built from Aqil's first video ("3 ketakutan sebelum jadi freelancer", Nov 2026). It runs the
`pip-explainer-style` engine with Aqil's standing preferences. Reply in casual Malaysian BM (aku/kau).

## Standing rules (Aqil's, do not ask again)
1. **Render straight away.** No storyboard, no "ok" gate, no questions. Aqil trusts the edit. Still state which skill
   files you read and which assumptions you made, in the final note.
2. **Safe zones for TikTok.** Titles at y≈335, every card/diagram/overlay inside y 430–1180, captions at y 1060 (FULL) and
   1250 (PiP). Never in the top ~300 px (For You / Following) or bottom ~400 px (caption, buttons). Covering the face is fine.
3. **Hook title first.** A big hook title (kicker chip + yellow box) is on screen from frame 0, in the middle band.
4. **Text only, no logo.** No company logo or third-party brand, and the end card is text only.
5. **No music.** The voice is the bed. Restrained synth SFX only (one cue per visual event), master −14 LUFS.
6. **Fast pace, same meaning.** Use his voice as is. Switch FULL ↔ PiP on meaning every 2.6–6 s, punch-ins and one slam
   per punchline. Don't cut the footage unless gaps are long (his gaps are usually ≤ 0.5 s, so no cuts). If a word is
   unclear, assume the word that fits his story. Never change what he means; don't invent numbers, prices or testimonials.
7. **Use this session's material only.** Don't copy another video's niche, script, brand or offer. Don't reuse the
   previous video's scene metaphors (see the video log below).

## Required reading (every run; say which ones you read)
`.claude/skills/pip-explainer-style/SKILL.md`, `references/style_spec.md`, `references/scene_playbook.md`,
`references/pipeline.md`, then `.claude/skills/hyperframes/SKILL.md` when building or rendering.
If a file is missing, say so; never assume a skill was loaded.

## Workflow
1. **Get the footage.**
   - Drive folder link: list it with `mcp__Google_Drive__search_files` (`parentId = '<folderId>'`). The MCP download is
     capped at 10 MB, so download big files with the public link:
     `curl -sSL -o input/footage.mov "https://drive.usercontent.google.com/download?id=<fileId>&export=download&confirm=t"`
     and confirm the size matches the Drive metadata (`fileSize`). If the link is private and curl returns HTML, tell him.
   - Otherwise use what is in `input/`. Several clips are fine: probe each, transcribe each, and plan the cuts.
   - Probe with `ffprobe` (size, fps, HDR or SDR, duration). Contact sheet: `fps=0.2,scale=216:384,tile=10x2`.
2. **Environment** (once per container): `pip install --break-system-packages -q scipy opencv-python-headless soundfile faster-whisper`.
   The repo's `python3` is `/usr/local/bin/python3`; `/usr/bin/python3` does not exist here. Do not install `av` again
   (it fails to build); the patched `transcribe.py` reads the wav through soundfile instead.
3. **Project.** `python3 .claude/skills/content-aqil/setup_project.py <name>` copies the PiP template to `work/<name>/` and
   applies the safe-zone, transcribe, end-tail and no-music patches. Then, from `work/<name>/`:
   ```
   ffmpeg -i ../../input/footage.mov -vn -ac 1 -ar 16000 analysis/foot16k.wav        # mkdir analysis qc first
   python3 scripts/transcribe.py analysis/foot16k.wav analysis/words.json            # large-v3, ~2 min on CPU
   export SRC_MOV=<abs path to footage> SRC_DUR=<seconds>
   python3 scripts/edl.py && python3 scripts/prep_footage.py main                     # ~4 min, writes a 220 MB main.mp4
   ```
   Voice only (no speech) or several shots: skip the presenter layout, plan visuals from the shots, never invent a presenter.
4. **Write the per-video files** (the template ones are the Bisnes Baru example, replace them):
   - `timing.py`: define `SEQ = [(name, start, end, layout 0=FULL/1=PiP), ...]`, then `S`, `LAYOUT`, `PANEL_CUTS`, `PUNCH`,
     `SHAKES`, `FLASHES`, `END_CARD`, and `T = {}` (build.py imports it). Anchors are Whisper word starts.
   - `captions.py`: `FIX`/`JOIN` (standard BM spelling; "kadang -kadang" → "kadang-kadang"), `KEY` regex for yellow keywords.
   - `scenes.py`: one scene per idea built from kit pieces (title, big_card, rows, pair, bars, counters), the FULL slams
     and the text-only end card (`fit()` the line). Visualise the sentence being said.
   - `make_audio.py` `build_sfx()` cues, then `python3 scripts/make_audio.py`.
5. **Check.** `python3 scripts/build.py`, then in `hf/`: `npx --yes hyperframes lint .` and `check .` (0 errors; `line_unread`
   warnings are expected). `snapshot . --at <every beat> --no-end -o ../qc/snap`, then LOOK at the contact sheets: overflow past
   960 px, empty panels, anything outside the safe zone. Fix, rebuild.
6. **Render** (about 12 min for 99 s on 4 cores). It must run as a real background task or it dies with the shell:
   Bash with `run_in_background: true` and `npx --yes hyperframes render hf --quality standard --fps 30 --sdr -o renders/_raw.mp4`.
   Don't poll in a loop; you are notified when it ends. Then mux the exact audio master:
   `ffmpeg -i renders/_raw.mp4 -i hf/assets/audio/mix_master.wav -map 0:v:0 -map 1:a:0 -vf format=yuv420p -c:v libx264 -profile:v high
   -preset medium -crf 18 -r 30 -g 60 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -c:a aac -b:a 256k
   -ar 48000 -ac 2 -shortest -movflags +faststart output/<Name>_9x16.mp4` (`finish.sh` needs zsh, which is not installed).
7. **QC then deliver.** `ffprobe` (1080×1920, 30 fps, duration); `ebur128` ≈ −14 LUFS, peak ≤ −1.5 dBTP (a lower peak is fine);
   audio lag vs the source ≈ 0 ms (cross-correlation); re-transcribe the last ~10 s so nothing masks the last word; end card ≥ 2 s.
   Send the file with `SendUserFile` (`display: "attach"`) and write a short BM note: skills read, assets used, every assumption.
   Append the video to the log below. Never commit videos, audio or `work/`.

## Video log
- **Freelancer, 3 ketakutan** (Nov 2026, 99 s): hook = "3 KETAKUTAN" yellow box + kicker chip → 0→3 counter + 3 "?" cards.
  Scenes: bill→komitmen pair, tick rows (gaji/skills/rehat/langkah), 3–5 hari vs 1 bulan bars, 8 pagi→5 petang timeline,
  usaha→rajin pair, subuh/malam cards, "takut itu guru" pair, makan gaji vs kerja sendiri CTA. End card "BUKAN TAK MAMPU / TAKUT JE".
  Next video: pick different metaphors (e.g. counters, stacks, maps, funnels) instead of repeating the tick-row / pair layout.
- **Cara buat konten guna AI** (Nov 2026, 75 s): hook = kicker "CARA AKU BUAT KONTEN" + kotak kuning "GUNA AI". Scenes: garis jagged→smooth,
  idea→ChatGPT chat, blok berselerak tersusun / bar skrip mengecut / kad HOOK, skrip→CapCut editor, telefon teleprompter + stamp,
  prompt bar bertaip + kad animation/visual, ring timer 30 min→1 jam + slider, pipeline 5 nod + titik bergerak, 5 kad video + sweep + tick,
  repost cycle + story, butang FOLLOW. End card "IDEA SENDIRI / AI BANTU". Next: elak ring timer, pipeline dan stack kad ini.
