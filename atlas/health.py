"""Health scoring — computes multi-dimensional health grades for projects."""
from __future__ import annotations

from pathlib import Path

from atlas.models import HealthScore, Project


def compute_health(project: Project) -> HealthScore:
    """Compute health score for a project across 4 dimensions."""
    score = HealthScore()
    path = Path(project.path)

    score.tests = _score_tests(project)
    score.git_hygiene = _score_git(project)
    score.documentation = _score_docs(path)
    score.structure = _score_structure(path, project)
    score.compute()

    return score


def _score_tests(project: Project) -> float:
    """Score based on test file presence and ratio."""
    if project.test_file_count == 0:
        return 0.0
    if project.source_file_count == 0:
        return 0.5

    ratio = project.test_file_count / project.source_file_count

    # Generous scaling: ratio of 0.3+ is excellent
    if ratio >= 0.4:
        return 1.0
    elif ratio >= 0.25:
        return 0.9
    elif ratio >= 0.15:
        return 0.8
    elif ratio >= 0.08:
        return 0.7
    elif ratio >= 0.03:
        return 0.5
    else:
        return 0.3


def _score_git(project: Project) -> float:
    """Score based on git health."""
    gi = project.git_info
    score = 0.0

    # Has git
    if gi.total_commits > 0:
        score += 0.3

    # Has remote
    if gi.has_remote:
        score += 0.2

    # Active (commits > 10 suggests real project)
    if gi.total_commits >= 100:
        score += 0.2
    elif gi.total_commits >= 10:
        score += 0.1

    # Clean working tree
    if gi.uncommitted_changes == 0:
        score += 0.2
    elif gi.uncommitted_changes < 5:
        score += 0.1

    # On main/master branch is neutral (not penalized)
    score += 0.1

    return min(score, 1.0)


def _score_docs(path: Path) -> float:
    """Score based on documentation presence."""
    score = 0.0

    # README
    for readme in ("README.md", "README.rst", "README.txt", "README"):
        if (path / readme).exists():
            score += 0.35
            break

    # CLAUDE.md or .claude/ (AI-ready)
    if (path / "CLAUDE.md").exists() or (path / ".claude").exists():
        score += 0.2

    # .asif/NEXUS.md (portfolio-governed)
    if (path / ".asif" / "NEXUS.md").exists():
        score += 0.2

    # Any docs/ directory
    if (path / "docs").exists() or (path / "doc").exists():
        score += 0.15

    # CHANGELOG or similar
    for f in ("CHANGELOG.md", "CHANGES.md", "HISTORY.md"):
        if (path / f).exists():
            score += 0.1
            break

    return min(score, 1.0)


def _score_structure(path: Path, project: Project) -> float:
    """Score based on project structure and tooling."""
    score = 0.0

    # Has CI (.github/workflows/)
    workflows = path / ".github" / "workflows"
    if workflows.exists() and any(workflows.iterdir()):
        score += 0.3

    # Has .gitignore
    if (path / ".gitignore").exists():
        score += 0.1

    # Has pyproject.toml or package.json (proper packaging)
    if (path / "pyproject.toml").exists() or (path / "package.json").exists() or (path / "Cargo.toml").exists():
        score += 0.2

    # Has source organization (src/ or standard dirs)
    has_src = any(
        (path / d).is_dir()
        for d in ("src", "lib", "app", "api", "server", "client")
    )
    if has_src:
        score += 0.15

    # Not too few files (at least a real project)
    if project.source_file_count >= 10:
        score += 0.15
    elif project.source_file_count >= 3:
        score += 0.1

    # Has linting config
    lint_files = (".eslintrc.js", ".eslintrc.json", "eslint.config.js",
                  "ruff.toml", ".flake8", ".pylintrc", "biome.json")
    if any((path / f).exists() for f in lint_files):
        score += 0.1

    return min(score, 1.0)
