#!/usr/bin/env python3
"""Builds index.html (1080x1920) for 'Tingkap Bujur' – cartoon explainer on the supplied VO."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OL = 'stroke="#141414" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"'
SKIN = "#e0a469"

# ---------- scene starts (word start - ~0.1 so the wipe lands on the word) ----------
SC = [
    ("s1", 0.0), ("s2", 2.72), ("s3", 7.0), ("s4", 14.45), ("s5", 20.4),
    ("s7", 30.35), ("s8", 38.5), ("s9", 39.5), ("s10", 45.3), ("s11", 47.2),
]
TOTAL = 51.0


def mascot(p, x, y, s, mouth="smile", extra=""):
    """Original Malaysian blob mascot: songkok + baju Melayu teal + red sampin. Origin = head centre."""
    mouths = {
        "smile": f'<path d="M-70 100 Q0 170 70 100" fill="none" {OL}/>',
        "grin": f'<path d="M-90 92 Q0 215 90 92 Z" fill="#8b2323" {OL}/><path d="M-50 150 Q0 190 50 150 Q0 135 -50 150Z" fill="#e8605a"/>',
        "open": f'<ellipse cx="0" cy="130" rx="42" ry="52" fill="#7a1f1f" {OL}/><ellipse cx="0" cy="150" rx="26" ry="20" fill="#e8605a"/>',
        "worry": f'<path d="M-65 150 Q0 95 65 150" fill="none" {OL}/>',
        "flat": f'<path d="M-55 125 L55 125" fill="none" {OL}/>',
    }
    mouth_svg = "".join(
        f'<g id="{p}mo_{k}" opacity="{1 if k == mouth else 0}">{v}</g>' for k, v in mouths.items()
    )

    def eye(side, cx):
        return (
            f'<ellipse cx="{cx}" cy="-10" rx="66" ry="74" fill="#fff" stroke="#141414" stroke-width="9"/>'
            f'<g id="{p}pup{side}"><circle cx="{cx}" cy="-6" r="22" fill="#141414"/>'
            f'<circle cx="{cx-7}" cy="-16" r="7" fill="#fff"/></g>'
        )

    return f'''
<g transform="translate({x} {y}) scale({s})">
 <g id="{p}m">
  <path d="M-235 340 Q-245 205 -150 192 L150 192 Q245 205 235 340 L235 470 L-235 470 Z" fill="#19a39a" {OL}/>
  <path d="M-235 380 L235 380 L235 470 L-235 470Z" fill="#d63a2b" {OL}/>
  <path d="M-235 410 L235 410" stroke="#f2c230" stroke-width="12"/>
  <rect x="-52" y="150" width="104" height="60" fill="{SKIN}" {OL}/>
  <path d="M-48 190 L0 262 L48 190 Z" fill="#0f7d76" {OL}/>
  <circle cx="0" cy="300" r="13" fill="#f2c230" stroke="#141414" stroke-width="6"/>
  <circle cx="0" cy="345" r="13" fill="#f2c230" stroke="#141414" stroke-width="6"/>
  <ellipse cx="-252" cy="25" rx="36" ry="50" fill="{SKIN}" {OL}/>
  <ellipse cx="252" cy="25" rx="36" ry="50" fill="{SKIN}" {OL}/>
  <ellipse cx="0" cy="0" rx="258" ry="228" fill="{SKIN}" {OL}/>
  <ellipse cx="-165" cy="92" rx="38" ry="23" fill="#ef7f6e" opacity=".6"/>
  <ellipse cx="165" cy="92" rx="38" ry="23" fill="#ef7f6e" opacity=".6"/>
  {eye("L", -100)}{eye("R", 100)}
  <path id="{p}browL" d="M-172 -112 Q-102 -150 -40 -116" fill="none" {OL}/>
  <path id="{p}browR" d="M172 -112 Q102 -150 40 -116" fill="none" {OL}/>
  <g transform="translate(0 6)">{mouth_svg}</g>
  <path d="M-196 -128 Q-200 -300 -150 -334 L150 -334 Q200 -300 196 -128 Q0 -188 -196 -128 Z" fill="#1d1d1d" {OL}/>
  <path d="M-196 -128 Q0 -188 196 -128" fill="none" stroke="#f2c230" stroke-width="13" stroke-linecap="round"/>
  <ellipse cx="-70" cy="-270" rx="46" ry="14" fill="#fff" opacity=".14"/>
  {extra}
 </g>
</g>'''


def hand(p, x, y, s, thumb=True):
    t = (
        f'<rect x="-22" y="-120" width="44" height="90" rx="22" fill="{SKIN}" {OL}/>' if thumb else ""
    )
    return f'''<g transform="translate({x} {y}) scale({s})"><g id="{p}">{t}
 <rect x="-78" y="-50" width="156" height="120" rx="52" fill="{SKIN}" {OL}/>
 <path d="M-40 -8 L40 -8 M-40 22 L40 22" stroke="#141414" stroke-width="7" stroke-linecap="round"/></g></g>'''


def star(cx, cy, r, fill="#ffd400", idn=""):
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return f'<polygon id="{idn}" points="{" ".join(pts)}" fill="{fill}" {OL}/>'


def rays(idn, cx, cy, c1, c2, n=18, R=2400):
    import math
    out = []
    for i in range(n):
        a0 = i * 2 * math.pi / n
        a1 = a0 + math.pi / n
        out.append(
            f'<path d="M{cx} {cy} L{cx+R*math.cos(a0):.0f} {cy+R*math.sin(a0):.0f} L{cx+R*math.cos(a1):.0f} {cy+R*math.sin(a1):.0f}Z" fill="{c2}"/>'
        )
    return f'<rect width="1080" height="1920" fill="{c1}"/><g id="{idn}" style="transform-origin:{cx}px {cy}px">{"".join(out)}</g>'


def window(p, cx, cy, w, h, rx, glass="#8fd3ff", frame="#f6f0e2", sill=True):
    """Airplane window: outer frame + glass + shade line + little cloud. pathLength=1 on the outline for draw-on."""
    fw, fh = w + 80, h + 80
    return f'''<g id="{p}" >
 <rect id="{p}_fr" x="{cx-fw/2}" y="{cy-fh/2}" width="{fw}" height="{fh}" rx="{rx+40}" fill="{frame}" {OL}/>
 <rect id="{p}_gl" x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{rx}" fill="{glass}" {OL}/>
 <g id="{p}_in" clip-path="url(#{p}_clip)">
   <ellipse cx="{cx-w*0.12}" cy="{cy+h*0.2}" rx="{w*0.34}" ry="{h*0.07}" fill="#fff" opacity=".95"/>
   <ellipse cx="{cx+w*0.14}" cy="{cy+h*0.13}" rx="{w*0.2}" ry="{h*0.06}" fill="#fff" opacity=".95"/>
   <rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h*0.22}" fill="#fff" opacity=".35"/>
 </g>
 <clipPath id="{p}_clip"><rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{rx}"/></clipPath>
</g>'''


def plane_side(p, cx, cy, w, windows, shape="oval", wc="#8fd3ff", body="#fffaf0"):
    h = w * 0.26
    ws = []
    n = windows
    gap = w * 0.5 / n
    x0 = cx - w * 0.5 * 0.5 + gap / 2 - w * 0.02
    for i in range(n):
        wx = x0 + i * gap
        if shape == "oval":
            ws.append(f'<rect id="{p}w{i}" x="{wx-14}" y="{cy-w*0.036}" width="28" height="{w*0.075}" rx="14" fill="{wc}" {OL.replace("10","7")}/>')
        else:
            ws.append(f'<rect id="{p}w{i}" x="{wx-20}" y="{cy-w*0.03}" width="40" height="40" rx="3" fill="{wc}" {OL.replace("10","7")}/>')
    return f'''<g id="{p}">
 <path d="M{cx-w/2} {cy} Q{cx-w/2} {cy-h/2} {cx-w*0.3} {cy-h/2} L{cx+w*0.28} {cy-h/2} Q{cx+w/2+30} {cy-h*0.3} {cx+w/2+60} {cy+h*0.05} Q{cx+w/2} {cy+h/2} {cx+w*0.25} {cy+h/2} L{cx-w*0.3} {cy+h/2} Q{cx-w/2} {cy+h/2} {cx-w/2} {cy}Z" fill="{body}" {OL}/>
 <path d="M{cx-w*0.47} {cy+h*0.2} L{cx+w*0.5} {cy+h*0.2}" stroke="#d63a2b" stroke-width="16"/>
 <path d="M{cx-w*0.46} {cy+h*0.33} L{cx+w*0.4} {cy+h*0.33}" stroke="#1d4ed8" stroke-width="10"/>
 <path d="M{cx-w*0.34} {cy-h*0.45} L{cx-w*0.46} {cy-h*1.5} L{cx-w*0.5} {cy-h*1.5} L{cx-w*0.5} {cy-h*0.45}Z" fill="#d63a2b" {OL}/>
 {"".join(ws)}
</g>'''


# ---------- scenes ----------
def s1():
    return f'''
{rays("s1_rays", 540, 760, "#ffc83d", "#ffb11a")}
<g id="s1_wall">
 <rect x="640" y="150" width="440" height="700" fill="#f6f0e2" {OL}/>
 {window("s1_win", 860, 520, 210, 330, 105)}
</g>
{mascot("s1", 460, 880, 1.45, "grin")}
<g id="s1_q1"><text x="760" y="1000" font-family="Archivo Black" font-size="190" fill="#e0262b" stroke="#141414" stroke-width="14" paint-order="stroke" transform="rotate(14 760 1000)">?</text></g>
<g id="s1_q2"><text x="130" y="520" font-family="Archivo Black" font-size="150" fill="#e0262b" stroke="#141414" stroke-width="14" paint-order="stroke" transform="rotate(-14 130 520)">?</text></g>
'''


def s2():
    seams = "".join(f'<path d="M0 {y} L1080 {y}" stroke="#d9ceb4" stroke-width="6"/>' for y in (260, 1280, 1500))
    return f'''
<rect width="1080" height="1920" fill="#efe6d2"/>{seams}
<g id="s2_oval">{window("s2o", 540, 780, 330, 500, 165)}</g>
<g id="s2_sq">{window("s2s", 540, 780, 400, 400, 14, glass="#ffd8d8", frame="#e8dcc0")}</g>
<g id="s2_x"><path d="M330 570 L750 990 M750 570 L330 990" stroke="#e0262b" stroke-width="56" stroke-linecap="round"/><path d="M330 570 L750 990 M750 570 L330 990" stroke="#141414" stroke-width="4" stroke-linecap="round" opacity=".0"/></g>
<g id="s2_ok"><circle cx="840" cy="440" r="86" fill="#27b35a" {OL}/><path d="M800 440 L830 475 L885 405" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/></g>
'''


def s3():
    shield = '<path d="M0 -120 L100 -85 L100 15 Q100 100 0 140 Q-100 100 -100 15 L-100 -85 Z" fill="#27b35a" stroke="#141414" stroke-width="12" stroke-linejoin="round"/><path d="M-45 5 L-12 40 L52 -35" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
    mag = '<g id="s3_mag"><circle cx="0" cy="0" r="86" fill="#bfe8ff" fill-opacity=".55" stroke="#141414" stroke-width="16"/><path d="M60 60 L170 170" stroke="#141414" stroke-width="30" stroke-linecap="round"/><path d="M60 60 L170 170" stroke="#8a5a2b" stroke-width="14" stroke-linecap="round"/></g>'
    sp = "".join(
        f'<g id="s3_st{i}">{star(x, y, r)}</g>' for i, (x, y, r) in enumerate([(560, 360, 46), (850, 330, 38), (880, 790, 50), (540, 760, 32)])
    )
    return f'''
{rays("s3_rays", 700, 620, "#ff7a59", "#ff6a45")}
<g id="s3_win">{window("s3w", 720, 600, 300, 460, 150)}</g>
{sp}
<g id="s3_shield" transform="translate(720 640)"><g id="s3_shieldi">{shield}</g></g>
{mascot("s3", 330, 1110, 1.05, "smile")}
<g transform="translate(430 1000)"><g id="s3_magg" style="transform-origin:0px 0px">{mag}</g></g>
'''


def s4():
    return f'''
<rect width="1080" height="1920" fill="#d8b684"/>
<rect width="1080" height="1920" fill="url(#s4_vig)"/>
<defs><radialGradient id="s4_vig" cx="50%" cy="45%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#5a3b14" stop-opacity=".55"/></radialGradient></defs>
<g id="s4_cl1"><ellipse cx="200" cy="420" rx="160" ry="46" fill="#f4e6c8" {OL.replace("10","7")}/></g>
<g id="s4_cl2"><ellipse cx="880" cy="1180" rx="190" ry="52" fill="#f4e6c8" {OL.replace("10","7")}/></g>
<g id="s4_cam">{plane_side("s4p", 540, 760, 1500, 6, shape="sq", wc="#fff2c4", body="#f0e6cf")}</g>
<path id="s4_l1" d="M60 640 L340 640 M0 760 L260 760 M80 880 L360 880" stroke="#8a6a3a" stroke-width="9" stroke-linecap="round"/>
'''


def s5():
    # fuselage panel with a square window, dark sky around
    corners = [(540 - 300, 900 - 300), (540 + 300, 900 - 300), (540 - 300, 900 + 300), (540 + 300, 900 + 300)]
    glow = "".join(f'<circle id="s5_c{i}" cx="{x}" cy="{y}" r="70" fill="#ff3b30" opacity="0"/>' for i, (x, y) in enumerate(corners))
    arrows = ""
    # 8 arrows from outside converging toward the corners
    ends = [(240, 600), (840, 600), (240, 1200), (840, 1200)]
    starts = [(60, 420), (1020, 420), (60, 1380), (1020, 1380)]
    for i, ((sx, sy), (ex, ey)) in enumerate(zip(starts, ends)):
        arrows += f'<g id="s5_a{i}"><path d="M{sx} {sy} L{ex} {ey}" stroke="#ff9f1c" stroke-width="30" stroke-linecap="round"/><path d="M{ex} {ey} l-60 -10 m60 10 l-10 -60" fill="none" stroke="#ff9f1c" stroke-width="30" stroke-linecap="round"/></g>' if False else ""
    # build proper arrow heads by rotating
    import math
    for i, ((sx, sy), (ex, ey)) in enumerate(zip(starts, ends)):
        ang = math.degrees(math.atan2(ey - sy, ex - sx))
        ln = math.hypot(ex - sx, ey - sy)
        arrows += f'''<g id="s5_a{i}"><g transform="translate({sx} {sy}) rotate({ang:.1f})">
 <path d="M0 0 L{ln-50:.0f} 0" stroke="#141414" stroke-width="44" stroke-linecap="round"/><path d="M0 0 L{ln-50:.0f} 0" stroke="#ffb02e" stroke-width="26" stroke-linecap="round"/>
 <path d="M{ln-90:.0f} -56 L{ln:.0f} 0 L{ln-90:.0f} 56 Z" fill="#ffb02e" {OL}/></g></g>'''
    return f'''
<rect width="1080" height="1920" fill="#1b2a49"/>
<g id="s5_cam" style="transform-origin:540px 900px">
 <rect x="-60" y="300" width="1200" height="1200" rx="110" fill="#c7d0dc" {OL}/>
 <path d="M-60 460 L1140 460 M-60 1340 L1140 1340" stroke="#a9b4c4" stroke-width="8"/>
 <rect x="190" y="550" width="700" height="700" rx="30" fill="#f6f0e2" {OL}/>
 <rect x="240" y="600" width="600" height="600" rx="14" fill="#8fd3ff" {OL}/>
 <ellipse cx="450" cy="1030" rx="170" ry="38" fill="#fff"/><ellipse cx="640" cy="980" rx="100" ry="30" fill="#fff"/>
 <g id="s5_ex" opacity="0"><text x="540" y="920" text-anchor="middle" font-family="Archivo Black" font-size="1" fill="none"></text></g>
 {glow}
 <path id="s5_crack" d="M840 600 L780 690 L810 740 L730 800 L770 850 L690 930 L720 960 L650 1030" fill="none" stroke="#141414" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>
 <path id="s5_crack2" d="M730 800 L650 770 L610 800 M690 930 L760 990" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>
 <path id="s5_crackw" d="M840 600 L780 690 L810 740 L730 800 L770 850 L690 930 L720 960 L650 1030" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" pathLength="1" opacity=".7"/>
 <path id="s5_crack3" d="M-60 430 L140 520 L100 600 L260 680 L230 800 L190 850" fill="none" stroke="#141414" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>
 <path id="s5_crack4" d="M1140 1250 L980 1180 L1010 1100 L880 1030 L920 960 L890 900" fill="none" stroke="#141414" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>
</g>
{arrows}
<g id="s5_peek">{mascot("s5", 190, 1500, 0.62, "worry")}</g>
<g id="s5_ex1"><text x="340" y="1260" font-family="Archivo Black" font-size="150" fill="#ff3b30" stroke="#141414" stroke-width="14" paint-order="stroke">!</text></g>
<g id="s5_sweat"><path d="M300 1330 q-24 40 0 56 q24 -16 0 -56z" fill="#9fe0ff" {OL.replace("10","6")}/></g>
'''


def s7():
    import math
    # flow arcs around oval window (cx 540, cy 860, outer 410x590) – green arrows that wrap around the curved edges
    arcs = ""
    pts = [
        ("M 210 520 Q 260 330 540 300 Q 820 330 870 520", "s7_f1"),
        ("M 870 1200 Q 820 1390 540 1420 Q 260 1390 210 1200", "s7_f2"),
        ("M 160 560 Q 130 860 190 1160", "s7_f3"),
        ("M 920 560 Q 950 860 890 1160", "s7_f4"),
    ]
    for d, i in pts:
        arcs += f'<path id="{i}" d="{d}" fill="none" stroke="#141414" stroke-width="46" stroke-linecap="round" pathLength="1"/><path id="{i}g" d="{d}" fill="none" stroke="#2ecc71" stroke-width="26" stroke-linecap="round" pathLength="1"/>'
    return f'''
{rays("s7_rays", 540, 860, "#6fd0ff", "#5ac2f7")}
<g id="s7_win">{window("s7w", 540, 860, 330, 480, 165)}</g>
{arcs}
<g id="s7_ok"><circle cx="540" cy="860" r="1" fill="none"/><g transform="translate(540 860)"><g id="s7_okg"><circle r="110" fill="#27b35a" {OL}/><path d="M-52 4 L-14 46 L58 -40" fill="none" stroke="#fff" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/></g></g></g>
'''


def s8():
    sp = "".join(f'<g id="s8_st{i}">{star(x, y, r)}</g>' for i, (x, y, r) in enumerate([(130, 460, 70), (950, 520, 56), (880, 1200, 62), (180, 1180, 46)]))
    return f'''
{rays("s8_rays", 540, 780, "#ffd23f", "#ffc21a")}
{mascot("s8", 470, 830, 1.35, "grin")}
{hand("s8_hand", 880, 1010, 1.3)}
{sp}
'''


def s9():
    cl = "".join(
        f'<g id="s9_c{i}"><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*0.3:.0f}" fill="#fff" {OL.replace("10","7")}/></g>'
        for i, (x, y, rx) in enumerate([(120, 420, 150), (900, 580, 190), (300, 1200, 170), (860, 1250, 140)])
    )
    return f'''
<rect width="1080" height="1920" fill="#74d2ff"/>
<rect y="1500" width="1080" height="420" fill="#4db8ee"/>
{cl}
<g id="s9_cam" style="transform-origin:700px 780px">
 <g id="s9_plane">{plane_side("s9p", 540, 780, 1300, 6)}</g>
 <g id="s9_face"><clipPath id="s9_fc"><rect x="648" y="733" width="56" height="98" rx="28"/></clipPath>
   <g clip-path="url(#s9_fc)"><rect x="640" y="720" width="80" height="130" fill="#8fd3ff"/>
   <g transform="translate(676 805) scale(.15)"><path d="M-235 340 Q-245 205 -150 192 L150 192 Q245 205 235 340 L235 470 L-235 470 Z" fill="#19a39a"/>
     <ellipse cx="0" cy="0" rx="258" ry="228" fill="{SKIN}"/><path d="M-196 -128 Q-200 -300 -150 -334 L150 -334 Q200 -300 196 -128 Q0 -188 -196 -128 Z" fill="#1d1d1d"/>
     <ellipse cx="-100" cy="-10" rx="66" ry="74" fill="#fff"/><ellipse cx="100" cy="-10" rx="66" ry="74" fill="#fff"/><circle cx="-90" cy="-6" r="24"/><circle cx="110" cy="-6" r="24"/>
     <path d="M-70 100 Q0 170 70 100" fill="none" stroke="#141414" stroke-width="16" stroke-linecap="round"/>
     <path d="M-210 200 L210 380" stroke="#ffd23f" stroke-width="52"/></g></g>
   <rect x="648" y="733" width="56" height="98" rx="28" fill="none" stroke="#141414" stroke-width="7"/></g>
</g>
<g id="s9_shield" transform="translate(676 782)"><g id="s9_shieldi"><path d="M0 -120 L100 -85 L100 15 Q100 100 0 140 Q-100 100 -100 15 L-100 -85 Z" fill="#27b35a" {OL}/><path d="M-45 5 L-12 40 L52 -35" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/></g></g>
'''


def s10():
    bulb = f'''<g id="s10_bulb" transform="translate(0 -470)"><g id="s10_bulbi">
 <path d="M0 -150 Q-110 -150 -110 -40 Q-110 20 -60 60 L-60 110 L60 110 L60 60 Q110 20 110 -40 Q110 -150 0 -150Z" fill="#ffe14d" {OL}/>
 <rect x="-52" y="110" width="104" height="30" rx="8" fill="#9aa3b2" {OL}/>
 <path d="M-170 -90 L-230 -110 M170 -90 L230 -110 M0 -210 L0 -270 M-130 -190 L-170 -240 M130 -190 L170 -240" stroke="#141414" stroke-width="12" stroke-linecap="round"/></g></g>'''
    return f'''
{rays("s10_rays", 540, 900, "#8ee3b0", "#7bd9a2")}
{mascot("s10", 540, 980, 1.3, "smile", extra=bulb)}
'''


def s11():
    return f'''
<rect width="1080" height="1920" fill="#19a39a"/>
<g id="s11_band"><rect x="-200" y="1010" width="1500" height="360" fill="#ffc83d" {OL} transform="rotate(-6 540 1190)"/></g>
{mascot("s11", 540, 520, 0.9, "grin")}
<g id="s11_brand"><text id="s11_t1" x="540" y="1130" text-anchor="middle" font-family="Archivo Black" font-size="150" fill="#fff" stroke="#141414" stroke-width="18" paint-order="stroke">BARU</text>
<text id="s11_t2" x="540" y="1300" text-anchor="middle" font-family="Archivo Black" font-size="150" fill="#ffd400" stroke="#141414" stroke-width="18" paint-order="stroke">TAHU</text></g>
<g id="s11_btn"><rect x="290" y="1400" width="500" height="130" rx="65" fill="#e0262b" {OL}/>
 <text x="540" y="1490" text-anchor="middle" font-family="Archivo Black" font-size="70" fill="#fff">FOLLOW</text></g>
{hand("s11_hand", 740, 1560, 1.2, thumb=False)}
'''


exec(open(ROOT/"scripts"/"patch_scenes.py").read())
SCENES = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s7": s7, "s8": s8, "s9": s9, "s10": s10, "s11": s11}

# ---------- captions (corrected spelling; times from Whisper words) ----------
CAPS = [
    ("Eh, korang", 0.03, ""), ("tahu tak?", 0.76, ""), ("Pernah tak", 1.35, ""), ("korang perasan,", 1.91, ""),
    ("Tingkap kapal", 2.83, ""), ("terbang semuanya", 3.68, ""), ("berbentuk", 4.8, ""), ("BUJUR.", 5.61, "k"),
    ("Bukannya", 5.91, ""), ("PETAK.", 6.66, "k"),
    ("Sebenarnya,", 7.11, ""), ("bentuk tingkap ini", 8.4, ""), ("bukan sekadar", 9.16, ""), ("nampak CANTIK.", 9.98, "k"),
    ("Tapi ada sebab", 11.15, ""), ("KESELAMATAN", 12.04, "k"), ("yang sangat penting.", 12.88, ""),
    ("Pada awal sejarah", 14.55, ""), ("penerbangan komersial,", 15.78, ""), ("ada kapal terbang", 17.03, ""),
    ("yang menggunakan", 17.95, ""), ("tingkap berbentuk PETAK.", 18.93, "k"),
    ("Masalahnya,", 20.51, ""), ("TEKANAN UDARA", 21.56, "k"), ("boleh tertumpu", 22.49, ""), ("pada bucu tingkap.", 23.48, ""),
    ("Lama kelamaan,", 25.19, ""), ("TEKANAN ini boleh", 26.14, "k"), ("menyebabkan", 27.24, ""), ("KERETAKAN", 28.06, "k"),
    ("kepada struktur", 28.75, ""), ("kapal terbang.", 29.53, ""),
    ("Sebab itulah", 30.47, ""), ("tingkap kapal", 31.16, ""), ("terbang modern", 31.94, ""), ("direka berbentuk", 32.84, ""),
    ("BUJUR,", 33.91, "k"), ("dengan bahagian tepi", 34.47, ""), ("yang MELENGKUNG", 35.42, "k"),
    ("untuk mengurangkan", 36.4, ""), ("tumpuan tekanan.", 37.34, ""),
    ("Menarik kan?", 38.59, ""), ("Rumusnya,", 39.63, ""), ("bentuk tingkap pun", 40.4, ""), ("boleh memainkan", 41.36, ""),
    ("peranan PENTING", 42.2, "k"), ("dalam KESELAMATAN", 43.19, "k"), ("kita ketika terbang.", 44.13, ""),
    ("Hah,", 45.43, ""), ("sekarang dah TAHU.", 45.81, "k"),
    ("Follow untuk lebih", 47.31, ""), ("banyak fakta", 48.7, ""), ("menarik dalam", 49.36, ""), ("BARU TAHU.", 50.23, "k"),
]
ENDS = {  # explicit end where there is a pause in the VO
    "Eh, korang": 0.72, "Sebenarnya,": 8.1, "yang sangat penting.": 14.15, "Masalahnya,": 21.4,
    "BARU TAHU.": 50.95, "PETAK.": 7.0,
}


def cap_html():
    out = []
    for i, (txt, st, kw) in enumerate(CAPS):
        nxt = CAPS[i + 1][1] if i + 1 < len(CAPS) else TOTAL
        en = ENDS.get(txt, nxt - 0.04)
        st0 = max(0, st - 0.04)
        words = txt.split(" ")
        spans = []
        for w in words:
            core = w.strip(",.?")
            hot = core.isupper() and len(core) > 2
            spans.append(f'<span class="{"hot" if hot else ""}">{w}</span>')
        rot = [-2.5, 1.8, -1.2, 2.6, -1.8][i % 5]
        dur = round(en - st0, 3)
        out.append(
            f'<div id="cap{i}" class="clip capw" data-start="{st0:.3f}" data-duration="{dur}" data-track-index="5">'
            f'<div class="cap" data-rot="{rot}">{" ".join(spans)}</div></div>'
        )
    return "\n".join(out)


def main():
    scenes_html = []
    for i, (sid, st) in enumerate(SC):
        nxt = SC[i + 1][1] if i + 1 < len(SC) else TOTAL
        dur = round(min(TOTAL, nxt + 0.4) - st, 3)
        scenes_html.append(
            f'<div id="{sid}" class="clip scene" data-start="{st}" data-duration="{dur}" data-track-index="{i+1}" data-track-kind="graphics" style="z-index:{10+i}">'
            f'<svg viewBox="0 0 1080 1920" width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">{SCENES[sid]()}</svg></div>'
        )
    anim = (ROOT / "scripts" / "anim.js").read_text()
    html = f'''<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#141414}}
#root{{position:absolute;inset:0;overflow:hidden;font-family:'Archivo Black',sans-serif}}
.scene{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}}
.scene svg{{position:absolute;left:0;top:0}}
.capw{{position:absolute;left:90px;width:900px;top:1290px;height:260px;z-index:100;display:flex;align-items:center;justify-content:center}}
.cap{{font-family:'Archivo Black',sans-serif;font-size:92px;line-height:1.02;text-align:center;color:#fff;text-transform:none;
  -webkit-text-stroke:16px #141414;paint-order:stroke fill;letter-spacing:.5px}}
.cap .hot{{color:#ffd400}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
<audio id="vo" src="assets/mix.wav" data-start="0" data-duration="50.95" data-volume="1"></audio>
{chr(10).join(scenes_html)}
<div id="captions" data-track-kind="captions">
{cap_html()}
</div>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
const SC = {json.dumps(dict(SC))};
{anim}
window.__timelines["main"] = tl;
</script>
</body>
</html>'''
    (ROOT / "index.html").write_text(html)
    print("index.html written", len(html))


main()
