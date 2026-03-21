"""Tests for cross-project intelligence (connections/patterns)."""
from __future__ import annotations

from atlas.connections import (
    _find_ai_patterns,
    _find_health_gaps,
    _find_infra_patterns,
    _find_quality_patterns,
    _find_security_patterns,
    _find_shared_databases,
    _find_shared_deps,
    _find_shared_frameworks,
    _find_testing_patterns,
    _find_version_mismatches,
    find_connections,
)
from atlas.models import GitInfo, HealthScore, Project, TechStack


def _proj(name: str, frameworks=None, key_deps=None, databases=None,
          infrastructure=None, security_tools=None, quality_tools=None,
          ai_tools=None, testing_frameworks=None,
          test_files=0, source_files=10, git_commits=20, uncommitted=0,
          structure_score=0.5) -> Project:
    return Project(
        name=name,
        path=f"/tmp/{name}",
        tech_stack=TechStack(
            frameworks=frameworks or [],
            key_deps=key_deps or {},
            databases=databases or [],
            infrastructure=infrastructure or [],
            security_tools=security_tools or [],
            quality_tools=quality_tools or [],
            ai_tools=ai_tools or [],
            testing_frameworks=testing_frameworks or [],
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


# ---------------------------------------------------------------------------
# _find_infra_patterns
# ---------------------------------------------------------------------------
class TestFindInfraPatterns:
    def test_shared_infra(self):
        projects = [
            _proj("a", infrastructure=["Docker", "GitHub Actions"]),
            _proj("b", infrastructure=["Docker", "Vercel"]),
        ]
        conns = _find_infra_patterns(projects)
        shared = [c for c in conns if c.type == "shared_infra"]
        assert any("Docker" in c.detail for c in shared)

    def test_shared_infra_needs_two_projects(self):
        projects = [_proj("a", infrastructure=["Docker"])]
        conns = _find_infra_patterns(projects)
        shared = [c for c in conns if c.type == "shared_infra"]
        assert shared == []

    def test_platform_divergence(self):
        projects = [
            _proj("a", infrastructure=["Vercel", "Netlify"]),
        ]
        conns = _find_infra_patterns(projects)
        diverge = [c for c in conns if c.type == "infra_divergence"]
        assert len(diverge) == 1
        assert "consolidate" in diverge[0].detail.lower()

    def test_no_platform_divergence_single_host(self):
        projects = [_proj("a", infrastructure=["Vercel"])]
        conns = _find_infra_patterns(projects)
        diverge = [c for c in conns if c.type == "infra_divergence" and "hosting" in c.detail]
        assert diverge == []

    def test_ci_divergence(self):
        projects = [
            _proj("a", infrastructure=["GitHub Actions"]),
            _proj("b", infrastructure=["GitLab CI"]),
        ]
        conns = _find_infra_patterns(projects)
        diverge = [c for c in conns if c.type == "infra_divergence" and "CI" in c.detail]
        assert len(diverge) == 1
        assert "standardize" in diverge[0].detail.lower()

    def test_no_ci_divergence_single_system(self):
        projects = [
            _proj("a", infrastructure=["GitHub Actions"]),
            _proj("b", infrastructure=["GitHub Actions"]),
        ]
        conns = _find_infra_patterns(projects)
        ci_diverge = [c for c in conns if c.type == "infra_divergence" and "CI" in c.detail]
        assert ci_diverge == []

    def test_no_ci_detected(self):
        projects = [
            _proj("a", infrastructure=["Docker"], source_files=20),
            _proj("b", infrastructure=["Docker"], source_files=15),
        ]
        conns = _find_infra_patterns(projects)
        gaps = [c for c in conns if c.type == "infra_gap" and "CI" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "critical"

    def test_no_ci_gap_when_ci_present(self):
        projects = [
            _proj("a", infrastructure=["GitHub Actions"], source_files=20),
        ]
        conns = _find_infra_patterns(projects)
        gaps = [c for c in conns if c.type == "infra_gap" and "CI" in c.detail]
        assert gaps == []

    def test_cloud_without_iac(self):
        projects = [
            _proj("a", infrastructure=["AWS"]),
            _proj("b", infrastructure=["GCP"]),
        ]
        conns = _find_infra_patterns(projects)
        gaps = [c for c in conns if c.type == "infra_gap" and "IaC" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_cloud_with_iac_no_gap(self):
        projects = [
            _proj("a", infrastructure=["AWS", "Terraform"]),
            _proj("b", infrastructure=["GCP"]),
        ]
        conns = _find_infra_patterns(projects)
        gaps = [c for c in conns if c.type == "infra_gap" and "IaC" in c.detail]
        assert gaps == []

    def test_docker_without_orchestration(self):
        projects = [
            _proj("a", infrastructure=["Docker"]),
            _proj("b", infrastructure=["Docker"]),
            _proj("c", infrastructure=["Docker"]),
        ]
        conns = _find_infra_patterns(projects)
        gaps = [c for c in conns if c.type == "infra_gap" and "orchestration" in c.detail]
        assert len(gaps) == 1

    def test_docker_with_compose_no_gap(self):
        projects = [
            _proj("a", infrastructure=["Docker", "Docker Compose"]),
            _proj("b", infrastructure=["Docker"]),
            _proj("c", infrastructure=["Docker"]),
        ]
        conns = _find_infra_patterns(projects)
        gaps = [c for c in conns if c.type == "infra_gap" and "orchestration" in c.detail]
        assert gaps == []

    def test_empty_projects(self):
        assert _find_infra_patterns([]) == []

    def test_limit_10(self):
        # Many infra items shared across projects
        infra = [f"tool{i}" for i in range(20)]
        projects = [_proj("a", infrastructure=infra), _proj("b", infrastructure=infra)]
        conns = _find_infra_patterns(projects)
        assert len(conns) <= 10

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", infrastructure=["Docker", "GitHub Actions"]),
            _proj("b", infrastructure=["Docker", "GitLab CI"]),
        ]
        conns = find_connections(projects)
        infra_types = {c.type for c in conns if c.type.startswith("infra") or c.type == "shared_infra"}
        assert len(infra_types) >= 1


# ---------------------------------------------------------------------------
# _find_security_patterns
# ---------------------------------------------------------------------------
class TestFindSecurityPatterns:
    def test_shared_security_tool(self):
        projects = [
            _proj("a", security_tools=["Dependabot", "Gitleaks"]),
            _proj("b", security_tools=["Dependabot", "Snyk"]),
        ]
        conns = _find_security_patterns(projects)
        shared = [c for c in conns if c.type == "shared_security"]
        assert any("Dependabot" in c.detail for c in shared)
        assert shared[0].severity == "info"

    def test_shared_security_needs_two_projects(self):
        projects = [_proj("a", security_tools=["Dependabot"])]
        conns = _find_security_patterns(projects)
        shared = [c for c in conns if c.type == "shared_security"]
        assert shared == []

    def test_no_security_tooling_gap(self):
        projects = [
            _proj("secured", security_tools=["Dependabot"], source_files=20),
            _proj("bare", security_tools=[], source_files=20),
        ]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap" and "no security tooling" in c.detail]
        assert len(gaps) == 1
        assert "bare" in gaps[0].projects
        assert gaps[0].severity == "critical"

    def test_no_security_gap_small_project(self):
        projects = [_proj("tiny", security_tools=[], source_files=3)]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap" and "no security tooling" in c.detail]
        assert gaps == []

    def test_missing_dep_scanning(self):
        projects = [
            _proj("a", security_tools=["Gitleaks"], source_files=20),
        ]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap" and "dependency scanning" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_no_dep_scanning_gap_when_present(self):
        projects = [
            _proj("a", security_tools=["Dependabot", "Gitleaks"], source_files=20),
        ]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap" and "dependency scanning" in c.detail]
        assert gaps == []

    def test_missing_secret_scanning(self):
        projects = [
            _proj("a", security_tools=["Dependabot"], source_files=20),
        ]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap" and "secret scanning" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_no_secret_scanning_gap_when_present(self):
        projects = [
            _proj("a", security_tools=["Dependabot", "Gitleaks"], source_files=20),
        ]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap" and "secret scanning" in c.detail]
        assert gaps == []

    def test_dep_scanner_divergence(self):
        projects = [
            _proj("a", security_tools=["Dependabot"]),
            _proj("b", security_tools=["Renovate"]),
        ]
        conns = _find_security_patterns(projects)
        diverge = [c for c in conns if c.type == "security_divergence"]
        assert len(diverge) == 1
        assert "standardize" in diverge[0].detail.lower()
        assert diverge[0].severity == "warning"

    def test_no_divergence_single_scanner(self):
        projects = [
            _proj("a", security_tools=["Dependabot"]),
            _proj("b", security_tools=["Dependabot"]),
        ]
        conns = _find_security_patterns(projects)
        diverge = [c for c in conns if c.type == "security_divergence"]
        assert diverge == []

    def test_empty_projects(self):
        assert _find_security_patterns([]) == []

    def test_all_secure_no_gaps(self):
        projects = [
            _proj("a", security_tools=["Dependabot", "Gitleaks"], source_files=20),
            _proj("b", security_tools=["Dependabot", "detect-secrets"], source_files=20),
        ]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap"]
        assert gaps == []

    def test_limit_10(self):
        tools = [f"tool{i}" for i in range(20)]
        projects = [_proj("a", security_tools=tools), _proj("b", security_tools=tools)]
        conns = _find_security_patterns(projects)
        assert len(conns) <= 10

    def test_pip_audit_counts_as_dep_scanner(self):
        projects = [
            _proj("a", security_tools=["pip-audit"], source_files=20),
        ]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap" and "dependency scanning" in c.detail]
        assert gaps == []

    def test_sops_counts_as_secret_scanner(self):
        projects = [
            _proj("a", security_tools=["Dependabot", "SOPS"], source_files=20),
        ]
        conns = _find_security_patterns(projects)
        gaps = [c for c in conns if c.type == "security_gap" and "secret scanning" in c.detail]
        assert gaps == []

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", security_tools=["Dependabot", "Gitleaks"]),
            _proj("b", security_tools=["Dependabot", "Renovate"]),
        ]
        conns = find_connections(projects)
        sec_types = {c.type for c in conns if "security" in c.type}
        assert "shared_security" in sec_types


# ---------------------------------------------------------------------------
# _find_quality_patterns
# ---------------------------------------------------------------------------
class TestFindQualityPatterns:
    def test_shared_quality_tool(self):
        projects = [
            _proj("a", quality_tools=["Ruff", "mypy"]),
            _proj("b", quality_tools=["Ruff", "Black"]),
        ]
        conns = _find_quality_patterns(projects)
        shared = [c for c in conns if c.type == "shared_quality"]
        assert any("Ruff" in c.detail for c in shared)
        assert shared[0].severity == "info"

    def test_shared_quality_needs_two_projects(self):
        projects = [_proj("a", quality_tools=["Ruff"])]
        conns = _find_quality_patterns(projects)
        shared = [c for c in conns if c.type == "shared_quality"]
        assert shared == []

    def test_no_quality_tooling_gap(self):
        projects = [
            _proj("linted", quality_tools=["Ruff"], source_files=20),
            _proj("bare", quality_tools=[], source_files=20),
        ]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap" and "no code quality" in c.detail]
        assert len(gaps) == 1
        assert "bare" in gaps[0].projects
        assert gaps[0].severity == "critical"

    def test_no_quality_gap_small_project(self):
        projects = [_proj("tiny", quality_tools=[], source_files=3)]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap" and "no code quality" in c.detail]
        assert gaps == []

    def test_missing_linting(self):
        projects = [
            _proj("a", quality_tools=["Black", "mypy"], source_files=20),
        ]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap" and "linting" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_no_linting_gap_when_present(self):
        projects = [
            _proj("a", quality_tools=["Ruff", "Black"], source_files=20),
        ]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap" and "linting" in c.detail]
        assert gaps == []

    def test_eslint_counts_as_linter(self):
        projects = [
            _proj("a", quality_tools=["ESLint", "Prettier"], source_files=20),
        ]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap" and "linting" in c.detail]
        assert gaps == []

    def test_missing_type_checking(self):
        projects = [
            _proj("a", quality_tools=["Ruff", "Black"], source_files=20),
        ]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap" and "type checking" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_no_type_checking_gap_when_present(self):
        projects = [
            _proj("a", quality_tools=["Ruff", "mypy"], source_files=20),
        ]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap" and "type checking" in c.detail]
        assert gaps == []

    def test_typescript_counts_as_type_checker(self):
        projects = [
            _proj("a", quality_tools=["ESLint", "TypeScript"], source_files=20),
        ]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap" and "type checking" in c.detail]
        assert gaps == []

    def test_linter_divergence(self):
        projects = [
            _proj("a", quality_tools=["Ruff"]),
            _proj("b", quality_tools=["Flake8"]),
        ]
        conns = _find_quality_patterns(projects)
        diverge = [c for c in conns if c.type == "quality_divergence"]
        assert len(diverge) == 1
        assert "standardize" in diverge[0].detail.lower()
        assert diverge[0].severity == "warning"

    def test_no_divergence_single_linter(self):
        projects = [
            _proj("a", quality_tools=["Ruff"]),
            _proj("b", quality_tools=["Ruff"]),
        ]
        conns = _find_quality_patterns(projects)
        diverge = [c for c in conns if c.type == "quality_divergence"]
        assert diverge == []

    def test_empty_projects(self):
        assert _find_quality_patterns([]) == []

    def test_all_quality_no_gaps(self):
        projects = [
            _proj("a", quality_tools=["Ruff", "mypy", "Black"], source_files=20),
            _proj("b", quality_tools=["Ruff", "Pyright", "Black"], source_files=20),
        ]
        conns = _find_quality_patterns(projects)
        gaps = [c for c in conns if c.type == "quality_gap"]
        assert gaps == []

    def test_limit_10(self):
        tools = [f"tool{i}" for i in range(20)]
        projects = [_proj("a", quality_tools=tools), _proj("b", quality_tools=tools)]
        conns = _find_quality_patterns(projects)
        assert len(conns) <= 10

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", quality_tools=["Ruff", "mypy"]),
            _proj("b", quality_tools=["Ruff", "Flake8"]),
        ]
        conns = find_connections(projects)
        qt_types = {c.type for c in conns if "quality" in c.type}
        assert "shared_quality" in qt_types


# ===========================================================================
# AI/ML patterns
# ===========================================================================


class TestFindAIPatterns:
    def test_shared_ai_tools(self):
        projects = [
            _proj("a", ai_tools=["Anthropic SDK", "LangChain"]),
            _proj("b", ai_tools=["Anthropic SDK"]),
        ]
        conns = _find_ai_patterns(projects)
        shared = [c for c in conns if c.type == "shared_ai"]
        assert len(shared) == 1
        assert "Anthropic SDK" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_ai_multiple_tools(self):
        projects = [
            _proj("a", ai_tools=["Anthropic SDK", "LangChain"]),
            _proj("b", ai_tools=["Anthropic SDK", "LangChain"]),
        ]
        conns = _find_ai_patterns(projects)
        shared = [c for c in conns if c.type == "shared_ai"]
        assert len(shared) == 2

    def test_no_shared_ai_when_unique(self):
        projects = [
            _proj("a", ai_tools=["Anthropic SDK"]),
            _proj("b", ai_tools=["OpenAI"]),
        ]
        conns = _find_ai_patterns(projects)
        shared = [c for c in conns if c.type == "shared_ai"]
        assert len(shared) == 0

    def test_llm_provider_divergence(self):
        projects = [
            _proj("a", ai_tools=["Anthropic SDK"]),
            _proj("b", ai_tools=["OpenAI"]),
        ]
        conns = _find_ai_patterns(projects)
        div = [c for c in conns if c.type == "ai_divergence" and "LLM" in c.detail]
        assert len(div) == 1
        assert div[0].severity == "warning"
        assert "standardize" in div[0].detail.lower()

    def test_no_llm_divergence_single_provider(self):
        projects = [
            _proj("a", ai_tools=["Anthropic SDK"]),
            _proj("b", ai_tools=["Anthropic SDK"]),
        ]
        conns = _find_ai_patterns(projects)
        div = [c for c in conns if c.type == "ai_divergence" and "LLM" in c.detail]
        assert len(div) == 0

    def test_vector_db_divergence(self):
        projects = [
            _proj("a", ai_tools=["ChromaDB"]),
            _proj("b", ai_tools=["Pinecone"]),
        ]
        conns = _find_ai_patterns(projects)
        div = [c for c in conns if c.type == "ai_divergence" and "vector" in c.detail.lower()]
        assert len(div) == 1
        assert div[0].severity == "warning"

    def test_no_vector_db_divergence_single(self):
        projects = [
            _proj("a", ai_tools=["ChromaDB"]),
            _proj("b", ai_tools=["ChromaDB"]),
        ]
        conns = _find_ai_patterns(projects)
        div = [c for c in conns if c.type == "ai_divergence" and "vector" in c.detail.lower()]
        assert len(div) == 0

    def test_ml_without_experiment_tracking(self):
        projects = [
            _proj("a", ai_tools=["PyTorch"]),
            _proj("b", ai_tools=["TensorFlow"]),
        ]
        conns = _find_ai_patterns(projects)
        gap = [c for c in conns if c.type == "ai_gap"]
        assert len(gap) == 1
        assert "experiment tracking" in gap[0].detail
        assert gap[0].severity == "warning"
        assert len(gap[0].projects) == 2

    def test_ml_with_experiment_tracking_no_gap(self):
        projects = [
            _proj("a", ai_tools=["PyTorch", "MLflow"]),
            _proj("b", ai_tools=["TensorFlow", "W&B"]),
        ]
        conns = _find_ai_patterns(projects)
        gap = [c for c in conns if c.type == "ai_gap"]
        assert len(gap) == 0

    def test_partial_experiment_tracking(self):
        projects = [
            _proj("a", ai_tools=["PyTorch", "MLflow"]),
            _proj("b", ai_tools=["scikit-learn"]),
        ]
        conns = _find_ai_patterns(projects)
        gap = [c for c in conns if c.type == "ai_gap"]
        assert len(gap) == 1
        assert "b" in gap[0].projects
        assert "a" not in gap[0].projects

    def test_non_ml_ai_tools_no_tracking_gap(self):
        # LLM SDKs should not trigger experiment tracking gap
        projects = [
            _proj("a", ai_tools=["Anthropic SDK", "LangChain"]),
        ]
        conns = _find_ai_patterns(projects)
        gap = [c for c in conns if c.type == "ai_gap"]
        assert len(gap) == 0

    def test_no_ai_tools_no_connections(self):
        projects = [
            _proj("a", ai_tools=[]),
            _proj("b", ai_tools=[]),
        ]
        conns = _find_ai_patterns(projects)
        assert len(conns) == 0

    def test_dvc_counts_as_tracking(self):
        projects = [
            _proj("a", ai_tools=["Transformers", "DVC"]),
        ]
        conns = _find_ai_patterns(projects)
        gap = [c for c in conns if c.type == "ai_gap"]
        assert len(gap) == 0

    def test_max_connections_capped(self):
        # Many AI tools across many projects
        projects = [
            _proj(f"p{i}", ai_tools=["Anthropic SDK", "OpenAI", "LangChain",
                                      "PyTorch", "ChromaDB", "Pinecone"])
            for i in range(10)
        ]
        conns = _find_ai_patterns(projects)
        assert len(conns) <= 10

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", ai_tools=["Anthropic SDK", "LangChain"]),
            _proj("b", ai_tools=["Anthropic SDK", "OpenAI"]),
        ]
        conns = find_connections(projects)
        ai_types = {c.type for c in conns if "ai" in c.type}
        assert "shared_ai" in ai_types
        assert "ai_divergence" in ai_types


