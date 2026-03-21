"""Tests for cross-project intelligence (connections/patterns)."""
from __future__ import annotations

from atlas.connections import (
    _find_ai_patterns,
    _find_ci_config_patterns,
    _find_docs_artifact_patterns,
    _find_health_gaps,
    _find_infra_patterns,
    _find_quality_patterns,
    _find_security_patterns,
    _find_database_patterns,
    _find_shared_deps,
    _find_shared_frameworks,
    _find_testing_patterns,
    _find_license_patterns,
    _find_package_manager_patterns,
    _find_runtime_version_patterns,
    _find_build_tool_patterns,
    _find_api_spec_patterns,
    _find_monitoring_patterns,
    _find_auth_patterns,
    _find_messaging_patterns,
    _find_deploy_target_patterns,
    _find_version_mismatches,
    _find_validation_patterns,
    _find_logging_patterns,
    _find_container_orchestration_patterns,
    _find_cloud_provider_patterns,
    _find_task_queue_patterns,
    find_connections,
)
from atlas.models import GitInfo, HealthScore, Project, TechStack


def _proj(name: str, frameworks=None, key_deps=None, databases=None,
          infrastructure=None, security_tools=None, quality_tools=None,
          ai_tools=None, testing_frameworks=None, package_managers=None,
          docs_artifacts=None, ci_config=None, runtime_versions=None,
          build_tools=None, api_specs=None, monitoring_tools=None,
          auth_tools=None, messaging_tools=None, deploy_targets=None,
          state_management=None, css_frameworks=None, bundlers=None, orm_tools=None, i18n_tools=None, validation_tools=None, logging_tools=None, container_orchestration=None, cloud_providers=None, task_queues=None, search_engines=None, project_license="",
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
            package_managers=package_managers or [],
            docs_artifacts=docs_artifacts or [],
            ci_config=ci_config or [],
            runtime_versions=runtime_versions or {},
            build_tools=build_tools or [],
            api_specs=api_specs or [],
            monitoring_tools=monitoring_tools or [],
            auth_tools=auth_tools or [],
            messaging_tools=messaging_tools or [],
            deploy_targets=deploy_targets or [],
            state_management=state_management or [],
            css_frameworks=css_frameworks or [],
            bundlers=bundlers or [],
            orm_tools=orm_tools or [],
            i18n_tools=i18n_tools or [],
            validation_tools=validation_tools or [],
            logging_tools=logging_tools or [],
            container_orchestration=container_orchestration or [],
            cloud_providers=cloud_providers or [],
            task_queues=task_queues or [],
            search_engines=search_engines or [],
        ),
        git_info=GitInfo(total_commits=git_commits, uncommitted_changes=uncommitted),
        health=HealthScore(structure=structure_score),
        test_file_count=test_files,
        source_file_count=source_files,
        license=project_license,
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
# _find_database_patterns
# ---------------------------------------------------------------------------
class TestFindDatabasePatterns:
    def test_shared_db(self):
        projects = [
            _proj("a", databases=["PostgreSQL"]),
            _proj("b", databases=["PostgreSQL"]),
        ]
        conns = _find_database_patterns(projects)
        shared = [c for c in conns if c.type == "shared_database"]
        assert len(shared) == 1
        assert "PostgreSQL" in shared[0].detail

    def test_no_shared_db(self):
        projects = [
            _proj("a", databases=["PostgreSQL"]),
            _proj("b", databases=["Redis"]),
        ]
        shared = [c for c in _find_database_patterns(projects) if c.type == "shared_database"]
        assert shared == []

    def test_single_project(self):
        projects = [_proj("a", databases=["PostgreSQL"])]
        shared = [c for c in _find_database_patterns(projects) if c.type == "shared_database"]
        assert shared == []

    def test_limit_10(self):
        dbs = [f"db{i}" for i in range(15)]
        projects = [_proj("a", databases=dbs), _proj("b", databases=dbs)]
        conns = _find_database_patterns(projects)
        assert len(conns) <= 10

    def test_shared_severity_is_info(self):
        projects = [
            _proj("a", databases=["Redis"]),
            _proj("b", databases=["Redis"]),
        ]
        conns = _find_database_patterns(projects)
        shared = [c for c in conns if c.type == "shared_database"]
        assert shared[0].severity == "info"

    def test_relational_divergence(self):
        projects = [
            _proj("a", databases=["PostgreSQL"]),
            _proj("b", databases=["MySQL"]),
        ]
        conns = _find_database_patterns(projects)
        div = [c for c in conns if c.type == "database_divergence"]
        assert len(div) == 1
        assert "relational" in div[0].detail.lower()
        assert div[0].severity == "warning"

    def test_no_relational_divergence_same_db(self):
        projects = [
            _proj("a", databases=["PostgreSQL"]),
            _proj("b", databases=["PostgreSQL"]),
        ]
        conns = _find_database_patterns(projects)
        div = [c for c in conns if c.type == "database_divergence"]
        assert len(div) == 0

    def test_sqlite_excluded_from_relational_divergence(self):
        projects = [
            _proj("a", databases=["PostgreSQL", "SQLite"]),
            _proj("b", databases=["PostgreSQL"]),
        ]
        conns = _find_database_patterns(projects)
        div = [c for c in conns if c.type == "database_divergence" and "relational" in c.detail.lower()]
        assert len(div) == 0

    def test_vector_db_divergence(self):
        projects = [
            _proj("a", databases=["ChromaDB"]),
            _proj("b", databases=["Pinecone"]),
        ]
        conns = _find_database_patterns(projects)
        div = [c for c in conns if c.type == "database_divergence" and "vector" in c.detail.lower()]
        assert len(div) == 1
        assert div[0].severity == "warning"

    def test_no_vector_divergence_same_db(self):
        projects = [
            _proj("a", databases=["ChromaDB"]),
            _proj("b", databases=["ChromaDB"]),
        ]
        conns = _find_database_patterns(projects)
        div = [c for c in conns if c.type == "database_divergence" and "vector" in c.detail.lower()]
        assert len(div) == 0

    def test_broker_divergence(self):
        projects = [
            _proj("a", databases=["RabbitMQ"]),
            _proj("b", databases=["Kafka"]),
        ]
        conns = _find_database_patterns(projects)
        div = [c for c in conns if c.type == "database_divergence" and "broker" in c.detail.lower()]
        assert len(div) == 1

    def test_database_gap_web_no_db(self):
        projects = [
            _proj("a", frameworks=["FastAPI"], databases=["PostgreSQL"]),
            _proj("b", frameworks=["FastAPI"], databases=[]),
        ]
        conns = _find_database_patterns(projects)
        gap = [c for c in conns if c.type == "database_gap"]
        assert len(gap) == 1
        assert "b" in gap[0].projects
        assert gap[0].severity == "warning"

    def test_no_gap_non_web_project(self):
        projects = [
            _proj("a", frameworks=[], databases=[]),
            _proj("b", frameworks=[], databases=[]),
        ]
        conns = _find_database_patterns(projects)
        gap = [c for c in conns if c.type == "database_gap"]
        assert len(gap) == 0

    def test_no_gap_all_have_db(self):
        projects = [
            _proj("a", frameworks=["Django"], databases=["PostgreSQL"]),
            _proj("b", frameworks=["Express"], databases=["MongoDB"]),
        ]
        conns = _find_database_patterns(projects)
        gap = [c for c in conns if c.type == "database_gap"]
        assert len(gap) == 0

    def test_empty_projects(self):
        conns = _find_database_patterns([])
        assert conns == []

    def test_integration_with_find_connections_database(self):
        projects = [
            _proj("a", databases=["PostgreSQL"]),
            _proj("b", databases=["PostgreSQL", "MySQL"]),
        ]
        conns = find_connections(projects)
        db_types = {c.type for c in conns if "database" in c.type}
        assert "shared_database" in db_types


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


# ---------------------------------------------------------------------------
# Package manager patterns (N-35)
# ---------------------------------------------------------------------------
class TestFindPackageManagerPatterns:
    def test_shared_package_manager(self):
        projects = [
            _proj("a", package_managers=["Poetry"]),
            _proj("b", package_managers=["Poetry"]),
        ]
        conns = _find_package_manager_patterns(projects)
        shared = [c for c in conns if c.type == "shared_pkg_manager"]
        assert len(shared) == 1
        assert "Poetry" in shared[0].detail
        assert shared[0].severity == "info"

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", package_managers=["Poetry"]),
            _proj("b", package_managers=["npm"]),
        ]
        conns = _find_package_manager_patterns(projects)
        shared = [c for c in conns if c.type == "shared_pkg_manager"]
        assert len(shared) == 0

    def test_js_divergence_npm_vs_yarn(self):
        projects = [
            _proj("a", package_managers=["npm"]),
            _proj("b", package_managers=["Yarn"]),
        ]
        conns = _find_package_manager_patterns(projects)
        div = [c for c in conns if c.type == "pkg_manager_divergence"]
        assert len(div) == 1
        assert "JS package managers" in div[0].detail
        assert div[0].severity == "warning"

    def test_js_divergence_three_managers(self):
        projects = [
            _proj("a", package_managers=["npm"]),
            _proj("b", package_managers=["Yarn"]),
            _proj("c", package_managers=["pnpm"]),
        ]
        conns = _find_package_manager_patterns(projects)
        div = [c for c in conns if c.type == "pkg_manager_divergence" and "JS" in c.detail]
        assert len(div) == 1
        assert "npm" in div[0].detail
        assert "Yarn" in div[0].detail
        assert "pnpm" in div[0].detail

    def test_no_js_divergence_same_manager(self):
        projects = [
            _proj("a", package_managers=["pnpm"]),
            _proj("b", package_managers=["pnpm"]),
        ]
        conns = _find_package_manager_patterns(projects)
        div = [c for c in conns if c.type == "pkg_manager_divergence"]
        assert len(div) == 0

    def test_python_divergence_pip_vs_poetry(self):
        projects = [
            _proj("a", package_managers=["pip"]),
            _proj("b", package_managers=["Poetry"]),
        ]
        conns = _find_package_manager_patterns(projects)
        div = [c for c in conns if c.type == "pkg_manager_divergence" and "Python" in c.detail]
        assert len(div) == 1

    def test_no_python_divergence_same_manager(self):
        projects = [
            _proj("a", package_managers=["Poetry"]),
            _proj("b", package_managers=["Poetry"]),
        ]
        conns = _find_package_manager_patterns(projects)
        div = [c for c in conns if c.type == "pkg_manager_divergence" and "Python" in c.detail]
        assert len(div) == 0

    def test_java_divergence_maven_vs_gradle(self):
        projects = [
            _proj("a", package_managers=["Maven"]),
            _proj("b", package_managers=["Gradle"]),
        ]
        conns = _find_package_manager_patterns(projects)
        div = [c for c in conns if c.type == "pkg_manager_divergence" and "Java" in c.detail]
        assert len(div) == 1

    def test_mixed_divergence_js_and_python(self):
        projects = [
            _proj("a", package_managers=["pip", "npm"]),
            _proj("b", package_managers=["Poetry", "Yarn"]),
        ]
        conns = _find_package_manager_patterns(projects)
        div = [c for c in conns if c.type == "pkg_manager_divergence"]
        assert len(div) == 2  # one JS, one Python

    def test_empty_projects(self):
        conns = _find_package_manager_patterns([])
        assert conns == []


