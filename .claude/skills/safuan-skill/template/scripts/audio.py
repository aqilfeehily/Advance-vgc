import numpy as np, soundfile as sf, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sfx_dsp import place, pop, whoosh, ding, click, impact
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
v, sr = sf.read(f"{ROOT}/analysis/voice48.wav", dtype="float64"); assert sr == 48000
N = len(v); fx = np.zeros((2, N))
P = lambda sig, t, g, pan=0.0: place(fx, sig, t, g, pan)
for t in (2.05, 8.35, 14.8, 22.7, 43.4, 66.0):
    P(whoosh(0.28, 500, 4500), t - 0.02, 0.10)
    P(pop(900, 0.09), t + 0.2, 0.12)
P(ding(1320), 12.55, 0.12)
P(click(), 15.1, 0.08); P(click(), 17.0, 0.08)
P(click(), 43.7, 0.07); P(click(), 69.6, 0.09)
P(pop(700, 0.09), 0.05, 0.12)
P(impact(1.0), 86.95, 0.22)
mix = v.T.copy() if v.shape[1] == 2 else np.vstack([v, v])
mix = mix[:, :N] + fx[:, :N]
sf.write(f"{ROOT}/analysis/mix_pre.wav", mix.T, sr)
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{ROOT}/analysis/mix_pre.wav","-af",
  "highpass=f=70,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=140,loudnorm=I=-14:TP=-1.5:LRA=9",
  "-ar","48000",f"{ROOT}/hf/assets/audio/mix_master.wav"],check=True)
print("audio ok")
