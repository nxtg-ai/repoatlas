# r/Python Post

**Title:** I built a CLI tool to health-score my repos across a portfolio -- Typer + Rich, 30 tests, feedback welcome

**Body:**

I've been building a portfolio of 8+ projects (Python, TypeScript, Rust) and realized I had no way to answer basic questions like "which repos have no tests" or "am I running different FastAPI versions across projects." Everything in the Python ecosystem is great at analyzing one project. Nothing looks across many.

So I built **nxtg-atlas** -- a Python CLI that scans local repos and scores health across 4 dimensions.

```bash
pip install nxtg-atlas
atlas init --name "My Portfolio"
atlas add ~/projects/api
atlas scan
atlas status
```

## Technical details (since this is r/Python)

**Stack:**
- Python 3.11+ (uses tomllib from stdlib, no third-party TOML parser)
- **Typer** for the CLI framework -- first time using it over Click directly, and the type-hint-driven approach is great
- **Rich** for all terminal output (tables, panels, progress bars, color-coded health grades)
- **Pydantic** for data models (project configs, scan results, portfolio state)
- State lives in `~/.atlas/portfolio.json` -- no database, fully portable

**Testing:**
- 30 tests with pytest
- CI runs on Python 3.11, 3.12, 3.13
- Tests cover the scanner, health scoring, tech detection, and CLI commands
- Uses tmp_path fixtures for isolated file system tests

**How the scanner works:**
1. Walks the file tree (skipping node_modules, .venv, target, __pycache__, etc.)
2. Counts source files and test files per language
3. Parses `pyproject.toml`, `package.json`, `Cargo.toml` for dependencies and framework detection
4. Runs git commands (`git log`, `git status`, `git branch`) for repo health
5. Scores 4 dimensions with configurable weights: Tests (35%), Structure (25%), Git Hygiene (20%), Documentation (20%)
6. Aggregates into A-F letter grades

**Things I learned building this:**
- `tomllib` in 3.11+ is great for reading pyproject.toml without adding tomli as a dep
- Rich's `Table` and `Panel` classes make terminal dashboards surprisingly easy
- Typer's `typer.Option()` with `help=` strings gives you beautiful auto-generated `--help` for free
- The hardest part was calibrating the health weights. Too much weight on tests and every frontend gets an F. Too little and untested repos look fine.

**Detection coverage:**
- Languages: Python, TypeScript, JavaScript, Rust, Go, Java, Ruby, C++, Swift, Kotlin
- Frameworks: FastAPI, Django, Flask, React, Next.js, Vue, Express, Tailwind, Vite
- Test frameworks: pytest, Vitest, Jest, Playwright
- Databases: PostgreSQL, SQLite, Redis, MongoDB, pgvector

**What I'd like feedback on:**
- The health scoring formula -- is 35% weight on tests too aggressive?
- Should framework detection read import statements, or is config-file-only good enough?
- Any Typer/Rich patterns I might be missing?

Zero network calls, no telemetry. MIT license. 100% free — no tiers, no limits, no feature gates.

- GitHub: https://github.com/nxtg-ai/repoatlas
- PyPI: https://pypi.org/project/nxtg-atlas/

If atlas saves you time, consider [supporting development on Polar](https://polar.sh/nxtg-ai/repoatlas).
