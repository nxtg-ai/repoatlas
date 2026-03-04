"""Tests for cross-project intelligence."""
from atlas.connections import find_connections
from atlas.models import GitInfo, HealthScore, Project, TechStack


def _proj(name: str, frameworks=None, key_deps=None, databases=None,
          test_files=0, source_files=10, git_commits=20) -> Project:
    return Project(
        name=name,
        path=f"/tmp/{name}",
        tech_stack=TechStack(
            frameworks=frameworks or [],
            key_deps=key_deps or {},
            databases=databases or [],
        ),
        git_info=GitInfo(total_commits=git_commits),
        health=HealthScore(structure=0.5),
        test_file_count=test_files,
        source_file_count=source_files,
    )


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
