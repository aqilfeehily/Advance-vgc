# Video 02 "Kenapa wanita nampak lebih emosional" – overrides SC / TOTAL / SCENES / CAPS / ENDS
import math

TOTAL = 58.05
SC = [
    ("s1", 0.0), ("s2", 3.12), ("s3", 8.8), ("s4", 14.16), ("s5", 18.64), ("s6", 24.2),
    ("s7", 32.72), ("s8", 37.92), ("s9", 42.76), ("s10", 45.56), ("s11", 52.16), ("s12", 54.18),
]
OL6 = OL.replace("10", "6")
TUD = "#ff6f91"       # tudung
KURUNG = "#7a4bc7"    # baju kurung
SKIN2 = "#ecb98a"


def kak(p, x, y, s, mouth="smile", extra=""):
    """Original second character 'Kak': tudung bawal pink + baju kurung purple. Same ids as mascot()."""
    mouths = {
        "smile": f'<path d="M-62 92 Q0 150 62 92" fill="none" {OL}/>',
        "grin": f'<path d="M-80 85 Q0 195 80 85 Z" fill="#8b2323" {OL}/><path d="M-44 140 Q0 175 44 140 Q0 125 -44 140Z" fill="#e8605a"/>',
        "open": f'<ellipse cx="0" cy="118" rx="36" ry="46" fill="#7a1f1f" {OL}/><ellipse cx="0" cy="136" rx="22" ry="17" fill="#e8605a"/>',
        "worry": f'<path d="M-58 138 Q0 88 58 138" fill="none" {OL}/>',
        "flat": f'<path d="M-50 112 L50 112" fill="none" {OL}/>',
    }
    mo = "".join(f'<g id="{p}mo_{k}" opacity="{1 if k == mouth else 0}">{v}</g>' for k, v in mouths.items())

    def eye(side, cx):
        return (f'<ellipse cx="{cx}" cy="8" rx="56" ry="64" fill="#fff" stroke="#141414" stroke-width="9"/>'
                f'<g id="{p}pup{side}"><circle cx="{cx}" cy="12" r="20" fill="#141414"/><circle cx="{cx-6}" cy="2" r="6.5" fill="#fff"/></g>')
    return f'''
<g transform="translate({x} {y}) scale({s})">
 <g id="{p}m">
  <path d="M-225 340 Q-235 205 -150 192 L150 192 Q235 205 225 340 L225 470 L-225 470 Z" fill="{KURUNG}" {OL}/>
  <path d="M-290 330 Q-320 190 -150 160 L150 160 Q320 190 290 330 Q210 450 0 470 Q-210 450 -290 330Z" fill="{TUD}" {OL}/>
  <path d="M-120 330 Q0 380 120 330" fill="none" stroke="#e2527a" stroke-width="9" stroke-linecap="round"/>
  <ellipse cx="0" cy="-8" rx="288" ry="262" fill="{TUD}" {OL}/>
  <ellipse cx="0" cy="22" rx="216" ry="192" fill="{SKIN2}" {OL}/>
  <path d="M-216 -30 Q0 -120 216 -30" fill="none" stroke="#e2527a" stroke-width="9" opacity=".0"/>
  <ellipse cx="-150" cy="90" rx="36" ry="22" fill="#ef7f6e" opacity=".6"/>
  <ellipse cx="150" cy="90" rx="36" ry="22" fill="#ef7f6e" opacity=".6"/>
  {eye("L", -82)}{eye("R", 82)}
  <path d="M-132 -22 l-20 -14 M132 -22 l20 -14" fill="none" {OL.replace('stroke-width="10"', 'stroke-width="8"')}/>
  <path id="{p}browL" d="M-140 -72 Q-86 -104 -34 -78" fill="none" {OL}/>
  <path id="{p}browR" d="M140 -72 Q86 -104 34 -78" fill="none" {OL}/>
  <g transform="translate(0 4)">{mo}</g>
  <circle cx="200" cy="-150" r="30" fill="#ffd23f" {OL.replace("10","7")}/><circle cx="200" cy="-150" r="10" fill="#ff8c00"/>
  {extra}
 </g>
</g>'''


def mascot_var(p, x, y, s, mouth, shirt, dark):
    return mascot(p, x, y, s, mouth).replace("#19a39a", shirt).replace("#0f7d76", dark)


