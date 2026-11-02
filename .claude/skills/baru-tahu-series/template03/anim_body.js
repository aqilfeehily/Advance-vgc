const press = (sel, t, col = "#ffd400") => {
  tl.to(sel, { scale: 1.22, duration: 0.1, yoyo: true, repeat: 1, transformOrigin: "50% 50%", ease: "power2.out" }, t);
  tl.to(`${sel} rect:nth-of-type(2)`, { fill: col, duration: 0.05 }, t);
};
// ---------- S1 hook ----------
{
  spin("#s1_rays", 0, 3.6, 540, 600, 24);
  mascotIn("s1", 0.05, { y: 200 });
  bob("#s1m", 0.5, 3.0, 8);
  tl.fromTo("#s1_kb", { y: 700 }, { y: 0, duration: 0.55, ease: "back.out(1.3)" }, 0.08);
  look("s1", 0, 40, 0.5); look("s1", 0, 30, 1.8);
  brows("s1", -22, 0.9, 6);
  mouth("s1", "open", 0.0); mouth("s1", "smile", 1.4); mouth("s1", "grin", 2.82);
  pop("#s1_q1", 1.0, 0.3); pop("#s1_q2", 1.9, 0.3);
  for (let i = 0; i < 6; i++) press(`#s1_r0_${i}`, 2.82 + i * 0.1);
}

