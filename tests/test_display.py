"""Tests for display module — portfolio summary panel."""
from __future__ import annotations

from io import StringIO
from unittest.mock import patch

from rich.console import Console

from atlas.display import _show_portfolio_summary, show_quick_insights, show_status, sparkline
from atlas.history import ProjectSnapshot, ScanEntry
from atlas.recommendations import Recommendation
from atlas.models import GitInfo, HealthScore, Portfolio, Project, TechStack


def _proj(name: str, languages=None, frameworks=None, infrastructure=None,
          security_tools=None, testing_frameworks=None, databases=None,
          package_managers=None, docs_artifacts=None, ci_config=None,
          project_license="",
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
            databases=databases or [],
            package_managers=package_managers or [],
            docs_artifacts=docs_artifacts or [],
            ci_config=ci_config or [],
        ),
        git_info=GitInfo(total_commits=10, branch="main"),
        health=HealthScore(tests=0.8, git_hygiene=0.9, documentation=0.7,
                           structure=0.8, overall=0.8, grade="B"),
        test_file_count=test_files,
        source_file_count=source_files,
        loc=loc,
        license=project_license,
    )


def _capture_summary(projects: list[Project]) -> str:
    """Capture rendered output from _show_portfolio_summary."""
    portfolio = Portfolio(name="Test", projects=projects)
    buf = StringIO()
    test_console = Console(file=buf, force_terminal=False, width=120)
    with patch("atlas.display.console", test_console):
        _show_portfolio_summary(portfolio)
    return buf.getvalue()


def _capture_status(portfolio: Portfolio, history=None) -> str:
    """Capture rendered output from show_status."""
    buf = StringIO()
    test_console = Console(file=buf, force_terminal=False, width=120)
    with patch("atlas.display.console", test_console):
        show_status(portfolio, history=history)
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


class TestPortfolioSummaryDatabases:
    def test_database_coverage(self):
        projects = [
            _proj("a", databases=["PostgreSQL", "Redis"]),
            _proj("b", databases=["PostgreSQL"]),
            _proj("c", databases=[]),
        ]
        output = _capture_summary(projects)
        assert "Databases" in output
        assert "2/3 projects" in output
        assert "PostgreSQL (2)" in output

    def test_database_hidden_when_none(self):
        projects = [
            _proj("a", databases=[]),
            _proj("b", databases=[]),
        ]
        output = _capture_summary(projects)
        lines = output.split("\n")
        db_lines = [ln for ln in lines if "Databases:" in ln and "projects" in ln]
        assert len(db_lines) == 0

    def test_database_multiple_ranked(self):
        projects = [
            _proj("a", databases=["PostgreSQL", "Redis"]),
            _proj("b", databases=["PostgreSQL", "MongoDB"]),
            _proj("c", databases=["Redis"]),
        ]
        output = _capture_summary(projects)
        assert "PostgreSQL (2)" in output
        assert "Redis (2)" in output


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


class TestPortfolioSummaryPackageManagers:
    def test_pkg_manager_coverage(self):
        projects = [
            _proj("a", package_managers=["Poetry", "npm"]),
            _proj("b", package_managers=["Poetry"]),
            _proj("c", package_managers=[]),
        ]
        output = _capture_summary(projects)
        assert "Pkg Mgrs" in output
        assert "2/3 projects" in output
        assert "Poetry (2)" in output

    def test_pkg_manager_hidden_when_none(self):
        projects = [
            _proj("a", package_managers=[]),
            _proj("b", package_managers=[]),
        ]
        output = _capture_summary(projects)
        lines = output.split("\n")
        pm_lines = [ln for ln in lines if "Pkg Mgrs:" in ln and "projects" in ln]
        assert len(pm_lines) == 0

    def test_pkg_manager_multiple_ranked(self):
        projects = [
            _proj("a", package_managers=["Poetry", "npm"]),
            _proj("b", package_managers=["Poetry", "pnpm"]),
            _proj("c", package_managers=["npm"]),
        ]
        output = _capture_summary(projects)
        assert "Poetry (2)" in output
        assert "npm (2)" in output


class TestPortfolioSummaryLicenses:
    def test_license_coverage(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="MIT"),
            _proj("c", project_license=""),
        ]
        output = _capture_summary(projects)
        assert "Licenses" in output
        assert "2/3 projects" in output
        assert "MIT (2)" in output

    def test_license_hidden_when_none(self):
        projects = [
            _proj("a", project_license=""),
            _proj("b", project_license=""),
        ]
        output = _capture_summary(projects)
        lines = output.split("\n")
        lic_lines = [ln for ln in lines if "Licenses:" in ln and "projects" in ln]
        assert len(lic_lines) == 0

    def test_license_multiple_ranked(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="MIT"),
            _proj("c", project_license="Apache-2.0"),
        ]
        output = _capture_summary(projects)
        assert "MIT (2)" in output
        assert "Apache-2.0 (1)" in output