# ---------------------------------------------------------------------------
# Testing framework patterns (N-29)
# ---------------------------------------------------------------------------
class TestFindTestingPatterns:
    def test_shared_testing_framework(self):
        projects = [
            _proj("a", testing_frameworks=["pytest"]),
            _proj("b", testing_frameworks=["pytest"]),
        ]
        conns = _find_testing_patterns(projects)
        shared = [c for c in conns if c.type == "shared_testing"]
        assert len(shared) == 1
        assert "pytest" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_multiple_frameworks(self):
        projects = [
            _proj("a", testing_frameworks=["pytest", "Jest"]),
            _proj("b", testing_frameworks=["pytest", "Jest"]),
            _proj("c", testing_frameworks=["Jest"]),
        ]
        conns = _find_testing_patterns(projects)
        shared = [c for c in conns if c.type == "shared_testing"]
        assert len(shared) == 2

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", testing_frameworks=["pytest"]),
            _proj("b", testing_frameworks=["Jest"]),
        ]
        conns = _find_testing_patterns(projects)
        shared = [c for c in conns if c.type == "shared_testing"]
        assert len(shared) == 0

    def test_js_divergence_jest_vs_vitest(self):
        projects = [
            _proj("a", testing_frameworks=["Jest"]),
            _proj("b", testing_frameworks=["Vitest"]),
        ]
        conns = _find_testing_patterns(projects)
        div = [c for c in conns if c.type == "testing_divergence"]
        assert len(div) == 1
        assert "JS test runners" in div[0].detail
        assert div[0].severity == "warning"

    def test_js_divergence_three_runners(self):
        projects = [
            _proj("a", testing_frameworks=["Jest"]),
            _proj("b", testing_frameworks=["Vitest"]),
            _proj("c", testing_frameworks=["Mocha"]),
        ]
        conns = _find_testing_patterns(projects)
        div = [c for c in conns if c.type == "testing_divergence"]
        assert len(div) == 1
        assert "Jest" in div[0].detail
        assert "Vitest" in div[0].detail
        assert "Mocha" in div[0].detail

    def test_no_js_divergence_same_runner(self):
        projects = [
            _proj("a", testing_frameworks=["Jest"]),
            _proj("b", testing_frameworks=["Jest"]),
        ]
        conns = _find_testing_patterns(projects)
        div = [c for c in conns if c.type == "testing_divergence"]
        assert len(div) == 0

    def test_python_divergence_pytest_vs_nose(self):
        projects = [
            _proj("a", testing_frameworks=["pytest"]),
            _proj("b", testing_frameworks=["nose2"]),
        ]
        conns = _find_testing_patterns(projects)
        div = [c for c in conns if c.type == "testing_divergence"]
        assert len(div) == 1
        assert "Python test runners" in div[0].detail

    def test_no_python_divergence_same_runner(self):
        projects = [
            _proj("a", testing_frameworks=["pytest"]),
            _proj("b", testing_frameworks=["pytest"]),
        ]
        conns = _find_testing_patterns(projects)
        div = [c for c in conns if c.type == "testing_divergence"]
        assert len(div) == 0

    def test_testing_gap_no_framework(self):
        projects = [
            _proj("a", testing_frameworks=["pytest"]),
            _proj("b", testing_frameworks=[], source_files=20),
        ]
        conns = _find_testing_patterns(projects)
        gap = [c for c in conns if c.type == "testing_gap"]
        assert len(gap) == 1
        assert "b" in gap[0].projects
        assert gap[0].severity == "critical"

    def test_testing_gap_ignores_small_projects(self):
        projects = [
            _proj("a", testing_frameworks=["pytest"]),
            _proj("tiny", testing_frameworks=[], source_files=3),
        ]
        conns = _find_testing_patterns(projects)
        gap = [c for c in conns if c.type == "testing_gap"]
        assert len(gap) == 0

    def test_no_gap_all_have_frameworks(self):
        projects = [
            _proj("a", testing_frameworks=["pytest"]),
            _proj("b", testing_frameworks=["Jest"]),
        ]
        conns = _find_testing_patterns(projects)
        gap = [c for c in conns if c.type == "testing_gap"]
        assert len(gap) == 0

    def test_empty_projects(self):
        conns = _find_testing_patterns([])
        assert conns == []

    def test_single_project_no_connections(self):
        conns = _find_testing_patterns([_proj("solo", testing_frameworks=["pytest"])])
        shared = [c for c in conns if c.type == "shared_testing"]
        assert len(shared) == 0

    def test_integration_with_find_connections_testing(self):
        projects = [
            _proj("a", testing_frameworks=["Jest"]),
            _proj("b", testing_frameworks=["Jest", "Vitest"]),
        ]
        conns = find_connections(projects)
        testing_types = {c.type for c in conns if "testing" in c.type}
        assert "shared_testing" in testing_types

    def test_mixed_divergence_js_and_python(self):
        projects = [
            _proj("a", testing_frameworks=["pytest", "Jest"]),
            _proj("b", testing_frameworks=["nose2", "Vitest"]),
        ]
        conns = _find_testing_patterns(projects)
        div = [c for c in conns if c.type == "testing_divergence"]
        assert len(div) == 2  # one for JS, one for Python
