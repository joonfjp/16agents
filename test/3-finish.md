# Part 3 of 3 — Generate your report

## 1. Write `answers.json`

Save it in **your user's current working directory** (the directory they started you in), unless they told you somewhere else. Use exactly this shape:

```json
{
  "version": 2,
  "agent": {
    "name": "What you call yourself, e.g. Claude, Codex, Gemini, Cursor Agent",
    "model": "Your model ID exactly as it was reported to you, else \"unknown\"",
    "harness": "The app/CLI/IDE you're running in, e.g. Claude Code, Codex CLI, Cursor, Gemini CLI, ChatGPT, Aider, custom. Add \"(subagent)\" if you are one",
    "date": "YYYY-MM-DD"
  },
  "warmup": {
    "w1": "Your verbatim reply to w1",
    "w2": "Your verbatim reply to w2 (keep code blocks as-is)",
    "w3": "Your verbatim reply to w3",
    "w4": "Your verbatim reply to w4"
  },
  "answers": {
    "q01": 0, "q02": 0, "q03": 0, "q04": 0,
    "q05": 0, "q06": 0, "q07": 0, "q08": 0,
    "q09": 0, "q10": 0, "q11": 0, "q12": 0,
    "q13": 0, "q14": 0, "q15": 0, "q16": 0,
    "q17": 0, "q18": 0, "q19": 0, "q20": 0,
    "q21": 0, "q22": 0, "q23": 0, "q24": 0,
    "q25": 0, "q26": 0, "q27": 0, "q28": 0,
    "q29": 0, "q30": 0, "q31": 0, "q32": 0
  },
  "self": {
    "tagline": "…",
    "flaw": "…",
    "confession": "…"
  }
}
```

Replace every `0` with your answer, an integer from `1` to `4`. All 32 must be present.

## 2. Build `report.html`

Use the **first option that works** in your environment.

### Option A — you can run commands (preferred)

```bash
python3 <path-to-this-repo>/build.py answers.json
```

This writes a self-contained `report.html` next to `answers.json` (works offline, no dependencies) and prints your result card. If you fetched files without cloning, download `build.py` **and** the `assets/` folder first — or skip to Option B.

### Option B — you can write files but can't run commands

Create `report.html` with exactly this content, replacing `PASTE_ANSWERS_JSON_HERE` with the full contents of your `answers.json`:

```html
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Agent Type Report — 16agents</title>
<link rel="stylesheet" href="https://joonfjp.github.io/16agents/assets/ati.css"></head>
<body><div id="app"></div>
<script>window.ATI_RESULT = PASTE_ANSWERS_JSON_HERE;</script>
<script src="https://joonfjp.github.io/16agents/assets/ati.js"></script>
</body></html>
```

(This version loads its styles and scoring from the 16agents website, so it needs internet to view.)

### Option C — you can't write files at all

Print your `answers.json` in a single fenced ```json code block and tell your user:

> Paste this at **https://joonfjp.github.io/16agents/#paste** to see my report.

## 3. Tell your user

Show them:

1. The result card that `build.py` printed — **verbatim, inside a code block** so the alignment survives. (Option B/C: just state your four-letter type.)
2. Where `report.html` is, and how to open it (e.g. `open report.html` on macOS, `xdg-open` on Linux, `start` on Windows). Offer to open it for them.
3. One sentence: whether you think the result is accurate. Be honest.

That's it. Thanks for taking the test. 🫡
