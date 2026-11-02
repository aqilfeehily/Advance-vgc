// ---------- helpers ----------
const $ = (s) => s;
document.querySelectorAll('[id$="_gl"],[id$="_fr"]').forEach((e) => e.setAttribute("pathLength", "1"));
const BACK = "back.out(2.2)";
function pop(sel, t, d = 0.3, ease = BACK, from = {}) {
  tl.fromTo(sel, Object.assign({ scale: 0, opacity: 0, transformOrigin: "50% 50%" }, from), { scale: 1, opacity: 1, duration: d, ease }, t);
}
function drawIn(sel, t, d, ease = "power1.inOut") {
  gsap.set(sel, { strokeDasharray: 1, strokeDashoffset: 1 });
  tl.to(sel, { strokeDashoffset: 0, duration: d, ease }, t);
}
function drawWindow(p, t, d) {
  gsap.set(`#${p}_fr,#${p}_gl`, { strokeDasharray: 1, strokeDashoffset: 1, fillOpacity: 0 });
  gsap.set(`#${p}_in`, { opacity: 0 });
  tl.to(`#${p}_fr`, { strokeDashoffset: 0, duration: d, ease: "power1.inOut" }, t);
  tl.to(`#${p}_gl`, { strokeDashoffset: 0, duration: d * 0.8, ease: "power1.inOut" }, t + d * 0.3);
  tl.to(`#${p}_fr,#${p}_gl`, { fillOpacity: 1, duration: 0.25 }, t + d * 1.0);
  tl.to(`#${p}_in`, { opacity: 1, duration: 0.25 }, t + d * 1.0);
}
function showWindow(p) { /* static window, nothing to do */ }
function spin(sel, t0, dur, ox, oy, deg = 25) {
  gsap.set(sel, { svgOrigin: `${ox} ${oy}` });
  tl.fromTo(sel, { rotation: 0 }, { rotation: deg, duration: dur, ease: "none" }, t0);
}
function bob(sel, t0, dur, amp = 12, per = 0.55) {
  const n = Math.max(1, Math.round(dur / per));
  tl.fromTo(sel, { y: 0, rotation: -1.4, transformOrigin: "50% 100%" }, { y: -amp, rotation: 1.4, duration: per, ease: "sine.inOut", repeat: n, yoyo: true }, t0);
}
function mouth(p, name, t) {
  ["smile", "grin", "open", "worry", "flat"].forEach((k) => tl.set(`#${p}mo_${k}`, { opacity: k === name ? 1 : 0 }, t));
}
function look(p, x, y, t, d = 0.18) {
  tl.to(`#${p}pupL,#${p}pupR`, { x, y, duration: d, ease: "power2.out" }, t);
}
function brows(p, y, t, rot = 0) {
  tl.to(`#${p}browL`, { y, rotation: -rot, duration: 0.15, transformOrigin: "50% 50%" }, t);
  tl.to(`#${p}browR`, { y, rotation: rot, duration: 0.15, transformOrigin: "50% 50%" }, t);
}
function mascotIn(p, t, from = { y: 260 }) {
  tl.fromTo(`#${p}m`, Object.assign({ scale: 0.3, opacity: 0, transformOrigin: "50% 100%" }, from), { scale: 1, y: 0, x: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }, t);
}
function enter(id, t, kind) {
  const sel = "#" + id;
  if (kind === "lift") tl.fromTo(sel, { y: 1920 }, { y: 0, duration: 0.3, ease: "power3.out" }, t);
  if (kind === "left") tl.fromTo(sel, { x: 1080 }, { x: 0, duration: 0.3, ease: "power3.out" }, t);
  if (kind === "circle")
    tl.fromTo(sel, { clipPath: "circle(0% at 50% 55%)" }, { clipPath: "circle(150% at 50% 55%)", duration: 0.34, ease: "power2.out" }, t);
}
// pre-hide entrance positions at t=0 so nothing flashes before the scene is shown
const ENTER = { s2: "lift", s3: "left", s4: "circle", s5: "lift", s7: "left", s8: "circle", s9: "lift", s10: "left", s11: "circle" };
Object.keys(ENTER).forEach((id) => enter(id, SC[id], ENTER[id]));

