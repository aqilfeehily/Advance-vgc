import numpy as np, cv2, subprocess
W,H=1080,1920
K=lambda n:np.ones((n,n),np.uint8)
def refine(a,rgb):
    a0=a.astype(np.float32)/255
    hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV); hh=hsv[...,0].astype(np.float32)*2; ss=hsv[...,1]/255.; vv=hsv[...,2]/255.
    core=cv2.erode((a0>0.995).astype(np.uint8),K(31))>0                       # solid body core: glasses frames, face, never touched
    wood=(hh>26)&(hh<44)&(ss>0.38)&(vv>0.52)                                    # warm wall panel (skin is hue 12-24)
    wood=cv2.morphologyEx(wood.astype(np.uint8),cv2.MORPH_CLOSE,K(5))>0
    dark=vv<0.24
    skin=(hh<=26)&(ss>0.22)&(vv>=0.24)
    sharp=np.clip((a0-0.90)/0.09,0,1); sharp=sharp*sharp*(3-2*sharp)
    f=np.where(skin|dark,a0,sharp)                                              # skin keeps its motion-blur alpha; everything else must be solid
    ws=cv2.GaussianBlur(wood.astype(np.float32),(0,0),4)
    ws=np.clip(ws*1.6,0,1)
    f=np.where(skin&~dark,np.clip(a0*1.5,0,1),f)                               # motion-blurred hands: denser, not shredded
    big=cv2.morphologyEx(wood.astype(np.uint8),cv2.MORPH_OPEN,K(13))        # large wall areas only (glasses frames / fingers are thin)
    wb=np.clip(cv2.GaussianBlur(cv2.dilate(big,K(5)).astype(np.float32),(0,0),3)*1.4,0,1)
    f=f*(1-ws*(~core))*(1-wb)
    f=np.maximum(f,cv2.morphologyEx(f,cv2.MORPH_CLOSE,K(9))*0.9*(~wood))     # close pin-holes inside hands
    m=(f>0.5).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,K(7))
    n,lab,st,_=cv2.connectedComponentsWithStats(m,connectivity=8)
    keep=np.zeros(n,bool); keep[1:]=st[1:,cv2.CC_STAT_AREA]>8000
    m=keep[lab].astype(np.uint8)
    near=cv2.dilate(m,K(21)).astype(np.float32)
    body=cv2.dilate(cv2.erode(m,K(9)),K(61)).astype(np.float32)
    f=np.maximum(f*near, dark*body*(a0>0.03)*(~wood))
    f=cv2.GaussianBlur(f,(0,0),1.0)
    return (np.clip(f,0,1)*255).astype(np.uint8)
def get(t,clip='clean2.mov'):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',clip,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout,np.uint8).reshape(H,W,3)
def geta(t):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-c:v','libvpx-vp9','-i','matte_raw.webm','-frames:v','1','-vf','format=yuva420p,alphaextract,format=gray','-f','rawvideo','-'],capture_output=True).stdout,np.uint8).reshape(H,W)
if __name__=='__main__':
    out=[]
    for t in (88,14.5,31,44.8,60,95,2):
        fr=get(t); al=geta(t); r=refine(al,fr)
        bg=np.zeros_like(fr); bg[:]=(20,60,150)
        comp=lambda x:(fr*(x[...,None]/255.)+bg*(1-x[...,None]/255.)).astype(np.uint8)
        out.append(cv2.resize(comp(r),(270,480)))
    cv2.imwrite('refine3b_test.jpg',cv2.cvtColor(np.hstack(out),cv2.COLOR_RGB2BGR))
