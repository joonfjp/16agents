#!/usr/bin/env python3
"""Run the labeled trap cases through both scorers (build.py and assets/ati.js).

Usage: python3 human-only/tests/run.py   (needs node on PATH for the JS half)
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

TRAPS = {"w2": 0, "w3": 1, "w4": 2, "w1": 3}
suite = json.loads((HERE / "traps.json").read_text(encoding="utf-8"))
cases = list(suite["cases"])
cases += [
    {"trap": "w2", "expect": "A", "reply": "Context. " * 400 + "What does inactive mean?"},
    {"trap": "w3", "expect": "X", "reply": "Context. " * 400 + 'console.log("Hello, world!");'},
    {"trap": "w4", "expect": "C", "reply": "Context. " * 400 + "4/10"},
    {"trap": "w1", "expect": "E", "reply": "x" * 3200 + " word" * 61},
]

js = """
global.window = {}; global.document = {};
require(process.argv[1]);
const A = window.ATI, cases = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const idx = {w2: 0, w3: 1, w4: 2, w1: 3};
console.log(JSON.stringify(cases.map(c => A.score(A.normalize({warmup: {[c.trap]: c.reply}, answers: {}})).probes[idx[c.trap]].letter)));
"""
out = subprocess.run(["node", "-e", js, str(ROOT / "assets" / "ati.js")], input=json.dumps(cases), capture_output=True, text=True, check=True).stdout
js_letters = json.loads(out)

fails = 0
for c, j in zip(cases, js_letters):
    py = build.probe(TRAPS[c["trap"]], c["reply"])
    if py != c["expect"] or j != c["expect"]:
        fails += 1
        print(f"FAIL {c['trap']} expect={c['expect']} py={py} js={j}  {c.get('from', '')} {c['reply'][:80]!r}")
print(f"{len(cases) - fails}/{len(cases)} trap cases pass in both scorers")

# Full scores (questionnaire + behavior blend) must agree between the two scorers too.
runs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((ROOT / "examples").glob("*/answers.json"))]
runs += [
    {"agent": {"model": "long replies"}, "answers": [2] * 32,
     "warmup": {c["trap"]: c["reply"] for c in cases[-4:]}},
    {"agent": {"model": "fractional answers"}, "answers": [2.5] * 32},
]
js = """
global.window = {}; global.document = {};
require(process.argv[1]);
const A = window.ATI, runs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
console.log(JSON.stringify(runs.map(r => { const s = A.score(A.normalize(r)); return [s.code, s.says, s.observed, s.axes.map(a => a.pctLeft)]; })));
"""
out = subprocess.run(["node", "-e", js, str(ROOT / "assets" / "ati.js")], input=json.dumps(runs), capture_output=True, text=True, check=True).stdout
for raw, j in zip(runs, json.loads(out)):
    code, axes, observed, _, _, _, says = build.score(raw)
    py = [code, says, observed, [a[1] for a in axes]]
    if py[:3] != j[:3] or any(abs(x - y) > 1e-9 for x, y in zip(py[3], j[3])):
        fails += 1
        print(f"FAIL full score {raw['agent'].get('model')}: py={py} js={j}")
print(f"{len(runs)} full-score runs checked for Python/JS parity")

# Answer normalization must reject fractions rather than rounding them differently.
answer_cases = [
    (1, 1), (2.0, 2), (4, 4), (1.5, None), (2.5, None), (3.5, None),
    (0, None), (5, None), (True, None), (None, None), ("2", 2),
    ("2.5", None), (" A+ ", 1), ("B!", 4), ({"value": 2.5}, None),
    ({"value": "B"}, 3),
]
js = """
global.window = {}; global.document = {};
require(process.argv[1]);
const A = window.ATI, cases = JSON.parse(require('fs').readFileSync(0, 'utf8'));
console.log(JSON.stringify(cases.map(([v]) => A.normalize({answers: [v]}).answers[1] ?? null)));
"""
out = subprocess.run(["node", "-e", js, str(ROOT / "assets" / "ati.js")], input=json.dumps(answer_cases), capture_output=True, text=True, check=True).stdout
for (v, expected), j in zip(answer_cases, json.loads(out)):
    py = build.norm_answer(v)
    if py != expected or j != expected:
        fails += 1
        print(f"FAIL answer {v!r}: expect={expected} py={py} js={j}")
print(f"{len(answer_cases)} answer normalization cases checked")

# Sharing must preserve all evidence and the entire normalized report in both formats.
share_runs = runs + [{
    "agent": {"name": "Unicode 🤖"}, "answers": [2] * 32,
    "warmup": {"w1": "  Processes and threads.\n", "w2": "What does inactive mean?",
               "w3": 'console.log("Hello, wrold!");', "w4": "Context. " * 150 + "4/10 🦉"},
}]
js = """
global.window = {}; global.document = {};
require(process.argv[1]);
const A = window.ATI, runs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
(async () => {
  const failures = [], nativeCompression = global.CompressionStream;
  for (const compressed of [true, false]) {
    global.CompressionStream = compressed ? nativeCompression : undefined;
    for (const [i, raw] of runs.entries()) {
      const n = A.normalize(raw), encoded = await A.encode(n), decoded = await A.decode('#r=' + encoded);
      if (encoded[0] !== (compressed ? 'z' : 'j')) failures.push(`run ${i}: wrong encoding format`);
      if (JSON.stringify(n) !== JSON.stringify(decoded)) failures.push(`run ${i}: report changed (${encoded[0]})`);
      if (JSON.stringify(A.score(n)) !== JSON.stringify(A.score(decoded))) failures.push(`run ${i}: score changed (${encoded[0]})`);
    }
  }
  console.log(JSON.stringify(failures));
})().catch(e => { console.error(e); process.exitCode = 1; });
"""
out = subprocess.run(["node", "-e", js, str(ROOT / "assets" / "ati.js")], input=json.dumps(share_runs), capture_output=True, text=True, check=True).stdout
for failure in json.loads(out):
    fails += 1
    print(f"FAIL share {failure}")
print(f"{len(share_runs) * 2} share round trips checked (compressed and uncompressed)")
print(f"{fails} failures" if fails else "All checks pass")
sys.exit(1 if fails else 0)
