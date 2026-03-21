# Reddit Launch Posts

## r/Python

**Title**: I built a CLI that scans all your repos and gives you a portfolio health dashboard

**Body**:

I manage 10+ repos and got tired of not having a cross-project view. Every tool works inside one repo, but nobody tells you which repos have zero tests, whether your dependency versions are consistent, or where you're duplicating patterns.

So I built **Atlas** -- a CLI that scans your local directories and gives you:

- **Health scoring** across 4 dimensions (tests, git hygiene, docs, structure) with A-F grades
- **Tech stack detection** for Python, TypeScript, Rust, Go, Java + frameworks (FastAPI, React, Django, etc.)
- **Cross-project intelligence** -- shared deps, version mismatches, health gaps

```
pip install nxtg-atlas
atlas init && atlas batch-add ~/projects && atlas scan && atlas status
```

30 seconds, 8 repos, 1.25M LOC. No network calls, no telemetry, no cloud. Everything runs locally.

221 tests. MIT license. 100% free.

GitHub: https://github.com/nxtg-ai/repoatlas
PyPI: https://pypi.org/project/nxtg-atlas/

Would love to hear what signals you'd want detected across a portfolio of repos.

---

## r/commandline

**Title**: Atlas -- terminal dashboard for multi-repo portfolio health (Python CLI)

**Body**:

Built a CLI tool that scans multiple git repos and renders a Rich-based dashboard with health grades, tech stack detection, and cross-project pattern analysis.

```
pip install nxtg-atlas
atlas batch-add ~/projects
atlas scan
atlas status
```

Features: A-F health grades across 4 dimensions, tech stack detection (10+ languages, 15+ frameworks), cross-project intelligence (shared deps, version mismatches), markdown/JSON export.

8 repos, 1.25M LOC scanned in 31 seconds. Zero network calls. State in a single JSON file.

GitHub: https://github.com/nxtg-ai/repoatlas

---

## Posting notes
- r/Python: post weekday mornings ET, flair as "I Made This"
- r/commandline: post any weekday
- Respond to comments within first 2 hours
