"""Rich markdown export — portfolio report generation."""
from __future__ import annotations

from collections import Counter

from atlas.connections import find_connections
from atlas.models import Portfolio, Project


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

    # AI/ML
    has_ai = sum(1 for p in projects if p.tech_stack.ai_tools)
    if has_ai:
        ai_counter: Counter[str] = Counter()
        for p in projects:
            for tool in p.tech_stack.ai_tools:
                ai_counter[tool] += 1
        top_ai = ai_counter.most_common(5)
        lines.append(f"**AI/ML**: {has_ai}/{n} projects · {', '.join(t for t, _ in top_ai)}")

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
