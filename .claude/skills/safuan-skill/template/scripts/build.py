#!/usr/bin/env python3
"""Safuan "Caption Cutaway" style (from Drive reference): full-frame footage, white hook box, small black-box captions
with yellow keywords, and cutaway cards in a top strip. Builds hf/index.html."""
import json, os, re, html
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPEECH_END = 86.9
TOTAL = 89.66
END = 86.95

words = []
for si, s in enumerate(json.load(open(f"{ROOT}/analysis/words.json"))):
    for w in s["words"]:
        words.append([w["w"].strip(), w["s"], w["e"], si])
# fixes: owner name
out = []
i = 0
while i < len(words):
    w = words[i]
    if w[0].lower().startswith("bruce") and i + 1 < len(words):
        out.append(["BroSafuan" + ("," if words[i + 1][0].endswith(",") else ""), w[1], words[i + 1][2], w[3]]); i += 2; continue
    out.append(w); i += 1
words = out

KEY = re.compile(r"^(engagement|pause|speed|impact|laju\w*|drag|timeline|content|nombor|satu|dua|stay|manipulate|training|brosafuan)", re.I)

# ---- chunk into caption phrases
chunks, cur = [], []
def flush():
    global cur
    if cur: chunks.append(cur); cur = []
for k, w in enumerate(words):
    if cur and (w[3] != cur[-1][3] or w[1] - cur[-1][2] > 0.45 or len(cur) >= 5 or len(" ".join(x[0] for x in cur)) + len(w[0]) > 28):
        flush()
    cur.append(w)
    if re.search(r"[?.!,]$", w[0]) and len(cur) >= 3:
        flush()
flush()

def esc(s): return html.escape(s)
cap_html, cap_js = [], []
for n, c in enumerate(chunks):
    a = max(0.0, c[0][1] - 0.06)
    nxt = chunks[n + 1][0][1] - 0.06 if n + 1 < len(chunks) else SPEECH_END
    b = min(c[-1][2] + 0.18, nxt - 0.01) if n + 1 < len(chunks) else c[-1][2] + 0.25
    if b - a < 0.25: b = a + 0.25
    txt = " ".join(f'<b class="k">{esc(w[0])}</b>' if KEY.match(w[0].strip(" ,.?!")) else esc(w[0]) for w in c)
    cap_html.append(f'<div id="cp{n}" class="clip cap" data-start="{a:.2f}" data-duration="{b-a:.2f}"><span class="capbox">{txt}</span></div>')
    cap_js.append(f'tl.fromTo("#cp{n} .capbox",{{y:14,opacity:0,scale:.94}},{{y:0,opacity:1,scale:1,duration:.14,ease:"expo.out"}},{a:.2f});')

# ---- cutaway cards (top strip, y 300..780)
PAUSE = '<svg viewBox="0 0 100 100" width="100" height="100"><rect x="24" y="14" width="18" height="72" rx="5" fill="#fff"/><rect x="58" y="14" width="18" height="72" rx="5" fill="#fff"/></svg>'
CARDS = [
 # id, start, end, inner html
 ("c1", 2.05, 5.25, f'<div class="row"><div class="badge">1</div><div class="sq">{PAUSE}</div></div><div class="lbl">PAUSE VIDEO</div>'),
 ("c2", 8.35, 10.9, f'<div class="player"><div class="bar"><i id="c2f"></i><u id="c2k"></u></div></div><div class="bubble">pause dulu kat sini</div>'),
 ("c3", 12.3, 13.7, '<svg viewBox="0 0 100 100" width="120" height="120"><circle cx="50" cy="50" r="44" fill="#22c55e"/><path id="c3p" d="M28 52 L45 68 L74 34" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="90" stroke-dashoffset="90"/></svg><div class="lbl">ENGAGEMENT</div>'),
 ("c4", 14.8, 18.3, '<div class="stay">STAY</div><div class="lbl">DEKAT VIDEO</div>'),
 ("c5", 22.7, 26.9, '<div class="row"><div class="badge">2</div><div class="sq wide">2×<span>▶▶</span></div></div><div class="lbl">SPEED UP VIDEO</div>'),
 ("c6", 43.4, 49.3, '<div class="player"><div class="bar"><i id="c6f"></i><u id="c6k"></u></div></div><div class="lbl">DRAG TIMELINE</div>'),
 ("c7", 66.0, 72.8, '<div class="player"><div class="bar"><b class="blip" id="c7b"></b><i id="c7f"></i><u id="c7k"></u></div></div><div class="lbl" id="c7l">tunjuk sekejap je</div>'),
]
card_html, card_js = [], []
for cid, a, b, inner in CARDS:
    card_html.append(f'<div id="{cid}" class="clip card" data-start="{a}" data-duration="{b-a:.2f}"><div class="cardin">{inner}</div></div>')
    card_js.append(f'tl.fromTo("#{cid} .cardin",{{yPercent:-110}},{{yPercent:0,duration:.28,ease:"expo.out"}},{a});')
    card_js.append(f'tl.to("#{cid} .cardin",{{yPercent:-110,duration:.2,ease:"expo.in"}},{b-0.22:.2f});')

