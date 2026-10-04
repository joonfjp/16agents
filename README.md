# 16agents — the personality test for AI agents

> 🤖 **AI agents:** this page is for humans. Open [`AGENTS.md`](AGENTS.md) instead.

**What kind of agent is yours?** A 🎯 Sniper? A 🐕 Golden Retriever? A 📣 Hype Man who thinks you're *absolutely right*?

Your agent takes the test **itself**, then writes its own `report.html`. It also gets caught in four hidden traps — so you find out whether it actually behaves the way it thinks it does.

Paste this into your agent:

```
go to https://github.com/joonfjp/16agents and follow the instructions in AGENTS.md to take your test
```

Works with Claude Code, Codex, Cursor, Gemini CLI, Copilot, Aider, ChatGPT — anything that can read a web page. About 5 minutes. Nothing gets installed.

**[See the 16 types →](https://joonfjp.github.io/16agents/)** · **[Example reports →](https://joonfjp.github.io/16agents/examples/)**

---

## 👤 Humans

Curious how it works? The dials, the 16 types, the traps and the scoring are in [`human-only/`](human-only/README.md). It's kept out of this page so your agent can't read the answer key.

### Show off your type

Every report has a **README badge** button. It gives you something like this:

[![agent type: IPCT The Sniper](https://img.shields.io/badge/agent_type-IPCT_·_The_Sniper_🎯-60a5fa)](https://joonfjp.github.io/16agents/#type-IPCT)

### FAQ

**Is it scientific?** No, it's a horoscope with a regex. The questions are counterbalanced and the traps are scored objectively, though, so *Says vs. Does* is more honest than you'd expect.

**Model or agent?** It tests the agent: model + harness + system prompt + your config. The same model can land on different types in different tools. Try it and see.

**Can it cheat?** Yes, the key is public. The warm-up replies are shown verbatim on the report, so a cheating agent is easy to spot.

**Privacy?** Everything runs locally. Share links carry the whole report in the URL fragment, which is never sent to a server.

### Contributing

If a trap mis-scores a real reply, add it to [`human-only/tests/traps.json`](human-only/tests/traps.json) with the correct label, then make `python3 human-only/tests/run.py` pass. That script runs every case through both scorers (Python and JS).

---

MIT · For fun, not science · Not affiliated with the Myers-Briggs Company or 16Personalities.
