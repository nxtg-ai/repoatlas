"""Tests for cross-project intelligence (connections/patterns)."""
from __future__ import annotations

from atlas.connections import (
    _find_health_gaps,
    _find_shared_databases,
    _find_shared_deps,
    _find_shared_frameworks,
    _find_version_mismatches,
    find_connections,
)
from atlas.models import GitInfo, HealthScore, Project, TechStack


def _proj(name: str, frameworks=None, key_deps=None, databases=None,
          test_files=0, source_files=10, git_commits=20,
          uncommitted=0, structure_score=0.5) -> Project:
    return Project(
        name=name,
        path=f"/tmp/{name}",
        tech_stack=TechStack(
            frameworks=frameworks or [],
            key_deps=key_deps or {},
            databases=databases or [],
        ),
        git_info=GitInfo(total_commits=git_commits, uncommitted_changes=uncommitted),
        health=HealthScore(structure=structure_score),
        test_file_count=test_files,
        source_file_count=source_files,
    )


# ---------------------------------------------------------------------------
# find_connections — integration
# ---------------------------------------------------------------------------
class TestFindConnections:
    def test_finds_shared_deps(self):
        projects = [
            _proj("app1", key_deps={"fastapi": "0.109.0", "pydantic": "2.5.0"}),
            _proj("app2", key_deps={"fastapi": "0.115.0", "django": "5.0"}),
            _proj("app3", key_deps={"express": "4.18"}),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_dep"]
        assert any("fastapi" in c.detail.lower() for c in shared)

    def test_finds_version_mismatches(self):
        projects = [
            _proj("app1", key_deps={"react": "^18.2.0"}),
            _proj("app2", key_deps={"react": "^19.0.0"}),
        ]
        conns = find_connections(projects)
        mismatches = [c for c in conns if c.type == "version_mismatch"]
        assert any("react" in c.detail for c in mismatches)

    def test_finds_health_gaps_zero_tests(self):
        projects = [
            _proj("healthy", test_files=20, source_files=50),
            _proj("untested", test_files=0, source_files=30),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "health_gap"]
        assert any("zero tests" in c.detail for c in gaps)
        assert "untested" in gaps[0].projects

    def test_finds_shared_frameworks(self):
        projects = [
            _proj("a", frameworks=["Docker", "FastAPI"]),
            _proj("b", frameworks=["Docker", "Flask"]),
            _proj("c", frameworks=["Docker", "Django"]),
        ]
        conns = find_connections(projects)
        shared_fw = [c for c in conns if c.type == "shared_framework"]
        assert any("Docker" in c.detail for c in shared_fw)

    def test_finds_shared_databases(self):
        projects = [
            _proj("a", databases=["PostgreSQL"]),
            _proj("b", databases=["PostgreSQL", "Redis"]),
        ]
        conns = find_connections(projects)
        shared_db = [c for c in conns if c.type == "shared_database"]
        assert any("PostgreSQL" in c.detail for c in shared_db)

    def test_empty_portfolio(self):
        conns = find_connections([])
        assert conns == []

    def test_single_project(self):
        conns = find_connections([_proj("solo", key_deps={"fastapi": "0.109.0"})])
        shared = [c for c in conns if c.type == "shared_dep"]
        assert shared == []

    def test_all_connection_types_present(self):
        projects = [
            _proj("a", frameworks=["Docker", "FastAPI"], key_deps={"fastapi": "0.109"},
                  databases=["PostgreSQL"], test_files=0, source_files=20,
                  uncommitted=15, git_commits=3),
            _proj("b", frameworks=["Docker", "Flask"], key_deps={"fastapi": "0.115"},
                  databases=["PostgreSQL"]),
            _proj("c", frameworks=["Docker", "Django"], key_deps={"express": "4.18"},
                  databases=["Redis"]),
        ]
        conns = find_connections(projects)
        types = {c.type for c in conns}
        assert "shared_framework" in types
        assert "version_mismatch" in types
        assert "health_gap" in types
        assert "shared_database" in types


# ---------------------------------------------------------------------------
# _find_shared_deps
# ---------------------------------------------------------------------------
class TestFindSharedDeps:
    def test_only_important_deps_matched(self):
        projects = [
            _proj("a", key_deps={"obscure-lib": "1.0"}),
            _proj("b", key_deps={"obscure-lib": "1.0"}),
        ]
        conns = _find_shared_deps(projects)
        assert conns == []

    def test_important_dep_shared(self):
        projects = [
            _proj("a", key_deps={"fastapi": "0.109.0"}),
            _proj("b", key_deps={"fastapi": "0.115.0"}),
        ]
        conns = _find_shared_deps(projects)
        assert len(conns) == 1
        assert "fastapi" in conns[0].detail.lower()
        assert conns[0].severity == "info"

    def test_limit_10(self):
        # Create 15 shared important deps — should be capped at 10
        important = ["fastapi", "react", "next", "express", "sqlalchemy",
                      "pydantic", "anthropic", "openai", "django", "flask",
                      "pytest", "vitest", "jest", "tailwindcss", "redis"]
        deps = {d: "1.0" for d in important}
        projects = [_proj("a", key_deps=deps), _proj("b", key_deps=deps)]
        conns = _find_shared_deps(projects)
        assert len(conns) <= 10

    def test_needs_at_least_two_projects(self):
        projects = [_proj("a", key_deps={"fastapi": "0.109.0"})]
        assert _find_shared_deps(projects) == []

    def test_projects_listed(self):
        projects = [
            _proj("alpha", key_deps={"react": "18.0"}),
            _proj("beta", key_deps={"react": "18.0"}),
        ]
        conns = _find_shared_deps(projects)
        assert "alpha" in conns[0].projects
        assert "beta" in conns[0].projects


# ---------------------------------------------------------------------------
# _find_shared_frameworks
# ---------------------------------------------------------------------------
class TestFindSharedFrameworks:
    def test_needs_three_projects(self):
        projects = [
            _proj("a", frameworks=["FastAPI"]),
            _proj("b", frameworks=["FastAPI"]),
        ]
        assert _find_shared_frameworks(projects) == []

    def test_three_projects_shared(self):
        projects = [
            _proj("a", frameworks=["React"]),
            _proj("b", frameworks=["React"]),
            _proj("c", frameworks=["React"]),
        ]
        conns = _find_shared_frameworks(projects)
        assert len(conns) == 1
        assert "React" in conns[0].detail

    def test_limit_5(self):
        fws = [f"fw{i}" for i in range(10)]
        projects = [_proj(f"p{j}", frameworks=fws) for j in range(3)]
        conns = _find_shared_frameworks(projects)
        assert len(conns) <= 5

    def test_severity_is_info(self):
        projects = [_proj(f"p{i}", frameworks=["Docker"]) for i in range(3)]
        conns = _find_shared_frameworks(projects)
        assert all(c.severity == "info" for c in conns)


# ---------------------------------------------------------------------------
# _find_version_mismatches
# ---------------------------------------------------------------------------
class TestFindVersionMismatches:
    def test_same_version_no_mismatch(self):
        projects = [
            _proj("a", key_deps={"react": "^18.2.0"}),
            _proj("b", key_deps={"react": "^18.2.0"}),
        ]
        assert _find_version_mismatches(projects) == []

    def test_different_versions_detected(self):
        projects = [
            _proj("a", key_deps={"react": "^18.2.0"}),
            _proj("b", key_deps={"react": "^19.0.0"}),
        ]
        conns = _find_version_mismatches(projects)
        assert len(conns) == 1
        assert "react" in conns[0].detail
        assert conns[0].severity == "warning"

    def test_three_versions(self):
        projects = [
            _proj("a", key_deps={"react": "16.0"}),
            _proj("b", key_deps={"react": "17.0"}),
            _proj("c", key_deps={"react": "18.0"}),
        ]
        conns = _find_version_mismatches(projects)
        assert len(conns) == 1

    def test_limit_8(self):
        projects = []
        for i in range(2):
            deps = {f"dep{j}": f"v{i}" for j in range(15)}
            projects.append(_proj(f"p{i}", key_deps=deps))
        conns = _find_version_mismatches(projects)
        assert len(conns) <= 8

    def test_all_projects_listed(self):
        projects = [
            _proj("alpha", key_deps={"fastapi": "0.109"}),
            _proj("beta", key_deps={"fastapi": "0.115"}),
        ]
        conns = _find_version_mismatches(projects)
        assert "alpha" in conns[0].projects
        assert "beta" in conns[0].projects


# ---------------------------------------------------------------------------
# _find_health_gaps
# ---------------------------------------------------------------------------
class TestFindHealthGaps:
    def test_zero_tests_detected(self):
        projects = [_proj("untested", test_files=0, source_files=20)]
        conns = _find_health_gaps(projects)
        assert any("zero tests" in c.detail for c in conns)

    def test_zero_tests_ignored_if_few_source_files(self):
        projects = [_proj("tiny", test_files=0, source_files=3)]
        conns = _find_health_gaps(projects)
        test_gaps = [c for c in conns if "zero tests" in c.detail]
        assert test_gaps == []

    def test_dirty_working_tree(self):
        projects = [_proj("dirty", uncommitted=15)]
        conns = _find_health_gaps(projects)
        assert any("uncommitted" in c.detail for c in conns)

    def test_slightly_dirty_not_flagged(self):
        projects = [_proj("ok", uncommitted=5)]
        conns = _find_health_gaps(projects)
        dirty_gaps = [c for c in conns if "uncommitted" in c.detail]
        assert dirty_gaps == []

    def test_stale_project(self):
        projects = [_proj("stale", git_commits=3, source_files=10)]
        conns = _find_health_gaps(projects)
        assert any("stale" in c.detail for c in conns)

    def test_stale_ignored_if_few_source_files(self):
        projects = [_proj("tiny", git_commits=3, source_files=3)]
        conns = _find_health_gaps(projects)
        stale_gaps = [c for c in conns if "stale" in c.detail]
        assert stale_gaps == []

    def test_stale_ignored_if_zero_commits(self):
        projects = [_proj("new", git_commits=0, source_files=20)]
        conns = _find_health_gaps(projects)
        stale_gaps = [c for c in conns if "stale" in c.detail]
        assert stale_gaps == []

    def test_healthy_project_no_gaps(self):
        projects = [_proj("healthy", test_files=10, source_files=30,
                         git_commits=50, uncommitted=0)]
        conns = _find_health_gaps(projects)
        assert conns == []

    def test_severity_levels(self):
        projects = [
            _proj("untested", test_files=0, source_files=20),
            _proj("dirty", uncommitted=15),
        ]
        conns = _find_health_gaps(projects)
        severities = {c.severity for c in conns}
        assert "critical" in severities
        assert "warning" in severities


# ---------------------------------------------------------------------------
# _find_shared_databases
# ---------------------------------------------------------------------------
class TestFindSharedDatabases:
    def test_shared_db(self):
        projects = [
            _proj("a", databases=["PostgreSQL"]),
            _proj("b", databases=["PostgreSQL"]),
        ]
        conns = _find_shared_databases(projects)
        assert len(conns) == 1
        assert "PostgreSQL" in conns[0].detail

    def test_no_shared_db(self):
        projects = [
            _proj("a", databases=["PostgreSQL"]),
            _proj("b", databases=["Redis"]),
        ]
        assert _find_shared_databases(projects) == []

    def test_single_project(self):
        projects = [_proj("a", databases=["PostgreSQL"])]
        assert _find_shared_databases(projects) == []

    def test_limit_5(self):
        dbs = [f"db{i}" for i in range(10)]
        projects = [_proj("a", databases=dbs), _proj("b", databases=dbs)]
        conns = _find_shared_databases(projects)
        assert len(conns) <= 5

    def test_severity_is_info(self):
        projects = [
            _proj("a", databases=["Redis"]),
            _proj("b", databases=["Redis"]),
        ]
        conns = _find_shared_databases(projects)
        assert conns[0].severity == "info"