def bubble(idn, x, y, w, h, tail="left"):
    t = f"M{x+40} {y+h-4} L{x+10} {y+h+50} L{x+90} {y+h-4}" if tail == "left" else f"M{x+w-90} {y+h-4} L{x+w-10} {y+h+50} L{x+w-40} {y+h-4}"
    return f'<g id="{idn}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="#fff" {OL}/><path d="{t}" fill="#fff" {OL}/></g>'


def heart(idn, cx, cy, sc, fill="#ff5c8a"):
    return f'<g id="{idn}" transform="translate({cx} {cy}) scale({sc})"><g id="{idn}i"><path d="M0 60 C-110 -10 -70 -90 0 -35 C70 -90 110 -10 0 60Z" fill="{fill}" {OL}/></g></g>'


# ------------------------------------------------------------------ scenes
def s1():
    return f'''
{rays("s1_rays", 540, 760, "#ffc83d", "#ffb11a")}
{mascot("s1", 540, 860, 1.4, "open")}
<g id="s1_q1"><text x="880" y="640" font-family="Archivo Black" font-size="190" fill="#a8151a" stroke="#141414" stroke-width="14" paint-order="stroke" transform="rotate(14 880 640)">?</text></g>
<g id="s1_q2"><text x="90" y="520" font-family="Archivo Black" font-size="150" fill="#a8151a" stroke="#141414" stroke-width="14" paint-order="stroke" transform="rotate(-14 90 520)">?</text></g>
'''


def s2():
    pan = lambda i, x: f'''<g id="s2_pan{i}">
 <path d="M{x} 432 L{x-95} 700 M{x} 432 L{x+95} 700" stroke="#141414" stroke-width="8" fill="none"/>
 <ellipse cx="{x}" cy="706" rx="125" ry="26" fill="#f2c230" {OL}/>
 {mascot("s2a", x, 590, 0.2, "smile") if i == 0 else kak("s2b", x, 590, 0.2, "smile")}
</g>'''
    return f'''
{rays("s2_rays", 540, 600, "#cbbcff", "#bda9ff")}
<g id="s2_sc">
 <path d="M440 900 L640 900 L600 840 L480 840Z" fill="#8a5a2b" {OL}/>
 <rect x="522" y="430" width="36" height="420" rx="10" fill="#8a5a2b" {OL}/>
 <g id="s2_beam"><rect x="190" y="414" width="700" height="34" rx="17" fill="#f2c230" {OL}/><circle cx="540" cy="431" r="26" fill="#ffd23f" {OL}/></g>
 {pan(0, 230)}{pan(1, 850)}
</g>
{mascot("s2m", 280, 1120, 0.75, "smile")}
{kak("s2k", 800, 1120, 0.75, "smile")}
<g id="s2_q"><text x="520" y="1020" font-family="Archivo Black" font-size="180" fill="#e0262b" stroke="#141414" stroke-width="14" paint-order="stroke">?</text></g>
'''


def s3():
    cards = ""
    for i in range(4):
        x = 80 + i * 240
        rot = [-4, 3, -3, 4][i]
        cards += f'''<g id="s3_k{i}" ><g transform="translate({x+100} 430) rotate({rot})"><g id="s3_ki{i}">
 <rect x="-100" y="-125" width="200" height="250" rx="26" fill="#fff" {OL}/>
 <text x="0" y="55" text-anchor="middle" font-family="Archivo Black" font-size="170" fill="#ff6a45" stroke="#141414" stroke-width="10" paint-order="stroke">?</text></g></g></g>'''
    return f'''
{rays("s3_rays", 540, 860, "#ff7a59", "#ff6a45")}
{cards}
{kak("s3", 540, 1040, 1.0, "flat")}
'''


