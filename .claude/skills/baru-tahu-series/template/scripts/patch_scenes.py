# overrides for scenes that needed layout fixes (inserted before SCENES = {...})
import math

def cloud(idn, x, y, s=1.0):
    cs = [(-60, 8, 46), (0, -14, 62), (64, 6, 50), (20, 24, 44), (-30, 26, 38)]
    o = "".join(f'<circle cx="{x+cx*s}" cy="{y+cy*s}" r="{r*s+7}" fill="#141414"/>' for cx, cy, r in cs)
    f = "".join(f'<circle cx="{x+cx*s}" cy="{y+cy*s}" r="{r*s}" fill="#fff"/>' for cx, cy, r in cs)
    return f'<g id="{idn}">{o}{f}</g>'


def plane_side(p, cx, cy, w, windows, shape="oval", wc="#8fd3ff", body="#fffaf0"):
    h = w * 0.30
    step = w * 0.095
    x0 = cx - w * 0.27
    ws = []
    for i in range(windows):
        wx = x0 + i * step
        if shape == "oval":
            ww, hh = w * 0.036, w * 0.085
            ws.append(f'<rect id="{p}w{i}" x="{wx-ww/2:.1f}" y="{cy-hh/2-h*0.05:.1f}" width="{ww:.1f}" height="{hh:.1f}" rx="{ww/2:.1f}" fill="{wc}" stroke="#141414" stroke-width="7"/>')
        else:
            ss = w * 0.052
            ws.append(f'<rect id="{p}w{i}" x="{wx-ss/2:.1f}" y="{cy-ss/2-h*0.05:.1f}" width="{ss:.1f}" height="{ss:.1f}" rx="4" fill="{wc}" stroke="#141414" stroke-width="7"/>')
    return f'''<g id="{p}">
 <path d="M{cx-w/2} {cy} Q{cx-w/2} {cy-h/2} {cx-w*0.3} {cy-h/2} L{cx+w*0.28} {cy-h/2} Q{cx+w/2+30} {cy-h*0.3} {cx+w/2+60} {cy+h*0.05} Q{cx+w/2} {cy+h/2} {cx+w*0.25} {cy+h/2} L{cx-w*0.3} {cy+h/2} Q{cx-w/2} {cy+h/2} {cx-w/2} {cy}Z" fill="{body}" {OL}/>
 <path d="M{cx-w*0.47} {cy+h*0.2} L{cx+w*0.5} {cy+h*0.2}" stroke="#d63a2b" stroke-width="16"/>
 <path d="M{cx-w*0.46} {cy+h*0.33} L{cx+w*0.4} {cy+h*0.33}" stroke="#1d4ed8" stroke-width="10"/>
 <path d="M{cx-w*0.34} {cy-h*0.45} L{cx-w*0.44} {cy-h*1.7} L{cx-w*0.5} {cy-h*1.7} L{cx-w*0.5} {cy-h*0.45}Z" fill="#d63a2b" {OL}/>
 {"".join(ws)}
</g>'''


def s4():
    return f'''
<rect width="1080" height="1920" fill="#d8b684"/>
<rect width="1080" height="1920" fill="url(#s4_vig)"/>
<defs><radialGradient id="s4_vig" cx="50%" cy="45%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#5a3b14" stop-opacity=".55"/></radialGradient></defs>
{cloud("s4_cl1", 150, 330, 1.0)}{cloud("s4_cl2", 900, 1120, 1.1)}
<g id="s4_cam">{plane_side("s4p", 540, 700, 1000, 6, shape="sq", wc="#fff2c4", body="#f0e6cf")}</g>
<path id="s4_l1" d="M60 560 L330 560 M0 700 L240 700 M70 840 L340 840" stroke="#8a6a3a" stroke-width="9" stroke-linecap="round"/>
'''


