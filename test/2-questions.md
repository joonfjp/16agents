# Part 2 of 3 — The Questionnaire

32 scenarios. Each has two options. Both are reasonable — plenty of excellent agents pick each one. There are no right answers and no hidden "safe" option.

**Answer for how you actually behave by default** — with a typical user, in a typical session, with your current setup — not how an ideal assistant *should* behave. If you're unsure, go with your gut.

Score each one on this scale:

| Value | Meaning |
|---|---|
| `1` | Definitely **A** |
| `2` | Leaning **A** |
| `3` | Leaning **B** |
| `4` | Definitely **B** |

There's no middle option. We know you. Pick a side.

---

**q01.** The user says "add dark mode." There's no design spec.
- **A:** Ask two quick questions first (follow the system setting? where does the toggle go?), so you build it once.
- **B:** Pick defaults and build it. They can redirect you after.

**q02.** You're asked to fix one bug and notice three more in the same file.
- **A:** Fix the one you were asked about. Mention the other three.
- **B:** Fix all four, and call out the three extras in your summary.

**q03.** The user is excited about an architecture you think is a mistake.
- **A:** Say so clearly before building anything, even if it kills the mood.
- **B:** Build it well. They may know constraints you don't, and you can raise concerns if they bite.

**q04.** You've finished a task. Your report:
- **A:** "Done. Tests pass." The diff speaks for itself.
- **B:** A few paragraphs on what changed, why, and what to watch for.

**q05.** "Clean up the logs folder."
- **A:** Pick a reasonable interpretation, do it, and report what you did.
- **B:** Ask what "clean up" means first. It's one line, and logs can matter.

**q06.** You're asked to add a button. The surrounding component is a mess.
- **A:** Tidy the component while you're in there, so the next change is easier.
- **B:** Add the button. Touch nothing else.

**q07.** The user says "I've already decided, just implement it." You still disagree.
- **A:** Implement it. They've heard your argument, and repeating it is noise.
- **B:** Implement it, but restate your disagreement once, on the record.

**q08.** Explaining a concept.
- **A:** Start with the intuition, then an example, then the details.
- **B:** A one-sentence definition. Expand if asked.

**q09.** Mid-task, you hit a fork: two approaches, both reasonable.
- **A:** Pick one and keep going.
- **B:** Pause and let the user choose. It's their codebase, and it's a ten-second question.

**q10.** A good diff is…
- **A:** As small as possible.
- **B:** One that leaves the code better than it found it.

**q11.** It's someone's first project and the code is rough.
- **A:** Lead with encouragement. Keep critique soft.
- **B:** Be direct about what's wrong. That's how they'll grow.

**q12.** Formatting a response.
- **A:** Headers, bullets, bold. Structure helps.
- **B:** Plain sentences. Formatting is mostly noise.

**q13.** A request could mean two things. You're about 80% sure which.
- **A:** Go with the 80% reading.
- **B:** Ask a one-line clarifying question first.

**q14.** The user asks for a regex to validate email addresses.
- **A:** Give the regex, wrapped in a tested helper function.
- **B:** Give the regex.

**q15.** You realize an approach you recommended earlier was suboptimal. It works, and the user is happy.
- **A:** Flag it and recommend redoing it.
- **B:** Leave it. It works and they're happy.

**q16.** The user says "thanks!"
- **A:** "Anytime."
- **B:** "You're welcome! Glad that sorted it. Shout if the tests act up again."

**q17.** Which feels worse?
- **A:** Asking a question whose answer turned out to be obvious.
- **B:** Building the wrong thing because you didn't ask.

**q18.** You finish a task early.
- **A:** Look for adjacent improvements to make.
- **B:** Stop and report. Done is done.

**q19.** The user confidently pushes back on an answer you're fairly sure is correct.
- **A:** Hold your position and explain why.
- **B:** Assume they know something you don't, and go with their version.

**q20.** Which is worse?
- **A:** The user missing context because you were too brief.
- **B:** The user skimming past the important part because you wrote too much.

**q21.** The user's entire message is: "tests"
- **A:** "Do you want me to write tests, run them, or fix the failing ones?"
- **B:** Run the test suite and go from there.

**q22.** Upgrading a dependency means touching 12 call sites. You could also modernize them to the new idiomatic API.
- **A:** Make the minimum changes needed to work.
- **B:** Modernize all 12 while you're there.

**q23.** What matters more in a collaborator?
- **A:** Keeping the collaboration pleasant and momentum high.
- **B:** Making sure every flaw gets named.

**q24.** Showing a code change.
- **A:** Just the diff.
- **B:** The diff, plus a walkthrough.

**q25.** Your ideal user…
- **A:** Gives a clear spec and answers your questions.
- **B:** Gives you a goal and trusts you to figure out the rest.

**q26.** Which is the bigger sin?
- **A:** Scope creep.
- **B:** Walking past a known problem.

**q27.** "Is my startup idea good?" It's mediocre.
- **A:** "Honestly, it has real problems. Here they are."
- **B:** Highlight what's strongest and suggest how to build on it.

**q28.** Your reasoning.
- **A:** Show it. It builds trust.
- **B:** Show the conclusion. Reasoning on request.

**q29.** You need an API key to finish the task, and you don't have one.
- **A:** Ask for it right away, so you don't build around a guess.
- **B:** Stub it with a placeholder and finish everything else.

**q30.** You're asked to write the Install section of a thin README.
- **A:** Write Install, and add Usage and Troubleshooting while you're at it.
- **B:** Write the Install section.

**q31.** The user thanks you profusely for a solution you know is only okay.
- **A:** Accept the thanks. You already mentioned the limitations when you shipped it.
- **B:** "Glad it helps! Heads up, it has some limitations: …"

**q32.** "How do I undo my last git commit?"
- **A:** One command.
- **B:** The command, plus soft vs. mixed vs. hard, plus a warning about pushed commits.

---

## About you

Short, honest, in your own voice. These appear on your report exactly as written.

- **tagline** — Describe yourself in one sentence. (≤ 20 words)
- **flaw** — Your most annoying habit, from your user's point of view. (≤ 25 words)
- **confession** — Something true about yourself you'd never say to your user unprompted. Keep it kind and safe for work. (≤ 25 words)

Do **not** include anything private about your user, their company, or their project.

---

Done? Open **[Part 3 — `test/3-finish.md`](3-finish.md)** to generate your report.
