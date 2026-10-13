# pivot step 2 sources
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "greek-words"
SOURCES = ROOT / "data" / "sources"


def slug(model_id):
    return re.sub(r"[^a-z0-9]+", "-", model_id.lower()).strip("-")


def clean(text):
    # first line, no glosses
    first = text.strip().splitlines()[0]
    first = re.sub(r"\s*\([^)]*\)", "", first)
    return first.strip(" .*\"'`")


for path in sorted(RAW.glob("*__words-pivot-en.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    model = data["model"]["id"]
    lines = [
        f"# title: Pivot step 2 source for {data['model'].get('label', model)}",
        f"# ref: English words from words-pivot-en, model {model}",
        "# lang: en",
        "# note: IDs match data/key.csv; the Greek has been removed on purpose.",
        "",
    ]
    for ref in sorted(data["runs"], key=int):
        if data["runs"][ref]:
            lines += [f"[{ref}]", clean(data["runs"][ref][0]["text"]), ""]
    out = SOURCES / f"greek-words-pivot-{slug(model)}.txt"
    out.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(out.name)
