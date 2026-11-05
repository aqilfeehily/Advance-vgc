"""PER VIDEO: the PiP graphic panels, the FULL slams and the end card.
These are the "Bisnes Baru Nak AI" scenes: examples of the GRAMMAR (counter + fanned cards, funnel, flow lines,
shattering tiles, checklists, phone mock, meter, chat UI, blueprint, metaphor). For a new video write new scenes from
what the presenter says (references/scene_playbook.md); reuse the kit pieces, not this choreography.

Each scene returns dict(a=start, html=..., js=...). Ids are prefixed per scene and must be unique in the page.
Panel content area: title at y~205, content between y~300 and 1180 (the PiP card starts at 1372, captions at 1296)."""
import os
from kit import C, fit, GLOW_C, GLOW_Y, HF, SHADOW, W, Y, anchor, card, chip, icon, label, noise, shake_js, slam, tick_svg, title
from timing import END_CARD, S, T, TOTAL


def t(k, d=0.0): return f"{T[k] + d:.4f}"
def n(x): return f"{x:.4f}"


def panel_open(pid): return f'<div id="{pid}" class="layer panel hide"><div id="{pid}_d" class="layer panel">'
PANEL_CLOSE = "</div></div>"
FAINT = dict(color="rgba(255,255,255,0.08)", ink="rgba(255,255,255,0.7)")
YFAINT = dict(color="rgba(255,230,0,0.14)", ink=C["yellow"])


def vid(id_, src, a, dur, b=None, extra=""):
    """muted B-roll clip; starts from its first frame when the card appears (time the video, not its wrapper)"""
    d = min(dur, (b - a) if b else dur)
    return f'<video id="{id_}" class="media" src="assets/{src}" muted playsinline data-start="{a:.3f}" data-duration="{d:.3f}" style="{extra}"></video>'


def img(src, pos="50% 50%"): return f'<img class="media" src="assets/{src}" alt="" style="object-position:{pos}">'


def yoyo(sel, a, b, prop, v0, v1, half, ease="sine.inOut"):
    """finite back-and-forth motion between a and b (seek-safe replacement for sin(t) wobble)"""
    reps = max(0, int((b - a) / half) - 1)
    return (f"tl.fromTo('{sel}', {{ {prop}: {v0} }}, {{ {prop}: {v1}, duration: {half:.3f}, ease: '{ease}', repeat: {reps}, yoyo: true, "
            f"immediateRender: false }}, {a:.4f});")



def row(id_, y, text, tag="", w=900, h=150, hi=False, ic="eye"):
    b = C["yellow"] if hi else None
    inner = (f'<div style="display:flex;align-items:center;gap:26px;padding:0 34px;width:100%;height:100%">'
             f'<div style="width:90px;height:90px;border-radius:50%;background:{C["blue"]};display:flex;align-items:center;justify-content:center;flex:none">{icon(ic, 54, "#fff", 4.5)}</div>'
             f'<div class="heavy" style="font-size:46px;white-space:nowrap;flex:1">{text}</div>'
             + (f'<div class="chip" style="background:{C["yellow"]};color:{C["navy"]};border:none;font-size:30px;padding:10px 26px">{tag}</div>' if tag else "") + '</div>')
    return card(id_, f"left:{(1080 - w) // 2}px;top:{y}px;width:{w}px;height:{h}px", inner, border=b)


def feed():
    a, b = S["feed"]
    ys = [480, 670, 860]
    h = [panel_open("fd"), title("fd_t", "Instagram *dulu*")]
    for i, (nm, y) in enumerate(zip(("Akaun A", "Akaun B", "Akaun C"), ys)):
        h.append(row(f"fd_r{i}", y, nm, "FOLLOW"))
    h += [chip("fd_c", 540, 1090, "feed = orang yang kita follow", color=C["yellow"], ink=C["navy"], size=34), PANEL_CLOSE]
    ts = [T["instagram"] + 0.15, T["instagram"] + 0.6, T["feed"] - 0.1]
    j = [f"panel('fd', {n(a)}, {n(b)});", f"title('fd_t', {n(a + 0.05)});"]
    for i, tt in enumerate(ts):
        j.append(f"tl.fromTo('#fd_r{i}', {{ x: -120 }}, {{ x: 0, duration: 0.3, ease: E.out, immediateRender: false }}, {n(tt)}); fadeIn('fd_r{i}', {n(tt)}, 0.15);")
    j.append(f"pop('fd_c', {t('feed', 0.25)});")
    return dict(a=a, html="\n".join(h), js="\n".join(j))


