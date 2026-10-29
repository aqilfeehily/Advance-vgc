import json,re
tm=json.load(open('work/timemap.json'))   # [src_s, src_e, edit_s]
d=json.load(open('tools/transcript.json')); w=d if isinstance(d,list) else d['words']
def E(t):
    for s,e,o in tm:
        if s-0.001<=t<e: return round(o+t-s,2)
    return None
FIX={'sesemen':'salesman','luasannya':'luar sana','bonging':'bosan','desain':'design','kerasiti':'kekurangan','kerasa':'rasa','kaya':'weh','bagus':'baguslah','cita':'cerita','konten':'content','benar':'penuh','di':'beli'}
DROP={'oh','lah'}
KW=['stop','bosan','bulanan','kelayakan','fresh','best','idea','tahu','basic','flyers','kekurangan','design','button','fungsi','gali','educate','baru','followers','client','mengajar','komen','bisnes','follow','share','pakar','korang?']
words=[]
for i,x in enumerate(w):
    t=x['text'].strip(); s=x['start']
    if E(s) is None or t.lower().strip(',.') in ('eh','kau-kau'): continue
    k=t.lower().strip(',.')
    if k=='gaji': k='kelayakan' if s<10 else ('kaji' if 30<s<36 else 'gali')
    k=FIX.get(k,k)
    if s>=79.5 and s<80.4: continue   # 'dealing dengan berada ni' uncertain Whisper words: not captioned
    words.append((E(s),k))
chunks=[];cur=[]
for t,k in words:
    if cur and (len(cur)>=3 or (t-cur[-1][0])>0.5 or sum(len(x[1]) for x in cur)+len(k)>18): chunks.append(cur);cur=[]
    cur.append((t,k))
if cur: chunks.append(cur)
out=[]
for i,c in enumerate(chunks):
    t0=c[0][0]; t1=chunks[i+1][0][0] if i+1<len(chunks) else c[-1][0]+0.9
    t1=min(t1,t0+2.2)
    text=' '.join(k for _,k in c); kw=next((k for _,k in c if k in KW),'')
    out.append([t0,round(t1,2),text,kw])
js='// Caption chunks: [start, end, "Text", "keyword"] in EDIT time. Spelling corrected from Whisper.\nwindow.AKG_CAPS = [\n'+''.join(f'  {json.dumps(o,ensure_ascii=False)},\n' for o in out)+'];\n'
open('assets/js/captions.js','w').write(js); print(len(out))
for key in ['stop','tolonglah','fresh','tahu','cari','kekurangan','kenapa','gali','bila','educate','padahal','sangat','customer','followers','client','mengajar','komen','follow']:
    print(key,[E(x['start']) for x in w if x['text'].strip().lower().strip(',.')==key][:6])