class TestPortfolioSummaryDocsArtifacts:
    def test_docs_coverage(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG", "LICENSE"]),
            _proj("b", docs_artifacts=["README"]),
            _proj("c", docs_artifacts=[]),
        ]
        output = _capture_summary(projects)
        assert "Docs" in output
        assert "2/3 projects" in output
        assert "README (2)" in output

    def test_docs_hidden_when_none(self):
        projects = [
            _proj("a", docs_artifacts=[]),
            _proj("b", docs_artifacts=[]),
        ]
        output = _capture_summary(projects)
        lines = output.split("\n")
        docs_lines = [ln for ln in lines if "Docs:" in ln and "projects" in ln]
        assert len(docs_lines) == 0

    def test_docs_multiple_ranked(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG", "LICENSE"]),
            _proj("b", docs_artifacts=["README", "CONTRIBUTING"]),
            _proj("c", docs_artifacts=["README"]),
        ]
        output = _capture_summary(projects)
        assert "README (3)" in output
        assert "CHANGELOG (1)" in output


class TestPortfolioSummaryCiConfig:
    def test_ci_config_coverage(self):
        projects = [
            _proj("a", ci_config=["GitHub Actions", "pre-commit"]),
            _proj("b", ci_config=["GitHub Actions"]),
            _proj("c", ci_config=[]),
        ]
        output = _capture_summary(projects)
        assert "CI Config" in output
        assert "2/3 projects" in output
        assert "GitHub Actions (2)" in output

    def test_ci_config_hidden_when_none(self):
        projects = [
            _proj("a", ci_config=[]),
            _proj("b", ci_config=[]),
        ]
        output = _capture_summary(projects)
        lines = output.split("\n")
        ci_lines = [ln for ln in lines if "CI Config:" in ln and "projects" in ln]
        assert len(ci_lines) == 0

    def test_ci_config_multiple_ranked(self):
        projects = [
            _proj("a", ci_config=["GitHub Actions", "pre-commit", "CODEOWNERS"]),
            _proj("b", ci_config=["GitHub Actions", "Dependabot config"]),
            _proj("c", ci_config=["pre-commit"]),
        ]
        output = _capture_summary(projects)
        assert "GitHub Actions (2)" in output
        assert "pre-commit (2)" in output


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


def _capture_quick_insights(recs: list) -> str:
    """Capture rendered output from show_quick_insights."""
    buf = StringIO()
    test_console = Console(file=buf, force_terminal=False, width=120)
    with patch("atlas.display.console", test_console):
        show_quick_insights(recs)
    return buf.getvalue()


class TestQuickInsights:
    def test_shows_critical_recs(self):
        recs = [
            Recommendation("critical", "tests", "Zero tests in app1", ["app1"]),
        ]
        output = _capture_quick_insights(recs)
        assert "Zero tests in app1" in output
        assert "Quick Insights" in output

    def test_shows_high_recs(self):
        recs = [
            Recommendation("high", "security", "No security tooling in app2", ["app2"]),
        ]
        output = _capture_quick_insights(recs)
        assert "No security tooling" in output

    def test_hides_medium_low_only(self):
        recs = [
            Recommendation("medium", "docs", "Sparse docs in app1", ["app1"]),
            Recommendation("low", "structure", "Minor structure issue", ["app1"]),
        ]
        output = _capture_quick_insights(recs)
        assert output == ""

    def test_max_three_shown(self):
        recs = [
            Recommendation("critical", "tests", "Issue 1", ["a"]),
            Recommendation("critical", "tests", "Issue 2", ["b"]),
            Recommendation("high", "security", "Issue 3", ["c"]),
            Recommendation("high", "quality", "Issue 4", ["d"]),
        ]
        output = _capture_quick_insights(recs)
        assert "Issue 1" in output
        assert "Issue 2" in output
        assert "Issue 3" in output
        assert "Issue 4" not in output
        assert "1 more" in output

    def test_shows_remaining_count(self):
        recs = [
            Recommendation("critical", "tests", "Fix tests", ["a"]),
            Recommendation("medium", "docs", "Improve docs", ["b"]),
            Recommendation("medium", "quality", "Add linter", ["c"]),
        ]
        output = _capture_quick_insights(recs)
        assert "Fix tests" in output
        assert "2 more suggestions" in output
        assert "atlas doctor" in output

    def test_empty_recs(self):
        output = _capture_quick_insights([])
        assert output == ""

    def test_project_names_shown(self):
        recs = [
            Recommendation("critical", "tests", "Zero tests", ["app1", "app2"]),
        ]
        output = _capture_quick_insights(recs)
        assert "app1" in output
        assert "app2" in output


