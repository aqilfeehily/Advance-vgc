import cv2, numpy as np, subprocess, sys
W,H=1080,1920; Y0,Y1=1250,1500
def fill(b,m):
    k=(m==0).astype(np.float32); bf=b.astype(np.float32)*k[...,None]
    out=bf.copy(); w=k.copy()
    for sg in (6,14,30):
        num=cv2.GaussianBlur(bf,(0,0),sg); den=cv2.GaussianBlur(k,(0,0),sg)[...,None]
        est=num/np.maximum(den,1e-4)
        hole=(den[...,0]>1e-3)
        if sg==6: res=est
        else: res=np.where((den>0.05),est,res)
    res=np.where(m[...,None]>0,res,b.astype(np.float32))
    soft=cv2.GaussianBlur((m>0).astype(np.float32),(0,0),2)[...,None]
    return np.clip(res*soft+b.astype(np.float32)*(1-soft),0,255).astype(np.uint8)
def clean(f):
    b=f[Y0:Y1]
    m=(b.min(axis=2)>175).astype(np.uint8)*255
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))   # drop specks
    m=cv2.dilate(m,np.ones((9,9),np.uint8),iterations=3)
    f=f.copy(); f[Y0:Y1]=fill(b,m); return f
if sys.argv[1]=='test':
    out=[]
    for t in (2,13,45,60,95):
        r=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i','edit.mov','-frames:v','1','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True).stdout
        f=np.frombuffer(r,np.uint8).reshape(H,W,3); out.append(np.hstack([f[1150:1550],clean(f)[1150:1550]]))
    cv2.imwrite('decap_test.jpg',np.vstack(out)[::1,:])
else:
    rd=subprocess.Popen(['ffmpeg','-v','error','-i','edit.mov','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
    wr=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','30','-i','-','-i','edit.mov','-map','0:v','-map','1:a','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-c:a','copy','clean.mov'],stdin=subprocess.PIPE)
    n=0
    while True:
        r=rd.stdout.read(W*H*3)
        if len(r)<W*H*3: break
        wr.stdin.write(clean(np.frombuffer(r,np.uint8).reshape(H,W,3)).tobytes()); n+=1
    wr.stdin.close(); wr.wait(); print(n)
