# Video 03 "Kenapa keyboard QWERTY" – overrides SC / TOTAL / SCENES / CAPS / ENDS
import math

TOTAL = 55.55
SC = [
    ("s1", 0.0), ("s2", 3.48), ("s3", 6.36), ("s4", 11.6), ("s5", 21.28),
    ("s6", 33.4), ("s7", 42.4), ("s8", 49.32), ("s9", 51.36),
]
OL6 = OL.replace("10", "6")
OL8 = OL.replace("10", "8")
SKIN3 = "#efc8a0"


def keycap(idn, x, y, s, letter, fill="#fff", fs=None):
    fs = fs or int(s * 0.52)
    return (f'<g id="{idn}"><rect x="{x}" y="{y+8}" width="{s}" height="{s}" rx="{s*0.18:.0f}" fill="#141414"/>'
            f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*0.18:.0f}" fill="{fill}" stroke="#141414" stroke-width="8"/>'
            f'<text x="{x+s/2}" y="{y+s*0.68:.0f}" text-anchor="middle" font-family="Archivo Black" font-size="{fs}" fill="#141414">{letter}</text></g>')


def inventor(p, x, y, s, mouth="smile"):
    """Generic cartoon inventor (original, not a likeness): bowler hat, moustache, round glasses, brown vest."""
    mouths = {
        "smile": f'<path d="M-40 150 Q0 185 40 150" fill="none" {OL8}/>',
        "grin": f'<path d="M-60 140 Q0 215 60 140 Z" fill="#8b2323" {OL8}/>',
        "open": f'<ellipse cx="0" cy="160" rx="30" ry="36" fill="#7a1f1f" {OL8}/>',
        "worry": f'<path d="M-40 175 Q0 140 40 175" fill="none" {OL8}/>',
        "flat": f'<path d="M-38 160 L38 160" fill="none" {OL8}/>',
    }
    mo = "".join(f'<g id="{p}mo_{k}" opacity="{1 if k == mouth else 0}">{v}</g>' for k, v in mouths.items())

    def eye(side, cx):
        return (f'<ellipse cx="{cx}" cy="-15" rx="46" ry="54" fill="#fff" stroke="#141414" stroke-width="8"/>'
                f'<g id="{p}pup{side}"><circle cx="{cx}" cy="-12" r="17" fill="#141414"/><circle cx="{cx-5}" cy="-21" r="5.5" fill="#fff"/></g>'
                f'<ellipse cx="{cx}" cy="-15" rx="64" ry="70" fill="none" stroke="#8a5a2b" stroke-width="8"/>')
    return f'''
<g transform="translate({x} {y}) scale({s})">
 <g id="{p}m">
  <path d="M-235 340 Q-245 205 -150 192 L150 192 Q245 205 235 340 L235 470 L-235 470 Z" fill="#fffaf0" {OL}/>
  <path d="M-150 192 L-30 470 L-235 470 L-235 340 Q-245 205 -150 192Z M150 192 L30 470 L235 470 L235 340 Q245 205 150 192Z" fill="#8a5a2b" {OL}/>
  <path d="M-34 214 L0 250 L-34 286Z M34 214 L0 250 L34 286Z" fill="#d63a2b" {OL8}/><circle cx="0" cy="250" r="14" fill="#d63a2b" {OL8}/>
  <circle cx="-120" cy="340" r="11" fill="#f2c230"/><circle cx="120" cy="340" r="11" fill="#f2c230"/>
  <rect x="-48" y="150" width="96" height="62" fill="{SKIN3}" {OL}/>
  <ellipse cx="-246" cy="20" rx="34" ry="48" fill="{SKIN3}" {OL}/><ellipse cx="246" cy="20" rx="34" ry="48" fill="{SKIN3}" {OL}/>
  <ellipse cx="0" cy="0" rx="252" ry="224" fill="{SKIN3}" {OL}/>
  <ellipse cx="-160" cy="95" rx="34" ry="21" fill="#ef7f6e" opacity=".55"/><ellipse cx="160" cy="95" rx="34" ry="21" fill="#ef7f6e" opacity=".55"/>
  {eye("L", -92)}{eye("R", 92)}
  <path d="M-30 -15 L30 -15" stroke="#8a5a2b" stroke-width="8"/>
  <path id="{p}browL" d="M-150 -98 Q-95 -128 -40 -102" fill="none" {OL}/><path id="{p}browR" d="M150 -98 Q95 -128 40 -102" fill="none" {OL}/>
  <g transform="translate(0 0)">{mo}</g>
  <path d="M-165 105 Q-90 55 0 95 Q90 55 165 105 Q92 150 0 118 Q-92 150 -165 105Z" fill="#3a2a1a" {OL8}/>
  <ellipse cx="0" cy="-150" rx="285" ry="42" fill="#4b3a2a" {OL}/>
  <path d="M-185 -150 Q-185 -350 0 -350 Q185 -350 185 -150Z" fill="#4b3a2a" {OL}/>
  <path d="M-186 -170 Q0 -135 186 -170" fill="none" stroke="#141414" stroke-width="26"/>
 </g>
</g>'''