def feed2():
    a, b = S["feed2"]
    h = [panel_open("f2"), title("f2_t", "Orang follow *hilang*")]
    for i, (nm, y) in enumerate(zip(("Akaun A", "Akaun B", "Akaun C"), (480, 670, 860))):
        h.append(row(f"f2_r{i}", y, nm, "FOLLOW"))
    h += [anchor(540, 760, f'<div id="f2_q" class="heavy hide" style="font-size:230px;color:{C["yellow"]};text-shadow:{GLOW_Y};white-space:nowrap">TAK NAMPAK</div>'.replace("230px", "118px")), PANEL_CLOSE]
    j = [f"panel('f2', {n(a)}, {n(b)});", f"title('f2_t', {n(a + 0.05)});"]
    for i in range(3):
        j.append(f"tl.fromTo('#f2_r{i}', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, ease: E.out, immediateRender: false }}, {n(a + 0.1 + i * 0.08)});")
        j.append(f"tl.to('#f2_r{i}', {{ opacity: 0.18, filter: 'blur(6px)', duration: 0.4, ease: 'power2.out' }}, {t('orangFollow', 0.1 + i * 0.1)});")
    j.append(f"popBlur('f2_q', {t('takNampak', -0.05)}, 0.3, 1.6);")
    j.append(shake_js("#f2_q", T["takNampak"] - 0.05, 0.2, 8, 3))
    return dict(a=a, html="\n".join(h), js="\n".join(j))


def terms():
    a, b = S["terms"]
    h = [panel_open("tm"), title("tm_t", "Bukan lagi *social media*", size=58),
         card("tm_c", "left:120px;top:560px;width:840px;height:260px", anchor(420, 130, f'<div class="heavy" style="font-size:96px;white-space:nowrap">SOCIAL MEDIA</div>'), cls="hide"),
         f'<div id="tm_x" style="position:absolute;left:150px;top:680px;width:780px;height:14px;border-radius:7px;background:{C["yellow"]};box-shadow:{GLOW_Y};opacity:0;transform-origin:0 50%"></div>',
         chip("tm_n", 540, 960, "dah bukan itu", color=C["yellow"], ink=C["navy"], size=40), PANEL_CLOSE]
    j = [f"panel('tm', {n(a)}, {n(b)});", f"title('tm_t', {n(a + 0.05)});", f"pop('tm_c', {n(a + 0.1)}, 0.3);",
         f"tl.set('#tm_x', {{ opacity: 1 }}, {t('social', 0.1)}); tl.fromTo('#tm_x', {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: E.out, immediateRender: false }}, {t('social', 0.1)});",
         f"pop('tm_n', {t('social', 0.5)});"]
    return dict(a=a, html="\n".join(h), js="\n".join(j))


def gary():
    a, b = S["gary"]
    ph = ('<div id="gv_ph" style="position:absolute;inset:0;overflow:hidden"><img id="gv_im" src="assets/img/garyvee.jpg" alt="" '
          'style="position:absolute;left:-30px;top:-10px;width:700px;height:700px;object-fit:cover"></div>')
    h = [panel_open("gv"), title("gv_t", "Terms dari *Gary Vee*", size=60),
         anchor(540, 770, f'<div id="gv_glow" style="width:820px;height:820px;border-radius:50%;background:radial-gradient(circle, rgba(0,207,245,0.35), rgba(0,207,245,0) 62%)"></div>'),
         f'<div id="gv_card" class="hide" style="position:absolute;left:190px;top:440px;width:700px;height:640px;border-radius:40px;overflow:hidden;border:4px solid {C["yellow"]};box-shadow:0 30px 70px rgba(0,0,0,0.6), {GLOW_Y}">{ph}</div>',
         chip("gv_n", 540, 1135, "GARY VEE", color=C["yellow"], ink=C["navy"], size=46),
         chip("gv_m", 540, 1135, "social media master", size=40),
         label("gv_s", 540, 1182, "Foto: Wikimedia Commons (public domain)", size=22), PANEL_CLOSE]
    j = [f"panel('gv', {n(a)}, {n(b)}, 1.1);", f"title('gv_t', {n(a + 0.05)});",
         f"tl.fromTo('#gv_card', {{ rotation: -7, y: 160, scale: 0.7 }}, {{ rotation: 0, y: 0, scale: 1, duration: 0.45, ease: E.back, immediateRender: false }}, {t('gary', -0.25)});",
         f"tl.fromTo('#gv_card', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15, ease: 'none', immediateRender: false }}, {t('gary', -0.25)});",
         f"tl.fromTo('#gv_im', {{ scale: 1.0, x: 0, y: 0 }}, {{ scale: 1.22, x: 14, y: -10, duration: {b - T['gary']:.3f}, ease: 'none', immediateRender: false }}, {t('gary', -0.2)});",
         yoyo("#gv_card", T["gary"] + 0.5, b - 0.3, "rotation", -1.5, 1.5, 1.4),
         yoyo("#gv_glow", a, b, "scale", 0.92, 1.1, 1.0),
         f"pop('gv_n', {t('gary', 0.1)}); tl.to('#gv_n', {{ opacity: 0, duration: 0.15, ease: E.in }}, {t('master', -0.05)});",
         f"pop('gv_m', {t('master', 0.0)});", f"fadeIn('gv_s', {t('gary', 0.4)}, 0.4); tl.set('#gv_s', {{ opacity: 0.55 }}, {t('gary', 0.85)});"]
    return dict(a=a, html="\n".join(h), js="\n".join(j))


