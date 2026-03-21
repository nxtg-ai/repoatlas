"""CLI integration tests — every user-facing command."""
from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from atlas.cli import app, generate_badges
from atlas.models import GitInfo, HealthScore, Portfolio, Project, TechStack

runner = CliRunner()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_project(name: str = "test-proj", path: str = "/tmp/test-proj") -> Project:
    """Create a minimal Project for testing."""
    hs = HealthScore(tests=0.8, git_hygiene=0.9, documentation=0.7, structure=0.8)
    hs.compute()
    return Project(
        name=name,
        path=path,
        tech_stack=TechStack(languages={"Python": 10}, frameworks=["FastAPI"]),
        git_info=GitInfo(branch="main", total_commits=50, has_remote=True),
        health=hs,
        test_file_count=5,
        source_file_count=20,
        total_file_count=30,
        loc=1000,
    )


@pytest.fixture()
def portfolio_dir(tmp_path):
    """Patch DEFAULT_PORTFOLIO_FILE and DEFAULT_PORTFOLIO_DIR to use tmp_path."""
    pf = tmp_path / "portfolio.json"
    pd = tmp_path
    with patch("atlas.cli.DEFAULT_PORTFOLIO_FILE", pf), \
         patch("atlas.cli.DEFAULT_PORTFOLIO_DIR", pd):
        yield tmp_path, pf


# ===========================================================================
# atlas init
# ===========================================================================


class TestInit:
    def test_init_creates_portfolio(self, portfolio_dir):
        tmp_path, pf = portfolio_dir
        result = runner.invoke(app, ["init", "--name", "Test Portfolio"])
        assert result.exit_code == 0
        assert "Test Portfolio" in result.output
        assert pf.exists()
        data = json.loads(pf.read_text())
        assert data["name"] == "Test Portfolio"

    def test_init_default_name(self, portfolio_dir):
        tmp_path, pf = portfolio_dir
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        data = json.loads(pf.read_text())
        assert data["name"] == "My Portfolio"

    def test_init_already_exists(self, portfolio_dir):
        tmp_path, pf = portfolio_dir
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "already exists" in result.output


# ===========================================================================
# atlas add
# ===========================================================================


class TestAdd:
    def test_add_project(self, portfolio_dir, tmp_path):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        proj = _make_project("myproject", str(project_dir))
        with patch("atlas.cli.scan_project", return_value=proj):
            result = runner.invoke(app, ["add", str(project_dir)])
        assert result.exit_code == 0
        assert "myproject" in result.output
        data = json.loads(pf.read_text())
        assert len(data["projects"]) == 1

    def test_add_nonexistent_dir(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["add", "/nonexistent/path/xyz"])
        assert result.exit_code == 1

    def test_add_duplicate(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        proj = _make_project("myproject", str(project_dir.resolve()))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(project_dir)])
            result = runner.invoke(app, ["add", str(project_dir)])
        assert "already in portfolio" in result.output

    def test_add_no_portfolio(self, portfolio_dir, tmp_path):
        project_dir = tmp_path / "proj"
        project_dir.mkdir()
        result = runner.invoke(app, ["add", str(project_dir)])
        assert result.exit_code == 1

    def test_add_custom_name(self, portfolio_dir, tmp_path):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        project_dir = tmp_path / "myproject"
        project_dir.mkdir()
        proj = _make_project("myproject", str(project_dir))
        with patch("atlas.cli.scan_project", return_value=proj):
            result = runner.invoke(app, ["add", str(project_dir), "--name", "Custom Name"])
        assert result.exit_code == 0
        data = json.loads(pf.read_text())
        assert data["projects"][0]["name"] == "Custom Name"


# ===========================================================================
# atlas scan
# ===========================================================================


class TestScan:
    def test_scan_updates_projects(self, portfolio_dir, tmp_path):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        project_dir = tmp_path / "proj"
        project_dir.mkdir()
        proj = _make_project("proj", str(project_dir))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(project_dir)])
        updated = _make_project("proj", str(project_dir))
        updated.loc = 2000
        with patch("atlas.cli.scan_project", return_value=updated):
            result = runner.invoke(app, ["scan"])
        assert result.exit_code == 0
        data = json.loads(pf.read_text())
        assert data["projects"][0]["loc"] == 2000
        assert data["last_scan"] is not None

    def test_scan_empty_portfolio(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["scan"])
        assert "No projects" in result.output

    def test_scan_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["scan"])
        assert result.exit_code == 1


# ===========================================================================
# atlas status
# ===========================================================================


class TestStatus:
    def test_status_shows_dashboard(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init", "--name", "Test"])
        project_dir = tmp_path / "proj"
        project_dir.mkdir()
        proj = _make_project("proj", str(project_dir))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(project_dir)])
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "proj" in result.output

    def test_status_empty_portfolio(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["status"])
        assert "No projects" in result.output

    def test_status_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 1