# ---------------------------------------------------------------------------
# License patterns (N-38)
# ---------------------------------------------------------------------------
class TestFindLicensePatterns:
    def test_shared_license(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="MIT"),
            _proj("c", project_license="Apache-2.0"),
        ]
        conns = _find_license_patterns(projects)
        shared = [c for c in conns if c.type == "shared_license"]
        assert len(shared) == 1
        assert "MIT" in shared[0].detail
        assert shared[0].severity == "info"

    def test_no_shared_when_all_different(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="Apache-2.0"),
            _proj("c", project_license="ISC"),
        ]
        conns = _find_license_patterns(projects)
        shared = [c for c in conns if c.type == "shared_license"]
        assert len(shared) == 0

    def test_license_divergence_permissive(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="Apache-2.0"),
        ]
        conns = _find_license_patterns(projects)
        div = [c for c in conns if c.type == "license_divergence"]
        assert len(div) == 1
        assert div[0].severity == "warning"
        assert "standardizing" in div[0].detail

    def test_license_divergence_copyleft_mix(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="GPL-3.0"),
        ]
        conns = _find_license_patterns(projects)
        div = [c for c in conns if c.type == "license_divergence"]
        assert len(div) == 1
        assert div[0].severity == "critical"
        assert "Copyleft/permissive mix" in div[0].detail

    def test_no_divergence_same_license(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="MIT"),
        ]
        conns = _find_license_patterns(projects)
        div = [c for c in conns if c.type == "license_divergence"]
        assert len(div) == 0

    def test_license_gap(self):
        projects = [
            _proj("a", project_license="MIT", source_files=20),
            _proj("b", project_license="", source_files=20),
        ]
        conns = _find_license_patterns(projects)
        gap = [c for c in conns if c.type == "license_gap"]
        assert len(gap) == 1
        assert "b" in gap[0].projects
        assert gap[0].severity == "warning"

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", project_license="MIT", source_files=20),
            _proj("b", project_license="", source_files=3),
        ]
        conns = _find_license_patterns(projects)
        gap = [c for c in conns if c.type == "license_gap"]
        assert len(gap) == 0

    def test_no_gap_all_licensed(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="Apache-2.0"),
        ]
        conns = _find_license_patterns(projects)
        gap = [c for c in conns if c.type == "license_gap"]
        assert len(gap) == 0

    def test_multiple_gaps(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="", source_files=20),
            _proj("c", project_license="", source_files=15),
        ]
        conns = _find_license_patterns(projects)
        gap = [c for c in conns if c.type == "license_gap"]
        assert len(gap) == 1
        assert "2 project(s)" in gap[0].detail
        assert "b" in gap[0].projects
        assert "c" in gap[0].projects

    def test_agpl_copyleft_detection(self):
        projects = [
            _proj("a", project_license="Apache-2.0"),
            _proj("b", project_license="AGPL-3.0"),
        ]
        conns = _find_license_patterns(projects)
        div = [c for c in conns if c.type == "license_divergence"]
        assert len(div) == 1
        assert div[0].severity == "critical"

    def test_lgpl_copyleft_detection(self):
        projects = [
            _proj("a", project_license="MIT"),
            _proj("b", project_license="LGPL-3.0"),
        ]
        conns = _find_license_patterns(projects)
        div = [c for c in conns if c.type == "license_divergence"]
        assert len(div) == 1
        assert div[0].severity == "critical"

    def test_empty_projects(self):
        conns = _find_license_patterns([])
        assert conns == []

    def test_all_unlicensed(self):
        projects = [
            _proj("a", project_license="", source_files=20),
            _proj("b", project_license="", source_files=20),
        ]
        conns = _find_license_patterns(projects)
        # No shared/divergence, just gap
        shared = [c for c in conns if c.type == "shared_license"]
        div = [c for c in conns if c.type == "license_divergence"]
        gap = [c for c in conns if c.type == "license_gap"]
        assert len(shared) == 0
        assert len(div) == 0
        assert len(gap) == 1

    def test_single_project(self):
        conns = _find_package_manager_patterns([_proj("solo", package_managers=["Poetry"])])
        shared = [c for c in conns if c.type == "shared_pkg_manager"]
        assert len(shared) == 0

    def test_multiple_shared(self):
        projects = [
            _proj("a", package_managers=["Poetry", "npm"]),
            _proj("b", package_managers=["Poetry", "npm"]),
        ]
        conns = _find_package_manager_patterns(projects)
        shared = [c for c in conns if c.type == "shared_pkg_manager"]
        assert len(shared) == 2

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", package_managers=["npm"]),
            _proj("b", package_managers=["npm", "Yarn"]),
        ]
        conns = find_connections(projects)
        pm_types = {c.type for c in conns if "pkg_manager" in c.type}
        assert "shared_pkg_manager" in pm_types


# ---------------------------------------------------------------------------
# _find_docs_artifact_patterns
# ---------------------------------------------------------------------------
class TestFindDocsArtifactPatterns:
    def test_shared_docs_basic(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG"]),
            _proj("b", docs_artifacts=["README", "LICENSE"]),
        ]
        conns = _find_docs_artifact_patterns(projects)
        shared = [c for c in conns if c.type == "shared_docs"]
        assert len(shared) == 1
        assert "README" in shared[0].detail

    def test_shared_multiple_artifacts(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG", "LICENSE"]),
            _proj("b", docs_artifacts=["README", "CHANGELOG", "LICENSE"]),
        ]
        conns = _find_docs_artifact_patterns(projects)
        shared = [c for c in conns if c.type == "shared_docs"]
        assert len(shared) == 3

    def test_no_shared_when_different(self):
        projects = [
            _proj("a", docs_artifacts=["README"]),
            _proj("b", docs_artifacts=["CHANGELOG"]),
        ]
        conns = _find_docs_artifact_patterns(projects)
        shared = [c for c in conns if c.type == "shared_docs"]
        assert len(shared) == 0

    def test_shared_severity_info(self):
        projects = [
            _proj("a", docs_artifacts=["README"]),
            _proj("b", docs_artifacts=["README"]),
        ]
        conns = _find_docs_artifact_patterns(projects)
        shared = [c for c in conns if c.type == "shared_docs"]
        assert shared[0].severity == "info"

    def test_docs_divergence_rich_vs_minimal(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG", "CONTRIBUTING", "LICENSE", "docs/"],
                  source_files=20),
            _proj("b", docs_artifacts=["README"], source_files=20),
        ]
        conns = _find_docs_artifact_patterns(projects)
        div = [c for c in conns if c.type == "docs_divergence"]
        assert len(div) == 1
        assert div[0].severity == "warning"

    def test_no_divergence_all_rich(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG", "CONTRIBUTING", "LICENSE", "docs/"]),
            _proj("b", docs_artifacts=["README", "CHANGELOG", "CONTRIBUTING", "LICENSE", "SECURITY"]),
        ]
        conns = _find_docs_artifact_patterns(projects)
        div = [c for c in conns if c.type == "docs_divergence"]
        assert len(div) == 0

    def test_no_divergence_all_minimal(self):
        projects = [
            _proj("a", docs_artifacts=["README"], source_files=20),
            _proj("b", docs_artifacts=["README"], source_files=20),
        ]
        conns = _find_docs_artifact_patterns(projects)
        div = [c for c in conns if c.type == "docs_divergence"]
        assert len(div) == 0

    def test_minimal_not_flagged_for_small_projects(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG", "CONTRIBUTING", "LICENSE", "docs/"]),
            _proj("b", docs_artifacts=["README"], source_files=3),
        ]
        conns = _find_docs_artifact_patterns(projects)
        div = [c for c in conns if c.type == "docs_divergence"]
        assert len(div) == 0

    def test_readme_gap(self):
        projects = [
            _proj("a", docs_artifacts=[], source_files=20),
            _proj("b", docs_artifacts=["README"], source_files=20),
        ]
        conns = _find_docs_artifact_patterns(projects)
        gaps = [c for c in conns if c.type == "docs_gap" and "README" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "critical"
        assert "a" in gaps[0].projects

    def test_no_readme_gap_for_small_projects(self):
        projects = [
            _proj("a", docs_artifacts=[], source_files=3),
        ]
        conns = _find_docs_artifact_patterns(projects)
        gaps = [c for c in conns if c.type == "docs_gap" and "README" in c.detail]
        assert len(gaps) == 0

    def test_changelog_gap(self):
        projects = [
            _proj("a", docs_artifacts=["README"], source_files=15),
        ]
        conns = _find_docs_artifact_patterns(projects)
        gaps = [c for c in conns if c.type == "docs_gap" and "CHANGELOG" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_no_changelog_gap_for_small_projects(self):
        projects = [
            _proj("a", docs_artifacts=["README"], source_files=8),
        ]
        conns = _find_docs_artifact_patterns(projects)
        gaps = [c for c in conns if c.type == "docs_gap" and "CHANGELOG" in c.detail]
        assert len(gaps) == 0

    def test_contributing_gap(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG"], source_files=25),
        ]
        conns = _find_docs_artifact_patterns(projects)
        gaps = [c for c in conns if c.type == "docs_gap" and "CONTRIBUTING" in c.detail]
        assert len(gaps) == 1

    def test_no_contributing_gap_for_small_projects(self):
        projects = [
            _proj("a", docs_artifacts=["README"], source_files=15),
        ]
        conns = _find_docs_artifact_patterns(projects)
        gaps = [c for c in conns if c.type == "docs_gap" and "CONTRIBUTING" in c.detail]
        assert len(gaps) == 0

    def test_empty_projects(self):
        conns = _find_docs_artifact_patterns([])
        assert conns == []

    def test_all_well_documented(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG", "CONTRIBUTING", "LICENSE", "docs/"]),
            _proj("b", docs_artifacts=["README", "CHANGELOG", "CONTRIBUTING", "LICENSE", "docs/"]),
        ]
        conns = _find_docs_artifact_patterns(projects)
        gaps = [c for c in conns if c.type == "docs_gap"]
        div = [c for c in conns if c.type == "docs_divergence"]
        assert len(gaps) == 0
        assert len(div) == 0

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", docs_artifacts=["README", "CHANGELOG"],
                  project_license="MIT", source_files=20),
            _proj("b", docs_artifacts=["README"],
                  project_license="MIT", source_files=20),
        ]
        conns = find_connections(projects)
        docs_types = {c.type for c in conns if "docs" in c.type}
        assert "shared_docs" in docs_types


