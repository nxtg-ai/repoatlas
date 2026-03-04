# Show HN: Atlas -- Portfolio health dashboard for multi-repo teams (Python CLI)

I manage 8+ production repos across Python, TypeScript, and Rust. Every dev tool I use -- Cursor, Copilot, Claude Code -- is great inside a single repo. But none of them answer the cross-cutting questions:

- Which repos have zero tests?
- Are my React versions consistent across 3 frontends?
- Which project hasn't been committed to in weeks?
- Where am I duplicating FastAPI patterns instead of sharing a library?

I got tired of manually checking, so I built Atlas. It's a Python CLI that scans your repos locally and gives you a portfolio-level health dashboard.

## What it does

Point it at your projects, run `atlas scan`, and you get this:

```
pip install nxtg-atlas

atlas init --name "My Portfolio"
atlas add ~/projects/api
atlas add ~/projects/frontend
atlas scan
atlas status
```

Real output from my 8 production repos:

```
+---------+--------------------+----------+--------+----------+---------------------+
|         | Project            | Health   |  Tests |      LOC | Tech Stack          |
+---------+--------------------+----------+--------+----------+---------------------+
| (green) | Dx3                |  A 94%   |    179 |  164,806 | Python . TypeScript |
| (green) | content-engine     |  B+ 88%  |     23 |   12,552 | Python              |
| (green) | Podcast-Pipeline   |  B+ 88%  |     49 |   33,680 | Python . FastAPI    |
| (green) | nxtg.ai            |  B+ 87%  |     36 |   49,938 | TypeScript . Next.js|
| (green) | Faultline          |  B+ 86%  |     29 |   15,527 | TypeScript . React  |
| (green) | voice-jib-jab      |  B+ 86%  |     58 |   45,311 | TypeScript . Python |
| (yellow)| SynApps            |  C 67%   |    114 |  793,406 | Python . TypeScript |
| (red)   | NXTG-Forge         |  D 59%   |    121 |  136,083 | TypeScript . Rust   |
+---------+--------------------+----------+--------+----------+---------------------+

8 Projects  |  609 Test Files  |  1,251,303 LOC  |  Scanned in 31 seconds
```

That's not a mockup. That's the actual output from scanning our production portfolio. The C and D grades were embarrassing -- but that's the point. You can't fix what you can't see.

## How health scoring works

Each project gets an A-F grade based on 4 weighted dimensions:

- **Tests (35%)** -- test file count relative to source files
- **Structure (25%)** -- CI/CD, .gitignore, package config, linting, source organization
- **Git Hygiene (20%)** -- commit history, remote status, clean working tree
- **Documentation (20%)** -- README, CHANGELOG, docs/, etc.

## Cross-project intelligence

This is where it gets interesting. Atlas compares deps and versions across all your repos:

- Shared dependencies (fastapi used in 4 projects, react in 3)
- Version mismatches (react ^18.2.0 in one app, ^19.2.1 in another)
- Health gaps (3 projects with zero tests, 1 with 50+ uncommitted changes)

These are the things that bite you six months from now.

## What it is NOT

- Not a cloud service. Zero network calls, no telemetry, no accounts.
- Not a linter or code quality tool. It doesn't read your source code line by line.
- Not a replacement for SonarQube / CodeClimate. Those go deep on one repo. Atlas goes wide across many.

## Details

- Python 3.11+, built with Typer + Rich
- State is a single JSON file at `~/.atlas/portfolio.json`
- Detects 10+ languages, 15+ frameworks, 5+ databases
- MIT license, open source
- Free tier: 3 projects, full health scoring. Pro ($49 one-time): unlimited projects + cross-project intelligence.

GitHub: https://github.com/nxtg-ai/repoatlas
PyPI: https://pypi.org/project/nxtg-atlas/

Happy to answer questions about the scoring algorithm, the detection heuristics, or how we're using it internally.