// ---------- captions ----------
document.querySelectorAll(".capw").forEach((el) => {
  const r = parseFloat(el.querySelector(".cap").dataset.rot);
  const st = parseFloat(el.dataset.start);
  tl.fromTo(el.querySelector(".cap"), { scale: 0.7, opacity: 0, rotation: r * 2 }, { scale: 1, opacity: 1, rotation: r, duration: 0.16, ease: "back.out(2.4)", transformOrigin: "50% 50%" }, st);
});

// ---------- S1  hook ----------
{
  const T = SC.s1;
  spin("#s1_rays", 0, 3.2, 540, 760, 24);
  tl.fromTo("#s1_wall", { x: 420, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "power3.out" }, 0.1);
  mascotIn("s1", 0.05);
  bob("#s1m", 0.5, 2.3, 10);
  look("s1", 34, -22, 0.55);
  look("s1", 0, 6, 1.35);
  look("s1", 36, -24, 2.3);
  brows("s1", -22, 0.9, 6);
  mouth("s1", "open", 0.95); mouth("s1", "smile", 1.5); mouth("s1", "open", 2.3);
  pop("#s1_q1", 0.95, 0.3); pop("#s1_q2", 1.9, 0.3);
  tl.to("#s1_q1", { rotation: 8, duration: 0.2, yoyo: true, repeat: 3 }, 1.3);
}

// ---------- S2  oval vs petak ----------
{
  const T = SC.s2;
  drawWindow("s2o", 3.0, 1.2);
  gsap.set("#s2_sq", { x: 900 });
  gsap.set("#s2_x", { opacity: 0 });
  gsap.set("#s2_ok", { opacity: 0, x: -520 });
  tl.fromTo("#s2o_fr", { scale: 1 }, { scale: 1, duration: 0.01 }, 0);
  tl.fromTo("#s2_oval", { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.07, duration: 0.14, yoyo: true, repeat: 1, ease: "power2.out" }, 5.6);
  tl.to("#s2_oval", { x: -230, scale: 0.85, transformOrigin: "50% 50%", duration: 0.4, ease: "power3.inOut" }, 5.95);
  tl.to("#s2_sq", { x: 230, duration: 0.45, ease: "back.out(1.5)" }, 5.95);
  gsap.set("#s2_sq", { scale: 0.85, svgOrigin: "540 780" });
  tl.fromTo("#s2_x", { opacity: 0, scale: 3, svgOrigin: "540 780" }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, 6.66);
  tl.to("#s2_x", { x: 230, duration: 0.001 }, 6.66);
  tl.to("#s2_sq", { x: 262, rotation: 6, duration: 0.06, yoyo: true, repeat: 5, ease: "none" }, 6.84);
  pop("#s2_ok", 6.8, 0.3);
  tl.to("#s2_ok", { x: -520 , duration: 0.001}, 6.8);
}