class TestFindCiConfigPatterns:
    """Tests for _find_ci_config_patterns()."""

    # --- Shared CI config ---

    def test_shared_ci_config_two_projects(self):
        projects = [
            _proj("a", ci_config=["GitHub Actions", "pre-commit"]),
            _proj("b", ci_config=["GitHub Actions", "PR template"]),
        ]
        conns = _find_ci_config_patterns(projects)
        shared = [c for c in conns if c.type == "shared_ci_config"]
        assert len(shared) >= 1
        gh_shared = [c for c in shared if "GitHub Actions" in c.detail]
        assert len(gh_shared) == 1
        assert gh_shared[0].severity == "info"

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", ci_config=["GitHub Actions"]),
            _proj("b", ci_config=["GitLab CI"]),
        ]
        conns = _find_ci_config_patterns(projects)
        shared = [c for c in conns if c.type == "shared_ci_config"]
        assert len(shared) == 0

    def test_shared_sorted_by_count(self):
        projects = [
            _proj("a", ci_config=["GitHub Actions", "pre-commit"]),
            _proj("b", ci_config=["GitHub Actions", "pre-commit"]),
            _proj("c", ci_config=["GitHub Actions"]),
        ]
        conns = _find_ci_config_patterns(projects)
        shared = [c for c in conns if c.type == "shared_ci_config"]
        # GitHub Actions in 3 projects should come first
        assert "3 projects" in shared[0].detail

    # --- Dep update strategy divergence ---

    def test_dep_update_divergence(self):
        projects = [
            _proj("a", ci_config=["Dependabot config"]),
            _proj("b", ci_config=["Renovate config"]),
        ]
        conns = _find_ci_config_patterns(projects)
        div = [c for c in conns if c.type == "ci_config_divergence"]
        assert len(div) == 1
        assert "dep update" in div[0].detail.lower()
        assert div[0].severity == "warning"

    def test_no_divergence_same_strategy(self):
        projects = [
            _proj("a", ci_config=["Dependabot config"]),
            _proj("b", ci_config=["Dependabot config"]),
        ]
        conns = _find_ci_config_patterns(projects)
        div = [c for c in conns if c.type == "ci_config_divergence"]
        assert len(div) == 0

    def test_no_divergence_no_dep_updates(self):
        projects = [
            _proj("a", ci_config=["GitHub Actions"]),
            _proj("b", ci_config=["pre-commit"]),
        ]
        conns = _find_ci_config_patterns(projects)
        div = [c for c in conns if c.type == "ci_config_divergence"]
        assert len(div) == 0

    # --- PR template gap ---

    def test_pr_template_gap(self):
        projects = [
            _proj("a", ci_config=[], infrastructure=["GitHub Actions"],
                  source_files=15),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "PR template" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_no_pr_template_gap_when_present(self):
        projects = [
            _proj("a", ci_config=["PR template"],
                  infrastructure=["GitHub Actions"], source_files=15),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "PR template" in c.detail]
        assert len(gaps) == 0

    def test_no_pr_template_gap_without_ci(self):
        projects = [
            _proj("a", ci_config=[], infrastructure=[], source_files=15),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "PR template" in c.detail]
        assert len(gaps) == 0

    def test_no_pr_template_gap_small_project(self):
        projects = [
            _proj("a", ci_config=[], infrastructure=["GitHub Actions"],
                  source_files=8),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "PR template" in c.detail]
        assert len(gaps) == 0

    # --- CODEOWNERS gap ---

    def test_codeowners_gap(self):
        projects = [
            _proj("a", ci_config=[], source_files=25),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "CODEOWNERS" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_no_codeowners_gap_when_present(self):
        projects = [
            _proj("a", ci_config=["CODEOWNERS"], source_files=25),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "CODEOWNERS" in c.detail]
        assert len(gaps) == 0

    def test_no_codeowners_gap_small_project(self):
        projects = [
            _proj("a", ci_config=[], source_files=15),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "CODEOWNERS" in c.detail]
        assert len(gaps) == 0

    # --- Pre-commit gap ---

    def test_precommit_gap(self):
        projects = [
            _proj("a", ci_config=[], quality_tools=["Ruff", "mypy"],
                  source_files=10),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "pre-commit" in c.detail]
        assert len(gaps) == 1
        assert gaps[0].severity == "warning"

    def test_no_precommit_gap_when_present(self):
        projects = [
            _proj("a", ci_config=["pre-commit"], quality_tools=["Ruff"],
                  source_files=10),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "pre-commit" in c.detail]
        assert len(gaps) == 0

    def test_no_precommit_gap_without_quality_tools(self):
        projects = [
            _proj("a", ci_config=[], quality_tools=[], source_files=10),
        ]
        conns = _find_ci_config_patterns(projects)
        gaps = [c for c in conns if c.type == "ci_config_gap"
                and "pre-commit" in c.detail]
        assert len(gaps) == 0

    # --- Integration ---

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", ci_config=["GitHub Actions", "pre-commit"],
                  source_files=20),
            _proj("b", ci_config=["GitHub Actions", "PR template"],
                  source_files=20),
        ]
        conns = find_connections(projects)
        ci_types = {c.type for c in conns if "ci_config" in c.type}
        assert "shared_ci_config" in ci_types


class TestFindRuntimeVersionPatterns:
    """Tests for _find_runtime_version_patterns()."""

    # --- Shared runtime versions ---

    def test_shared_runtime_two_projects(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={"Python": "3.11"}),
        ]
        conns = _find_runtime_version_patterns(projects)
        shared = [c for c in conns if c.type == "shared_runtime"]
        assert len(shared) == 1
        assert "Python" in shared[0].detail
        assert shared[0].severity == "info"

    def test_no_shared_when_different_languages(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={"Node": "20.11"}),
        ]
        conns = _find_runtime_version_patterns(projects)
        shared = [c for c in conns if c.type == "shared_runtime"]
        assert len(shared) == 0

    def test_shared_sorted_by_count(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12", "Node": "20"}),
            _proj("b", runtime_versions={"Python": "3.12", "Node": "20"}),
            _proj("c", runtime_versions={"Python": "3.11"}),
        ]
        conns = _find_runtime_version_patterns(projects)
        shared = [c for c in conns if c.type == "shared_runtime"]
        # Python in 3 projects should come first
        assert "3 projects" in shared[0].detail

    # --- Runtime version divergence ---

    def test_version_divergence_same_language(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={"Python": "3.11"}),
        ]
        conns = _find_runtime_version_patterns(projects)
        div = [c for c in conns if c.type == "runtime_divergence"]
        assert len(div) == 1
        assert "Python" in div[0].detail
        assert "3.12" in div[0].detail
        assert "3.11" in div[0].detail
        assert div[0].severity == "warning"

    def test_no_divergence_same_version(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={"Python": "3.12"}),
        ]
        conns = _find_runtime_version_patterns(projects)
        div = [c for c in conns if c.type == "runtime_divergence"]
        assert len(div) == 0

    def test_no_divergence_different_languages(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={"Node": "20"}),
        ]
        conns = _find_runtime_version_patterns(projects)
        div = [c for c in conns if c.type == "runtime_divergence"]
        assert len(div) == 0

    def test_divergence_shows_project_names(self):
        projects = [
            _proj("alpha", runtime_versions={"Node": "18"}),
            _proj("beta", runtime_versions={"Node": "20"}),
        ]
        conns = _find_runtime_version_patterns(projects)
        div = [c for c in conns if c.type == "runtime_divergence"]
        assert len(div) == 1
        assert "alpha" in div[0].detail
        assert "beta" in div[0].detail

    # --- Runtime version pinning gap ---

    def test_runtime_gap(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={}, source_files=10),
        ]
        conns = _find_runtime_version_patterns(projects)
        gaps = [c for c in conns if c.type == "runtime_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_when_all_pinned(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={"Node": "20"}),
        ]
        conns = _find_runtime_version_patterns(projects)
        gaps = [c for c in conns if c.type == "runtime_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_none_pinned(self):
        projects = [
            _proj("a", runtime_versions={}),
            _proj("b", runtime_versions={}),
        ]
        conns = _find_runtime_version_patterns(projects)
        gaps = [c for c in conns if c.type == "runtime_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={}, source_files=3),
        ]
        conns = _find_runtime_version_patterns(projects)
        gaps = [c for c in conns if c.type == "runtime_gap"]
        assert len(gaps) == 0

    # --- Integration ---

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", runtime_versions={"Python": "3.12"}),
            _proj("b", runtime_versions={"Python": "3.11"}),
        ]
        conns = find_connections(projects)
        runtime_types = {c.type for c in conns if "runtime" in c.type}
        assert "shared_runtime" in runtime_types
        assert "runtime_divergence" in runtime_types


class TestFindBuildToolPatterns:
    """Tests for _find_build_tool_patterns()."""

    # --- Shared build tools ---

    def test_shared_build_tool_two_projects(self):
        projects = [
            _proj("a", build_tools=["Make", "tox"]),
            _proj("b", build_tools=["Make", "npm scripts"]),
        ]
        conns = _find_build_tool_patterns(projects)
        shared = [c for c in conns if c.type == "shared_build_tool"]
        assert len(shared) >= 1
        make_shared = [c for c in shared if "Make" in c.detail]
        assert len(make_shared) == 1
        assert make_shared[0].severity == "info"

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", build_tools=["Make"]),
            _proj("b", build_tools=["Gradle"]),
        ]
        conns = _find_build_tool_patterns(projects)
        shared = [c for c in conns if c.type == "shared_build_tool"]
        assert len(shared) == 0

    def test_shared_sorted_by_count(self):
        projects = [
            _proj("a", build_tools=["Make", "tox"]),
            _proj("b", build_tools=["Make", "tox"]),
            _proj("c", build_tools=["Make"]),
        ]
        conns = _find_build_tool_patterns(projects)
        shared = [c for c in conns if c.type == "shared_build_tool"]
        assert "3 projects" in shared[0].detail

    # --- Python task runner divergence ---

    def test_python_runner_divergence(self):
        projects = [
            _proj("a", build_tools=["tox"]),
            _proj("b", build_tools=["nox"]),
        ]
        conns = _find_build_tool_patterns(projects)
        div = [c for c in conns if c.type == "build_tool_divergence"]
        assert len(div) == 1
        assert "Python task runners" in div[0].detail
        assert div[0].severity == "warning"

    def test_no_python_divergence_same_runner(self):
        projects = [
            _proj("a", build_tools=["tox"]),
            _proj("b", build_tools=["tox"]),
        ]
        conns = _find_build_tool_patterns(projects)
        div = [c for c in conns if c.type == "build_tool_divergence"
               and "Python" in c.detail]
        assert len(div) == 0

    def test_no_python_divergence_no_runners(self):
        projects = [
            _proj("a", build_tools=["Make"]),
            _proj("b", build_tools=["Gradle"]),
        ]
        conns = _find_build_tool_patterns(projects)
        div = [c for c in conns if c.type == "build_tool_divergence"
               and "Python" in c.detail]
        assert len(div) == 0

    # --- Java build tool divergence ---

    def test_java_build_divergence(self):
        projects = [
            _proj("a", build_tools=["Gradle"]),
            _proj("b", build_tools=["Maven"]),
        ]
        conns = _find_build_tool_patterns(projects)
        div = [c for c in conns if c.type == "build_tool_divergence"
               and "Java" in c.detail]
        assert len(div) == 1
        assert div[0].severity == "warning"

    def test_no_java_divergence_same_tool(self):
        projects = [
            _proj("a", build_tools=["Gradle"]),
            _proj("b", build_tools=["Gradle"]),
        ]
        conns = _find_build_tool_patterns(projects)
        div = [c for c in conns if c.type == "build_tool_divergence"
               and "Java" in c.detail]
        assert len(div) == 0

    # --- Build automation gap ---

    def test_build_gap(self):
        projects = [
            _proj("a", build_tools=["Make"]),
            _proj("b", build_tools=[], source_files=15),
        ]
        conns = _find_build_tool_patterns(projects)
        gaps = [c for c in conns if c.type == "build_tool_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_when_all_have_tools(self):
        projects = [
            _proj("a", build_tools=["Make"]),
            _proj("b", build_tools=["tox"]),
        ]
        conns = _find_build_tool_patterns(projects)
        gaps = [c for c in conns if c.type == "build_tool_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_none_have_tools(self):
        projects = [
            _proj("a", build_tools=[]),
            _proj("b", build_tools=[]),
        ]
        conns = _find_build_tool_patterns(projects)
        gaps = [c for c in conns if c.type == "build_tool_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", build_tools=["Make"]),
            _proj("b", build_tools=[], source_files=5),
        ]
        conns = _find_build_tool_patterns(projects)
        gaps = [c for c in conns if c.type == "build_tool_gap"]
        assert len(gaps) == 0

    # --- Integration ---

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", build_tools=["Make", "tox"]),
            _proj("b", build_tools=["Make", "nox"]),
        ]
        conns = find_connections(projects)
        build_types = {c.type for c in conns if "build_tool" in c.type}
        assert "shared_build_tool" in build_types
        assert "build_tool_divergence" in build_types