// ---------- S2 bukannya A B C ----------
{
  spin("#s2_rays", 3.48, 3.0, 540, 640, 20);
  mascotIn("s2", 3.55, { y: 300 });
  bob("#s2m", 4.0, 2.3, 8);
  gsap.set("#s2_x", { opacity: 0 });
  pop("#s2_no", 3.6, 0.3);
  [["s2_k0", 4.14], ["s2_k1", 4.51], ["s2_k2", 4.9], ["s2_dots", 5.3], ["s2_k4", 5.83]].forEach(([id, t]) =>
    tl.fromTo(`#${id}`, { scale: 0, opacity: 0, y: 60, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, y: 0, duration: 0.3, ease: BACK }, t));
  tl.fromTo("#s2_x", { opacity: 0, scale: 2.5, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, 6.0);
  mouth("s2", "flat", 3.55); mouth("s2", "worry", 6.0);
  look("s2", 0, -30, 4.0); brows("s2", 8, 6.0, -6);
}

// ---------- S3 mesin taip ----------
{
  tl.fromTo("#s3_tw0", { x: -1200 }, { x: 0, duration: 0.6, ease: "power3.out" }, 6.5);
  tl.fromTo("#s3tw_paper", { y: 340 }, { y: 0, duration: 0.6, ease: "power2.out" }, 9.3);
  gsap.set("#s3tw_l0,#s3tw_l1,#s3tw_l2", { transformOrigin: "0% 50%" });
  [9.6, 10.15, 10.7].forEach((t, i) => {
    tl.fromTo(`#s3tw_l${i}`, { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "none" }, t);
    tl.fromTo("#s3tw_arm", { y: 0 }, { y: -36, duration: 0.08, yoyo: true, repeat: 5, ease: "none", immediateRender: false }, t);
  });
  [9.55, 10.1, 10.65].forEach((t, i) => {
    gsap.set(`#s3_t${i}`, { opacity: 0 });
    tl.fromTo(`#s3_t${i}`, { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.2, ease: BACK }, t);
    tl.to(`#s3_t${i}`, { opacity: 0, duration: 0.2 }, t + 0.5);
  });
  tl.to("#s3_tw0", { y: -10, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut" }, 7.4);
}

// ---------- S4 Sholes ----------
{
  pop("#s4_date", 12.0, 0.4);
  mascotIn("s4i", 13.0, { y: 300, x: -100 });
  bob("#s4im", 13.6, 7.5, 7);
  tl.fromTo("#s4_name", { scale: 2.2, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "power4.in" }, 14.36);
  tl.fromTo("#s4_scroll", { x: 700 }, { x: 0, duration: 0.5, ease: "power3.out" }, 16.1);
  for (let i = 0; i < 6; i++) {
    tl.fromTo(`#s4_k${i}`, { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: BACK }, 17.4 + i * 0.5);
  }
  for (let i = 0; i < 6; i++) press(`#s4_k${i}`, 20.76 + i * 0.05);
  mouth("s4i", "smile", 13.0); mouth("s4i", "grin", 18.72); mouth("s4i", "open", 20.76);
  look("s4i", 30, 6, 16.2); look("s4i", 30, 6, 20);
  brows("s4i", -18, 14.36, 5);
}

// ---------- S5 tersangkut ----------
{
  const rest = [-38, -38, -38, 38, 38, 38, 38];
  for (let i = 0; i < 7; i++) gsap.set(`#s5_a${i}`, { svgOrigin: `${240 + i * 100} 1080`, rotation: rest[i] });
  const strike = (i, t, hold = false) => {
    tl.to(`#s5_a${i}`, { rotation: 0, duration: 0.1, ease: "power2.in" }, t);
    if (!hold) tl.to(`#s5_a${i}`, { rotation: rest[i], duration: 0.22, ease: "power1.out" }, t + 0.12);
  };
  const calm = [22.0, 22.55, 23.1, 23.7, 24.3, 24.9, 25.5, 26.1, 26.7];
  const ci = [0, 3, 1, 5, 2, 4, 6, 3, 0];
  calm.forEach((t, n) => { strike(ci[n], t); tl.to(`#s5_pl${n}`, { opacity: 1, duration: 0.05 }, t + 0.1); });
  const fast = [29.85, 30.2, 30.5, 30.75, 30.95, 31.1, 31.22, 31.32];
  const fi = [1, 4, 2, 5, 0, 6, 3, 2];
  fast.forEach((t, n) => strike(fi[n], t, false));
  strike(3, 31.5, true); strike(2, 31.58, true);
  gsap.set("#s5_spk", { opacity: 0 });
  tl.fromTo("#s5_spk", { scale: 0, opacity: 0, transformOrigin: "540px 610px" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, 31.76);
  tl.to("#s5_cam", { x: 14, duration: 0.04, yoyo: true, repeat: 11, ease: "none" }, 31.76);
  tl.fromTo("#s5m", { y: 300, opacity: 0, scale: 0.4, transformOrigin: "50% 100%" }, { y: 0, opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 30.6);
  mouth("s5", "worry", 30.6); mouth("s5", "open", 31.76);
  look("s5", -30, -30, 30.7);
  brows("s5", -20, 31.76, -6);
  tl.to("#s5m", { y: -8, duration: 0.5, yoyo: true, repeat: 3, ease: "sine.inOut" }, 32.0);
}

// ---------- S6 mesin taip -> komputer -> telefon ----------
{
  gsap.set("#s6_bg2,#s6_bg3", { opacity: 0 });
  tl.to("#s6_bg2", { opacity: 1, duration: 0.4 }, 36.3);
  tl.to("#s6_bg3", { opacity: 1, duration: 0.4 }, 37.5);
  gsap.set("#s6_ar0,#s6_ar1", { opacity: 0 });
  pop("#s6_c0", 33.9, 0.4); pop("#s6_c1", 36.4, 0.4); pop("#s6_c2", 37.6, 0.4);
  tl.to("#s6_ar0", { opacity: 1, duration: 0.2 }, 36.8); tl.to("#s6_ar1", { opacity: 1, duration: 0.2 }, 38.0);
  for (let c = 0; c < 3; c++) for (let j = 0; j < 6; j++) press(`#s6_k${c}_${j}`, 38.58 + j * 0.07);
  for (let c = 0; c < 3; c++) {
    tl.fromTo(`#s6_ok${c}`, { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.6)" }, 40.06 + c * 0.2);
  }
}

// ---------- S7 100 tahun ----------
{
  spin("#s7_rays", 42.4, 7, 540, 760, 28);
  mascotIn("s7", 42.5, { y: 300 });
  bob("#s7m", 43.1, 6, 8);
  pop("#s7_bub", 43.5, 0.4);
  look("s7", -34, -30, 43.5); look("s7", 0, 10, 45.2);
  mouth("s7", "smile", 42.5); mouth("s7", "open", 47.8);
  brows("s7", -22, 47.8, 6);
  tl.to("#s7_bub", { opacity: 0, scale: 0.6, transformOrigin: "50% 50%", duration: 0.2 }, 45.1);
  for (let i = 0; i < 8; i++) {
    tl.fromTo(`#s7_pg${i}`, { x: 1300, opacity: 1, rotation: 0 }, { x: -1400, rotation: -30, duration: 0.5, ease: "power1.in" }, 45.2 + i * 0.28);
  }
  gsap.set("#s7_num", { opacity: 0 });
  tl.fromTo("#s7_num", { scale: 0.4, opacity: 0, transformOrigin: "540px 700px" }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 47.8);
  const nEl = document.getElementById("s7_n");
  const proxy = { v: 0 };
  tl.to(proxy, { v: 100, duration: 1.1, ease: "power2.out", onUpdate: () => { nEl.textContent = Math.round(proxy.v) + "+"; } }, 47.85);
  tl.to("#s7_num", { scale: 1.08, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: "540px 700px" }, 48.9);
}

// ---------- S8 dah tahu ----------
{
  spin("#s8_rays", 49.32, 2, 540, 800, 16);
  mascotIn("s8", 49.4);
  mouth("s8", "smile", 49.4); mouth("s8", "grin", 50.64);
  look("s8", 0, 6, 49.5); look("s8", -30, -30, 49.95); look("s8", 0, 4, 50.7);
  brows("s8", -22, 50.2, 6);
  gsap.set("#s8_bulbi", { opacity: 0 });
  tl.fromTo("#s8_bulbi", { scale: 0, opacity: 0, transformOrigin: "50% 100%" }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(3)" }, 50.2);
  tl.to("#s8m", { y: 22, duration: 0.14, yoyo: true, repeat: 3, ease: "sine.inOut" }, 50.7);
}

// ---------- S9 CTA ----------
{
  tl.fromTo("#s9_band", { x: -1400 }, { x: 0, duration: 0.5, ease: "power3.out" }, 51.42);
  mascotIn("s9", 51.4, { y: -200 });
  bob("#s9m", 51.9, 3.5, 10);
  look("s9", 0, 14, 51.5);
  pop("#s9_btn", 51.55, 0.35);
  tl.fromTo("#s9_hand", { x: 500, y: 300, opacity: 0, transformOrigin: "50% 50%" }, { x: 0, y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 52.0);
  tl.to("#s9_hand", { y: -30, x: -20, duration: 0.12, yoyo: true, repeat: 1 }, 52.75);
  tl.to("#s9_btn", { scale: 0.92, duration: 0.1, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 52.8);
  tl.to("#s9_btn rect", { fill: "#ffffff", duration: 0.12 }, 52.87);
  tl.to("#s9_btn text", { fill: "#141414", duration: 0.12 }, 52.87);
  gsap.set("#s9_t1,#s9_t2", { opacity: 0 });
  tl.fromTo("#s9_t1", { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 52.0);
  tl.fromTo("#s9_t2", { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 52.25);
  tl.to("#s9_t1", { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 54.4);
  tl.to("#s9_t2", { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 54.6);
  tl.to("#s9_hand", { opacity: 0, y: 200, duration: 0.3 }, 53.5);
}
