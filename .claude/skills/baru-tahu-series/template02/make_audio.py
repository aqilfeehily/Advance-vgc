import numpy as np, subprocess, wave
from scipy.signal import butter, lfilter
SR=48000; DUR=58.05
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

for t in [3.12,8.8,14.16,18.64,24.2,32.72,37.92,42.76,45.56,52.16,54.18]: add(t-0.05,whoosh(),0.6)
for t,f in [(0.1,600),(0.95,700),(1.9,760),(3.3,480),(3.5,520),(5.0,420),(8.3,700),(10.0,560),(10.3,600),(10.6,640),(10.9,680),
            (14.3,500),(17.15,560),(20.0,520),(21.0,580),(22.4,640),(33.3,600),(35.1,480),(36.8,420),
            (38.0,520),(38.1,560),(38.2,600),(39.6,600),(40.1,660),(40.6,720),(41.26,800),(41.36,900),(41.46,1000),
            (42.9,480),(47.68,620),(50.45,420),(54.4,560),(54.8,500),(55.05,560)]: add(t,pop(f),0.7)
for t in [25.16,26.2,27.96]: add(t+0.25,thud(),0.8)
add(43.31,thud(),0.9); add(44.9,whoosh(),0.5)
add(18.15,ding(1100),0.6); add(53.2,ding(1760),0.8); add(53.7,pop(400),0.6)
for t in [5.0,7.56]: add(t,boing(),0.45)
for i,t in enumerate([20.95,21.6,22.4,23.2]): add(t,tone(600+60*i,420,0.15,0.06)*0.5,0.6)
for i,t in enumerate([15.27,15.95,16.57,17.3]): add(t,noise_bp(0.35,500,2400,0.15,0.08)*0.5,0.5)
for t in [31.8,31.92,32.04,32.16]: add(t,noise_bp(0.3,800,3000,0.12,0.05)*0.4,0.5)
for t in [36.88,37.1,37.3]: add(t,click(),0.5)
add(49.75,whoosh(),0.5); add(49.7,tone(160,60,0.6,0.3)*0.5,0.7)
add(55.65,click(),1.0); add(55.72,ding(1568),0.6)
add(57.25,pop(450),0.7); add(57.55,pop(520),0.7)
sfx*=0.5
mix=out+sfx*np.max(np.abs(out))*0.9
open("mix_raw.f32","wb").write(mix.astype(np.float32).tobytes())
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","f32le","-ar",str(SR),"-ac","1","-i","mix_raw.f32","-af","loudnorm=I=-14:TP=-1.5:LRA=7,alimiter=limit=0.89","-ar","48000","-ac","2","assets/mix.wav"],check=True)
