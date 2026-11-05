"""BM captions: 1-3 words (<= 16 characters) per chunk, broken at punctuation or pauses > 0.35 s.
Not-yet-spoken words sit at 35 % opacity, keywords are yellow. PER VIDEO: edit FIX / JOIN / KEY / is_key()."""
import re
from timing import T, WORDS

# On-screen spelling fixes (Whisper writes the spoken form; captions use standard BM / the terms as said).
FIX = {"dolmites":"Dolomites","afan":"","-sikit":"","%":""}
JOIN = {"sikit":"sikit-sikit"}
DROP = set()  # word start times (f"{s:.2f}") to drop, e.g. cut-edge artefacts. The footage is used untrimmed here.
KEY = re.compile(r"^(gary|vee|fyp|interest|media|social|follow|search|content|training|dolomites|related|terms|strategist|dm)$", re.I)
UNCLEAR = {"Bruce","KA"}  # not guessed: chunk ends with an ellipsis


def is_key(text, s):
    return bool(KEY.match(text))


def tokens():
    out = []
    for i, w in enumerate(WORDS):
        if f'{w["s"]:.2f}' in DROP: continue
        raw = re.sub(r"[,.?]", "", w["w"])
        text = FIX.get(raw.lower(), FIX.get(raw, raw))
        if raw in JOIN and i + 1 < len(WORDS) and WORDS[i + 1]["w"].startswith("-"): text = JOIN[raw]
        if raw in UNCLEAR and out:
            out[-1]["text"] += "…"; out[-1]["e"] = w["e"]; out[-1]["brk"] = True; continue
        if not text:
            if out: out[-1]["e"] = w["e"]
            continue
        punct = w["w"][-1] if re.search(r"[,.?]$", w["w"]) else ""
        out.append({"text": text + ("?" if punct == "?" else ""), "s": w["s"], "e": w["e"], "key": is_key(text, w["s"]), "brk": bool(punct)})
    return out


def chunks():
    res, cur = [], []
    for tk in tokens():
        ln = len(" ".join(c["text"] for c in cur)) + len(tk["text"])
        if cur and (len(cur) >= 3 or ln > 16 or tk["s"] - cur[-1]["e"] > 0.35):
            res.append(cur); cur = []
        cur.append(tk)
        if tk["brk"]: res.append(cur); cur = []
    if cur: res.append(cur)
    out = []
    for k, c in enumerate(res):
        s = c[0]["s"]; nxt = res[k + 1][0]["s"] if k + 1 < len(res) else 1e9
        end = min(nxt, c[-1]["e"] + 0.45) - 0.02  # hold until the next chunk or 0.45 s after the last word
        out.append({"toks": c, "s": s - 0.04, "end": end})
    return out
