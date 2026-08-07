# -*- coding: utf-8 -*-
"""把内容编译成 app/src/main/assets/data.js"""
import json, os, sys, io
import engine as E
from content_articles import ARTICLES
from content_phonemes import PHONEMES, MINIMAL_PAIRS
from content_phonics import LEVELS, WORDBANK

MISSING = set()

def syl_detail(word, phones):
    """按音节给出 IPA + 谐音 + 重音"""
    s2 = E.syllabify(phones)
    parts = E.word_parts(word, phones)
    if len(parts) != len(s2):
        parts = None                       # 人工覆盖的多音节词不拆
    out, idx = [], 0
    for i, (onset, nuc, coda) in enumerate(s2):
        n = len(onset) + (1 if nuc is not None else 0) + len(coda)
        out.append({"ipa": ''.join(E.sym(phones[idx + k]) for k in range(n)),
                    "st": E.stress(nuc) if nuc is not None else -1,
                    "cn": parts[i] if parts else ''})
        idx += n
    if parts is None and out:
        out = [{"ipa": E.to_ipa(phones), "st": 1, "cn": E.word_xieyin(word, phones)}]
    return out

def w(word):
    ph = E.lookup(word)
    if ph is None:
        MISSING.add(word.lower())
        return {"t": word, "p": "", "c": ""}
    return {"t": word, "p": E.to_ipa(ph), "c": E.word_xieyin(word, ph)}

def wd(word):
    ph = E.lookup(word)
    if ph is None:
        MISSING.add(word.lower()); return None
    return {"t": word, "p": E.to_ipa(ph), "c": E.word_xieyin(word, ph), "s": syl_detail(word, ph)}

# ---------------------------------------------------------------- 文章
arts = []
for a in ARTICLES:
    lines = []
    for en, zh in a["lines"]:
        toks, miss = E.annotate(en)
        MISSING.update(miss)
        lines.append({"en": en, "zh": zh, "cn": E.sent_xieyin(toks),
                      "tk": [{"t": t["t"], "p": t.get("p", ""), "c": t.get("c", ""), "w": t["w"]} for t in toks]})
    arts.append({k: a[k] for k in ("id", "tag", "level", "title", "title_zh", "note")} | {"lines": lines})

# ---------------------------------------------------------------- 音标
phs = []
for i, p in enumerate(PHONEMES):
    phs.append({"id": "P%02d" % i, "g": p["g"], "sym": p["sym"], "cn": p["cn"], "like": p["like"],
                "tip": p["tip"], "err": p["err"], "words": [w(x) for x in p["words"]]})
pairs = []
for a, b, ws, note in MINIMAL_PAIRS:
    pairs.append({"a": a, "b": b, "note": note,
                  "ws": [[w(x), w(y)] for x, y in ws]})

# ---------------------------------------------------------------- 拼读
lvs = []
for L in LEVELS:
    rules = []
    for r in L["rules"]:
        rules.append({"p": r["p"], "s": r["s"], "note": r["note"], "ex": [w(x) for x in r["ex"]]})
    lvs.append({"id": L["id"], "title": L["title"], "goal": L["goal"], "rules": rules, "quiz": L["quiz"]})

# ---------------------------------------------------------------- 词库
wbs = []
for g in WORDBANK:
    seen, items = set(), []
    for x in g["words"]:
        x = x.strip()
        if not x or x.lower() in seen: continue
        seen.add(x.lower())
        d = wd(x)
        if d: items.append(d)
    wbs.append({"id": g["id"], "title": g["title"], "desc": g["desc"], "words": items})

data = {"articles": arts, "phonemes": phs, "pairs": pairs, "levels": lvs, "wordbank": wbs}

out = os.path.join(os.path.dirname(__file__), "..", "app", "src", "main", "assets", "data.js")
os.makedirs(os.path.dirname(out), exist_ok=True)
with io.open(out, "w", encoding="utf-8") as f:
    f.write("window.DATA=")
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";")

n_sent = sum(len(a["lines"]) for a in arts)
n_word = sum(len(g["words"]) for g in wbs)
print("文章 %d 篇 / %d 句" % (len(arts), n_sent))
print("音标 %d 个，对比组 %d 组" % (len(phs), len(pairs)))
print("拼读 %d 关，规则 %d 条，题 %d 道" % (len(lvs), sum(len(l["rules"]) for l in lvs), sum(len(l["quiz"]) for l in lvs)))
print("词库 %d 组 / %d 词" % (len(wbs), n_word))
print("data.js  %.1f KB" % (os.path.getsize(out) / 1024))
if MISSING:
    print("\n!! 词典缺失 %d 个：" % len(MISSING))
    print(" ".join(sorted(MISSING)))
