# r/devops Post

**Title:** We had 3 repos running different React versions and 2 with zero tests -- built a CLI to catch this stuff early

**Body:**

I run a portfolio of 8 production repos. Different languages (Python, TypeScript, Rust), different teams, different cadences. Last month I discovered:

- Two repos had **zero test files**
- Three frontends were running **different React major versions** (18 vs 19)
- One repo had **50+ uncommitted changes** sitting in the working tree
- A FastAPI service was pinned to a version two minors behind the others

None of this showed up in any dashboard. CI was green. PRs were merging. The drift was invisible until it wasn't.

## What I built

**nxtg-atlas** -- a Python CLI that scans local repos and gives you a portfolio-level health report.

```bash
pip install nxtg-atlas
atlas init --name "Our Platform"
atlas add ~/repos/api-gateway
atlas add ~/repos/frontend-v2
atlas add ~/repos/ml-service
atlas add ~/repos/infra
atlas scan
atlas status
```

31 seconds later, you get a table of every repo with:
- **Health grade (A-F)** based on 4 dimensions: test coverage, git hygiene, documentation, project structure
- **Test file count** and LOC
- **Detected tech stack** (languages, frameworks, databases)
- Color-coded status (green/yellow/red)

Then run `atlas connections` for the cross-project view:

- **Shared dependencies** -- fastapi used in 4 services, react in 3 frontends
- **Version mismatches** -- the ones that cause "works on my machine" in staging
- **Health gaps** -- repos below a threshold, repos with no CI, repos going stale

## What this is NOT

This is not SonarQube. It's not CodeClimate. Those tools go deep on code quality inside a single repo. Atlas goes wide across many repos.

Think of it as a lightweight governance layer. The stuff you'd check manually before a quarterly review -- except automated and repeatable.

## How it works operationally

- **Zero network calls.** No cloud, no accounts, no telemetry. Scans your local filesystem and git history.
- **State is a JSON file** at `~/.atlas/portfolio.json`. Portable, inspectable, version-controllable.
- **CI-friendly.** `atlas export --format json` gives you machine-readable output. You could gate deployments on health scores if you wanted to.
- **Fast.** 8 repos with 1.25M LOC scanned in 31 seconds on a standard dev machine.

## Health scoring

4 dimensions, weighted:

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Tests | 35% | Test files relative to source files |
| Structure | 25% | CI/CD config, .gitignore, package config, linting, source organization |
| Git Hygiene | 20% | Commit count, remote status, clean working tree |
| Documentation | 20% | README, CHANGELOG, docs/, etc. |

Each dimension scores 0-100%, weighted into a composite score, mapped to A-F. The weights are opinionated -- tests matter most in my world. Your mileage may vary.

## The real value

The dashboard is nice. But the version mismatch detection is where it pays for itself. Catching `react ^18.2.0` in one app and `^19.2.1` in another before it hits a shared component library saves hours of debugging.

Same for the "zero tests" flag. It's easy to ship a quick prototype repo and forget to add tests. Six months later it's in production and nobody remembers it has no coverage.

## Details

- Python 3.11+, MIT license, 100% open source — no tiers, no limits, no feature gates
- Built with Typer + Rich + Pydantic
- Everything works: unlimited projects, cross-project intelligence, export
- GitHub: https://github.com/nxtg-ai/repoatlas
- PyPI: https://pypi.org/project/nxtg-atlas/
- If atlas saves you time, consider [supporting development](https://polar.sh/nxtg-ai/repoatlas)

If you manage more than a handful of repos and want a quick sanity check across all of them, give it a try. Feedback welcome -- especially on the health scoring weights.
