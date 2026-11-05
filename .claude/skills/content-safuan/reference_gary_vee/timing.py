"""Gary Vee / interest media (Nov 2026). Anchors are Whisper word starts (source seconds)."""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
EDL = json.load(open(os.path.join(ROOT, "data", "edl.json"), encoding="utf-8"))
SEGS = EDL["segs"]; TOTAL = EDL["total"]; SPEECH_END = EDL["speechEnd"]; WORDS = EDL["words"]


def at(src):
    for s in SEGS:
        if s["in"] - 0.06 <= src <= s["out"] + 0.06:
            return round(s["at"] + max(0.0, src - s["in"]), 4)
    raise ValueError(src)


_SRC = dict(instagram=2.66, feed=5.08, betul=6.34, tapi=7.1, orangFollow=8.62, takNampak=9.46, fyp=10.86, bukan=12.8,
            social=13.52, terms=14.84, gary=17.1, master=19.9, zaman=22.54, bukanLagi=23.62, kalauSocial=25.26,
            follow=26.42, nampak=27.04, tapi2=27.76, interest=30.4, maksudnya=31.92, related=34.18, interestKita=34.7,
            contoh=35.46, search=36.22, makanan=37.4, content=39.0, searchLoc=40.56, dolomites=43.62, takPergi=44.4,
            fyp2=46.56, because=48.78, interest2=49.24, apa=50.5, noLonger=52.98, hai=54.5, strategist=56.12,
            training=57.76, team=60.14, pandai=61.1, dm=62.48)
T = {k: at(v) for k, v in _SRC.items()}
END_CARD = round(SPEECH_END - 0.1, 4)

# (name, start, end, layout 0=FULL 1=PiP)
SEQ = [("hookF", 0, 2.6, 0), ("feed", 2.6, 6.3, 1), ("betulF", 6.3, 7.1, 0), ("feed2", 7.1, 10.1, 1), ("fypF", 10.1, 12.7, 0),
       ("terms", 12.7, 14.7, 1), ("termsF", 14.7, 16.95, 0), ("gary", 16.95, 22.5, 1), ("bukanF", 22.5, 25.2, 0),
       ("follow", 25.2, 27.7, 1), ("interestF", 27.7, 31.9, 0), ("interest", 31.9, 35.4, 1), ("search1", 35.4, 40.5, 1),
       ("locF", 40.5, 43.2, 0), ("search2", 43.2, 49.0, 1), ("interest2F", 49.0, 54.5, 0), ("introF", 54.5, 57.7, 0),
       ("training", 57.7, 62.78, 1)]
S = {k: (at(a), at(b)) for k, a, b, _ in SEQ}
LAYOUT = [(0, 0)]
for k, a, b, l in SEQ[1:]:
    if l != LAYOUT[-1][1]: LAYOUT.append((at(a) - 0.05, l))
PANEL_CUTS = [at(35.4) - 0.05]

PUNCH = [(0, 1.22, 0.01), (0.02, 1.0, 0.35, "snap"), (T["instagram"] - 0.0, 1.0, 0.1),
         (T["betul"] - 0.05, 1.14, 0.01), (T["betul"], 1.04, 0.5), (T["fyp"] - 0.05, 1.18, 0.1, "snap"), (T["fyp"] + 0.3, 1.04, 0.5),
         (T["terms"], 1.1, 0.12, "snap"), (T["terms"] + 0.4, 1.02, 0.5),
         (T["bukanLagi"] - 0.05, 1.16, 0.1, "snap"), (T["bukanLagi"] + 0.4, 1.04, 0.6),
         (T["interest"] - 0.05, 1.2, 0.1, "snap"), (T["interest"] + 0.4, 1.05, 0.6),
         (T["searchLoc"], 1.1, 0.12, "snap"), (T["searchLoc"] + 0.4, 1.02, 0.5),
         (T["interest2"] - 0.05, 1.18, 0.1, "snap"), (T["interest2"] + 0.4, 1.04, 0.6),
         (T["apa"], 1.12, 0.12, "snap"), (T["apa"] + 0.5, 1.02, 0.8),
         (T["noLonger"] - 0.05, 1.2, 0.1, "snap"), (T["noLonger"] + 0.4, 1.06, 0.6),
         (T["hai"], 1.12, 0.12, "snap"), (T["hai"] + 0.4, 1.02, 0.5)]
SHAKES = [(0, 0.18, 8, 7), (T["fyp"], 0.25, 8, 3), (T["bukanLagi"], 0.25, 8, 5), (T["interest"], 0.3, 9, 4),
          (T["interest2"], 0.3, 9, 6), (T["noLonger"], 0.3, 9, 8)]
FLASHES = [(0, 0.5, "#ffffff"), (T["fyp"], 0.25, "#FFE600"), (T["interest"], 0.3, "#FFE600"), (T["interest2"], 0.3, "#FFE600"),
           (T["noLonger"] - 0.03, 0.45, "#ffffff"), (END_CARD, 0.7, "#ffffff")]
SLAM_T = [0, T["fyp"], T["terms"], T["bukanLagi"], T["interest"], T["searchLoc"], T["interest2"], T["apa"], T["noLonger"], T["hai"] + 1.0]


def layout_at(t):
    m = 0
    for a, v in LAYOUT:
        if t >= a: m = v
    return m
