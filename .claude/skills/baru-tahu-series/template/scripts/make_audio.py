import numpy as np, subprocess, wave
from scipy.signal import butter, lfilter
SR=48000; DUR=51.0
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","vo.mp3","-ar",str(SR),"-ac","1","-f","f32le","vo_raw.f32"],check=True)
vo=np.fromfile("vo_raw.f32",dtype=np.float32)
out=np.zeros(int(SR*DUR),dtype=np.float32); out[:len(vo)]+=vo[:len(out)]
sfx=np.zeros_like(out)
rng=np.random.default_rng(7)
def add(t,x,g=1.0):
    i=int(t*SR); x=x[:len(sfx)-i]; sfx[i:i+len(x)]+=g*x
def env(n,a=0.005,d=0.1):
    t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def tone(f0,f1,dur,d=0.08,wave_='sin'):
    n=int(dur*SR); t=np.arange(n)/SR; f=f0+(f1-f0)*t/dur; ph=2*np.pi*np.cumsum(f)/SR
    s=np.sin(ph) if wave_=='sin' else np.sign(np.sin(ph))*0.5
    return s*env(n,0.003,d)
def noise_bp(dur,lo,hi,d=0.15,a=0.02):
    n=int(dur*SR); x=rng.standard_normal(n); b,aa=butter(2,[lo/(SR/2),hi/(SR/2)],'band'); return lfilter(b,aa,x)*env(n,a,d)
def pop(f=520): return tone(f,f*0.5,0.12,0.04)*0.5
def whoosh(): return noise_bp(0.32,400,3500,0.12,0.12)*0.5
def ding(f=1320): return (tone(f,f,0.5,0.18)+0.4*tone(f*2,f*2,0.5,0.12))*0.35
def boing(): return tone(220,520,0.25,0.12)*0.45
def thud(): return (tone(120,45,0.25,0.1)+noise_bp(0.25,200,1200,0.04))*0.7
def click(): return noise_bp(0.05,2500,7000,0.015,0.001)*0.7
def crack(): return noise_bp(0.18,1500,6000,0.05,0.001)*0.8
for t in [2.72,7.0,14.45,20.4,30.35,38.5,39.5,45.3,47.2]: add(t-0.05,whoosh(),0.6)
for t,f in [(0.1,600),(0.95,700),(1.9,760),(3.0,480),(5.95,420),(7.15,560),(10.0,800),(10.16,900),(10.32,1000),(10.48,1100),(38.6,500),(38.85,900),(38.93,1000),(39.01,1100),(47.5,620),(47.7,520),(47.95,580)]: add(t,pop(f),0.7)
add(6.66,thud(),0.9); add(6.8,ding(1100),0.6)
add(12.04,ding(1480),0.9); add(43.9,ding(1480),0.9); add(37.85,ding(1180),0.8)
add(11.15,boing(),0.6); add(5.6,boing(),0.4); add(33.9,boing(),0.4)
for i,t in enumerate([21.56,21.78,22.0,22.22]): add(t,pop(380+40*i),0.6)
for i,t in enumerate([23.85,23.97,24.09,24.21]): add(t,tone(700,300,0.18,0.07)*0.5,0.7)
for t in np.linspace(26.4,28.6,9): add(t,crack(),0.35+0.04*(t-26.4))
add(28.06,thud(),1.0); add(28.95,whoosh(),0.5)
for i,t in enumerate([35.42,35.72,36.02,36.32]): add(t,noise_bp(0.4,600,2600,0.18,0.1)*0.45,0.6)
for i in range(6): add(18.95+i*0.22,click(),0.6)
add(46.35,ding(1760),0.8); add(46.8,pop(400),0.6)
add(49.05,click(),1.0); add(49.12,ding(1568),0.6)
add(50.23,pop(450),0.7); add(50.55,pop(520),0.7)
# duck sfx a bit under VO is unnecessary: sfx are short and quiet
sfx*=0.5
mix=out+sfx*np.max(np.abs(out))*0.9
open("mix_raw.f32","wb").write(mix.astype(np.float32).tobytes())
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","f32le","-ar",str(SR),"-ac","1","-i","mix_raw.f32","-af","loudnorm=I=-14:TP=-1.5:LRA=7,alimiter=limit=0.89","-ar","48000","-ac","2","assets/mix.wav"],check=True)
