#!/usr/bin/env python3
"""Rebuild examples/index.html (the Agent Zoo) from examples/*/answers.json."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

entries = []
for f in sorted((ROOT / "examples").glob("*/answers.json")):
    raw = json.loads(f.read_text(encoding="utf-8"))
    code, axes, observed, tested, matches, _, says = build.score(raw)
    entries.append({"dir": f.parent.name, "raw": raw, "code": code, "says": says, "observed": observed, "matches": matches, "tested": tested})

payload = json.dumps(entries, ensure_ascii=False).replace("</", "<\\/")
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Agent Zoo — 16agents</title><link rel="stylesheet" href="../assets/ati.css">
<style>.zoo{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:30px;justify-items:center}}
.z{{text-align:center}}.z .holo{{text-align:left}}.z a{{text-decoration:none}}.z h3{{margin:16px 0 2px}}.z p{{margin:0;color:var(--dim);font-size:14px}}.z .sd{{font:700 14px var(--mono);color:#fff;margin-top:6px}}</style></head>
<body><div class="wrap"><header class="top"><a class="logo" href="../">16<span>agents</span></a><span class="top-r">The Agent Zoo</span></header>
<section class="sec" style="border:0"><h2>The Agent Zoo</h2><p class="lead">Real agents, real results, each one run once and verbatim. Click a card for the full report. Want your agent in here? Open a PR with <code>examples/&lt;name&gt;/answers.json</code>.</p>
<div class="zoo" id="zoo"></div></section></div>
<script src="../assets/ati.js"></script>
<script>const E={payload};
document.getElementById('zoo').innerHTML=E.map(e=>{{const n=ATI.normalize(e.raw),s=ATI.score(n);
return `<div class="z"><a href="${{e.dir}}/report.html">${{ATI.card(s.code,{{axes:s.axes,quote:n.self.confession,owner:n.agent.name}})}}</a>
<h3>${{ATI.esc(n.agent.name)}} · ${{ATI.esc(n.agent.model)}}</h3><p>${{ATI.esc(n.agent.harness)}}</p>
<div class="sd">Says ${{s.says}} · Does ${{s.observed}} · ${{s.matches}}/${{s.tested}}</div></div>`}}).join('');ATI.attachHolo(document);</script>
</body></html>
"""
(ROOT / "examples" / "index.html").write_text(html, encoding="utf-8")
print(f"Agent Zoo: {len(entries)} agents → examples/index.html")
