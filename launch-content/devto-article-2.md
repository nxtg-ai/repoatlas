---
title: "I Scanned 8 Repos in 31 Seconds — Here's What I Found"
published: false
description: "I pointed a CLI tool at 8 production repos — 1.25M lines of code — and got a portfolio health dashboard in 31 seconds. The results were humbling."
tags: python, cli, devops, opensource
cover_image:
canonical_url:
---

I manage 8 production repos. Last week I pointed a CLI tool at all of them.

31 seconds later I was staring at a dashboard that told me things I didn't want to hear.

The tool is called [nxtg-atlas](https://github.com/nxtg-ai/repoatlas). I built it because I was tired of not knowing the health of my own portfolio. Here's what it showed me.

## The Dashboard

```
╭───────────────────────  ATLAS Portfolio Dashboard  ─────────────────────────╮
│                                                                             │
│  Portfolio: NXTG.AI  |  8 Projects  |  609 Test Files  |  1,251,303 LOC    │
│  Health: B (82%)  |  Scanned: 2026-03-04T01:15                             │
│                                                                             │
╰─────────────────────────────────────────────────────────────────────────────╯
┌────┬────────────────────┬──────────┬────────┬──────────┬─────────────────────┐
│    │ Project            │ Health   │  Tests │      LOC │ Tech Stack          │
├────┼────────────────────┼──────────┼────────┼──────────┼─────────────────────┤
│ ●  │ Dx3                │  A 94%   │    179 │  164,806 │ Python · TypeScript │
│ ●  │ content-engine     │  B+ 88%  │     23 │   12,552 │ Python              │
│ ●  │ Podcast-Pipeline   │  B+ 88%  │     49 │   33,680 │ Python · FastAPI    │
│ ●  │ nxtg.ai            │  B+ 87%  │     36 │   49,938 │ TypeScript · Next.js│
│ ●  │ Faultline          │  B+ 86%  │     29 │   15,527 │ TypeScript · React  │
│ ●  │ voice-jib-jab      │  B+ 86%  │     58 │   45,311 │ TypeScript · Python │
│ ●  │ SynApps            │  C 67%   │    114 │  793,406 │ Python · TypeScript │
│ ●  │ NXTG-Forge         │  D 59%   │    121 │  136,083 │ TypeScript · Rust   │
└────┴────────────────────┴──────────┴────────┴──────────┴─────────────────────┘
```

That's real output. Not a mockup. 1,251,303 lines of code across 8 repos, 609 test files detected, portfolio health grade of B.

My immediate reaction: "A D? NXTG-Forge is a D?"

Yes. And it was right.

## Discovery #1: My Biggest Project Was My Weakest

NXTG-Forge is 136,000 lines of code spread across three connected repos (UI, orchestrator, plugin). It's the most complex thing in the portfolio. And it scored 59% — a D.

Atlas scores health across four dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| **Tests** | 35% | Test file count relative to source files |
| **Git Hygiene** | 20% | Commits, remote configured, clean working tree |
| **Documentation** | 20% | README, changelog, docs directory, CLAUDE.md |
| **Structure** | 25% | CI/CD, .gitignore, package config, linting |

Forge had the test files (121 of them), but its documentation was sparse, its structure score was low — no consistent linting config across the three sub-repos, no changelog — and git hygiene flagged uncommitted changes. The weight system penalized it correctly. Complex project, inconsistent foundation.

Meanwhile, Dx3 — a younger project I'd been more disciplined about — scored 94%. Fewer lines of code, but proper CI, clean git history, thorough docs.

The health score doesn't just tell you "this is good" or "this is bad." It tells you *where* the weakness is. When I ran `atlas inspect NXTG-Forge`, the breakdown showed exactly which dimensions were dragging the grade down.

```
  Health Breakdown:
    Tests          █████████████░░  90%
    Git Hygiene    ██████████████░  99%
    Documentation  ███████████████  100%
    Structure      █████████████░░  90%
```

(That's from a healthy project. Forge's bars looked much more uneven.)

## Discovery #2: Version Drift I Didn't Know About

This one stung. Atlas has a cross-project intelligence feature that compares dependencies across repos. Here's what it found:

```
╭───────────────── Cross-Project Intelligence ──────────────────╮
│                                                                │
│  Shared Dependencies                                           │
│    ℹ  fastapi used across 4 projects                           │
│    ℹ  react used across 3 projects                             │
│                                                                │
│  Version Mismatches                                            │
│    ⚠  react: ^18.2.0 (app-a), ^19.2.1 (app-b)                 │
│    ⚠  fastapi: >=0.100.0 (api-v1), >=0.115.9 (api-v2)         │
│                                                                │
│  Health Gaps                                                   │
│    ✖  3 projects have zero tests                               │
│    ⚠  1 project has 50+ uncommitted changes                    │
│                                                                │
╰────────────────────────────────────────────────────────────────╯
```

React 18 in one project, React 19 in another. FastAPI 0.100 in one, 0.115 in another. These aren't theoretical risks — they're real mismatches that will cause bugs when you share code or deploy to the same infrastructure.

I had no idea. Each repo's CI was green. Each project worked in isolation. But the portfolio as a whole had invisible fault lines running through it.

## Discovery #3: The 793K LOC Outlier

SynApps — 793,406 lines of code — was my biggest repo by far. It scored a C (67%). That's a project with 114 test files, which sounds decent until you realize it's proportionally low for a codebase that large.

Atlas measures tests relative to source files, not in absolute numbers. A project with 10 source files and 8 test files scores higher than a project with 1,000 source files and 100 test files. That's intentional. The question isn't "do you have tests?" — it's "are you testing what you're building?"

SynApps had accumulated a lot of code but hadn't kept test coverage proportional. The health score caught that instantly.

## Discovery #4: The Tech Stack Map

Something I didn't expect to be useful but turned out to be: the tech stack detection. Atlas reads your config files and identifies languages, frameworks, databases, and tools.

Seeing it all in one table — Python in 5 projects, TypeScript in 5, Rust in 1, FastAPI in 4, React in 3, Next.js in 1 — gave me a portfolio-level view I'd never had. I could immediately see which technologies are core (Python, TypeScript) and which are one-offs (Rust in Forge).

It also detected databases (PostgreSQL, Redis, SQLite), CI configurations (GitHub Actions across all 8), and even AI SDKs (Anthropic, OpenAI). No configuration needed. It just reads your `pyproject.toml`, `package.json`, and `Cargo.toml`.

## How It Works

Atlas is deliberately simple. No cloud. No accounts. No network calls. No telemetry.

```bash
pip install nxtg-atlas

atlas init --name "My Portfolio"
atlas add ~/projects/api
atlas add ~/projects/frontend
atlas scan
atlas status
```

It walks your project directories, parses config files, inspects git history, counts source and test files (skipping `node_modules`, `.venv`, `target`, etc.), and scores everything with a weighted formula. State lives in `~/.atlas/portfolio.json` — a plain JSON file you can inspect or version control.

Built with Python 3.11+, Typer for the CLI, and Rich for the terminal output. 30 tests. CI running on Python 3.11, 3.12, and 3.13. MIT licensed.

The scan across my 8 repos — 1.25 million lines of code — took 31 seconds on a standard dev machine. No optimization tricks. File walking and config parsing is just fast when you're not sending anything over the network.

## What I Did About It

After staring at the dashboard for a few minutes, I made a list:

1. **Forge (D)** — added missing changelogs, unified linting config across the three sub-repos, committed dirty changes
2. **SynApps (C)** — queued a test coverage sprint, prioritized the most critical paths
3. **Version drift** — standardized React 19 and FastAPI 0.115+ across all projects that use them
4. **Documentation gaps** — added READMEs to the two repos that were missing them

None of these were emergencies. All of them were preventing future emergencies. The dashboard gave me the prioritization I needed: fix the D first, then the C, then address cross-cutting issues.

## Try It Yourself

```bash
pip install nxtg-atlas
```

Everything is free. No tiers, no limits, no feature gates. Unlimited projects, cross-project intelligence, batch-add, markdown/JSON export — all included.

If atlas saves you time, consider [supporting development](https://polar.sh/nxtg-ai/repoatlas).

**GitHub**: [github.com/nxtg-ai/repoatlas](https://github.com/nxtg-ai/repoatlas)

The worst blind spots are the ones you can't see from inside a single repo. Start scanning across them.
