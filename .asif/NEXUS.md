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
| N-16 | [Configuration File](#n-16-configuration-file) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-17 | [Infrastructure Detection](#n-17-infrastructure-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-18 | [Infrastructure Intelligence](#n-18-infrastructure-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-19 | [Security Posture Detection](#n-19-security-posture-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-20 | [Portfolio Summary Panel](#n-20-portfolio-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-21 | [AI/ML Tooling Detection](#n-21-aiml-tooling-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-22 | [Rich Markdown Export](#n-22-rich-markdown-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-23 | [Security Intelligence](#n-23-security-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-24 | [Code Quality Tooling Detection](#n-24-code-quality-tooling-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-25 | [Quality Intelligence](#n-25-quality-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-26 | [Enhanced Doctor Recommendations](#n-26-enhanced-doctor-recommendations) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-27 | [AI/ML Intelligence](#n-27-aiml-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-28 | [Testing Framework Detection](#n-28-testing-framework-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-29 | [Testing Intelligence](#n-29-testing-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-30 | [Testing Summary Panel](#n-30-testing-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-31 | [Enhanced Database Detection](#n-31-enhanced-database-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-32 | [Database Intelligence](#n-32-database-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-33 | [Database Summary Panel](#n-33-database-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-34 | [Package Manager Detection](#n-34-package-manager-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-35 | [Package Manager Intelligence](#n-35-package-manager-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-36 | [Package Manager Summary Panel](#n-36-package-manager-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-37 | [License Detection](#n-37-license-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-38 | [License Intelligence](#n-38-license-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-39 | [License Summary Panel](#n-39-license-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-40 | [Enhanced JSON Export](#n-40-enhanced-json-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-41 | [Documentation Artifacts Detection](#n-41-documentation-artifacts-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-42 | [Documentation Artifacts Intelligence](#n-42-documentation-artifacts-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-43 | [CI/CD Configuration Detection](#n-43-cicd-configuration-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-44 | [Filterable Project List](#n-44-filterable-project-list) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |

**Summary**: 41/44 SHIPPED | 3 DECIDED | 0 IDEA | 0 BUILDING

---

## Vision Pillars

### DETECTION — "Know what you have"
- Automatic tech stack detection across Python/TS/Rust/Go/Java
- File-level analysis, dependency parsing, framework identification
- Infrastructure & deployment: Docker, K8s, Terraform, cloud providers, serverless
- Security posture: Dependabot, Renovate, Snyk, CodeQL, Bandit, Gitleaks, Trivy, SECURITY.md
- AI/ML tooling: Anthropic, OpenAI, LangChain, LlamaIndex, Transformers, PyTorch, TensorFlow, Vercel AI SDK, MLflow, W&B, DVC, Jupyter
- Code quality tooling: Ruff, Flake8, Pylint, ESLint, Biome, Black, Prettier, mypy, Pyright, TypeScript, golangci-lint, Clippy
- Testing frameworks: pytest, Jest, Vitest, Mocha, Cypress, Playwright, go test, cargo test, tox, nox, Hypothesis, AVA, Testing Library
- Database & data stores: PostgreSQL, MySQL, SQLite, MongoDB, Redis, Elasticsearch, Neo4j, Cassandra, InfluxDB, DynamoDB, Firestore, Supabase, PlanetScale, CockroachDB, ChromaDB, Pinecone, Qdrant, Weaviate, Kafka, RabbitMQ, Memcached
- Package managers & build tools: pip, Poetry, PDM, uv, Pipenv, setuptools, Hatch, Flit, npm, Yarn, pnpm, Bun, Cargo, Go Modules, Bundler, Maven, Gradle, NuGet, Composer
- License detection: MIT, Apache-2.0, GPL-2.0/3.0, AGPL-3.0, LGPL, BSD-2/3, ISC, MPL-2.0, Unlicense, CC0 from LICENSE files and package configs
- Documentation artifacts: README, CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE, docs/, API specs (OpenAPI/Swagger), .editorconfig
- CI/CD configuration: GitHub Actions workflows (release/deploy detection), GitLab CI, PR templates, issue templates, CODEOWNERS, Dependabot/Renovate config, pre-commit, git hooks (.husky/.githooks), .gitattributes
- **Shipped**: N-01, N-17, N-19, N-21, N-24, N-28, N-31, N-34, N-37, N-41, N-43

### INTELLIGENCE — "See what others miss"
- Health scoring across 4 dimensions (tests/git/docs/structure)
- Cross-project pattern detection (shared deps, version mismatches, health gaps)
- Side-by-side project comparison with actionable insights
- Cross-project infrastructure intelligence (shared infra, divergence, gaps)
- Cross-project security intelligence (shared tools, adoption gaps, divergence)
- Cross-project quality intelligence (shared tools, adoption gaps, linter divergence)
- Cross-project AI/ML intelligence (shared tools, LLM provider divergence, experiment tracking gaps)
- Cross-project testing intelligence (shared frameworks, runner divergence, testing gaps)
- Cross-project database intelligence (shared databases, relational/vector/broker divergence, database gaps)
- Cross-project package manager intelligence (shared managers, JS/Python/Java divergence)
- Cross-project license intelligence (shared licenses, copyleft/permissive divergence, license gaps)
- Cross-project documentation intelligence (shared artifacts, docs coverage divergence, README/CHANGELOG/CONTRIBUTING gaps)
- **Shipped**: N-02, N-03, N-15, N-18, N-23, N-25, N-27, N-29, N-32, N-35, N-38, N-42

### EXPERIENCE — "Beautiful enough to screenshot"
- Rich terminal dashboard with tables, progress bars, color
- Fast scanning (31s for 8 projects, 1.2M LOC)
- Scan history & health trends over time
- Persistent TOML configuration
- Portfolio summary panel: language distribution, framework adoption, infra coverage, security posture
- Rich markdown export for portfolio reports
- Enhanced doctor recommendations leveraging all detection data
- Testing framework adoption in portfolio summary panel and markdown export
- Database adoption in portfolio summary panel and markdown export
- Package manager adoption in portfolio summary panel and markdown export
- License distribution in portfolio summary panel and markdown export
- Comprehensive JSON export with connections, recommendations, and portfolio aggregates
- Filterable dashboard: `atlas status --grade A --lang Python --has Docker --min-health 80`
- **Shipped**: N-04, N-13, N-16, N-20, N-22, N-26, N-30, N-33, N-36, N-39, N-40, N-44

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
**What**: New `atlas doctor` command with recommendations engine (`recommendations.py`). Analyzes per-project health (tests, git, docs, structure) and cross-project patterns (version mismatches, health focus). Outputs prioritized suggestions (critical/high/medium/low) with specific fix actions. 24 recommendation tests + 4 CLI doctor tests. Enhanced by N-26 to cover security, quality, and infrastructure.
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

### N-16: Configuration File
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas config` command with persistent TOML configuration (`~/.atlas/config.toml`). View all settings, get/set individual keys. Supports `ci.min_health`, `ci.min_project_health`, `export.format`. CI command reads defaults from config when flags aren't explicitly set. Uses stdlib `tomllib` (Python 3.11+) — no new dependencies. 15 config unit tests + 5 CLI config tests.
**Shipped**: 2026-03-13. Total test count: 347 → 367. README commands table updated.

### N-17: Infrastructure Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_infrastructure()` in detector.py. Detects Docker/Compose, Kubernetes/Helm, Terraform/Pulumi/CDK, CI/CD (GitHub Actions/GitLab CI/Jenkins/CircleCI), serverless (Vercel/Netlify/Cloudflare Workers/Fly.io/Render), and cloud providers (AWS/GCP/Azure from SDK deps). Added `infrastructure` field to TechStack model. Shows in `atlas inspect`. 28 infrastructure tests.
**Shipped**: 2026-03-13. Total test count: 367 → 395. README "What It Detects" table expanded.

### N-21: AI/ML Tooling Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_ai_tools()` in detector.py. Detects AI/ML frameworks and tools across Python (Anthropic, OpenAI, LangChain, LlamaIndex, Transformers, PyTorch, TensorFlow, scikit-learn, MLflow, W&B, ChromaDB, Pinecone, Sentence Transformers) and JavaScript (@anthropic-ai/sdk, openai, LangChain, Vercel AI SDK, Hugging Face). Also detects Jupyter notebooks (.ipynb), ML infrastructure (MLproject, wandb/, DVC). Added `ai_tools` field to TechStack model. Shows in `atlas inspect` and portfolio summary panel. 32 AI tools tests.
**Shipped**: 2026-03-13. Total test count: 451 → 483. README "What It Detects" table expanded. Directly serves North Star ("AI Engineering Teams").

### N-20: Portfolio Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Aggregate portfolio insights panel added to `atlas status` dashboard (shown for 2+ projects). Displays language distribution with project counts, framework adoption (excluding Docker), infrastructure coverage (CI/CD, Docker, Cloud as X/N ratios), and security posture overview (tooling coverage, dep scanning, secret scanning). Uses Rich Panel rendering. 15 display tests.
**Shipped**: 2026-03-13. Total test count: 436 → 451. Surfaces N-17/N-19 detection data in the main dashboard.

### N-19: Security Posture Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_security_tools()` in detector.py. Detects security tooling across projects: dependency scanning (Dependabot, Renovate, Snyk), secret scanning (Gitleaks, SOPS, detect-secrets), Python SAST (Bandit, Safety, pip-audit), code analysis (CodeQL, Trivy), and security policy (SECURITY.md). Reads pre-commit configs for security hooks. Added `security_tools` field to TechStack model. Shows in `atlas inspect`. 26 security tests.
**Shipped**: 2026-03-13. Total test count: 410 → 436. README "What It Detects" table expanded.

### N-22: Rich Markdown Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Refactored markdown export into dedicated `export_report.py` module with `build_markdown_report()`. Generates comprehensive portfolio reports: header with aggregate stats, project table sorted by health, portfolio summary (languages, frameworks, infra coverage, security posture, AI/ML adoption), per-project details (health breakdown across 4 dimensions, all tech stack fields, git info), and cross-project intelligence grouped by type with severity icons. Replaces inline markdown generation in cli.py. 23 export tests.
**Shipped**: 2026-03-13. Total test count: 483 → 506. Surfaces all detection data (N-17, N-19, N-21) in exported reports.

### N-25: Quality Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project quality pattern detection via `_find_quality_patterns()` in connections.py. Analyzes quality tooling from N-24 across the portfolio to detect: shared quality tools (Ruff/mypy across 2+ projects), quality adoption gaps (no tooling, missing linting, missing type checking), and linter divergence (multiple linters across portfolio). New connection types (`shared_quality`, `quality_divergence`, `quality_gap`) displayed in `atlas connections` and markdown export. 16 quality pattern tests.
**Shipped**: 2026-03-13. Total test count: 567 → 583. Completes N-24 detection→intelligence pipeline. Parallels N-19→N-23 and N-17→N-18 patterns.

### N-24: Code Quality Tooling Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_quality_tools()` in detector.py. Detects code quality tooling across projects: Python linters (Ruff, Flake8, Pylint), Python formatters (Black, isort, autopep8), Python type checkers (mypy, Pyright), JS/TS tools (ESLint, Prettier, TypeScript, Biome), Go (golangci-lint), Rust (Clippy). Reads config files, dependency files, pyproject.toml sections, and pre-commit hooks. Added `quality_tools` field to TechStack model. Shows in `atlas inspect`, portfolio summary panel, and markdown export. 45 quality tools tests.
**Shipped**: 2026-03-13. Total test count: 522 → 567. Enables future quality intelligence layer.

### N-23: Security Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project security pattern detection via `_find_security_patterns()` in connections.py. Analyzes security tooling from N-19 across the portfolio to detect: shared security tools (Dependabot/Gitleaks across 2+ projects), security adoption gaps (no tooling, missing dep scanning, missing secret scanning), and security tool divergence (multiple dep scanners across portfolio). New connection types (`shared_security`, `security_divergence`, `security_gap`) displayed in `atlas connections` and markdown export. 16 security pattern tests.
**Shipped**: 2026-03-13. Total test count: 506 → 522. Builds on N-19 detection data. Parallels N-17→N-18 (detection→intelligence) pattern.

### N-26: Enhanced Doctor Recommendations
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Enhanced `atlas doctor` recommendations engine to leverage all detection data from N-17/N-19/N-24/N-25. Per-project: security (no tooling, missing dep scanning, missing secret scanning), quality (no tooling, missing linting, missing type checking), infrastructure (no CI/CD). Cross-project: maps security_gap/security_divergence, quality_gap/quality_divergence, infra_gap/infra_divergence connections to prioritized recommendations. 23 new recommendation tests.
**Shipped**: 2026-03-13. Total test count: 583 → 606. Surfaces all detection+intelligence data through actionable `atlas doctor` output.

### N-35: Package Manager Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project package manager pattern detection via `_find_package_manager_patterns()` in connections.py. Detects: shared package managers (Poetry/npm across 2+ projects), JS package manager divergence (npm vs Yarn vs pnpm vs Bun), Python package manager divergence (pip vs Poetry vs PDM vs uv vs Pipenv), Java build tool divergence (Maven vs Gradle). New connection types (`shared_pkg_manager`, `pkg_manager_divergence`) displayed in `atlas connections`, markdown export, and `atlas doctor`. 13 package manager pattern tests.
**Shipped**: 2026-03-21. Total test count: 736 → 749. Completes N-34 detection→intelligence pipeline. All 7 detection→intelligence pipelines complete.

### N-44: Filterable Project List
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added 5 filter options to `atlas status`: `--grade` (filter by health grade A/B+/B/C/D/F), `--lang` (filter by language), `--has` (filter by any tech — searches all TechStack fields including frameworks, databases, infrastructure, security, quality, testing, package managers, docs artifacts, CI config), `--min-health` (minimum health %), `--max-health` (maximum health %). Filters compose (AND logic). When filters active, shows "Filtered: ..." header and creates a temporary Portfolio with only matching projects. Cross-project intelligence runs on filtered set. No match shows friendly message. Helper `_project_has_tech()` does case-insensitive search across all 11 TechStack list fields. 6 new CLI integration tests.
**Shipped**: 2026-03-21. Total test count: 871 → 877. First interactive UX feature since N-16 (config).

### N-43: CI/CD Configuration Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_ci_config()` in detector.py. Detects CI/CD configuration and workflow artifacts: GitHub Actions workflows (with release/deploy pattern detection), GitLab CI, PR templates (file + directory forms), issue templates, CODEOWNERS (3 locations), Dependabot config, Renovate config (4 file variants), pre-commit hooks, git hooks (.husky/.githooks directories), and .gitattributes. Added `ci_config` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py and export_report.py), markdown export project details, and JSON export portfolio_summary. 18 new detection tests, 3 display tests.
**Shipped**: 2026-03-21. Total test count: 850 → 871. 11th detection category.

### N-42: Documentation Artifacts Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project documentation artifact pattern detection via `_find_docs_artifact_patterns()` in connections.py. Analyzes docs_artifacts data from N-41 across the portfolio to detect: shared documentation artifacts (README/CHANGELOG/LICENSE across 2+ projects, info), documentation coverage divergence (projects with 5+ artifacts vs projects with ≤1 artifact and 5+ source files, warning), and documentation gaps — README missing (critical, >5 source files), CHANGELOG missing (warning, >10 source files), CONTRIBUTING missing (warning, >20 source files). New connection types (`shared_docs`, `docs_divergence`, `docs_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps to `docs` recommendation category. 17 documentation pattern tests.
**Shipped**: 2026-03-21. Total test count: 833 → 850. Completes N-41 detection→intelligence pipeline. 9th intelligence layer.

### N-41: Documentation Artifacts Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_docs_artifacts()` in detector.py. Detects documentation artifacts present in projects: README (md/rst/txt), CHANGELOG (also CHANGES/HISTORY variants), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY policy, LICENSE file, docs/ directory, API specs (OpenAPI/Swagger JSON/YAML — checks root and docs/ subdirectory), and .editorconfig. Returns sorted list of artifact names. Added `docs_artifacts` field to TechStack model. Shows in `atlas inspect` project card, markdown export project details, portfolio summary panel (display.py and export_report.py), and JSON export portfolio_summary. 17 new detection tests, 3 display tests. Distinct from health.py documentation scoring — health gives a numeric score for README/CHANGELOG/docs/CLAUDE.md presence; docs_artifacts provides a detailed inventory of specific documentation artifacts.
**Shipped**: 2026-03-21. Total test count: 813 → 833. 10th detection category.

### N-40: Enhanced JSON Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Comprehensive JSON export via `build_json_report()` in export_report.py. Replaces the basic inline JSON generation in cli.py. Now includes: portfolio summary aggregates (languages, frameworks, infra, security, quality, testing, databases, package managers, AI/ML, licenses — all as structured data), cross-project connections (type, detail, projects, severity), and doctor recommendations (priority, category, message, projects). Per-project data includes license field. Uses raw `print()` for JSON stdout to avoid Rich markup corruption. 14 new JSON export tests.
**Shipped**: 2026-03-21. Total test count: 799 → 813. JSON export now at full parity with markdown export.

### N-39: License Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added license distribution stats to the portfolio summary panel (display.py) and markdown export (export_report.py). Shows `Licenses: X/N projects · MIT (3), Apache-2.0 (2)` with top licenses ranked by usage. Row hidden when no projects have detected licenses. 6 new tests (3 display, 3 export).
**Shipped**: 2026-03-21. Total test count: 793 → 799. Completes the detection→intelligence→summary pipeline for licenses (N-37→N-38→N-39). All 8 pipelines now have full summary panel visibility.

### N-38: License Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project license pattern detection via `_find_license_patterns()` in connections.py. Analyzes license data from N-37 across the portfolio to detect: shared licenses (MIT/Apache-2.0 across 2+ projects), license divergence with copyleft/permissive detection (GPL+MIT mix = critical severity, MIT+Apache = warning severity), and license gaps (projects with 5+ source files but no detected license). New connection types (`shared_license`, `license_divergence`, `license_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps to `docs` recommendation category. 13 license pattern tests.
**Shipped**: 2026-03-21. Total test count: 780 → 793. Completes N-37 detection→intelligence pipeline. 8th intelligence layer.

### N-37: License Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_license()` in detector.py. Detects project licenses from three sources: config files (pyproject.toml `[project] license`, package.json `license`, Cargo.toml `[package] license`), and LICENSE/LICENCE/COPYING file content analysis. Recognizes 13 license families: MIT, Apache-2.0, GPL-2.0/3.0, AGPL-3.0, LGPL-2.1/3.0, BSD-2-Clause/3-Clause, ISC, MPL-2.0, Unlicense, CC0-1.0. SPDX normalization handles variant identifiers (e.g., `GPL-3.0-only` → `GPL-3.0`). Config files take priority over LICENSE file content. Added `license` field to Project model (not TechStack — license is project-level). Shows in `atlas inspect` and markdown export. 25 license detection tests.
**Shipped**: 2026-03-21. Total test count: 755 → 780. 9th detection category. Enables future license intelligence layer for compliance.

### N-36: Package Manager Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added package manager adoption stats to the portfolio summary panel (display.py) and markdown export (export_report.py). Shows `Pkg Mgrs: X/N projects · Poetry (3), npm (2)` with top managers ranked by usage. Row hidden when no projects have package managers. 6 new tests (3 display, 3 export).
**Shipped**: 2026-03-21. Completes the detection→intelligence→summary pipeline for package managers (N-34→N-35→N-36). All 7 pipelines now have full summary panel visibility.

### N-34: Package Manager Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_package_managers()` in detector.py. Detects package managers and build tools across ecosystems: Python (pip, Poetry, PDM, uv, Pipenv, setuptools, Hatch, Flit), JavaScript/TypeScript (npm, Yarn, pnpm, Bun), Rust (Cargo), Go (Go Modules), Ruby (Bundler), Java/Kotlin (Maven, Gradle), .NET (NuGet), PHP (Composer). Detects via lockfiles, config files, and pyproject.toml build-system declarations. Smart deduplication — pip not added when Poetry/PDM/uv/Pipenv present. Added `package_managers` field to TechStack model. Shows in `atlas inspect` and markdown export. 25 package manager tests.
**Shipped**: 2026-03-21. Total test count: 711 → 736. 8th detection category.

### N-33: Database Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added database adoption stats to the portfolio summary panel (display.py) and markdown export (export_report.py). Shows `Databases: X/N projects · PostgreSQL (3), Redis (2)` with top databases ranked by usage. Row hidden when no projects have databases. 6 new tests (3 display, 3 export).
**Shipped**: 2026-03-21. Total test count: 705 → 711. All detection categories now have portfolio summary panel visibility: languages, frameworks, infra, security, quality, testing, databases, AI/ML.

### N-32: Database Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Replaced `_find_shared_databases()` with `_find_database_patterns()` in connections.py. Keeps shared database detection (info) and adds: relational DB divergence (PostgreSQL vs MySQL across portfolio, SQLite excluded as dev DB), vector DB divergence (ChromaDB vs Pinecone), message broker divergence (RabbitMQ vs Kafka), and database gaps (web/API projects with FastAPI/Django/Express/etc but no database detected). New connection types (`database_divergence`, `database_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. 16 new database pattern tests (replacing 5 old shared-only tests = net +11).
**Shipped**: 2026-03-13. Total test count: 694 → 705. Completes N-31 detection→intelligence pipeline. All 6 detection→intelligence pipelines complete.

### N-31: Enhanced Database Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Expanded `detect_databases()` from 5 to 21 databases/data stores. New categories: relational (MySQL/MariaDB, CockroachDB, PlanetScale, Supabase), document (Firestore, DynamoDB), search (Elasticsearch/OpenSearch), graph (Neo4j), time-series (InfluxDB), wide-column (Cassandra), cache (Memcached), vector (ChromaDB, Pinecone, Qdrant, Weaviate), message brokers (RabbitMQ/AMQP, Kafka). Expanded search to go.mod, Cargo.toml, Gemfile, pom.xml, build.gradle, requirements-dev.txt, .env.sample. Refactored to use `_add()` helper for deduplication. 21 new database detection tests.
**Shipped**: 2026-03-13. Total test count: 673 → 694. 4.2x expansion of database detection coverage.

### N-30: Testing Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added testing framework adoption stats to the portfolio summary panel (display.py) and markdown export (export_report.py). Shows `Testing: X/N projects · pytest (3), Jest (2)` with top frameworks ranked by usage. Row hidden when no projects have testing frameworks. Follows the established pattern from security/quality/AI/ML summary rows. 7 new tests (4 display, 3 export).
**Shipped**: 2026-03-13. Total test count: 666 → 673. Completes the summary panel — all detection categories now have portfolio-level visibility.

### N-29: Testing Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project testing framework pattern detection via `_find_testing_patterns()` in connections.py. Analyzes testing framework data from N-28 across the portfolio to detect: shared testing frameworks (pytest/Jest across 2+ projects), JS test runner divergence (Jest vs Vitest vs Mocha vs AVA), Python test runner divergence (pytest vs nose2 vs unittest2), and testing gaps (projects with 5+ source files but no testing framework). New connection types (`shared_testing`, `testing_divergence`, `testing_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. 15 testing pattern tests.
**Shipped**: 2026-03-13. Total test count: 651 → 666. Completes N-28 detection→intelligence pipeline. All 5 detection→intelligence pipelines complete: infra (N-17→N-18), security (N-19→N-23), quality (N-24→N-25), AI/ML (N-21→N-27), testing (N-28→N-29).

### N-28: Testing Framework Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_testing_frameworks()` in detector.py. Detects testing frameworks and tools across projects: Python (pytest, tox, nox, Hypothesis, coverage.py, nose2), JavaScript/TypeScript (Jest, Vitest, Mocha, Cypress, Playwright, AVA, Testing Library), Go (go test from _test.go files), Rust (cargo test from Cargo.toml). Reads config files (pytest.ini, jest.config.*, vitest.config.*, .mocharc.*, cypress.config.*, playwright.config.*), dependency files, and conftest.py. Added `testing_frameworks` field to TechStack model. Shows in `atlas inspect` and markdown export. 30 testing framework tests.
**Shipped**: 2026-03-13. Total test count: 621 → 651. Separates testing tools from general frameworks for dedicated visibility.

### N-27: AI/ML Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project AI/ML pattern detection via `_find_ai_patterns()` in connections.py. Analyzes AI/ML tooling from N-21 across the portfolio to detect: shared AI/ML tools (Anthropic SDK/LangChain across 2+ projects), LLM provider divergence (Anthropic vs OpenAI across portfolio), vector DB divergence (ChromaDB vs Pinecone), and experiment tracking gaps (ML projects using PyTorch/TensorFlow/sklearn without MLflow/W&B/DVC). New connection types (`shared_ai`, `ai_divergence`, `ai_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. 15 AI pattern tests.
**Shipped**: 2026-03-13. Total test count: 606 → 621. Completes N-21 detection→intelligence pipeline. Completes all 4 detection→intelligence pipelines: infra (N-17→N-18), security (N-19→N-23), quality (N-24→N-25), AI/ML (N-21→N-27).

### N-18: Infrastructure Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project infrastructure pattern detection via `_find_infra_patterns()` in connections.py. Analyzes infrastructure data from N-17 across the portfolio to detect: shared infrastructure (Docker/CI across 2+ projects), platform divergence (multiple hosting platforms per project), CI divergence (multiple CI systems across portfolio), no-CI gaps, cloud usage without IaC, Docker without orchestration. New connection types (`shared_infra`, `infra_divergence`, `infra_gap`) displayed in `atlas connections`. 16 infra pattern tests.
**Shipped**: 2026-03-13. Total test count: 395 → 410. Builds on N-17 detection data.

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
