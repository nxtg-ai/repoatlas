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
| N-06 | [PyPI Publishing](#n-06-pypi-publishing) | DISTRIBUTION | DECIDED | P0 | 2026-03-04 |
| N-07 | [README + GIF Demo](#n-07-readme-gif-demo) | DISTRIBUTION | IDEA | P1 | — |
| N-08 | [Show HN Launch](#n-08-show-hn-launch) | DISTRIBUTION | IDEA | P1 | — |
| N-09 | [Pro Tier / Monetization](#n-09-pro-tier-monetization) | DISTRIBUTION | IDEA | P2 | — |

**Summary**: 5/9 SHIPPED | 1 DECIDED | 3 IDEA | 0 BUILDING

---

## Vision Pillars

### DETECTION — "Know what you have"
- Automatic tech stack detection across Python/TS/Rust/Go/Java
- File-level analysis, dependency parsing, framework identification
- **Shipped**: N-01

### INTELLIGENCE — "See what others miss"
- Health scoring across 4 dimensions (tests/git/docs/structure)
- Cross-project pattern detection (shared deps, version mismatches, health gaps)
- **Shipped**: N-02, N-03

### EXPERIENCE — "Beautiful enough to screenshot"
- Rich terminal dashboard with tables, progress bars, color
- Fast scanning (31s for 8 projects, 1.2M LOC)
- **Shipped**: N-04

### DISTRIBUTION — "Get it into hands"
- PyPI package, GitHub repo, CI pipeline
- Show HN launch, Dev.to articles, Product Hunt
- Open Core monetization (Free single-repo, Pro $49 cross-project)
- **Shipped**: N-05 | **Next**: N-06, N-07, N-08

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
**What**: Publish to PyPI as `repoatlas`. Needs PyPI API token or Trusted Publisher setup.
**Blocker**: PyPI credentials. See `PUBLISH.md`.
**Next step**: Asif sets up PyPI token, then publish.

### N-07: README + GIF Demo
**Pillar**: DISTRIBUTION | **Status**: IDEA | **Priority**: P1
**What**: Polished README with terminal recording GIF showing full portfolio scan.
**Next step**: Record terminal session with asciinema or VHS, convert to GIF.

### N-08: Show HN Launch
**Pillar**: DISTRIBUTION | **Status**: IDEA | **Priority**: P1
**What**: Launch on Hacker News + Reddit + Twitter same day. Product Hunt day 2-3.
**Next step**: Depends on N-06 (PyPI) and N-07 (README).

### N-09: Pro Tier / Monetization
**Pillar**: DISTRIBUTION | **Status**: IDEA | **Priority**: P2
**What**: Open Core model. Free (single repo) + Pro $49 one-time (cross-project intelligence, portfolio dashboard).
**Next step**: Define feature gate. Polar.sh or Lemon Squeezy for payment.

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

### DIRECTIVE-NXTG-20260311-01 — Test Coverage Push (30 → 100+)
**From**: NXTG-AI CoS (Wolf) | **Priority**: P1
**Injected**: 2026-03-11 05:40 | **Estimate**: S | **Status**: DONE

**Context**: Atlas has 30 tests and 1,814 LOC — that's ~1.7 tests per 100 lines, well below portfolio standard. As a revenue-track product heading toward PyPI publishing (N-06), test quality is a gate. Every other revenue-track product (Faultline Pro: 909, Forge: 4,590) has 10x+ your count. This is the gap to close before any distribution work.

**Action Items**:
1. [x] Run `pytest --co -q` — confirm baseline count. **Baseline: 30 tests.**
2. [x] Identify the 3 modules with lowest coverage. **models.py (0), scanner.py (3), connections.py (6).**
3. [x] Add unit tests for `scanner.py` — edge cases: empty dirs, monorepos, Rust projects, git info mocking. **12 tests.**
4. [x] Add unit tests for `health.py` — all scoring formula brackets, boundary conditions, doc/structure scoring. **49 tests.**
5. [x] Add unit tests for `connections.py` (cross-project analysis) — shared deps, frameworks, version mismatches, health gaps, databases. **38 tests.**
6. [x] Target: 100+ tests minimum. **Result: 221 tests (7.4x increase).**
7. [x] Run full suite. All green. **221 passed in 0.23s.**

**Also added**: `test_models.py` (37 tests) — TechStack, GitInfo, HealthScore, Project roundtrip, Portfolio save/load. `test_detector.py` expanded from 12 → 85 tests.

**Constraints**:
- Real tests with meaningful assertions. No hollow `assert result is not None`.
- Follow CRUCIBLE Protocol — Gate 2 (non-empty assertions), Gate 4 (delta gate).
- S-sized: focused on core modules, not CLI or dashboard.

---

## Portfolio Intelligence

- **Formalized as P-15** (2026-03-06): Asif approved Atlas formalization. Part of Portfolio Intelligence vertical.
- **Revenue track**: Second revenue product after Faultline Pro (P-08b). Open Core vs Faultline SaaS model — different GTM.
- **ASIF dogfooding**: Atlas scans the same portfolio ASIF governs. The CLI could consume NEXUS data for richer health scoring.
- **Cognitive Bridge opportunity**: dx3-mcp (threedb P-05) Cognitive Memory Bridge could give Atlas persistent memory across scans.

---

## Team Questions

_(No pending questions)_

---

## Changelog

| Date | Change |
|------|--------|
| 2026-03-06 | Formalized as P-15. NEXUS created by CLX9 Sr. CoS (Emma). |
| 2026-03-04 | Product built by Wolf (NXTG-AI CoS). 1,814 LOC, 30 tests, CI GREEN. |
