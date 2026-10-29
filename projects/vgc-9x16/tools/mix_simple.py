import subprocess, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T=100.4
lifts=[5.2,12.06,18.43,24.13,30.4,38.5,44.0,50.4,53.4,57.6,63.0,70.0,75.5,84.1,87.4,91.4]
pops=[0.4,5.55,12.45,27.15,38.85,44.15,45.7,47.35,50.75,53.65,58.35,61.6,63.3,66.95,76.75,78.45,84.45,91.65]
ev=[('lift.wav',t-0.3,1.0) for t in lifts]+[('pop.wav',t,0.6) for t in pops]
ev+=[('wind.wav',5.2,0.35)]   # one soft bed for the "masalah" beat only
ins=['-i','work/vo.wav']; fc=['[0:a]apad=whole_dur=%s,atrim=0:%s[vo]'%(T,T)]
sx=[]
for i,(f,t,g) in enumerate(ev):
    ins+=['-i','work/sfx/'+f]; d=int(max(0,t)*1000)
    fc.append(f'[{i+1}:a]volume={g},adelay={d}|{d}[s{i}]'); sx.append(f'[s{i}]')
fc.append(''.join(sx)+f'amix=inputs={len(sx)}:normalize=0,volume=-12dB,apad=whole_dur={T},atrim=0:{T}[sfx]')
fc.append(f'[vo][sfx]amix=inputs=2:normalize=0,afade=t=out:st={T-0.5}:d=0.5,alimiter=limit=0.89:level=disabled[m]')
subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',';'.join(fc),'-map','[m]','-ar','48000','-ac','2','-c:a','aac','-b:a','224k','assets/audio_mix.m4a'],check=True)
print('ok')
