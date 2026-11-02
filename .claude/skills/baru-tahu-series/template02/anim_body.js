// ---------- S1 hook ----------
{
  spin("#s1_rays", 0, 3.2, 540, 760, 24);
  mascotIn("s1", 0.05);
  bob("#s1m", 0.5, 2.5, 10);
  look("s1", 0, 6, 0.5); look("s1", -34, -10, 2.33); look("s1", 34, -10, 2.7);
  brows("s1", -22, 0.9, 6);
  mouth("s1", "open", 0.0); mouth("s1", "smile", 1.4); mouth("s1", "open", 2.33);
  pop("#s1_q1", 0.95, 0.3); pop("#s1_q2", 1.9, 0.3);
  tl.to("#s1_q1", { rotation: 8, duration: 0.2, yoyo: true, repeat: 3, transformOrigin: "50% 50%" }, 1.3);
}

// ---------- S2 penimbang ----------
{
  spin("#s2_rays", 3.12, 5.8, 540, 600, 24);
  pop("#s2_sc", 3.3, 0.4);
  mascotIn("s2m", 3.35, { y: 300, x: -120 }); mascotIn("s2k", 3.5, { y: 300, x: 120 });
  bob("#s2mm", 4.0, 4.8, 8); bob("#s2km", 4.1, 4.7, 8, 0.6);
  gsap.set("#s2_beam", { svgOrigin: "540 431" });
  const tilt = (deg, t, d = 0.5, ease = "back.out(1.6)") => {
    const dy = 310 * Math.sin((deg * Math.PI) / 180);
    tl.to("#s2_beam", { rotation: deg, duration: d, ease }, t);
    tl.to("#s2_pan0", { y: -dy, duration: d, ease }, t);
    tl.to("#s2_pan1", { y: dy, duration: d, ease }, t);
  };
  tilt(10, 5.0); tilt(-8, 7.56); tilt(3, 8.3, 0.25, "sine.inOut"); tilt(-3, 8.55, 0.25, "sine.inOut");
  look("s2m", 20, -24, 3.5); look("s2k", -20, -24, 3.5);
  mouth("s2m", "flat", 5.0); mouth("s2k", "worry", 6.5); mouth("s2m", "worry", 8.4); mouth("s2k", "flat", 8.4);
  brows("s2m", -20, 3.6, 6); brows("s2k", -20, 3.7, 6);
  pop("#s2_q", 8.3, 0.3);
}

// ---------- S3 faktor ----------
{
  spin("#s3_rays", 8.8, 5.4, 540, 860, 28);
  mascotIn("s3", 8.9);
  bob("#s3m", 9.4, 4.7, 8);
  mouth("s3", "flat", 8.9); mouth("s3", "open", 10.3); mouth("s3", "smile", 12.67);
  look("s3", 0, -26, 9.9); look("s3", 0, 6, 13.7);
  brows("s3", -22, 10.0, 6);
  for (let i = 0; i < 4; i++) {
    tl.fromTo(`#s3_ki${i}`, { scale: 0, opacity: 0, y: 80, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, y: 0, duration: 0.3, ease: BACK }, 10.0 + i * 0.3);
    tl.to(`#s3_ki${i}`, { rotation: i % 2 ? 6 : -6, duration: 0.18, yoyo: true, repeat: 3, transformOrigin: "50% 50%", ease: "sine.inOut" }, 12.0 + i * 0.12);
  }
}

// ---------- S4 hormon + kitaran ----------
{
  spin("#s4_rays", 14.16, 4.5, 540, 700, 22);
  pop("#s4_dial", 14.3, 0.4);
  gsap.set("#s4_needle", { svgOrigin: "300 700", rotation: -70 });
  tl.to("#s4_needle", { rotation: 60, duration: 0.5, ease: "back.out(1.6)" }, 15.27);
  tl.to("#s4_needle", { rotation: -30, duration: 0.4, ease: "power2.inOut" }, 15.95);
  tl.to("#s4_needle", { rotation: 45, duration: 0.4, ease: "power2.inOut" }, 16.57);
  tl.to("#s4_needle", { rotation: 72, duration: 0.4, ease: "back.out(2)" }, 17.3);
  pop("#s4_cal", 17.15, 0.4);
  drawIn("#s4_loop,#s4_loopg", 17.6, 0.6);
  gsap.set("#s4_loopa", { opacity: 0 });
  tl.to("#s4_loopa", { opacity: 1, duration: 0.1 }, 18.15);
  tl.fromTo("#s4_day", { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.4, duration: 0.2, yoyo: true, repeat: 3 }, 18.2);
  tl.fromTo("#s4_peek", { y: 380 }, { y: 0, duration: 0.4, ease: "back.out(1.6)" }, 14.4);
  bob("#s4m", 14.9, 3.6, 7);
  look("s4", 34, -6, 14.5); look("s4", 24, -6, 17.2);
  mouth("s4", "smile", 14.4); mouth("s4", "open", 18.1);
}

