---
name: baru-tahu-series
description: >-
  "Baru Tahu" series: the user's locked style for 9:16 TikTok "fakta menarik" cartoon explainers on a supplied
  ElevenLabs VO (first video: "Tingkap Kapal Terbang Bujur", Nov 2026). Flat cartoon, thick #141414 outlines,
  sunburst backgrounds, an original Malaysian mascot (songkok + teal baju Melayu + red sampin), big Archivo Black
  keyword captions, one visual metaphor per sentence. Use whenever the user says "Baru Tahu", "series Baru Tahu",
  "macam video tingkap tu", "style TheOdd1sOut", or gives a new short fact VO to edit in this cartoon look.
  Built with HyperFrames; no music, light SFX.
---

# Baru Tahu (series)

Channel/handle: **Baru Tahu** (text only, no logo file). The VO ends with "Follow untuk lebih banyak fakta menarik dalam Baru Tahu".
Video 01: `work/baru-tahu-01-tingkap/` (VO 50.9 s, Bahasa Melayu Gen-Z narrator "Ashraf", ElevenLabs). Draft approved by the user as final ("preview dah cukup").

## Brief the user locked
- **Format:** 9:16 TikTok, 1080x1920, 30 fps. **Text only** brand, **no background music**, **captions yes**.
- **Look:** reference was TheOdd1sOut ("Animation Before Computers"). I could not download it (YouTube bot block), so the look is from its thumbnail + knowledge: flat colours, thick black outlines, expressive big-eyed blob, comic zoom/squash, pop SFX. Mascot is **original** (never copy TheOdd1sOut's character).
- **Facts:** never add facts, names or numbers that are not in the VO.
- Talk to the user in casual Bahasa Melayu. Show the storyboard first, ask before render. The user usually wants a **draft render** (`--quality draft`) for review; only render `delivery` when they say "final".

## Locked identity
| Layer | Rule |
|---|---|
| Mascot | Head ellipse skin `#e0a469`, black songkok with gold band, teal `#19a39a` baju Melayu, red `#d63a2b` sampin with gold line, big white eyes with movable pupils, brows, 5 mouths (smile/grin/open/worry/flat). Defined as `mascot()` in `build.py`; hand = `hand()`; bulb/shield/stars/clouds are reusable |
| Strokes | `#141414`, width 10, round caps/joins |
| Backgrounds | One flat colour or sunburst `rays()` per scene, colour changes every scene (yellow, coral, sky blue, mint, teal, cream, sepia, navy). Navy = danger/stress, green = solved |
| Captions | Archivo Black 92 px, white, `-webkit-text-stroke:16px #141414; paint-order:stroke fill`, keyword `#ffd400` (written in CAPS in `CAPS`), 1-3 words per chunk, pop-in with small tilt, box `top:1290 left:90 width:900`. Keep art out of y 1290-1550; TikTok UI covers the top ~200 px and the bottom ~370 px |
| Motion | Scene changes: lift (y), slide-left (x) or circle clip-path wipe, 0.3 s, landing on the first word. Mascot pops with back-ease, gentle bob, pupils look at the subject, brows/mouth change per beat. Windows/icons draw on with stroke-dashoffset (`pathLength=1`). Camera zoom/shake only on the key beat |
| Audio | VO only + synthesised soft SFX (`make_audio.py`): whoosh per scene change, pops, thud on X slam, ding on shield/check, crack ticks, click on Follow. Mix normalised to **-14 LUFS**, TP -1.5 (video 01 measured -14.2 LUFS, peak -3.5 dBFS) |
| Structure | Beat per sentence. Hook: mascot reacts + "?" popups. Middle: one metaphor per sentence (compare, cross out, shield, arrows, crack, green flow arrows, check). Then "Menarik kan?" thumbs-up, recap, bulb "dah tahu", CTA: Follow button tapped by a hand, then big BARU TAHU slam on the last words |

## Workflow (what worked, ~1 session)
1. `npx hyperframes transcribe vo.mp3 -m small -l ms --json` (whisper `small`, language `ms`). Then fix Malay mis-hearings by hand ("peta"->petak, "melengkong"->melengkung, "Rukunya"->Rumusnya, "diri ke"->direka). Word times were good enough; no envelope snapping needed for this VO.
2. Write the beat table (time | words | visual) and show it. Ask: format, brand text/logo, mascot, captions, music. Wait for answers.
3. Copy `template/` to `work/baru-tahu-NN-<topic>/`, put the VO at `vo.mp3`, `assets/`. Rewrite: scene functions in `patch_scenes.py` (+ `build.py` base scenes), `CAPS`/`SC` in `build.py`, timings in `anim.js`, SFX events in `make_audio.py`. Do **not** reuse the previous video's metaphors (break pattern): new topic = new drawings, same identity.
4. `python3 scripts/make_audio.py` (needs numpy+scipy: `pip install numpy scipy`) then `python3 scripts/build.py` -> `index.html`.
5. `npx hyperframes check` must be 0 errors; `npx hyperframes snapshot --at ... -o <scratch dir>` and look at the contact sheets. Fix art overlapping the caption zone first.
6. `npx hyperframes render --quality draft --fps 30 -o ../../output/baru-tahu-NN-<topic>_9x16_draft.mp4` (~1.5 min for 51 s). Verify with ffprobe.

## Gotchas learned
- `mascotIn()` must tween `x:0` too if the `from` offsets x.
- Use `transformOrigin:"50% 50%"` for scaling a group; `svgOrigin` is global coords, so avoid it on elements inside translated wrappers. Do not put a `transform` attribute on an element GSAP also animates; wrap it in a `<g>`.
- Two `fromTo` on the same target need `immediateRender:false` on the later one.
- Caption chunk ends = next start - 0.04 so they never overlap.
- Closing line must stay on screen >= 2 s (lint `line_unread`): show BARU TAHU from ~47.7 s and only pulse it on the last words.
- Audio element duration must not exceed the file (VO 50.88 s).
- `check` warns about one big file / dense track (single-file build); accepted, 0 errors.
- Bundled font Archivo Black works by name; no `@font-face` needed.
- `work/` and `output/` videos are git-ignored; this skill's `template/` is the only copy of the build scripts that survives.

## Video 02 additions ("Kenapa wanita nampak lebih emosional", VO 58 s, female narrator)
- New **second character "Kak"** (original): pink tudung bawal `#ff6f91`, purple baju kurung `#7a4bc7`, skin `#ecb98a`, eyelashes, yellow flower pin. `kak()` in `template02/project.py`, same ids as `mascot()` (so `look/mouth/brows/mascotIn` work). `mascot_var()` recolours the mascot for crowd scenes. Maskot lama (songkok) stays as presenter for hook/bulb/CTA.
- New metaphors used (do not repeat in later videos): balance scale, 4 "?" cards, hormone dial + calendar loop, mood/battery/heart gauges, stacked weights squashing Kak, weather icon over mascot, three coping bubbles, crossed-out label card, iceberg ("TEKANAN" hidden below water).
- Tone rule the user approved: sensitive topics show stress/tiredness, never a woman shouting; "angry" only as a small face at the iceberg tip.
- `template02/` is a **project-structure refactor**: `build.py` (helpers + `exec(project.py)`), `project.py` (SC, TOTAL, scenes, CAPS, ENDS for one video), `anim_head.js` (helpers + captions + ENTER list) + `anim_body.js` (per-scene timeline), `make_audio.py` (SFX events). For video N: copy `template02/` to `work/baru-tahu-NN/scripts/`, rewrite `project.py` + `anim_body.js` + events, `cat anim_head.js anim_body.js > anim.js`, then build. `patch_scenes.py` (from `template/scripts`) is still needed (cloud/plane helpers); copy it too.
- Hold ~0.04 s gaps between caption chunks; stack-weight offsets must be equal for all stacked items at each moment or they overlap.
