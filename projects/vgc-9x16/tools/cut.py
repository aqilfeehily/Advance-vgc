import numpy as np, subprocess, json
SR=16000
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','work/src30.mp4','-ac','1','-ar',str(SR),'-f','s16le','-'],capture_output=True).stdout,dtype=np.int16).astype(float)
def snap(t,r=0.14):
    # dip in 10 ms RMS within +-r of t
    w=int(.01*SR); lo=int((t-r)*SR); hi=int((t+r)*SR)
    best=None
    for i in range(lo,hi,w//2):
        e=np.sqrt(np.mean(a[i:i+w]**2))
        if best is None or e<best[0]: best=(e,i/SR)
    return best[1]
# cuts (remove [s,e)) from word times; meaning kept
cuts=[(27.52,28.31),(41.49,44.49),(66.76,67.96),(92.24,94.44)]
END=107.05
keep=[];cur=0.0
for s,e in cuts:
    s2,e2=snap(s),snap(e); keep.append((cur,s2)); cur=e2
keep.append((cur,snap(END,0.2)))
tm=[];t=0
for s,e in keep:
    tm.append((s,e,t)); t+=e-s
json.dump(tm,open('work/timemap.json','w'))
print(tm,t)
v=''.join(f"[0:v]trim={s:.3f}:{e:.3f},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e-s-0.02:.3f}:d=0.02[a{i}];" for i,(s,e) in enumerate(keep))
v+=''.join(f"[v{i}][a{i}]" for i in range(len(keep)))+f"concat=n={len(keep)}:v=1:a=1[v][a]"
subprocess.run(['ffmpeg','-v','error','-y','-i','work/src30.mp4','-filter_complex',v,'-map','[v]','-map','[a]','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-r','30','-c:a','pcm_s16le','work/edit.mov'],check=True)