def s4():
    arcs = ""
    for a0, a1, c in [(180, 240, "#2ecc71"), (240, 300, "#ffd23f"), (300, 360, "#e0262b")]:
        P = lambda a: (300 + 150 * math.cos(math.radians(a)), 700 + 150 * math.sin(math.radians(a)))
        (x0, y0), (x1, y1) = P(a0), P(a1)
        arcs += f'<path d="M{x0:.0f} {y0:.0f} A150 150 0 0 1 {x1:.0f} {y1:.0f}" fill="none" stroke="{c}" stroke-width="46"/>'
    dots = "".join(f'<circle cx="{680+c*62}" cy="{650+r*56}" r="9" fill="#141414"/>' for r in range(3) for c in range(5))
    return f'''
{rays("s4_rays", 540, 700, "#19a39a", "#1fb3a9")}
<g id="s4_dial"><circle cx="300" cy="700" r="215" fill="#fff" {OL}/>{arcs}
 <g id="s4_needle"><path d="M300 700 L300 560" stroke="#141414" stroke-width="16" stroke-linecap="round"/><circle cx="300" cy="700" r="26" fill="#141414"/></g>
 <text x="300" y="900" text-anchor="middle" font-family="Archivo Black" font-size="58" fill="#fff" stroke="#141414" stroke-width="12" paint-order="stroke">HORMON</text></g>
<g id="s4_cal"><rect x="630" y="470" width="300" height="340" rx="26" fill="#fff" {OL}/><rect x="630" y="470" width="300" height="86" rx="26" fill="#e0262b" {OL}/>
 <circle cx="700" cy="470" r="14" fill="#141414"/><circle cx="860" cy="470" r="14" fill="#141414"/>{dots}
 <circle id="s4_day" cx="805" cy="706" r="30" fill="#ffd23f" opacity=".95" stroke="#141414" stroke-width="7"/></g>
<path id="s4_loop" d="M780 400 A250 250 0 1 1 560 530" fill="none" stroke="#141414" stroke-width="40" stroke-linecap="round" pathLength="1"/>
<path id="s4_loopg" d="M780 400 A250 250 0 1 1 560 530" fill="none" stroke="#ffd23f" stroke-width="22" stroke-linecap="round" pathLength="1"/>
<g id="s4_loopa" opacity="0"><g transform="translate(560 530) rotate(40)"><path d="M-34 -52 L40 0 L-34 52Z" fill="#ffd23f" {OL}/></g></g>
<g id="s4_peek">{mascot("s4", 150, 1130, 0.42, "smile")}</g>
'''


def s5():
    def plate(i, cx):
        return f'<circle id="s5_pl{i}" cx="{cx}" cy="640" r="150" fill="#fff" {OL}/>'
    face = lambda k, d: f'<g id="s5_f_{k}" opacity="{1 if k == "smile" else 0}">{d}</g>'
    mood = f'''<g id="s5_i0"><circle cx="195" cy="640" r="98" fill="#ffd23f" {OL}/>
 <circle cx="165" cy="615" r="11" fill="#141414"/><circle cx="225" cy="615" r="11" fill="#141414"/>
 {face("smile", '<path d="M150 665 Q195 715 240 665" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round"/>')}
 {face("flat", '<path d="M155 685 L235 685" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round"/>')}
 {face("worry", '<path d="M150 700 Q195 650 240 700" fill="none" stroke="#141414" stroke-width="10" stroke-linecap="round"/>')}</g>'''
    bat = f'''<g id="s5_i1"><rect x="480" y="545" width="120" height="190" rx="18" fill="#fff" {OL}/><rect x="523" y="525" width="34" height="24" rx="6" fill="#141414"/>
 <g id="s5_bat"><rect x="492" y="557" width="96" height="166" rx="10" fill="#2ecc71"/></g></g>'''
    hrt = f'''<g id="s5_i2">{heart("s5_h", 885, 640, 1.45)}
 <path d="M790 560 l-30 -22 M980 560 l30 -22 M780 700 l-36 10 M990 700 l36 10" stroke="#141414" stroke-width="9" stroke-linecap="round"/></g>'''
    lab = lambda x, t: f'<text x="{x}" y="860" text-anchor="middle" font-family="Archivo Black" font-size="40" fill="#fff" stroke="#141414" stroke-width="10" paint-order="stroke">{t}</text>'
    return f'''
{rays("s5_rays", 540, 700, "#8ee3b0", "#7bd9a2")}
<g id="s5_g0">{plate(0, 195)}{mood}{lab(195, "MOOD")}</g>
<g id="s5_g1">{plate(1, 540)}{bat}{lab(540, "TENAGA")}</g>
<g id="s5_g2">{plate(2, 885)}{hrt}{lab(885, "SENSITIVITY")}</g>
{kak("s5", 540, 1150, 0.5, "smile")}
'''


