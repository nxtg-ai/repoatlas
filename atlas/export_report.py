"""Portfolio report generation — markdown and JSON formats."""
from __future__ import annotations

import json as json_mod
from collections import Counter

from atlas.connections import find_connections
from atlas.models import Portfolio, Project
from atlas.recommendations import generate_recommendations


def build_markdown_report(portfolio: Portfolio) -> str:
    """Build a comprehensive markdown portfolio report."""
    lines: list[str] = []

    # Header
    lines.append(f"# {portfolio.name} — Portfolio Report")
    lines.append("")
    lines.append(f"**Scanned**: {portfolio.last_scan[:19] if portfolio.last_scan else 'Never'}")
    lines.append(
        f"**Projects**: {len(portfolio.projects)} | "
        f"**Test Files**: {portfolio.total_tests:,} | "
        f"**LOC**: {portfolio.total_loc:,} | "
        f"**Health**: {portfolio.avg_grade} ({int(portfolio.avg_health * 100)}%)"
    )
    lines.append("")

    # Project table
    lines.append("## Projects")
    lines.append("")
    lines.append("| Project | Health | Tests | LOC | Stack |")
    lines.append("|---------|--------|-------|-----|-------|")
    sorted_projects = sorted(portfolio.projects, key=lambda x: x.health.overall, reverse=True)
    for p in sorted_projects:
        lines.append(
            f"| {p.name} | {p.health.grade} ({p.health.percent}%) | "
            f"{p.test_file_count:,} | {p.loc:,} | {p.tech_stack.summary} |"
        )
    lines.append("")

    # Portfolio summary
    if len(portfolio.projects) >= 2:
        lines.extend(_portfolio_summary(portfolio))

    # Per-project details
    lines.extend(_project_details(sorted_projects))

    # Cross-project intelligence
    conns = find_connections(portfolio.projects)
    if conns:
        lines.extend(_connections_section(conns))

    return "\n".join(lines)


def _portfolio_summary(portfolio: Portfolio) -> list[str]:
    """Build portfolio summary stats section."""
    lines: list[str] = []
    projects = portfolio.projects
    n = len(projects)

    lines.append("## Portfolio Summary")
    lines.append("")

    # Languages
    lang_counter: Counter[str] = Counter()
    for p in projects:
        for lang in p.tech_stack.primary_languages:
            lang_counter[lang] += 1
    if lang_counter:
        top = lang_counter.most_common(8)
        lines.append(f"**Languages**: {', '.join(f'{lang} ({cnt})' for lang, cnt in top)}")

    # Frameworks
    fw_counter: Counter[str] = Counter()
    for p in projects:
        for fw in p.tech_stack.frameworks:
            if fw != "Docker":
                fw_counter[fw] += 1
    if fw_counter:
        top = fw_counter.most_common(8)
        lines.append(f"**Frameworks**: {', '.join(f'{f} ({c})' for f, c in top)}")

    # Infrastructure
    ci_systems = {"GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"}
    has_ci = sum(1 for p in projects if any(i in p.tech_stack.infrastructure for i in ci_systems))
    has_docker = sum(1 for p in projects if "Docker" in p.tech_stack.infrastructure)
    lines.append(f"**Infrastructure**: CI/CD {has_ci}/{n} · Docker {has_docker}/{n}")

    # Security
    has_security = sum(1 for p in projects if p.tech_stack.security_tools)
    lines.append(f"**Security**: {has_security}/{n} projects have security tooling")

    # Testing
    has_testing = sum(1 for p in projects if p.tech_stack.testing_frameworks)
    if has_testing:
        tf_counter: Counter[str] = Counter()
        for p in projects:
            for tf in p.tech_stack.testing_frameworks:
                tf_counter[tf] += 1
        top_tf = tf_counter.most_common(6)
        lines.append(f"**Testing**: {has_testing}/{n} projects · {', '.join(t for t, _ in top_tf)}")

    # Databases
    has_db = sum(1 for p in projects if p.tech_stack.databases)
    if has_db:
        db_counter: Counter[str] = Counter()
        for p in projects:
            for db in p.tech_stack.databases:
                db_counter[db] += 1
        top_db = db_counter.most_common(6)
        lines.append(f"**Databases**: {has_db}/{n} projects · {', '.join(t for t, _ in top_db)}")

    # Package managers
    has_pm = sum(1 for p in projects if p.tech_stack.package_managers)
    if has_pm:
        pm_counter: Counter[str] = Counter()
        for p in projects:
            for pm in p.tech_stack.package_managers:
                pm_counter[pm] += 1
        top_pm = pm_counter.most_common(6)
        lines.append(f"**Pkg Managers**: {has_pm}/{n} projects · {', '.join(t for t, _ in top_pm)}")

    # AI/ML
    has_ai = sum(1 for p in projects if p.tech_stack.ai_tools)
    if has_ai:
        ai_counter: Counter[str] = Counter()
        for p in projects:
            for tool in p.tech_stack.ai_tools:
                ai_counter[tool] += 1
        top_ai = ai_counter.most_common(5)
        lines.append(f"**AI/ML**: {has_ai}/{n} projects · {', '.join(t for t, _ in top_ai)}")

    # Documentation artifacts
    has_docs = sum(1 for p in projects if p.tech_stack.docs_artifacts)
    if has_docs:
        da_counter: Counter[str] = Counter()
        for p in projects:
            for da in p.tech_stack.docs_artifacts:
                da_counter[da] += 1
        top_da = da_counter.most_common(6)
        lines.append(f"**Docs**: {has_docs}/{n} projects · {', '.join(t for t, _ in top_da)}")

    # CI/CD configuration
    has_ci_config = sum(1 for p in projects if p.tech_stack.ci_config)
    if has_ci_config:
        ci_counter: Counter[str] = Counter()
        for p in projects:
            for ci in p.tech_stack.ci_config:
                ci_counter[ci] += 1
        top_ci = ci_counter.most_common(6)
        lines.append(f"**CI Config**: {has_ci_config}/{n} projects · {', '.join(t for t, _ in top_ci)}")

    # Runtime versions
    has_runtimes = sum(1 for p in projects if p.tech_stack.runtime_versions)
    if has_runtimes:
        rv_counter: Counter[str] = Counter()
        for p in projects:
            for rt in p.tech_stack.runtime_versions:
                rv_counter[rt] += 1
        top_rv = rv_counter.most_common(6)
        lines.append(f"**Runtimes**: {has_runtimes}/{n} projects · {', '.join(t for t, _ in top_rv)}")

    # Licenses
    lic_counter: Counter[str] = Counter()
    for p in projects:
        if p.license:
            lic_counter[p.license] += 1
    has_license = sum(1 for p in projects if p.license)
    if has_license:
        top_lic = lic_counter.most_common(6)
        lines.append(f"**Licenses**: {has_license}/{n} projects · {', '.join(t for t, _ in top_lic)}")

    lines.append("")
    return lines


