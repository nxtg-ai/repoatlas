"""Tests for recommendations engine — actionable health suggestions."""
from __future__ import annotations

from atlas.models import GitInfo, HealthScore, Portfolio, Project, TechStack
from atlas.recommendations import (
    PRIORITY_ORDER,
    Recommendation,
    _cross_project_recommendations,
    _project_recommendations,
    generate_recommendations,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_project(
    name: str = "proj",
    tests: float = 0.8,
    git: float = 0.9,
    docs: float = 0.7,
    structure: float = 0.8,
    test_files: int = 5,
    source_files: int = 20,
    loc: int = 1000,
    uncommitted: int = 0,
    has_remote: bool = True,
    total_commits: int = 50,
    key_deps: dict | None = None,
) -> Project:
    hs = HealthScore(tests=tests, git_hygiene=git, documentation=docs, structure=structure)
    hs.compute()
    return Project(
        name=name,
        path=f"/tmp/{name}",
        tech_stack=TechStack(
            languages={"Python": 10},
            frameworks=["FastAPI"],
            key_deps=key_deps or {},
        ),
        git_info=GitInfo(
            branch="main",
            total_commits=total_commits,
            has_remote=has_remote,
            uncommitted_changes=uncommitted,
        ),
        health=hs,
        test_file_count=test_files,
        source_file_count=source_files,
        total_file_count=source_files + test_files,
        loc=loc,
    )


def _make_portfolio(*projects: Project) -> Portfolio:
    p = Portfolio(name="Test Portfolio")
    p.projects = list(projects)
    return p


# ===========================================================================
# Recommendation dataclass
# ===========================================================================


class TestRecommendation:
    def test_icon_critical(self):
        r = Recommendation("critical", "tests", "msg", ["p"])
        assert "\u2716" in r.icon

    def test_icon_high(self):
        r = Recommendation("high", "tests", "msg", ["p"])
        assert "\u26a0" in r.icon

    def test_icon_medium(self):
        r = Recommendation("medium", "tests", "msg", ["p"])
        assert "\u2139" in r.icon

    def test_icon_low(self):
        r = Recommendation("low", "tests", "msg", ["p"])
        assert "\u2022" in r.icon


# ===========================================================================
# Per-project recommendations
# ===========================================================================


class TestProjectRecommendations:
    def test_zero_tests_critical(self):
        proj = _make_project(tests=0.0, test_files=0, source_files=20)
        recs = _project_recommendations(proj)
        test_recs = [r for r in recs if r.category == "tests"]
        assert len(test_recs) == 1
        assert test_recs[0].priority == "critical"
        assert "Zero tests" in test_recs[0].message

    def test_low_tests_high(self):
        proj = _make_project(tests=0.3, test_files=1, source_files=20)
        recs = _project_recommendations(proj)
        test_recs = [r for r in recs if r.category == "tests"]
        assert len(test_recs) == 1
        assert test_recs[0].priority == "high"

    def test_good_tests_no_rec(self):
        proj = _make_project(tests=0.8, test_files=10, source_files=20)
        recs = _project_recommendations(proj)
        test_recs = [r for r in recs if r.category == "tests"]
        assert len(test_recs) == 0

    def test_many_uncommitted_high(self):
        proj = _make_project(uncommitted=60)
        recs = _project_recommendations(proj)
        git_recs = [r for r in recs if r.category == "git" and "uncommitted" in r.message]
        assert len(git_recs) == 1
        assert git_recs[0].priority == "high"

    def test_some_uncommitted_medium(self):
        proj = _make_project(uncommitted=15)
        recs = _project_recommendations(proj)
        git_recs = [r for r in recs if r.category == "git" and "uncommitted" in r.message]
        assert len(git_recs) == 1
        assert git_recs[0].priority == "medium"

    def test_clean_git_no_rec(self):
        proj = _make_project(uncommitted=0)
        recs = _project_recommendations(proj)
        git_recs = [r for r in recs if r.category == "git" and "uncommitted" in r.message]
        assert len(git_recs) == 0

    def test_no_remote_high(self):
        proj = _make_project(has_remote=False, total_commits=10)
        recs = _project_recommendations(proj)
        remote_recs = [r for r in recs if "remote" in r.message]
        assert len(remote_recs) == 1
        assert remote_recs[0].priority == "high"

    def test_minimal_docs_high(self):
        proj = _make_project(docs=0.1)
        recs = _project_recommendations(proj)
        doc_recs = [r for r in recs if r.category == "docs"]
        assert len(doc_recs) == 1
        assert doc_recs[0].priority == "high"
        assert "README" in doc_recs[0].message

    def test_sparse_docs_medium(self):
        proj = _make_project(docs=0.35)
        recs = _project_recommendations(proj)
        doc_recs = [r for r in recs if r.category == "docs"]
        assert len(doc_recs) == 1
        assert doc_recs[0].priority == "medium"

    def test_good_docs_no_rec(self):
        proj = _make_project(docs=0.7)
        recs = _project_recommendations(proj)
        doc_recs = [r for r in recs if r.category == "docs"]
        assert len(doc_recs) == 0

    def test_no_ci_high(self):
        proj = _make_project(structure=0.2, source_files=20)
        recs = _project_recommendations(proj)
        ci_recs = [r for r in recs if r.category == "structure"]
        assert len(ci_recs) == 1
        assert "CI" in ci_recs[0].message

    def test_healthy_project_no_recs(self):
        proj = _make_project(
            tests=0.9, git=1.0, docs=0.8, structure=0.9,
            test_files=15, source_files=20,
        )
        recs = _project_recommendations(proj)
        assert len(recs) == 0

    def test_small_project_skips_test_rec(self):
        # Projects with <= 5 source files don't get test recommendations
        proj = _make_project(tests=0.0, test_files=0, source_files=3)
        recs = _project_recommendations(proj)
        test_recs = [r for r in recs if r.category == "tests"]
        assert len(test_recs) == 0


# ===========================================================================
# Cross-project recommendations
# ===========================================================================


class TestCrossProjectRecommendations:
    def test_version_mismatch_detected(self):
        a = _make_project("api-v1", key_deps={"fastapi": ">=0.100.0"})
        b = _make_project("api-v2", key_deps={"fastapi": ">=0.115.9"})
        portfolio = _make_portfolio(a, b)
        recs = _cross_project_recommendations(portfolio)
        dep_recs = [r for r in recs if r.category == "deps"]
        assert len(dep_recs) >= 1
        assert dep_recs[0].priority == "high"

    def test_low_health_focus_recommendation(self):
        good = _make_project("good", tests=0.9, git=1.0, docs=0.8, structure=0.9)
        bad = _make_project("bad", tests=0.2, git=0.3, docs=0.1, structure=0.2)
        portfolio = _make_portfolio(good, bad)
        recs = _cross_project_recommendations(portfolio)
        focus_recs = [r for r in recs if "Focus" in r.message]
        assert len(focus_recs) == 1
        assert "bad" in focus_recs[0].message

    def test_all_healthy_minimal_recs(self):
        a = _make_project("a", tests=0.9, git=1.0, docs=0.8, structure=0.9)
        b = _make_project("b", tests=0.9, git=1.0, docs=0.8, structure=0.9)
        portfolio = _make_portfolio(a, b)
        recs = _cross_project_recommendations(portfolio)
        # Should only have low-priority recs or none
        high_recs = [r for r in recs if r.priority in ("critical", "high")]
        assert len(high_recs) == 0


# ===========================================================================
# Full pipeline
# ===========================================================================


class TestGenerateRecommendations:
    def test_sorted_by_priority(self):
        bad = _make_project("bad", tests=0.0, test_files=0, source_files=20, docs=0.1, structure=0.2)
        portfolio = _make_portfolio(bad)
        recs = generate_recommendations(portfolio)
        assert len(recs) > 0
        # Critical should come before high, high before medium
        priorities = [r.priority for r in recs]
        priority_values = [PRIORITY_ORDER.get(p, 99) for p in priorities]
        assert priority_values == sorted(priority_values)

    def test_empty_portfolio(self):
        portfolio = _make_portfolio()
        recs = generate_recommendations(portfolio)
        assert recs == []

    def test_single_healthy_project(self):
        proj = _make_project(tests=0.9, git=1.0, docs=0.8, structure=0.9, test_files=15)
        portfolio = _make_portfolio(proj)
        recs = generate_recommendations(portfolio)
        assert len(recs) == 0

    def test_multiple_issues_all_captured(self):
        proj = _make_project(
            tests=0.0, test_files=0, source_files=30,
            docs=0.1, structure=0.2,
            uncommitted=60, has_remote=False, total_commits=10,
        )
        portfolio = _make_portfolio(proj)
        recs = generate_recommendations(portfolio)
        categories = {r.category for r in recs}
        assert "tests" in categories
        assert "git" in categories
        assert "docs" in categories
        assert "structure" in categories
