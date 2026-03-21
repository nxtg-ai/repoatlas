"""Recommendations engine — turns health data into actionable suggestions."""
from __future__ import annotations

from dataclasses import dataclass

from atlas.connections import find_connections
from atlas.models import Portfolio, Project


@dataclass
class Recommendation:
    priority: str  # critical, high, medium, low
    category: str  # tests, git, docs, structure, deps, security, quality, infra
    message: str
    projects: list[str]

    @property
    def icon(self) -> str:
        return {
            "critical": "[red]\u2716[/red]",
            "high": "[yellow]\u26a0[/yellow]",
            "medium": "[cyan]\u2139[/cyan]",
            "low": "[dim]\u2022[/dim]",
        }.get(self.priority, " ")


PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def generate_recommendations(portfolio: Portfolio) -> list[Recommendation]:
    """Analyze portfolio and return prioritized recommendations."""
    recs: list[Recommendation] = []

    for project in portfolio.projects:
        recs.extend(_project_recommendations(project))

    if len(portfolio.projects) > 1:
        recs.extend(_cross_project_recommendations(portfolio))

    recs.sort(key=lambda r: (PRIORITY_ORDER.get(r.priority, 99), r.category))
    return recs


def _project_recommendations(project: Project) -> list[Recommendation]:
    """Generate recommendations for a single project."""
    recs: list[Recommendation] = []
    name = project.name

    # --- Tests ---
    if project.test_file_count == 0 and project.source_file_count > 5:
        recs.append(Recommendation(
            priority="critical",
            category="tests",
            message=f"Zero tests in {name} ({project.source_file_count} source files). Add test coverage.",
            projects=[name],
        ))
    elif project.health.tests < 0.5 and project.source_file_count > 5:
        recs.append(Recommendation(
            priority="high",
            category="tests",
            message=f"Low test coverage in {name} ({project.test_file_count} test files / {project.source_file_count} source files).",
            projects=[name],
        ))

    # --- Git hygiene ---
    if project.git_info.uncommitted_changes > 50:
        recs.append(Recommendation(
            priority="high",
            category="git",
            message=f"{name} has {project.git_info.uncommitted_changes} uncommitted changes. Commit or stash.",
            projects=[name],
        ))
    elif project.git_info.uncommitted_changes > 10:
        recs.append(Recommendation(
            priority="medium",
            category="git",
            message=f"{name} has {project.git_info.uncommitted_changes} uncommitted changes.",
            projects=[name],
        ))

    if not project.git_info.has_remote and project.git_info.total_commits > 0:
        recs.append(Recommendation(
            priority="high",
            category="git",
            message=f"{name} has no remote. Push to GitHub/GitLab for backup.",
            projects=[name],
        ))

    # --- Documentation ---
    if project.health.documentation < 0.2:
        recs.append(Recommendation(
            priority="high",
            category="docs",
            message=f"{name} has minimal documentation. Add a README.",
            projects=[name],
        ))
    elif project.health.documentation < 0.5:
        recs.append(Recommendation(
            priority="medium",
            category="docs",
            message=f"{name} documentation is sparse. Consider adding CHANGELOG or docs/.",
            projects=[name],
        ))

    # --- Structure ---
    if project.health.structure < 0.3 and project.source_file_count > 5:
        recs.append(Recommendation(
            priority="high",
            category="structure",
            message=f"{name} has no CI. Add a GitHub Actions workflow.",
            projects=[name],
        ))

    # --- Security ---
    if not project.tech_stack.security_tools and project.source_file_count > 5:
        recs.append(Recommendation(
            priority="high",
            category="security",
            message=f"{name} has no security tooling. Add Dependabot + Gitleaks.",
            projects=[name],
        ))
    else:
        dep_scanners = {"Dependabot", "Renovate", "Snyk", "pip-audit", "Safety"}
        if project.tech_stack.security_tools and not any(
            t in dep_scanners for t in project.tech_stack.security_tools
        ):
            recs.append(Recommendation(
                priority="medium",
                category="security",
                message=f"{name} has no dependency scanning. Add Dependabot or Renovate.",
                projects=[name],
            ))

        secret_scanners = {"Gitleaks", "detect-secrets", "SOPS"}
        if project.tech_stack.security_tools and not any(
            t in secret_scanners for t in project.tech_stack.security_tools
        ):
            recs.append(Recommendation(
                priority="medium",
                category="security",
                message=f"{name} has no secret scanning. Add Gitleaks or detect-secrets.",
                projects=[name],
            ))

    # --- Quality ---
    if not project.tech_stack.quality_tools and project.source_file_count > 5:
        recs.append(Recommendation(
            priority="high",
            category="quality",
            message=f"{name} has no code quality tooling. Add a linter and type checker.",
            projects=[name],
        ))
    else:
        linters = {"Ruff", "Flake8", "Pylint", "ESLint", "Biome", "golangci-lint", "Clippy"}
        if project.tech_stack.quality_tools and not any(
            t in linters for t in project.tech_stack.quality_tools
        ):
            recs.append(Recommendation(
                priority="medium",
                category="quality",
                message=f"{name} has no linter. Add Ruff (Python) or ESLint (JS/TS).",
                projects=[name],
            ))

        type_checkers = {"mypy", "Pyright", "TypeScript"}
        if project.tech_stack.quality_tools and not any(
            t in type_checkers for t in project.tech_stack.quality_tools
        ):
            recs.append(Recommendation(
                priority="medium",
                category="quality",
                message=f"{name} has no type checking. Add mypy or Pyright.",
                projects=[name],
            ))

    # --- Infrastructure ---
    ci_systems = {"GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"}
    if project.source_file_count > 5 and not any(
        i in ci_systems for i in project.tech_stack.infrastructure
    ):
        recs.append(Recommendation(
            priority="high",
            category="infra",
            message=f"{name} has no CI/CD pipeline. Add GitHub Actions.",
            projects=[name],
        ))

    return recs