def _project_details(projects: list[Project]) -> list[str]:
    """Build per-project detail sections."""
    lines: list[str] = []
    lines.append("## Project Details")
    lines.append("")

    for p in projects:
        lines.append(f"### {p.name}")
        lines.append("")
        lines.append(f"- **Health**: {p.health.grade} ({p.health.percent}%)")
        lines.append(
            f"  - Tests: {int(p.health.tests * 100)}% · "
            f"Git: {int(p.health.git_hygiene * 100)}% · "
            f"Docs: {int(p.health.documentation * 100)}% · "
            f"Structure: {int(p.health.structure * 100)}%"
        )
        lines.append(f"- **Files**: {p.source_file_count:,} source · {p.test_file_count:,} tests · {p.loc:,} LOC")
        lines.append(f"- **Stack**: {p.tech_stack.summary}")

        if p.tech_stack.frameworks:
            lines.append(f"- **Frameworks**: {', '.join(p.tech_stack.frameworks[:8])}")
        if p.tech_stack.databases:
            lines.append(f"- **Databases**: {', '.join(p.tech_stack.databases)}")
        if p.tech_stack.infrastructure:
            lines.append(f"- **Infrastructure**: {', '.join(p.tech_stack.infrastructure[:8])}")
        if p.tech_stack.security_tools:
            lines.append(f"- **Security**: {', '.join(p.tech_stack.security_tools[:8])}")
        if p.tech_stack.ai_tools:
            lines.append(f"- **AI/ML**: {', '.join(p.tech_stack.ai_tools[:8])}")
        if p.tech_stack.quality_tools:
            lines.append(f"- **Quality**: {', '.join(p.tech_stack.quality_tools[:8])}")
        if p.tech_stack.testing_frameworks:
            lines.append(f"- **Testing**: {', '.join(p.tech_stack.testing_frameworks[:8])}")
        if p.tech_stack.package_managers:
            lines.append(f"- **Pkg Managers**: {', '.join(p.tech_stack.package_managers[:8])}")
        if p.tech_stack.docs_artifacts:
            lines.append(f"- **Docs**: {', '.join(p.tech_stack.docs_artifacts[:8])}")
        if p.tech_stack.ci_config:
            lines.append(f"- **CI Config**: {', '.join(p.tech_stack.ci_config[:8])}")
        if p.tech_stack.runtime_versions:
            rv = ", ".join(f"{k} {v}" for k, v in p.tech_stack.runtime_versions.items())
            lines.append(f"- **Runtimes**: {rv}")

        if p.license:
            lines.append(f"- **License**: {p.license}")

        if p.git_info.branch:
            lines.append(f"- **Git**: {p.git_info.branch} · {p.git_info.total_commits:,} commits")
            if p.git_info.uncommitted_changes > 0:
                lines.append(f"  - {p.git_info.uncommitted_changes} uncommitted changes")

        lines.append("")

    return lines