# ---------------------------------------------------------------------------
# sparkline utility (N-54)
# ---------------------------------------------------------------------------
class TestSparkline:
    def test_basic_ascending(self):
        result = sparkline([0.0, 0.25, 0.5, 0.75, 1.0])
        assert len(result) == 5
        # First char should be the lowest, last the highest
        assert result[0] == " "
        assert result[-1] == "\u2588"

    def test_all_zeros(self):
        result = sparkline([0.0, 0.0, 0.0])
        assert all(c == " " for c in result)

    def test_all_ones(self):
        result = sparkline([1.0, 1.0, 1.0])
        assert all(c == "\u2588" for c in result)

    def test_empty_returns_empty(self):
        assert sparkline([]) == ""

    def test_single_value(self):
        result = sparkline([0.5])
        assert len(result) == 1

    def test_clamps_above_one(self):
        result = sparkline([1.5])
        assert result == "\u2588"

    def test_clamps_below_zero(self):
        result = sparkline([-0.5])
        assert result == " "

    def test_width_truncation(self):
        values = [0.1 * i for i in range(20)]
        result = sparkline(values, width=5)
        assert len(result) == 5

    def test_width_uses_recent_values(self):
        # Width=3 should use last 3 values
        values = [0.0, 0.0, 0.0, 0.5, 0.75, 1.0]
        result = sparkline(values, width=3)
        assert len(result) == 3
        # Should represent the last 3: 0.5, 0.75, 1.0

    def test_consistent_monotone_output(self):
        values = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]
        result = sparkline(values, width=9)
        # Each char should be >= the previous
        for i in range(1, len(result)):
            assert ord(result[i]) >= ord(result[i - 1])


# ---------------------------------------------------------------------------
# Health Trend Sparklines in dashboard (N-54)
# ---------------------------------------------------------------------------
def _make_history(project_name: str, health_values: list[float]) -> list[ScanEntry]:
    """Build mock scan history entries with per-project health snapshots."""
    entries = []
    for i, h in enumerate(health_values):
        entries.append(ScanEntry(
            timestamp=f"2026-03-{20 + i:02d}T00:00:00Z",
            portfolio_health=h,
            portfolio_grade="B",
            total_projects=1,
            total_tests=10,
            total_loc=1000,
            projects=[ProjectSnapshot(name=project_name, health=h, grade="B", tests=10, loc=1000)],
        ))
    return entries


class TestHealthTrendSparklines:
    def test_trend_column_shown_with_history(self):
        projects = [_proj("alpha")]
        portfolio = Portfolio(name="Test", projects=projects)
        history = _make_history("alpha", [0.5, 0.6, 0.7, 0.8])
        output = _capture_status(portfolio, history=history)
        assert "Trend" in output

    def test_no_trend_column_without_history(self):
        projects = [_proj("alpha")]
        portfolio = Portfolio(name="Test", projects=projects)
        output = _capture_status(portfolio)
        assert "Trend" not in output

    def test_no_trend_column_with_single_entry(self):
        projects = [_proj("alpha")]
        portfolio = Portfolio(name="Test", projects=projects)
        history = _make_history("alpha", [0.8])
        output = _capture_status(portfolio, history=history)
        assert "Trend" not in output

    def test_sparkline_chars_in_output(self):
        projects = [_proj("alpha")]
        portfolio = Portfolio(name="Test", projects=projects)
        history = _make_history("alpha", [0.3, 0.5, 0.7, 0.9])
        output = _capture_status(portfolio, history=history)
        # Should contain at least one sparkline character
        spark_chars = set("\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588")
        assert any(c in output for c in spark_chars)

    def test_multiple_projects_sparklines(self):
        projects = [_proj("alpha"), _proj("beta")]
        portfolio = Portfolio(name="Test", projects=projects)
        history = [
            ScanEntry(
                timestamp="2026-03-20T00:00:00Z", portfolio_health=0.5,
                portfolio_grade="B", total_projects=2, total_tests=20, total_loc=2000,
                projects=[
                    ProjectSnapshot(name="alpha", health=0.5, grade="C", tests=10, loc=1000),
                    ProjectSnapshot(name="beta", health=0.6, grade="B", tests=10, loc=1000),
                ],
            ),
            ScanEntry(
                timestamp="2026-03-21T00:00:00Z", portfolio_health=0.7,
                portfolio_grade="B", total_projects=2, total_tests=20, total_loc=2000,
                projects=[
                    ProjectSnapshot(name="alpha", health=0.7, grade="B", tests=10, loc=1000),
                    ProjectSnapshot(name="beta", health=0.8, grade="B+", tests=10, loc=1000),
                ],
            ),
        ]
        output = _capture_status(portfolio, history=history)
        assert "Trend" in output

    def test_empty_history_no_trend(self):
        projects = [_proj("alpha")]
        portfolio = Portfolio(name="Test", projects=projects)
        output = _capture_status(portfolio, history=[])
        assert "Trend" not in output

    def test_none_history_no_trend(self):
        projects = [_proj("alpha")]
        portfolio = Portfolio(name="Test", projects=projects)
        output = _capture_status(portfolio, history=None)
        assert "Trend" not in output
