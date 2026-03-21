"""Tests for display module — portfolio summary panel."""
from __future__ import annotations

from io import StringIO
from unittest.mock import patch

from rich.console import Console

from atlas.display import _show_portfolio_summary, show_status
from atlas.models import GitInfo, HealthScore, Portfolio, Project, TechStack


def _proj(name: str, languages=None, frameworks=None, infrastructure=None,
          security_tools=None, testing_frameworks=None,
          test_files=0, source_files=10, loc=100) -> Project:
    return Project(
        name=name,
        path=f"/tmp/{name}",
        tech_stack=TechStack(
            languages={"Python": 5} if languages is None else languages,
            frameworks=frameworks or [],
            infrastructure=infrastructure or [],
            security_tools=security_tools or [],
            testing_frameworks=testing_frameworks or [],
        ),
        git_info=GitInfo(total_commits=10, branch="main"),
        health=HealthScore(tests=0.8, git_hygiene=0.9, documentation=0.7,
                           structure=0.8, overall=0.8, grade="B"),
        test_file_count=test_files,
        source_file_count=source_files,
        loc=loc,
    )


def _capture_summary(projects: list[Project]) -> str:
    """Capture rendered output from _show_portfolio_summary."""
    portfolio = Portfolio(name="Test", projects=projects)
    buf = StringIO()
    test_console = Console(file=buf, force_terminal=False, width=120)
    with patch("atlas.display.console", test_console):
        _show_portfolio_summary(portfolio)
    return buf.getvalue()


def _capture_status(portfolio: Portfolio) -> str:
    """Capture rendered output from show_status."""
    buf = StringIO()
    test_console = Console(file=buf, force_terminal=False, width=120)
    with patch("atlas.display.console", test_console):
        show_status(portfolio)
    return buf.getvalue()


class TestPortfolioSummaryLanguages:
    def test_shows_language_counts(self):
        projects = [
            _proj("a", languages={"Python": 10, "TypeScript": 5}),
            _proj("b", languages={"Python": 8, "Rust": 3}),
            _proj("c", languages={"TypeScript": 12}),
        ]
        output = _capture_summary(projects)
        assert "Python (2)" in output
        assert "TypeScript (2)" in output
        assert "Rust (1)" in output

    def test_empty_languages(self):
        projects = [
            _proj("a", languages={}),
            _proj("b", languages={}),
        ]
        output = _capture_summary(projects)
        assert "Languages" not in output


class TestPortfolioSummaryFrameworks:
    def test_shows_framework_counts(self):
        projects = [
            _proj("a", frameworks=["FastAPI", "pytest"]),
            _proj("b", frameworks=["FastAPI", "Django"]),
            _proj("c", frameworks=["React", "Vite"]),
        ]
        output = _capture_summary(projects)
        assert "FastAPI (2)" in output

    def test_excludes_docker_from_frameworks(self):
        projects = [
            _proj("a", frameworks=["Docker", "FastAPI"]),
            _proj("b", frameworks=["Docker"]),
        ]
        output = _capture_summary(projects)
        # Docker should be excluded from framework counts
        assert "FastAPI (1)" in output

    def test_empty_frameworks(self):
        projects = [
            _proj("a", frameworks=[]),
            _proj("b", frameworks=[]),
        ]
        output = _capture_summary(projects)
        assert "Frameworks" not in output


class TestPortfolioSummaryInfra:
    def test_ci_coverage(self):
        projects = [
            _proj("a", infrastructure=["GitHub Actions", "Docker"]),
            _proj("b", infrastructure=["Docker"]),
            _proj("c", infrastructure=["GitHub Actions"]),
        ]
        output = _capture_summary(projects)
        assert "CI/CD 2/3" in output
        assert "Docker 2/3" in output

    def test_cloud_coverage(self):
        projects = [
            _proj("a", infrastructure=["AWS"]),
            _proj("b", infrastructure=["GCP"]),
            _proj("c", infrastructure=[]),
        ]
        output = _capture_summary(projects)
        assert "Cloud 2/3" in output

    def test_no_cloud_hides_cloud(self):
        projects = [
            _proj("a", infrastructure=["Docker"]),
            _proj("b", infrastructure=[]),
        ]
        output = _capture_summary(projects)
        assert "Cloud" not in output