def s6():
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".7"/>' for x, y, r in [(110, 300, 6), (960, 260, 8), (230, 760, 5), (900, 880, 6), (60, 1000, 5), (1010, 640, 5)])
    pillow = '''<g id="s6_pil"><g transform="translate(540 810)"><rect x="-190" y="-55" width="380" height="110" rx="46" fill="#9fd3ff" stroke="#141414" stroke-width="10"/>
 <text x="0" y="22" text-anchor="middle" font-family="Archivo Black" font-size="80" fill="#fff" stroke="#141414" stroke-width="10" paint-order="stroke">Zzz</text></g></g>'''
    case = '''<g id="s6_cas"><g transform="translate(540 685)"><path d="M-50 -70 L-50 -100 L50 -100 L50 -70" fill="none" stroke="#141414" stroke-width="14" stroke-linejoin="round"/>
 <rect x="-170" y="-70" width="340" height="140" rx="20" fill="#a0632b" stroke="#141414" stroke-width="10"/><rect x="-24" y="-18" width="48" height="36" rx="6" fill="#ffd23f" stroke="#141414" stroke-width="7"/></g></g>'''
    rock = '''<g id="s6_rock"><g transform="translate(540 535)"><path d="M-150 80 Q-190 -10 -110 -60 Q-40 -100 40 -75 Q150 -60 160 20 Q170 80 100 80 Z" fill="#8d97a6" stroke="#141414" stroke-width="10" stroke-linejoin="round"/>
 <path d="M-60 -40 L-20 10 L-70 40 M70 -30 L40 20" fill="none" stroke="#141414" stroke-width="8" stroke-linecap="round"/></g></g>'''
    steam = "".join(f'<circle id="s6_st{i}" cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#141414" stroke-width="6" opacity="0"/>' for i, (x, y, r) in enumerate([(240, 960, 26), (210, 905, 18), (840, 960, 26), (870, 905, 18)]))
    sweat = '<g id="s6_sw"><path d="M770 800 q-22 36 0 50 q22 -14 0 -50z" fill="#9fe0ff" stroke="#141414" stroke-width="6"/></g>'
    return f'''
<rect width="1080" height="1920" fill="#1b2a49"/>{stars}
{kak("s6", 540, 1020, 0.95, "smile")}
{pillow}{case}{rock}{steam}{sweat}
'''