# ===========================================================================
# atlas connections
# ===========================================================================


class TestConnections:
    def test_connections_with_projects(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        for name in ("proj-a", "proj-b"):
            d = tmp_path / name
            d.mkdir()
            proj = _make_project(name, str(d))
            with patch("atlas.cli.scan_project", return_value=proj):
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections"])
        assert result.exit_code == 0

    def test_connections_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["connections"])
        assert result.exit_code == 1

    def test_connections_type_filter(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        for name in ("proj-a", "proj-b"):
            d = tmp_path / name
            d.mkdir()
            proj = _make_project(name, str(d))
            with patch("atlas.cli.scan_project", return_value=proj):
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "--type", "deps"])
        assert result.exit_code == 0
        assert "Filtered" in result.output

    def test_connections_type_filter_short_flag(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        for name in ("proj-a", "proj-b"):
            d = tmp_path / name
            d.mkdir()
            proj = _make_project(name, str(d))
            with patch("atlas.cli.scan_project", return_value=proj):
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "-t", "security"])
        assert result.exit_code == 0
        assert "Filtered" in result.output

    def test_connections_invalid_type(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "--type", "bogus"])
        assert result.exit_code == 1
        assert "Unknown category" in result.output

    def test_connections_no_filter_shows_all(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        for name in ("proj-a", "proj-b"):
            d = tmp_path / name
            d.mkdir()
            proj = _make_project(name, str(d))
            with patch("atlas.cli.scan_project", return_value=proj):
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections"])
        assert result.exit_code == 0
        assert "Filtered" not in result.output

    def test_connections_all_categories_valid(self, portfolio_dir, tmp_path):
        from atlas.cli import CONNECTION_CATEGORIES
        runner.invoke(app, ["init"])
        for name in ("proj-a", "proj-b"):
            d = tmp_path / name
            d.mkdir()
            proj = _make_project(name, str(d))
            with patch("atlas.cli.scan_project", return_value=proj):
                runner.invoke(app, ["add", str(d)])
        for cat in CONNECTION_CATEGORIES:
            result = runner.invoke(app, ["connections", "--type", cat])
            assert result.exit_code == 0, f"Category '{cat}' failed"

    def test_connections_type_list(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "--type", "list"])
        assert result.exit_code == 0
        assert "Available connection categories" in result.output
        assert "deps" in result.output
        assert "security" in result.output
        assert "css" in result.output
        assert "state_mgmt" in result.output

    def test_connections_type_list_shows_count(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "--type", "list"])
        assert result.exit_code == 0
        assert "28 categories" in result.output

    def test_connections_type_list_shows_types(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "--type", "list"])
        assert result.exit_code == 0
        # Each category should show its connection types
        assert "shared_dep" in result.output
        assert "shared_css" in result.output

    def test_connections_type_list_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["connections", "--type", "list"])
        assert result.exit_code == 1

    def test_connections_severity_filter(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "--severity", "warning"])
        assert result.exit_code == 0
        assert "severity: warning" in result.output

    def test_connections_severity_invalid(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "--severity", "high"])
        assert result.exit_code == 1
        assert "Unknown severity" in result.output

    def test_connections_severity_info(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["connections", "--severity", "info"])
        assert result.exit_code == 0
        assert "severity: info" in result.output


# ===========================================================================
# atlas search
# ===========================================================================


class TestSearch:
    def test_search_by_name(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "myproject"
        d.mkdir()
        proj = _make_project("myproject", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["search", "myproject"])
        assert result.exit_code == 0
        assert "myproject" in result.output
        assert "1 project" in result.output

    def test_search_no_match(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["search", "nonexistent"])
        assert result.exit_code == 0
        assert "No projects match" in result.output

    def test_search_empty_portfolio(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["search", "test"])
        assert "No projects" in result.output

    def test_search_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["search", "test"])
        assert result.exit_code == 1


# ===========================================================================
# atlas doctor
# ===========================================================================