// ---------- S5 mood / tenaga / sensitivity ----------
{
  spin("#s5_rays", 18.64, 5.6, 540, 700, 26);
  mascotIn("s5", 18.75, { y: 300 });
  bob("#s5m", 19.3, 4.8, 7);
  look("s5", -26, -40, 20.0); look("s5", 0, -40, 21.0); look("s5", 26, -40, 22.4);
  pop("#s5_g0", 20.0, 0.35); pop("#s5_g1", 21.0, 0.35); pop("#s5_g2", 22.4, 0.35);
  const face = (k, t) => ["smile", "flat", "worry"].forEach((n) => tl.set(`#s5_f_${n}`, { opacity: n === k ? 1 : 0 }, t));
  face("flat", 20.95); face("worry", 21.6); face("smile", 22.4); face("worry", 23.2);
  gsap.set("#s5_bat", { transformOrigin: "50% 100%" });
  tl.fromTo("#s5_bat", { scaleY: 0.9 }, { scaleY: 0.3, duration: 0.5, ease: "power2.inOut" }, 21.6);
  tl.to("#s5_bat", { scaleY: 0.85, duration: 0.5, ease: "power2.inOut" }, 22.4);
  tl.to("#s5_bat", { scaleY: 0.35, duration: 0.5, ease: "power2.inOut" }, 23.2);
  tl.to("#s5_hi", { scale: 1.25, duration: 0.2, yoyo: true, repeat: 7, transformOrigin: "50% 50%", ease: "sine.inOut" }, 22.7);
  mouth("s5", "smile", 18.8); mouth("s5", "open", 21.6); mouth("s5", "worry", 23.2);
}

// ---------- S6 beban ----------
{
  mascotIn("s6", 24.3);
  gsap.set("#s6m", { transformOrigin: "50% 100%" });
  tl.to("#s6m", { scaleY: 0.94, duration: 0.15, ease: "power2.out", transformOrigin: "50% 100%" }, 25.4);
  tl.to("#s6m", { scaleY: 0.88, duration: 0.15, ease: "power2.out", transformOrigin: "50% 100%" }, 26.45);
  tl.to("#s6m", { scaleY: 0.82, duration: 0.15, ease: "power2.out", transformOrigin: "50% 100%" }, 28.2);
  tl.fromTo("#s6_pil", { y: -1000 }, { y: -87, duration: 0.3, ease: "power2.in" }, 25.16);
  tl.to("#s6_pil", { y: -43, duration: 0.15 }, 26.5); tl.to("#s6_pil", { y: 0, duration: 0.15 }, 28.2);
  tl.fromTo("#s6_cas", { y: -1000 }, { y: -87, duration: 0.3, ease: "power2.in" }, 26.2);
  tl.to("#s6_cas", { y: -43, duration: 0.15 }, 26.5);
  tl.to("#s6_cas", { y: 0, duration: 0.15 }, 28.2);
  tl.fromTo("#s6_rock", { y: -1000 }, { y: -43, duration: 0.3, ease: "power2.in" }, 27.96);
  tl.to("#s6_rock", { y: 0, duration: 0.15 }, 28.3);
  mouth("s6", "smile", 24.3); mouth("s6", "worry", 25.4); mouth("s6", "open", 28.3); mouth("s6", "worry", 29.2);
  look("s6", 0, 20, 25.4); look("s6", 0, 28, 28.3);
  brows("s6", 8, 28.3, -8);
  gsap.set("#s6_sw", { opacity: 0 });
  tl.fromTo("#s6_sw", { y: -10, opacity: 0 }, { y: 60, opacity: 1, duration: 0.5, ease: "power1.in" }, 29.6);
  tl.to("#s6_sw", { opacity: 0, duration: 0.1 }, 30.1);
  tl.fromTo("#s6_sw", { y: -10, opacity: 0, immediateRender: false }, { y: 60, opacity: 1, duration: 0.5, ease: "power1.in" }, 30.6);
  tl.to("#s6_sw", { opacity: 0, duration: 0.1 }, 31.1);
  for (let i = 0; i < 4; i++) {
    tl.fromTo(`#s6_st${i}`, { y: 0, opacity: 0 }, { y: -70, opacity: 1, duration: 0.5, ease: "power1.out", repeat: 1 }, 31.8 + i * 0.12);
    tl.to(`#s6_st${i}`, { opacity: 0, duration: 0.15 }, 32.65);
  }
}