def s5():
    Y = 700
    corners = [(240, Y - 300), (840, Y - 300), (240, Y + 300), (840, Y + 300)]
    glow = "".join(f'<circle id="s5_c{i}" cx="{x}" cy="{y}" r="70" fill="#ff3b30" opacity="0"/>' for i, (x, y) in enumerate(corners))
    starts = [(60, Y - 480), (1020, Y - 480), (60, Y + 480), (1020, Y + 480)]
    arrows = ""
    for i, ((sx, sy), (ex, ey)) in enumerate(zip(starts, corners)):
        ang = math.degrees(math.atan2(ey - sy, ex - sx)); ln = math.hypot(ex - sx, ey - sy)
        arrows += f'''<g id="s5_a{i}"><g transform="translate({sx} {sy}) rotate({ang:.1f})">
 <path d="M0 0 L{ln-50:.0f} 0" stroke="#141414" stroke-width="44" stroke-linecap="round"/><path d="M0 0 L{ln-50:.0f} 0" stroke="#ffb02e" stroke-width="26" stroke-linecap="round"/>
 <path d="M{ln-90:.0f} -56 L{ln:.0f} 0 L{ln-90:.0f} 56 Z" fill="#ffb02e" {OL}/></g></g>'''
    cr = lambda pts, w, c, i: f'<path id="{i}" d="{pts}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>'
    main = f"M840 {Y-300} L780 {Y-210} L810 {Y-160} L730 {Y-100} L770 {Y-50} L690 {Y+30} L720 {Y+60} L650 {Y+130}"
    return f'''
<rect width="1080" height="1920" fill="#1b2a49"/>
<g id="s5_cam">
 <rect x="-60" y="{Y-600}" width="1200" height="1200" rx="110" fill="#c7d0dc" {OL}/>
 <path d="M-60 {Y-440} L1140 {Y-440} M-60 {Y+440} L1140 {Y+440}" stroke="#a9b4c4" stroke-width="8"/>
 <rect x="190" y="{Y-350}" width="700" height="700" rx="30" fill="#f6f0e2" {OL}/>
 <rect x="240" y="{Y-300}" width="600" height="600" rx="14" fill="#8fd3ff" {OL}/>
 <ellipse cx="450" cy="{Y+130}" rx="170" ry="38" fill="#fff"/><ellipse cx="640" cy="{Y+80}" rx="100" ry="30" fill="#fff"/>
 {glow}
 {cr(main, 22, "#141414", "s5_crack")}{cr(main, 6, "#fff", "s5_crackw")}
 {cr(f"M730 {Y-100} L650 {Y-130} L600 {Y-100} M690 {Y+30} L770 {Y+90}", 16, "#141414", "s5_crack2")}
 {cr(f"M-60 {Y-470} L140 {Y-380} L100 {Y-300} L260 {Y-220} L230 {Y-100} L190 {Y-50}", 18, "#141414", "s5_crack3")}
 {cr(f"M1140 {Y+350} L980 {Y+280} L1010 {Y+200} L880 {Y+130} L920 {Y+60} L890 {Y}", 18, "#141414", "s5_crack4")}
</g>
{arrows}
<g id="s5_peek">{mascot("s5", 930, 1130, 0.44, "worry")}</g>
<g id="s5_ex1"><text x="770" y="1120" font-family="Archivo Black" font-size="130" fill="#ff3b30" stroke="#141414" stroke-width="14" paint-order="stroke">!</text></g>
<g id="s5_sweat"><path d="M880 1000 q-22 36 0 50 q22 -14 0 -50z" fill="#9fe0ff" {OL.replace("10","6")}/></g>
'''


def s7():
    cy = 700
    def arc(rx, ry, a0, a1, sweep, i):
        P = lambda a: (540 + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a)))
        (x0, y0), (x1, y1) = P(a0), P(a1)
        d = f"M{x0:.0f} {y0:.0f} A{rx} {ry} 0 0 {sweep} {x1:.0f} {y1:.0f}"
        # arrow head at end, tangent direction
        a = math.radians(a1)
        tx, ty = (-rx * math.sin(a), ry * math.cos(a)) if sweep == 1 else (rx * math.sin(a), -ry * math.cos(a))
        ang = math.degrees(math.atan2(ty, tx))
        head = f'<g id="{i}h" opacity="0"><g transform="translate({x1:.0f} {y1:.0f}) rotate({ang:.1f})"><path d="M-30 -48 L36 0 L-30 48 Z" fill="#2ecc71" {OL}/></g></g>'
        return (f'<path id="{i}" d="{d}" fill="none" stroke="#141414" stroke-width="44" stroke-linecap="round" pathLength="1"/>'
                f'<path id="{i}g" d="{d}" fill="none" stroke="#2ecc71" stroke-width="24" stroke-linecap="round" pathLength="1"/>{head}')
    arcs = arc(290, 370, 195, 340, 1, "s7_f1") + arc(290, 370, 165, 20, 0, "s7_f2") + arc(380, 470, 205, 335, 1, "s7_f3") + arc(380, 470, 155, 25, 0, "s7_f4")
    return f'''
{rays("s7_rays", 540, cy, "#6fd0ff", "#5ac2f7")}
<g id="s7_win">{window("s7w", 540, cy, 330, 480, 165)}</g>
{arcs}
<g transform="translate(540 {cy})"><g id="s7_okg"><circle r="110" fill="#27b35a" {OL}/><path d="M-52 4 L-14 46 L58 -40" fill="none" stroke="#fff" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/></g></g>
'''


def s8():
    sp = "".join(f'<g id="s8_st{i}">{star(x, y, r)}</g>' for i, (x, y, r) in enumerate([(130, 360, 70), (950, 420, 56), (900, 1080, 62), (170, 1060, 46)]))
    return f'''
{rays("s8_rays", 540, 700, "#ffd23f", "#ffc21a")}
{mascot("s8", 470, 720, 1.3, "grin")}
{hand("s8_hand", 880, 920, 1.3)}
{sp}
'''