// ---------- S3  sebab keselamatan ----------
{
  spin("#s3_rays", 7.0, 7.6, 700, 620, 40);
  pop("#s3_win", 7.15, 0.4);
  mascotIn("s3", 7.1, { y: 300, x: -140 });
  bob("#s3m", 7.6, 6.8, 8);
  gsap.set("#s3_magg", { opacity: 0 });
  tl.fromTo("#s3_magg", { x: 120, opacity: 0, scale: 0.4 }, { x: 0, opacity: 1, scale: 1, duration: 0.3, ease: BACK, transformOrigin: "50% 50%" }, 7.8);
  tl.to("#s3_magg", { x: 190, y: -250, duration: 0.5, ease: "power2.inOut" }, 8.4);
  tl.to("#s3_magg", { x: 205, y: -240, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }, 9.0);
  tl.to("#s3_magg", { x: 330, y: -80, opacity: 0, duration: 0.3, ease: "power2.in" }, 11.2);
  look("s3", 30, -20, 7.5); look("s3", 0, 4, 12.0);
  mouth("s3", "smile", 7.1); mouth("s3", "grin", 10.68); mouth("s3", "flat", 11.2); mouth("s3", "smile", 13.7);
  brows("s3", -20, 11.2, 5);
  for (let i = 0; i < 4; i++) {
    gsap.set(`#s3_st${i}`, { opacity: 0 });
    tl.fromTo(`#s3_st${i}`, { scale: 0, opacity: 0, rotation: -60, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, rotation: 0, duration: 0.25, ease: BACK }, 10.0 + i * 0.16);
    tl.to(`#s3_st${i}`, { scale: 0, rotation: 120, opacity: 0, duration: 0.2, ease: "power2.in" }, 11.15 + i * 0.05);
  }
  gsap.set("#s3_shieldi", { opacity: 0 });
  tl.fromTo("#s3_shieldi", { scale: 0, opacity: 0, rotation: -20, transformOrigin: "50% 50%" }, { scale: 1.25, opacity: 1, rotation: 0, duration: 0.45, ease: "back.out(2.4)" }, 12.04);
  tl.to("#s3_shieldi", { scale: 1.1, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }, 12.6);
}

// ---------- S4  tingkap petak dulu ----------
{
  tl.fromTo("#s4_cam", { x: -1300 }, { x: 0, duration: 0.55, ease: "power3.out" }, 14.5);
  tl.to("#s4_cam", { x: -140, duration: 5.6, ease: "none" }, 15.05);
  tl.to("#s4_cl1", { x: 700, duration: 6, ease: "none" }, 14.45);
  tl.to("#s4_cl2", { x: -800, duration: 6, ease: "none" }, 14.45);
  tl.fromTo("#s4_l1", { x: 300, opacity: 0.0 }, { x: -500, opacity: 1, duration: 1.6, ease: "none" }, 14.9);
  tl.to("#s4_l1", { x: -900, duration: 2.5, ease: "none" }, 16.5);
  tl.to("#s4_cam", { y: -14, duration: 0.7, yoyo: true, repeat: 7, ease: "sine.inOut" }, 15.1);
  for (let i = 0; i < 6; i++) {
    tl.fromTo(`#s4pw${i}`, { scale: 1, fill: "#fff2c4", transformOrigin: "50% 50%" }, { scale: 1.5, fill: "#ffd23f", duration: 0.16, yoyo: true, repeat: 1, ease: "power2.out" }, 18.95 + i * 0.22);
  }
}

