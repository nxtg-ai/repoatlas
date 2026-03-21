"""Portfolio report generation — markdown, JSON, and CSV formats."""
from __future__ import annotations

import csv
import io
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

    # Build tools
    has_build = sum(1 for p in projects if p.tech_stack.build_tools)
    if has_build:
        bt_counter: Counter[str] = Counter()
        for p in projects:
            for bt in p.tech_stack.build_tools:
                bt_counter[bt] += 1
        top_bt = bt_counter.most_common(6)
        lines.append(f"**Build Tools**: {has_build}/{n} projects · {', '.join(t for t, _ in top_bt)}")

    # API specs
    has_api = sum(1 for p in projects if p.tech_stack.api_specs)
    if has_api:
        api_counter: Counter[str] = Counter()
        for p in projects:
            for spec in p.tech_stack.api_specs:
                api_counter[spec] += 1
        top_api = api_counter.most_common(6)
        lines.append(f"**API Specs**: {has_api}/{n} projects · {', '.join(t for t, _ in top_api)}")


    # Monitoring & observability
    has_mon = sum(1 for p in projects if p.tech_stack.monitoring_tools)
    if has_mon:
        mon_counter: Counter[str] = Counter()
        for p in projects:
            for mt in p.tech_stack.monitoring_tools:
                mon_counter[mt] += 1
        top_mon = mon_counter.most_common(6)
        mon_names = ", ".join(t for t, _ in top_mon)
        lines.append(f"**Monitoring**: {has_mon}/{n} projects \u00b7 {mon_names}")

    # Auth tools
    has_auth = sum(1 for p in projects if p.tech_stack.auth_tools)
    if has_auth:
        auth_counter: Counter[str] = Counter()
        for p in projects:
            for at in p.tech_stack.auth_tools:
                auth_counter[at] += 1
        top_auth = auth_counter.most_common(6)
        auth_names = ", ".join(t for t, _ in top_auth)
        lines.append(f"**Auth**: {has_auth}/{n} projects \u00b7 {auth_names}")

    # Messaging tools
    has_msg = sum(1 for p in projects if p.tech_stack.messaging_tools)
    if has_msg:
        msg_counter: Counter[str] = Counter()
        for p in projects:
            for mt in p.tech_stack.messaging_tools:
                msg_counter[mt] += 1
        top_msg = msg_counter.most_common(6)
        msg_names = ", ".join(t for t, _ in top_msg)
        lines.append(f"**Messaging**: {has_msg}/{n} projects \u00b7 {msg_names}")

    # Deploy targets
    has_deploy = sum(1 for p in projects if p.tech_stack.deploy_targets)
    if has_deploy:
        dt_counter: Counter[str] = Counter()
        for p in projects:
            for dt in p.tech_stack.deploy_targets:
                dt_counter[dt] += 1
        top_dt = dt_counter.most_common(6)
        dt_names = ", ".join(t for t, _ in top_dt)
        lines.append(f"**Deploy Targets**: {has_deploy}/{n} projects \u00b7 {dt_names}")

    # State management
    has_sm = sum(1 for p in projects if p.tech_stack.state_management)
    if has_sm:
        sm_counter: Counter[str] = Counter()
        for p in projects:
            for sm in p.tech_stack.state_management:
                sm_counter[sm] += 1
        top_sm = sm_counter.most_common(6)
        sm_names = ", ".join(t for t, _ in top_sm)
        lines.append(f"**State Mgmt**: {has_sm}/{n} projects \u00b7 {sm_names}")

    # CSS frameworks
    has_css = sum(1 for p in projects if p.tech_stack.css_frameworks)
    if has_css:
        css_counter: Counter[str] = Counter()
        for p in projects:
            for css in p.tech_stack.css_frameworks:
                css_counter[css] += 1
        top_css = css_counter.most_common(6)
        css_names = ", ".join(t for t, _ in top_css)
        lines.append(f"**CSS/Style**: {has_css}/{n} projects \u00b7 {css_names}")

    # Bundlers
    has_bnd = sum(1 for p in projects if p.tech_stack.bundlers)
    if has_bnd:
        bnd_counter: Counter[str] = Counter()
        for p in projects:
            for bnd in p.tech_stack.bundlers:
                bnd_counter[bnd] += 1
        top_bnd = bnd_counter.most_common(6)
        bnd_names = ", ".join(t for t, _ in top_bnd)
        lines.append(f"**Bundlers**: {has_bnd}/{n} projects \u00b7 {bnd_names}")

    # ORM / DB Clients
    has_orm = sum(1 for p in projects if p.tech_stack.orm_tools)
    if has_orm:
        orm_counter: Counter[str] = Counter()
        for p in projects:
            for orm in p.tech_stack.orm_tools:
                orm_counter[orm] += 1
        top_orm = orm_counter.most_common(6)
        orm_names = ", ".join(t for t, _ in top_orm)
        lines.append(f"**ORM/DB Clients**: {has_orm}/{n} projects \u00b7 {orm_names}")

    # i18n
    has_i18n = sum(1 for p in projects if p.tech_stack.i18n_tools)
    if has_i18n:
        i18n_counter: Counter[str] = Counter()
        for p in projects:
            for i18n in p.tech_stack.i18n_tools:
                i18n_counter[i18n] += 1
        top_i18n = i18n_counter.most_common(6)
        i18n_names = ", ".join(t for t, _ in top_i18n)
        lines.append(f"**i18n**: {has_i18n}/{n} projects \u00b7 {i18n_names}")

    # Validation
    has_val = sum(1 for p in projects if p.tech_stack.validation_tools)
    if has_val:
        val_counter: Counter[str] = Counter()
        for p in projects:
            for val in p.tech_stack.validation_tools:
                val_counter[val] += 1
        top_val = val_counter.most_common(6)
        val_names = ", ".join(t for t, _ in top_val)
        lines.append(f"**Validation**: {has_val}/{n} projects \u00b7 {val_names}")

    # Logging
    has_log = sum(1 for p in projects if p.tech_stack.logging_tools)
    if has_log:
        log_counter: Counter[str] = Counter()
        for p in projects:
            for lt in p.tech_stack.logging_tools:
                log_counter[lt] += 1
        top_log = log_counter.most_common(6)
        log_names = ", ".join(t for t, _ in top_log)
        lines.append(f"**Logging**: {has_log}/{n} projects \u00b7 {log_names}")

    # Container orchestration
    has_co = sum(1 for p in projects if p.tech_stack.container_orchestration)
    if has_co:
        co_counter: Counter[str] = Counter()
        for p in projects:
            for co in p.tech_stack.container_orchestration:
                co_counter[co] += 1
        top_co = co_counter.most_common(6)
        co_names = ", ".join(t for t, _ in top_co)
        lines.append(f"**Containers**: {has_co}/{n} projects \u00b7 {co_names}")

    # Cloud providers
    has_cloud = sum(1 for p in projects if p.tech_stack.cloud_providers)
    if has_cloud:
        cloud_counter: Counter[str] = Counter()
        for p in projects:
            for cp in p.tech_stack.cloud_providers:
                cloud_counter[cp] += 1
        top_cloud = cloud_counter.most_common(6)
        cloud_names = ", ".join(t for t, _ in top_cloud)
        lines.append(f"**Cloud**: {has_cloud}/{n} projects \u00b7 {cloud_names}")

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
        if p.tech_stack.build_tools:
            lines.append(f"- **Build Tools**: {', '.join(p.tech_stack.build_tools[:8])}")
        if p.tech_stack.api_specs:
            lines.append(f"- **API Specs**: {', '.join(p.tech_stack.api_specs[:8])}")
        if p.tech_stack.monitoring_tools:
            lines.append(f"- **Monitoring**: {', '.join(p.tech_stack.monitoring_tools[:8])}")
        if p.tech_stack.auth_tools:
            lines.append(f"- **Auth**: {', '.join(p.tech_stack.auth_tools[:8])}")
        if p.tech_stack.messaging_tools:
            lines.append(f"- **Messaging**: {', '.join(p.tech_stack.messaging_tools[:8])}")
        if p.tech_stack.deploy_targets:
            lines.append(f"- **Deploy Targets**: {', '.join(p.tech_stack.deploy_targets[:8])}")
        if p.tech_stack.state_management:
            lines.append(f"- **State Mgmt**: {', '.join(p.tech_stack.state_management[:8])}")

        if p.tech_stack.css_frameworks:
            lines.append(f"- **CSS/Style**: {', '.join(p.tech_stack.css_frameworks[:8])}")

        if p.tech_stack.bundlers:
            lines.append(f"- **Bundlers**: {', '.join(p.tech_stack.bundlers[:8])}")

        if p.tech_stack.orm_tools:
            lines.append(f"- **ORM/DB Clients**: {', '.join(p.tech_stack.orm_tools[:8])}")

        if p.tech_stack.i18n_tools:
            lines.append(f"- **i18n**: {', '.join(p.tech_stack.i18n_tools[:8])}")

        if p.tech_stack.validation_tools:
            lines.append(f"- **Validation**: {', '.join(p.tech_stack.validation_tools[:8])}")

        if p.tech_stack.logging_tools:
            lines.append(f"- **Logging**: {', '.join(p.tech_stack.logging_tools[:8])}")

        if p.tech_stack.container_orchestration:
            lines.append(f"- **Containers**: {', '.join(p.tech_stack.container_orchestration[:8])}")

        if p.tech_stack.cloud_providers:
            lines.append(f"- **Cloud**: {', '.join(p.tech_stack.cloud_providers[:8])}")

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

    # Summary stats
    total = len(conns)
    sev_counts: dict[str, int] = {}
    for c in conns:
        sev_counts[c.severity] = sev_counts.get(c.severity, 0) + 1
    sev_parts = []
    for s in ("critical", "warning", "info"):
        if s in sev_counts:
            sev_parts.append(f"{sev_counts[s]} {s}")
    lines.append(f"**{total} connections**: {', '.join(sev_parts)}")
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
        "shared_runtime": "Shared Runtime Versions",
        "runtime_divergence": "Runtime Version Divergence",
        "runtime_gap": "Runtime Version Gaps",
        "shared_build_tool": "Shared Build Tools",
        "build_tool_divergence": "Build Tool Divergence",
        "build_tool_gap": "Build Tool Gaps",
        "shared_api_spec": "Shared API Specs",
        "api_spec_divergence": "API Spec Divergence",
        "api_spec_gap": "API Spec Gaps",
        "shared_monitoring": "Shared Monitoring Tools",
        "monitoring_divergence": "Monitoring Divergence",
        "monitoring_gap": "Monitoring Gaps",
        "shared_auth": "Shared Auth Tools",
        "auth_divergence": "Auth Divergence",
        "auth_gap": "Auth Gaps",
        "shared_messaging": "Shared Messaging Tools",
        "messaging_divergence": "Messaging Divergence",
        "messaging_gap": "Messaging Gaps",
        "shared_deploy": "Shared Deploy Targets",
        "deploy_divergence": "Deploy Target Divergence",
        "deploy_gap": "Deploy Target Gaps",
        "shared_state_mgmt": "Shared State Management",
        "state_mgmt_divergence": "State Management Divergence",
        "state_mgmt_gap": "State Management Gaps",
        "shared_css": "Shared CSS Frameworks",
        "css_divergence": "CSS Framework Divergence",
        "css_gap": "CSS Framework Gaps",
        "shared_bundler": "Shared Bundlers",
        "bundler_divergence": "Bundler Divergence",
        "bundler_gap": "Bundler Gaps",
        "shared_orm": "Shared ORM/DB Clients",
        "orm_divergence": "ORM Strategy Divergence",
        "orm_gap": "ORM/DB Client Gaps",
        "shared_i18n": "Shared i18n Tools",
        "i18n_divergence": "i18n Strategy Divergence",
        "i18n_gap": "i18n Gaps",
        "shared_validation": "Shared Validation Tools",
        "validation_divergence": "Validation Strategy Divergence",
        "validation_gap": "Validation Gaps",
        "shared_logging": "Shared Logging Tools",
        "logging_divergence": "Logging Strategy Divergence",
        "logging_gap": "Logging Gaps",
        "shared_container_orch": "Shared Container Orchestration",
        "container_orch_divergence": "Container Orchestration Divergence",
        "container_orch_gap": "Container Orchestration Gaps",
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
        "connection_summary": {
            "total": len(conns),
            "critical": sum(1 for c in conns if c.severity == "critical"),
            "warning": sum(1 for c in conns if c.severity == "warning"),
            "info": sum(1 for c in conns if c.severity == "info"),
        },
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

    # Build tools
    bt_counter: Counter[str] = Counter()
    for p in projects:
        for bt in p.tech_stack.build_tools:
            bt_counter[bt] += 1
    has_build = sum(1 for p in projects if p.tech_stack.build_tools)

    # API specs
    api_counter: Counter[str] = Counter()
    for p in projects:
        for spec in p.tech_stack.api_specs:
            api_counter[spec] += 1
    has_api = sum(1 for p in projects if p.tech_stack.api_specs)

    # Monitoring
    mon_counter: Counter[str] = Counter()
    for p in projects:
        for mt in p.tech_stack.monitoring_tools:
            mon_counter[mt] += 1
    has_mon = sum(1 for p in projects if p.tech_stack.monitoring_tools)

    # Auth tools
    auth_counter: Counter[str] = Counter()
    for p in projects:
        for at in p.tech_stack.auth_tools:
            auth_counter[at] += 1
    has_auth = sum(1 for p in projects if p.tech_stack.auth_tools)

    # Messaging tools
    msg_counter2: Counter[str] = Counter()
    for p in projects:
        for mt in p.tech_stack.messaging_tools:
            msg_counter2[mt] += 1
    has_msg = sum(1 for p in projects if p.tech_stack.messaging_tools)

    # Deploy targets
    dt_counter: Counter[str] = Counter()
    for p in projects:
        for dt in p.tech_stack.deploy_targets:
            dt_counter[dt] += 1
    has_deploy = sum(1 for p in projects if p.tech_stack.deploy_targets)

    # State management
    sm_counter: Counter[str] = Counter()
    for p in projects:
        for sm in p.tech_stack.state_management:
            sm_counter[sm] += 1
    has_sm = sum(1 for p in projects if p.tech_stack.state_management)

    # CSS frameworks
    css_counter: Counter[str] = Counter()
    for p in projects:
        for css in p.tech_stack.css_frameworks:
            css_counter[css] += 1
    has_css = sum(1 for p in projects if p.tech_stack.css_frameworks)

    # Bundlers
    bnd_counter2: Counter[str] = Counter()
    for p in projects:
        for bnd in p.tech_stack.bundlers:
            bnd_counter2[bnd] += 1
    has_bnd = sum(1 for p in projects if p.tech_stack.bundlers)

    # ORM / DB Clients
    orm_counter2: Counter[str] = Counter()
    for p in projects:
        for orm in p.tech_stack.orm_tools:
            orm_counter2[orm] += 1
    has_orm = sum(1 for p in projects if p.tech_stack.orm_tools)

    # i18n
    i18n_counter2: Counter[str] = Counter()
    for p in projects:
        for i18n in p.tech_stack.i18n_tools:
            i18n_counter2[i18n] += 1
    has_i18n = sum(1 for p in projects if p.tech_stack.i18n_tools)

    # Validation
    val_counter2: Counter[str] = Counter()
    for p in projects:
        for val in p.tech_stack.validation_tools:
            val_counter2[val] += 1
    has_val = sum(1 for p in projects if p.tech_stack.validation_tools)

    # Logging
    log_counter2: Counter[str] = Counter()
    for p in projects:
        for lt in p.tech_stack.logging_tools:
            log_counter2[lt] += 1
    has_log = sum(1 for p in projects if p.tech_stack.logging_tools)

    # Container orchestration
    co_counter2: Counter[str] = Counter()
    for p in projects:
        for co in p.tech_stack.container_orchestration:
            co_counter2[co] += 1
    has_co = sum(1 for p in projects if p.tech_stack.container_orchestration)

    # Cloud providers
    cloud_counter2: Counter[str] = Counter()
    for p in projects:
        for cp in p.tech_stack.cloud_providers:
            cloud_counter2[cp] += 1
    has_cloud = sum(1 for p in projects if p.tech_stack.cloud_providers)

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
        "build_tools": {"coverage": f"{has_build}/{n}", "tools": dict(bt_counter.most_common(10))},
        "api_specs": {"coverage": f"{has_api}/{n}", "specs": dict(api_counter.most_common(10))},
        "monitoring": {"coverage": f"{has_mon}/{n}", "tools": dict(mon_counter.most_common(10))},
        "auth": {"coverage": f"{has_auth}/{n}", "tools": dict(auth_counter.most_common(10))},
        "messaging": {"coverage": f"{has_msg}/{n}", "tools": dict(msg_counter2.most_common(10))},
        "deploy_targets": {"coverage": f"{has_deploy}/{n}", "targets": dict(dt_counter.most_common(10))},
        "state_management": {"coverage": f"{has_sm}/{n}", "tools": dict(sm_counter.most_common(10))},
        "css_frameworks": {"coverage": f"{has_css}/{n}", "frameworks": dict(css_counter.most_common(10))},
        "bundlers": {"coverage": f"{has_bnd}/{n}", "tools": dict(bnd_counter2.most_common(10))},
        "orm_tools": {"coverage": f"{has_orm}/{n}", "tools": dict(orm_counter2.most_common(10))},
        "i18n_tools": {"coverage": f"{has_i18n}/{n}", "tools": dict(i18n_counter2.most_common(10))},
        "validation_tools": {"coverage": f"{has_val}/{n}", "tools": dict(val_counter2.most_common(10))},
        "logging_tools": {"coverage": f"{has_log}/{n}", "tools": dict(log_counter2.most_common(10))},
        "container_orchestration": {"coverage": f"{has_co}/{n}", "tools": dict(co_counter2.most_common(10))},
        "cloud_providers": {"coverage": f"{has_cloud}/{n}", "providers": dict(cloud_counter2.most_common(10))},
        "licenses": {"coverage": f"{has_license}/{n}", "licenses": dict(lic_counter.most_common(10))},
    }