def _connections_section(conns: list) -> list[str]:
    """Build cross-project intelligence section."""
    lines: list[str] = []
    lines.append("## Cross-Project Intelligence")
    lines.append("")

    # Group by type
    groups: dict[str, list] = {}
    for conn in conns:
        groups.setdefault(conn.type, []).append(conn)

    type_labels = {
        "shared_dep": "Shared Dependencies",
        "shared_framework": "Shared Frameworks",
        "version_mismatch": "Version Mismatches",
        "health_gap": "Health Gaps",
        "shared_database": "Shared Databases",
        "database_divergence": "Database Divergence",
        "database_gap": "Database Gaps",
        "shared_infra": "Shared Infrastructure",
        "infra_divergence": "Infrastructure Divergence",
        "infra_gap": "Infrastructure Gaps",
        "shared_security": "Shared Security Tools",
        "security_divergence": "Security Divergence",
        "security_gap": "Security Gaps",
        "shared_quality": "Shared Quality Tools",
        "quality_divergence": "Quality Divergence",
        "quality_gap": "Quality Gaps",
        "shared_ai": "Shared AI/ML Tools",
        "ai_divergence": "AI/ML Divergence",
        "ai_gap": "AI/ML Gaps",
        "shared_testing": "Shared Testing Frameworks",
        "testing_divergence": "Testing Divergence",
        "testing_gap": "Testing Gaps",
        "shared_pkg_manager": "Shared Package Managers",
        "pkg_manager_divergence": "Package Manager Divergence",
        "shared_license": "Shared Licenses",
        "license_divergence": "License Divergence",
        "license_gap": "License Gaps",
        "shared_docs": "Shared Documentation",
        "docs_divergence": "Documentation Divergence",
        "docs_gap": "Documentation Gaps",
        "shared_ci_config": "Shared CI/CD Config",
        "ci_config_divergence": "CI/CD Config Divergence",
        "ci_config_gap": "CI/CD Config Gaps",
    }

    severity_icons = {"info": "ℹ️", "warning": "⚠️", "critical": "❌"}

    for conn_type, group in groups.items():
        label = type_labels.get(conn_type, conn_type)
        lines.append(f"### {label}")
        lines.append("")
        for conn in group:
            icon = severity_icons.get(conn.severity, "-")
            projs = ", ".join(conn.projects[:4])
            if len(conn.projects) > 4:
                projs += f" +{len(conn.projects) - 4}"
            lines.append(f"- {icon} {conn.detail} ({projs})")
        lines.append("")

    return lines


def build_json_report(portfolio: Portfolio) -> str:
    """Build a comprehensive JSON portfolio report."""
    projects = portfolio.projects
    conns = find_connections(projects) if len(projects) > 1 else []
    recs = generate_recommendations(portfolio)

    data: dict = {
        "name": portfolio.name,
        "scanned": portfolio.last_scan,
        "summary": {
            "projects": len(projects),
            "test_files": portfolio.total_tests,
            "loc": portfolio.total_loc,
            "health_grade": portfolio.avg_grade,
            "health_percent": int(portfolio.avg_health * 100),
        },
        "portfolio_summary": _json_portfolio_summary(projects),
        "projects": [_json_project(p) for p in projects],
        "connections": [
            {
                "type": c.type,
                "detail": c.detail,
                "projects": c.projects,
                "severity": c.severity,
            }
            for c in conns
        ],
        "recommendations": [
            {
                "priority": r.priority,
                "category": r.category,
                "message": r.message,
                "projects": r.projects,
            }
            for r in recs
        ],
    }

    return json_mod.dumps(data, indent=2)