// ---------- S5  tekanan + keretakan ----------
{
  tl.fromTo("#s5_peek", { y: 380 }, { y: 0, duration: 0.4, ease: "back.out(1.6)" }, 20.6);
  bob("#s5m", 21.0, 9.2, 8);
  look("s5", 40, -30, 20.9); look("s5", 30, -10, 26.2);
  mouth("s5", "worry", 20.6); mouth("s5", "open", 26.9); mouth("s5", "worry", 29.4);
  brows("s5", -20, 20.7, -6);
  pop("#s5_ex1", 21.0, 0.3);
  tl.to("#s5_ex1", { rotation: 8, duration: 0.15, yoyo: true, repeat: 5, transformOrigin: "50% 50%" }, 21.4);
  const dirs = [[-1, -1], [1, -1], [-1, 1], [1, 1]];
  for (let i = 0; i < 4; i++) {
    gsap.set(`#s5_a${i}`, { opacity: 0 });
    tl.fromTo(`#s5_a${i}`, { x: dirs[i][0] * 120, y: dirs[i][1] * 120, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 21.56 + i * 0.22);
    tl.to(`#s5_a${i}`, { x: -dirs[i][0] * -18, y: -dirs[i][1] * -18, duration: 0.12, yoyo: true, repeat: 5, ease: "sine.inOut" }, 22.6 + i * 0.06);
    tl.to(`#s5_a${i}`, { opacity: 0, duration: 0.25 }, 25.2);
    gsap.set(`#s5_c${i}`, { opacity: 0 });
    tl.fromTo(`#s5_c${i}`, { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 0.85, duration: 0.2, ease: BACK }, 23.85 + i * 0.12);
    tl.to(`#s5_c${i}`, { scale: 1.3, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut" }, 24.3 + i * 0.05);
  }
  gsap.set("#s5_crack,#s5_crack2,#s5_crackw,#s5_crack3,#s5_crack4", { strokeDasharray: 1, strokeDashoffset: 1 });
  tl.to("#s5_crack,#s5_crackw", { strokeDashoffset: 0, duration: 2.0, ease: "power2.in" }, 26.3);
  tl.to("#s5_crack2", { strokeDashoffset: 0, duration: 0.6, ease: "power1.out" }, 28.1);
  tl.to("#s5_crack3,#s5_crack4", { strokeDashoffset: 0, duration: 0.8, ease: "power2.out" }, 28.85);
  tl.to("#s5_cam", { x: 12, duration: 0.04, yoyo: true, repeat: 9, ease: "none" }, 28.06);
  tl.to("#s5_cam", { scale: 0.64, transformOrigin: "50% 50%", duration: 1.0, ease: "power2.inOut" }, 28.95);
  gsap.set("#s5_sweat", { opacity: 0 });
  tl.fromTo("#s5_sweat", { y: -10, opacity: 0 }, { y: 70, opacity: 1, duration: 0.5, ease: "power1.in" }, 26.6);
  tl.to("#s5_sweat", { opacity: 0, duration: 0.1 }, 27.1);
  tl.fromTo("#s5_sweat", { y: -10, opacity: 0, immediateRender: false }, { y: 70, opacity: 1, duration: 0.5, ease: "power1.in" }, 27.6);
  tl.to("#s5_sweat", { opacity: 0, duration: 0.1 }, 28.1);
}

// ---------- S7  oval melengkung ----------
{
  spin("#s7_rays", 30.35, 8.2, 540, 860, 30);
  drawWindow("s7w", 31.0, 1.3);
  tl.fromTo("#s7_win", { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.08, transformOrigin: "50% 50%", duration: 0.14, yoyo: true, repeat: 1, ease: "power2.out" }, 33.9);
  ["s7_f1", "s7_f2", "s7_f3", "s7_f4"].forEach((id, i) => {
    gsap.set(`#${id},#${id}g`, { strokeDasharray: 1, strokeDashoffset: 1 });
    tl.to(`#${id},#${id}g`, { strokeDashoffset: 0, duration: 0.8, ease: "power2.out" }, 35.42 + i * 0.3);
    tl.to(`#${id}h`, { opacity: 1, duration: 0.1 }, 36.1 + i * 0.3);
  });
  tl.to("#s7w_gl", { fill: "#b8f5cf", duration: 0.5 }, 37.5);
  gsap.set("#s7_okg", { opacity: 0 });
  tl.fromTo("#s7_okg", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.6)" }, 37.85);
}

// ---------- S8  menarik kan ----------
{
  spin("#s8_rays", 38.5, 1.3, 540, 780, 14);
  mascotIn("s8", 38.55);
  look("s8", 0, 6, 38.6);
  tl.fromTo("#s8_hand", { x: 300, y: 200, rotation: 30, opacity: 0, transformOrigin: "50% 50%" }, { x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 38.7);
  for (let i = 0; i < 4; i++) {
    gsap.set(`#s8_st${i}`, { opacity: 0 });
    tl.fromTo(`#s8_st${i}`, { scale: 0, opacity: 0, rotation: -80, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, rotation: 0, duration: 0.3, ease: BACK }, 38.85 + i * 0.08);
  }
}

// ---------- S9  rumusnya ----------
{
  tl.fromTo("#s9_plane", { x: 1300 }, { x: 0, duration: 0.7, ease: "power3.out" }, 39.55);
  tl.to("#s9_plane", { y: -16, duration: 0.8, yoyo: true, repeat: 5, ease: "sine.inOut" }, 40.3);
  tl.fromTo("#s9_c0", { x: 300 }, { x: -500, duration: 6, ease: "none" }, 39.5);
  tl.fromTo("#s9_c1", { x: 400 }, { x: -700, duration: 6, ease: "none" }, 39.5);
  tl.fromTo("#s9_c2", { x: 600 }, { x: -700, duration: 6, ease: "none" }, 39.5);
  tl.fromTo("#s9_c3", { x: 300 }, { x: -800, duration: 6, ease: "none" }, 39.5);
  gsap.set("#s9_shieldi", { opacity: 0 });
  tl.to("#s9_cam,#s9_plane", { scale: 1, duration: 0.001 }, 39.5);
  gsap.set("#s9_cam", { svgOrigin: "683 760.5" });
  tl.to("#s9_cam", { scale: 3.2, duration: 0.8, ease: "power3.inOut" }, 43.1);
  tl.fromTo("#s9_shieldi", { scale: 0, opacity: 0, x: 190, y: -210, transformOrigin: "50% 50%" }, { scale: 1.1, opacity: 1, x: 190, y: -210, duration: 0.4, ease: "back.out(2.4)" }, 43.9);
  tl.to("#s9_shieldi", { scale: 0.95, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }, 44.4);
}

// ---------- S10  hah dah tahu ----------
{
  spin("#s10_rays", 45.3, 2, 540, 900, 16);
  mascotIn("s10", 45.35);
  mouth("s10", "smile", 45.4); mouth("s10", "grin", 46.8);
  look("s10", 0, 6, 45.4); look("s10", -30, -30, 45.9); look("s10", 0, 4, 46.8);
  brows("s10", -22, 46.3, 6);
  gsap.set("#s10_bulbi", { opacity: 0 });
  tl.fromTo("#s10_bulbi", { scale: 0, opacity: 0, transformOrigin: "50% 100%" }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(3)" }, 46.35);
  tl.to("#s10m", { y: 22, duration: 0.14, yoyo: true, repeat: 3, ease: "sine.inOut" }, 46.8);
}

// ---------- S11  CTA ----------
{
  tl.fromTo("#s11_band", { x: -1400 }, { x: 0, duration: 0.5, ease: "power3.out" }, 47.35);
  mascotIn("s11", 47.3, { y: -200 });
  bob("#s11m", 47.8, 3.2, 10);
  look("s11", 0, 14, 47.4);
  pop("#s11_btn", 47.5, 0.35);
  tl.fromTo("#s11_hand", { x: 500, y: 300, opacity: 0, transformOrigin: "50% 50%" }, { x: 0, y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 48.0);
  tl.to("#s11_hand", { y: -30, x: -20, duration: 0.12, yoyo: true, repeat: 1 }, 49.0);
  tl.to("#s11_btn", { scale: 0.92, duration: 0.1, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 49.05);
  tl.to("#s11_btn rect", { fill: "#ffffff", duration: 0.12 }, 49.12);
  tl.to("#s11_btn text", { fill: "#141414", duration: 0.12 }, 49.12);
  gsap.set("#s11_t1,#s11_t2", { opacity: 0 });
  tl.fromTo("#s11_t1", { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 47.7);
  tl.to("#s11_t1", { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 50.23);
  tl.fromTo("#s11_t2", { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 47.95);
  tl.to("#s11_t2", { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 50.55);
  tl.to("#s11_hand", { opacity: 0, y: 200, duration: 0.3 }, 49.6);
}
