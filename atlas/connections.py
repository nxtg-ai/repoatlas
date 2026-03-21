"""Cross-project intelligence — finds shared deps, version mismatches, reuse candidates."""
from __future__ import annotations

from collections import defaultdict

from atlas.models import Connection, Project


def find_connections(projects: list[Project]) -> list[Connection]:
    """Analyze cross-project patterns and return connections."""
    connections: list[Connection] = []
    connections.extend(_find_shared_deps(projects))
    connections.extend(_find_shared_frameworks(projects))
    connections.extend(_find_version_mismatches(projects))
    connections.extend(_find_health_gaps(projects))
    connections.extend(_find_shared_databases(projects))
    connections.extend(_find_infra_patterns(projects))
    connections.extend(_find_security_patterns(projects))
    connections.extend(_find_quality_patterns(projects))
    connections.extend(_find_ai_patterns(projects))
    return connections


def _find_shared_deps(projects: list[Project]) -> list[Connection]:
    """Find dependencies used by 2+ projects."""
    dep_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for dep_name in proj.tech_stack.key_deps:
            dep_to_projects[dep_name].append(proj.name)

    connections = []
    important_deps = {
        "fastapi", "react", "next", "express", "sqlalchemy",
        "pydantic", "anthropic", "openai", "django", "flask",
        "pytest", "vitest", "jest", "tailwindcss", "drizzle-orm",
        "prisma", "redis", "celery",
    }

    for dep, projs in sorted(dep_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2 and dep.lower() in important_deps:
            connections.append(Connection(
                type="shared_dep",
                detail=f"{dep} used across {len(projs)} projects",
                projects=projs,
                severity="info",
            ))

    return connections[:10]


def _find_shared_frameworks(projects: list[Project]) -> list[Connection]:
    """Find framework patterns across projects."""
    fw_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for fw in proj.tech_stack.frameworks:
            fw_to_projects[fw].append(proj.name)

    connections = []
    for fw, projs in sorted(fw_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 3:
            connections.append(Connection(
                type="shared_framework",
                detail=f"{fw} in {len(projs)} projects — standardize patterns",
                projects=projs,
                severity="info",
            ))

    return connections[:5]


def _find_version_mismatches(projects: list[Project]) -> list[Connection]:
    """Find dependency version inconsistencies."""
    dep_versions: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))

    for proj in projects:
        for dep, version in proj.tech_stack.key_deps.items():
            dep_versions[dep][version].append(proj.name)

    connections = []
    for dep, versions in dep_versions.items():
        if len(versions) >= 2:
            version_summary = ", ".join(
                f"{v} ({', '.join(ps)})" for v, ps in versions.items()
            )
            all_projects = [p for ps in versions.values() for p in ps]
            connections.append(Connection(
                type="version_mismatch",
                detail=f"{dep}: {version_summary}",
                projects=all_projects,
                severity="warning",
            ))

    return connections[:8]


def _find_health_gaps(projects: list[Project]) -> list[Connection]:
    """Find projects with critical health issues."""
    connections = []

    no_tests = [p.name for p in projects if p.test_file_count == 0 and p.source_file_count > 5]
    if no_tests:
        connections.append(Connection(
            type="health_gap",
            detail=f"{len(no_tests)} projects have zero tests",
            projects=no_tests,
            severity="critical",
        ))

    dirty = [p.name for p in projects if p.git_info.uncommitted_changes > 10]
    if dirty:
        connections.append(Connection(
            type="health_gap",
            detail=f"{len(dirty)} projects have 10+ uncommitted changes",
            projects=dirty,
            severity="warning",
        ))

    stale = [
        p.name for p in projects
        if p.git_info.total_commits > 0 and p.git_info.total_commits < 5
        and p.source_file_count > 5
    ]
    if stale:
        connections.append(Connection(
            type="health_gap",
            detail=f"{len(stale)} projects appear stale (<5 commits)",
            projects=stale,
            severity="warning",
        ))

    return connections


def _find_shared_databases(projects: list[Project]) -> list[Connection]:
    """Find shared database patterns."""
    db_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for db in proj.tech_stack.databases:
            db_to_projects[db].append(proj.name)

    connections = []
    for db, projs in sorted(db_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_database",
                detail=f"{db} used across {len(projs)} projects — unify connection patterns",
                projects=projs,
                severity="info",
            ))

    return connections[:5]


