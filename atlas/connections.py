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

    no_ci = [
        p.name for p in projects
        if not (p.health.structure >= 0.3)
        and p.source_file_count > 5
    ]
    # Note: structure score >= 0.3 means CI exists

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
