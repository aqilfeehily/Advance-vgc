import numpy as np, subprocess, wave
from scipy.signal import butter, lfilter
SR=48000; DUR=55.55
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


for t in [3.48,6.36,11.6,21.28,33.4,42.4,49.32,51.36]: add(t-0.05,whoosh(),0.6)
for i in range(6): add(2.82+i*0.1,click(),0.6)
for t,f in [(0.1,600),(1.0,700),(1.9,760),(3.6,480),(4.14,560),(4.51,620),(4.9,680),(5.3,500),(5.83,740),
            (12.0,520),(14.36,420),(16.1,480),(33.9,520),(36.4,580),(37.6,640),(42.5,520),(43.5,600),(47.8,560),(52.0,500),(52.25,560),(51.55,560),(54.4,450),(54.6,520)]: add(t,pop(f),0.7)
add(6.0,thud(),0.9); add(14.36,thud(),0.7)
for t in [9.6,10.15,10.7]:
    for k in range(5): add(t+k*0.16,click(),0.6)
add(11.0,ding(1500),0.6)
for i in range(6): add(17.4+i*0.5,pop(520+30*i),0.5)
for i in range(6): add(20.76+i*0.05,click(),0.6)
for t in [22.0,22.55,23.1,23.7,24.3,24.9,25.5,26.1,26.7,29.85,30.2,30.5,30.75,30.95,31.1,31.22,31.32,31.5,31.58]: add(t+0.06,click(),0.8)
add(31.76,thud(),1.0); add(31.76,crack(),0.8); add(31.9,boing(),0.4)
for i in range(6): add(38.58+i*0.07,click(),0.4)
for c in range(3): add(40.06+c*0.2,ding(1200+150*c),0.5)
for i in range(8): add(45.2+i*0.28+0.2,whoosh(),0.35)
add(47.85,tone(300,900,1.1,0.9)*0.5,0.7); add(48.9,ding(1500),0.8)
add(50.2,ding(1760),0.8); add(50.64,pop(400),0.6)
add(52.75,click(),1.0); add(52.87,ding(1568),0.6)
sfx*=0.5
mix=out+sfx*np.max(np.abs(out))*0.9
open("mix_raw.f32","wb").write(mix.astype(np.float32).tobytes())
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","f32le","-ar",str(SR),"-ac","1","-i","mix_raw.f32","-af","loudnorm=I=-14:TP=-1.5:LRA=7,alimiter=limit=0.89","-ar","48000","-ac","2","assets/mix.wav"],check=True)
