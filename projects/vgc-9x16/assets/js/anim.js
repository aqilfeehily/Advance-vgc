(function () {
  const tl = gsap.timeline({ paused: true });
  const T_END = 100.4, ACT2 = 12.06;

  /* ============ transitions: vertical "lift" (scene rises from below) ============ */
  const LIFT = 0.7;
  const lift = (t, inSel, outSel, dur = LIFT) => {
    tl.set(inSel, { autoAlpha: 1 }, t);
    tl.fromTo(inSel, { yPercent: 100, filter: "blur(14px)" }, { yPercent: 0, filter: "blur(0px)", duration: dur, ease: "power3.inOut", immediateRender: false }, t);
    if (outSel) {
      tl.fromTo(outSel, { yPercent: 0, filter: "blur(0px)" }, { yPercent: -24, filter: "blur(8px)", duration: dur, ease: "power3.inOut", immediateRender: false }, t);
      tl.set(outSel, { autoAlpha: 0 }, t + dur + 0.03);
      tl.set(outSel, { yPercent: 0, filter: "none" }, t + dur + 0.05);
    }
  };

  /* ============ layered typographic backgrounds ============ */
  // [id, start, class, ghost word, ghost x, ghost y, ghost rotation]
  const SC = [
    ["bg01", 0, "a1l", "BOSAN", -60, 700, -8],
    ["bg02", 5.2, "a1d", "?", 250, 380, 6],
    ["bg03", 12.06, "a2a", "FRESH", -120, 760, -6],
    ["bg04", 24.13, "a2b", "TAHU", -40, 420, 7],
    ["bg05", 30.4, "a2c", "BASIC", -150, 900, -5],
    ["bg06", 38.5, "a2a", "CARI", 60, 360, 5],
    ["bg07", 44.0, "a2b", "?!", 220, 820, -7],
    ["bg08", 50.4, "a2c", "DETAIL", -170, 500, 6],
    ["bg09", 53.4, "a2a", "BUAT", 30, 880, -6],
    ["bg10", 57.6, "a2b", "PAKAR", -110, 380, 5],
    ["bg11", 63.0, "a2c", "WEH!", 80, 760, -7],
    ["bg12", 70.0, "a2a", "LAIN", -100, 430, 6],
    ["bg13", 75.5, "a2b", "GAIN", 20, 860, -5],
    ["bg14", 87.4, "a2c", "AJAR", -130, 520, 7],
    ["bg15", 91.4, "a2a", "KOMEN", -170, 820, -6],
  ];
  const broll = document.getElementById("broll");
  SC.forEach(([id, t0, cls, word, gx, gy, gr], i) => {
    const bk = document.createElement("div");
    bk.className = "bk " + cls; bk.id = id;
    const sx = (n) => ((i * 197 + n * 61) % 100) / 100;      // deterministic layout
    let h = `<div class="kb"><div class="gh" style="left:${gx}px;top:${gy}px;transform:rotate(${gr}deg)">${word}</div>`;
    h += `<div class="sh" style="left:${60 + sx(1) * 700}px;top:${240 + sx(2) * 500}px;width:${260 + sx(3) * 200}px;height:${260 + sx(3) * 200}px"></div>`;
    h += `<div class="sh" style="left:${500 + sx(4) * 500}px;top:${1100 + sx(5) * 500}px;width:${180 + sx(6) * 160}px;height:${180 + sx(6) * 160}px"></div>`;
    h += `<div class="ln" style="left:${100 + sx(7) * 300}px;top:${1000 + sx(8) * 380}px;width:${300 + sx(9) * 380}px;transform:rotate(${-12 + sx(10) * 24}deg)"></div>`;
    h += `<div class="ln" style="left:${400 + sx(11) * 300}px;top:${300 + sx(12) * 300}px;width:${240 + sx(13) * 300}px;transform:rotate(${-12 + sx(14) * 24}deg)"></div></div>`;
    bk.innerHTML = h; broll.appendChild(bk);
  });
  gsap.set(".bk", { autoAlpha: 0, transformOrigin: "50% 50%" });
  gsap.set(".bk .kb", { transformOrigin: "50% 45%" });
  tl.set("#bg01", { autoAlpha: 1 }, 0);
  const INS_A = [18.43, 24.13], INS_B = [84.1, 87.4];
  SC.forEach(([id, t0], i) => {
    const end = i + 1 < SC.length ? SC[i + 1][1] : T_END;
    // slow linear drift so the layers never sit still
    tl.fromTo(`#${id} .kb`, { x: i % 2 ? 40 : -40, y: 0, scale: 1.0 }, { x: i % 2 ? -40 : 40, y: i % 3 ? 50 : -50, scale: 1.08, duration: end - t0 + LIFT, ease: "none", immediateRender: false }, t0);
    if (i === 0) return;
    const prev = SC[i - 1][0];
    if (t0 === INS_A[1] || t0 === INS_B[1]) {            // appears under the insert, which lifts off
      tl.set("#" + id, { autoAlpha: 1 }, t0 - 0.01);
      tl.set("#" + prev, { autoAlpha: 0 }, t0 + LIFT + 0.05);
    } else lift(t0, "#" + id, "#" + prev);
  });

  /* ============ inserts: the student's own photo / screen grid / teaching clip ============ */
  gsap.set(".ins", { autoAlpha: 0 });
  const insert = (sel, t0, t1) => {
    lift(t0, sel, null);
    tl.set("#pres-wrap", { autoAlpha: 0 }, t0 + LIFT + 0.05);
    tl.set("#pres-wrap", { autoAlpha: 1 }, t1 - 0.01);
    tl.fromTo(sel, { yPercent: 0, filter: "blur(0px)" }, { yPercent: -100, filter: "blur(10px)", duration: 0.75, ease: "power3.inOut", immediateRender: false }, t1);
    tl.set(sel, { autoAlpha: 0 }, t1 + 0.8);
  };
  insert("#insA", INS_A[0], INS_A[1]);
  insert("#insB", INS_B[0], INS_B[1]);

  /* ============ presenter: calm shot sizes (sine glides only) ============ */
  gsap.set("#pres-cam", { transformOrigin: "540px 1000px" });
  const CAM = [ // [time, scale, x]
    [0, 1.04, 0], [5.0, 1.0, 0], [9.0, 1.14, -8], [12.06, 1.0, 0], [16.0, 1.12, 0], [24.2, 1.05, 0], [27.2, 1.04, 0],
    [30.4, 1.0, 0], [34.0, 1.1, 8], [38.6, 1.2, 0], [44.0, 1.0, 0], [47.2, 1.14, -8], [50.6, 1.04, 0], [53.4, 1.0, 0],
    [57.6, 1.06, 0], [61.5, 1.04, 0], [63.0, 1.0, 0], [67.5, 1.1, 8], [70.0, 1.0, 0], [76.7, 1.04, 0], [78.4, 1.0, 0],
    [87.4, 1.08, 0], [91.4, 1.0, 0], [T_END, 1.06, 0],
  ];
  gsap.set("#pres-cam", { scale: CAM[0][1], x: CAM[0][2] });
  for (let i = 0; i < CAM.length - 1; i++) {
    const [ta, sa, xa] = CAM[i], [tb, sb, xb] = CAM[i + 1];
    const glide = Math.min(1.2, tb - ta);
    tl.fromTo("#pres-cam", { scale: sa, x: xa }, { scale: sb, x: xb, duration: glide, ease: "sine.inOut", immediateRender: false }, tb - glide);
  }

  /* ============ titles ============ */
  gsap.set(".hero, .place, #url", { autoAlpha: 0 });
  const hero = (sel, t0, t1) => {
    tl.set(sel, { autoAlpha: 1 }, t0);
    tl.fromTo(`${sel} .big`, { opacity: 0, y: 60, filter: "blur(16px)", letterSpacing: "0.04em" }, { opacity: 1, y: 0, filter: "blur(0px)", letterSpacing: "-0.035em", duration: 0.9, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`${sel} .scr`, { clipPath: "inset(-30% 100% -30% -5%)" }, { clipPath: "inset(-30% -5% -30% -5%)", duration: 0.9, ease: "sine.inOut", immediateRender: false }, t0 + 0.25);
    tl.fromTo(sel, { scale: 1 }, { scale: 1.04, duration: t1 - t0, ease: "none", immediateRender: false }, t0);
    tl.to(sel, { opacity: 0, y: -20, filter: "blur(10px)", duration: 0.4, ease: "power2.in" }, t1 - 0.4);
    tl.set(sel, { autoAlpha: 0, filter: "none" }, t1);
  };
  const place = (sel, t0, t1) => {
    tl.set(sel, { autoAlpha: 1 }, t0);
    tl.fromTo(`${sel} .kick`, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out", immediateRender: false }, t0);
    tl.fromTo(`${sel} .ln`, { clipPath: "inset(0 0 100% 0)", y: 70 }, { clipPath: "inset(0 0 -10% 0)", y: 0, duration: 0.8, stagger: 0.14, ease: "power3.out", immediateRender: false }, t0 + 0.15);
    tl.fromTo(sel, { scale: 1 }, { scale: 1.03, duration: t1 - t0, ease: "none", immediateRender: false }, t0);
    tl.to(sel, { opacity: 0, y: -16, filter: "blur(8px)", duration: 0.4, ease: "power2.in" }, t1 - 0.4);
    tl.set(sel, { autoAlpha: 0, filter: "none" }, t1);
  };
  place("#p-bulan", 0.25, 4.95);
  hero("#h-stop", 5.4, 9.2);
  place("#p-fresh", 12.3, 17.2);
  hero("#h-tahu", 27.0, 30.3);
  place("#p-cari", 38.7, 42.8);
  place("#p-q1", 44.0, 45.55);
  place("#p-q2", 45.55, 47.2);
  place("#p-q3", 47.2, 50.2);
  hero("#h-gali", 50.6, 53.3);
  place("#p-buat", 53.5, 57.5);
  hero("#h-baru", 58.2, 61.5);
  // signature: "BARU TAHU" is swapped for "PAKAR" by a vertical slot-roll, like a title rising a floor
  hero("#h-pakar", 61.45, 63.0);
  tl.fromTo("#h-pakar .big", { yPercent: 40, clipPath: "inset(0 0 100% 0)" }, { yPercent: 0, clipPath: "inset(0 0 -10% 0)", duration: 0.7, ease: "power3.out", immediateRender: false }, 61.45);
  place("#p-bagus", 63.15, 66.6);
  place("#p-lain", 66.8, 70.6);
  hero("#h-fol", 76.6, 78.35);
  hero("#h-cli", 78.3, 80.6);
  place("#p-ajar", 84.3, 87.2);
  place("#p-cta", 91.5, T_END - 0.05);

  /* ============ captions ============ */
  const caps = document.getElementById("caps");
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  window.AKG_CAPS.forEach(([t0, t1, text, kw], i) => {
    const el = document.createElement("div");
    el.className = "cap" + (t0 >= ACT2 ? " ak" : "");
    el.id = "cap-" + i;
    el.innerHTML = kw && text.includes(kw) ? esc(text).replace(esc(kw), `<span class="kw">${esc(kw)}</span>`) : esc(text);
    caps.appendChild(el);
    gsap.set(el, { autoAlpha: 0, transformOrigin: "50% 60%" });
    tl.set(el, { autoAlpha: 1 }, t0);
    tl.fromTo(el, { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.18, ease: "power2.out", immediateRender: false }, t0);
    tl.set(el, { autoAlpha: 0 }, Math.max(t0 + 0.2, t1 - 0.02));
  });

  tl.set({}, {}, T_END);
  window.AKG_TL = tl;
})();