def typewriter(p):
    r1 = "".join(f'<g><circle cx="{164+i*76}" cy="945" r="31" fill="#fffdf5" {OL8}/><text x="{164+i*76}" y="957" text-anchor="middle" font-family="Archivo Black" font-size="32" fill="#141414">{c}</text></g>' for i, c in enumerate("QWERTYUIOP"))
    r2 = "".join(f'<g><circle cx="{202+i*76}" cy="1018" r="31" fill="#fffdf5" {OL8}/><text x="{202+i*76}" y="1030" text-anchor="middle" font-family="Archivo Black" font-size="32" fill="#141414">{c}</text></g>' for i, c in enumerate("ASDFGHJKL"))
    lines = "".join(f'<rect id="{p}_l{i}" x="370" y="{520+i*72}" width="340" height="18" rx="9" fill="#9d9788"/>' for i in range(3))
    return f'''<g id="{p}">
 <g id="{p}_paper"><rect x="330" y="400" width="420" height="400" rx="8" fill="#fffdf5" {OL}/>{lines}</g>
 <rect x="190" y="760" width="700" height="78" rx="39" fill="#1d1d1d" {OL}/>
 <circle cx="158" cy="799" r="38" fill="#cfd6e0" {OL}/><circle cx="922" cy="799" r="38" fill="#cfd6e0" {OL}/>
 <g id="{p}_arm"><path d="M540 870 L540 800" stroke="#141414" stroke-width="22" stroke-linecap="round"/><rect x="518" y="770" width="44" height="44" rx="8" fill="#cfd6e0" {OL8}/></g>
 <path d="M120 860 L960 860 L1020 1090 L60 1090Z" fill="#3a4252" {OL}/>
 {r1}{r2}
 <rect x="330" y="1055" width="420" height="22" rx="11" fill="#fffdf5" {OL8}/>
</g>'''


def laptop():
    keys = "".join(f'<rect x="{-150+c*27}" y="{70+r*14}" width="22" height="10" rx="3" fill="#fff" stroke="#141414" stroke-width="3"/>' for r in range(3) for c in range(12))
    return f'''<rect x="-130" y="-120" width="260" height="180" rx="16" fill="#2b2f3a" {OL8}/><rect x="-110" y="-102" width="220" height="144" rx="6" fill="#bfe9ff"/>
<path d="M-60 -60 L60 -60 M-60 -30 L30 -30 M-60 0 L50 0" stroke="#7da6c9" stroke-width="10" stroke-linecap="round"/>
<path d="M-180 60 L180 60 L205 125 L-205 125Z" fill="#cfd6e0" {OL8}/>{keys}'''


def phone():
    rows = ""
    for r, n in enumerate([10, 9, 7]):
        off = [0, 6, 18][r]
        rows += "".join(f'<rect x="{-56+off+c*11.5:.1f}" y="{40+r*30}" width="9" height="22" rx="3" fill="#fff" stroke="#141414" stroke-width="2.5"/>' for c in range(n))
    return f'''<rect x="-78" y="-170" width="156" height="330" rx="34" fill="#2b2f3a" {OL8}/><rect x="-64" y="-150" width="128" height="290" rx="20" fill="#bfe9ff"/>
<rect x="-64" y="25" width="128" height="115" rx="12" fill="#e8eef5"/>{rows}<path d="M-40 -100 L40 -100 M-40 -70 L20 -70" stroke="#7da6c9" stroke-width="9" stroke-linecap="round"/>'''


