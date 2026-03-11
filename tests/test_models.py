"""Tests for data models — TechStack, GitInfo, HealthScore, Project, Connection, Portfolio."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from atlas.models import Connection, GitInfo, HealthScore, Portfolio, Project, TechStack


class TestTechStack:
    def test_primary_languages_top_three(self):
        ts = TechStack(languages={"Python": 50, "TypeScript": 30, "Go": 10, "Java": 5})
        assert ts.primary_languages == ["Python", "TypeScript", "Go"]

    def test_primary_languages_excludes_markdown_mdx_shell(self):
        # primary_languages takes top 3 by count, then filters out Markdown/MDX/Shell
        # So if all top 3 are excluded, result is empty
        ts = TechStack(languages={"Markdown": 100, "MDX": 50, "Shell": 30})
        assert ts.primary_languages == []
        # When a real language is in top 3, it survives the filter
        ts2 = TechStack(languages={"Python": 100, "Markdown": 50, "Shell": 30})
        assert ts2.primary_languages == ["Python"]

    def test_primary_languages_empty(self):
        ts = TechStack(languages={})
        assert ts.primary_languages == []

    def test_summary_with_languages_and_frameworks(self):
        ts = TechStack(
            languages={"Python": 50, "TypeScript": 10},
            frameworks=["FastAPI", "React", "Docker"],
        )
        summary = ts.summary
        assert "Python" in summary
        # Docker is excluded from summary frameworks
        assert "Docker" not in summary

    def test_summary_frameworks_limited_to_two(self):
        ts = TechStack(
            languages={"Python": 50},
            frameworks=["FastAPI", "Pydantic", "SQLAlchemy"],
        )
        parts = ts.summary.split(" · ")
        assert len(parts) <= 3

    def test_summary_empty(self):
        ts = TechStack()
        assert ts.summary == "Unknown"

    def test_summary_only_markdown_files(self):
        ts = TechStack(languages={"Markdown": 10})
        assert ts.summary == "Unknown"

    def test_defaults(self):
        ts = TechStack()
        assert ts.languages == {}
        assert ts.frameworks == []
        assert ts.databases == []
        assert ts.key_deps == {}


class TestGitInfo:
    def test_defaults(self):
        gi = GitInfo()
        assert gi.branch == ""
        assert gi.last_commit_date == ""
        assert gi.last_commit_msg == ""
        assert gi.uncommitted_changes == 0
        assert gi.total_commits == 0
        assert gi.has_remote is False


class TestHealthScore:
    def test_compute_grade_a(self):
        hs = HealthScore(tests=1.0, git_hygiene=1.0, documentation=1.0, structure=1.0)
        hs.compute()
        assert hs.grade == "A"
        assert hs.overall == 1.0

    def test_compute_grade_b_plus(self):
        hs = HealthScore(tests=0.9, git_hygiene=0.8, documentation=0.8, structure=0.8)
        hs.compute()
        assert hs.grade == "B+"

    def test_compute_grade_b(self):
        hs = HealthScore(tests=0.8, git_hygiene=0.7, documentation=0.75, structure=0.8)
        hs.compute()
        assert hs.grade == "B"

    def test_compute_grade_c(self):
        hs = HealthScore(tests=0.5, git_hygiene=0.7, documentation=0.6, structure=0.7)
        hs.compute()
        assert hs.grade == "C"

    def test_compute_grade_d(self):
        # overall = 0.4*0.35 + 0.5*0.20 + 0.5*0.20 + 0.5*0.25 = 0.14+0.10+0.10+0.125 = 0.465
        hs = HealthScore(tests=0.4, git_hygiene=0.5, documentation=0.5, structure=0.5)
        hs.compute()
        assert hs.grade == "D"

    def test_compute_grade_f(self):
        hs = HealthScore(tests=0.0, git_hygiene=0.0, documentation=0.0, structure=0.0)
        hs.compute()
        assert hs.grade == "F"
        assert hs.overall == 0.0

    def test_overall_is_weighted_sum(self):
        hs = HealthScore(tests=1.0, git_hygiene=1.0, documentation=1.0, structure=1.0)
        hs.compute()
        expected = 1.0 * 0.35 + 1.0 * 0.20 + 1.0 * 0.20 + 1.0 * 0.25
        assert hs.overall == pytest.approx(expected)

    def test_weights_sum_to_one(self):
        assert 0.35 + 0.20 + 0.20 + 0.25 == pytest.approx(1.0)

    def test_percent(self):
        hs = HealthScore()
        hs.overall = 0.756
        assert hs.percent == 75

    def test_icon_green(self):
        hs = HealthScore()
        hs.overall = 0.80
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
        hs.overall = 0.30
        assert "dim red" in hs.icon


class TestConnection:
    def test_defaults(self):
        c = Connection(type="shared_dep", detail="react across 3")
        assert c.projects == []
        assert c.severity == "info"

    def test_full_init(self):
        c = Connection(
            type="version_mismatch",
            detail="react: 18 vs 19",
            projects=["app1", "app2"],
            severity="warning",
        )
        assert c.type == "version_mismatch"
        assert len(c.projects) == 2


class TestProject:
    def test_to_dict_roundtrip(self):
        orig = Project(
            name="myapp",
            path="/tmp/myapp",
            tech_stack=TechStack(
                languages={"Python": 30},
                frameworks=["FastAPI"],
                databases=["PostgreSQL"],
                key_deps={"fastapi": "==0.109.0"},
            ),
            git_info=GitInfo(
                branch="main",
                last_commit_date="2026-01-01",
                last_commit_msg="init",
                uncommitted_changes=2,
                total_commits=50,
                has_remote=True,
            ),
            health=HealthScore(
                tests=0.8, git_hygiene=0.7,
                documentation=0.6, structure=0.9,
                overall=0.76, grade="B",
            ),
            test_file_count=5,
            source_file_count=30,
            total_file_count=60,
            loc=1500,
        )
        d = orig.to_dict()
        restored = Project.from_dict(d)
        assert restored.name == "myapp"
        assert restored.tech_stack.languages == {"Python": 30}
        assert restored.tech_stack.frameworks == ["FastAPI"]
        assert restored.tech_stack.databases == ["PostgreSQL"]
        assert restored.git_info.branch == "main"
        assert restored.git_info.total_commits == 50
        assert restored.git_info.has_remote is True
        assert restored.health.grade == "B"
        assert restored.test_file_count == 5
        assert restored.loc == 1500

    def test_from_dict_missing_fields(self):
        p = Project.from_dict({"name": "minimal", "path": "/tmp/minimal"})
        assert p.name == "minimal"
        assert p.tech_stack.languages == {}
        assert p.git_info.total_commits == 0
        assert p.health.grade == "F"
        assert p.loc == 0

    def test_defaults(self):
        p = Project(name="x", path="/tmp/x")
        assert p.test_file_count == 0
        assert p.source_file_count == 0
        assert p.total_file_count == 0
        assert p.loc == 0


class TestPortfolio:
    def _make_project(self, name, test_files=5, loc=500, health_overall=0.7):
        p = Project(name=name, path=f"/tmp/{name}")
        p.test_file_count = test_files
        p.loc = loc
        p.health = HealthScore(overall=health_overall, grade="C")
        return p

    def test_total_tests(self):
        pf = Portfolio(name="test")
        pf.projects = [self._make_project("a", test_files=10), self._make_project("b", test_files=20)]
        assert pf.total_tests == 30

    def test_total_loc(self):
        pf = Portfolio(name="test")
        pf.projects = [self._make_project("a", loc=1000), self._make_project("b", loc=2000)]
        assert pf.total_loc == 3000

    def test_avg_health(self):
        pf = Portfolio(name="test")
        pf.projects = [
            self._make_project("a", health_overall=0.8),
            self._make_project("b", health_overall=0.6),
        ]
        assert pf.avg_health == pytest.approx(0.7)

    def test_avg_health_empty(self):
        pf = Portfolio(name="test")
        assert pf.avg_health == 0.0

    def test_avg_grade_a(self):
        pf = Portfolio(name="test")
        pf.projects = [self._make_project("a", health_overall=0.95)]
        assert pf.avg_grade == "A"

    def test_avg_grade_f(self):
        pf = Portfolio(name="test")
        pf.projects = [self._make_project("a", health_overall=0.2)]
        assert pf.avg_grade == "F"

    def test_save_and_load(self, tmp_path):
        pf = Portfolio(name="test-portfolio", created="2026-01-01", last_scan="2026-03-01")
        pf.projects = [
            Project(
                name="app1", path="/tmp/app1",
                tech_stack=TechStack(languages={"Python": 10}),
                test_file_count=5, source_file_count=20,
                total_file_count=40, loc=800,
            ),
        ]
        save_path = tmp_path / "portfolios" / "test.json"
        pf.save(save_path)

        loaded = Portfolio.load(save_path)
        assert loaded.name == "test-portfolio"
        assert loaded.created == "2026-01-01"
        assert len(loaded.projects) == 1
        assert loaded.projects[0].name == "app1"
        assert loaded.projects[0].tech_stack.languages == {"Python": 10}

    def test_find_project(self):
        pf = Portfolio(name="test")
        pf.projects = [
            Project(name="Atlas", path="/tmp/atlas"),
            Project(name="Forge", path="/tmp/forge"),
        ]
        assert pf.find_project("atlas").name == "Atlas"
        assert pf.find_project("FORGE").name == "Forge"
        assert pf.find_project("missing") is None

    def test_find_project_empty(self):
        pf = Portfolio(name="test")
        assert pf.find_project("anything") is None