// ---------- S7 lelaki pun ----------
{
  mascotIn("s7", 32.8);
  bob("#s7m", 33.3, 4.5, 9);
  gsap.set("#s7_sun,#s7_cl,#s7_rain", { opacity: 0 });
  look("s7", 0, -30, 33.0);
  mouth("s7", "grin", 32.8); mouth("s7", "smile", 34.44); mouth("s7", "flat", 35.1); mouth("s7", "worry", 36.88);
  brows("s7", -20, 32.85, 6); brows("s7", 6, 36.88, -6);
  tl.fromTo("#s7_sun", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.35, ease: BACK }, 33.3);
  tl.fromTo("#s7_sunr", { rotation: 0, transformOrigin: "50% 50%" }, { rotation: 90, duration: 1.8, ease: "none" }, 33.3);
  tl.to("#s7_sun", { opacity: 0, y: -20, duration: 0.25 }, 35.1);
  tl.fromTo("#s7_cl", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.35, ease: BACK }, 35.1);
  tl.to("#s7_cl", { opacity: 0, duration: 0.2 }, 36.8);
  tl.fromTo("#s7_rain", { scale: 0.6, opacity: 0, transformOrigin: "50% 30%" }, { scale: 1, opacity: 1, duration: 0.35, ease: BACK }, 36.8);
  for (let i = 0; i < 4; i++) tl.fromTo(`#s7_d${i}`, { y: 0, opacity: 1 }, { y: 80, opacity: 0, duration: 0.45, ease: "power1.in", repeat: 2 }, 37.1 + i * 0.1);
  tl.to("#s7_c1", { x: 300, duration: 5.2, ease: "none" }, 32.72);
  tl.to("#s7_c2", { x: -350, duration: 5.2, ease: "none" }, 32.72);
}

// ---------- S8 cara berbeza ----------
{
  spin("#s8_rays", 37.92, 4.8, 540, 760, 22);
  mascotIn("s8a", 38.0); mascotIn("s8b", 38.1, { y: 300 }); mascotIn("s8c", 38.2);
  bob("#s8am", 38.6, 4.0, 6); bob("#s8bm", 38.7, 3.9, 6, 0.6); bob("#s8cm", 38.8, 3.8, 6, 0.5);
  pop("#s8_b1", 39.6, 0.3); pop("#s8_b2", 40.1, 0.3); pop("#s8_b3", 40.6, 0.3);
  tl.to("#s8_bub", { scale: 1.35, duration: 0.5, yoyo: true, repeat: 3, transformOrigin: "50% 50%", ease: "sine.inOut" }, 39.7);
  tl.to("#s8_note", { rotation: 10, duration: 0.25, yoyo: true, repeat: 5, transformOrigin: "50% 100%", ease: "sine.inOut" }, 40.7);
  look("s8a", 0, -20, 39.6); look("s8b", 0, -20, 40.1); look("s8c", 0, -20, 40.6);
  mouth("s8a", "flat", 39.6); mouth("s8b", "open", 40.1); mouth("s8c", "grin", 40.6);
  mouth("s8a", "smile", 41.3); mouth("s8b", "smile", 41.3); mouth("s8c", "smile", 41.3);
  for (let i = 0; i < 3; i++) {
    tl.fromTo(`#s8_h${i}i`, { scale: 0, opacity: 0, y: 40, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, y: -60, duration: 0.6, ease: "power2.out" }, 41.26 + i * 0.1);
    tl.to(`#s8_h${i}i`, { opacity: 0, y: -120, duration: 0.5 }, 41.95 + i * 0.1);
  }
}