class TestDoctor:
    def test_doctor_with_healthy_project(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0

    def test_doctor_empty_portfolio(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["doctor"])
        assert "No projects" in result.output

    def test_doctor_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 1

    def test_doctor_shows_recommendations(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "bad-proj"
        d.mkdir()
        # Create a project with poor health
        from atlas.models import HealthScore as HS
        hs = HS(tests=0.0, git_hygiene=0.3, documentation=0.1, structure=0.2)
        hs.compute()
        proj = Project(
            name="bad-proj", path=str(d),
            tech_stack=TechStack(languages={"Python": 10}),
            git_info=GitInfo(branch="main", total_commits=10, has_remote=False, uncommitted_changes=60),
            health=hs, test_file_count=0, source_file_count=30, total_file_count=30, loc=2000,
        )
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        assert "recommendation" in result.output.lower()
        assert "CRITICAL" in result.output

    def test_doctor_shows_category_summary(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "bad-proj"
        d.mkdir()
        from atlas.models import HealthScore as HS
        hs = HS(tests=0.0, git_hygiene=0.3, documentation=0.1, structure=0.2)
        hs.compute()
        proj = Project(
            name="bad-proj", path=str(d),
            tech_stack=TechStack(languages={"Python": 10}),
            git_info=GitInfo(branch="main", total_commits=10, has_remote=False, uncommitted_changes=60),
            health=hs, test_file_count=0, source_file_count=30, total_file_count=30, loc=2000,
        )
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        assert "Categories:" in result.output

    def test_doctor_category_summary_counts(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        from atlas.models import HealthScore as HS
        hs = HS(tests=0.0, git_hygiene=0.0, documentation=0.0, structure=0.0)
        hs.compute()
        proj = Project(
            name="proj", path=str(d),
            tech_stack=TechStack(languages={"Python": 10}),
            git_info=GitInfo(branch="main", total_commits=0, has_remote=False, uncommitted_changes=100),
            health=hs, test_file_count=0, source_file_count=50, total_file_count=50, loc=3000,
        )
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        # Should show category names in summary
        out = result.output
        assert "Categories:" in out
        # At least one category should appear with a count
        import re
        cat_match = re.search(r"Categories:\s*(.+)", out)
        assert cat_match is not None
        cat_text = cat_match.group(1)
        # Format is "N category, M category, ..."
        assert re.search(r"\d+\s+\w+", cat_text) is not None

    def test_doctor_healthy_no_category_summary(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        # Empty portfolio = no recs = no category summary
        assert "Categories:" not in result.output


# ===========================================================================
# atlas ci
# ===========================================================================


class TestCi:
    def _setup_portfolio_with_project(self, portfolio_dir, tmp_path, health=0.8):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        hs = HealthScore(tests=health, git_hygiene=health, documentation=health, structure=health)
        hs.compute()
        proj = Project(
            name="proj", path=str(d),
            tech_stack=TechStack(languages={"Python": 10}),
            git_info=GitInfo(branch="main", total_commits=50, has_remote=True),
            health=hs, test_file_count=5, source_file_count=20, total_file_count=30, loc=1000,
        )
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        return proj

    def test_ci_json_pass(self, portfolio_dir, tmp_path):
        proj = self._setup_portfolio_with_project(portfolio_dir, tmp_path)
        with patch("atlas.cli.scan_project", return_value=proj):
            result = runner.invoke(app, ["ci"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "pass"
        assert data["portfolio"]["health"] == 80
        assert len(data["projects"]) == 1

    def test_ci_json_fail_portfolio_health(self, portfolio_dir, tmp_path):
        proj = self._setup_portfolio_with_project(portfolio_dir, tmp_path, health=0.5)
        with patch("atlas.cli.scan_project", return_value=proj):
            result = runner.invoke(app, ["ci", "--min-health", "70"])
        assert result.exit_code == 1
        data = json.loads(result.output)
        assert data["status"] == "fail"
        assert len(data["violations"]) >= 1
        assert data["violations"][0]["type"] == "portfolio_health"

    def test_ci_json_fail_project_health(self, portfolio_dir, tmp_path):
        proj = self._setup_portfolio_with_project(portfolio_dir, tmp_path, health=0.4)
        with patch("atlas.cli.scan_project", return_value=proj):
            result = runner.invoke(app, ["ci", "--min-project-health", "60"])
        assert result.exit_code == 1
        data = json.loads(result.output)
        assert data["status"] == "fail"
        assert any(v["type"] == "project_health" for v in data["violations"])

    def test_ci_summary_format(self, portfolio_dir, tmp_path):
        proj = self._setup_portfolio_with_project(portfolio_dir, tmp_path)
        with patch("atlas.cli.scan_project", return_value=proj):
            result = runner.invoke(app, ["ci", "--format", "summary"])
        assert result.exit_code == 0
        assert "PASS" in result.output

    def test_ci_no_projects(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["ci"])
        assert result.exit_code == 1

    def test_ci_pass_with_thresholds_met(self, portfolio_dir, tmp_path):
        proj = self._setup_portfolio_with_project(portfolio_dir, tmp_path, health=0.9)
        with patch("atlas.cli.scan_project", return_value=proj):
            result = runner.invoke(app, ["ci", "--min-health", "80", "--min-project-health", "80"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["status"] == "pass"
        assert data["violations"] == []


# ===========================================================================
# atlas inspect
# ===========================================================================


class TestInspect:
    def test_inspect_existing(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["inspect", "proj"])
        assert result.exit_code == 0
        assert "proj" in result.output

    def test_inspect_not_found(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["inspect", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_inspect_case_insensitive(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "MyProject"
        d.mkdir()
        proj = _make_project("MyProject", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["inspect", "myproject"])
        assert result.exit_code == 0


# ===========================================================================
# atlas compare
# ===========================================================================


class TestCompare:
    def _add_two_projects(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        da = tmp_path / "proj-a"
        db = tmp_path / "proj-b"
        da.mkdir()
        db.mkdir()
        proj_a = _make_project("proj-a", str(da))
        # Give proj-b different health
        hs_b = HealthScore(tests=0.5, git_hygiene=0.6, documentation=0.4, structure=0.5)
        hs_b.compute()
        proj_b = Project(
            name="proj-b", path=str(db),
            tech_stack=TechStack(languages={"TypeScript": 20}, frameworks=["React"]),
            git_info=GitInfo(branch="main", total_commits=30, has_remote=True),
            health=hs_b, test_file_count=2, source_file_count=15, total_file_count=20, loc=800,
        )
        call_count = {"n": 0}
        def mock_scan(path):
            call_count["n"] += 1
            if "proj-a" in str(path):
                return proj_a
            return proj_b
        with patch("atlas.cli.scan_project", side_effect=mock_scan):
            runner.invoke(app, ["add", str(da)])
            runner.invoke(app, ["add", str(db)])

    def test_compare_two_projects(self, portfolio_dir, tmp_path):
        self._add_two_projects(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["compare", "proj-a", "proj-b"])
        assert result.exit_code == 0
        assert "proj-a" in result.output
        assert "proj-b" in result.output
        assert "Comparison" in result.output

    def test_compare_not_found(self, portfolio_dir, tmp_path):
        self._add_two_projects(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["compare", "proj-a", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_compare_same_project(self, portfolio_dir, tmp_path):
        self._add_two_projects(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["compare", "proj-a", "proj-a"])
        assert result.exit_code == 1
        assert "itself" in result.output

    def test_compare_shows_insights(self, portfolio_dir, tmp_path):
        self._add_two_projects(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["compare", "proj-a", "proj-b"])
        assert result.exit_code == 0
        assert "Insights" in result.output

    def test_compare_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["compare", "a", "b"])
        assert result.exit_code == 1


# ===========================================================================
# atlas remove
# ===========================================================================


class TestRemove:
    def test_remove_existing(self, portfolio_dir, tmp_path):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["remove", "proj"])
        assert result.exit_code == 0
        assert "Removed" in result.output
        data = json.loads(pf.read_text())
        assert len(data["projects"]) == 0

    def test_remove_not_found(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["remove", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output


# ===========================================================================
# atlas batch-add
# ===========================================================================


class TestBatchAdd:
    def test_batch_add_finds_repos(self, portfolio_dir, tmp_path):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        parent = tmp_path / "repos"
        parent.mkdir()
        for name in ("repo-a", "repo-b"):
            d = parent / name
            d.mkdir()
            (d / ".git").mkdir()
        proj_a = _make_project("repo-a", str(parent / "repo-a"))
        proj_b = _make_project("repo-b", str(parent / "repo-b"))
        call_count = {"n": 0}
        def mock_scan(path):
            call_count["n"] += 1
            if "repo-a" in str(path):
                return proj_a
            return proj_b
        with patch("atlas.cli.scan_project", side_effect=mock_scan):
            result = runner.invoke(app, ["batch-add", str(parent)])
        assert result.exit_code == 0
        assert "2" in result.output
        data = json.loads(pf.read_text())
        assert len(data["projects"]) == 2

    def test_batch_add_skips_dotdirs(self, portfolio_dir, tmp_path):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        parent = tmp_path / "repos"
        parent.mkdir()
        (parent / ".hidden").mkdir()
        (parent / ".hidden" / ".git").mkdir()
        (parent / "_private").mkdir()
        (parent / "_private" / ".git").mkdir()
        result = runner.invoke(app, ["batch-add", str(parent)])
        assert "No new git repos" in result.output

    def test_batch_add_exclude(self, portfolio_dir, tmp_path):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        parent = tmp_path / "repos"
        parent.mkdir()
        for name in ("keep", "skip"):
            d = parent / name
            d.mkdir()
            (d / ".git").mkdir()
        proj = _make_project("keep", str(parent / "keep"))
        with patch("atlas.cli.scan_project", return_value=proj):
            result = runner.invoke(app, ["batch-add", str(parent), "--exclude", "skip"])
        assert result.exit_code == 0
        data = json.loads(pf.read_text())
        assert len(data["projects"]) == 1

    def test_batch_add_nonexistent_dir(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["batch-add", "/nonexistent/dir"])
        assert result.exit_code == 1


# ===========================================================================
# atlas export
# ===========================================================================


class TestExport:
    def _setup_portfolio(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init", "--name", "Export Test"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])

    def test_export_markdown(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["export"])
        assert result.exit_code == 0
        assert "Portfolio Report" in result.output
        assert "proj" in result.output

    def test_export_json(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["export", "--format", "json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["name"] == "Export Test"
        assert len(data["projects"]) == 1

    def test_export_to_file(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "report.md"
        result = runner.invoke(app, ["export", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        assert "Portfolio Report" in out.read_text()

    def test_export_csv(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["export", "--format", "csv"])
        assert result.exit_code == 0
        assert "Name" in result.output
        assert "proj" in result.output

    def test_export_csv_to_file(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "report.csv"
        result = runner.invoke(app, ["export", "--format", "csv", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        content = out.read_text()
        assert "Name" in content
        assert "proj" in content

    def test_auto_detect_json(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "report.json"
        result = runner.invoke(app, ["export", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["name"] == "Export Test"

    def test_auto_detect_csv(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "report.csv"
        result = runner.invoke(app, ["export", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        content = out.read_text()
        assert "Name" in content
        assert "proj" in content

    def test_auto_detect_md(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "report.md"
        result = runner.invoke(app, ["export", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        assert "Portfolio Report" in out.read_text()

    def test_auto_detect_unknown_ext_defaults_markdown(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "report.txt"
        result = runner.invoke(app, ["export", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        assert "Portfolio Report" in out.read_text()

    def test_explicit_format_overrides_extension(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "report.md"
        result = runner.invoke(app, ["export", "--format", "json", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        data = json.loads(out.read_text())
        assert "name" in data

    def test_no_output_no_format_defaults_markdown(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["export"])
        assert result.exit_code == 0
        assert "Portfolio Report" in result.output

    def test_output_shows_format_in_message(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "report.json"
        result = runner.invoke(app, ["export", "-o", str(out)])
        assert "(json)" in result.output


# ===========================================================================
# atlas config
# ===========================================================================


class TestConfig:
    def test_config_show_all(self, portfolio_dir, tmp_path):
        with patch("atlas.cli.load_config", return_value={
            "ci": {"min_health": 0, "min_project_health": 0},
            "export": {"format": "markdown"},
        }), patch("atlas.cli.valid_keys", return_value=["ci.min_health"]):
            result = runner.invoke(app, ["config"])
        assert result.exit_code == 0
        assert "min_health" in result.output

    def test_config_get_key(self, portfolio_dir):
        with patch("atlas.cli.get_value", return_value=0):
            result = runner.invoke(app, ["config", "ci.min_health"])
        assert result.exit_code == 0
        assert "ci.min_health" in result.output

    def test_config_get_unknown(self, portfolio_dir):
        with patch("atlas.cli.get_value", return_value=None):
            result = runner.invoke(app, ["config", "bogus.key"])
        assert result.exit_code == 1
        assert "Unknown" in result.output

    def test_config_set_value(self, portfolio_dir):
        with patch("atlas.cli.set_value", return_value=True):
            result = runner.invoke(app, ["config", "ci.min_health", "--set", "70"])
        assert result.exit_code == 0
        assert "70" in result.output

    def test_config_set_invalid(self, portfolio_dir):
        with patch("atlas.cli.set_value", return_value=False):
            result = runner.invoke(app, ["config", "bogus.key", "--set", "val"])
        assert result.exit_code == 1
        assert "Invalid" in result.output


# ===========================================================================
# atlas license
# ===========================================================================


class TestLicenseCmd:
    def test_license_free_tier(self, portfolio_dir):
        with patch("atlas.cli.get_license_status", return_value={
            "tier": "Free", "project_limit": "3",
            "cross_project": False, "export": False, "batch_add": False,
        }):
            result = runner.invoke(app, ["license"])
        assert result.exit_code == 0
        assert "Free" in result.output

    def test_license_pro_tier(self, portfolio_dir):
        with patch("atlas.cli.get_license_status", return_value={
            "tier": "Pro", "project_limit": "Unlimited",
            "cross_project": True, "export": True, "batch_add": True,
        }):
            result = runner.invoke(app, ["license"])
        assert result.exit_code == 0
        assert "Pro" in result.output
        assert "Unlimited" in result.output


# ===========================================================================
# atlas activate
# ===========================================================================


class TestActivateCmd:
    def test_activate_valid_key(self, portfolio_dir):
        with patch("atlas.cli.activate_license", return_value=True):
            result = runner.invoke(app, ["activate", "ATLAS-TEST-KEY1-KEY2-ABCD"])
        assert result.exit_code == 0
        assert "activated" in result.output

    def test_activate_invalid_key(self, portfolio_dir):
        with patch("atlas.cli.activate_license", return_value=False):
            result = runner.invoke(app, ["activate", "BAD-KEY"])
        assert result.exit_code == 1
        assert "Invalid" in result.output


# ===========================================================================
# atlas support
# ===========================================================================


class TestSupport:
    def test_support_output(self, portfolio_dir):
        result = runner.invoke(app, ["support"])
        assert result.exit_code == 0
        assert "free" in result.output.lower()
        assert "sponsors" in result.output


# ===========================================================================
# atlas reset
# ===========================================================================


class TestReset:
    def test_reset_confirms_and_deletes(self, portfolio_dir):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        assert pf.exists()
        result = runner.invoke(app, ["reset"], input="y\n")
        assert result.exit_code == 0
        assert not pf.exists()

    def test_reset_cancel(self, portfolio_dir):
        _, pf = portfolio_dir
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["reset"], input="n\n")
        assert result.exit_code == 0
        assert pf.exists()
        assert "Cancelled" in result.output

    def test_reset_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["reset"])
        assert result.exit_code == 0
        assert "No portfolio" in result.output


# ===========================================================================
# atlas trends
# ===========================================================================


class TestTrends:
    def test_trends_no_history(self, portfolio_dir):
        with patch("atlas.cli.load_history", return_value=[]):
            result = runner.invoke(app, ["trends"])
        assert result.exit_code == 0
        assert "No scan history" in result.output

    def test_trends_single_scan(self, portfolio_dir):
        from atlas.history import ProjectSnapshot, ScanEntry
        entry = ScanEntry(
            timestamp="2026-03-13T00:00:00+00:00",
            portfolio_health=0.8, portfolio_grade="B+",
            total_projects=1, total_tests=5, total_loc=1000,
            projects=[ProjectSnapshot("proj", 0.8, "B+", 5, 1000)],
        )
        with patch("atlas.cli.load_history", return_value=[entry]):
            result = runner.invoke(app, ["trends"])
        assert result.exit_code == 0
        assert "Need at least 2 scans" in result.output

    def test_trends_shows_changes(self, portfolio_dir):
        from atlas.history import ProjectSnapshot, ScanEntry
        prev = ScanEntry(
            timestamp="2026-03-12T00:00:00+00:00",
            portfolio_health=0.7, portfolio_grade="B",
            total_projects=1, total_tests=3, total_loc=800,
            projects=[ProjectSnapshot("proj", 0.7, "B", 3, 800)],
        )
        curr = ScanEntry(
            timestamp="2026-03-13T00:00:00+00:00",
            portfolio_health=0.9, portfolio_grade="A",
            total_projects=1, total_tests=10, total_loc=1200,
            projects=[ProjectSnapshot("proj", 0.9, "A", 10, 1200)],
        )
        with patch("atlas.cli.load_history", return_value=[prev, curr]):
            result = runner.invoke(app, ["trends"])
        assert result.exit_code == 0
        assert "Portfolio Trends" in result.output
        assert "proj" in result.output
        assert "2 scans" in result.output


# ===========================================================================
# atlas status --filter
# ===========================================================================


def _make_varied_project(name, path, grade="B", lang="Python", framework="FastAPI",
                         health_pct=0.8) -> Project:
    """Create a Project with configurable health and tech for filter tests."""
    hs = HealthScore(tests=health_pct, git_hygiene=health_pct,
                     documentation=health_pct, structure=health_pct)
    hs.compute()
    return Project(
        name=name,
        path=path,
        tech_stack=TechStack(
            languages={lang: 10},
            frameworks=[framework] if framework else [],
            infrastructure=["Docker"],
        ),
        git_info=GitInfo(branch="main", total_commits=10),
        health=hs,
        test_file_count=5,
        source_file_count=20,
        loc=500,
    )


class TestStatusFilters:
    def test_filter_by_grade(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        p1 = _make_varied_project("good", str(tmp_path / "good"), health_pct=0.95)
        p2 = _make_varied_project("bad", str(tmp_path / "bad"), health_pct=0.3)
        with patch("atlas.cli.scan_project", side_effect=[p1, p2]):
            for name in ("good", "bad"):
                d = tmp_path / name
                d.mkdir(exist_ok=True)
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["status", "--grade", "A"])
        assert result.exit_code == 0
        assert "good" in result.output
        assert "Filtered" in result.output

    def test_filter_by_lang(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        p1 = _make_varied_project("pyproj", str(tmp_path / "pyproj"), lang="Python")
        p2 = _make_varied_project("tsproj", str(tmp_path / "tsproj"), lang="TypeScript")
        with patch("atlas.cli.scan_project", side_effect=[p1, p2]):
            for name in ("pyproj", "tsproj"):
                d = tmp_path / name
                d.mkdir(exist_ok=True)
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["status", "--lang", "TypeScript"])
        assert result.exit_code == 0
        assert "tsproj" in result.output
        assert "Filtered" in result.output

    def test_filter_by_has(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        p1 = _make_varied_project("api", str(tmp_path / "api"), framework="FastAPI")
        p2 = _make_varied_project("web", str(tmp_path / "web"), framework="React")
        with patch("atlas.cli.scan_project", side_effect=[p1, p2]):
            for name in ("api", "web"):
                d = tmp_path / name
                d.mkdir(exist_ok=True)
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["status", "--has", "FastAPI"])
        assert result.exit_code == 0
        assert "api" in result.output
        assert "Filtered" in result.output

    def test_filter_by_min_health(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        p1 = _make_varied_project("good", str(tmp_path / "good"), health_pct=0.95)
        p2 = _make_varied_project("bad", str(tmp_path / "bad"), health_pct=0.3)
        with patch("atlas.cli.scan_project", side_effect=[p1, p2]):
            for name in ("good", "bad"):
                d = tmp_path / name
                d.mkdir(exist_ok=True)
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["status", "--min-health", "80"])
        assert result.exit_code == 0
        assert "good" in result.output
        assert "Filtered" in result.output

    def test_filter_no_match(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        p1 = _make_varied_project("proj", str(tmp_path / "proj"))
        with patch("atlas.cli.scan_project", return_value=p1):
            d = tmp_path / "proj"
            d.mkdir(exist_ok=True)
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["status", "--lang", "Haskell"])
        assert result.exit_code == 0
        assert "No projects match" in result.output

    def test_no_filter_shows_all(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        p1 = _make_varied_project("a", str(tmp_path / "a"))
        p2 = _make_varied_project("b", str(tmp_path / "b"))
        with patch("atlas.cli.scan_project", side_effect=[p1, p2]):
            for name in ("a", "b"):
                d = tmp_path / name
                d.mkdir(exist_ok=True)
                runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "a" in result.output
        assert "b" in result.output
        assert "Filtered" not in result.output


# ===========================================================================
# atlas status — quick insights
# ===========================================================================


class TestQuickInsights:
    def test_status_shows_quick_insights_for_unhealthy(self, portfolio_dir, tmp_path):
        """Projects missing security/quality tools should trigger quick insights."""
        runner.invoke(app, ["init"])
        # No security_tools, no quality_tools → recommendations generated
        proj = _make_project("app1", str(tmp_path / "app1"))
        with patch("atlas.cli.scan_project", return_value=proj):
            d = tmp_path / "app1"
            d.mkdir()
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Quick Insights" in result.output

    def test_status_hides_quick_insights_when_healthy(self, portfolio_dir, tmp_path):
        """Fully healthy project should not show quick insights."""
        runner.invoke(app, ["init"])
        hs = HealthScore(tests=0.9, git_hygiene=1.0, documentation=0.8, structure=0.9)
        hs.compute()
        proj = Project(
            name="healthy",
            path=str(tmp_path / "healthy"),
            tech_stack=TechStack(
                languages={"Python": 10},
                frameworks=["FastAPI"],
                security_tools=["Dependabot", "Gitleaks"],
                quality_tools=["Ruff", "mypy"],
                infrastructure=["GitHub Actions"],
                testing_frameworks=["pytest"],
                docs_artifacts=["README", "CHANGELOG", "CONTRIBUTING"],
                ci_config=["PR template", "pre-commit"],
            ),
            git_info=GitInfo(branch="main", total_commits=50, has_remote=True),
            health=hs,
            test_file_count=10,
            source_file_count=15,
            loc=1000,
            license="MIT",
        )
        with patch("atlas.cli.scan_project", return_value=proj):
            d = tmp_path / "healthy"
            d.mkdir()
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["status"])
        assert result.exit_code == 0
        assert "Quick Insights" not in result.output


# ===========================================================================
# atlas badge (N-57)
# ===========================================================================


class TestBadge:
    def _setup_portfolio(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init", "--name", "Badge Test"])
        d = tmp_path / "proj"
        d.mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])

    def test_badge_output(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["badge"])
        assert result.exit_code == 0
        assert "img.shields.io" in result.output
        assert "health" in result.output
        assert "projects" in result.output

    def test_badge_contains_health_grade(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["badge"])
        assert "health-B" in result.output

    def test_badge_contains_test_count(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["badge"])
        assert "test%20files" in result.output

    def test_badge_contains_loc(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["badge"])
        assert "LOC" in result.output

    def test_badge_contains_language(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        result = runner.invoke(app, ["badge"])
        assert "Python" in result.output

    def test_badge_to_file(self, portfolio_dir, tmp_path):
        self._setup_portfolio(portfolio_dir, tmp_path)
        out = tmp_path / "badges.md"
        result = runner.invoke(app, ["badge", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        content = out.read_text()
        assert "img.shields.io" in content
        assert "health" in content

    def test_badge_no_portfolio(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["badge"])
        assert result.exit_code == 1


# ===========================================================================
# generate_badges unit tests (N-57)
# ===========================================================================


class TestGenerateBadges:
    def _portfolio(self, *projects) -> Portfolio:
        return Portfolio(name="Test", projects=list(projects))

    def test_returns_list_of_strings(self):
        proj = _make_project()
        badges = generate_badges(self._portfolio(proj))
        assert isinstance(badges, list)
        assert all(isinstance(b, str) for b in badges)

    def test_all_badges_are_markdown_images(self):
        proj = _make_project()
        badges = generate_badges(self._portfolio(proj))
        assert all(b.startswith("![") for b in badges)

    def test_health_grade_a(self):
        hs = HealthScore(tests=1.0, git_hygiene=1.0, documentation=1.0, structure=1.0)
        hs.compute()
        proj = _make_project()
        proj.health = hs
        badges = generate_badges(self._portfolio(proj))
        health_badge = [b for b in badges if "health" in b][0]
        assert "health-A" in health_badge
        assert "brightgreen" in health_badge

    def test_health_grade_f(self):
        hs = HealthScore(tests=0.0, git_hygiene=0.0, documentation=0.0, structure=0.0)
        hs.compute()
        proj = _make_project()
        proj.health = hs
        badges = generate_badges(self._portfolio(proj))
        health_badge = [b for b in badges if "health" in b][0]
        assert "health-F" in health_badge
        assert "red" in health_badge

    def test_loc_formatting_millions(self):
        proj = _make_project()
        proj.loc = 1_500_000
        badges = generate_badges(self._portfolio(proj))
        loc_badge = [b for b in badges if "LOC" in b][0]
        assert "1.5M" in loc_badge

    def test_loc_formatting_thousands(self):
        proj = _make_project()
        proj.loc = 15_000
        badges = generate_badges(self._portfolio(proj))
        loc_badge = [b for b in badges if "LOC" in b][0]
        assert "15.0K" in loc_badge

    def test_loc_formatting_small(self):
        proj = _make_project()
        proj.loc = 500
        badges = generate_badges(self._portfolio(proj))
        loc_badge = [b for b in badges if "LOC" in b][0]
        assert "500" in loc_badge

    def test_project_count(self):
        p1 = _make_project("a", "/a")
        p2 = _make_project("b", "/b")
        badges = generate_badges(self._portfolio(p1, p2))
        proj_badge = [b for b in badges if "projects" in b][0]
        assert "projects-2" in proj_badge

    def test_test_color_high(self):
        proj = _make_project()
        proj.test_file_count = 100
        badges = generate_badges(self._portfolio(proj))
        test_badge = [b for b in badges if "test" in b][0]
        assert "brightgreen" in test_badge

    def test_test_color_zero(self):
        proj = _make_project()
        proj.test_file_count = 0
        badges = generate_badges(self._portfolio(proj))
        test_badge = [b for b in badges if "test" in b][0]
        assert "red" in test_badge


# ---------------------------------------------------------------------------
# rename
# ---------------------------------------------------------------------------
class TestRename:
    def test_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["rename", "old", "new"])
        assert result.exit_code == 1

    def test_project_not_found(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["rename", "nonexistent", "new"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_rename_success(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        (d / ".git").mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["rename", "proj", "my-app"])
        assert result.exit_code == 0
        assert "my-app" in result.output
        # Verify rename persisted
        result2 = runner.invoke(app, ["inspect", "my-app"])
        assert result2.exit_code == 0

    def test_rename_collision(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d1 = tmp_path / "proj1"
        d1.mkdir()
        (d1 / ".git").mkdir()
        d2 = tmp_path / "proj2"
        d2.mkdir()
        (d2 / ".git").mkdir()
        p1 = _make_project("proj1", str(d1))
        p2 = _make_project("proj2", str(d2))
        with patch("atlas.cli.scan_project", return_value=p1):
            runner.invoke(app, ["add", str(d1)])
        with patch("atlas.cli.scan_project", return_value=p2):
            runner.invoke(app, ["add", str(d2)])
        result = runner.invoke(app, ["rename", "proj1", "proj2"])
        assert result.exit_code == 1
        assert "already in use" in result.output.lower()


# ---------------------------------------------------------------------------
# batch-remove
# ---------------------------------------------------------------------------
class TestBatchRemove:
    def test_no_portfolio(self, portfolio_dir):
        result = runner.invoke(app, ["batch-remove"])
        assert result.exit_code == 1

    def test_empty_portfolio(self, portfolio_dir):
        runner.invoke(app, ["init"])
        result = runner.invoke(app, ["batch-remove"])
        assert result.exit_code == 0
        assert "No projects" in result.output

    def test_all_exist(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        (d / ".git").mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        result = runner.invoke(app, ["batch-remove"])
        assert result.exit_code == 0
        assert "All projects still exist" in result.output

    def test_removes_stale(self, portfolio_dir, tmp_path):
        runner.invoke(app, ["init"])
        d = tmp_path / "proj"
        d.mkdir()
        (d / ".git").mkdir()
        proj = _make_project("proj", str(d))
        with patch("atlas.cli.scan_project", return_value=proj):
            runner.invoke(app, ["add", str(d)])
        # Now remove the directory to make it stale
        import shutil
        shutil.rmtree(d)
        result = runner.invoke(app, ["batch-remove"])
        assert result.exit_code == 0
        assert "Removed 1 stale project" in result.output
        # Verify it's gone
        result2 = runner.invoke(app, ["status"])
        assert "proj" not in result2.output or "No projects" in result2.output
