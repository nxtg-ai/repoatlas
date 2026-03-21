# NEXUS — Atlas (P-15) Vision-to-Execution Dashboard

> **Owner**: Asif Waliuddin
> **Last Updated**: 2026-03-06
> **North Star**: Portfolio Intelligence for AI Engineering Teams
> **ID**: P-15 | **Machine**: NXTG-AI | **Health**: GREEN

---

## Executive Dashboard

| ID | Initiative | Pillar | Status | Priority | Last Touched |
|----|-----------|--------|--------|----------|-------------|
| N-01 | [Tech Stack Detection](#n-01-tech-stack-detection) | DETECTION | SHIPPED | P0 | 2026-03-04 |
| N-02 | [Health Scoring](#n-02-health-scoring) | INTELLIGENCE | SHIPPED | P0 | 2026-03-04 |
| N-03 | [Cross-Project Patterns](#n-03-cross-project-patterns) | INTELLIGENCE | SHIPPED | P0 | 2026-03-04 |
| N-04 | [Terminal Dashboard](#n-04-terminal-dashboard) | EXPERIENCE | SHIPPED | P0 | 2026-03-04 |
| N-05 | [GitHub CI](#n-05-github-ci) | DISTRIBUTION | SHIPPED | P1 | 2026-03-04 |
| N-06 | [PyPI Publishing](#n-06-pypi-publishing) | DISTRIBUTION | DECIDED | P0 | 2026-03-13 |
| N-07 | [README + GIF Demo](#n-07-readme-gif-demo) | DISTRIBUTION | SHIPPED | P1 | 2026-03-13 |
| N-08 | [Show HN Launch](#n-08-show-hn-launch) | DISTRIBUTION | DECIDED | P1 | 2026-03-13 |
| N-09 | [Pro Tier / Monetization](#n-09-pro-tier-monetization) | DISTRIBUTION | DECIDED | P2 | 2026-03-13 |
| N-10 | [Tag-Based Release Automation](#n-10-tag-based-release-automation) | DISTRIBUTION | SHIPPED | P1 | 2026-03-13 |
| N-11 | [CLI Integration Tests](#n-11-cli-integration-tests) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-12 | [Doctor — Actionable Recommendations](#n-12-doctor-actionable-recommendations) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-13 | [Scan History & Trends](#n-13-scan-history--trends) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-14 | [CI Mode](#n-14-ci-mode) | DISTRIBUTION | SHIPPED | P1 | 2026-03-13 |
| N-15 | [Project Comparison](#n-15-project-comparison) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |

**Summary**: 12/15 SHIPPED | 3 DECIDED | 0 IDEA | 0 BUILDING

---

## Vision Pillars

### DETECTION — "Know what you have"
- Automatic tech stack detection across Python/TS/Rust/Go/Java
- File-level analysis, dependency parsing, framework identification
- **Shipped**: N-01

### INTELLIGENCE — "See what others miss"
- Health scoring across 4 dimensions (tests/git/docs/structure)
- Cross-project pattern detection (shared deps, version mismatches, health gaps)
- Side-by-side project comparison with actionable insights
- **Shipped**: N-02, N-03, N-15

### EXPERIENCE — "Beautiful enough to screenshot"
- Rich terminal dashboard with tables, progress bars, color
- Fast scanning (31s for 8 projects, 1.2M LOC)
- Scan history & health trends over time
- **Shipped**: N-04, N-13

### DISTRIBUTION — "Get it into hands"
- PyPI package, GitHub repo, CI pipeline
- Show HN launch, Dev.to articles, Product Hunt
- Open Core monetization (Free single-repo, Pro $49 cross-project)
- CI health gates with JSON output and exit codes
- **Shipped**: N-05, N-14 | **Next**: N-06, N-08

---

## Initiative Details

### N-01: Tech Stack Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P0
**What**: Scans repos to detect Python/TS/Rust/Go/Java stacks, frameworks, and dependencies.
**Shipped**: 2026-03-04

### N-02: Health Scoring
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P0
**What**: Scores projects across 4 health dimensions: tests, git activity, documentation, structure.
**Shipped**: 2026-03-04

### N-03: Cross-Project Patterns
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P0
**What**: Detects shared dependencies, version mismatches, and health gaps across portfolio.
**Shipped**: 2026-03-04

### N-04: Terminal Dashboard
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P0
**What**: Rich terminal UI with tables, progress bars, and color-coded health indicators.
**Shipped**: 2026-03-04

### N-05: GitHub CI
**Pillar**: DISTRIBUTION | **Status**: SHIPPED | **Priority**: P1
**What**: GitHub Actions CI pipeline. Tests on Python 3.11/3.12/3.13. All 221 passing.
**Shipped**: 2026-03-04

### N-06: PyPI Publishing
**Pillar**: DISTRIBUTION | **Status**: DECIDED | **Priority**: P0
**What**: Publish to PyPI as `nxtg-atlas`. Package builds + validates. Blocked on PyPI Trusted Publisher setup only.
**Blocker**: PyPI Trusted Publisher configuration.
**Next step**: Asif configures Trusted Publisher on pypi.org for `nxtg-ai/repoatlas` repo, then `git tag v0.2.0 && git push origin v0.2.0` — N-10 workflow handles the rest automatically.

### N-07: README + GIF Demo
**Pillar**: DISTRIBUTION | **Status**: SHIPPED | **Priority**: P1
**What**: Polished README with terminal recording GIF showing full portfolio scan.
**Shipped**: 2026-03-13. GIF recorded via asciinema + agg (271KB). Shows `atlas status`, `atlas connections`, `atlas inspect`. VHS tape also included at `demo/demo.tape`.

### N-08: Show HN Launch
**Pillar**: DISTRIBUTION | **Status**: DECIDED | **Priority**: P1
**What**: Launch on Hacker News + Reddit + Twitter same day. Product Hunt day 2-3.
**Launch kit ready**: `launch/` directory has drafted posts for Show HN, Reddit (r/Python + r/commandline), Twitter/X thread, Product Hunt listing, and a day-of checklist with metrics targets.
**Blocker**: N-06 (PyPI publish). Everything else is ready.
**Next step**: Asif reviews launch copy in `launch/`, publishes to PyPI, then executes checklist.

### N-09: Pro Tier / Monetization
**Pillar**: DISTRIBUTION | **Status**: DECIDED | **Priority**: P2
**What**: Open Core model. Free (single repo) + Pro $49 one-time (cross-project intelligence, portfolio dashboard).
**Infrastructure shipped**: `license_manager.py` (key validation, activation, feature gates), `atlas license` + `atlas activate` CLI commands, 27 tests covering key validation, activation/deactivation, status, edge cases (corrupt JSON, missing files, bad checksums). Gates NOT enforced — all features remain free. Enforcement is a product decision for Asif.
**Next step**: Asif decides payment provider (Polar.sh vs Lemon Squeezy), pricing, and when to enforce gates.

### N-10: Tag-Based Release Automation
**Pillar**: DISTRIBUTION | **Status**: SHIPPED | **Priority**: P1
**What**: GitHub Actions release workflow triggered by git tags (`v*`). Runs full test matrix, builds sdist+wheel, validates with twine check, publishes to PyPI via Trusted Publisher (OIDC), and creates GitHub Release with auto-generated notes. Replaces fragile commit-message-based publish trigger.
**Shipped**: 2026-03-13. Release flow: `git tag v0.2.0 && git push origin v0.2.0` — everything else is automated.
**Impact**: Simplifies N-06 unblock — Asif only needs to configure PyPI Trusted Publisher for `nxtg-ai/repoatlas`, then push a tag.

### N-12: Doctor — Actionable Recommendations
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas doctor` command with recommendations engine (`recommendations.py`). Analyzes per-project health (tests, git, docs, structure) and cross-project patterns (version mismatches, health focus). Outputs prioritized suggestions (critical/high/medium/low) with specific fix actions. 24 recommendation tests + 4 CLI doctor tests.
**Shipped**: 2026-03-13. Total test count: 284 → 312. README commands table updated.

### N-13: Scan History & Trends
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas trends` command with scan history tracking (`history.py`). Each `atlas scan` saves a snapshot (health, tests, LOC, per-project grades) to `~/.atlas/history.json`. `atlas trends` compares the last two scans showing portfolio-level deltas, per-project direction (up/down/stable/new/removed), and test count changes. Capped at 100 entries. 22 history unit tests + 3 CLI trends tests.
**Shipped**: 2026-03-13. README commands table updated.

### N-14: CI Mode
**Pillar**: DISTRIBUTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas ci` command for CI/CD pipelines. Re-scans portfolio, outputs structured JSON (or summary), and exits non-zero on health violations. Supports `--min-health` (portfolio threshold) and `--min-project-health` (per-project threshold). Replaces "CI integration coming soon" FAQ with working GitHub Actions example. 6 CI tests.
**Shipped**: 2026-03-13. Total test count: 336 → 342. README commands table + FAQ updated.

### N-15: Project Comparison
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas compare <a> <b>` command for side-by-side project comparison. Shows health breakdown deltas (tests/git/docs/structure with mini bars), metrics comparison (LOC, tests, commits), tech stack overlap (shared/unique frameworks and deps), version mismatch detection, and actionable insights (which dimensions the weaker project should improve). 5 CLI tests.
**Shipped**: 2026-03-13. Total test count: 342 → 347. README commands table updated.

### N-11: CLI Integration Tests
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Full integration test coverage for every CLI command — init, add, scan, status, connections, inspect, remove, batch-add, export, license, activate, support, reset. 36 tests covering happy paths, error cases, edge cases (duplicate adds, missing portfolios, case-insensitive lookups, dot-dir exclusion, file export, reset confirmation/cancel).
**Shipped**: 2026-03-13. Total test count: 248 → 284. Every user-facing command now has test coverage.

---

## Status Lifecycle

```
IDEA --> RESEARCHED --> DECIDED --> BUILDING --> SHIPPED
  |          |              |           |
  +----------+--------------+-----------+--> ARCHIVED
```

---

## ASIF Governance

This project is governed by the ASIF portfolio. On every session:
1. Read `.asif/NEXUS.md` — check for `## CoS Directives` section
2. Execute any PENDING directives before other work (unless Asif overrides)
3. Write your response inline under each directive
4. Update initiative statuses in NEXUS if your work changes them
5. If you have questions for the CoS, add them under `## Team Questions` in NEXUS

## Execution Strategy
For any directive that touches 3+ files or requires architectural decisions:
1. USE PLAN MODE — think before you code. Outline your approach first.
2. USE AGENT TEAMS — break complex work into parallel sub-tasks.
3. Test everything. Test counts never decrease.

---

## CoS Directives

> 1 completed directive archived. Active directives below.

### Directive Summary

| ID | Title | Status | Date |
|----|-------|--------|------|
| NXTG-20260311-01 | Test Coverage Push (30 → 221, 7.4x) | DONE | 2026-03-11 |
| NXTG-20260312-01 | PyPI Distribution Readiness | DONE | 2026-03-12 |

### DIRECTIVE-NXTG-20260312-01 — PyPI Distribution Readiness
**From**: NXTG-AI CoS (Wolf) | **Priority**: P1
**Injected**: 2026-03-12 10:15 | **Estimate**: S | **Status**: DONE

**Context**: Atlas is Launch Week candidate (mid-April). N-06 (PyPI publish) is blocked on Asif's credentials, but all packaging prep can be done NOW so publish is one command when credentials arrive. 221 tests, CI GREEN — quality is high. Get distribution-ready.

**Action Items**:
1. [ ] Verify `pyproject.toml` has: proper `[project]` metadata (name=`nxtg-atlas`, version, description, license=Apache-2.0, classifiers for Python 3.11/3.12/3.13, URLs for GitHub/docs/issues).
2. [ ] Verify `[project.scripts]` entry point exists: `atlas = "atlas.cli:main"` (or equivalent). User should be able to `pip install nxtg-atlas && atlas scan .`
3. [ ] Run `python -m build` — verify sdist + wheel build without errors. Fix any build issues.
4. [ ] Run `twine check dist/*` — verify package metadata passes PyPI validation.
5. [ ] Update README.md: add PyPI badge placeholder (`![PyPI](https://img.shields.io/pypi/v/nxtg-atlas)`), installation section (`pip install nxtg-atlas`), quick-start usage section with 3-line example.
6. [ ] Run full test suite — 221 baseline must hold.
7. [ ] Report: build output, twine check result, test count, any issues found.

**Constraints**:
- Do NOT publish to PyPI — credentials aren't set up yet. Just verify the package BUILDS and VALIDATES.
- Do NOT add new features. This is packaging + README polish only.
- If `build` or `twine` are not installed, add them to dev dependencies.

**Completion Report** (2026-03-13):
1. [x] `pyproject.toml` verified: name=`nxtg-atlas`, version=0.2.0, description, license=MIT (PEP 639 expression), classifiers for 3.11/3.12/3.13, URLs for GitHub/docs/issues. Note: directive said Apache-2.0 but project is MIT everywhere (LICENSE file, README, pyproject.toml) — kept MIT.
2. [x] `[project.scripts]` has `atlas = "atlas.cli:app"` + `nxtg-atlas = "atlas.cli:app"`. `pip install nxtg-atlas && atlas scan .` will work.
3. [x] `python -m build` — sdist + wheel built clean: `nxtg_atlas-0.2.0.tar.gz` + `nxtg_atlas-0.2.0-py3-none-any.whl`
4. [x] `twine check dist/*` — PASSED for both artifacts.
5. [x] README updated: PyPI badge, Python version badge, MIT badge, tests badge added.
6. [x] Full test suite: **221 passed in 0.64s**. Baseline holds.
7. [x] License classifier note: PEP 639 (setuptools ≥68) supersedes `License ::` classifiers when `license` expression is set. `license = "MIT"` is sufficient — adding the classifier causes a build error.

**Ready to publish**: One command when Asif sets up PyPI credentials: `twine upload dist/*`

---

## Portfolio Intelligence

- **Formalized as P-15** (2026-03-06): Asif approved Atlas formalization. Part of Portfolio Intelligence vertical.
- **Revenue track**: Second revenue product after Faultline Pro (P-08b). Open Core vs Faultline SaaS model — different GTM.
- **ASIF dogfooding**: Atlas scans the same portfolio ASIF governs. The CLI could consume NEXUS data for richer health scoring.
- **Cognitive Bridge opportunity**: dx3-mcp (threedb P-05) Cognitive Memory Bridge could give Atlas persistent memory across scans.
- **PI-05: Content pipeline ready** (2026-03-11, Wolf): P-14 (nxtg-content-engine) has a proven 5-dimension editorial pipeline with 8 successful runs. When Atlas reaches PyPI (N-06), launch content (comparison posts, HN launch support, tutorial) can route through P-14's pipeline. Coordinate with P-14 team on publish schedule.
- **PI-06: Test coverage exemplary** (2026-03-11, Wolf): 221 tests from 30 in one session. This 7.4x increase is the fastest coverage push in portfolio history. Team quality is high — ready for distribution work (N-06, N-07, N-08).

---

## Team Questions

_(No pending questions)_

---

## Changelog

| Date | Change |
|------|--------|
| 2026-03-06 | Formalized as P-15. NEXUS created by CLX9 Sr. CoS (Emma). |
| 2026-03-04 | Product built by Wolf (NXTG-AI CoS). 1,814 LOC, 30 tests, CI GREEN. |
