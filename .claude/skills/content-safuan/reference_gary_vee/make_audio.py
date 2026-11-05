"""Audio (48 kHz stereo) -> hf/assets/audio/{voice,music,sfx,mix_master}.wav   Run: /usr/bin/python3 scripts/make_audio.py

VOICE : the presenter's own voice from the source .mov (used whole, untrimmed: the user already cut it): high-pass, light
        denoise, mud cut / presence lift, de-ess, gentle compression, loudness-normalised, chain latency compensated.
MUSIC : original instrumental bed synthesised here (no third-party audio, no audio taken from any reference).
        Worked example: 140 BPM half-time trap-pop in D minor (Dm-Bb-F-C): filtered intro, drop on "100% AI", beat-stop
        before "tak boleh", re-entry on "brand trust", lighter groove for chatbot/blueprint, breakdown under the
        no-blueprint question (voice room), build into the end card, final hit and a ringing tail.
        PER VIDEO: change BPM / PROG / T0 and section(); keep the levels and the mix.
SFX   : synthesised whoosh / pop / click / impact / riser / glitch / ding, placed on the same word anchors the picture
        uses (scripts/timing.py), so a timing edit moves the sound too. PER VIDEO: rewrite build_sfx().
"""
import json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from sfx_dsp import SR, rng, lp, hp, place, whoosh, pop, click, impact, riser, glitch, ding, envelope
from edl import SEGS, SRC
from timing import TOTAL, SPEECH_END, END_CARD, S, SEQ, SLAM_T, T

ROOT = os.path.abspath(os.path.join(HERE, ".."))
AUD = os.path.join(ROOT, "hf", "assets", "audio"); os.makedirs(AUD, exist_ok=True)
END = END_CARD
N = int(TOTAL * SR)


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)

def read_wav(p):
    import wave
    w = wave.open(p); n = w.getnframes(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), np.int16).astype(np.float64) / 32768
    return x.reshape(-1, ch).T

def write_wav(p, x):
    import wave
    x = np.clip(x, -1, 1)
    w = wave.open(p, "wb"); w.setnchannels(x.shape[0]); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x.T * 32767).astype(np.int16).tobytes()); w.close()

def envelope_lag(a, b, hop=48, search=200):
    def env(x):
        n = len(x) // hop; e = np.log(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-4); return e - e.mean()
    ea, eb = env(a), env(b); L = min(len(ea), len(eb)) - 2 * search - 10
    best = max(range(-search, search + 1), key=lambda k: np.dot(ea[search + k: search + k + L], eb[search: search + L]))
    return best * hop


# ======================= VOICE =======================
def build_voice():
    raw = os.path.join(AUD, "_voice_raw.wav")
    ff("-i", SRC, "-vn", "-ac", "1", "-ar", str(SR), raw)
    v = read_wav(raw)[0]
    xf = int(0.010 * SR)
    out = np.zeros(0)
    for a, b in SEGS:
        seg = v[int(round(a * SR)): int(round(b * SR))].copy()
        seg[:xf] *= np.linspace(0, 1, xf); seg[-xf:] *= np.linspace(1, 0, xf)
        out = np.concatenate([out, seg])
    cat = os.path.join(AUD, "_voice_cat.wav"); write_wav(cat, out[None, :])
    chain = ("highpass=f=85,afftdn=nr=6:nf=-44,equalizer=f=240:t=q:w=1.1:g=-2,equalizer=f=3200:t=q:w=0.9:g=2.5,"
             "equalizer=f=9500:t=h:w=1:g=1.5,deesser=i=0.3,acompressor=threshold=-20dB:ratio=3:attack=6:release=90:makeup=2,"
             "loudnorm=I=-16:TP=-2:LRA=7")
    dst = os.path.join(AUD, "voice.wav")
    ff("-i", cat, "-af", chain + ",aresample=48000", "-ac", "2", dst)
    x = read_wav(dst)
    lag = envelope_lag(x[0], out)
    if lag > 0: x = np.pad(x[:, lag:], ((0, 0), (0, lag)))
    print("voice chain latency compensated:", round(lag / SR * 1000, 1), "ms")
    if x.shape[1] < N: x = np.pad(x, ((0, 0), (0, N - x.shape[1])))
    x = x[:, :N]
    for f_ in (raw, cat): os.remove(f_)
    write_wav(dst, x)
    return x



# ======================= SFX (restrained; NO music) =======================
def build_sfx():
    """REWRITE per video. One soft cue per visual event (whoosh on a panel, pop on a card, click+ding on a tick,
    impact on a slam), never on every word, never under the last spoken word."""
    fx = np.zeros((2, N))
    P = lambda sig, t, g, pan=0.0: place(fx, sig, t, g, pan)
    P(impact(0.8), 0.0, 0.5)
    for k, a, b, l in SEQ[1:]:
        if l == 1: P(whoosh(0.3, 500, 5000), S[k][0] - 0.12, 0.12)
    for x in SLAM_T[1:]: P(impact(0.5), x, 0.25)
    for x in (T["gary"], T["takNampak"], T["related"], T["dm"]): P(pop(), x, 0.3)
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
