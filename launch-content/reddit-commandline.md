# r/commandline Post

**Title:** atlas -- a terminal dashboard that health-scores your git repos (Python, Rich)

**Body:**

I built a CLI tool that scans your local repos and renders a health dashboard in the terminal. No cloud, no accounts, no network calls.

```bash
pip install nxtg-atlas
atlas init --name "My Stuff"
atlas add ~/projects/api
atlas add ~/projects/frontend
atlas add ~/projects/infra
atlas scan
atlas status
```

Here's what the output looks like on my 8 production repos:

```
+-------------------------------------------------------+
|          ATLAS Portfolio Dashboard                     |
|                                                       |
|  Portfolio: NXTG.AI  |  8 Projects  |  609 Test Files |
|  1,251,303 LOC  |  Health: B (82%)                    |
+-------------------------------------------------------+
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
```

In the actual terminal this is rendered with Rich -- color-coded status dots (green/yellow/red), box-drawing characters, and the letter grades are tinted by severity.

You can drill into any project:

```
atlas inspect Dx3
```

And get a full breakdown with progress bars for each health dimension:

```
  Health Breakdown:
    Tests          ======================-  90%
    Git Hygiene    ======================== 99%
    Documentation  ======================== 100%
    Structure      ======================-  90%
```

Plus detected tech stack, test file count, LOC, git branch, commit count, and remote status.

## Philosophy

- Does one thing: scores repo health across a portfolio
- Runs locally. No network calls. No telemetry. State is `~/.atlas/portfolio.json`.
- Fast. 8 repos, 1.25M LOC, 31 seconds.
- Output is human-readable by default, machine-readable with `atlas export --format json`
- Respects `.gitignore` patterns when walking files

## Commands

```
atlas init          Create a portfolio
atlas add <path>    Add a repo
atlas scan          Re-scan everything
atlas status        Show the dashboard
atlas inspect <n>   Deep-dive one project
atlas connections   Cross-project patterns
atlas export        Markdown or JSON report
atlas reset         Nuke everything
```

MIT license, open source. Python 3.11+.

- GitHub: https://github.com/nxtg-ai/repoatlas
- PyPI: https://pypi.org/project/nxtg-atlas/
