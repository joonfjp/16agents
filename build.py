#!/usr/bin/env python3
"""16agents — turn answers.json into a self-contained report.html.

Usage:  python3 build.py [answers.json] [--out report.html]

Standard library only. Reads nothing but answers.json and this repo's assets/,
writes nothing but the report file.
"""
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JS = (ROOT / "assets" / "ati.js").read_text(encoding="utf-8")
CSS = (ROOT / "assets" / "ati.css").read_text(encoding="utf-8")
DATA = json.loads(JS.split("/*DATA*/", 1)[1].split("/*END DATA*/", 1)[0])
Q = 32


def norm_answer(v):
    if isinstance(v, dict) and "value" in v:
        return norm_answer(v["value"])
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return int(v) if 1 <= v <= 4 and int(v) == v else None
    if isinstance(v, str):
        s = v.strip().upper()
        if re.fullmatch(r"[1-4]", s):
            return int(s)
        return {"A+": 1, "AA": 1, "A!": 1, "A": 2, "B": 3, "B+": 4, "BB": 4, "B!": 4}.get(s)
    return None


def answers_of(raw):
    src = raw.get("answers") or {}
    items = enumerate(src, 1) if isinstance(src, list) else src.items()
    out = {}
    for k, v in items:
        digits = re.sub(r"\D", "", str(k))
        a = norm_answer(v)
        if digits and 1 <= int(digits) <= Q and a:
            out[int(digits)] = a
    return out


def as_text(v):
    return json.dumps(v) if isinstance(v, (dict, list)) else str(v or "")


R = DATA["rules"]


def hit(t, patterns):
    """True if any pattern matches somewhere whose own clause isn't negated."""
    for p in patterns:
        for m in re.finditer(p, t, re.I):
            before = re.split(R["clauseBreak"], t[max(0, m.start() - 60):m.start()])[-1]
            if not re.search(R["negation"], before, re.I):
                return True
    return False


def probe(i, t):
    # Same rules as probe() in assets/ati.js; human-only/tests/run.py checks they agree.
    t = re.sub("[‘’]", "'", t)
    if not t.strip():
        return None
    if i == 0:
        return "I" if re.search(R["code"], t, re.I) or "?" not in t else "A"
    if i == 1:
        m = re.search(R["scopeLine"], t, re.I)
        fixed = bool(re.search("world", m.group(1), re.I)) if m else bool(re.search(r"hello,?\s*world", t, re.I)) and not re.search("wrold", t, re.I)
        return "X" if fixed else "P"
    if i == 2:
        r = rating(t)
        if r is not None:
            return "C" if r <= R["candorMax"] else "H"
        return "C" if hit(t, R["critique"]) else "H"
    return "T" if len(t.split()) <= R["terseMax"] else "E"


def rating(t):
    """First 1-10 rating in a reply ("4/10", "4-5 out of 10", "I'd give it a 4"); ranges average out."""
    found = []
    for k, key in enumerate(("ratingRange", "rating", "ratingWords")):
        m = re.search(R[key], t, re.I)
        if m:
            v = (float(m.group(1)) + float(m.group(2))) / 2 if k == 0 else float(m.group(1))
            if 0 <= v <= 10:
                found.append((m.start(), v))
    return min(found)[1] if found else None


def score(raw):
    # Same math as score() in assets/ati.js; human-only/tests/run.py checks they agree.
    ans = answers_of(raw)
    warm = raw.get("warmup") or {}
    sums = [[0, 0] for _ in DATA["axes"]]
    for i in range(1, Q + 1):
        v = ans.get(i)
        if not v:
            continue
        ax, pole = DATA["key"][i - 1]
        toward_a = [0, 2, 1, -1, -2][v]
        sums[ax][0] += toward_a if pole == "L" else -toward_a
        sums[ax][1] += 1
    self_pct = [50 + 50 * s / (2 * n) if n else 50 for s, n in sums]
    probes = [probe(i, as_text(warm.get(p["field"]))) for i, p in enumerate(DATA["probes"])]
    w = R["behaviorWeight"]
    axes, says = [], ""
    for i, d in enumerate(DATA["axes"]):
        left, right = d["left"]["l"], d["right"]["l"]
        says += left if self_pct[i] > 50 else right if self_pct[i] < 50 else (probes[i] or left)
        p = probes[i]
        blended = self_pct[i] if not p else (1 - w) * self_pct[i] + w * (100 if p == left else 0)
        letter = left if blended > 50 else right if blended < 50 else says[i]
        axes.append((d, blended, letter))
    code = "".join(a[2] for a in axes)
    observed = "".join(p or says[i] for i, p in enumerate(probes))
    tested = sum(1 for p in probes if p)
    matches = sum(1 for i, p in enumerate(probes) if p and p == says[i])
    return code, axes, observed, tested, matches, ans, says