# ---------------------------------------------------------------------------
# _find_api_spec_patterns (N-53)
# ---------------------------------------------------------------------------
class TestFindApiSpecPatterns:
    # --- Shared API specs ---

    def test_shared_api_spec(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"]),
            _proj("b", api_specs=["OpenAPI"]),
        ]
        conns = _find_api_spec_patterns(projects)
        shared = [c for c in conns if c.type == "shared_api_spec"]
        assert len(shared) == 1
        assert "OpenAPI" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_multiple_specs(self):
        projects = [
            _proj("a", api_specs=["OpenAPI", "GraphQL"]),
            _proj("b", api_specs=["OpenAPI", "GraphQL"]),
        ]
        conns = _find_api_spec_patterns(projects)
        shared = [c for c in conns if c.type == "shared_api_spec"]
        assert len(shared) == 2

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"]),
            _proj("b", api_specs=["GraphQL"]),
        ]
        conns = _find_api_spec_patterns(projects)
        shared = [c for c in conns if c.type == "shared_api_spec"]
        assert len(shared) == 0

    def test_shared_needs_two_projects(self):
        projects = [_proj("a", api_specs=["OpenAPI"])]
        conns = _find_api_spec_patterns(projects)
        shared = [c for c in conns if c.type == "shared_api_spec"]
        assert len(shared) == 0

    # --- API paradigm divergence ---

    def test_rest_vs_graphql_divergence(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"]),
            _proj("b", api_specs=["GraphQL"]),
        ]
        conns = _find_api_spec_patterns(projects)
        div = [c for c in conns if c.type == "api_spec_divergence"]
        assert len(div) == 1
        assert "REST" in div[0].detail
        assert "GraphQL" in div[0].detail
        assert div[0].severity == "info"

    def test_rest_vs_rpc_divergence(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"]),
            _proj("b", api_specs=["gRPC/Protobuf"]),
        ]
        conns = _find_api_spec_patterns(projects)
        div = [c for c in conns if c.type == "api_spec_divergence"]
        assert len(div) == 1
        assert "REST" in div[0].detail
        assert "RPC" in div[0].detail

    def test_no_divergence_same_paradigm(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"]),
            _proj("b", api_specs=["AsyncAPI"]),
        ]
        conns = _find_api_spec_patterns(projects)
        div = [c for c in conns if c.type == "api_spec_divergence"]
        assert len(div) == 0

    def test_three_paradigm_divergence(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"]),
            _proj("b", api_specs=["GraphQL"]),
            _proj("c", api_specs=["tRPC"]),
        ]
        conns = _find_api_spec_patterns(projects)
        div = [c for c in conns if c.type == "api_spec_divergence"]
        assert len(div) == 1
        assert len(div[0].projects) == 3

    # --- API spec gap ---

    def test_api_gap_web_framework_no_spec(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"], frameworks=["FastAPI"]),
            _proj("b", api_specs=[], frameworks=["Flask"], source_files=20),
        ]
        conns = _find_api_spec_patterns(projects)
        gaps = [c for c in conns if c.type == "api_spec_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_when_all_have_specs(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"], frameworks=["FastAPI"]),
            _proj("b", api_specs=["GraphQL"], frameworks=["Express"]),
        ]
        conns = _find_api_spec_patterns(projects)
        gaps = [c for c in conns if c.type == "api_spec_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_no_web_frameworks(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"]),
            _proj("b", api_specs=[], frameworks=["React"], source_files=20),
        ]
        conns = _find_api_spec_patterns(projects)
        gaps = [c for c in conns if c.type == "api_spec_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", api_specs=["OpenAPI"], frameworks=["FastAPI"]),
            _proj("b", api_specs=[], frameworks=["Flask"], source_files=3),
        ]
        conns = _find_api_spec_patterns(projects)
        gaps = [c for c in conns if c.type == "api_spec_gap"]
        assert len(gaps) == 0

    # --- Edge cases ---

    def test_empty_projects(self):
        conns = _find_api_spec_patterns([])
        assert conns == []

    def test_no_specs_no_connections(self):
        projects = [
            _proj("a", api_specs=[]),
            _proj("b", api_specs=[]),
        ]
        conns = _find_api_spec_patterns(projects)
        assert len(conns) == 0

    def test_limit_10(self):
        specs = [f"Spec{i}" for i in range(20)]
        projects = [_proj("a", api_specs=specs), _proj("b", api_specs=specs)]
        conns = _find_api_spec_patterns(projects)
        assert len(conns) <= 10

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", api_specs=["OpenAPI", "GraphQL"]),
            _proj("b", api_specs=["OpenAPI", "gRPC/Protobuf"]),
        ]
        conns = find_connections(projects)
        api_types = {c.type for c in conns if "api_spec" in c.type}
        assert "shared_api_spec" in api_types
        assert "api_spec_divergence" in api_types


# ---------------------------------------------------------------------------
# _find_monitoring_patterns (N-56)
# ---------------------------------------------------------------------------
class TestFindMonitoringPatterns:
    # --- Shared monitoring tools ---

    def test_shared_monitoring_tool(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry", "Datadog"]),
            _proj("b", monitoring_tools=["Sentry"]),
        ]
        conns = _find_monitoring_patterns(projects)
        shared = [c for c in conns if c.type == "shared_monitoring"]
        assert len(shared) == 1
        assert "Sentry" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_multiple_tools(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry", "Datadog"]),
            _proj("b", monitoring_tools=["Sentry", "Datadog"]),
        ]
        conns = _find_monitoring_patterns(projects)
        shared = [c for c in conns if c.type == "shared_monitoring"]
        assert len(shared) == 2

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry"]),
            _proj("b", monitoring_tools=["Datadog"]),
        ]
        conns = _find_monitoring_patterns(projects)
        shared = [c for c in conns if c.type == "shared_monitoring"]
        assert len(shared) == 0

    def test_shared_needs_two_projects(self):
        projects = [_proj("a", monitoring_tools=["Sentry"])]
        conns = _find_monitoring_patterns(projects)
        shared = [c for c in conns if c.type == "shared_monitoring"]
        assert len(shared) == 0

    # --- Error tracking divergence ---

    def test_error_tracker_divergence(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry"]),
            _proj("b", monitoring_tools=["Bugsnag"]),
        ]
        conns = _find_monitoring_patterns(projects)
        div = [c for c in conns if c.type == "monitoring_divergence"
               and "error tracker" in c.detail.lower()]
        assert len(div) == 1
        assert "Sentry" in div[0].detail
        assert "Bugsnag" in div[0].detail
        assert div[0].severity == "warning"

    def test_no_error_tracker_divergence_same_tool(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry"]),
            _proj("b", monitoring_tools=["Sentry"]),
        ]
        conns = _find_monitoring_patterns(projects)
        div = [c for c in conns if c.type == "monitoring_divergence"
               and "error tracker" in c.detail.lower()]
        assert len(div) == 0

    # --- APM divergence ---

    def test_apm_divergence(self):
        projects = [
            _proj("a", monitoring_tools=["Datadog"]),
            _proj("b", monitoring_tools=["New Relic"]),
        ]
        conns = _find_monitoring_patterns(projects)
        div = [c for c in conns if c.type == "monitoring_divergence"
               and "APM" in c.detail]
        assert len(div) == 1
        assert "Datadog" in div[0].detail
        assert "New Relic" in div[0].detail
        assert div[0].severity == "warning"

    def test_no_apm_divergence_same_tool(self):
        projects = [
            _proj("a", monitoring_tools=["Datadog"]),
            _proj("b", monitoring_tools=["Datadog"]),
        ]
        conns = _find_monitoring_patterns(projects)
        div = [c for c in conns if c.type == "monitoring_divergence"
               and "APM" in c.detail]
        assert len(div) == 0

    # --- Monitoring gap ---

    def test_monitoring_gap(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry"]),
            _proj("b", monitoring_tools=[], source_files=15),
        ]
        conns = _find_monitoring_patterns(projects)
        gaps = [c for c in conns if c.type == "monitoring_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_when_all_have_monitoring(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry"]),
            _proj("b", monitoring_tools=["Datadog"]),
        ]
        conns = _find_monitoring_patterns(projects)
        gaps = [c for c in conns if c.type == "monitoring_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_none_have_monitoring(self):
        projects = [
            _proj("a", monitoring_tools=[]),
            _proj("b", monitoring_tools=[]),
        ]
        conns = _find_monitoring_patterns(projects)
        gaps = [c for c in conns if c.type == "monitoring_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry"]),
            _proj("b", monitoring_tools=[], source_files=5),
        ]
        conns = _find_monitoring_patterns(projects)
        gaps = [c for c in conns if c.type == "monitoring_gap"]
        assert len(gaps) == 0

    # --- Edge cases ---

    def test_empty_projects(self):
        conns = _find_monitoring_patterns([])
        assert conns == []

    def test_no_tools_no_connections(self):
        projects = [
            _proj("a", monitoring_tools=[]),
            _proj("b", monitoring_tools=[]),
        ]
        conns = _find_monitoring_patterns(projects)
        assert len(conns) == 0

    def test_limit_10(self):
        tools = [f"Tool{i}" for i in range(20)]
        projects = [_proj("a", monitoring_tools=tools), _proj("b", monitoring_tools=tools)]
        conns = _find_monitoring_patterns(projects)
        assert len(conns) <= 10

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", monitoring_tools=["Sentry", "Datadog"]),
            _proj("b", monitoring_tools=["Sentry", "New Relic"]),
        ]
        conns = find_connections(projects)
        mon_types = {c.type for c in conns if "monitoring" in c.type}
        assert "shared_monitoring" in mon_types
        assert "monitoring_divergence" in mon_types