# ------------------------------------------------------------------ scenes
def s1():
    rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
    keys = ""
    for r, row in enumerate(rows):
        off = [0, 40, 100][r]
        for i, c in enumerate(row):
            kid = f"s1_r{r}_{i}" if r == 0 else f"s1_r{r}_{i}"
            keys += keycap(kid, 75 + off + i * 94, 650 + r * 108, 84, c)
    space = '<g id="s1_sp"><rect x="280" y="974" width="520" height="84" rx="16" fill="#141414"/><rect x="280" y="966" width="520" height="84" rx="16" fill="#fff" stroke="#141414" stroke-width="8"/></g>'
    return f'''
{rays("s1_rays", 540, 600, "#ffc83d", "#ffb11a")}
{mascot("s1", 540, 450, 0.72, "open")}
<g id="s1_kb"><rect x="45" y="610" width="990" height="560" rx="46" fill="#2b2f3a" {OL}/>{keys}{space}</g>
<g id="s1_q1"><text x="840" y="420" font-family="Archivo Black" font-size="190" fill="#a8151a" stroke="#141414" stroke-width="14" paint-order="stroke" transform="rotate(14 840 420)">?</text></g>
<g id="s1_q2"><text x="90" y="400" font-family="Archivo Black" font-size="150" fill="#a8151a" stroke="#141414" stroke-width="14" paint-order="stroke" transform="rotate(-14 90 400)">?</text></g>
'''


def s2():
    ks = ""
    xs = [60, 252, 444, 636, 828]
    for i, (c, x) in enumerate(zip(["A", "B", "C", "", "Z"], xs)):
        if c:
            ks += keycap(f"s2_k{i}", x, 560, 170, c, fs=110)
    dots = '<g id="s2_dots"><text x="745" y="690" text-anchor="middle" font-family="Archivo Black" font-size="140" fill="#141414">...</text></g>'
    return f'''
{rays("s2_rays", 540, 640, "#cbbcff", "#bda9ff")}
{ks}{dots}
<g id="s2_no"><circle cx="150" cy="420" r="82" fill="#e0262b" {OL}/><path d="M112 382 L188 458 M188 382 L112 458" stroke="#fff" stroke-width="24" stroke-linecap="round"/></g>
<g id="s2_x"><path d="M120 480 L960 860 M960 480 L120 860" stroke="#141414" stroke-width="84" stroke-linecap="round"/><path d="M120 480 L960 860 M960 480 L120 860" stroke="#e0262b" stroke-width="62" stroke-linecap="round" opacity=".92"/></g>
{mascot("s2", 540, 1130, 0.75, "flat")}
'''


def s3():
    return f'''
<rect width="1080" height="1920" fill="#d8b684"/>
<rect width="1080" height="1920" fill="url(#s3_vig)"/>
<defs><radialGradient id="s3_vig" cx="50%" cy="45%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#5a3b14" stop-opacity=".55"/></radialGradient></defs>
<g id="s3_tw0">{typewriter("s3tw")}</g>
<g id="s3_t0"><text x="800" y="470" font-family="Archivo Black" font-size="90" fill="#fff" stroke="#141414" stroke-width="12" paint-order="stroke" transform="rotate(10 800 470)">TAK!</text></g>
<g id="s3_t1"><text x="860" y="600" font-family="Archivo Black" font-size="70" fill="#ffd400" stroke="#141414" stroke-width="12" paint-order="stroke" transform="rotate(-8 860 600)">tak!</text></g>
<g id="s3_t2"><text x="230" y="520" font-family="Archivo Black" font-size="80" fill="#fff" stroke="#141414" stroke-width="12" paint-order="stroke" transform="rotate(-10 230 520)">TAK!</text></g>
'''