class TestPortfolioSummarySecurity:
    def test_security_coverage(self):
        projects = [
            _proj("a", security_tools=["Dependabot", "Gitleaks"]),
            _proj("b", security_tools=["Snyk"]),
            _proj("c", security_tools=[]),
        ]
        output = _capture_summary(projects)
        assert "Any tooling 2/3" in output
        assert "Dep scanning 2/3" in output
        assert "Secret scanning 1/3" in output

    def test_no_security(self):
        projects = [
            _proj("a", security_tools=[]),
            _proj("b", security_tools=[]),
        ]
        output = _capture_summary(projects)
        assert "Any tooling 0/2" in output

    def test_no_dep_scanning_hides_label(self):
        projects = [
            _proj("a", security_tools=["Gitleaks"]),
            _proj("b", security_tools=[]),
        ]
        output = _capture_summary(projects)
        assert "Dep scanning" not in output

    def test_no_secret_scanning_hides_label(self):
        projects = [
            _proj("a", security_tools=["Dependabot"]),
            _proj("b", security_tools=[]),
        ]
        output = _capture_summary(projects)
        assert "Secret scanning" not in output


class TestPortfolioSummaryTesting:
    def test_testing_coverage(self):
        projects = [
            _proj("a", testing_frameworks=["pytest", "tox"]),
            _proj("b", testing_frameworks=["pytest"]),
            _proj("c", testing_frameworks=[]),
        ]
        output = _capture_summary(projects)
        assert "Testing" in output
        assert "2/3 projects" in output
        assert "pytest (2)" in output

    def test_no_testing(self):
        projects = [
            _proj("a", testing_frameworks=[]),
            _proj("b", testing_frameworks=[]),
        ]
        output = _capture_summary(projects)
        # Testing row hidden when no projects have testing frameworks
        assert "Testing" not in output or "0/2" not in output

    def test_testing_multiple_frameworks_ranked(self):
        projects = [
            _proj("a", testing_frameworks=["pytest", "Jest"]),
            _proj("b", testing_frameworks=["pytest", "Vitest"]),
            _proj("c", testing_frameworks=["Jest"]),
        ]
        output = _capture_summary(projects)
        assert "pytest (2)" in output
        assert "Jest (2)" in output

    def test_testing_hidden_when_none(self):
        projects = [
            _proj("a", testing_frameworks=[]),
            _proj("b", testing_frameworks=[]),
        ]
        output = _capture_summary(projects)
        # When no projects have testing, the Testing row should not appear
        lines = output.split("\n")
        testing_lines = [ln for ln in lines if "Testing:" in ln and "projects" in ln]
        assert len(testing_lines) == 0


class TestShowStatusSummaryPanel:
    def test_summary_shown_for_two_plus_projects(self):
        projects = [
            _proj("a", languages={"Python": 5}),
            _proj("b", languages={"Python": 3}),
        ]
        portfolio = Portfolio(name="Test", projects=projects, last_scan="2026-03-13T12:00:00")
        output = _capture_status(portfolio)
        assert "Portfolio Summary" in output

    def test_summary_hidden_for_single_project(self):
        projects = [_proj("solo")]
        portfolio = Portfolio(name="Test", projects=projects, last_scan="2026-03-13T12:00:00")
        output = _capture_status(portfolio)
        assert "Portfolio Summary" not in output

    def test_summary_hidden_for_empty_portfolio(self):
        portfolio = Portfolio(name="Test", projects=[], last_scan="2026-03-13T12:00:00")
        output = _capture_status(portfolio)
        assert "Portfolio Summary" not in output