def _find_infra_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project infrastructure patterns."""
    connections: list[Connection] = []
    infra_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for item in proj.tech_stack.infrastructure:
            infra_to_projects[item].append(proj.name)

    # Shared infrastructure (2+ projects)
    for item, projs in sorted(infra_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_infra",
                detail=f"{item} used across {len(projs)} projects — standardize config",
                projects=projs,
                severity="info",
            ))

    # Platform divergence — multiple hosting platforms
    hosting = {"Vercel", "Netlify", "Fly.io", "Render", "Cloudflare Workers", "Serverless Framework"}
    host_found: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for item in proj.tech_stack.infrastructure:
            if item in hosting:
                host_found[proj.name].append(item)
    multi_host = {p: hosts for p, hosts in host_found.items() if len(hosts) >= 2}
    if multi_host:
        for proj_name, hosts in multi_host.items():
            connections.append(Connection(
                type="infra_divergence",
                detail=f"{proj_name} uses {', '.join(hosts)} — consolidate hosting",
                projects=[proj_name],
                severity="warning",
            ))

    # CI divergence — multiple CI systems across portfolio
    ci_systems = {"GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"}
    ci_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for item in proj.tech_stack.infrastructure:
            if item in ci_systems:
                ci_to_projects[item].append(proj.name)
    if len(ci_to_projects) >= 2:
        detail_parts = [f"{ci} ({', '.join(ps[:3])})" for ci, ps in ci_to_projects.items()]
        all_ci_projects = list({p for ps in ci_to_projects.values() for p in ps})
        connections.append(Connection(
            type="infra_divergence",
            detail=f"Multiple CI systems: {', '.join(detail_parts)} — standardize",
            projects=all_ci_projects,
            severity="warning",
        ))

    # No CI detected
    has_ci = {p for ps in ci_to_projects.values() for p in ps}
    no_ci = [p.name for p in projects if p.name not in has_ci and p.source_file_count > 5]
    if no_ci:
        connections.append(Connection(
            type="infra_gap",
            detail=f"{len(no_ci)} projects have no CI/CD detected",
            projects=no_ci,
            severity="critical",
        ))

    # Cloud usage without IaC
    iac_tools = {"Terraform", "Pulumi", "AWS CDK"}
    cloud_providers = {"AWS", "GCP", "Azure"}
    has_iac = any(
        item in iac_tools
        for proj in projects
        for item in proj.tech_stack.infrastructure
    )
    cloud_projects = [
        p.name for p in projects
        if any(item in cloud_providers for item in p.tech_stack.infrastructure)
    ]
    if cloud_projects and not has_iac:
        connections.append(Connection(
            type="infra_gap",
            detail=f"{len(cloud_projects)} projects use cloud services without IaC — add Terraform/Pulumi",
            projects=cloud_projects,
            severity="warning",
        ))

    # Docker without orchestration
    has_docker = [
        p.name for p in projects
        if "Docker" in p.tech_stack.infrastructure
    ]
    has_orch = any(
        item in {"Kubernetes", "Docker Compose"}
        for proj in projects
        for item in proj.tech_stack.infrastructure
    )
    if len(has_docker) >= 3 and not has_orch:
        connections.append(Connection(
            type="infra_gap",
            detail=f"{len(has_docker)} projects use Docker without orchestration — consider Compose/K8s",
            projects=has_docker,
            severity="info",
        ))

    return connections[:10]


def _find_security_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project security patterns."""
    connections: list[Connection] = []
    sec_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for tool in proj.tech_stack.security_tools:
            sec_to_projects[tool].append(proj.name)

    # Shared security tools (2+ projects)
    for tool, projs in sorted(sec_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_security",
                detail=f"{tool} used across {len(projs)} projects — standardize config",
                projects=projs,
                severity="info",
            ))

    # No security tooling at all
    no_security = [p.name for p in projects if not p.tech_stack.security_tools and p.source_file_count > 5]
    if no_security:
        connections.append(Connection(
            type="security_gap",
            detail=f"{len(no_security)} projects have no security tooling",
            projects=no_security,
            severity="critical",
        ))

    # Missing dependency scanning
    dep_scanners = {"Dependabot", "Renovate", "Snyk", "pip-audit", "Safety"}
    no_dep_scan = [
        p.name for p in projects
        if p.tech_stack.security_tools
        and not any(t in dep_scanners for t in p.tech_stack.security_tools)
        and p.source_file_count > 5
    ]
    if no_dep_scan:
        connections.append(Connection(
            type="security_gap",
            detail=f"{len(no_dep_scan)} projects lack dependency scanning — add Dependabot/Renovate",
            projects=no_dep_scan,
            severity="warning",
        ))

    # Missing secret scanning
    secret_scanners = {"Gitleaks", "detect-secrets", "SOPS"}
    no_secret_scan = [
        p.name for p in projects
        if p.tech_stack.security_tools
        and not any(t in secret_scanners for t in p.tech_stack.security_tools)
        and p.source_file_count > 5
    ]
    if no_secret_scan:
        connections.append(Connection(
            type="security_gap",
            detail=f"{len(no_secret_scan)} projects lack secret scanning — add Gitleaks/detect-secrets",
            projects=no_secret_scan,
            severity="warning",
        ))

    # Dep scanner divergence — multiple dep scanners across portfolio
    dep_scan_tools = {"Dependabot", "Renovate", "Snyk"}
    dep_scan_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for tool in proj.tech_stack.security_tools:
            if tool in dep_scan_tools:
                dep_scan_to_projects[tool].append(proj.name)
    if len(dep_scan_to_projects) >= 2:
        detail_parts = [f"{tool} ({', '.join(ps[:3])})" for tool, ps in dep_scan_to_projects.items()]
        all_projects = list({p for ps in dep_scan_to_projects.values() for p in ps})
        connections.append(Connection(
            type="security_divergence",
            detail=f"Multiple dep scanners: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    return connections[:10]


def _find_quality_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project code quality patterns."""
    connections: list[Connection] = []
    qt_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for tool in proj.tech_stack.quality_tools:
            qt_to_projects[tool].append(proj.name)

    # Shared quality tools (2+ projects)
    for tool, projs in sorted(qt_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_quality",
                detail=f"{tool} used across {len(projs)} projects — share config",
                projects=projs,
                severity="info",
            ))

    # No quality tooling at all
    no_quality = [p.name for p in projects if not p.tech_stack.quality_tools and p.source_file_count > 5]
    if no_quality:
        connections.append(Connection(
            type="quality_gap",
            detail=f"{len(no_quality)} projects have no code quality tooling",
            projects=no_quality,
            severity="critical",
        ))

    # Missing linting
    linters = {"Ruff", "Flake8", "Pylint", "ESLint", "Biome", "golangci-lint", "Clippy"}
    no_linting = [
        p.name for p in projects
        if p.tech_stack.quality_tools
        and not any(t in linters for t in p.tech_stack.quality_tools)
        and p.source_file_count > 5
    ]
    if no_linting:
        connections.append(Connection(
            type="quality_gap",
            detail=f"{len(no_linting)} projects lack linting — add Ruff/ESLint",
            projects=no_linting,
            severity="warning",
        ))

    # Missing type checking
    type_checkers = {"mypy", "Pyright", "TypeScript"}
    no_types = [
        p.name for p in projects
        if p.tech_stack.quality_tools
        and not any(t in type_checkers for t in p.tech_stack.quality_tools)
        and p.source_file_count > 5
    ]
    if no_types:
        connections.append(Connection(
            type="quality_gap",
            detail=f"{len(no_types)} projects lack type checking — add mypy/Pyright/TypeScript",
            projects=no_types,
            severity="warning",
        ))

    # Linter divergence — multiple linters across portfolio
    linter_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for tool in proj.tech_stack.quality_tools:
            if tool in linters:
                linter_to_projects[tool].append(proj.name)
    if len(linter_to_projects) >= 2:
        detail_parts = [f"{tool} ({', '.join(ps[:3])})" for tool, ps in linter_to_projects.items()]
        all_projects = list({p for ps in linter_to_projects.values() for p in ps})
        connections.append(Connection(
            type="quality_divergence",
            detail=f"Multiple linters: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    return connections[:10]


def _find_ai_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project AI/ML patterns."""
    connections: list[Connection] = []
    ai_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for tool in proj.tech_stack.ai_tools:
            ai_to_projects[tool].append(proj.name)

    # Shared AI/ML tools (2+ projects)
    for tool, projs in sorted(ai_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_ai",
                detail=f"{tool} used across {len(projs)} projects — share patterns",
                projects=projs,
                severity="info",
            ))

    # LLM provider divergence — multiple providers across portfolio
    llm_providers = {"Anthropic SDK", "OpenAI"}
    llm_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for tool in proj.tech_stack.ai_tools:
            if tool in llm_providers:
                llm_to_projects[tool].append(proj.name)
    if len(llm_to_projects) >= 2:
        detail_parts = [f"{p} ({', '.join(ps[:3])})" for p, ps in llm_to_projects.items()]
        all_projects = list({p for ps in llm_to_projects.values() for p in ps})
        connections.append(Connection(
            type="ai_divergence",
            detail=f"Multiple LLM providers: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Vector DB divergence — multiple vector DBs across portfolio
    vector_dbs = {"ChromaDB", "Pinecone", "Sentence Transformers"}
    vdb_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for tool in proj.tech_stack.ai_tools:
            if tool in vector_dbs:
                vdb_to_projects[tool].append(proj.name)
    if len(vdb_to_projects) >= 2:
        detail_parts = [f"{db} ({', '.join(ps[:3])})" for db, ps in vdb_to_projects.items()]
        all_projects = list({p for ps in vdb_to_projects.values() for p in ps})
        connections.append(Connection(
            type="ai_divergence",
            detail=f"Multiple vector DBs: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # ML projects without experiment tracking
    ml_frameworks = {"PyTorch", "TensorFlow", "Transformers", "scikit-learn"}
    experiment_tracking = {"MLflow", "W&B", "DVC"}
    ml_no_tracking = [
        p.name for p in projects
        if any(t in ml_frameworks for t in p.tech_stack.ai_tools)
        and not any(t in experiment_tracking for t in p.tech_stack.ai_tools)
    ]
    if ml_no_tracking:
        connections.append(Connection(
            type="ai_gap",
            detail=f"{len(ml_no_tracking)} ML projects lack experiment tracking — add MLflow/W&B",
            projects=ml_no_tracking,
            severity="warning",
        ))

    return connections[:10]
