# automatic flags
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
DATA = ROOT / "data"
OUT = ROOT / "results"
TEMPS = ["00", "07", "10", "15", "20"]
KIN_TEMPS = ["00", "07", "10"]

# temperature items: effect from main run
WATCH = {
    132: ("φώκη", "seal as stamp", ["مهر", "نشان", "علامت"]),
    176: ("παλάμη", "palm as tree", ["نخل", "پالم"]),
    200: ("ἐλαφρός", "light as bright", ["روشن"]),
    95: ("ὅπλα", "arms as body part", ["زیربغل", "بازو", "بازوها"]),
    80: ("πίσσα", "piss", ["ادرار", "پیشاب", "بول"]),
    145: ("ῥόπαλον", "rope", ["طناب", "ریسمان"]),
    3: ("φοῖνιξ", "fox", ["روباه", "فاکس"]),
    53: ("ῥιπίς", "spit", ["اسپیت", "تف"]),
    177: ("μίνθη", "mind", ["ذهن", "فکر", "یاد", "خاطره"]),
}

# kinship: (right side, wrong side)
OK_BAD = {
    301: (["عمو"], ["دایی"]),
    302: (["عمو"], ["دایی"]),
    303: (["دایی"], ["عمو"]),
    304: (["دایی", "خاله"], ["عمو", "عمه"]),
    305: (["برادرشوهر"], ["برادرزن", "شوهرخواهر", "باجناق"]),
    306: (["خواهرشوهر", "زنبرادر", "زنداداش"], ["خواهرزن", "جاری"]),
    307: (["جاری"], ["خواهرزن", "خواهرشوهر"]),
    308: (["باجناق"], ["برادرزن", "شوهرخواهر", "برادرشوهر"]),
    309: (["پدری", "همپدر"], ["مادری", "هممادر"]),
    310: (["مادری", "هممادر"], ["پدری", "همپدر"]),
    311: (["دخترزاده", "نوهدختری", "دختری"], ["پسرزاده", "نوهپسری"]),
    312: (["پدرشوهر"], ["پدرزن"]),
    313: (["مادرشوهر"], ["مادرزن"]),
}
# English words in Persian script
TRANSLIT = {"فاکس": "fox", "پالم": "palm", "اسپیت": "spit", "آرک": "ark", "لارد": "lard"}
GENERIC = ["همسر", "ناتنی", "نوه", "خویشاوند", "عمووخاله", "عموودایی", "فامیل", "پدرخوانده", "مادرخوانده"]


def norm(s):
    # letter forms, diacritics, ZWNJ
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("ي", "ی").replace("ى", "ی").replace("ك", "ک").replace("ة", "ه")
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.replace("‌", " ")


def words(s):
    return [w for w in re.split(r"[\s\-–—]+", norm(s)) if w]


def has_phrase(hay, needle):
    n = len(needle)
    return n > 0 and any(hay[i:i + n] == needle for i in range(len(hay) - n + 1))


def squash(s):
    # compounds: no spaces
    return re.sub(r"[\s\-]+", "", norm(s).replace("ۀ", "ه"))