// ---------- S9 bukan semua ----------
{
  tl.fromTo("#s9_card", { y: -700 }, { y: 0, duration: 0.4, ease: "back.out(1.4)" }, 42.86);
  mascotIn("s9", 42.9);
  bob("#s9m", 43.5, 2.0, 6);
  gsap.set("#s9_x", { opacity: 0 });
  tl.fromTo("#s9_x", { opacity: 0, scale: 3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.18, ease: "power4.in" }, 43.31);
  tl.to("#s9_card", { x: 10, duration: 0.05, yoyo: true, repeat: 5, ease: "none" }, 43.5);
  tl.to("#s9_card,#s9_x", { y: 1500, rotation: 22, duration: 0.55, ease: "power2.in", transformOrigin: "50% 50%" }, 44.9);
  mouth("s9", "flat", 42.9); mouth("s9", "smile", 43.6);
  brows("s9", -14, 43.3, 4);
}

// ---------- S10 bukit ais ----------
{
  gsap.set("#s10_face", { opacity: 0, transformOrigin: "50% 50%" });
  tl.fromTo("#s10_face", { scale: 0, opacity: 0, transformOrigin: "540px 700px" }, { scale: 1, opacity: 1, duration: 0.3, ease: BACK }, 47.68);
  gsap.set("#s10_ice,#s10_fac,#s10_t", { opacity: 0 });
  tl.to("#s10_ice", { opacity: 0.92, duration: 0.7 }, 49.7);
  tl.to("#s10_fac", { opacity: 1, duration: 0.7 }, 49.7);
  tl.to("#s10_cam", { y: -330, duration: 1.1, ease: "power2.inOut" }, 49.75);
  tl.fromTo("#s10_t", { scale: 0.5, opacity: 0, transformOrigin: "540px 1130px" }, { scale: 1, opacity: 1, duration: 0.35, ease: BACK }, 50.45);
}

// ---------- S11 haa dah tahu ----------
{
  spin("#s11_rays", 52.16, 2.2, 540, 800, 16);
  mascotIn("s11", 52.2);
  mouth("s11", "smile", 52.2); mouth("s11", "grin", 53.7);
  look("s11", 0, 6, 52.3); look("s11", -30, -30, 52.8); look("s11", 0, 4, 53.7);
  brows("s11", -22, 53.1, 6);
  gsap.set("#s11_bulbi", { opacity: 0 });
  tl.fromTo("#s11_bulbi", { scale: 0, opacity: 0, transformOrigin: "50% 100%" }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(3)" }, 53.2);
  tl.to("#s11m", { y: 22, duration: 0.14, yoyo: true, repeat: 3, ease: "sine.inOut" }, 53.7);
}

// ---------- S12 CTA ----------
{
  tl.fromTo("#s12_band", { x: -1400 }, { x: 0, duration: 0.5, ease: "power3.out" }, 54.25);
  mascotIn("s12", 54.2, { y: -200 });
  bob("#s12m", 54.8, 3.2, 10);
  look("s12", 0, 14, 54.3);
  pop("#s12_btn", 54.4, 0.35);
  tl.fromTo("#s12_hand", { x: 500, y: 300, opacity: 0, transformOrigin: "50% 50%" }, { x: 0, y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 54.9);
  tl.to("#s12_hand", { y: -30, x: -20, duration: 0.12, yoyo: true, repeat: 1 }, 55.6);
  tl.to("#s12_btn", { scale: 0.92, duration: 0.1, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 55.65);
  tl.to("#s12_btn rect", { fill: "#ffffff", duration: 0.12 }, 55.72);
  tl.to("#s12_btn text", { fill: "#141414", duration: 0.12 }, 55.72);
  gsap.set("#s12_t1,#s12_t2", { opacity: 0 });
  tl.fromTo("#s12_t1", { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 54.8);
  tl.fromTo("#s12_t2", { scale: 2.4, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.22, ease: "power4.in" }, 55.05);
  tl.to("#s12_t1", { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 57.25);
  tl.to("#s12_t2", { scale: 1.12, duration: 0.12, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, 57.55);
  tl.to("#s12_hand", { opacity: 0, y: 200, duration: 0.3 }, 56.4);
}