def build_csv_report(portfolio: Portfolio) -> str:
    """Build a CSV portfolio report — one row per project."""
    buf = io.StringIO()
    writer = csv.writer(buf)

    headers = [
        "Name", "Path", "Health %", "Grade",
        "Tests", "Git", "Docs", "Structure",
        "Source Files", "Test Files", "Total Files", "LOC",
        "Languages", "Frameworks", "Databases",
        "Infrastructure", "Security Tools", "Quality Tools",
        "Testing Frameworks", "Package Managers", "AI/ML Tools",
        "Docs Artifacts", "CI Config", "Runtime Versions", "Build Tools", "API Specs",
        "Monitoring Tools", "Auth Tools", "Messaging Tools", "Deploy Targets", "State Management",
        "CSS Frameworks", "Bundlers", "ORM/DB Clients", "i18n", "Validation", "Logging",
        "Container Orchestration", "Cloud Providers",
        "License", "Branch", "Last Commit", "Commits",
    ]
    writer.writerow(headers)

    for p in portfolio.projects:
        ts = p.tech_stack
        h = p.health
        gi = p.git_info
        writer.writerow([
            p.name,
            p.path,
            h.percent,
            h.grade,
            round(h.tests * 100),
            round(h.git_hygiene * 100),
            round(h.documentation * 100),
            round(h.structure * 100),
            p.source_file_count,
            p.test_file_count,
            p.total_file_count,
            p.loc,
            "; ".join(ts.primary_languages),
            "; ".join(ts.frameworks),
            "; ".join(ts.databases),
            "; ".join(ts.infrastructure),
            "; ".join(ts.security_tools),
            "; ".join(ts.quality_tools),
            "; ".join(ts.testing_frameworks),
            "; ".join(ts.package_managers),
            "; ".join(ts.ai_tools),
            "; ".join(ts.docs_artifacts),
            "; ".join(ts.ci_config),
            "; ".join(f"{k}={v}" for k, v in ts.runtime_versions.items()),
            "; ".join(ts.build_tools),
            "; ".join(ts.api_specs),
            "; ".join(ts.monitoring_tools),
            "; ".join(ts.auth_tools),
            "; ".join(ts.messaging_tools),
            "; ".join(ts.deploy_targets),
            "; ".join(ts.state_management),
            "; ".join(ts.css_frameworks),
            "; ".join(ts.bundlers),
            "; ".join(ts.orm_tools),
            "; ".join(ts.i18n_tools),
            "; ".join(ts.validation_tools),
            "; ".join(ts.logging_tools),
            "; ".join(ts.container_orchestration),
            "; ".join(ts.cloud_providers),
            p.license,
            gi.branch if gi else "",
            gi.last_commit_date if gi else "",
            gi.total_commits if gi else 0,
        ])

    return buf.getvalue()
