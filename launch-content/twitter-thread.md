# nxtg-atlas Launch Thread — Twitter/X

---

**Tweet 1 (Hook)**

I manage 14 repos. Every AI coding tool works inside ONE repo. Nobody sees the full picture.

So I built a CLI that scans all of them in 31 seconds and tells me what's broken.

---

**Tweet 2 (Problem — version drift)**

The silent killer in multi-repo setups: version drift.

Three of my repos used React 18. Two were still on 17. One had a transitive dep pinned to 16.

Nobody noticed for months. No tool flagged it. Every repo looked fine in isolation.

---

**Tweet 3 (Problem — test gaps)**

Worse: 3 of my 8 production repos had zero tests.

Not "low coverage." Zero. No test runner. No CI check. Nothing.

I only found out because I went looking. That's the problem — nobody goes looking across repos.

---

**Tweet 4 (What I built — intro)**

So I built nxtg-atlas.

It's a Python CLI. You point it at a directory of repos. It scans every one — code, tests, dependencies, structure — and gives you a health grade (A through F) across 4 dimensions.

No config. No setup. Just run it.

---

**Tweet 5 (What I built — how it works)**

Four health dimensions, each scored independently:

- Code Quality (size, structure, complexity)
- Test Coverage (test files, frameworks, ratio)
- Dependency Health (freshness, mismatches, count)
- Project Hygiene (docs, CI, linting, README)

Combined into a single A-F grade per repo. One dashboard for everything.

---

**Tweet 6 (Screenshot prompt)**

[SCREENSHOT: Run `atlas scan ~/projects --format table` in terminal. Show the output table with repo names, individual dimension scores, and overall grades. The contrast between A-grade and D-grade repos in the same portfolio tells the whole story.]

---

**Tweet 7 (What it found)**

First real scan across 8 production repos:

- 8 dependency version mismatches across shared libraries
- 3 repos with zero test files
- 5 shared dependencies with diverging versions
- 2 repos missing CI entirely

All invisible when you look at repos one at a time.

---

**Tweet 8 (The numbers)**

The scan:
- 1,251,303 lines of code
- 8 repos
- 609 test files detected
- 31 seconds total
- Zero network calls
- Fully local — no telemetry, no cloud, no account

Your code never leaves your machine.

---

**Tweet 9 (How to try it)**

Try it in 60 seconds:

```
pip install nxtg-atlas
atlas scan ~/projects --format table
atlas report ~/projects -o report.html
```

Free for up to 3 projects. $49 one-time for unlimited. No subscription.

MIT licensed. Works on Mac, Linux, WSL.

---

**Tweet 10 (CTA)**

If you manage more than one repo and nobody on your team can answer "which repos have zero tests?" — this is for you.

GitHub: github.com/nxtg-ai/repoatlas
Install: pip install nxtg-atlas

Built by @nxtgai. Feedback welcome — this is week one.
