import numpy as np, subprocess
from refine3b import refine, W, H
rd_rgb=subprocess.Popen(['ffmpeg','-v','error','-i','clean2.mov','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
rd_a=subprocess.Popen(['ffmpeg','-v','error','-c:v','libvpx-vp9','-i','matte_raw.webm','-vf','format=yuva420p,alphaextract,format=gray','-f','rawvideo','-'],stdout=subprocess.PIPE)
wr=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','gray','-s',f'{W}x{H}','-r','30','-i','-','-c:v','ffv1','alpha_refined3b.mkv'],stdin=subprocess.PIPE)
buf=[];n=0
def emit():
    if len(buf)==3: o=0.25*buf[0]+0.5*buf[1]+0.25*buf[2]
    else: o=buf[-1]
    wr.stdin.write(np.clip(o,0,255).astype(np.uint8).tobytes())
while True:
    r=rd_rgb.stdout.read(W*H*3); a=rd_a.stdout.read(W*H)
    if len(r)<W*H*3 or len(a)<W*H: break
    buf.append(refine(np.frombuffer(a,np.uint8).reshape(H,W),np.frombuffer(r,np.uint8).reshape(H,W,3)).astype(np.float32)); n+=1
    if len(buf)>3: buf.pop(0)
    if n==1: wr.stdin.write(buf[0].astype(np.uint8).tobytes())
    elif n>=3: emit()
# tail: last two frames
wr.stdin.write(buf[-1].astype(np.uint8).tobytes()); wr.stdin.write(buf[-1].astype(np.uint8).tobytes())
wr.stdin.close(); wr.wait(); print('frames',n)