def _json_project(p: Project) -> dict:
    """Build a single project dict for JSON export."""
    d = p.to_dict()
    d["license"] = p.license
    return d


def _json_portfolio_summary(projects: list[Project]) -> dict:
    """Build portfolio-level aggregate stats for JSON export."""
    if not projects:
        return {}

    n = len(projects)

    # Languages
    lang_counter: Counter[str] = Counter()
    for p in projects:
        for lang in p.tech_stack.primary_languages:
            lang_counter[lang] += 1

    # Frameworks
    fw_counter: Counter[str] = Counter()
    for p in projects:
        for fw in p.tech_stack.frameworks:
            if fw != "Docker":
                fw_counter[fw] += 1

    # Infrastructure
    ci_systems = {"GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"}
    has_ci = sum(1 for p in projects if any(i in p.tech_stack.infrastructure for i in ci_systems))
    has_docker = sum(1 for p in projects if "Docker" in p.tech_stack.infrastructure)

    # Security
    has_security = sum(1 for p in projects if p.tech_stack.security_tools)

    # Quality
    has_quality = sum(1 for p in projects if p.tech_stack.quality_tools)

    # Testing
    tf_counter: Counter[str] = Counter()
    for p in projects:
        for tf in p.tech_stack.testing_frameworks:
            tf_counter[tf] += 1
    has_testing = sum(1 for p in projects if p.tech_stack.testing_frameworks)

    # Databases
    db_counter: Counter[str] = Counter()
    for p in projects:
        for db in p.tech_stack.databases:
            db_counter[db] += 1
    has_db = sum(1 for p in projects if p.tech_stack.databases)

    # Package managers
    pm_counter: Counter[str] = Counter()
    for p in projects:
        for pm in p.tech_stack.package_managers:
            pm_counter[pm] += 1
    has_pm = sum(1 for p in projects if p.tech_stack.package_managers)

    # AI/ML
    ai_counter: Counter[str] = Counter()
    for p in projects:
        for tool in p.tech_stack.ai_tools:
            ai_counter[tool] += 1
    has_ai = sum(1 for p in projects if p.tech_stack.ai_tools)

    # Documentation artifacts
    da_counter: Counter[str] = Counter()
    for p in projects:
        for da in p.tech_stack.docs_artifacts:
            da_counter[da] += 1
    has_docs = sum(1 for p in projects if p.tech_stack.docs_artifacts)

    # CI/CD configuration
    ci_counter: Counter[str] = Counter()
    for p in projects:
        for ci in p.tech_stack.ci_config:
            ci_counter[ci] += 1
    has_ci_config = sum(1 for p in projects if p.tech_stack.ci_config)

    # Runtime versions
    rv_counter: Counter[str] = Counter()
    for p in projects:
        for rt in p.tech_stack.runtime_versions:
            rv_counter[rt] += 1
    has_runtimes = sum(1 for p in projects if p.tech_stack.runtime_versions)

    # Licenses
    lic_counter: Counter[str] = Counter()
    for p in projects:
        if p.license:
            lic_counter[p.license] += 1
    has_license = sum(1 for p in projects if p.license)

    return {
        "total_projects": n,
        "languages": dict(lang_counter.most_common(10)),
        "frameworks": dict(fw_counter.most_common(10)),
        "infrastructure": {
            "ci_cd": f"{has_ci}/{n}",
            "docker": f"{has_docker}/{n}",
        },
        "security": f"{has_security}/{n}",
        "quality": f"{has_quality}/{n}",
        "testing": {"coverage": f"{has_testing}/{n}", "frameworks": dict(tf_counter.most_common(10))},
        "databases": {"coverage": f"{has_db}/{n}", "databases": dict(db_counter.most_common(10))},
        "package_managers": {"coverage": f"{has_pm}/{n}", "managers": dict(pm_counter.most_common(10))},
        "ai_ml": {"coverage": f"{has_ai}/{n}", "tools": dict(ai_counter.most_common(10))},
        "docs_artifacts": {"coverage": f"{has_docs}/{n}", "artifacts": dict(da_counter.most_common(10))},
        "ci_config": {"coverage": f"{has_ci_config}/{n}", "config": dict(ci_counter.most_common(10))},
        "runtime_versions": {"coverage": f"{has_runtimes}/{n}", "runtimes": dict(rv_counter.most_common(10))},
        "licenses": {"coverage": f"{has_license}/{n}", "licenses": dict(lic_counter.most_common(10))},
    }