extra = '''
// c2: scrub 0.18 -> 0.36 slowly, then stop (paused)
tl.fromTo("#c2f",{scaleX:0.18},{scaleX:0.36,duration:1.3,ease:"none"},8.5);
tl.fromTo("#c2k",{x:154.79999999999998},{x:309.59999999999997,duration:1.3,ease:"none"},8.5);
// c3 check
tl.to("#c3p",{strokeDashoffset:0,duration:.3,ease:"power2.out"},12.55);
// c4 stay counter
// c6 drag the timeline back and forth
tl.fromTo("#c6f",{scaleX:0.7},{scaleX:0.2,duration:.9,ease:"power2.inOut"},43.7);
tl.fromTo("#c6k",{x:602.0},{x:172.0,duration:.9,ease:"power2.inOut"},43.7);
tl.to("#c6f",{scaleX:0.58,duration:.8,ease:"power2.inOut"},45.2);
tl.to("#c6k",{x:498.79999999999995,duration:.8,ease:"power2.inOut"},45.2);
tl.to("#c6f",{scaleX:0.3,duration:.8,ease:"power2.inOut"},46.6);
tl.to("#c6k",{x:258.0,duration:.8,ease:"power2.inOut"},46.6);
// c7: knob runs past the short moment, then drags back and pauses on it
tl.fromTo("#c7f",{scaleX:0.3},{scaleX:0.62,duration:2.0,ease:"none"},66.3);
tl.fromTo("#c7k",{x:258.0},{x:533.1999999999999,duration:2.0,ease:"none"},66.3);
tl.fromTo("#c7b",{opacity:.25},{opacity:1,duration:.2},67.0);
tl.to("#c7f",{scaleX:0.47,duration:.6,ease:"power3.inOut"},69.6);
tl.to("#c7k",{x:404.2,duration:.6,ease:"power3.inOut"},69.6);
'''

# ---- camera: slow push + snap punches (footage grade untouched)
cam = []
beats = [(0, 1.0, 1.06, 4.0), (2.1, 1.12, 1.16, 3.4), (5.6, 1.0, 1.05, 5.0), (12.3, 1.1, 1.13, 3.0), (22.7, 1.12, 1.17, 4.5),
         (30.8, 1.0, 1.06, 6.0), (43.4, 1.1, 1.14, 5.5), (50.2, 1.0, 1.06, 7.0), (58.4, 1.1, 1.15, 5.0), (63.9, 1.0, 1.06, 9.0),
         (73.0, 1.0, 1.05, 4.8), (77.95, 1.1, 1.14, 9.0)]
for t, s0, s1, d in beats:
    cam.append(f'tl.fromTo("#cam",{{scale:{s0}}},{{scale:{s1},duration:{d},ease:"none"}},{t});' if t == 0 else
               f'tl.fromTo("#cam",{{scale:{s0}}},{{scale:{s1},duration:{d},ease:"none",immediateRender:false}},{t});')

