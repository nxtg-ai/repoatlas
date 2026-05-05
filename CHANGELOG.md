# Changelog

All notable changes to `nxtg-atlas` are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] — 2026-05-05

Major release. Adds new CLI commands (`ci`, `doctor`, `trends`, `compare`, `config`, `search`), expands detection by ~50 categories, and ships extensive cross-project intelligence. 2,979 tests passing.

### Added — CLI commands
- `atlas ci` — CI/CD gate command. Re-scans portfolio, exits non-zero on health-threshold violations. Outputs structured JSON or one-line summary. `--min-health` and `--min-project-health` thresholds. Powers the new [`atlas-action`](https://github.com/nxtg-ai/atlas-action) GitHub Action.
- `atlas doctor` — actionable per-project and portfolio-wide recommendations (critical / high / medium / low) with specific fix actions across health, security, quality, infrastructure, AI/ML, testing, and documentation dimensions.
- `atlas trends` — scan history and deltas. Compares the last two snapshots showing portfolio direction, per-project up/down/stable/new/removed, and test-count changes. Capped at 100 entries.
- `atlas compare <a> <b>` — side-by-side project comparison. Health breakdown deltas, metrics comparison, tech-stack overlap, version-mismatch detection, actionable insights.
- `atlas config` — persistent TOML configuration at `~/.atlas/config.toml`. Stores CI thresholds and export defaults. Stdlib-only (no new dependencies).
- `atlas search` — search across projects by name, language, framework, or tech.
- `atlas inspect <name>` — detailed per-project card with all detected tech.

### Added — detection (50+ new categories)
Infrastructure (Docker, K8s, Terraform, CI/CD, serverless, cloud providers), security tooling, code-quality tooling, testing frameworks, databases, package managers, licenses, documentation artifacts, CI/CD configuration, runtime versions, AI/ML tooling, monitoring & observability, i18n / localization, geospatial, data visualization, PDF & documents, cryptography, async, media, scraping, compression, accessibility, email, desktop frameworks, file storage, form libraries, animation, routing libraries, game frameworks, CMS, rate limiting, database migrations, gRPC/RPC, code generation, mocking, changelog & release tools, E2E & browser testing, monorepo tools, error tracking & APM, static site generators, mobile frameworks, analytics, workflow engines, secrets management.

### Added — intelligence (cross-project patterns)
Shared-tool detection, divergence warnings, gap detection, and recommendation hooks for every detection category. Connection categories expanded across security, infrastructure, AI/ML, testing, databases, packages, licenses, documentation, CI/CD, monitoring, i18n, geospatial, data viz, PDF, crypto, async, media, scraping, compression, a11y, email, desktop, file storage, forms, animation, routing, game, CMS, rate limiting, migrations, gRPC, codegen, mocking, changelog, E2E, monorepo, error tracking, SSG, mobile, analytics, workflows, secrets.

### Added — experience
- Portfolio summary panel with quick insights.
- Per-category summary panels (testing, database, package manager, license).
- Filterable project list (`--lang`, `--has`, `--grade`, `--min-health`, `--max-health`, sort, limit).
- Rich markdown export.
- Enhanced JSON / CSV export.
- Sort commands across status, search, doctor, compare, connections, and export.

### Added — distribution
- Tag-based release automation: pushing `v*` tags triggers full test matrix → build → twine validate → PyPI publish via Trusted Publisher → GitHub Release.
- CLI integration tests covering every shipped command.

### Changed
- `atlas inspect`, `atlas doctor`, and `atlas status` now surface the full detection footprint across 50+ categories.
- `atlas ci` is the canonical CI integration path; supersedes the prior "CI integration coming soon" FAQ.

### Notes
- Test count: 2,979 passing (up from 30 at 0.1.0, 221 at 0.2.0 baseline).
- ADR-036 release-protocol enforcement (Layer 1 pre-push, Layer 2 nightly drift check) is active for all future releases.

## [0.2.0] — 2026-03-13

Initial public release. Tech stack detection, health scoring, cross-project patterns, terminal dashboard, GitHub CI integration, PyPI publishing.

## [0.1.0] — 2026-03-04

Internal release. 1,814 LOC, 30 tests.