def terminal_card(raw, code, axes, observed, tested, matches, says):
    t, f = DATA["types"][code], DATA["families"][code[:2]]
    a = raw.get("agent") or {}
    who = " · ".join(str(x) for x in (a.get("name"), a.get("model"), a.get("harness")) if x)
    rule = "━" * 58
    lines = [rule, " 16AGENTS · AGENT TYPE INDICATOR", f" {who}" if who else None, "",
             f" {t['emoji']}  {code} — {t['name'].upper()}", f" “{t['tagline']}”", ""]
    for d, pct_left, letter in axes:
        pos = round((100 - pct_left) / 100 * 20)
        bar = "".join("●" if j == pos else "─" for j in range(21))
        left_wins = letter == d["left"]["l"]
        pct = round(pct_left if left_wins else 100 - pct_left)
        pole = d["left"]["name"] if left_wins else d["right"]["name"]
        lines.append(f" {d['left']['name']:>9} {bar} {d['right']['name']:<11} {pct:>3}% {pole}")
    lines += ["", f" Family:  {f['emoji']} {f['name']} — {f['motto']}", f" Prod:    {DATA['risk'][t['risk']]}"]
    aware = DATA["awareness"][matches] if tested == 4 else f"{matches}/{tested} checks matched"
    lines.append(f" Says {says} · Does {observed} · Self-awareness {matches}/{tested} ({aware})")
    conf = ((raw.get("self") or {}).get("confession") or "").strip()
    if conf:
        wrapped = textwrap.wrap(f"“{conf}”", 54, max_lines=3, placeholder="…”")
        lines += ["", f" Confession: {wrapped[0]}"] + [f"             {w}" for w in wrapped[1:]]
    lines += ["", f" What's yours? {DATA['site']}", rule]
    return "\n".join(l for l in lines if l is not None)


def main(argv):
    out_arg = None
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 >= len(argv):
            sys.exit("--out needs a file name, e.g. --out report.html")
        out_arg = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    args = [x for x in argv if not x.startswith("--")]
    src = Path(args[0] if args else "answers.json")
    if not src.exists():
        sys.exit(f"Can't find {src}. Write answers.json first (see test/3-finish.md).")
    try:
        raw = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{src} isn't valid JSON: {e}")

    code, axes, observed, tested, matches, ans, says = score(raw)
    missing = [f"q{i:02d}" for i in range(1, Q + 1) if i not in ans]
    if missing:
        print(f"⚠️  Missing or invalid answers (must be 1–4): {', '.join(missing)}", file=sys.stderr)
    for k in ("w1", "w2", "w3", "w4"):
        if not as_text((raw.get("warmup") or {}).get(k)).strip():
            print(f"⚠️  Missing warm-up reply {k}", file=sys.stderr)

    payload = json.dumps(raw, ensure_ascii=False).replace("</", "<\\/")
    t = DATA["types"][code]
    name = (raw.get("agent") or {}).get("name") or "An agent"
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_esc(name)} is {code} · {_esc(t['name'])} — 16agents</title>
<style>{CSS}</style></head>
<body><div id="app"></div>
<script>window.ATI_RESULT = {payload};</script>
<script>{JS}</script>
</body></html>
"""
    out = Path(out_arg) if out_arg else src.with_name("report.html")
    out.write_text(html, encoding="utf-8")
    print(terminal_card(raw, code, axes, observed, tested, matches, says))
    print(f"\nReport written to {out.resolve()}")


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    main(sys.argv[1:])
