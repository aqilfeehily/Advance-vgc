---
name: content-safuan
description: "Content Safuan": Aqil's one-shot talking-head edit for the owner BroSafuan. When he says "content safuan" (optionally with a Google Drive folder link or footage in input/), do the whole job without asking, exactly like content-aqil, but the video owner is BroSafuan and his photo is the end-card logo. Use whenever the user says "content safuan", "buat content safuan", or "macam video Gary Vee tadi".
---

# Content Safuan

Same engine and workflow as `content-aqil` (read `.claude/skills/content-aqil/SKILL.md` and follow it fully: fetch Drive footage, transcribe,
build with `pip-explainer-style`, render, mux, QC, send the MP4). Reply in casual Malaysian BM (aku/kau). Render straight away, no questions
(only stop if the skill files or the Drive link cannot be read).

## Overrides (Aqil's standing rules for this trigger)
1. **Owner = BroSafuan.** Whenever the speaker introduces themself ("Hai saya …", Whisper may hear "Bruce Afan"), the caption and any
   on-screen name is **BroSafuan** (one word, that capitalisation). Put it in `FIX`, e.g. {"bruce": "BroSafuan", "afan": ""}, and
   remove "Bruce" from `UNCLEAR`. Never write "Bruce Afan".
2. **Logo = BroSafuan's photo.** The end card shows the circular photo `assets/brosafuan_logo_circle.png` (300 px circle, white 4 px
   border, cyan glow, at y≈1040). Copy it to `hf/assets/img/logo_icon.png`. If he sends a new photo, replace both files here.
   The source is `assets/brosafuan_logo_source.jpg`. Never use another brand or logo.
3. **Named people.** Keep the spelling he gives (e.g. "Gary Vee"). If a famous person is mentioned, animate **only that person's photo**
   (public-domain/Wikimedia Commons, labelled "Foto: Wikimedia Commons (public domain)"); the speaker's own clips stay as they are.
4. **Everything else = content-aqil**: TikTok safe zones, hook title from frame 0, text only (the photo logo at the end is the one
   exception), no music, restrained SFX, −14 LUFS, FULL↔PiP on meaning, don't invent numbers/prices/testimonials, unclear words get "…".
5. Pick fresh scene metaphors each video. Reference build: `reference_gary_vee/` (timing.py, captions.py, scenes.py, make_audio.py:
   feed rows, strike-through term card, photo card with Ken Burns, KITA→DIA arrow, orbiting icons, typing search bar + tiles, training rows).
   Reuse the pieces, not the choreography.

## Video log
- **Gary Vee / Interest Media** (Nov 2026, 65.7 s, owner line was captioned "Hai saya…" because the name was unclear; it is BroSafuan).
