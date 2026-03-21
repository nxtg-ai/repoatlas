"""Tests for health scoring."""
from __future__ import annotations


import pytest

from atlas.health import _score_docs, _score_git, _score_structure, _score_tests, compute_health
from atlas.models import GitInfo, HealthScore, Project


def _make_project(**kwargs) -> Project:
    defaults = {
        "name": "test",
        "path": "/tmp/test",
        "test_file_count": 10,
        "source_file_count": 50,
        "total_file_count": 100,
    }
    defaults.update(kwargs)
    return Project(**defaults)


# ---------------------------------------------------------------------------
# HealthScore dataclass (compute, percent, icon)
# ---------------------------------------------------------------------------
class TestHealthScore:
    def test_compute_grade_a(self):
        hs = HealthScore(tests=1.0, git_hygiene=0.9, documentation=0.9, structure=0.9)
        hs.compute()
        assert hs.grade == "A"
        assert hs.percent >= 90

    def test_compute_grade_f(self):
        hs = HealthScore(tests=0.0, git_hygiene=0.0, documentation=0.0, structure=0.0)
        hs.compute()
        assert hs.grade == "F"
        assert hs.percent == 0

    def test_compute_grade_c(self):
        hs = HealthScore(tests=0.5, git_hygiene=0.7, documentation=0.6, structure=0.7)
        hs.compute()
        assert hs.grade in ("C", "B")
        assert 55 <= hs.percent <= 75

    def test_icon_green(self):
        hs = HealthScore()
        hs.overall = 0.9
        assert "green" in hs.icon

    def test_icon_yellow(self):
        hs = HealthScore()
        hs.overall = 0.65
        assert "yellow" in hs.icon

    def test_icon_red(self):
        hs = HealthScore()
        hs.overall = 0.45
        assert "red" in hs.icon
        assert "dim" not in hs.icon

    def test_icon_dim_red(self):
        hs = HealthScore()
        hs.overall = 0.20
        assert "dim red" in hs.icon


# ---------------------------------------------------------------------------
# _score_tests — all ratio brackets
# ---------------------------------------------------------------------------
class TestScoreTests:
    def test_zero_test_files(self):
        proj = _make_project(test_file_count=0, source_file_count=50)
        assert _score_tests(proj) == 0.0

    def test_zero_source_files(self):
        proj = _make_project(test_file_count=5, source_file_count=0)
        assert _score_tests(proj) == 0.5

    def test_ratio_above_0_4(self):
        proj = _make_project(test_file_count=50, source_file_count=100)
        assert _score_tests(proj) == 1.0

    def test_ratio_0_25_to_0_4(self):
        proj = _make_project(test_file_count=30, source_file_count=100)
        assert _score_tests(proj) == 0.9

    def test_ratio_0_15_to_0_25(self):
        proj = _make_project(test_file_count=20, source_file_count=100)
        assert _score_tests(proj) == 0.8

    def test_ratio_0_08_to_0_15(self):
        proj = _make_project(test_file_count=10, source_file_count=100)
        assert _score_tests(proj) == 0.7

    def test_ratio_0_03_to_0_08(self):
        proj = _make_project(test_file_count=5, source_file_count=100)
        assert _score_tests(proj) == 0.5

    def test_ratio_below_0_03(self):
        proj = _make_project(test_file_count=1, source_file_count=100)
        assert _score_tests(proj) == 0.3

    def test_exact_boundary_0_4(self):
        proj = _make_project(test_file_count=40, source_file_count=100)
        assert _score_tests(proj) == 1.0

    def test_exact_boundary_0_25(self):
        proj = _make_project(test_file_count=25, source_file_count=100)
        assert _score_tests(proj) == 0.9