def _cross_project_recommendations(portfolio: Portfolio) -> list[Recommendation]:
    """Generate recommendations from cross-project analysis."""
    recs: list[Recommendation] = []
    connections = find_connections(portfolio.projects)

    severity_to_priority = {"critical": "critical", "warning": "high", "info": "medium"}
    type_to_category = {
        "security_gap": "security",
        "security_divergence": "security",
        "infra_gap": "infra",
        "infra_divergence": "infra",
        "quality_gap": "quality",
        "quality_divergence": "quality",
        "ai_gap": "ai",
        "ai_divergence": "ai",
        "testing_gap": "tests",
        "testing_divergence": "tests",
        "database_gap": "deps",
        "database_divergence": "deps",
        "pkg_manager_divergence": "deps",
        "license_gap": "docs",
        "license_divergence": "docs",
        "docs_gap": "docs",
        "docs_divergence": "docs",
        "ci_config_gap": "infra",
        "ci_config_divergence": "infra",
        "runtime_gap": "infra",
        "runtime_divergence": "deps",
        "build_tool_gap": "infra",
        "build_tool_divergence": "infra",
        "api_spec_gap": "infra",
        "api_spec_divergence": "infra",
        "monitoring_gap": "infra",
        "monitoring_divergence": "infra",
        "auth_gap": "infra",
        "auth_divergence": "infra",
        "messaging_gap": "infra",
        "messaging_divergence": "infra",
        "deploy_gap": "infra",
        "deploy_divergence": "infra",
        "state_mgmt_gap": "frontend",
        "state_mgmt_divergence": "frontend",
        "css_gap": "frontend",
        "css_divergence": "frontend",
        "bundler_gap": "frontend",
        "bundler_divergence": "frontend",
        "orm_gap": "database",
        "orm_divergence": "database",
        "i18n_gap": "frontend",
        "i18n_divergence": "frontend",
        "validation_gap": "quality",
        "validation_divergence": "quality",
        "logging_gap": "infra",
        "logging_divergence": "infra",
        "container_orch_gap": "infra",
        "container_orch_divergence": "infra",
        "cloud_gap": "infra",
        "cloud_divergence": "infra",
        "task_queue_gap": "infra",
        "task_queue_divergence": "infra",
        "search_gap": "infra",
        "search_divergence": "infra",
        "feature_flag_gap": "infra",
        "feature_flag_divergence": "infra",
        "http_client_gap": "deps",
        "http_client_divergence": "deps",
        "doc_generator_gap": "docs",
        "doc_generator_divergence": "docs",
        "cli_framework_divergence": "deps",
        "config_tool_gap": "deps",
        "config_tool_divergence": "deps",
        "caching_gap": "deps",
        "caching_divergence": "deps",
        "template_engine_divergence": "deps",
        "serialization_divergence": "deps",
        "di_divergence": "deps",
        "websocket_divergence": "deps",
        "graphql_divergence": "deps",
        "event_streaming_divergence": "infra",
        "payment_divergence": "deps",
        "date_lib_divergence": "deps",
    }

    for conn in connections:
        if conn.type == "version_mismatch":
            recs.append(Recommendation(
                priority="high",
                category="deps",
                message=f"Version mismatch: {conn.detail}. Standardize across projects.",
                projects=conn.projects,
            ))
        elif conn.type == "health_gap" and conn.severity == "critical":
            recs.append(Recommendation(
                priority="critical",
                category="tests",
                message=conn.detail,
                projects=conn.projects,
            ))
        elif conn.type in type_to_category:
            recs.append(Recommendation(
                priority=severity_to_priority.get(conn.severity, "medium"),
                category=type_to_category[conn.type],
                message=conn.detail,
                projects=conn.projects,
            ))

    # Overall portfolio health
    low_health = [
        p for p in portfolio.projects
        if p.health.overall < 0.6
    ]
    if low_health:
        worst = min(low_health, key=lambda p: p.health.overall)
        recs.append(Recommendation(
            priority="medium",
            category="structure",
            message=f"Focus improvements on {worst.name} (grade {worst.health.grade}, {worst.health.percent}%) — lowest health in portfolio.",
            projects=[worst.name],
        ))

    return recs