# ---------------------------------------------------------------------------
# _find_auth_patterns
# ---------------------------------------------------------------------------
class TestFindAuthPatterns:
    # --- Shared auth tools ---

    def test_shared_auth_tool(self):
        projects = [
            _proj("a", auth_tools=["Clerk", "PyJWT"]),
            _proj("b", auth_tools=["Clerk"]),
        ]
        conns = _find_auth_patterns(projects)
        shared = [c for c in conns if c.type == "shared_auth"]
        assert len(shared) == 1
        assert "Clerk" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_multiple_tools(self):
        projects = [
            _proj("a", auth_tools=["Clerk", "PyJWT"]),
            _proj("b", auth_tools=["Clerk", "PyJWT"]),
        ]
        conns = _find_auth_patterns(projects)
        shared = [c for c in conns if c.type == "shared_auth"]
        assert len(shared) == 2

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", auth_tools=["Clerk"]),
            _proj("b", auth_tools=["Auth0"]),
        ]
        conns = _find_auth_patterns(projects)
        shared = [c for c in conns if c.type == "shared_auth"]
        assert len(shared) == 0

    def test_shared_needs_two_projects(self):
        projects = [_proj("a", auth_tools=["Clerk"])]
        conns = _find_auth_patterns(projects)
        shared = [c for c in conns if c.type == "shared_auth"]
        assert len(shared) == 0

    # --- Auth provider divergence ---

    def test_auth_provider_divergence(self):
        projects = [
            _proj("a", auth_tools=["Clerk"]),
            _proj("b", auth_tools=["Auth0"]),
        ]
        conns = _find_auth_patterns(projects)
        div = [c for c in conns if c.type == "auth_divergence"
               and "provider" in c.detail.lower()]
        assert len(div) == 1
        assert "Clerk" in div[0].detail
        assert "Auth0" in div[0].detail
        assert div[0].severity == "warning"

    def test_no_provider_divergence_same_provider(self):
        projects = [
            _proj("a", auth_tools=["Auth0"]),
            _proj("b", auth_tools=["Auth0"]),
        ]
        conns = _find_auth_patterns(projects)
        div = [c for c in conns if c.type == "auth_divergence"
               and "provider" in c.detail.lower()]
        assert len(div) == 0

    def test_no_provider_divergence_non_providers(self):
        projects = [
            _proj("a", auth_tools=["PyJWT"]),
            _proj("b", auth_tools=["jsonwebtoken"]),
        ]
        conns = _find_auth_patterns(projects)
        div = [c for c in conns if c.type == "auth_divergence"
               and "provider" in c.detail.lower()]
        assert len(div) == 0

    # --- Auth strategy divergence ---

    def test_auth_strategy_divergence(self):
        projects = [
            _proj("a", auth_tools=["Passport.js"]),
            _proj("b", auth_tools=["PyJWT"]),
        ]
        conns = _find_auth_patterns(projects)
        div = [c for c in conns if c.type == "auth_divergence"
               and "session-based" in c.detail.lower()]
        assert len(div) == 1
        assert div[0].severity == "info"

    def test_no_strategy_divergence_same_category(self):
        projects = [
            _proj("a", auth_tools=["PyJWT"]),
            _proj("b", auth_tools=["jsonwebtoken"]),
        ]
        conns = _find_auth_patterns(projects)
        div = [c for c in conns if c.type == "auth_divergence"
               and "session-based" in c.detail.lower()]
        assert len(div) == 0

    # --- Auth gap ---

    def test_auth_gap(self):
        projects = [
            _proj("a", auth_tools=["Clerk"], frameworks=["Next.js"]),
            _proj("b", auth_tools=[], frameworks=["FastAPI"], source_files=15),
        ]
        conns = _find_auth_patterns(projects)
        gaps = [c for c in conns if c.type == "auth_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_when_all_have_auth(self):
        projects = [
            _proj("a", auth_tools=["Clerk"], frameworks=["Next.js"]),
            _proj("b", auth_tools=["PyJWT"], frameworks=["FastAPI"]),
        ]
        conns = _find_auth_patterns(projects)
        gaps = [c for c in conns if c.type == "auth_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_no_web_frameworks(self):
        projects = [
            _proj("a", auth_tools=["Clerk"]),
            _proj("b", auth_tools=[], frameworks=[], source_files=15),
        ]
        conns = _find_auth_patterns(projects)
        gaps = [c for c in conns if c.type == "auth_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", auth_tools=["Clerk"], frameworks=["Next.js"]),
            _proj("b", auth_tools=[], frameworks=["Flask"], source_files=3),
        ]
        conns = _find_auth_patterns(projects)
        gaps = [c for c in conns if c.type == "auth_gap"]
        assert len(gaps) == 0

    # --- Edge cases ---

    def test_empty_projects(self):
        conns = _find_auth_patterns([])
        assert conns == []

    def test_no_tools_no_connections(self):
        projects = [
            _proj("a", auth_tools=[]),
            _proj("b", auth_tools=[]),
        ]
        conns = _find_auth_patterns(projects)
        assert len(conns) == 0

    def test_limit_10(self):
        tools = [f"AuthTool{i}" for i in range(20)]
        projects = [_proj("a", auth_tools=tools), _proj("b", auth_tools=tools)]
        conns = _find_auth_patterns(projects)
        assert len(conns) <= 10

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", auth_tools=["Clerk", "PyJWT"]),
            _proj("b", auth_tools=["Clerk", "Auth0"]),
        ]
        conns = find_connections(projects)
        auth_types = {c.type for c in conns if "auth" in c.type}
        assert "shared_auth" in auth_types
        assert "auth_divergence" in auth_types


# ---------------------------------------------------------------------------
# _find_messaging_patterns
# ---------------------------------------------------------------------------
class TestFindMessagingPatterns:
    # --- Shared messaging tools ---

    def test_shared_messaging_tool(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid", "Twilio"]),
            _proj("b", messaging_tools=["SendGrid"]),
        ]
        conns = _find_messaging_patterns(projects)
        shared = [c for c in conns if c.type == "shared_messaging"]
        assert len(shared) == 1
        assert "SendGrid" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_multiple_tools(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid", "Slack"]),
            _proj("b", messaging_tools=["SendGrid", "Slack"]),
        ]
        conns = _find_messaging_patterns(projects)
        shared = [c for c in conns if c.type == "shared_messaging"]
        assert len(shared) == 2

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid"]),
            _proj("b", messaging_tools=["Twilio"]),
        ]
        conns = _find_messaging_patterns(projects)
        shared = [c for c in conns if c.type == "shared_messaging"]
        assert len(shared) == 0

    def test_shared_needs_two_projects(self):
        projects = [_proj("a", messaging_tools=["SendGrid"])]
        conns = _find_messaging_patterns(projects)
        shared = [c for c in conns if c.type == "shared_messaging"]
        assert len(shared) == 0

    # --- Email provider divergence ---

    def test_email_provider_divergence(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid"]),
            _proj("b", messaging_tools=["Resend"]),
        ]
        conns = _find_messaging_patterns(projects)
        div = [c for c in conns if c.type == "messaging_divergence"
               and "email" in c.detail.lower()]
        assert len(div) == 1
        assert "SendGrid" in div[0].detail
        assert "Resend" in div[0].detail
        assert div[0].severity == "warning"

    def test_no_email_divergence_same_provider(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid"]),
            _proj("b", messaging_tools=["SendGrid"]),
        ]
        conns = _find_messaging_patterns(projects)
        div = [c for c in conns if c.type == "messaging_divergence"
               and "email" in c.detail.lower()]
        assert len(div) == 0

    # --- Real-time divergence ---

    def test_realtime_divergence(self):
        projects = [
            _proj("a", messaging_tools=["Socket.IO"]),
            _proj("b", messaging_tools=["Pusher"]),
        ]
        conns = _find_messaging_patterns(projects)
        div = [c for c in conns if c.type == "messaging_divergence"
               and "real-time" in c.detail.lower()]
        assert len(div) == 1
        assert div[0].severity == "info"

    def test_no_realtime_divergence_same_tool(self):
        projects = [
            _proj("a", messaging_tools=["Socket.IO"]),
            _proj("b", messaging_tools=["Socket.IO"]),
        ]
        conns = _find_messaging_patterns(projects)
        div = [c for c in conns if c.type == "messaging_divergence"
               and "real-time" in c.detail.lower()]
        assert len(div) == 0

    # --- Messaging gap ---

    def test_messaging_gap(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid"], frameworks=["FastAPI"]),
            _proj("b", messaging_tools=[], frameworks=["Django"], source_files=15),
        ]
        conns = _find_messaging_patterns(projects)
        gaps = [c for c in conns if c.type == "messaging_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_when_all_have_messaging(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid"], frameworks=["FastAPI"]),
            _proj("b", messaging_tools=["Twilio"], frameworks=["Django"]),
        ]
        conns = _find_messaging_patterns(projects)
        gaps = [c for c in conns if c.type == "messaging_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_no_web_frameworks(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid"]),
            _proj("b", messaging_tools=[], frameworks=[], source_files=15),
        ]
        conns = _find_messaging_patterns(projects)
        gaps = [c for c in conns if c.type == "messaging_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid"], frameworks=["FastAPI"]),
            _proj("b", messaging_tools=[], frameworks=["Flask"], source_files=5),
        ]
        conns = _find_messaging_patterns(projects)
        gaps = [c for c in conns if c.type == "messaging_gap"]
        assert len(gaps) == 0

    # --- Edge cases ---

    def test_empty_projects(self):
        conns = _find_messaging_patterns([])
        assert conns == []

    def test_no_tools_no_connections(self):
        projects = [
            _proj("a", messaging_tools=[]),
            _proj("b", messaging_tools=[]),
        ]
        conns = _find_messaging_patterns(projects)
        assert len(conns) == 0

    def test_limit_10(self):
        tools = [f"MsgTool{i}" for i in range(20)]
        projects = [_proj("a", messaging_tools=tools), _proj("b", messaging_tools=tools)]
        conns = _find_messaging_patterns(projects)
        assert len(conns) <= 10

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", messaging_tools=["SendGrid", "Socket.IO"]),
            _proj("b", messaging_tools=["SendGrid", "Pusher"]),
        ]
        conns = find_connections(projects)
        msg_types = {c.type for c in conns if "messaging" in c.type}
        assert "shared_messaging" in msg_types
        assert "messaging_divergence" in msg_types


# ---------------------------------------------------------------------------
# N-65: Deployment Target Intelligence
# ---------------------------------------------------------------------------
class TestFindDeployTargetPatterns:
    def test_shared_deploy_target(self):
        projects = [
            _proj("a", deploy_targets=["Vercel"]),
            _proj("b", deploy_targets=["Vercel"]),
        ]
        conns = _find_deploy_target_patterns(projects)
        shared = [c for c in conns if c.type == "shared_deploy"]
        assert len(shared) == 1
        assert "Vercel" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_deploy_multiple(self):
        projects = [
            _proj("a", deploy_targets=["Vercel", "Netlify"]),
            _proj("b", deploy_targets=["Vercel", "Netlify"]),
            _proj("c", deploy_targets=["Vercel"]),
        ]
        conns = _find_deploy_target_patterns(projects)
        shared = [c for c in conns if c.type == "shared_deploy"]
        assert len(shared) == 2

    def test_no_shared_with_different_targets(self):
        projects = [
            _proj("a", deploy_targets=["Vercel"]),
            _proj("b", deploy_targets=["Netlify"]),
        ]
        conns = _find_deploy_target_patterns(projects)
        shared = [c for c in conns if c.type == "shared_deploy"]
        assert len(shared) == 0

    def test_platform_divergence_serverless_vs_container(self):
        projects = [
            _proj("a", deploy_targets=["Vercel"]),
            _proj("b", deploy_targets=["Fly.io"]),
        ]
        conns = _find_deploy_target_patterns(projects)
        div = [c for c in conns if c.type == "deploy_divergence"]
        assert len(div) == 1
        assert "serverless/edge" in div[0].detail
        assert "container PaaS" in div[0].detail
        assert div[0].severity == "warning"

    def test_no_divergence_same_category(self):
        projects = [
            _proj("a", deploy_targets=["Vercel"]),
            _proj("b", deploy_targets=["Netlify"]),
        ]
        conns = _find_deploy_target_patterns(projects)
        div = [c for c in conns if c.type == "deploy_divergence"]
        assert len(div) == 0

    def test_deploy_gap(self):
        projects = [
            _proj("a", frameworks=["FastAPI"], deploy_targets=["Fly.io"], source_files=20),
            _proj("b", frameworks=["FastAPI"], deploy_targets=[], source_files=20),
        ]
        conns = _find_deploy_target_patterns(projects)
        gaps = [c for c in conns if c.type == "deploy_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_without_framework(self):
        projects = [
            _proj("a", deploy_targets=["Vercel"]),
            _proj("b", frameworks=[], deploy_targets=[], source_files=20),
        ]
        conns = _find_deploy_target_patterns(projects)
        gaps = [c for c in conns if c.type == "deploy_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", deploy_targets=["Vercel"]),
            _proj("b", frameworks=["FastAPI"], deploy_targets=[], source_files=3),
        ]
        conns = _find_deploy_target_patterns(projects)
        gaps = [c for c in conns if c.type == "deploy_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_none_have_deploy(self):
        projects = [
            _proj("a", frameworks=["FastAPI"], deploy_targets=[], source_files=20),
            _proj("b", frameworks=["Django"], deploy_targets=[], source_files=20),
        ]
        conns = _find_deploy_target_patterns(projects)
        gaps = [c for c in conns if c.type == "deploy_gap"]
        assert len(gaps) == 0

    def test_empty_projects(self):
        conns = _find_deploy_target_patterns([])
        assert conns == []

    def test_no_deploy_targets(self):
        projects = [
            _proj("a", deploy_targets=[]),
            _proj("b", deploy_targets=[]),
        ]
        conns = _find_deploy_target_patterns(projects)
        assert len(conns) == 0

    def test_shared_sorted_by_count(self):
        projects = [
            _proj("a", deploy_targets=["Vercel", "Heroku"]),
            _proj("b", deploy_targets=["Vercel", "Heroku"]),
            _proj("c", deploy_targets=["Vercel"]),
        ]
        conns = _find_deploy_target_patterns(projects)
        shared = [c for c in conns if c.type == "shared_deploy"]
        assert len(shared) == 2
        assert "3 projects" in shared[0].detail  # Vercel first (3 > 2)

    def test_divergence_container_vs_iaas(self):
        projects = [
            _proj("a", deploy_targets=["Heroku"]),
            _proj("b", deploy_targets=["Serverless Framework"]),
        ]
        conns = _find_deploy_target_patterns(projects)
        div = [c for c in conns if c.type == "deploy_divergence"]
        assert len(div) == 1

    def test_projects_sorted_in_shared(self):
        projects = [
            _proj("z-proj", deploy_targets=["Vercel"]),
            _proj("a-proj", deploy_targets=["Vercel"]),
        ]
        conns = _find_deploy_target_patterns(projects)
        shared = [c for c in conns if c.type == "shared_deploy"]
        assert shared[0].projects == ["a-proj", "z-proj"]

    def test_limit_10(self):
        targets = [f"Target{i}" for i in range(20)]
        projects = [_proj("a", deploy_targets=targets), _proj("b", deploy_targets=targets)]
        conns = _find_deploy_target_patterns(projects)
        assert len(conns) <= 10

    def test_gap_multiple_web_projects(self):
        projects = [
            _proj("a", frameworks=["FastAPI"], deploy_targets=["Fly.io"], source_files=20),
            _proj("b", frameworks=["Django"], deploy_targets=[], source_files=20),
            _proj("c", frameworks=["Express"], deploy_targets=[], source_files=20),
        ]
        conns = _find_deploy_target_patterns(projects)
        gaps = [c for c in conns if c.type == "deploy_gap"]
        assert len(gaps) == 1
        assert "2 web project(s)" in gaps[0].detail
        assert sorted(gaps[0].projects) == ["b", "c"]

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", deploy_targets=["Vercel"]),
            _proj("b", deploy_targets=["Vercel", "Fly.io"]),
        ]
        conns = find_connections(projects)
        deploy_types = {c.type for c in conns if "deploy" in c.type}
        assert "shared_deploy" in deploy_types