# ---------------------------------------------------------------------------
# _score_git — all conditions
# ---------------------------------------------------------------------------
class TestScoreGit:
    def test_perfect_git(self):
        proj = _make_project()
        proj.git_info = GitInfo(
            total_commits=150, has_remote=True, uncommitted_changes=0
        )
        score = _score_git(proj)
        assert score == pytest.approx(1.0)

    def test_no_commits(self):
        proj = _make_project()
        proj.git_info = GitInfo(total_commits=0, has_remote=False, uncommitted_changes=0)
        score = _score_git(proj)
        # Only gets neutral 0.1 + clean tree 0.2 = 0.3
        assert score == pytest.approx(0.3)

    def test_commits_10_to_99(self):
        proj = _make_project()
        proj.git_info = GitInfo(total_commits=50, has_remote=True, uncommitted_changes=0)
        score = _score_git(proj)
        # 0.3 (has git) + 0.2 (remote) + 0.1 (10-99 commits) + 0.2 (clean) + 0.1 (neutral)
        assert score == pytest.approx(0.9)

    def test_commits_gte_100(self):
        proj = _make_project()
        proj.git_info = GitInfo(total_commits=100, has_remote=True, uncommitted_changes=0)
        score = _score_git(proj)
        assert score == pytest.approx(1.0)

    def test_dirty_working_tree(self):
        proj = _make_project()
        proj.git_info = GitInfo(total_commits=10, has_remote=False, uncommitted_changes=10)
        score = _score_git(proj)
        # 0.3 + 0.1 (10-99) + 0.0 (dirty>=5) + 0.1
        assert score == pytest.approx(0.5)

    def test_slightly_dirty(self):
        proj = _make_project()
        proj.git_info = GitInfo(total_commits=10, has_remote=False, uncommitted_changes=3)
        score = _score_git(proj)
        # 0.3 + 0.1 + 0.1 (1-4 changes) + 0.1
        assert score == pytest.approx(0.6)

    def test_no_remote(self):
        proj = _make_project()
        proj.git_info = GitInfo(total_commits=50, has_remote=False, uncommitted_changes=0)
        score = _score_git(proj)
        # 0.3 + 0.0 (no remote) + 0.1 + 0.2 + 0.1
        assert score == pytest.approx(0.7)

    def test_capped_at_1(self):
        proj = _make_project()
        proj.git_info = GitInfo(total_commits=200, has_remote=True, uncommitted_changes=0)
        assert _score_git(proj) <= 1.0