def s4():
    keys = "".join(keycap(f"s4_k{i}", 506 + i * 86, 930, 76, c, fs=40) for i, c in enumerate("QWERTY"))
    return f'''
<rect width="1080" height="1920" fill="#1e4fd8"/>
<defs><pattern id="s4_grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0 L0 0 L0 60" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="3"/></pattern></defs>
<rect width="1080" height="1920" fill="url(#s4_grid)"/>
<g id="s4_date"><rect x="250" y="250" width="580" height="130" rx="30" fill="#fffaf0" {OL}/><text x="540" y="345" text-anchor="middle" font-family="Archivo Black" font-size="80" fill="#1e4fd8">ABAD KE-19</text></g>
<g id="s4_name"><path d="M80 470 L1000 470 L1000 650 L80 650 L130 560Z" fill="#ffd23f" {OL}/>
 <text x="560" y="540" text-anchor="middle" font-family="Archivo Black" font-size="58" fill="#141414">CHRISTOPHER</text>
 <text x="560" y="618" text-anchor="middle" font-family="Archivo Black" font-size="58" fill="#141414">LATHAM SHOLES</text></g>
{inventor("s4i", 250, 1040, 0.8, "smile")}
<g id="s4_scroll"><rect x="470" y="780" width="560" height="330" rx="14" fill="#f4f1ff" {OL}/><rect x="450" y="765" width="40" height="360" rx="20" fill="#d8b684" {OL}/><rect x="1010" y="765" width="40" height="360" rx="20" fill="#d8b684" {OL}/>
 <path d="M520 840 L960 840 M520 880 L760 880" stroke="#9fb4e8" stroke-width="10" stroke-linecap="round"/>{keys}</g>
'''


def s5():
    arms = ""
    for i in range(7):
        px = 240 + i * 100
        arms += f'''<g id="s5_a{i}"><path d="M{px} 1080 L540 575" stroke="#141414" stroke-width="36" stroke-linecap="round"/><path d="M{px} 1080 L540 575" stroke="#cfd6e0" stroke-width="18" stroke-linecap="round"/>
 <circle cx="540" cy="560" r="36" fill="#cfd6e0" {OL8}/><text x="540" y="575" text-anchor="middle" font-family="Archivo Black" font-size="40" fill="#141414">{"QWERTYU"[i]}</text></g>'''
    pl = "".join(f'<text id="s5_pl{i}" x="{330+i*52}" y="520" text-anchor="middle" font-family="Archivo Black" font-size="56" fill="#141414" opacity="0">{"QWERTYUIO"[i]}</text>' for i in range(9))
    spk = f'<g id="s5_spk">{star(540, 610, 120, "#ffd400")}<text x="540" y="650" text-anchor="middle" font-family="Archivo Black" font-size="110" fill="#e0262b" stroke="#141414" stroke-width="10" paint-order="stroke">!</text></g>'
    return f'''
<rect width="1080" height="1920" fill="#1b2a49"/>
<g id="s5_cam" data-layout-allow-overlap>
 <rect x="270" y="440" width="540" height="120" rx="12" fill="#fffdf5" {OL}/>{pl}
 <rect x="160" y="1060" width="760" height="70" rx="35" fill="#5b6577" {OL}/>
 {arms}
 {"".join(f'<circle cx="{240+i*100}" cy="1080" r="14" fill="#141414"/>' for i in range(7))}
 {spk}
</g>
{mascot("s5", 880, 1190, 0.5, "worry")}
'''