# ---------------------------------------------------------------------------
# _find_state_management_patterns
# ---------------------------------------------------------------------------
class TestFindStateManagementPatterns:
    def test_shared_state_management(self):
        projects = [
            _proj("a", state_management=["Redux"]),
            _proj("b", state_management=["Redux"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_state_mgmt"]
        assert len(shared) == 1
        assert "Redux" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_multiple_libs(self):
        projects = [
            _proj("a", state_management=["Redux", "Zustand"]),
            _proj("b", state_management=["Redux", "Zustand"]),
            _proj("c", state_management=["Redux"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_state_mgmt"]
        assert len(shared) == 2

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", state_management=["Redux"]),
            _proj("b", state_management=["Zustand"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_state_mgmt"]
        assert len(shared) == 0

    def test_no_shared_single_project(self):
        projects = [_proj("a", state_management=["Redux"])]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_state_mgmt"]
        assert len(shared) == 0

    def test_divergence_flux_vs_proxy(self):
        projects = [
            _proj("a", state_management=["Redux"]),
            _proj("b", state_management=["MobX"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "state_mgmt_divergence"]
        assert len(div) == 1
        assert "flux/store" in div[0].detail
        assert "proxy-based" in div[0].detail
        assert div[0].severity == "warning"

    def test_divergence_flux_vs_atomic(self):
        projects = [
            _proj("a", state_management=["Zustand"]),
            _proj("b", state_management=["Jotai"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "state_mgmt_divergence"]
        assert len(div) == 1
        assert "flux/store" in div[0].detail
        assert "atomic" in div[0].detail

    def test_divergence_vue_vs_angular(self):
        projects = [
            _proj("a", state_management=["Pinia"]),
            _proj("b", state_management=["NgRx"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "state_mgmt_divergence"]
        assert len(div) == 1
        assert "Vue" in div[0].detail
        assert "Angular" in div[0].detail

    def test_divergence_state_machine_vs_flux(self):
        projects = [
            _proj("a", state_management=["XState"]),
            _proj("b", state_management=["Redux"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "state_mgmt_divergence"]
        assert len(div) == 1
        assert "state machines" in div[0].detail

    def test_no_divergence_same_paradigm(self):
        projects = [
            _proj("a", state_management=["Redux"]),
            _proj("b", state_management=["Zustand"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "state_mgmt_divergence"]
        # Both are flux/store — no divergence (single category)
        assert len(div) == 0

    def test_no_divergence_empty(self):
        projects = [_proj("a"), _proj("b")]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "state_mgmt_divergence"]
        assert len(div) == 0

    def test_gap_frontend_no_state(self):
        projects = [
            _proj("a", frameworks=["React"], state_management=["Redux"], source_files=15),
            _proj("b", frameworks=["React"], source_files=15),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "state_mgmt_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_gap_multiple_frameworks(self):
        projects = [
            _proj("a", frameworks=["Next.js"], state_management=["Zustand"], source_files=20),
            _proj("b", frameworks=["Vue"], source_files=20),
            _proj("c", frameworks=["Angular"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "state_mgmt_gap"]
        assert len(gaps) == 1
        assert "2 frontend project(s)" in gaps[0].detail
        assert sorted(gaps[0].projects) == ["b", "c"]

    def test_no_gap_when_no_frontend(self):
        projects = [
            _proj("a", frameworks=["FastAPI"], state_management=["Redux"], source_files=20),
            _proj("b", frameworks=["Django"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "state_mgmt_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_no_state_portfolio(self):
        projects = [
            _proj("a", frameworks=["React"], source_files=20),
            _proj("b", frameworks=["Vue"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "state_mgmt_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", frameworks=["React"], state_management=["Redux"], source_files=20),
            _proj("b", frameworks=["React"], source_files=5),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "state_mgmt_gap"]
        assert len(gaps) == 0

    def test_integration_with_find_connections_state(self):
        projects = [
            _proj("a", state_management=["Redux"]),
            _proj("b", state_management=["Redux", "MobX"]),
        ]
        conns = find_connections(projects)
        state_types = {c.type for c in conns if "state_mgmt" in c.type}
        assert "shared_state_mgmt" in state_types


# ---------------------------------------------------------------------------
# _find_css_framework_patterns
# ---------------------------------------------------------------------------
class TestFindCssFrameworkPatterns:
    def test_shared_css_framework(self):
        projects = [
            _proj("a", css_frameworks=["Tailwind CSS"]),
            _proj("b", css_frameworks=["Tailwind CSS"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_css"]
        assert len(shared) == 1
        assert "Tailwind CSS" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_multiple(self):
        projects = [
            _proj("a", css_frameworks=["Tailwind CSS", "PostCSS"]),
            _proj("b", css_frameworks=["Tailwind CSS", "PostCSS"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_css"]
        assert len(shared) == 2

    def test_no_shared_unique(self):
        projects = [
            _proj("a", css_frameworks=["Tailwind CSS"]),
            _proj("b", css_frameworks=["Bootstrap"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_css"]
        assert len(shared) == 0

    def test_divergence_utility_vs_css_in_js(self):
        projects = [
            _proj("a", css_frameworks=["Tailwind CSS"]),
            _proj("b", css_frameworks=["Styled Components"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "css_divergence"]
        assert len(div) == 1
        assert "utility-first" in div[0].detail
        assert "CSS-in-JS" in div[0].detail
        assert div[0].severity == "warning"

    def test_divergence_utility_vs_component_lib(self):
        projects = [
            _proj("a", css_frameworks=["Tailwind CSS"]),
            _proj("b", css_frameworks=["Material UI"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "css_divergence"]
        assert len(div) == 1
        assert "utility-first" in div[0].detail
        assert "component library" in div[0].detail

    def test_divergence_css_in_js_vs_component_lib(self):
        projects = [
            _proj("a", css_frameworks=["Emotion"]),
            _proj("b", css_frameworks=["Chakra UI"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "css_divergence"]
        assert len(div) == 1

    def test_no_divergence_same_paradigm(self):
        projects = [
            _proj("a", css_frameworks=["Tailwind CSS"]),
            _proj("b", css_frameworks=["UnoCSS"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "css_divergence"]
        assert len(div) == 0

    def test_no_divergence_empty(self):
        projects = [_proj("a"), _proj("b")]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "css_divergence"]
        assert len(div) == 0

    def test_gap_frontend_no_css(self):
        projects = [
            _proj("a", frameworks=["React"], css_frameworks=["Tailwind CSS"], source_files=15),
            _proj("b", frameworks=["React"], source_files=15),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "css_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_gap_multiple(self):
        projects = [
            _proj("a", frameworks=["Next.js"], css_frameworks=["Tailwind CSS"], source_files=20),
            _proj("b", frameworks=["Vue"], source_files=20),
            _proj("c", frameworks=["Angular"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "css_gap"]
        assert len(gaps) == 1
        assert "2 frontend" in gaps[0].detail

    def test_no_gap_no_frontend(self):
        projects = [
            _proj("a", frameworks=["FastAPI"], css_frameworks=["Tailwind CSS"], source_files=20),
            _proj("b", frameworks=["Django"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "css_gap"]
        assert len(gaps) == 0

    def test_no_gap_no_css_portfolio(self):
        projects = [
            _proj("a", frameworks=["React"], source_files=20),
            _proj("b", frameworks=["Vue"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "css_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", frameworks=["React"], css_frameworks=["Tailwind CSS"], source_files=20),
            _proj("b", frameworks=["React"], source_files=5),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "css_gap"]
        assert len(gaps) == 0

    def test_integration_with_find_connections_css(self):
        projects = [
            _proj("a", css_frameworks=["Tailwind CSS"]),
            _proj("b", css_frameworks=["Tailwind CSS", "Emotion"]),
        ]
        conns = find_connections(projects)
        css_types = {c.type for c in conns if "css" in c.type}
        assert "shared_css" in css_types


# ---------------------------------------------------------------------------
# _find_bundler_patterns
# ---------------------------------------------------------------------------
class TestFindBundlerPatterns:
    def test_shared_bundler(self):
        projects = [
            _proj("a", bundlers=["Vite"]),
            _proj("b", bundlers=["Vite"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_bundler"]
        assert len(shared) == 1
        assert "Vite" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_multiple(self):
        projects = [
            _proj("a", bundlers=["Vite", "esbuild"]),
            _proj("b", bundlers=["Vite", "esbuild"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_bundler"]
        assert len(shared) == 2

    def test_no_shared_unique(self):
        projects = [
            _proj("a", bundlers=["Vite"]),
            _proj("b", bundlers=["Webpack"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_bundler"]
        assert len(shared) == 0

    def test_divergence_modern_vs_traditional(self):
        projects = [
            _proj("a", bundlers=["Vite"]),
            _proj("b", bundlers=["Webpack"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "bundler_divergence"]
        assert len(div) == 1
        assert "modern/fast" in div[0].detail
        assert "traditional" in div[0].detail
        assert div[0].severity == "warning"

    def test_divergence_modern_vs_library(self):
        projects = [
            _proj("a", bundlers=["esbuild"]),
            _proj("b", bundlers=["tsup"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "bundler_divergence"]
        assert len(div) == 1

    def test_no_divergence_same_generation(self):
        projects = [
            _proj("a", bundlers=["Vite"]),
            _proj("b", bundlers=["esbuild"]),
        ]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "bundler_divergence"]
        assert len(div) == 0

    def test_no_divergence_empty(self):
        projects = [_proj("a"), _proj("b")]
        conns = find_connections(projects)
        div = [c for c in conns if c.type == "bundler_divergence"]
        assert len(div) == 0

    def test_gap_js_no_bundler(self):
        projects = [
            _proj("a", bundlers=["Vite"], source_files=15),
            _proj("b", source_files=15),
        ]
        # b needs JS/TS languages for gap
        projects[1].tech_stack.languages = {"TypeScript": 100}
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "bundler_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects

    def test_no_gap_no_js(self):
        projects = [
            _proj("a", bundlers=["Vite"], source_files=15),
            _proj("b", source_files=15),
        ]
        projects[1].tech_stack.languages = {"Python": 100}
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "bundler_gap"]
        assert len(gaps) == 0

    def test_no_gap_no_bundler_portfolio(self):
        projects = [
            _proj("a", source_files=15),
            _proj("b", source_files=15),
        ]
        projects[0].tech_stack.languages = {"TypeScript": 100}
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "bundler_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", bundlers=["Vite"], source_files=15),
            _proj("b", source_files=5),
        ]
        projects[1].tech_stack.languages = {"TypeScript": 50}
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "bundler_gap"]
        assert len(gaps) == 0

    def test_integration_with_find_connections_bundler(self):
        projects = [
            _proj("a", bundlers=["Vite"]),
            _proj("b", bundlers=["Vite", "Webpack"]),
        ]
        conns = find_connections(projects)
        bnd_types = {c.type for c in conns if "bundler" in c.type}
        assert "shared_bundler" in bnd_types


class TestFindOrmPatterns:
    def test_no_orm_tools(self):
        projects = [_proj("a"), _proj("b")]
        conns = find_connections(projects)
        orm_types = {c.type for c in conns if "orm" in c.type}
        assert len(orm_types) == 0

    def test_shared_orm_detected(self):
        projects = [
            _proj("a", orm_tools=["SQLAlchemy"]),
            _proj("b", orm_tools=["SQLAlchemy"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_orm"]
        assert len(shared) == 1
        assert "SQLAlchemy" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_orm_needs_two_projects(self):
        projects = [
            _proj("a", orm_tools=["SQLAlchemy"]),
            _proj("b", orm_tools=["Prisma"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_orm"]
        assert len(shared) == 0

    def test_orm_divergence_orm_vs_raw(self):
        projects = [
            _proj("a", orm_tools=["SQLAlchemy"]),
            _proj("b", orm_tools=["asyncpg"]),
        ]
        conns = find_connections(projects)
        divs = [c for c in conns if c.type == "orm_divergence"]
        assert len(divs) == 1
        assert "ORM" in divs[0].detail
        assert "raw client" in divs[0].detail
        assert divs[0].severity == "warning"

    def test_no_divergence_same_paradigm(self):
        projects = [
            _proj("a", orm_tools=["SQLAlchemy"]),
            _proj("b", orm_tools=["Prisma"]),
        ]
        conns = find_connections(projects)
        divs = [c for c in conns if c.type == "orm_divergence"]
        assert len(divs) == 0

    def test_no_divergence_raw_only(self):
        projects = [
            _proj("a", orm_tools=["asyncpg"]),
            _proj("b", orm_tools=["node-postgres"]),
        ]
        conns = find_connections(projects)
        divs = [c for c in conns if c.type == "orm_divergence"]
        assert len(divs) == 0

    def test_orm_gap_with_databases(self):
        projects = [
            _proj("a", orm_tools=["SQLAlchemy"], databases=["PostgreSQL"]),
            _proj("b", databases=["PostgreSQL"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "orm_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects

    def test_no_orm_gap_without_databases(self):
        projects = [
            _proj("a", orm_tools=["SQLAlchemy"], databases=["PostgreSQL"]),
            _proj("b", source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "orm_gap"]
        assert len(gaps) == 0

    def test_no_orm_gap_small_project(self):
        projects = [
            _proj("a", orm_tools=["SQLAlchemy"], databases=["PostgreSQL"]),
            _proj("b", databases=["Redis"], source_files=5),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "orm_gap"]
        assert len(gaps) == 0

    def test_multiple_shared_orms(self):
        projects = [
            _proj("a", orm_tools=["SQLAlchemy", "Alembic"]),
            _proj("b", orm_tools=["SQLAlchemy", "Alembic"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_orm"]
        assert len(shared) == 2

    def test_integration_with_find_connections_orm(self):
        projects = [
            _proj("a", orm_tools=["Prisma"]),
            _proj("b", orm_tools=["Prisma", "Mongoose"]),
        ]
        conns = find_connections(projects)
        orm_types = {c.type for c in conns if "orm" in c.type}
        assert "shared_orm" in orm_types


class TestFindI18nPatterns:
    def test_no_i18n_tools(self):
        projects = [_proj("a"), _proj("b")]
        conns = find_connections(projects)
        i18n_types = {c.type for c in conns if "i18n" in c.type}
        assert len(i18n_types) == 0

    def test_shared_i18n_detected(self):
        projects = [
            _proj("a", i18n_tools=["i18next"]),
            _proj("b", i18n_tools=["i18next"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_i18n"]
        assert len(shared) == 1
        assert "i18next" in shared[0].detail
        assert shared[0].severity == "info"

    def test_shared_i18n_needs_two_projects(self):
        projects = [
            _proj("a", i18n_tools=["i18next"]),
            _proj("b", i18n_tools=["vue-i18n"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_i18n"]
        assert len(shared) == 0

    def test_i18n_divergence_icu_vs_key_based(self):
        projects = [
            _proj("a", i18n_tools=["react-intl"]),
            _proj("b", i18n_tools=["i18next"]),
        ]
        conns = find_connections(projects)
        divs = [c for c in conns if c.type == "i18n_divergence"]
        assert len(divs) == 1
        assert "ICU" in divs[0].detail
        assert "key-based" in divs[0].detail
        assert divs[0].severity == "warning"

    def test_no_divergence_same_paradigm(self):
        projects = [
            _proj("a", i18n_tools=["i18next"]),
            _proj("b", i18n_tools=["vue-i18n"]),
        ]
        conns = find_connections(projects)
        divs = [c for c in conns if c.type == "i18n_divergence"]
        assert len(divs) == 0

    def test_i18n_gap_web_projects(self):
        projects = [
            _proj("a", i18n_tools=["i18next"], frameworks=["React"]),
            _proj("b", frameworks=["React"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "i18n_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects

    def test_no_gap_non_web_project(self):
        projects = [
            _proj("a", i18n_tools=["i18next"], frameworks=["React"]),
            _proj("b", frameworks=["FastAPI"], source_files=5),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "i18n_gap"]
        assert len(gaps) == 0

    def test_no_gap_without_i18n_projects(self):
        projects = [
            _proj("a", frameworks=["React"], source_files=20),
            _proj("b", frameworks=["React"], source_files=20),
        ]
        conns = find_connections(projects)
        gaps = [c for c in conns if c.type == "i18n_gap"]
        assert len(gaps) == 0

    def test_multiple_shared_i18n(self):
        projects = [
            _proj("a", i18n_tools=["i18next", "react-i18next"]),
            _proj("b", i18n_tools=["i18next", "react-i18next"]),
        ]
        conns = find_connections(projects)
        shared = [c for c in conns if c.type == "shared_i18n"]
        assert len(shared) == 2

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", i18n_tools=["react-intl"]),
            _proj("b", i18n_tools=["react-intl", "i18next"]),
        ]
        conns = find_connections(projects)
        i18n_types = {c.type for c in conns if "i18n" in c.type}
        assert "shared_i18n" in i18n_types


# ---------------------------------------------------------------------------
# _find_validation_patterns
# ---------------------------------------------------------------------------
class TestFindValidationPatterns:
    def test_no_validation_no_connections(self):
        projects = [_proj("a"), _proj("b")]
        conns = _find_validation_patterns(projects)
        assert conns == []

    def test_shared_validation(self):
        projects = [
            _proj("a", validation_tools=["Pydantic"]),
            _proj("b", validation_tools=["Pydantic"]),
        ]
        conns = _find_validation_patterns(projects)
        shared = [c for c in conns if c.type == "shared_validation"]
        assert len(shared) == 1
        assert "Pydantic" in shared[0].detail
        assert shared[0].severity == "info"

    def test_no_shared_when_different(self):
        projects = [
            _proj("a", validation_tools=["Zod"]),
            _proj("b", validation_tools=["Yup"]),
        ]
        conns = _find_validation_patterns(projects)
        shared = [c for c in conns if c.type == "shared_validation"]
        assert len(shared) == 0

    def test_validation_divergence_schema_vs_model(self):
        projects = [
            _proj("a", validation_tools=["Zod"]),
            _proj("b", validation_tools=["Pydantic"]),
        ]
        conns = _find_validation_patterns(projects)
        div = [c for c in conns if c.type == "validation_divergence"]
        assert len(div) == 1
        assert div[0].severity == "warning"
        assert "schema-first" in div[0].detail
        assert "model/decorator-based" in div[0].detail

    def test_no_divergence_same_category(self):
        projects = [
            _proj("a", validation_tools=["Zod"]),
            _proj("b", validation_tools=["Yup"]),
        ]
        conns = _find_validation_patterns(projects)
        div = [c for c in conns if c.type == "validation_divergence"]
        assert len(div) == 0

    def test_validation_gap_api_project_no_validation(self):
        projects = [
            _proj("a", validation_tools=["Pydantic"], frameworks=["FastAPI"], source_files=20),
            _proj("b", validation_tools=[], frameworks=["Flask"], source_files=20),
        ]
        conns = _find_validation_patterns(projects)
        gaps = [c for c in conns if c.type == "validation_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "critical"

    def test_no_gap_when_no_api_framework(self):
        projects = [
            _proj("a", validation_tools=["Zod"]),
            _proj("b", validation_tools=[], frameworks=[], source_files=20),
        ]
        conns = _find_validation_patterns(projects)
        gaps = [c for c in conns if c.type == "validation_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_small_project(self):
        projects = [
            _proj("a", validation_tools=["Pydantic"], frameworks=["FastAPI"], source_files=20),
            _proj("b", validation_tools=[], frameworks=["FastAPI"], source_files=5),
        ]
        conns = _find_validation_patterns(projects)
        gaps = [c for c in conns if c.type == "validation_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_no_projects_have_validation(self):
        projects = [
            _proj("a", validation_tools=[], frameworks=["FastAPI"], source_files=20),
            _proj("b", validation_tools=[], frameworks=["Flask"], source_files=20),
        ]
        conns = _find_validation_patterns(projects)
        gaps = [c for c in conns if c.type == "validation_gap"]
        assert len(gaps) == 0

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", validation_tools=["Pydantic"]),
            _proj("b", validation_tools=["Pydantic", "Zod"]),
        ]
        conns = find_connections(projects)
        val_types = {c.type for c in conns if "validation" in c.type}
        assert "shared_validation" in val_types


# ---------------------------------------------------------------------------
# _find_logging_patterns
# ---------------------------------------------------------------------------
class TestFindLoggingPatterns:
    def test_no_logging_no_connections(self):
        projects = [_proj("a"), _proj("b")]
        conns = _find_logging_patterns(projects)
        assert conns == []

    def test_shared_logging(self):
        projects = [
            _proj("a", logging_tools=["Loguru"]),
            _proj("b", logging_tools=["Loguru"]),
        ]
        conns = _find_logging_patterns(projects)
        shared = [c for c in conns if c.type == "shared_logging"]
        assert len(shared) == 1
        assert "Loguru" in shared[0].detail
        assert shared[0].severity == "info"

    def test_no_shared_when_different(self):
        projects = [
            _proj("a", logging_tools=["Winston"]),
            _proj("b", logging_tools=["Pino"]),
        ]
        conns = _find_logging_patterns(projects)
        shared = [c for c in conns if c.type == "shared_logging"]
        assert len(shared) == 0

    def test_logging_divergence_structured_vs_traditional(self):
        projects = [
            _proj("a", logging_tools=["structlog"]),
            _proj("b", logging_tools=["Winston"]),
        ]
        conns = _find_logging_patterns(projects)
        div = [c for c in conns if c.type == "logging_divergence"]
        assert len(div) == 1
        assert div[0].severity == "warning"
        assert "structured" in div[0].detail
        assert "traditional" in div[0].detail

    def test_no_divergence_same_category(self):
        projects = [
            _proj("a", logging_tools=["structlog"]),
            _proj("b", logging_tools=["Pino"]),
        ]
        conns = _find_logging_patterns(projects)
        div = [c for c in conns if c.type == "logging_divergence"]
        assert len(div) == 0

    def test_logging_gap_backend_no_logging(self):
        projects = [
            _proj("a", logging_tools=["Loguru"], frameworks=["FastAPI"], source_files=20),
            _proj("b", logging_tools=[], frameworks=["Flask"], source_files=20),
        ]
        conns = _find_logging_patterns(projects)
        gaps = [c for c in conns if c.type == "logging_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_when_no_backend_framework(self):
        projects = [
            _proj("a", logging_tools=["Pino"]),
            _proj("b", logging_tools=[], frameworks=[], source_files=20),
        ]
        conns = _find_logging_patterns(projects)
        gaps = [c for c in conns if c.type == "logging_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_small_project(self):
        projects = [
            _proj("a", logging_tools=["Winston"], frameworks=["Express"], source_files=20),
            _proj("b", logging_tools=[], frameworks=["Express"], source_files=5),
        ]
        conns = _find_logging_patterns(projects)
        gaps = [c for c in conns if c.type == "logging_gap"]
        assert len(gaps) == 0

    def test_no_gap_when_no_projects_have_logging(self):
        projects = [
            _proj("a", logging_tools=[], frameworks=["FastAPI"], source_files=20),
            _proj("b", logging_tools=[], frameworks=["Flask"], source_files=20),
        ]
        conns = _find_logging_patterns(projects)
        gaps = [c for c in conns if c.type == "logging_gap"]
        assert len(gaps) == 0

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", logging_tools=["Loguru"]),
            _proj("b", logging_tools=["Loguru", "structlog"]),
        ]
        conns = find_connections(projects)
        log_types = {c.type for c in conns if "logging" in c.type}
        assert "shared_logging" in log_types


# ---------------------------------------------------------------------------
# Container Orchestration Patterns
# ---------------------------------------------------------------------------
class TestFindContainerOrchestrationPatterns:
    def test_shared_container_orch(self):
        projects = [
            _proj("a", container_orchestration=["Kubernetes", "Helm"]),
            _proj("b", container_orchestration=["Kubernetes"]),
        ]
        conns = _find_container_orchestration_patterns(projects)
        shared = [c for c in conns if c.type == "shared_container_orch"]
        assert len(shared) == 1
        assert "Kubernetes" in shared[0].detail

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", container_orchestration=["Terraform"]),
            _proj("b", container_orchestration=["Pulumi"]),
        ]
        conns = _find_container_orchestration_patterns(projects)
        shared = [c for c in conns if c.type == "shared_container_orch"]
        assert len(shared) == 0

    def test_divergence_iac_vs_k8s(self):
        projects = [
            _proj("a", container_orchestration=["Terraform"]),
            _proj("b", container_orchestration=["Kubernetes"]),
        ]
        conns = _find_container_orchestration_patterns(projects)
        divs = [c for c in conns if c.type == "container_orch_divergence"]
        assert len(divs) == 1
        assert "iac" in divs[0].detail
        assert "k8s" in divs[0].detail

    def test_divergence_compose_vs_k8s(self):
        projects = [
            _proj("a", container_orchestration=["Docker Compose"]),
            _proj("b", container_orchestration=["Helm"]),
        ]
        conns = _find_container_orchestration_patterns(projects)
        divs = [c for c in conns if c.type == "container_orch_divergence"]
        assert len(divs) == 1

    def test_no_divergence_same_category(self):
        projects = [
            _proj("a", container_orchestration=["Terraform"]),
            _proj("b", container_orchestration=["Pulumi"]),
        ]
        conns = _find_container_orchestration_patterns(projects)
        divs = [c for c in conns if c.type == "container_orch_divergence"]
        assert len(divs) == 0  # both are IaC, only 1 category

    def test_gap_docker_without_orchestration(self):
        projects = [
            _proj("a", container_orchestration=["Kubernetes"], infrastructure=["Docker"]),
            _proj("b", container_orchestration=[], infrastructure=["Docker"], source_files=20),
        ]
        conns = _find_container_orchestration_patterns(projects)
        gaps = [c for c in conns if c.type == "container_orch_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects

    def test_no_gap_all_have_orchestration(self):
        projects = [
            _proj("a", container_orchestration=["Helm"], infrastructure=["Docker"]),
            _proj("b", container_orchestration=["Terraform"], infrastructure=["Docker"]),
        ]
        conns = _find_container_orchestration_patterns(projects)
        gaps = [c for c in conns if c.type == "container_orch_gap"]
        assert len(gaps) == 0

    def test_no_gap_without_docker(self):
        projects = [
            _proj("a", container_orchestration=["Kubernetes"]),
            _proj("b", container_orchestration=[], source_files=20),
        ]
        conns = _find_container_orchestration_patterns(projects)
        gaps = [c for c in conns if c.type == "container_orch_gap"]
        assert len(gaps) == 0

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", container_orchestration=["Kubernetes"]),
            _proj("b", container_orchestration=["Kubernetes", "Helm"]),
        ]
        conns = find_connections(projects)
        co_types = {c.type for c in conns if "container_orch" in c.type}
        assert "shared_container_orch" in co_types


# ---------------------------------------------------------------------------
# Cloud Provider Patterns
# ---------------------------------------------------------------------------
class TestFindCloudProviderPatterns:
    def test_shared_cloud_provider(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=["AWS", "GCP"]),
        ]
        conns = _find_cloud_provider_patterns(projects)
        shared = [c for c in conns if c.type == "shared_cloud"]
        assert len(shared) == 1
        assert "AWS" in shared[0].detail

    def test_no_shared_when_unique(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=["GCP"]),
        ]
        conns = _find_cloud_provider_patterns(projects)
        shared = [c for c in conns if c.type == "shared_cloud"]
        assert len(shared) == 0

    def test_divergence_hyperscaler_vs_edge(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=["Cloudflare"]),
        ]
        conns = _find_cloud_provider_patterns(projects)
        divs = [c for c in conns if c.type == "cloud_divergence"]
        assert len(divs) >= 1

    def test_multi_hyperscaler_divergence(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=["GCP"]),
        ]
        conns = _find_cloud_provider_patterns(projects)
        divs = [c for c in conns if c.type == "cloud_divergence"]
        assert any("hyperscalers" in d.detail for d in divs)

    def test_no_divergence_same_provider(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=["AWS"]),
        ]
        conns = _find_cloud_provider_patterns(projects)
        divs = [c for c in conns if c.type == "cloud_divergence"]
        assert len(divs) == 0

    def test_gap_deployed_without_cloud(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=[], deploy_targets=["Vercel"], source_files=20),
        ]
        conns = _find_cloud_provider_patterns(projects)
        gaps = [c for c in conns if c.type == "cloud_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects

    def test_no_gap_all_have_cloud(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=["GCP"]),
        ]
        conns = _find_cloud_provider_patterns(projects)
        gaps = [c for c in conns if c.type == "cloud_gap"]
        assert len(gaps) == 0

    def test_no_gap_without_deploy(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=[], source_files=20),
        ]
        conns = _find_cloud_provider_patterns(projects)
        gaps = [c for c in conns if c.type == "cloud_gap"]
        assert len(gaps) == 0

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", cloud_providers=["AWS"]),
            _proj("b", cloud_providers=["AWS", "GCP"]),
        ]
        conns = find_connections(projects)
        cloud_types = {c.type for c in conns if "cloud" in c.type}
        assert "shared_cloud" in cloud_types


# ---------------------------------------------------------------------------
# _find_task_queue_patterns
# ---------------------------------------------------------------------------
class TestFindTaskQueuePatterns:
    def test_shared_task_queue(self):
        projects = [
            _proj("a", task_queues=["Celery", "RQ"]),
            _proj("b", task_queues=["Celery"]),
        ]
        conns = _find_task_queue_patterns(projects)
        shared = [c for c in conns if c.type == "shared_task_queue"]
        assert len(shared) == 1
        assert "Celery" in shared[0].detail
        assert shared[0].severity == "info"

    def test_no_shared_unique_queues(self):
        projects = [
            _proj("a", task_queues=["Celery"]),
            _proj("b", task_queues=["BullMQ"]),
        ]
        conns = _find_task_queue_patterns(projects)
        shared = [c for c in conns if c.type == "shared_task_queue"]
        assert len(shared) == 0

    def test_divergence_traditional_vs_workflow(self):
        projects = [
            _proj("a", task_queues=["Celery"]),
            _proj("b", task_queues=["Airflow"]),
        ]
        conns = _find_task_queue_patterns(projects)
        div = [c for c in conns if c.type == "task_queue_divergence"]
        assert len(div) == 1
        assert "Mixed task queue paradigms" in div[0].detail
        assert div[0].severity == "warning"

    def test_divergence_traditional_vs_cron(self):
        projects = [
            _proj("a", task_queues=["BullMQ"]),
            _proj("b", task_queues=["node-cron"]),
        ]
        conns = _find_task_queue_patterns(projects)
        div = [c for c in conns if c.type == "task_queue_divergence"]
        assert len(div) == 1

    def test_no_divergence_same_paradigm(self):
        projects = [
            _proj("a", task_queues=["Celery"]),
            _proj("b", task_queues=["BullMQ"]),
        ]
        conns = _find_task_queue_patterns(projects)
        div = [c for c in conns if c.type == "task_queue_divergence"]
        assert len(div) == 0

    def test_gap_backend_without_queues(self):
        projects = [
            _proj("a", task_queues=["Celery"], frameworks=["FastAPI"], source_files=30),
            _proj("b", task_queues=[], frameworks=["Django"], source_files=30),
        ]
        conns = _find_task_queue_patterns(projects)
        gaps = [c for c in conns if c.type == "task_queue_gap"]
        assert len(gaps) == 1
        assert "b" in gaps[0].projects
        assert gaps[0].severity == "warning"

    def test_no_gap_all_have_queues(self):
        projects = [
            _proj("a", task_queues=["Celery"], frameworks=["FastAPI"], source_files=30),
            _proj("b", task_queues=["RQ"], frameworks=["Flask"], source_files=30),
        ]
        conns = _find_task_queue_patterns(projects)
        gaps = [c for c in conns if c.type == "task_queue_gap"]
        assert len(gaps) == 0

    def test_no_gap_without_backend_framework(self):
        projects = [
            _proj("a", task_queues=["Celery"]),
            _proj("b", task_queues=[], frameworks=["React"], source_files=30),
        ]
        conns = _find_task_queue_patterns(projects)
        gaps = [c for c in conns if c.type == "task_queue_gap"]
        assert len(gaps) == 0

    def test_no_gap_small_project(self):
        projects = [
            _proj("a", task_queues=["Celery"]),
            _proj("b", task_queues=[], frameworks=["FastAPI"], source_files=5),
        ]
        conns = _find_task_queue_patterns(projects)
        gaps = [c for c in conns if c.type == "task_queue_gap"]
        assert len(gaps) == 0

    def test_integration_with_find_connections(self):
        projects = [
            _proj("a", task_queues=["Celery"]),
            _proj("b", task_queues=["Celery", "RQ"]),
        ]
        conns = find_connections(projects)
        queue_types = {c.type for c in conns if "task_queue" in c.type}
        assert "shared_task_queue" in queue_types