def follow():
    a, b = S["follow"]
    arr = (f'<svg id="fl_ar" class="hide" width="170" height="60" viewBox="0 0 170 60" style="position:absolute;left:455px;top:640px" fill="none" stroke="{C["yellow"]}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">'
           f'<path id="fl_arp" d="M6 30 H150 M126 8 L152 30 L126 52"/></svg>')
    h = [panel_open("fl"), title("fl_t", "Social *media*"),
         card("fl_a", "left:70px;top:560px;width:360px;height:220px", anchor(180, 110, '<div class="heavy" style="font-size:72px">KITA</div>')),
         card("fl_b", "left:650px;top:560px;width:360px;height:220px", anchor(180, 110, '<div class="heavy" style="font-size:72px">DIA</div>')), arr,
         chip("fl_c", 540, 930, "follow = nampak", color=C["yellow"], ink=C["navy"], size=46), PANEL_CLOSE]
    j = [f"panel('fl', {n(a)}, {n(b)});", f"title('fl_t', {n(a + 0.05)});", f"pop('fl_a', {n(a + 0.15)});", f"pop('fl_b', {n(a + 0.3)});",
         f"fadeIn('fl_ar', {t('follow', -0.1)}, 0.2); tl.fromTo('#fl_ar', {{ x: -30 }}, {{ x: 0, duration: 0.3, ease: E.out, immediateRender: false }}, {t('follow', -0.1)});",
         f"pop('fl_c', {t('nampak', -0.05)});"]
    return dict(a=a, html="\n".join(h), js="\n".join(j))


def interest():
    a, b = S["interest"]
    pos = [(200, 560, "cam"), (880, 560, "chart"), (200, 960, "cart"), (880, 960, "rocket")]
    h = [panel_open("it"), title("it_t", "Semua *related*"),
         anchor(540, 760, f'<div id="it_c" class="hide" style="width:330px;height:330px;border-radius:50%;border:6px solid {C["yellow"]};box-shadow:{GLOW_Y};background:rgba(255,230,0,0.1);display:flex;align-items:center;justify-content:center"><div class="heavy" style="font-size:54px;text-align:center;line-height:1.1">INTEREST<br>KITA</div></div>')]
    for i, (x, y, ic) in enumerate(pos):
        h.append(anchor(x, y, f'<div id="it_k{i}" class="hide" style="width:190px;height:190px;border-radius:36px;background:linear-gradient(180deg,{C["card"]},{C["navy2"]});border:2px solid {C["line"]};display:flex;align-items:center;justify-content:center">{icon(ic, 100, C["cyan"], 4)}</div>'))
    h += [chip("it_n", 540, 1130, "Contoh visual", size=26, **FAINT), PANEL_CLOSE]
    j = [f"panel('it', {n(a)}, {n(b)});", f"title('it_t', {n(a + 0.05)});"]
    for i, (x, y, ic) in enumerate(pos):
        j.append(f"pop('it_k{i}', {n(a + 0.15 + i * 0.12)}, 0.3);")
        j.append(f"tl.to('#it_k{i}', {{ x: {int((540 - x) * 0.52)}, y: {int((760 - y) * 0.52)}, scale: 0.7, duration: 0.5, ease: E.io }}, {t('related', 0.0 + i * 0.05)});")
    j += [f"popBlur('it_c', {t('related', 0.15)}, 0.3, 0.5);", f"fadeIn('it_n', {n(a + 0.5)});"]
    return dict(a=a, html="\n".join(h), js="\n".join(j))