def s6():
    cards = ""
    specs = [(190, "tw"), (540, "lp"), (890, "ph")]
    for i, (cx, kind) in enumerate(specs):
        if kind == "tw":
            icon = f'<g transform="translate({cx-540*0.3:.1f} {690-755*0.3:.1f}) scale(.3)">{typewriter("s6tw")}</g>'
        elif kind == "lp":
            icon = f'<g transform="translate({cx} 680) scale(.82)">{laptop()}</g>'
        else:
            icon = f'<g transform="translate({cx} 690) scale(.95)">{phone()}</g>'
        strip = "".join(keycap(f"s6_k{i}_{j}", cx - 147 + j * 50, 870, 44, c, fs=24) for j, c in enumerate("QWERTY"))
        cards += f'''<g id="s6_c{i}"><rect x="{cx-160}" y="440" width="320" height="560" rx="36" fill="#fffdf5" {OL}/>{icon}{strip}
 <g id="s6_ok{i}" opacity="0"><circle cx="{cx+110}" cy="500" r="44" fill="#27b35a" {OL8}/><path d="M{cx+90} 500 L{cx+106} 518 L{cx+132} 484" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g></g>'''
    arrows = "".join(f'<path d="M{x} 720 l40 0 m-18 -18 l18 18 l-18 18" fill="none" stroke="#141414" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" id="s6_ar{i}"/>' for i, x in enumerate([335, 685]))
    return f'''
<rect width="1080" height="1920" fill="#d8b684"/>
<rect id="s6_bg2" width="1080" height="1920" fill="#6fd0ff"/>
<rect id="s6_bg3" width="1080" height="1920" fill="#8ee3b0"/>
{cards}{arrows}
'''


def s7():
    pages = "".join(f'''<g id="s7_pg{i}"><g transform="translate(540 760) rotate({[-6,4,-3,7,-8,5,-4,6][i]})"><rect x="-190" y="-230" width="380" height="440" rx="22" fill="#fffdf5" {OL}/><rect x="-190" y="-230" width="380" height="96" rx="22" fill="#e0262b" {OL}/>
 <circle cx="-100" cy="-232" r="12" fill="#141414"/><circle cx="100" cy="-232" r="12" fill="#141414"/><path d="M-120 -50 L120 -50 M-120 10 L120 10 M-120 70 L40 70" stroke="#d6d2c4" stroke-width="12" stroke-linecap="round"/></g></g>''' for i in range(8))
    kb = "".join(keycap(f"s7_k{i}", 0, 0, 56, c, fs=30) for i, c in enumerate("QWERTY")).replace('<g id=', '<g transform="translate(0 0)" id=')
    return f'''
{rays("s7_rays", 540, 760, "#ff7a59", "#ff6a45")}
{mascot("s7", 540, 1130, 0.78, "smile")}
<g id="s7_bub"><g transform="translate(60 300)"><rect x="0" y="0" width="440" height="190" rx="70" fill="#fff" {OL}/><path d="M300 186 L350 250 L380 184Z" fill="#fff" {OL}/>
 {"".join(keycap(f"s7_k{i}", 30 + i * 64, 52, 56, c, fs=30) for i, c in enumerate("QWERTY"))}</g></g>
{pages}
<g id="s7_num"><text id="s7_n" x="540" y="640" text-anchor="middle" font-family="Archivo Black" font-size="300" fill="#ffd400" stroke="#141414" stroke-width="26" paint-order="stroke">100+</text>
 <text id="s7_th" x="540" y="820" text-anchor="middle" font-family="Archivo Black" font-size="130" fill="#fff" stroke="#141414" stroke-width="20" paint-order="stroke">TAHUN</text></g>
'''


def s8():
    bulb = f'''<g id="s8_bulb" transform="translate(0 -470)"><g id="s8_bulbi">
 <path d="M0 -150 Q-110 -150 -110 -40 Q-110 20 -60 60 L-60 110 L60 110 L60 60 Q110 20 110 -40 Q110 -150 0 -150Z" fill="#ffe14d" {OL}/>
 <rect x="-52" y="110" width="104" height="30" rx="8" fill="#9aa3b2" {OL}/>
 <path d="M-170 -90 L-230 -110 M170 -90 L230 -110 M0 -210 L0 -270 M-130 -190 L-170 -240 M130 -190 L170 -240" stroke="#141414" stroke-width="12" stroke-linecap="round"/></g></g>'''
    return f'''
{rays("s8_rays", 540, 800, "#8ee3b0", "#7bd9a2")}
{mascot("s8", 540, 880, 1.1, "smile", extra=bulb)}
'''