def s7():
    sun = ''.join(f'<path d="M0 -112 L0 -150" stroke="#141414" stroke-width="12" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45))
    return f'''
<rect width="1080" height="1920" fill="#8fd7ff"/>
<rect width="1080" height="1920" fill="#8fd7ff"/>
{cloud("s7_c1", 160, 1100, 1.1)}{cloud("s7_c2", 930, 330, 0.9)}
<g transform="translate(540 400)">
 <g id="s7_sun"><g id="s7_sunr">{sun}</g><circle r="92" fill="#ffd23f" {OL}/>
  <path d="M-34 8 Q0 44 34 8" fill="none" stroke="#141414" stroke-width="9" stroke-linecap="round"/><circle cx="-30" cy="-16" r="8" fill="#141414"/><circle cx="30" cy="-16" r="8" fill="#141414"/></g>
 <g id="s7_cl">{cloud("s7_cli", 0, 20, 1.5)}</g>
 <g id="s7_rain"><g transform="translate(0 20)">{cloud("s7_rc", 0, 0, 1.5).replace("#fff", "#9aa8bd")}</g>
  {''.join(f'<path id="s7_d{i}" d="M{x} 90 q-12 26 0 38 q12 -12 0 -38z" fill="#4fb4ff" {OL6}/>' for i, x in enumerate([-90, -30, 30, 90]))}</g>
</g>
{mascot("s7", 540, 1010, 1.05, "grin")}
'''


def s8():
    return f'''
{rays("s8_rays", 540, 760, "#ffc89a", "#ffbb84")}
<g id="s8_b1"><circle id="s8_bub" cx="190" cy="470" r="70" fill="#9fd3ff" {OL}/><circle cx="168" cy="448" r="14" fill="#fff" opacity=".8"/></g>
<g id="s8_b2">{bubble("s8_sp", 400, 380, 280, 150, "left")}<text x="540" y="478" text-anchor="middle" font-family="Archivo Black" font-size="90" fill="#141414">...</text></g>
<g id="s8_b3"><g transform="translate(890 470)"><g id="s8_note"><path d="M-30 60 L-30 -60 L50 -80 L50 40" fill="none" stroke="#141414" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><ellipse cx="-50" cy="64" rx="30" ry="22" fill="#141414"/><ellipse cx="30" cy="44" rx="30" ry="22" fill="#141414"/></g></g></g>
{mascot("s8a", 190, 820, 0.55, "smile")}
{kak("s8b", 540, 820, 0.55, "smile")}
{mascot_var("s8c", 890, 820, 0.55, "smile", "#f28c28", "#c46a12")}
{heart("s8_h0", 190, 330, 0.5)}{heart("s8_h1", 540, 300, 0.5)}{heart("s8_h2", 890, 330, 0.5)}
'''


def s9():
    return f'''
<rect width="1080" height="1920" fill="#efe6d2"/>
<g id="s9_card"><g transform="translate(540 530) rotate(-4)"><rect x="-450" y="-170" width="900" height="340" rx="36" fill="#fff" {OL}/>
 <text x="0" y="-20" text-anchor="middle" font-family="Archivo Black" font-size="76" fill="#141414">SEMUA PEREMPUAN</text>
 <text x="0" y="90" text-anchor="middle" font-family="Archivo Black" font-size="96" fill="#141414">CEPAT MARAH</text></g></g>
<g id="s9_x"><path d="M360 380 L720 680 M720 380 L360 680" stroke="#141414" stroke-width="76" stroke-linecap="round"/><path d="M360 380 L720 680 M720 380 L360 680" stroke="#e0262b" stroke-width="56" stroke-linecap="round"/></g>
{kak("s9", 540, 1090, 0.8, "flat")}
'''


def s10():
    wave = "".join(f'<path d="M{x} 760 q40 -26 80 0 t80 0" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".7"/>' for x in range(-80, 1160, 160))
    return f'''
<defs><linearGradient id="s10_wg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a7bc0"/><stop offset="0.45" stop-color="#0d4b82"/><stop offset="1" stop-color="#061f3e"/></linearGradient></defs>
<g id="s10_cam">
 <rect x="-10" y="-1200" width="1100" height="1960" fill="#bfe9ff"/>
 <rect x="-10" y="760" width="1100" height="2200" fill="url(#s10_wg)"/>
 <path id="s10_ice" d="M400 760 L660 760 L900 1010 L830 1400 L540 1580 L250 1390 L180 1010Z" fill="#8fd8ff" opacity=".92" {OL}/>
 <path id="s10_fac" d="M400 760 L470 1100 L540 1580 M660 760 L610 1090 L540 1580 M250 1390 L470 1100 L830 1400" fill="none" stroke="#5bb7e8" stroke-width="7"/>
 <path d="M410 770 L540 520 L650 770Z" fill="#fff" {OL}/>
 <path d="M540 520 L650 770 L585 770Z" fill="#cfeeff"/>
 <g id="s10_face"><circle cx="505" cy="690" r="9" fill="#141414"/><circle cx="575" cy="690" r="9" fill="#141414"/>
  <path d="M488 668 L520 680 M592 668 L560 680" stroke="#141414" stroke-width="8" stroke-linecap="round"/><path d="M510 726 Q540 704 570 726" fill="none" stroke="#141414" stroke-width="8" stroke-linecap="round"/></g>
 {wave}
 <text id="s10_t" x="540" y="1160" text-anchor="middle" font-family="Archivo Black" font-size="120" fill="#fff" stroke="#0a2f55" stroke-width="18" paint-order="stroke">TEKANAN</text>
</g>
'''


def s11():
    bulb = f'''<g id="s11_bulb" transform="translate(0 -470)"><g id="s11_bulbi">
 <path d="M0 -150 Q-110 -150 -110 -40 Q-110 20 -60 60 L-60 110 L60 110 L60 60 Q110 20 110 -40 Q110 -150 0 -150Z" fill="#ffe14d" {OL}/>
 <rect x="-52" y="110" width="104" height="30" rx="8" fill="#9aa3b2" {OL}/>
 <path d="M-170 -90 L-230 -110 M170 -90 L230 -110 M0 -210 L0 -270 M-130 -190 L-170 -240 M130 -190 L170 -240" stroke="#141414" stroke-width="12" stroke-linecap="round"/></g></g>'''
    return f'''
{rays("s11_rays", 540, 800, "#cbbcff", "#bda9ff")}
{mascot("s11", 540, 880, 1.1, "smile", extra=bulb)}
'''


def s12():
    return f'''
<rect width="1080" height="1920" fill="#19a39a"/>
<g id="s12_band"><rect x="-200" y="640" width="1500" height="380" fill="#ffc83d" {OL} transform="rotate(-5 540 830)"/></g>
{mascot("s12", 540, 330, 0.72, "grin")}
<g id="s12_brand"><text id="s12_t1" x="540" y="790" text-anchor="middle" font-family="Archivo Black" font-size="150" fill="#fff" stroke="#141414" stroke-width="18" paint-order="stroke">BARU</text>
<text id="s12_t2" x="540" y="950" text-anchor="middle" font-family="Archivo Black" font-size="150" fill="#e0262b" stroke="#141414" stroke-width="18" paint-order="stroke">TAHU</text></g>
<g id="s12_btn"><rect x="300" y="1070" width="480" height="120" rx="60" fill="#e0262b" {OL}/>
 <text x="540" y="1151" text-anchor="middle" font-family="Archivo Black" font-size="64" fill="#fff">FOLLOW</text></g>
{hand("s12_hand", 730, 1235, 1.0, thumb=False)}
'''


SCENES = {f"s{i}": globals()[f"s{i}"] for i in range(1, 13)}

CAPS = [
    ("Eh, korang", 0.02, ""), ("tahu tak?", 0.7, ""), ("Pernah tak", 1.42, ""), ("korang tertanya-tanya,", 1.94, ""),
    ("kenapa sesetengah", 3.22, ""), ("PEREMPUAN", 4.39, "k"), ("nampak lebih", 5.0, ""), ("mudah MARAH", 5.61, "k"),
    ("atau EMOSIONAL", 6.48, "k"), ("berbanding lelaki?", 7.56, ""),
    ("Sebenarnya,", 8.9, ""), ("ada beberapa", 9.84, ""), ("FAKTOR yang", 10.65, "k"), ("boleh mempengaruhi", 11.42, ""),
    ("EMOSI seseorang", 12.67, "k"), ("WANITA.", 13.7, "k"),
    ("Antaranya ialah", 14.26, ""), ("perubahan HORMON,", 15.27, "k"), ("terutamanya", 16.57, ""), ("ketika kitaran", 17.49, ""), ("HAID.", 18.16, "k"),
    ("Perubahan hormon", 18.74, ""), ("boleh mempengaruhi", 19.72, ""), ("MOOD,", 20.84, "k"), ("tahap tenaga", 21.36, ""),
    ("dan sensitivity", 22.42, ""), ("emosi.", 23.77, ""),
    ("Selain itu,", 24.3, ""), ("kurang TIDUR,", 25.16, "k"), ("tekanan kerja,", 26.2, ""), ("dan beban", 27.53, ""),
    ("MENTAL juga", 27.96, "k"), ("boleh menyebabkan", 28.8, ""), ("seseorang lebih", 29.6, ""), ("mudah terasa", 30.54, ""),
    ("atau cepat", 31.42, ""), ("MARAH.", 32.12, "k"),
    ("Tapi", 32.82, ""), ("menariknya,", 33.27, ""), ("LELAKI pun", 34.44, "k"), ("sebenarnya boleh", 35.1, ""),
    ("mengalami", 36.21, ""), ("perubahan EMOSI.", 36.88, "k"),
    ("Cuma setiap", 38.02, ""), ("individu mempunyai", 38.72, ""), ("cara BERBEZA", 39.95, "k"), ("untuk menguruskan", 40.74, ""), ("PERASAAN.", 41.9, "k"),
    ("Jadi,", 42.86, ""), ("bukan semua", 43.31, ""), ("PEREMPUAN", 44.06, "k"), ("cepat MARAH.", 44.64, "k"),
    ("Kadang-kadang,", 45.66, ""), ("apa yang kita", 46.59, ""), ("nampak sebagai", 47.3, ""), ("MARAH,", 48.17, "k"),
    ("sebenarnya mungkin", 48.54, ""), ("datang daripada", 49.79, ""), ("TEKANAN", 50.48, "k"), ("yang kita", 50.91, ""), ("tak nampak.", 51.4, ""),
    ("Haa,", 52.26, ""), ("sekarang", 52.69, ""), ("dah TAHU,", 53.69, "k"),
    ("follow untuk", 54.28, ""), ("lebih banyak", 55.11, ""), ("fakta menarik", 55.96, ""), ("dalam", 56.88, ""), ("BARU TAHU.", 57.25, "k"),
]
ENDS = {
    "Eh, korang": 0.7, "Sebenarnya,": 9.6, "WANITA.": 14.2, "MARAH.": 32.7, "menariknya,": 34.2, "emosi.": 24.2,
    "Haa,": 52.7, "sekarang": 53.6, "BARU TAHU.": 58.0, "PERASAAN.": 42.7, "tak nampak.": 52.1,
}