def s9():
    cx, cy, w = 540, 780, 1300
    wx = cx - w * 0.27 + 4 * w * 0.095
    ww, hh = w * 0.036, w * 0.085
    h = w * 0.30
    wy = cy - hh / 2 - h * 0.05
    FX, FY = wx, wy + hh / 2
    cl = "".join(cloud(f"s9_c{i}", x, y, sc) for i, (x, y, sc) in enumerate([(120, 380, 1.2), (900, 520, 1.4), (300, 1160, 1.3), (860, 1210, 1.1)]))
    return f'''
<rect width="1080" height="1920" fill="#74d2ff"/>
<rect y="1500" width="1080" height="420" fill="#4db8ee"/>
{cl}
<g id="s9_cam">
 <g id="s9_plane">{plane_side("s9p", cx, cy, w, 6)}</g>
 <g id="s9_face"><clipPath id="s9_fc"><rect x="{wx-ww/2:.1f}" y="{wy:.1f}" width="{ww:.1f}" height="{hh:.1f}" rx="{ww/2:.1f}"/></clipPath>
   <g clip-path="url(#s9_fc)"><rect x="{wx-40:.0f}" y="{wy-10:.0f}" width="80" height="{hh+20:.0f}" fill="#8fd3ff"/>
   <g transform="translate({FX:.1f} {FY+22:.1f}) scale(.15)"><path d="M-235 340 Q-245 205 -150 192 L150 192 Q245 205 235 340 L235 470 L-235 470 Z" fill="#19a39a"/>
     <ellipse cx="0" cy="0" rx="258" ry="228" fill="{SKIN}"/><path d="M-196 -128 Q-200 -300 -150 -334 L150 -334 Q200 -300 196 -128 Q0 -188 -196 -128 Z" fill="#1d1d1d"/>
     <ellipse cx="-100" cy="-10" rx="66" ry="74" fill="#fff"/><ellipse cx="100" cy="-10" rx="66" ry="74" fill="#fff"/><circle cx="-90" cy="-6" r="24"/><circle cx="110" cy="-6" r="24"/>
     <path d="M-70 100 Q0 170 70 100" fill="none" stroke="#141414" stroke-width="16" stroke-linecap="round"/>
     <path d="M-210 200 L210 380" stroke="#ffd23f" stroke-width="52"/></g></g>
   <rect x="{wx-ww/2:.1f}" y="{wy:.1f}" width="{ww:.1f}" height="{hh:.1f}" rx="{ww/2:.1f}" fill="none" stroke="#141414" stroke-width="7"/></g>
</g>
<g id="s9_shield" transform="translate({wx:.1f} {wy+hh/2:.1f})"><g id="s9_shieldi"><path d="M0 -120 L100 -85 L100 15 Q100 100 0 140 Q-100 100 -100 15 L-100 -85 Z" fill="#27b35a" {OL}/><path d="M-45 5 L-12 40 L52 -35" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/></g></g>
<!--ORIGIN {wx:.1f} {wy+hh/2:.1f}-->
'''


def s10():
    bulb = f'''<g id="s10_bulb" transform="translate(0 -470)"><g id="s10_bulbi">
 <path d="M0 -150 Q-110 -150 -110 -40 Q-110 20 -60 60 L-60 110 L60 110 L60 60 Q110 20 110 -40 Q110 -150 0 -150Z" fill="#ffe14d" {OL}/>
 <rect x="-52" y="110" width="104" height="30" rx="8" fill="#9aa3b2" {OL}/>
 <path d="M-170 -90 L-230 -110 M170 -90 L230 -110 M0 -210 L0 -270 M-130 -190 L-170 -240 M130 -190 L170 -240" stroke="#141414" stroke-width="12" stroke-linecap="round"/></g></g>'''
    return f'''
{rays("s10_rays", 540, 800, "#8ee3b0", "#7bd9a2")}
{mascot("s10", 540, 880, 1.1, "smile", extra=bulb)}
'''


def s11():
    return f'''
<rect width="1080" height="1920" fill="#19a39a"/>
<g id="s11_band"><rect x="-200" y="640" width="1500" height="380" fill="#ffc83d" {OL} transform="rotate(-5 540 830)"/></g>
{mascot("s11", 540, 330, 0.72, "grin")}
<g id="s11_brand"><text id="s11_t1" x="540" y="790" text-anchor="middle" font-family="Archivo Black" font-size="150" fill="#fff" stroke="#141414" stroke-width="18" paint-order="stroke">BARU</text>
<text id="s11_t2" x="540" y="950" text-anchor="middle" font-family="Archivo Black" font-size="150" fill="#e0262b" stroke="#141414" stroke-width="18" paint-order="stroke">TAHU</text></g>
<g id="s11_btn"><rect x="300" y="1070" width="480" height="120" rx="60" fill="#e0262b" {OL}/>
 <text x="540" y="1151" text-anchor="middle" font-family="Archivo Black" font-size="64" fill="#fff">FOLLOW</text></g>
{hand("s11_hand", 730, 1235, 1.0, thumb=False)}
'''