def s9():
    return f'''
<rect width="1080" height="1920" fill="#19a39a"/>
<g id="s9_band"><rect x="-200" y="640" width="1500" height="380" fill="#ffc83d" {OL} transform="rotate(-5 540 830)"/></g>
{mascot("s9", 540, 330, 0.72, "grin")}
<g id="s9_brand"><text id="s9_t1" x="540" y="790" text-anchor="middle" font-family="Archivo Black" font-size="150" fill="#fff" stroke="#141414" stroke-width="18" paint-order="stroke">BARU</text>
<text id="s9_t2" x="540" y="950" text-anchor="middle" font-family="Archivo Black" font-size="150" fill="#e0262b" stroke="#141414" stroke-width="18" paint-order="stroke">TAHU</text></g>
<g id="s9_btn"><rect x="300" y="1070" width="480" height="120" rx="60" fill="#e0262b" {OL}/>
 <text x="540" y="1151" text-anchor="middle" font-family="Archivo Black" font-size="64" fill="#fff">FOLLOW</text></g>
{hand("s9_hand", 730, 1235, 1.0, thumb=False)}
'''


SCENES = {f"s{i}": globals()[f"s{i}"] for i in range(1, 10)}

CAPS = [
    ("Kenapa keyboard", 0.06, ""), ("komputer kita", 0.83, ""), ("susun huruf", 1.76, ""), ("ikut QWERTY?", 2.52, "k"),
    ("Bukannya", 3.58, ""), ("A, B, C", 4.14, ""), ("sampai Z.", 4.9, ""),
    ("Sebenarnya", 6.46, ""), ("susunan ini", 7.26, ""), ("berasal daripada", 8.13, ""), ("MESIN TAIP", 9.41, "k"),
    ("pada zaman", 10.19, ""), ("dahulu.", 10.98, ""),
    ("Pada abad", 11.7, ""), ("KE-19,", 12.45, "k"), ("pencipta", 13.2, ""), ("mesin taip,", 13.72, ""), ("Christopher", 14.36, ""),
    ("LATHAM SHOLES,", 15.1, "k"), ("membangunkan", 16.06, ""), ("susunan papan", 16.84, ""), ("kekunci yang", 17.7, ""),
    ("akhirnya menjadi", 18.72, ""), ("asas kepada", 19.9, ""), ("QWERTY.", 20.76, "k"),
    ("Antara faktor", 21.38, ""), ("yang mempengaruhi", 22.13, ""), ("reka bentuk", 23.11, ""), ("awalnya ialah", 23.82, ""),
    ("untuk mengurangkan", 24.61, ""), ("masalah mekanisme", 25.75, ""), ("mesin taip", 26.82, ""),
    ("yang boleh", 27.75, ""), ("TERSANGKUT", 28.1, "k"), ("apabila beberapa", 28.82, ""), ("kekunci ditekan", 29.85, ""),
    ("terlalu CEPAT", 30.81, "k"), ("secara berturut-turut.", 31.76, ""),
    ("Walaupun teknologi", 33.5, ""), ("dah berubah", 34.53, ""), ("daripada mesin", 35.17, ""), ("taip kepada", 35.94, ""),
    ("KOMPUTER", 36.89, "k"), ("dan telefon", 37.24, ""), ("pintar,", 38.02, ""), ("susunan QWERTY", 38.58, "k"),
    ("masih KEKAL", 39.63, "k"), ("digunakan", 40.49, ""), ("sampai hari ini.", 41.29, ""),
    ("Bayangkan,", 42.5, ""), ("susunan huruf", 43.53, ""), ("yang kita guna", 44.33, ""), ("setiap hari", 45.16, ""),
    ("sebenarnya", 45.94, ""), ("mempunyai sejarah", 46.62, ""), ("lebih", 47.8, ""), ("100 TAHUN!", 48.22, "k"),
    ("Hah,", 49.42, ""), ("sekarang", 49.88, ""), ("dah TAHU.", 50.64, "k"),
    ("Follow untuk", 51.46, ""), ("lebih banyak", 52.22, ""), ("fakta menarik", 53.06, ""), ("dalam", 53.93, ""), ("BARU TAHU!", 54.4, "k"),
]
ENDS = {
    "QWERTY.": 21.28, "secara berturut-turut.": 33.4, "sampai hari ini.": 42.4, "Bayangkan,": 43.45,
    "100 TAHUN!": 49.3, "BARU TAHU!": 55.5, "dahulu.": 11.55, "sampai Z.": 6.3, "dah TAHU.": 51.4,
}
