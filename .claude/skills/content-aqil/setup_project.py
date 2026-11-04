#!/usr/bin/env python3
"""content-aqil: copy the PiP Explainer template into work/<name>/ and apply Aqil's standing patches.

  python3 .claude/skills/content-aqil/setup_project.py <name>

Patches (all idempotent, applied to the COPY only; the skill template is never touched):
  1. kit.py        : TikTok safe zone (title y 335, captions 1060 FULL / 1250 PiP, slams y 1235)
  2. transcribe.py : read the wav with soundfile (faster-whisper's `av` decoder breaks on newer PyAV)
  3. edl.py        : end-card tail 2.6 s (the closing line must be on screen >= 2 s)
  4. make_audio.py : NO music. Voice + restrained SFX only (the SFX cue list is a stub: rewrite build_sfx() per video)
"""
import os, shutil, sys

if len(sys.argv) != 2:
    sys.exit(__doc__)
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC = os.path.join(REPO, ".claude", "skills", "pip-explainer-style", "template")
DST = os.path.join(REPO, "work", sys.argv[1])
if os.path.exists(DST):
    sys.exit(f"{DST} already exists: pick another name or remove it first")
shutil.copytree(SRC, DST)


def patch(rel, pairs):
    p = os.path.join(DST, rel)
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        if a not in s:
            sys.exit(f"patch failed in {rel}: {a!r} not found (template changed?)")
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8").write(s)


patch("scripts/kit.py", [
    ("CAP_Y = dict(full=1210, pip=1296)", "CAP_Y = dict(full=1060, pip=1250)"),
    ("SLAM_Y = 1440", "SLAM_Y = 1235"),
    ("def title(id_, text, y=205, size=66", "def title(id_, text, y=335, size=66"),
])
patch("scripts/transcribe.py", [
    ("src, out = sys.argv[1], sys.argv[2]",
     'src, out = sys.argv[1], sys.argv[2]\nimport soundfile as sf\nsrc, _sr = sf.read(src, dtype="float32")'),
])
patch("scripts/edl.py", [("TAIL = 2.0", "TAIL = 2.6")])

# no-music make_audio: keep the voice chain, drop the synth bed
p = os.path.join(DST, "scripts", "make_audio.py")
s = open(p, encoding="utf-8").read()
head = s[:s.index("# ======================= MUSIC")].replace(
    "from timing import T, TOTAL, SPEECH_END, END_CARD", "from timing import TOTAL, SPEECH_END, END_CARD, S")
tail = '''
# ======================= SFX (restrained; NO music) =======================
def build_sfx():
    """REWRITE per video. One soft cue per visual event (whoosh on a panel, pop on a card, click+ding on a tick,
    impact on a slam), never on every word, never under the last spoken word."""
    fx = np.zeros((2, N))
    P = lambda sig, t, g, pan=0.0: place(fx, sig, t, g, pan)
    P(impact(0.8), 0.0, 0.5)
    for k, (a, b) in S.items():
        if k not in ("hookF",): P(whoosh(0.3, 500, 5000), a - 0.12, 0.12)
    P(impact(1.4), END_CARD, 0.65)
    return fx


if __name__ == "__main__":
    voice = build_voice()
    sfx = build_sfx()
    env = envelope(voice)
    act = np.clip(env / (np.percentile(env[env > 1e-4], 60) + 1e-9), 0, 1)
    duck_s = 10 ** (-3 * act / 20)
    sfx_n = sfx / (np.abs(sfx).max() + 1e-9)
    write_wav(os.path.join(AUD, "sfx.wav"), sfx_n * 0.9)
    mix = voice + sfx_n * duck_s * 0.32
    pre = os.path.join(AUD, "_mix_pre.wav"); write_wav(pre, mix)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(r[r.rindex("{"): r.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:linear=true:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']},alimiter=limit=0.84:level=false,aresample=48000")
    ff("-i", pre, "-af", af, "-ar", "48000", os.path.join(AUD, "mix_master.wav"))
    os.remove(pre)
    print("ok", {k: js[k] for k in ("input_i", "input_tp")})
'''
open(p, "w", encoding="utf-8").write(head + tail)
# timing.py needs a T dict for build.py's import; the worked-example timing/captions/scenes are replaced per video
print("project ready:", DST)
print("NEXT: write scripts/timing.py (SEQ/S/LAYOUT/PUNCH...), captions.py, scenes.py for this video; see .claude/skills/content-aqil/SKILL.md")