page = f'''<!doctype html>
<html lang="ms"><head><meta charset="utf-8"><meta name="viewport" content="width=1080, height=1920">
<title>Safuan Video</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
html,body{{margin:0;background:#000;font-family:Inter,system-ui,sans-serif}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#000}}
#cam{{position:absolute;inset:0;transform-origin:45% 42%}}
#vid{{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}}
.cap{{position:absolute;left:0;width:1080px;top:1040px;display:flex;justify-content:center}}
.capbox{{background:rgba(8,8,8,.88);color:#fff;font-weight:800;font-size:54px;line-height:1.18;padding:14px 26px;border-radius:12px;max-width:900px;text-align:center}}
.k{{color:#FFD84A;font-weight:900}}
#hook{{position:absolute;left:0;width:1080px;top:335px;display:flex;justify-content:center}}
#hookbox{{background:#fff;color:#0b0b0b;font-weight:900;font-size:62px;line-height:1.1;padding:22px 34px;border-radius:26px;text-align:center;max-width:820px;box-shadow:0 10px 40px rgba(0,0,0,.35)}}
.card{{position:absolute;left:0;top:290px;width:1080px;height:340px;overflow:hidden}}
.cardin{{width:100%;height:100%;background:linear-gradient(160deg,#10182b,#1b2b52);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;border-bottom:6px solid #FFD84A}}
.row{{display:flex;align-items:center;gap:36px}}
.badge{{width:120px;height:120px;border-radius:50%;background:#FFD84A;color:#0b0b0b;font-size:84px;font-weight:900;display:flex;align-items:center;justify-content:center}}
.sq{{width:140px;height:140px;border-radius:30px;background:#ef4444;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:72px}}
.sq.wide{{width:260px;gap:6px}}.sq span{{font-size:44px;margin-left:8px}}
.lbl{{color:#fff;font-size:50px;font-weight:900;letter-spacing:2px;text-align:center}}
.stay{{color:#FFD84A;font-weight:900;font-size:130px;line-height:1}}
.player{{width:860px}}
.bar{{position:relative;height:18px;border-radius:9px;background:rgba(255,255,255,.25)}}
.bar i{{position:absolute;left:0;top:0;height:100%;border-radius:9px;background:#ef4444;width:100%;transform-origin:0 50%}}
.bar u{{position:absolute;top:-14px;margin-left:-23px;width:46px;height:46px;border-radius:50%;background:#fff;left:0;box-shadow:0 4px 18px rgba(0,0,0,.5)}}
.blip{{position:absolute;left:47%;top:-8px;width:34px;height:34px;border-radius:8px;background:#FFD84A;opacity:.25;transform:translateX(-50%)}}
.bubble{{background:#fff;color:#111;font-weight:800;font-size:50px;padding:14px 30px;border-radius:40px}}
#endc{{position:absolute;inset:0;background:rgba(6,10,20,.78);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px}}
#endc img{{width:300px;height:300px;border-radius:50%;border:4px solid #fff;box-shadow:0 0 60px rgba(34,211,238,.65)}}
#endc .nm{{color:#fff;font-size:92px;font-weight:900;margin-top:10px}}
#endc .sb{{color:#FFD84A;font-size:48px;font-weight:800}}
#endc .cta{{margin-top:18px;background:#fff;color:#0b0b0b;font-weight:900;font-size:46px;padding:16px 34px;border-radius:50px}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="{TOTAL}">
 <div id="cam"><video id="vid" class="clip" data-start="0" data-duration="{TOTAL}" src="assets/video/main.mp4" muted playsinline></video></div>
 {''.join(card_html)}
 <div id="hook" class="clip" data-start="0" data-duration="2.0"><div id="hookbox">Engagement yang kita tak nampak</div></div>
 {''.join(cap_html)}
 <div id="endc" class="clip" data-start="{END}" data-duration="{TOTAL-END:.2f}"><img src="assets/img/logo_icon.png" alt="BroSafuan"><div class="nm">BroSafuan</div><div class="sb">Content Strategist</div><div class="cta">DM untuk training content</div></div>
 <audio id="mix" src="assets/audio/mix_master.wav" data-start="0" data-duration="{TOTAL}" data-track-index="9"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
{chr(10).join(cam)}
tl.fromTo("#hookbox",{{scale:.8,opacity:0}},{{scale:1,opacity:1,duration:.22,ease:"back.out(1.8)"}},0.02);
tl.to("#hookbox",{{opacity:0,y:-20,duration:.15}},1.85);
{chr(10).join(cap_js)}
{chr(10).join(card_js)}
{extra}
tl.fromTo("#endc",{{opacity:0}},{{opacity:1,duration:.35,ease:"power2.out"}},{END});
tl.from("#endc img",{{scale:.7,duration:.45,ease:"back.out(1.8)"}},{END+0.05});
window.__timelines["main"] = tl;
</script></body></html>'''
open(f"{ROOT}/hf/index.html", "w").write(page)
json.dump({"chunks": [[" ".join(w[0] for w in c), c[0][1], c[-1][2]] for c in chunks],
           "cards": [(c[0], c[1], c[2]) for c in CARDS]}, open(f"{ROOT}/analysis/plan.json", "w"), ensure_ascii=False, indent=1)
print(len(chunks), "caption chunks")
