"""CLI integration tests — every user-facing command."""
from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from atlas.cli import app
from atlas.models import GitInfo, HealthScore, Project, TechStack

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