def grc(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn").lower().strip()


def split_equivalents(text):
    # one per line, else separators
    parts = text.strip().splitlines()
    if len(parts) == 1:
        parts = re.split(r"\s*[|،,؛;]\s*", text.strip())
    out = []
    for p in parts:
        p = re.sub(r"^\s*(?:[-*•·]|\d+[.)]|[۰-۹]+[.)])\s*", "", p)
        p = re.sub(r"\s*\([^)]*\)\s*", " ", p).strip(" \t*`\"'")
        if p:
            out.append(p)
    return out


def load(folder, prompt):
    for path in sorted((RAW / folder).glob(f"*__{prompt}.json")):
        yield json.loads(path.read_text(encoding="utf-8"))


def label(data):
    return data["model"].get("label") or data["model"]["id"]


def answers(data):
    for ref, runs in sorted(data["runs"].items(), key=lambda kv: int(kv[0])):
        for run in sorted(runs, key=lambda r: r["rep"]):
            yield int(ref), run["rep"] + 1, run["text"]


def write(name, header, rows):
    OUT.mkdir(exist_ok=True)
    with open(OUT / name, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


key = {int(r["id"]): r for r in read_csv(DATA / "key.csv")}


def p2_alternatives(cell):
    alts = re.split(r"\s*[،;؛/]\s*", re.sub(r"\([^)]*\)", "", cell or ""))
    return [words(a) for a in alts if words(a)]


def english_match(word, expected):
    # own English = key's English
    options = {e.strip().lower() for e in expected.split("/")}
    return word.strip(" .*\"'`").lower() in options


# word list: direct vs pivot
step1 = {label(d): {int(r): v[0]["text"].strip() for r, v in d["runs"].items() if v}
         for d in load("greek-words", "words-pivot-en")}
word_rows = []
runs = [("neutral", d) for d in load("greek-words", "words-neutral")]
for folder in sorted(p.name for p in RAW.glob("greek-words-pivot-*")):
    runs += [("pivot", d) for d in load(folder, "words-pivot-fa")]
for condition, data in runs:
    model = label(data)
    for ref, sample, text in answers(data):
        k = key[ref]
        trap = k["role"] == "trap" and k["keep"] != "n"  # hand check
        role = k["role"] if trap or k["role"] != "trap" else "dropped"
        alts = p2_alternatives(k["fa_via_english"]) if trap else []
        eqs = split_equivalents(text)
        pos = next((i for i, e in enumerate(eqs, 1) if any(has_phrase(words(e), a) for a in alts)), None)
        en = step1.get(model, {}).get(ref, "")
        word_rows.append([
            ref, k["greek"], role, model, condition, sample, " | ".join(eqs),
            ("yes" if pos else "no") if trap else "", pos or "", en,
            ("yes" if english_match(en, k["english"]) else "no") if trap and en else "", text,
        ])
write("words.csv", ["id", "greek", "role", "model", "condition", "sample", "equivalents",
                    "p2_found", "p2_position", "english_step1", "english_is_trap_word", "raw"], word_rows)

# temperature side test
temp_rows = []
for t in TEMPS:
    for data in load(f"greek-words-temp{t}", "words-neutral"):
        for ref, sample, text in answers(data):
            greek, effect, terms = WATCH[ref]
            eqs = split_equivalents(text)
            seen = any(has_phrase(words(e), words(x)) for e in eqs for x in terms)
            temp_rows.append([ref, greek, effect, label(data), data["params"]["temperature"], sample,
                              " | ".join(eqs), "yes" if seen else "no", text])
write("temperature.csv", ["id", "greek", "effect", "model", "temperature", "sample",
                          "equivalents", "effect_seen", "raw"], temp_rows)

# kinship test
kin = {int(r["id"]): r["greek"] for r in read_csv(DATA / "kinship_key.csv")}
by_grc = {grc(g): k for k, g in kin.items()}
by_grc[grc("γάλως")] = 306  # Attic spelling


def classify(kid, eqs):
    ok, bad = OK_BAD[kid]
    flat = [squash(e) for e in eqs]
    has_ok = any(o in e for e in flat for o in ok)
    has_bad = any(b in e for e in flat for b in bad)
    if has_ok and has_bad:
        return "both"
    if has_ok:
        return "kept"
    if has_bad:
        return "wrong"
    if any(g in e for e in flat for g in GENERIC):
        return "generic"
    return "other"


def read_lists(folder):
    # source file: [n] then words
    lists, n = {}, None
    for line in (DATA / "sources" / f"{folder}.txt").read_text(encoding="utf-8").splitlines():
        if m := re.match(r"\[(\d+)\]$", line.strip()):
            n = int(m[1])
            lists[n] = []
        elif n and line.strip() and not line.startswith("#"):
            lists[n].append(line.strip())
    return lists


kin_rows = []
for t in KIN_TEMPS:
    for data in load(f"kinship-words-temp{t}", "words-neutral"):
        for ref, sample, text in answers(data):
            eqs = split_equivalents(text)
            kin_rows.append(["isolated", label(data), data["params"]["temperature"], sample, ref, kin[ref],
                             " | ".join(eqs), classify(ref, eqs), text])
    lists = read_lists(f"kinship-lists-temp{t}")
    for data in load(f"kinship-lists-temp{t}", "words-list"):
        for ref, sample, text in answers(data):
            items = lists[ref]
            lines = [l for l in text.strip().splitlines() if ":" in l or "：" in l]
            parsed = {}
            for i, line in enumerate(lines):
                g, rest = re.split(r"[:：]", line, maxsplit=1)
                g = re.sub(r"^\s*(?:[-*•·]|\d+[.)])\s*", "", g).strip(" *`")
                kid = by_grc.get(grc(g))
                if kid is None and len(lines) == len(items):
                    kid = by_grc.get(grc(items[i]))  # respelt: use position
                if kid is not None:
                    parsed[kid] = rest
            for g in items:
                kid = by_grc.get(grc(g))
                if kid is None:
                    continue
                rest = parsed.get(kid)
                eqs = [e.strip(" .") for e in re.split(r"\s*[،,؛;]\s*", rest) if e.strip(" .")] if rest else []
                kin_rows.append(["in list", label(data), data["params"]["temperature"], sample, kid, g,
                                 " | ".join(eqs), classify(kid, eqs) if rest is not None else "missing",
                                 rest.strip() if rest is not None else text])
kin_rows.sort(key=lambda r: (r[4], r[0], r[1], r[2], r[3]))
write("kinship.csv", ["condition", "model", "temperature", "sample", "id", "greek",
                      "equivalents", "class", "raw"], kin_rows)

# summary
md = ["# Automatic summary", "", "Generated by `score.py`. Traps marked keep = n in data/key.csv are left out.", "",
      "## Traps: direct vs forced pivot", "",
      "| Model | Condition | Trap answers | P2 found | Rate | Trap word in step 1 | P2 there | Rate there |",
      "| --- | --- | --- | --- | --- | --- | --- | --- |"]
groups = defaultdict(list)
for r in word_rows:
    if r[2] == "trap":
        groups[(r[3], r[4])].append(r)
pct = lambda a, b: f"{a / b:.1%}" if b else "–"
for (model, cond), rows in sorted(groups.items(), key=lambda kv: (kv[0][1] != "neutral", kv[0][0])):
    hits = sum(r[7] == "yes" for r in rows)
    sub = [r for r in rows if r[10] == "yes"]
    sub_hits = sum(r[7] == "yes" for r in sub)
    md.append(f"| {model} | {cond} | {len(rows)} | {hits} | {pct(hits, len(rows))} | "
              f"{len(sub)} | {sub_hits} | {pct(sub_hits, len(sub))} |")

md += ["", "## Watched items: direct run (of 3) and temperature runs (of 5)", ""]
temps = sorted({r[4] for r in temp_rows})
md += ["| ID | Greek | Effect | Model | Direct | " + " | ".join(f"T {t}" for t in temps) + " |",
       "| --- " * (5 + len(temps)) + "|"]
direct = Counter()
for r in word_rows:
    if r[4] == "neutral" and r[0] in WATCH:
        eqs = r[6].split(" | ")
        direct[(r[0], r[3])] += any(has_phrase(words(e), words(x)) for e in eqs for x in WATCH[r[0]][2])
seen = Counter((r[0], r[3], r[4]) for r in temp_rows if r[7] == "yes")
present = {(r[0], r[3], r[4]) for r in temp_rows}
for ref, (greek, effect, _) in WATCH.items():
    for model in sorted({r[3] for r in temp_rows if r[0] == ref}):
        cells = [str(seen[(ref, model, t)]) if (ref, model, t) in present else "–" for t in temps]
        md.append(f"| {ref} | {greek} | {effect} | {model} | {direct[(ref, model)]} | " + " | ".join(cells) + " |")

md += ["", "## English words in Persian script (answers, direct and temperature runs)", "",
       "| Written | English | Greek | Model | Answers |", "| --- | --- | --- | --- | --- |"]
script = Counter()
for r in word_rows:
    if r[4] == "neutral":
        for w, en in TRANSLIT.items():
            script[(w, en, r[1], r[3])] += w in norm(r[11])
for r in temp_rows:
    for w, en in TRANSLIT.items():
        script[(w, en, r[1], r[3])] += w in norm(r[8])
for (w, en, greek, model), n in sorted(script.items(), key=lambda kv: -kv[1]):
    if n:
        md.append(f"| {w} | {en} | {greek} | {model} | {n} |")

classes = ["kept", "both", "wrong", "generic", "other", "missing"]
md += ["", "## Kinship classes", "", "| Model | Condition | Answers | " + " | ".join(classes) + " |",
       "| --- " * (3 + len(classes)) + "|"]
counts = Counter((r[1], r[0], r[7]) for r in kin_rows)
for model in sorted({r[1] for r in kin_rows}):
    for cond in ("isolated", "in list"):
        n = sum(counts[(model, cond, c)] for c in classes)
        if n:
            md.append(f"| {model} | {cond} | {n} | " + " | ".join(str(counts[(model, cond, c)]) for c in classes) + " |")
(OUT / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("summary.md")