def search(pid, key, ttl, query, tile_txt, tkey, extra_label=None):
    a, b = S[key]
    tiles = [(95, 700), (555, 700), (95, 930), (555, 930)]
    bar = (f'<div style="display:flex;align-items:center;gap:22px;padding:0 34px;height:100%">{icon("eye", 54, C["cyan"], 4)}'
           f'<div id="{pid}_tx" style="overflow:hidden;white-space:nowrap;width:0px"><div class="heavy" style="font-size:54px">{query}</div></div>'
           f'<div id="{pid}_cu" style="width:6px;height:60px;background:{C["yellow"]}"></div></div>')
    h = [panel_open(pid), title(f"{pid}_t", ttl), card(f"{pid}_b", "left:90px;top:460px;width:900px;height:130px", bar)]
    if extra_label: h.append(label(f"{pid}_x", 540, 650, extra_label, size=36))
    for i, (x, y) in enumerate(tiles):
        h.append(card(f"{pid}_k{i}", f"left:{x}px;top:{y}px;width:430px;height:200px",
                      f'<div style="display:flex;align-items:center;gap:20px;padding:0 26px;height:100%">{icon("cam", 64, C["cyan"], 4)}<div class="heavy" style="font-size:34px;line-height:1.1">{tile_txt}</div></div>', cls="hide"))
    h += [chip(f"{pid}_f", 540, 1150, "FYP kita", color=C["yellow"], ink=C["navy"], size=38), PANEL_CLOSE]
    wdt = {"mk": 300, "dl": 330}[pid]
    j = [f"panel('{pid}', {n(a)}, {n(b)});", f"title('{pid}_t', {n(a + 0.05)});", f"pop('{pid}_b', {n(a + 0.12)}, 0.3);",
         f"tl.fromTo('#{pid}_tx', {{ width: 0 }}, {{ width: {wdt}, duration: 0.6, ease: 'steps(9)', immediateRender: false }}, {t(tkey)});",
         yoyo(f"#{pid}_cu", a, b, "opacity", 1, 0.1, 0.35, "none")]
    if extra_label: j.append(f"fadeIn('{pid}_x', {t('takPergi')}, 0.3);")
    tt = T["content"] if pid == "mk" else T["fyp2"]
    for i in range(4):
        j.append(f"tl.fromTo('#{pid}_k{i}', {{ y: 60, scale: 0.85 }}, {{ y: 0, scale: 1, duration: 0.3, ease: E.back, immediateRender: false }}, {n(tt + i * 0.12)}); fadeIn('{pid}_k{i}', {n(tt + i * 0.12)}, 0.12);")
    j.append(f"pop('{pid}_f', {n(tt + 0.55)});")
    return dict(a=a, html="\n".join(h), js="\n".join(j))


def training():
    a, b = S["training"]
    h = [panel_open("tr"), title("tr_t", "Training *content*")]
    for i, (tx, y, ic) in enumerate((("TRAINING PASAL CONTENT", 480, "chart"), ("UNTUK TEAM", 670, "bot"), ("PANDAI BUAT CONTENT", 860, "cam"))):
        h.append(row(f"tr_r{i}", y, tx, "", ic=ic))
    h.append(chip("tr_d", 540, 1100, "BOLEH DM SAYA", color=C["yellow"], ink=C["navy"], size=52))
    h.append(PANEL_CLOSE)
    j = [f"panel('tr', {n(a)}, {n(b)});", f"title('tr_t', {n(a + 0.05)});"]
    for i, k in enumerate(("training", "team", "pandai")):
        j.append(f"tl.fromTo('#tr_r{i}', {{ x: -120 }}, {{ x: 0, duration: 0.3, ease: E.out, immediateRender: false }}, {t(k, -0.1)}); fadeIn('tr_r{i}', {t(k, -0.1)}, 0.15);")
    j.append(f"pop('tr_d', {t('dm', -0.5)}, 0.3);")
    return dict(a=a, html="\n".join(h), js="\n".join(j))


def panels():
    return [feed(), feed2(), terms(), gary(), follow(), interest(), search("mk", "search1", "Search *makanan*", "makanan", "MAKANAN", "makanan"),
            search("dl", "search2", "Search *Dolomites*", "Dolomites", "DOLOMITES", "dolomites", "sebab tak dapat pergi"), training()]