# ---------------------------------------------------------------------------
# _score_docs — file presence
# ---------------------------------------------------------------------------
class TestScoreDocs:
    def test_readme_md(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello")
        assert _score_docs(tmp_path) == pytest.approx(0.35)

    def test_readme_rst(self, tmp_path):
        (tmp_path / "README.rst").write_text("Hello\n=====")
        assert _score_docs(tmp_path) == pytest.approx(0.35)

    def test_readme_txt(self, tmp_path):
        (tmp_path / "README.txt").write_text("Hello")
        assert _score_docs(tmp_path) == pytest.approx(0.35)

    def test_readme_no_extension(self, tmp_path):
        (tmp_path / "README").write_text("Hello")
        assert _score_docs(tmp_path) == pytest.approx(0.35)

    def test_claude_md(self, tmp_path):
        (tmp_path / "CLAUDE.md").write_text("# Instructions")
        assert _score_docs(tmp_path) == pytest.approx(0.2)

    def test_claude_dir(self, tmp_path):
        (tmp_path / ".claude").mkdir()
        assert _score_docs(tmp_path) == pytest.approx(0.2)

    def test_nexus(self, tmp_path):
        asif = tmp_path / ".asif"
        asif.mkdir()
        (asif / "NEXUS.md").write_text("# NEXUS")
        assert _score_docs(tmp_path) == pytest.approx(0.2)

    def test_docs_dir(self, tmp_path):
        (tmp_path / "docs").mkdir()
        assert _score_docs(tmp_path) == pytest.approx(0.15)

    def test_doc_dir(self, tmp_path):
        (tmp_path / "doc").mkdir()
        assert _score_docs(tmp_path) == pytest.approx(0.15)

    def test_changelog(self, tmp_path):
        (tmp_path / "CHANGELOG.md").write_text("# Changes")
        assert _score_docs(tmp_path) == pytest.approx(0.1)

    def test_changes_md(self, tmp_path):
        (tmp_path / "CHANGES.md").write_text("# Changes")
        assert _score_docs(tmp_path) == pytest.approx(0.1)

    def test_full_docs(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello")
        (tmp_path / "CLAUDE.md").write_text("# Instructions")
        asif = tmp_path / ".asif"
        asif.mkdir()
        (asif / "NEXUS.md").write_text("# NEXUS")
        (tmp_path / "docs").mkdir()
        (tmp_path / "CHANGELOG.md").write_text("# Changes")
        score = _score_docs(tmp_path)
        assert score == 1.0

    def test_empty_dir(self, tmp_path):
        assert _score_docs(tmp_path) == 0.0


# ---------------------------------------------------------------------------
# _score_structure — tooling and organization
# ---------------------------------------------------------------------------
class TestScoreStructure:
    def test_ci_workflows(self, tmp_path):
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "ci.yml").write_text("name: CI")
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        assert _score_structure(tmp_path, proj) >= 0.3

    def test_empty_workflows_dir(self, tmp_path):
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        # Empty workflows dir should NOT count
        assert _score_structure(tmp_path, proj) < 0.3

    def test_gitignore(self, tmp_path):
        (tmp_path / ".gitignore").write_text("*.pyc\n")
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.1

    def test_pyproject_toml(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.2

    def test_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text('{"name":"x"}')
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.2

    def test_cargo_toml(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[package]\nname="x"\n')
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.2

    def test_src_dir(self, tmp_path):
        (tmp_path / "src").mkdir()
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.15

    def test_lib_dir(self, tmp_path):
        (tmp_path / "lib").mkdir()
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.15

    def test_source_file_count_gte_10(self, tmp_path):
        proj = _make_project(path=str(tmp_path), source_file_count=15)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.15

    def test_source_file_count_3_to_9(self, tmp_path):
        proj = _make_project(path=str(tmp_path), source_file_count=5)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.1

    def test_source_file_count_below_3(self, tmp_path):
        proj = _make_project(path=str(tmp_path), source_file_count=1)
        # Only gets 0 from file count
        score = _score_structure(tmp_path, proj)
        assert score < 0.15

    def test_lint_config_ruff(self, tmp_path):
        (tmp_path / "ruff.toml").write_text("[tool.ruff]\n")
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.1

    def test_lint_config_eslint(self, tmp_path):
        (tmp_path / ".eslintrc.json").write_text("{}")
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.1

    def test_lint_config_biome(self, tmp_path):
        (tmp_path / "biome.json").write_text("{}")
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        score = _score_structure(tmp_path, proj)
        assert score >= 0.1

    def test_capped_at_1(self, tmp_path):
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "ci.yml").write_text("name: CI")
        (tmp_path / ".gitignore").write_text("*.pyc")
        (tmp_path / "pyproject.toml").write_text("[project]")
        (tmp_path / "src").mkdir()
        (tmp_path / "ruff.toml").write_text("[tool]")
        proj = _make_project(path=str(tmp_path), source_file_count=20)
        assert _score_structure(tmp_path, proj) == 1.0

    def test_empty_dir(self, tmp_path):
        proj = _make_project(path=str(tmp_path), source_file_count=0)
        assert _score_structure(tmp_path, proj) == 0.0


# ---------------------------------------------------------------------------
# compute_health — integration
# ---------------------------------------------------------------------------
class TestComputeHealth:
    def test_project_with_tests_scores_higher(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        proj.test_file_count = 10
        proj.source_file_count = 50
        health = compute_health(proj)
        assert health.tests > 0

    def test_project_without_tests(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        proj.test_file_count = 0
        proj.source_file_count = 50
        health = compute_health(proj)
        assert health.tests == 0.0

    def test_docs_score_with_readme(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        health = compute_health(proj)
        assert health.documentation > 0

    def test_structure_with_ci(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        health = compute_health(proj)
        assert health.structure > 0

    def test_overall_computed(self, tmp_project):
        proj = Project(name="test", path=str(tmp_project))
        proj.test_file_count = 10
        proj.source_file_count = 50
        health = compute_health(proj)
        assert health.overall > 0
        assert health.grade != "F"

    def test_empty_project(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        proj = Project(name="empty", path=str(empty), source_file_count=0, test_file_count=0)
        health = compute_health(proj)
        assert health.overall < 0.1
        assert health.grade == "F"
