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
const ENTER = { s2: "lift", s3: "left", s4: "circle", s5: "lift", s6: "left", s7: "circle", s8: "lift", s9: "left", s10: "lift", s11: "circle", s12: "left" };
Object.keys(ENTER).forEach((id) => enter(id, SC[id], ENTER[id]));

// ---------- captions ----------
document.querySelectorAll(".capw").forEach((el) => {
  const r = parseFloat(el.querySelector(".cap").dataset.rot);
  const st = parseFloat(el.dataset.start);
  tl.fromTo(el.querySelector(".cap"), { scale: 0.7, opacity: 0, rotation: r * 2 }, { scale: 1, opacity: 1, rotation: r, duration: 0.16, ease: "back.out(2.4)", transformOrigin: "50% 50%" }, st);
});