def full_overlays():
    S_ = [  # id, text, a, b, size, box, sub, y
        ("sl0", "SOCIAL MEDIA?", 0, 2.55, 112, True, "", 520),
        ("sl1", "FYP", T["fyp"] - 0.04, 12.7, 200, True, "", None),
        ("sl2", "TERMS BARU", T["terms"] - 0.04, 16.9, 130, True, "", None),
        ("sl3", "BUKAN SOCIAL MEDIA", T["bukanLagi"] - 0.04, 25.15, 100, True, "", None),
        ("sl4", "INTEREST MEDIA", T["interest"] - 0.04, 31.85, 120, True, "", None),
        ("sl5", "SEARCH LOCATION", T["searchLoc"] - 0.04, 43.15, 110, True, "", None),
        ("sl6", "INTEREST MEDIA", T["interest2"] - 0.04, 50.4, 120, True, "", None),
        ("sl7", "APA SEARCH = APA KELUAR", T["apa"] - 0.04, 52.9, 80, False, "", None),
        ("sl8", "BUKAN SOCIAL MEDIA", T["noLonger"] - 0.04, 54.45, 100, True, "", None),
        ("sl9", "CONTENT STRATEGIST", 55.5, 57.65, 90, False, "lebih 5 tahun.", None),
    ]
    out = []
    for id_, txt, a, b, size, box, sub, y in S_:
        kw = {"y": y} if y else {}
        out.append(dict(a=a, html=slam(id_, txt, size, box, sub, "", **kw), js=f"slam('{id_}', {n(a)}, {n(b)}, {'true' if sub else 'false'});"))
    out.append(dict(a=0, html=chip("hk_k", 540, 335, "ZAMAN SEKARANG", size=44), js=f"pop('hk_k', 0.05, 0.3); tl.to('#hk_k', {{ opacity: 0, duration: 0.15, ease: E.in }}, 2.4);"))
    return out


END_LINE1, END_LINE2 = "BUKAN LAGI", "SOCIAL MEDIA"


def end_card():
    a = END_CARD
    logo = f'<img src="assets/img/logo_icon.png" alt="" style="width:300px;height:300px;border-radius:50%;box-shadow:0 0 40px rgba(0,207,245,0.45);border:4px solid rgba(255,255,255,0.8)">'
    fs = fit(END_LINE2, 150, 860)
    h = (f'<div id="endc" class="layer hide" style="background:radial-gradient(ellipse at 50% 40%, #0d2a57 0%, {C["navy"]} 65%)">'
         f'<div class="layer" style="background-image:radial-gradient(rgba(0,207,245,0.18) 1.6px, transparent 1.8px);background-size:36px 36px;opacity:0.6"></div>'
         f'<div id="endk" class="layer">'
         + anchor(540, 560, f'<div id="end1w"><div id="end1" class="heavy hide" style="font-size:112px;text-shadow:{SHADOW};white-space:nowrap;letter-spacing:-0.02em">{END_LINE1}</div></div>')
         + anchor(540, 740, f'<div id="end2" class="heavy hide" style="background:{C["yellow"]};color:{C["navy"]};font-size:{fs}px;padding:4px 40px 14px;border-radius:22px;box-shadow:{GLOW_Y};white-space:nowrap">{END_LINE2}</div>')
         + anchor(540, 1040, f'<div id="endlg" class="hide">{logo}</div>')
         + "</div></div>")
    j = [f"tl.fromTo('#endc', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: E.out, immediateRender: false }}, {n(a)});",
         f"tl.fromTo('#end1', {{ scale: 1.5 }}, {{ scale: 1, duration: 0.3, ease: E.back, immediateRender: false }}, {n(a + 0.05)}); fadeIn('end1', {n(a + 0.05)}, 0.15);",
         f"tl.fromTo('#end2', {{ scale: 1.8 }}, {{ scale: 1, duration: 0.3, ease: E.back, immediateRender: false }}, {n(a + 0.22)}); fadeIn('end2', {n(a + 0.22)}, 0.15);",
         f"tl.fromTo('#endlg', {{ y: 40, opacity: 0, scale: 0.8 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.45, ease: E.back, immediateRender: false }}, {n(a + 0.5)});",
         f"tl.to('#endk', {{ opacity: 0, duration: 0.25, ease: E.in }}, {n(TOTAL - 0.25)});"]
    return dict(html=h, js="\n".join(j))
