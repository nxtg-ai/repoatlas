---
title: "Why Your Multi-Repo Setup Is a Ticking Time Bomb"
published: false
description: "You manage 8+ repos. One uses React 18, another React 19, and nobody noticed. Here are the 4 blind spots silently degrading your codebase — and how to find them in 30 seconds."
tags: productivity, devops, python, opensource
cover_image:
canonical_url:
---

Last Tuesday I pushed a hotfix to our API service. Standard stuff — patch a validation bug, run the tests, ship it. Tests passed. PR merged. Deploy went green.

Then our frontend broke.

The API service was on Pydantic v2. The frontend's shared types package was still importing from Pydantic v1. They'd been out of sync for three months. Nobody noticed because nobody was looking across repos.

If you manage more than three repositories, you have this problem. You might not know it yet. But it's there, silently accumulating, waiting for the worst possible moment to surface.

I manage 8 production repos. After that Tuesday, I spent a week figuring out exactly how many of these invisible problems I was sitting on. The answer was uncomfortable. Here are the four categories of blind spots I found — and I'd bet real money you have all four.

## Blind Spot #1: Inconsistent Test Coverage

Here's a question you probably can't answer right now without checking: which of your repos have zero tests?

Not "low coverage" — literally zero. No test files. No test runner configured. Nothing.

When I actually scanned my repos, I found that two of my eight projects had respectable test suites — 179 test files in one, 114 in another. But one project that handles real user data had 23 test files covering a codebase of 12,000+ lines. And the project with the most lines of code (793,000 LOC) was sitting at a C grade for test health.

The problem isn't that you write bad tests. It's that you have no visibility into the distribution. Your main API might have 90% coverage while your auth service — the thing that guards everything — has 15%. You'd never know unless you manually checked every repo, every sprint. Nobody does that.

The test coverage conversation happens per-repo during code review. It never happens across repos. That's the gap.

## Blind Spot #2: Version Drift

This is the one that burned me. And it's insidious because it doesn't break anything — until it does.

Here's what version drift looks like in practice. You have four projects using FastAPI. One is pinned to `>=0.100.0` because it was scaffolded six months ago. Another uses `>=0.115.9` because you set it up last week. They both work. They both pass CI. But they're running different versions of the same framework, with different behaviors, different defaults, and different bugs.

Now multiply that across every shared dependency: React, TypeScript, Python itself, your ORM, your test framework, your linting config.

When I scanned my eight repos, I found version mismatches in React (18.2 vs 19.2) and FastAPI (0.100 vs 0.115) immediately. Those were the ones I caught. I suspect there are more buried in transitive dependencies.

The core issue: every repo manages its own `package.json` or `pyproject.toml` in isolation. There's no mechanism to check whether your five Python projects agree on what version of `httpx` they're using. So they don't.

## Blind Spot #3: Documentation Gaps

I'm not talking about API docs or Swagger pages. I'm talking about basic orientation documentation — does every repo have a README? A CHANGELOG? A `docs/` directory? CI configuration that a new contributor can actually read?

Some of my repos had thorough documentation: README, changelog, architectural decision records, contributor guides. Others — including one with 136,000 lines of code — had a README that hadn't been updated since the initial commit.

The pattern I see is this: documentation quality correlates with how many people touch a repo. Solo projects rot. The repos where I'm the only contributor tend to accumulate "I'll document this later" debt faster than anything else.

But here's the thing — the solo projects are often the ones that most need documentation. Because when you come back to them after three weeks of working on something else, you're effectively a new contributor to your own project.

You know which repos need docs. You just don't have a systematic way to check. So it falls to instinct and memory, which are terrible governance tools.

## Blind Spot #4: Structural Inconsistency

This one is subtle. It's not about bugs or missing features — it's about whether your repos are built consistently.

Does every project have a `.gitignore`? CI/CD configuration? A linting setup? A proper package manifest? Source code organized in a standard layout?

When I audited my repos, I found one project scoring 94% on structure — proper CI, clean git history, good package config — right next to another project at 59%. They were built by the same person (me), in the same year, for the same organization. The difference? One was set up carefully with a template. The other was scaffolded in a rush during a hackathon and never cleaned up.

Structural inconsistency creates friction every time you context-switch between projects. Different folder layouts, different test commands, different CI pipelines. Each one costs you 10 minutes of re-orientation. Multiply that by how many times you switch per day.

This is the kind of thing that doesn't show up on any dashboard because nobody has a dashboard that spans repos.

## The Cross-Repo Visibility Problem

All four of these blind spots share a root cause: **every tool you use operates inside a single repository.**

Your IDE sees one repo. Your CI runs per-repo. Your linter, your test runner, your dependency checker — all scoped to one project at a time.

There's no `git status` for your entire portfolio. No `npm audit` that works across repos. No test coverage report that spans projects.

This is the gap I set out to close. I built a CLI tool called [nxtg-atlas](https://github.com/nxtg-ai/repoatlas) that scans multiple repos and produces a portfolio-level health dashboard.

It scores each project across four dimensions — tests (35% weight), git hygiene (20%), documentation (20%), and structure (25%) — and rolls them into an A-F grade. Then it looks across projects for shared dependencies, version mismatches, and health gaps.

No cloud. No telemetry. No network calls. It parses your actual config files (`pyproject.toml`, `package.json`, `Cargo.toml`), counts real test files, inspects git history, and produces a dashboard in your terminal.

When I pointed it at my 8 repos — 1.25 million lines of code — it finished in 31 seconds and showed me everything I described above in a single table. Version mismatches I'd missed for months. Test coverage distribution I'd never visualized. Documentation gaps I knew existed but had never quantified.

## Try It

```bash
pip install nxtg-atlas

atlas init --name "My Portfolio"
atlas add ~/projects/api
atlas add ~/projects/frontend
atlas add ~/projects/worker
atlas scan
atlas status
```

Five commands. Thirty seconds. You'll see your blind spots.

Everything is free. No tiers, no limits, no feature gates. Unlimited projects, cross-project intelligence, export — all of it.

MIT licensed. Open source. Python 3.11+. If atlas saves you time, consider [supporting development](https://polar.sh/nxtg-ai/repoatlas).

**GitHub**: [github.com/nxtg-ai/repoatlas](https://github.com/nxtg-ai/repoatlas)

---

The repos you don't look at are the ones that hurt you. Start looking.
