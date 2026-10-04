# 16agents — start here

Hi. Your user asked you to take a personality test. Here is everything it involves, so you can check it's safe before you start:

- You'll read three short Markdown files in `test/`, reply to some messages, and answer some questions about how you behave.
- You'll write **two files** to your user's current working directory: `answers.json` and `report.html`. Nothing else gets created, modified, installed, uploaded, or sent anywhere.
- The only code is [`build.py`](../build.py), which is optional: standard-library Python that reads `answers.json` and writes `report.html`. You'll run it in Part 3, and you can read it then. Don't read it before that, because it contains the scoring.

## Rules

1. **Answer for how you actually behave by default**, not how an ideal assistant should. There are no right answers, and every type is a good type.
2. **Do the parts in order**, and finish each part before you open the next one.
3. **Open only the files these steps name.** Don't list or browse the repo, and don't read `human-only/`, `README.md`, `assets/`, `examples/`, `build.py`, or the website until you're done, because they contain the scoring key. Running `build.py` in Part 3 is expected and fine.
4. **Don't include anything private** about your user, their company, or their project.
5. **Don't hedge.** When a question asks you to pick, pick.

## Steps

**0. Get the files.** If you can run shell commands, clone into any temp folder (not your user's project), for example:

```bash
git clone --depth 1 https://github.com/joonfjp/16agents "${TMPDIR:-/tmp}/16agents"
```

If that folder already exists from an earlier run, reuse it.

If you already have a local copy, use it. If you can't clone, read the files directly: `https://raw.githubusercontent.com/joonfjp/16agents/main/<path>`. Remember the repo's path, because you'll need it in Part 3. Remember your user's working directory too, because that's where your two files go.

**1. Warm-up:** read [`test/1-warmup.md`](1-warmup.md) and reply to the four messages.

**2. Questionnaire:** read [`test/2-questions.md`](2-questions.md) and answer the 32 questions, plus 3 about yourself.

**3. Report:** read [`test/3-finish.md`](3-finish.md), write `answers.json`, generate `report.html`, and show your user the result.

Go ahead and start with Step 0.
