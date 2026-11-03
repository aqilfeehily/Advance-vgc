import numpy as np, cv2, subprocess
W,H=1080,1920; R=6                                                    # +-6 frames (0.2 s)
K=lambda n:np.ones((n,n),np.uint8)
rd_a=subprocess.Popen(['ffmpeg','-v','error','-i','alpha_refined3b.mkv','-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE)
rd_c=subprocess.Popen(['ffmpeg','-v','error','-i','clean2.mov','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
wr=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','gray','-s',f'{W}x{H}','-r','30','-i','-','-c:v','ffv1','alpha_stab.mkv'],stdin=subprocess.PIPE)
A=[];C=[];out_i=0
def frames():
    while True:
        a=rd_a.stdout.read(W*H); c=rd_c.stdout.read(W*H*3)
        if len(a)<W*H or len(c)<W*H*3: return
        yield np.frombuffer(a,np.uint8).reshape(H,W),np.frombuffer(c,np.uint8).reshape(H,W,3)
def fix(cur,rgb,win):
    wmax=np.max(win,axis=0)
    hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV); hh=hsv[...,0].astype(np.float32)*2; ss=hsv[...,1]/255.; vv=hsv[...,2]/255.
    body=((hh<=26)&(ss>0.22)&(vv>=0.24))|(vv<0.24)                      # skin or dark (hair, jacket): never wall
    wood=(hh>26)&(hh<44)&(ss>0.38)&(vv>0.52)
    solid=cv2.erode((wmax>230).astype(np.uint8),K(5))>0                  # was solidly part of the body a moment ago
    fill=solid&body&~wood&(cur<200)
    o=np.where(fill,np.maximum(cur,(wmax*0.97).astype(np.uint8)),cur)
    if fill.any():
        o=cv2.GaussianBlur(o,(0,0),1.0)
    return o
from collections import deque
buf=deque(); idx=0; emitted=0
def emit(center_pos):
    win=np.stack([b[0] for b in buf]); cur,rgb=buf[center_pos]
    wr.stdin.write(fix(cur,rgb,win).tobytes())
for a,c in frames():
    buf.append((a,c)); idx+=1
    if len(buf)>2*R+1: buf.popleft()
    if idx>R:                                   # centre frame (idx-1-R) has R future frames
        emit(len(buf)-1-R if idx>=2*R+1 else idx-1-R); emitted+=1
# flush the last R frames with truncated windows
for k in range(R):
    pos=len(buf)-R+k
    if pos<0: continue
    emit(pos); emitted+=1
wr.stdin.close(); wr.wait(); print('frames',emitted)
