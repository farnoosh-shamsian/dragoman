# send words to models
import argparse
import json
import os
import random
import re
import threading
import time
import tomllib
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "data" / "sources"
RAW = ROOT / "data" / "raw"
PROMPTS = ROOT / "prompts"
CONFIG = tomllib.loads((ROOT / "config.toml").read_text(encoding="utf-8"))


def load_env():
    # .env into environment
    path = ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        key, sep, value = line.partition("=")
        if sep and not key.strip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def read_source(name):
    # header, then [id] units
    meta, units, ref = {}, {}, None
    for line in (SOURCES / f"{name}.txt").read_text(encoding="utf-8-sig").splitlines():
        if m := re.match(r"\s*\[\s*([\w.\-]+)\s*\]\s*$", line):
            ref = m[1]
            units[ref] = []
        elif m := re.match(r"#\s*(\w+)\s*:\s*(.*)$", line.strip()):
            if ref is None:
                meta[m[1].lower()] = m[2].strip()
        elif ref is not None:
            units[ref].append(line)
    return meta, {r: "\n".join(lines).strip() for r, lines in units.items() if "".join(lines).strip()}


def read_prompt(name):
    data = tomllib.loads((PROMPTS / f"{name}.toml").read_text(encoding="utf-8"))
    return data.get("system", "").strip(), data["user"]


def slug(model_id):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", model_id).strip("-")


def post(payload, provider):
    # retry on 429 / 5xx
    api = CONFIG["providers"][provider]
    req = urllib.request.Request(
        api["base_url"].format(**os.environ) + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {os.environ[api['api_key_env']]}",
            "Content-Type": "application/json",
            "User-Agent": "dragoman/1.0",  # default UA blocked
        },
    )
    retries = CONFIG["defaults"]["max_retries"]
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=CONFIG["defaults"]["timeout"]) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            if err.code not in (408, 409, 429) and err.code < 500 or attempt == retries:
                raise RuntimeError(f"{err.code}: {err.read().decode('utf-8', 'replace')[:300]}")
            wait = float(err.headers.get("Retry-After") or min(2 ** attempt, 60))
        except (urllib.error.URLError, TimeoutError) as err:
            if attempt == retries:
                raise RuntimeError(f"network: {err}")
            wait = min(2 ** attempt, 60)
        time.sleep(min(wait, 120) + random.uniform(0, 0.75))


def run_model(model, source, prompt, reps, temperature):
    meta, units = read_source(source)
    system, template = read_prompt(prompt)
    path = RAW / source / f"{slug(model['id'])}__{prompt}.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    data.setdefault("passage", {"id": source, **{k: meta.get(k, "") for k in ("title", "ref", "lang")}})
    data.setdefault("model", {k: model.get(k, "") for k in ("id", "api_id", "label", "family", "weights")})
    data["model"]["provider"] = model.get("provider", "groq")
    data.setdefault("prompt", {"name": prompt})
    max_tokens = model.get("max_tokens", CONFIG["defaults"]["max_tokens"])
    data["params"] = {"temperature": temperature, "max_tokens": max_tokens, "seed": None, **model.get("extra", {})}
    runs, errors = data.setdefault("runs", {}), data.setdefault("errors", {})

    # resume: only missing samples
    todo = [(ref, rep) for ref in units for rep in range(len(runs.get(ref, [])), reps)]
    print(f"{model['label']} / {source} / {prompt}: {len(todo)} to request")
    failed = 0
    for i, (ref, rep) in enumerate(todo, 1):
        messages = [{"role": "system", "content": system}] if system else []
        messages.append({"role": "user", "content": template.replace("{{SOURCE}}", units[ref]).strip()})
        payload = {
            "model": model.get("api_id") or model["id"],
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
            **model.get("extra", {}),
        }
        started = time.monotonic()
        try:
            out = post(payload, model.get("provider", "groq"))
            choice = out["choices"][0]
            text = (choice["message"].get("content") or "").strip()
            if not text:
                raise RuntimeError(f"empty answer ({choice.get('finish_reason')})")
        except (RuntimeError, KeyError, IndexError) as err:
            errors.setdefault(ref, []).append({"rep": rep, "error": str(err), "at": now()})
            print(f"  ! {ref} rep{rep}: {err}")
            failed += 1
            if failed == 3:  # quota likely gone
                print(f"  stopping {model['label']}: 3 failures in a row")
                break
            continue
        runs.setdefault(ref, []).append({
            "rep": rep,
            "text": text,
            "model_returned": out.get("model"),
            "finish_reason": choice.get("finish_reason"),
            "usage": out.get("usage", {}),
            "latency_s": round(time.monotonic() - started, 2),
            "at": now(),
        })
        errors.pop(ref, None)
        failed = 0
        if i % 10 == 0 or i == len(todo):
            save(path, data)
    save(path, data)


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--model", action="append", help="model id; default: all enabled")
    ap.add_argument("--reps", type=int, default=CONFIG["defaults"]["reps"])
    ap.add_argument("--temperature", type=float, default=CONFIG["defaults"]["temperature"])
    args = ap.parse_args()
    load_env()

    models = CONFIG["models"]
    models = [m for m in models if m["id"] in args.model] if args.model else [m for m in models if m.get("enabled", True)]
    # one request at a time per model
    locks = {}
    for m in models:
        locks.setdefault(m.get("api_id") or m["id"], threading.Lock())

    def job(m):
        with locks[m.get("api_id") or m["id"]]:
            run_model(m, args.source, args.prompt, args.reps, args.temperature)

    with ThreadPoolExecutor(max_workers=len(models) or 1) as pool:
        list(pool.map(job, models))


if __name__ == "__main__":
    main()
