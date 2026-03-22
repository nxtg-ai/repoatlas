"""Rich terminal display — the visual wow factor."""
from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from atlas.models import Connection, Portfolio, Project

console = Console()

SPARK_CHARS = " \u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"


def sparkline(values: list[float], width: int = 7) -> str:
    """Render a list of floats (0.0–1.0) as a Unicode sparkline string."""
    if not values:
        return ""
    # Clamp values to [0, 1]
    clamped = [max(0.0, min(1.0, v)) for v in values]
    # Take the most recent `width` values
    recent = clamped[-width:]
    return "".join(SPARK_CHARS[int(v * (len(SPARK_CHARS) - 1))] for v in recent)

HEALTH_COLORS = {
    "A": "bold green",
    "B+": "green",
    "B": "cyan",
    "C": "yellow",
    "D": "red",
    "F": "bold red",
}

SEVERITY_ICONS = {
    "info": "[cyan]\u2139[/cyan]",
    "warning": "[yellow]\u26a0[/yellow]",
    "critical": "[red]\u2716[/red]",
}

CONNECTION_ICONS = {
    "shared_dep": "[cyan]\u2500[/cyan]",
    "shared_framework": "[blue]\u25cf[/blue]",
    "version_mismatch": "[yellow]\u26a0[/yellow]",
    "health_gap": "[red]\u2716[/red]",
    "reuse_candidate": "[green]\u21bb[/green]",
    "shared_database": "[magenta]\u25c6[/magenta]",
    "database_divergence": "[yellow]\u25c7[/yellow]",
    "database_gap": "[red]\u25c8[/red]",
    "shared_infra": "[cyan]\u2b21[/cyan]",
    "infra_divergence": "[yellow]\u26a1[/yellow]",
    "infra_gap": "[red]\u25cb[/red]",
    "shared_security": "[green]\u2611[/green]",
    "security_divergence": "[yellow]\u2610[/yellow]",
    "security_gap": "[red]\u2612[/red]",
    "shared_quality": "[green]\u2714[/green]",
    "quality_divergence": "[yellow]\u2702[/yellow]",
    "quality_gap": "[red]\u2718[/red]",
    "shared_ai": "[magenta]\u2b50[/magenta]",
    "ai_divergence": "[yellow]\u2b53[/yellow]",
    "ai_gap": "[red]\u2b54[/red]",
    "shared_testing": "[green]\u2713[/green]",
    "testing_divergence": "[yellow]\u2263[/yellow]",
    "testing_gap": "[red]\u2717[/red]",
    "shared_pkg_manager": "[cyan]\u2696[/cyan]",
    "pkg_manager_divergence": "[yellow]\u2694[/yellow]",
    "shared_license": "[green]\u00a9[/green]",
    "license_divergence": "[yellow]\u00a7[/yellow]",
    "license_gap": "[red]\u2205[/red]",
    "shared_docs": "[green]\u2261[/green]",
    "docs_divergence": "[yellow]\u2260[/yellow]",
    "docs_gap": "[red]\u2717[/red]",
    "shared_ci_config": "[cyan]\u2699[/cyan]",
    "ci_config_divergence": "[yellow]\u21c4[/yellow]",
    "ci_config_gap": "[red]\u25cb[/red]",
    "shared_runtime": "[green]\u25b6[/green]",
    "runtime_divergence": "[yellow]\u21c5[/yellow]",
    "runtime_gap": "[red]\u25a1[/red]",
    "shared_build_tool": "[green]\u2692[/green]",
    "build_tool_divergence": "[yellow]\u21cb[/yellow]",
    "build_tool_gap": "[red]\u25a0[/red]",
    "shared_api_spec": "[cyan]\u2194[/cyan]",
    "api_spec_divergence": "[yellow]\u21ae[/yellow]",
    "api_spec_gap": "[red]\u2298[/red]",
    "shared_monitoring": "[green]\u2302[/green]",
    "monitoring_divergence": "[yellow]\u2300[/yellow]",
    "monitoring_gap": "[red]\u2301[/red]",
    "shared_auth": "[green]\u2302[/green]",
    "auth_divergence": "[yellow]\u2300[/yellow]",
    "auth_gap": "[red]\u2301[/red]",
    "shared_messaging": "[green]\u2302[/green]",
    "messaging_divergence": "[yellow]\u2300[/yellow]",
    "messaging_gap": "[red]\u2301[/red]",
    "shared_deploy": "[green]\u2601[/green]",
    "deploy_divergence": "[yellow]\u2601[/yellow]",
    "deploy_gap": "[red]\u2601[/red]",
    "shared_state_mgmt": "[green]\u26a1[/green]",
    "state_mgmt_divergence": "[yellow]\u26a1[/yellow]",
    "state_mgmt_gap": "[red]\u26a1[/red]",
    "shared_css": "[green]\u2744[/green]",
    "css_divergence": "[yellow]\u2744[/yellow]",
    "css_gap": "[red]\u2744[/red]",
    "shared_bundler": "[green]\u2692[/green]",
    "bundler_divergence": "[yellow]\u2692[/yellow]",
    "bundler_gap": "[red]\u2692[/red]",
    "shared_orm": "[green]\u2261[/green]",
    "orm_divergence": "[yellow]\u2261[/yellow]",
    "orm_gap": "[red]\u2261[/red]",
    "shared_i18n": "[green]\u2302[/green]",
    "i18n_divergence": "[yellow]\u2302[/yellow]",
    "i18n_gap": "[red]\u2302[/red]",
    "shared_validation": "[green]\u2713[/green]",
    "validation_divergence": "[yellow]\u2713[/yellow]",
    "validation_gap": "[red]\u2713[/red]",
    "shared_logging": "[green]\u2261[/green]",
    "logging_divergence": "[yellow]\u2261[/yellow]",
    "logging_gap": "[red]\u2261[/red]",
    "shared_container_orch": "[green]\u2699[/green]",
    "container_orch_divergence": "[yellow]\u2699[/yellow]",
    "container_orch_gap": "[red]\u2699[/red]",
    "shared_cloud": "[green]\u2601[/green]",
    "cloud_divergence": "[yellow]\u2601[/yellow]",
    "cloud_gap": "[red]\u2601[/red]",
    "shared_task_queue": "[green]\u23f1[/green]",
    "task_queue_divergence": "[yellow]\u23f1[/yellow]",
    "task_queue_gap": "[red]\u23f1[/red]",
    "shared_search": "[green]\U0001f50d[/green]",
    "search_divergence": "[yellow]\U0001f50d[/yellow]",
    "search_gap": "[red]\U0001f50d[/red]",
    "shared_feature_flag": "[green]\u2691[/green]",
    "feature_flag_divergence": "[yellow]\u2691[/yellow]",
    "feature_flag_gap": "[red]\u2691[/red]",
    "shared_http_client": "[green]\u21c4[/green]",
    "http_client_divergence": "[yellow]\u21c4[/yellow]",
    "http_client_gap": "[red]\u21c4[/red]",
    "shared_doc_generator": "[green]\u2261[/green]",
    "doc_generator_divergence": "[yellow]\u2261[/yellow]",
    "doc_generator_gap": "[red]\u2261[/red]",
    "shared_cli_framework": "[green]\u2318[/green]",
    "cli_framework_divergence": "[yellow]\u2318[/yellow]",
    "shared_config_tool": "[green]\u2699[/green]",
    "config_tool_divergence": "[yellow]\u2699[/yellow]",
    "config_tool_gap": "[red]\u2699[/red]",
    "shared_caching_tool": "[green]\u29bf[/green]",
    "caching_divergence": "[yellow]\u29bf[/yellow]",
    "caching_gap": "[red]\u29bf[/red]",
    "shared_template_engine": "[green]\u2756[/green]",
    "template_engine_divergence": "[yellow]\u2756[/yellow]",
    "shared_serialization_format": "[green]\u2b12[/green]",
    "serialization_divergence": "[yellow]\u2b12[/yellow]",
    "shared_di_framework": "[green]\u2b19[/green]",
    "di_divergence": "[yellow]\u2b19[/yellow]",
    "shared_websocket_lib": "[green]⇌[/green]",
    "websocket_divergence": "[yellow]⇌[/yellow]",
    "shared_graphql_lib": "[green]⇔[/green]",
    "graphql_divergence": "[yellow]⇔[/yellow]",
    "shared_event_streaming": "[green]⇆[/green]",
    "event_streaming_divergence": "[yellow]⇆[/yellow]",
    "shared_payment_tool": "[green]⇄[/green]",
    "payment_divergence": "[yellow]⇄[/yellow]",
    "shared_date_lib": "[green]⟳[/green]",
    "date_lib_divergence": "[yellow]⟳[/yellow]",
    "shared_image_lib": "[green]⬡[/green]",
    "image_lib_divergence": "[yellow]⬡[/yellow]",
    "shared_data_viz": "[green]◆[/green]",
    "data_viz_divergence": "[yellow]◆[/yellow]",
}


def show_status(portfolio: Portfolio, history: list | None = None):
    """Display the full portfolio dashboard."""
    # Build per-project sparkline data from history
    project_sparklines: dict[str, str] = {}
    if history and len(history) >= 2:
        # Collect health values for each project across entries
        project_health_series: dict[str, list[float]] = {}
        for entry in history:
            for snap in entry.projects:
                project_health_series.setdefault(snap.name, []).append(snap.health)
        for name, values in project_health_series.items():
            if len(values) >= 2:
                project_sparklines[name] = sparkline(values)

    # Header panel
    total_tests = portfolio.total_tests
    total_loc = portfolio.total_loc
    avg_grade = portfolio.avg_grade
    avg_pct = int(portfolio.avg_health * 100)

    grade_color = HEALTH_COLORS.get(avg_grade, "white")

    header_text = Text()
    header_text.append("Portfolio: ", style="dim")
    header_text.append(portfolio.name, style="bold white")
    header_text.append("   |   ", style="dim")
    header_text.append(f"{len(portfolio.projects)}", style="bold cyan")
    header_text.append(" Projects", style="dim")
    header_text.append("   |   ", style="dim")
    header_text.append(f"{total_tests:,}", style="bold cyan")
    header_text.append(" Test Files", style="dim")
    header_text.append("   |   ", style="dim")
    header_text.append(f"{total_loc:,}", style="bold cyan")
    header_text.append(" LOC", style="dim")
    header_text.append("   |   ", style="dim")
    header_text.append("Health: ", style="dim")
    header_text.append(f"{avg_grade} ({avg_pct}%)", style=grade_color)

    if portfolio.last_scan:
        header_text.append("   |   ", style="dim")
        header_text.append("Scanned: ", style="dim")
        header_text.append(portfolio.last_scan[:19], style="dim italic")

    console.print()
    console.print(Panel(
        header_text,
        title="[bold white] ATLAS Portfolio Dashboard [/bold white]",
        border_style="cyan",
        padding=(1, 2),
    ))

    # Project table
    table = Table(
        box=box.ROUNDED,
        border_style="dim",
        header_style="bold cyan",
        show_lines=False,
        pad_edge=True,
        expand=True,
    )
    table.add_column("", width=2, justify="center")
    table.add_column("Project", style="bold white", min_width=18)
    table.add_column("Health", justify="center", min_width=9)
    table.add_column("Tests", justify="right", min_width=7)
    table.add_column("LOC", justify="right", min_width=8)
    table.add_column("Tech Stack", min_width=25)
    if project_sparklines:
        table.add_column("Trend", justify="center", min_width=9)
    table.add_column("Branch", style="dim", min_width=8)
    table.add_column("Commits", justify="right", style="dim", min_width=7)

    sorted_projects = sorted(
        portfolio.projects,
        key=lambda p: p.health.overall,
        reverse=True,
    )

    for proj in sorted_projects:
        grade = proj.health.grade
        pct = proj.health.percent
        color = HEALTH_COLORS.get(grade, "white")

        icon = _health_icon(proj.health.overall)
        health_str = f"[{color}]{grade} {pct}%[/{color}]"
        tests_str = f"{proj.test_file_count:,}" if proj.test_file_count > 0 else "[dim]0[/dim]"
        loc_str = f"{proj.loc:,}" if proj.loc > 0 else "[dim]0[/dim]"
        tech = proj.tech_stack.summary
        branch = proj.git_info.branch[:12] if proj.git_info.branch else "[dim]-[/dim]"
        commits = str(proj.git_info.total_commits) if proj.git_info.total_commits > 0 else "[dim]-[/dim]"

        if project_sparklines:
            spark = project_sparklines.get(proj.name, "")
            trend_str = f"[dim]{spark}[/dim]" if spark else "[dim]-[/dim]"
            table.add_row(icon, proj.name, health_str, tests_str, loc_str, tech, trend_str, branch, commits)
        else:
            table.add_row(icon, proj.name, health_str, tests_str, loc_str, tech, branch, commits)

    console.print(table)

    # Portfolio summary panel (if 2+ projects)
    if len(portfolio.projects) >= 2:
        _show_portfolio_summary(portfolio)


def _show_portfolio_summary(portfolio: Portfolio):
    """Show aggregate portfolio insights below the project table."""
    from collections import Counter

    projects = portfolio.projects
    lines: list[str] = []

    # Language distribution
    lang_counter: Counter[str] = Counter()
    for p in projects:
        for lang in p.tech_stack.primary_languages:
            lang_counter[lang] += 1
    if lang_counter:
        top_langs = lang_counter.most_common(6)
        lang_parts = [f"{lang} ({count})" for lang, count in top_langs]
        lines.append(f"  [bold]Languages:[/bold]    {', '.join(lang_parts)}")

    # Framework adoption
    fw_counter: Counter[str] = Counter()
    for p in projects:
        for fw in p.tech_stack.frameworks:
            if fw != "Docker":
                fw_counter[fw] += 1
    if fw_counter:
        top_fws = fw_counter.most_common(6)
        fw_parts = [f"{fw} ({count})" for fw, count in top_fws]
        lines.append(f"  [bold]Frameworks:[/bold]   {', '.join(fw_parts)}")

    # Infrastructure coverage
    n = len(projects)
    has_ci = sum(1 for p in projects if any(
        i in p.tech_stack.infrastructure
        for i in ("GitHub Actions", "GitLab CI", "Jenkins", "CircleCI")
    ))
    has_docker = sum(1 for p in projects if "Docker" in p.tech_stack.infrastructure)
    has_cloud = sum(1 for p in projects if any(
        i in p.tech_stack.infrastructure for i in ("AWS", "GCP", "Azure")
    ))
    infra_parts = []
    infra_parts.append(f"CI/CD {has_ci}/{n}")
    infra_parts.append(f"Docker {has_docker}/{n}")
    if has_cloud:
        infra_parts.append(f"Cloud {has_cloud}/{n}")
    lines.append(f"  [bold]Infra:[/bold]        {' · '.join(infra_parts)}")

    # Security posture
    has_any_security = sum(1 for p in projects if p.tech_stack.security_tools)
    has_dep_scanning = sum(1 for p in projects if any(
        t in p.tech_stack.security_tools
        for t in ("Dependabot", "Renovate", "Snyk")
    ))
    has_secret_scan = sum(1 for p in projects if any(
        t in p.tech_stack.security_tools
        for t in ("Gitleaks", "detect-secrets", "SOPS")
    ))
    sec_parts = []
    sec_parts.append(f"Any tooling {has_any_security}/{n}")
    if has_dep_scanning:
        sec_parts.append(f"Dep scanning {has_dep_scanning}/{n}")
    if has_secret_scan:
        sec_parts.append(f"Secret scanning {has_secret_scan}/{n}")
    lines.append(f"  [bold]Security:[/bold]     {' · '.join(sec_parts)}")

    # Code quality tooling
    has_quality = sum(1 for p in projects if p.tech_stack.quality_tools)
    if has_quality:
        has_linter = sum(1 for p in projects if any(
            t in p.tech_stack.quality_tools
            for t in ("Ruff", "Flake8", "Pylint", "ESLint", "Biome", "golangci-lint", "Clippy")
        ))
        has_formatter = sum(1 for p in projects if any(
            t in p.tech_stack.quality_tools
            for t in ("Black", "Prettier", "Biome", "autopep8", "isort")
        ))
        has_types = sum(1 for p in projects if any(
            t in p.tech_stack.quality_tools
            for t in ("mypy", "Pyright", "TypeScript")
        ))
        qt_parts = [f"Any tooling {has_quality}/{n}"]
        if has_linter:
            qt_parts.append(f"Linting {has_linter}/{n}")
        if has_formatter:
            qt_parts.append(f"Formatting {has_formatter}/{n}")
        if has_types:
            qt_parts.append(f"Type checking {has_types}/{n}")
        lines.append(f"  [bold]Quality:[/bold]      {' · '.join(qt_parts)}")

    # Testing framework adoption
    has_testing = sum(1 for p in projects if p.tech_stack.testing_frameworks)
    if has_testing:
        tf_counter: Counter[str] = Counter()
        for p in projects:
            for tf in p.tech_stack.testing_frameworks:
                tf_counter[tf] += 1
        top_tf = tf_counter.most_common(6)
        tf_parts = [f"{tf} ({count})" for tf, count in top_tf]
        lines.append(f"  [bold]Testing:[/bold]      {has_testing}/{n} projects · {', '.join(tf_parts)}")

    # Database adoption
    has_db = sum(1 for p in projects if p.tech_stack.databases)
    if has_db:
        db_counter: Counter[str] = Counter()
        for p in projects:
            for db in p.tech_stack.databases:
                db_counter[db] += 1
        top_db = db_counter.most_common(6)
        db_parts = [f"{db} ({count})" for db, count in top_db]
        lines.append(f"  [bold]Databases:[/bold]    {has_db}/{n} projects · {', '.join(db_parts)}")

    # Package manager adoption
    has_pm = sum(1 for p in projects if p.tech_stack.package_managers)
    if has_pm:
        pm_counter: Counter[str] = Counter()
        for p in projects:
            for pm in p.tech_stack.package_managers:
                pm_counter[pm] += 1
        top_pm = pm_counter.most_common(6)
        pm_parts = [f"{pm} ({count})" for pm, count in top_pm]
        lines.append(f"  [bold]Pkg Mgrs:[/bold]     {has_pm}/{n} projects · {', '.join(pm_parts)}")

    # AI/ML adoption
    has_ai = sum(1 for p in projects if p.tech_stack.ai_tools)
    if has_ai:
        ai_counter: Counter[str] = Counter()
        for p in projects:
            for tool in p.tech_stack.ai_tools:
                ai_counter[tool] += 1
        top_ai = ai_counter.most_common(4)
        ai_parts = [f"{tool} ({count})" for tool, count in top_ai]
        lines.append(f"  [bold]AI/ML:[/bold]        {has_ai}/{n} projects · {', '.join(ai_parts)}")

    # Documentation artifacts
    has_docs = sum(1 for p in projects if p.tech_stack.docs_artifacts)
    if has_docs:
        da_counter: Counter[str] = Counter()
        for p in projects:
            for da in p.tech_stack.docs_artifacts:
                da_counter[da] += 1
        top_da = da_counter.most_common(6)
        da_parts = [f"{da} ({count})" for da, count in top_da]
        lines.append(f"  [bold]Docs:[/bold]         {has_docs}/{n} projects · {', '.join(da_parts)}")

    # CI/CD configuration
    has_ci_config = sum(1 for p in projects if p.tech_stack.ci_config)
    if has_ci_config:
        ci_counter: Counter[str] = Counter()
        for p in projects:
            for ci in p.tech_stack.ci_config:
                ci_counter[ci] += 1
        top_ci = ci_counter.most_common(6)
        ci_parts = [f"{ci} ({count})" for ci, count in top_ci]
        lines.append(f"  [bold]CI Config:[/bold]    {has_ci_config}/{n} projects · {', '.join(ci_parts)}")

    # Runtime versions
    has_runtimes = sum(1 for p in projects if p.tech_stack.runtime_versions)
    if has_runtimes:
        rv_counter: Counter[str] = Counter()
        for p in projects:
            for rt in p.tech_stack.runtime_versions:
                rv_counter[rt] += 1
        top_rv = rv_counter.most_common(6)
        rv_parts = [f"{rt} ({count})" for rt, count in top_rv]
        lines.append(f"  [bold]Runtimes:[/bold]     {has_runtimes}/{n} projects · {', '.join(rv_parts)}")

    # Build tools
    has_build = sum(1 for p in projects if p.tech_stack.build_tools)
    if has_build:
        bt_counter: Counter[str] = Counter()
        for p in projects:
            for bt in p.tech_stack.build_tools:
                bt_counter[bt] += 1
        top_bt = bt_counter.most_common(6)
        bt_parts = [f"{bt} ({count})" for bt, count in top_bt]
        lines.append(f"  [bold]Build Tools:[/bold]  {has_build}/{n} projects \u00b7 {', '.join(bt_parts)}")

    # Monitoring & observability
    has_mon = sum(1 for p in projects if p.tech_stack.monitoring_tools)
    if has_mon:
        mon_counter: Counter[str] = Counter()
        for p in projects:
            for mt in p.tech_stack.monitoring_tools:
                mon_counter[mt] += 1
        top_mon = mon_counter.most_common(6)
        mon_parts = [f"{mt} ({count})" for mt, count in top_mon]
        lines.append(f"  [bold]Monitoring:[/bold]   {has_mon}/{n} projects \u00b7 {', '.join(mon_parts)}")

    # Auth tools
    has_auth = sum(1 for p in projects if p.tech_stack.auth_tools)
    if has_auth:
        auth_counter: Counter[str] = Counter()
        for p in projects:
            for at in p.tech_stack.auth_tools:
                auth_counter[at] += 1
        top_auth = auth_counter.most_common(6)
        auth_parts = [f"{at} ({count})" for at, count in top_auth]
        lines.append(f"  [bold]Auth:[/bold]         {has_auth}/{n} projects \u00b7 {', '.join(auth_parts)}")

    # Messaging tools
    has_msg = sum(1 for p in projects if p.tech_stack.messaging_tools)
    if has_msg:
        msg_counter: Counter[str] = Counter()
        for p in projects:
            for mt in p.tech_stack.messaging_tools:
                msg_counter[mt] += 1
        top_msg = msg_counter.most_common(6)
        msg_parts = [f"{mt} ({count})" for mt, count in top_msg]
        lines.append(f"  [bold]Messaging:[/bold]    {has_msg}/{n} projects \u00b7 {', '.join(msg_parts)}")

    # Deploy targets
    has_deploy = sum(1 for p in projects if p.tech_stack.deploy_targets)
    if has_deploy:
        dt_counter: Counter[str] = Counter()
        for p in projects:
            for dt in p.tech_stack.deploy_targets:
                dt_counter[dt] += 1
        top_dt = dt_counter.most_common(6)
        dt_parts = [f"{dt} ({count})" for dt, count in top_dt]
        lines.append(f"  [bold]Deploy:[/bold]       {has_deploy}/{n} projects \u00b7 {', '.join(dt_parts)}")

    # State management
    has_sm = sum(1 for p in projects if p.tech_stack.state_management)
    if has_sm:
        sm_counter: Counter[str] = Counter()
        for p in projects:
            for sm in p.tech_stack.state_management:
                sm_counter[sm] += 1
        top_sm = sm_counter.most_common(6)
        sm_parts = [f"{sm} ({count})" for sm, count in top_sm]
        lines.append(f"  [bold]State Mgmt:[/bold]   {has_sm}/{n} projects \u00b7 {', '.join(sm_parts)}")

    has_css = sum(1 for p in projects if p.tech_stack.css_frameworks)
    if has_css:
        css_counter: Counter[str] = Counter()
        for p in projects:
            for css in p.tech_stack.css_frameworks:
                css_counter[css] += 1
        top_css = css_counter.most_common(6)
        css_parts = [f"{css} ({count})" for css, count in top_css]
        lines.append(f"  [bold]CSS/Style:[/bold]   {has_css}/{n} projects \u00b7 {', '.join(css_parts)}")

    has_bnd = sum(1 for p in projects if p.tech_stack.bundlers)
    if has_bnd:
        bnd_counter: Counter[str] = Counter()
        for p in projects:
            for bnd in p.tech_stack.bundlers:
                bnd_counter[bnd] += 1
        top_bnd = bnd_counter.most_common(6)
        bnd_parts = [f"{bnd} ({count})" for bnd, count in top_bnd]
        lines.append(f"  [bold]Bundlers:[/bold]    {has_bnd}/{n} projects \u00b7 {', '.join(bnd_parts)}")

    has_orm = sum(1 for p in projects if p.tech_stack.orm_tools)
    if has_orm:
        orm_counter: Counter[str] = Counter()
        for p in projects:
            for orm in p.tech_stack.orm_tools:
                orm_counter[orm] += 1
        top_orm = orm_counter.most_common(6)
        orm_parts = [f"{orm} ({count})" for orm, count in top_orm]
        lines.append(f"  [bold]ORM/DB Clients:[/bold] {has_orm}/{n} projects \u00b7 {', '.join(orm_parts)}")

    has_i18n = sum(1 for p in projects if p.tech_stack.i18n_tools)
    if has_i18n:
        i18n_counter: Counter[str] = Counter()
        for p in projects:
            for i18n in p.tech_stack.i18n_tools:
                i18n_counter[i18n] += 1
        top_i18n = i18n_counter.most_common(6)
        i18n_parts = [f"{i18n} ({count})" for i18n, count in top_i18n]
        lines.append(f"  [bold]i18n:[/bold]        {has_i18n}/{n} projects \u00b7 {', '.join(i18n_parts)}")

    has_val = sum(1 for p in projects if p.tech_stack.validation_tools)
    if has_val:
        val_counter: Counter[str] = Counter()
        for p in projects:
            for val in p.tech_stack.validation_tools:
                val_counter[val] += 1
        top_val = val_counter.most_common(6)
        val_parts = [f"{val} ({count})" for val, count in top_val]
        lines.append(f"  [bold]Validation:[/bold]  {has_val}/{n} projects \u00b7 {', '.join(val_parts)}")

    # Logging
    has_log = sum(1 for p in projects if p.tech_stack.logging_tools)
    if has_log:
        log_counter: Counter[str] = Counter()
        for p in projects:
            for lt in p.tech_stack.logging_tools:
                log_counter[lt] += 1
        top_log = log_counter.most_common(6)
        log_parts = [f"{lt} ({count})" for lt, count in top_log]
        lines.append(f"  [bold]Logging:[/bold]     {has_log}/{n} projects \u00b7 {', '.join(log_parts)}")

    # Container orchestration
    has_co = sum(1 for p in projects if p.tech_stack.container_orchestration)
    if has_co:
        co_counter: Counter[str] = Counter()
        for p in projects:
            for co in p.tech_stack.container_orchestration:
                co_counter[co] += 1
        top_co = co_counter.most_common(6)
        co_parts = [f"{co} ({count})" for co, count in top_co]
        lines.append(f"  [bold]Containers:[/bold]  {has_co}/{n} projects \u00b7 {', '.join(co_parts)}")

    # Cloud providers
    has_cloud = sum(1 for p in projects if p.tech_stack.cloud_providers)
    if has_cloud:
        cloud_counter: Counter[str] = Counter()
        for p in projects:
            for cp in p.tech_stack.cloud_providers:
                cloud_counter[cp] += 1
        top_cloud = cloud_counter.most_common(6)
        cloud_parts = [f"{cp} ({count})" for cp, count in top_cloud]
        lines.append(f"  [bold]Cloud:[/bold]      {has_cloud}/{n} projects \u00b7 {', '.join(cloud_parts)}")

    # Task queues
    has_tq = sum(1 for p in projects if p.tech_stack.task_queues)
    if has_tq:
        tq_counter: Counter[str] = Counter()
        for p in projects:
            for tq in p.tech_stack.task_queues:
                tq_counter[tq] += 1
        top_tq = tq_counter.most_common(6)
        tq_parts = [f"{tq} ({count})" for tq, count in top_tq]
        lines.append(f"  [bold]Task Queues:[/bold] {has_tq}/{n} projects \u00b7 {', '.join(tq_parts)}")

    # Search engines
    has_se = sum(1 for p in projects if p.tech_stack.search_engines)
    if has_se:
        se_counter: Counter[str] = Counter()
        for p in projects:
            for se in p.tech_stack.search_engines:
                se_counter[se] += 1
        top_se = se_counter.most_common(6)
        se_parts = [f"{se} ({count})" for se, count in top_se]
        lines.append(f"  [bold]Search:[/bold]      {has_se}/{n} projects \u00b7 {', '.join(se_parts)}")

    # Feature flags
    has_ff = sum(1 for p in projects if p.tech_stack.feature_flags)
    if has_ff:
        ff_counter: Counter[str] = Counter()
        for p in projects:
            for ff in p.tech_stack.feature_flags:
                ff_counter[ff] += 1
        top_ff = ff_counter.most_common(6)
        ff_parts = [f"{ff} ({count})" for ff, count in top_ff]
        lines.append(f"  [bold]Flags:[/bold]       {has_ff}/{n} projects \u00b7 {', '.join(ff_parts)}")

    # HTTP clients
    has_hc = sum(1 for p in projects if p.tech_stack.http_clients)
    if has_hc:
        hc_counter: Counter[str] = Counter()
        for p in projects:
            for hc in p.tech_stack.http_clients:
                hc_counter[hc] += 1
        top_hc = hc_counter.most_common(6)
        hc_parts = [f"{hc} ({count})" for hc, count in top_hc]
        lines.append(f"  [bold]HTTP:[/bold]        {has_hc}/{n} projects \u00b7 {', '.join(hc_parts)}")

    # Doc generators
    has_dg = sum(1 for p in projects if p.tech_stack.doc_generators)
    if has_dg:
        dg_counter: Counter[str] = Counter()
        for p in projects:
            for dg in p.tech_stack.doc_generators:
                dg_counter[dg] += 1
        top_dg = dg_counter.most_common(6)
        dg_parts = [f"{dg} ({count})" for dg, count in top_dg]
        lines.append(f"  [bold]Docs Gen:[/bold]   {has_dg}/{n} projects \u00b7 {', '.join(dg_parts)}")

    # CLI frameworks
    has_clf = sum(1 for p in projects if p.tech_stack.cli_frameworks)
    if has_clf:
        clf_counter: Counter[str] = Counter()
        for p in projects:
            for clf in p.tech_stack.cli_frameworks:
                clf_counter[clf] += 1
        top_clf = clf_counter.most_common(6)
        clf_parts = [f"{clf} ({count})" for clf, count in top_clf]
        lines.append(f"  [bold]CLI:[/bold]         {has_clf}/{n} projects \u00b7 {', '.join(clf_parts)}")

    # Config tools
    has_cfg = sum(1 for p in projects if p.tech_stack.config_tools)
    if has_cfg:
        cfg_counter: Counter[str] = Counter()
        for p in projects:
            for cfg in p.tech_stack.config_tools:
                cfg_counter[cfg] += 1
        top_cfg = cfg_counter.most_common(6)
        cfg_parts = [f"{cfg} ({count})" for cfg, count in top_cfg]
        lines.append(f"  [bold]Config:[/bold]      {has_cfg}/{n} projects \u00b7 {', '.join(cfg_parts)}")

    # Caching tools
    has_cache = sum(1 for p in projects if p.tech_stack.caching_tools)
    if has_cache:
        cache_counter: Counter[str] = Counter()
        for p in projects:
            for ct in p.tech_stack.caching_tools:
                cache_counter[ct] += 1
        top_cache = cache_counter.most_common(6)
        cache_parts = [f"{ct} ({count})" for ct, count in top_cache]
        lines.append(f"  [bold]Caching:[/bold]     {has_cache}/{n} projects \u00b7 {', '.join(cache_parts)}")

    # Template engines
    has_tpl = sum(1 for p in projects if p.tech_stack.template_engines)
    if has_tpl:
        tpl_counter: Counter[str] = Counter()
        for p in projects:
            for te in p.tech_stack.template_engines:
                tpl_counter[te] += 1
        top_tpl = tpl_counter.most_common(6)
        tpl_parts = [f"{te} ({count})" for te, count in top_tpl]
        lines.append(f"  [bold]Templates:[/bold]   {has_tpl}/{n} projects \u00b7 {', '.join(tpl_parts)}")

    # Serialization formats
    has_ser = sum(1 for p in projects if p.tech_stack.serialization_formats)
    if has_ser:
        ser_counter: Counter[str] = Counter()
        for p in projects:
            for sf in p.tech_stack.serialization_formats:
                ser_counter[sf] += 1
        top_ser = ser_counter.most_common(6)
        ser_parts = [f"{sf} ({count})" for sf, count in top_ser]
        lines.append(f"  [bold]Serialization:[/bold] {has_ser}/{n} projects \u00b7 {', '.join(ser_parts)}")

    # DI frameworks
    has_di = sum(1 for p in projects if p.tech_stack.di_frameworks)
    if has_di:
        di_counter: Counter[str] = Counter()
        for p in projects:
            for df in p.tech_stack.di_frameworks:
                di_counter[df] += 1
        top_di = di_counter.most_common(6)
        di_parts = [f"{df} ({count})" for df, count in top_di]
        lines.append(f"  [bold]DI:[/bold]            {has_di}/{n} projects \u00b7 {', '.join(di_parts)}")

    # WebSocket libs
    has_ws = sum(1 for p in projects if p.tech_stack.websocket_libs)
    if has_ws:
        ws_counter: Counter[str] = Counter()
        for p in projects:
            for wl in p.tech_stack.websocket_libs:
                ws_counter[wl] += 1
        top_ws = ws_counter.most_common(6)
        ws_parts = [f"{wl} ({count})" for wl, count in top_ws]
        lines.append(f"  [bold]WebSocket:[/bold]    {has_ws}/{n} projects \u00b7 {', '.join(ws_parts)}")

    # GraphQL
    has_gql = sum(1 for p in projects if p.tech_stack.graphql_libs)
    if has_gql:
        gql_counter: Counter[str] = Counter()
        for p in projects:
            for gl in p.tech_stack.graphql_libs:
                gql_counter[gl] += 1
        top_gql = gql_counter.most_common(6)
        gql_parts = [f"{gl} ({count})" for gl, count in top_gql]
        lines.append(f"  [bold]GraphQL:[/bold]      {has_gql}/{n} projects · {', '.join(gql_parts)}")

    # Event streaming
    has_es = sum(1 for p in projects if p.tech_stack.event_streaming)
    if has_es:
        es_counter: Counter[str] = Counter()
        for p in projects:
            for es in p.tech_stack.event_streaming:
                es_counter[es] += 1
        top_es = es_counter.most_common(6)
        es_parts = [f"{es} ({count})" for es, count in top_es]
        lines.append(f"  [bold]Streaming:[/bold]  {has_es}/{n} projects · {', '.join(es_parts)}")

    # Payment tools
    has_pay = sum(1 for p in projects if p.tech_stack.payment_tools)
    if has_pay:
        pay_counter: Counter[str] = Counter()
        for p in projects:
            for pay in p.tech_stack.payment_tools:
                pay_counter[pay] += 1
        top_pay = pay_counter.most_common(6)
        pay_parts = [f"{pay} ({count})" for pay, count in top_pay]
        lines.append(f"  [bold]Payments:[/bold]   {has_pay}/{n} projects · {', '.join(pay_parts)}")

    # Date/time libs
    has_dl = sum(1 for p in projects if p.tech_stack.date_libs)
    if has_dl:
        dl_counter: Counter[str] = Counter()
        for p in projects:
            for dl in p.tech_stack.date_libs:
                dl_counter[dl] += 1
        top_dl = dl_counter.most_common(6)
        dl_parts = [f"{dl} ({count})" for dl, count in top_dl]
        lines.append(f"  [bold]Date/Time:[/bold]  {has_dl}/{n} projects · {', '.join(dl_parts)}")

    # Image processing libs
    has_il = sum(1 for p in projects if p.tech_stack.image_libs)
    if has_il:
        il_counter: Counter[str] = Counter()
        for p in projects:
            for il in p.tech_stack.image_libs:
                il_counter[il] += 1
        top_il = il_counter.most_common(6)
        il_parts = [f"{il} ({count})" for il, count in top_il]
        lines.append(f"  [bold]Imaging:[/bold]    {has_il}/{n} projects · {', '.join(il_parts)}")

    # Crypto libs
    has_cl = sum(1 for p in projects if p.tech_stack.crypto_libs)
    if has_cl:
        cl_counter: Counter[str] = Counter()
        for p in projects:
            for cl in p.tech_stack.crypto_libs:
                cl_counter[cl] += 1
        top_cl = cl_counter.most_common(6)
        cl_parts = [f"{cl} ({count})" for cl, count in top_cl]
        lines.append(f"  [bold]Crypto:[/bold]     {has_cl}/{n} projects · {', '.join(cl_parts)}")

    # PDF/doc libs
    has_pdf = sum(1 for p in projects if p.tech_stack.pdf_libs)
    if has_pdf:
        pdf_counter: Counter[str] = Counter()
        for p in projects:
            for pl in p.tech_stack.pdf_libs:
                pdf_counter[pl] += 1
        top_pdf = pdf_counter.most_common(6)
        pdf_parts = [f"{pl} ({count})" for pl, count in top_pdf]
        lines.append(f"  [bold]PDF/Docs:[/bold]   {has_pdf}/{n} projects · {', '.join(pdf_parts)}")

    # Data viz libs
    has_dvl = sum(1 for p in projects if p.tech_stack.data_viz_libs)
    if has_dvl:
        dvl_counter: Counter[str] = Counter()
        for p in projects:
            for dv in p.tech_stack.data_viz_libs:
                dvl_counter[dv] += 1
        top_dvl = dvl_counter.most_common(6)
        dvl_parts = [f"{dv} ({count})" for dv, count in top_dvl]
        lines.append(f"  [bold]Data Viz:[/bold]   {has_dvl}/{n} projects · {', '.join(dvl_parts)}")

    # Geo libs
    has_geo = sum(1 for p in projects if p.tech_stack.geo_libs)
    if has_geo:
        geo_counter: Counter[str] = Counter()
        for p in projects:
            for gl in p.tech_stack.geo_libs:
                geo_counter[gl] += 1
        top_geo = geo_counter.most_common(6)
        geo_parts = [f"{gl} ({count})" for gl, count in top_geo]
        lines.append(f"  [bold]Geo/Maps:[/bold]   {has_geo}/{n} projects · {', '.join(geo_parts)}")

    # API specs
    has_api = sum(1 for p in projects if p.tech_stack.api_specs)
    if has_api:
        api_counter: Counter[str] = Counter()
        for p in projects:
            for spec in p.tech_stack.api_specs:
                api_counter[spec] += 1
        top_api = api_counter.most_common(6)
        api_parts = [f"{spec} ({count})" for spec, count in top_api]
        lines.append(f"  [bold]API Specs:[/bold]   {has_api}/{n} projects \u00b7 {', '.join(api_parts)}")

    # License distribution
    lic_counter: Counter[str] = Counter()
    for p in projects:
        if p.license:
            lic_counter[p.license] += 1
    has_license = sum(1 for p in projects if p.license)
    if has_license:
        top_lic = lic_counter.most_common(6)
        lic_parts = [f"{lic} ({count})" for lic, count in top_lic]
        lines.append(f"  [bold]Licenses:[/bold]     {has_license}/{n} projects · {', '.join(lic_parts)}")

    content = "\n".join(lines)
    console.print(Panel(
        content,
        title="[bold white] Portfolio Summary [/bold white]",
        border_style="dim cyan",
        padding=(1, 2),
    ))


def show_connections(connections: list[Connection]):
    """Display cross-project intelligence."""
    if not connections:
        console.print("[dim]No cross-project connections found.[/dim]")
        return

    # Group by type
    groups: dict[str, list[Connection]] = {}
    for conn in connections:
        groups.setdefault(conn.type, []).append(conn)

    type_labels = {
        "shared_dep": "Shared Dependencies",
        "shared_framework": "Shared Frameworks",
        "version_mismatch": "Version Mismatches",
        "health_gap": "Health Gaps",
        "reuse_candidate": "Reuse Opportunities",
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
        "shared_cloud": "Shared Cloud Providers",
        "cloud_divergence": "Cloud Provider Divergence",
        "cloud_gap": "Cloud Provider Gaps",
        "shared_task_queue": "Shared Task Queues",
        "task_queue_divergence": "Task Queue Divergence",
        "task_queue_gap": "Task Queue Gaps",
        "shared_search": "Shared Search Engines",
        "search_divergence": "Search Engine Divergence",
        "search_gap": "Search Engine Gaps",
        "shared_feature_flag": "Shared Feature Flags",
        "feature_flag_divergence": "Feature Flag Divergence",
        "feature_flag_gap": "Feature Flag Gaps",
        "shared_http_client": "Shared HTTP Clients",
        "http_client_divergence": "HTTP Client Divergence",
        "http_client_gap": "HTTP Client Gaps",
        "shared_doc_generator": "Shared Doc Generators",
        "doc_generator_divergence": "Doc Generator Divergence",
        "doc_generator_gap": "Doc Generator Gaps",
        "shared_cli_framework": "Shared CLI Frameworks",
        "cli_framework_divergence": "CLI Framework Divergence",
        "shared_config_tool": "Shared Config Tools",
        "config_tool_divergence": "Config Tool Divergence",
        "config_tool_gap": "Config Tool Gaps",
        "shared_caching_tool": "Shared Caching Tools",
        "caching_divergence": "Caching Divergence",
        "caching_gap": "Caching Gaps",
        "shared_template_engine": "Shared Template Engines",
        "template_engine_divergence": "Template Engine Divergence",
        "shared_serialization_format": "Shared Serialization Formats",
        "serialization_divergence": "Serialization Divergence",
        "shared_di_framework": "Shared DI Frameworks",
        "di_divergence": "DI Approach Divergence",
        "shared_websocket_lib": "Shared WebSocket Libs",
        "websocket_divergence": "WebSocket Approach Divergence",
        "shared_graphql_lib": "Shared GraphQL Libs",
        "graphql_divergence": "GraphQL Approach Divergence",
        "shared_event_streaming": "Shared Event Streaming",
        "event_streaming_divergence": "Streaming Approach Divergence",
        "shared_payment_tool": "Shared Payment Tool",
        "payment_divergence": "Payment Approach Divergence",
        "shared_date_lib": "Shared Date/Time Lib",
        "date_lib_divergence": "Date/Time Approach Divergence",
        "shared_image_lib": "Shared Image Lib",
        "image_lib_divergence": "Imaging Approach Divergence",
        "shared_data_viz": "Shared Data Viz Lib",
        "data_viz_divergence": "Data Viz Approach Divergence",
    }

    lines = []
    for conn_type, conns in groups.items():
        label = type_labels.get(conn_type, conn_type)
        lines.append(f"  [bold]{label}[/bold]")
        for conn in conns:
            sev_icon = SEVERITY_ICONS.get(conn.severity, " ")
            proj_list = ", ".join(conn.projects[:4])
            if len(conn.projects) > 4:
                proj_list += f" +{len(conn.projects) - 4}"
            lines.append(f"    {sev_icon}  {conn.detail}")
            lines.append(f"       [dim]{proj_list}[/dim]")
        lines.append("")

    content = "\n".join(lines)
    console.print(Panel(
        content,
        title="[bold white] Cross-Project Intelligence [/bold white]",
        border_style="yellow",
        padding=(1, 2),
    ))

    # Summary statistics
    _show_connection_stats(connections)


def _show_connection_stats(connections: list[Connection]):
    """Show summary statistics for connections."""
    from collections import Counter

    total = len(connections)
    sev_counter: Counter[str] = Counter()
    cat_counter: Counter[str] = Counter()

    # Category mapping: connection type prefix -> display category
    type_to_category = {
        "shared_dep": "deps", "shared_framework": "deps",
        "version_mismatch": "deps", "reuse_candidate": "deps",
        "health_gap": "health",
        "shared_infra": "infra", "infra_divergence": "infra", "infra_gap": "infra",
        "shared_security": "security", "security_divergence": "security", "security_gap": "security",
        "shared_quality": "quality", "quality_divergence": "quality", "quality_gap": "quality",
        "shared_ai": "ai", "ai_divergence": "ai", "ai_gap": "ai",
        "shared_testing": "testing", "testing_divergence": "testing", "testing_gap": "testing",
        "shared_database": "database", "database_divergence": "database", "database_gap": "database",
        "shared_pkg_manager": "packages", "pkg_manager_divergence": "packages",
        "shared_license": "license", "license_divergence": "license", "license_gap": "license",
        "shared_docs": "docs", "docs_divergence": "docs", "docs_gap": "docs",
        "shared_ci_config": "ci", "ci_config_divergence": "ci", "ci_config_gap": "ci",
        "shared_runtime": "runtime", "runtime_divergence": "runtime", "runtime_gap": "runtime",
        "shared_build_tool": "build", "build_tool_divergence": "build", "build_tool_gap": "build",
        "shared_api_spec": "api", "api_spec_divergence": "api", "api_spec_gap": "api",
        "shared_monitoring": "monitoring", "monitoring_divergence": "monitoring", "monitoring_gap": "monitoring",
        "shared_auth": "auth", "auth_divergence": "auth", "auth_gap": "auth",
        "shared_messaging": "messaging", "messaging_divergence": "messaging", "messaging_gap": "messaging",
        "shared_deploy": "deploy", "deploy_divergence": "deploy", "deploy_gap": "deploy",
        "shared_state_mgmt": "state_mgmt", "state_mgmt_divergence": "state_mgmt", "state_mgmt_gap": "state_mgmt",
        "shared_css": "css", "css_divergence": "css", "css_gap": "css",
        "shared_bundler": "bundler", "bundler_divergence": "bundler", "bundler_gap": "bundler",
        "shared_orm": "orm", "orm_divergence": "orm", "orm_gap": "orm",
        "shared_i18n": "i18n", "i18n_divergence": "i18n", "i18n_gap": "i18n",
        "shared_validation": "validation", "validation_divergence": "validation", "validation_gap": "validation",
        "shared_logging": "logging", "logging_divergence": "logging", "logging_gap": "logging",
        "shared_container_orch": "containers", "container_orch_divergence": "containers", "container_orch_gap": "containers",
        "shared_cloud": "cloud", "cloud_divergence": "cloud", "cloud_gap": "cloud",
        "shared_task_queue": "queues", "task_queue_divergence": "queues", "task_queue_gap": "queues",
        "shared_search": "search", "search_divergence": "search", "search_gap": "search",
        "shared_feature_flag": "flags", "feature_flag_divergence": "flags", "feature_flag_gap": "flags",
        "shared_http_client": "http", "http_client_divergence": "http", "http_client_gap": "http",
        "shared_doc_generator": "docgen", "doc_generator_divergence": "docgen", "doc_generator_gap": "docgen",
        "shared_cli_framework": "cli", "cli_framework_divergence": "cli",
        "shared_config_tool": "config", "config_tool_divergence": "config", "config_tool_gap": "config",
        "shared_caching_tool": "caching", "caching_divergence": "caching", "caching_gap": "caching",
        "shared_template_engine": "templates", "template_engine_divergence": "templates",
        "shared_serialization_format": "serialization", "serialization_divergence": "serialization",
        "shared_di_framework": "di", "di_divergence": "di",
        "shared_websocket_lib": "websocket", "websocket_divergence": "websocket",
        "shared_graphql_lib": "graphql", "graphql_divergence": "graphql",
        "shared_event_streaming": "streaming", "event_streaming_divergence": "streaming",
        "shared_payment_tool": "payments", "payment_divergence": "payments",
        "shared_date_lib": "datetime", "date_lib_divergence": "datetime",
        "shared_image_lib": "imaging", "image_lib_divergence": "imaging",
        "shared_data_viz": "dataviz", "data_viz_divergence": "dataviz",
    }

    for conn in connections:
        sev_counter[conn.severity] += 1
        cat = type_to_category.get(conn.type, "other")
        cat_counter[cat] += 1

    parts = [f"[bold]{total}[/bold] connections"]

    # Severity breakdown
    sev_parts = []
    if sev_counter["critical"]:
        sev_parts.append(f"[red]{sev_counter['critical']} critical[/red]")
    if sev_counter["warning"]:
        sev_parts.append(f"[yellow]{sev_counter['warning']} warning[/yellow]")
    if sev_counter["info"]:
        sev_parts.append(f"[cyan]{sev_counter['info']} info[/cyan]")
    if sev_parts:
        parts.append(" · ".join(sev_parts))

    # Top categories
    top_cats = cat_counter.most_common(5)
    if top_cats:
        cat_parts = [f"{cat} ({count})" for cat, count in top_cats]
        remaining = len(cat_counter) - len(top_cats)
        cat_str = ", ".join(cat_parts)
        if remaining > 0:
            cat_str += f" +{remaining} more"
        parts.append(f"Top: {cat_str}")

    content = "  " + "   |   ".join(parts)
    console.print(Panel(
        content,
        title="[bold white] Connection Summary [/bold white]",
        border_style="dim yellow",
        padding=(0, 2),
    ))


def show_project_card(project: Project):
    """Display a single project summary card."""
    grade = project.health.grade
    color = HEALTH_COLORS.get(grade, "white")

    lines = []
    lines.append(f"  [bold]Path:[/bold]      {project.path}")
    lines.append(f"  [bold]Health:[/bold]    [{color}]{grade} ({project.health.percent}%)[/{color}]")
    lines.append(f"  [bold]Tests:[/bold]     {project.test_file_count:,} files")
    lines.append(f"  [bold]Source:[/bold]    {project.source_file_count:,} files | {project.loc:,} LOC")
    lines.append(f"  [bold]Stack:[/bold]     {project.tech_stack.summary}")

    if project.tech_stack.frameworks:
        fw = ", ".join(project.tech_stack.frameworks[:6])
        lines.append(f"  [bold]Frameworks:[/bold] {fw}")

    if project.tech_stack.databases:
        dbs = ", ".join(project.tech_stack.databases)
        lines.append(f"  [bold]Databases:[/bold]  {dbs}")

    if project.tech_stack.infrastructure:
        infra = ", ".join(project.tech_stack.infrastructure[:6])
        lines.append(f"  [bold]Infra:[/bold]      {infra}")

    if project.tech_stack.security_tools:
        sec = ", ".join(project.tech_stack.security_tools[:6])
        lines.append(f"  [bold]Security:[/bold]   {sec}")

    if project.tech_stack.ai_tools:
        ai = ", ".join(project.tech_stack.ai_tools[:6])
        lines.append(f"  [bold]AI/ML:[/bold]      {ai}")

    if project.tech_stack.quality_tools:
        qt = ", ".join(project.tech_stack.quality_tools[:6])
        lines.append(f"  [bold]Quality:[/bold]    {qt}")

    if project.tech_stack.testing_frameworks:
        tf = ", ".join(project.tech_stack.testing_frameworks[:6])
        lines.append(f"  [bold]Testing:[/bold]    {tf}")

    if project.tech_stack.package_managers:
        pm = ", ".join(project.tech_stack.package_managers[:6])
        lines.append(f"  [bold]Pkg Mgrs:[/bold]   {pm}")

    if project.tech_stack.docs_artifacts:
        da = ", ".join(project.tech_stack.docs_artifacts[:8])
        lines.append(f"  [bold]Docs:[/bold]       {da}")

    if project.tech_stack.ci_config:
        ci = ", ".join(project.tech_stack.ci_config[:8])
        lines.append(f"  [bold]CI/CD:[/bold]      {ci}")

    if project.tech_stack.runtime_versions:
        rv = ", ".join(f"{k} {v}" for k, v in project.tech_stack.runtime_versions.items())
        lines.append(f"  [bold]Runtimes:[/bold]   {rv}")

    if project.tech_stack.build_tools:
        bt = ", ".join(project.tech_stack.build_tools[:8])
        lines.append(f"  [bold]Build:[/bold]     {bt}")

    if project.tech_stack.api_specs:
        api = ", ".join(project.tech_stack.api_specs[:8])
        lines.append(f"  [bold]API Specs:[/bold] {api}")

    if project.tech_stack.monitoring_tools:
        mon = ", ".join(project.tech_stack.monitoring_tools[:8])
        lines.append(f"  [bold]Monitoring:[/bold] {mon}")

    if project.tech_stack.auth_tools:
        auth = ", ".join(project.tech_stack.auth_tools[:8])
        lines.append(f"  [bold]Auth:[/bold]       {auth}")

    if project.tech_stack.messaging_tools:
        msg = ", ".join(project.tech_stack.messaging_tools[:8])
        lines.append(f"  [bold]Messaging:[/bold] {msg}")

    if project.tech_stack.deploy_targets:
        dt = ", ".join(project.tech_stack.deploy_targets[:8])
        lines.append(f"  [bold]Deploy:[/bold]     {dt}")

    if project.tech_stack.state_management:
        sm = ", ".join(project.tech_stack.state_management[:8])
        lines.append(f"  [bold]State Mgmt:[/bold] {sm}")

    if project.tech_stack.css_frameworks:
        css = ", ".join(project.tech_stack.css_frameworks[:8])
        lines.append(f"  [bold]CSS/Style:[/bold]  {css}")

    if project.tech_stack.bundlers:
        bnd = ", ".join(project.tech_stack.bundlers[:8])
        lines.append(f"  [bold]Bundlers:[/bold]   {bnd}")

    if project.tech_stack.orm_tools:
        orm = ", ".join(project.tech_stack.orm_tools[:8])
        lines.append(f"  [bold]ORM/DB:[/bold]     {orm}")

    if project.tech_stack.i18n_tools:
        i18n = ", ".join(project.tech_stack.i18n_tools[:8])
        lines.append(f"  [bold]i18n:[/bold]       {i18n}")

    if project.tech_stack.validation_tools:
        val = ", ".join(project.tech_stack.validation_tools[:8])
        lines.append(f"  [bold]Validation:[/bold] {val}")

    if project.tech_stack.logging_tools:
        log = ", ".join(project.tech_stack.logging_tools[:8])
        lines.append(f"  [bold]Logging:[/bold]    {log}")

    if project.tech_stack.container_orchestration:
        co = ", ".join(project.tech_stack.container_orchestration[:8])
        lines.append(f"  [bold]Containers:[/bold] {co}")

    if project.tech_stack.cloud_providers:
        cp = ", ".join(project.tech_stack.cloud_providers[:8])
        lines.append(f"  [bold]Cloud:[/bold]      {cp}")

    if project.tech_stack.task_queues:
        tq = ", ".join(project.tech_stack.task_queues[:8])
        lines.append(f"  [bold]Queues:[/bold]     {tq}")

    if project.tech_stack.search_engines:
        se = ", ".join(project.tech_stack.search_engines[:8])
        lines.append(f"  [bold]Search:[/bold]     {se}")

    if project.tech_stack.feature_flags:
        ff = ", ".join(project.tech_stack.feature_flags[:8])
        lines.append(f"  [bold]Flags:[/bold]      {ff}")

    if project.tech_stack.http_clients:
        hc = ", ".join(project.tech_stack.http_clients[:8])
        lines.append(f"  [bold]HTTP:[/bold]       {hc}")

    if project.tech_stack.doc_generators:
        dg = ", ".join(project.tech_stack.doc_generators[:8])
        lines.append(f"  [bold]Docs Gen:[/bold]  {dg}")

    if project.tech_stack.cli_frameworks:
        clf = ", ".join(project.tech_stack.cli_frameworks[:8])
        lines.append(f"  [bold]CLI:[/bold]        {clf}")

    if project.tech_stack.config_tools:
        cfg = ", ".join(project.tech_stack.config_tools[:8])
        lines.append(f"  [bold]Config:[/bold]     {cfg}")

    if project.tech_stack.caching_tools:
        cch = ", ".join(project.tech_stack.caching_tools[:8])
        lines.append(f"  [bold]Caching:[/bold]    {cch}")

    if project.tech_stack.template_engines:
        tpl = ", ".join(project.tech_stack.template_engines[:8])
        lines.append(f"  [bold]Templates:[/bold]  {tpl}")

    if project.tech_stack.serialization_formats:
        ser = ", ".join(project.tech_stack.serialization_formats[:8])
        lines.append(f"  [bold]Serialization:[/bold] {ser}")

    if project.tech_stack.di_frameworks:
        di = ", ".join(project.tech_stack.di_frameworks[:8])
        lines.append(f"  [bold]DI:[/bold]            {di}")

    if project.tech_stack.websocket_libs:
        ws = ", ".join(project.tech_stack.websocket_libs[:8])
        lines.append(f"  [bold]WebSocket:[/bold]  {ws}")

    if project.tech_stack.graphql_libs:
        gql = ", ".join(project.tech_stack.graphql_libs[:8])
        lines.append(f"  [bold]GraphQL:[/bold]    {gql}")

    if project.tech_stack.event_streaming:
        es = ", ".join(project.tech_stack.event_streaming[:8])
        lines.append(f"  [bold]Streaming:[/bold]  {es}")

    if project.tech_stack.payment_tools:
        pay = ", ".join(project.tech_stack.payment_tools[:8])
        lines.append(f"  [bold]Payments:[/bold]   {pay}")

    if project.tech_stack.date_libs:
        dl = ", ".join(project.tech_stack.date_libs[:8])
        lines.append(f"  [bold]Date/Time:[/bold]  {dl}")

    if project.tech_stack.image_libs:
        il = ", ".join(project.tech_stack.image_libs[:8])
        lines.append(f"  [bold]Imaging:[/bold]    {il}")

    if project.tech_stack.crypto_libs:
        cl = ", ".join(project.tech_stack.crypto_libs[:8])
        lines.append(f"  [bold]Crypto:[/bold]     {cl}")

    if project.tech_stack.pdf_libs:
        pl = ", ".join(project.tech_stack.pdf_libs[:8])
        lines.append(f"  [bold]PDF/Docs:[/bold]   {pl}")

    if project.tech_stack.data_viz_libs:
        dv = ", ".join(project.tech_stack.data_viz_libs[:8])
        lines.append(f"  [bold]Data Viz:[/bold]   {dv}")

    if project.tech_stack.geo_libs:
        gl = ", ".join(project.tech_stack.geo_libs[:8])
        lines.append(f"  [bold]Geo/Maps:[/bold]   {gl}")

    if project.license:
        lines.append(f"  [bold]License:[/bold]    {project.license}")

    if project.git_info.branch:
        lines.append(f"  [bold]Branch:[/bold]    {project.git_info.branch}")
        lines.append(f"  [bold]Commits:[/bold]   {project.git_info.total_commits:,}")
        if project.git_info.last_commit_msg:
            lines.append(f"  [bold]Latest:[/bold]    {project.git_info.last_commit_msg}")
        if project.git_info.uncommitted_changes > 0:
            lines.append(f"  [bold]Dirty:[/bold]     [yellow]{project.git_info.uncommitted_changes} uncommitted changes[/yellow]")

    # Health breakdown
    h = project.health
    bar_tests = _mini_bar(h.tests)
    bar_git = _mini_bar(h.git_hygiene)
    bar_docs = _mini_bar(h.documentation)
    bar_struct = _mini_bar(h.structure)
    lines.append("")
    lines.append("  [bold]Health Breakdown:[/bold]")
    lines.append(f"    Tests          {bar_tests}  {int(h.tests * 100)}%")
    lines.append(f"    Git Hygiene    {bar_git}  {int(h.git_hygiene * 100)}%")
    lines.append(f"    Documentation  {bar_docs}  {int(h.documentation * 100)}%")
    lines.append(f"    Structure      {bar_struct}  {int(h.structure * 100)}%")

    content = "\n".join(lines)
    icon = _health_icon(project.health.overall)
    console.print(Panel(
        content,
        title=f"[bold white] {icon} {project.name} [/bold white]",
        border_style=color.replace("bold ", ""),
        padding=(1, 1),
    ))


def show_scan_complete(portfolio: Portfolio, duration_s: float):
    """Show scan completion summary."""
    console.print()
    console.print(
        f"  [green]\u2713[/green] Scanned [bold]{len(portfolio.projects)}[/bold] projects "
        f"in [bold]{duration_s:.1f}s[/bold]"
    )
    console.print(
        f"  [green]\u2713[/green] Found [bold]{portfolio.total_loc:,}[/bold] lines of code "
        f"across [bold]{portfolio.total_tests:,}[/bold] test files"
    )
    console.print(
        f"  [green]\u2713[/green] Portfolio health: "
        f"[{HEALTH_COLORS.get(portfolio.avg_grade, 'white')}]"
        f"{portfolio.avg_grade} ({int(portfolio.avg_health * 100)}%)"
        f"[/{HEALTH_COLORS.get(portfolio.avg_grade, 'white')}]"
    )
    console.print()


def show_comparison(a: Project, b: Project):
    """Display a side-by-side comparison of two projects."""
    # Header
    color_a = HEALTH_COLORS.get(a.health.grade, "white")
    color_b = HEALTH_COLORS.get(b.health.grade, "white")

    table = Table(
        box=box.ROUNDED,
        border_style="cyan",
        header_style="bold cyan",
        title="[bold white] Project Comparison [/bold white]",
        show_lines=True,
        expand=True,
    )
    table.add_column("", style="bold", min_width=14)
    table.add_column(a.name, justify="center", min_width=20)
    table.add_column(b.name, justify="center", min_width=20)
    table.add_column("Delta", justify="center", min_width=12)

    # Health
    delta_h = a.health.percent - b.health.percent
    delta_str = _delta_str(delta_h, suffix="%")
    table.add_row(
        "Health",
        f"[{color_a}]{a.health.grade} ({a.health.percent}%)[/{color_a}]",
        f"[{color_b}]{b.health.grade} ({b.health.percent}%)[/{color_b}]",
        delta_str,
    )

    # Health dimensions
    for label, dim_a, dim_b in [
        ("Tests", a.health.tests, b.health.tests),
        ("Git Hygiene", a.health.git_hygiene, b.health.git_hygiene),
        ("Documentation", a.health.documentation, b.health.documentation),
        ("Structure", a.health.structure, b.health.structure),
    ]:
        pct_a = int(dim_a * 100)
        pct_b = int(dim_b * 100)
        d = pct_a - pct_b
        table.add_row(
            f"  {label}",
            f"{_mini_bar(dim_a, 10)}  {pct_a}%",
            f"{_mini_bar(dim_b, 10)}  {pct_b}%",
            _delta_str(d, suffix="%"),
        )

    # Metrics
    table.add_row(
        "Test Files",
        f"{a.test_file_count:,}",
        f"{b.test_file_count:,}",
        _delta_str(a.test_file_count - b.test_file_count),
    )
    table.add_row(
        "Source Files",
        f"{a.source_file_count:,}",
        f"{b.source_file_count:,}",
        _delta_str(a.source_file_count - b.source_file_count),
    )
    table.add_row(
        "LOC",
        f"{a.loc:,}",
        f"{b.loc:,}",
        _delta_str(a.loc - b.loc),
    )
    table.add_row(
        "Commits",
        f"{a.git_info.total_commits:,}",
        f"{b.git_info.total_commits:,}",
        _delta_str(a.git_info.total_commits - b.git_info.total_commits),
    )

    # Tech stack
    table.add_row(
        "Stack",
        a.tech_stack.summary,
        b.tech_stack.summary,
        "",
    )

    # Shared frameworks
    fw_a = set(a.tech_stack.frameworks)
    fw_b = set(b.tech_stack.frameworks)
    shared_fw = fw_a & fw_b
    only_a_fw = fw_a - fw_b
    only_b_fw = fw_b - fw_a
    if shared_fw:
        table.add_row("Shared FW", ", ".join(sorted(shared_fw)), "", "")
    if only_a_fw or only_b_fw:
        table.add_row(
            "Unique FW",
            ", ".join(sorted(only_a_fw)) if only_a_fw else "[dim]-[/dim]",
            ", ".join(sorted(only_b_fw)) if only_b_fw else "[dim]-[/dim]",
            "",
        )

    # Shared deps
    deps_a = set(a.tech_stack.key_deps.keys())
    deps_b = set(b.tech_stack.key_deps.keys())
    shared_deps = deps_a & deps_b
    if shared_deps:
        table.add_row("Shared Deps", f"{len(shared_deps)}", f"{len(shared_deps)}", "")

    console.print()
    console.print(table)

    # Insights
    console.print()
    console.print("  [bold]Insights[/bold]")
    console.print()

    if a.health.overall > b.health.overall + 0.05:
        winner, loser = a, b
    elif b.health.overall > a.health.overall + 0.05:
        winner, loser = b, a
    else:
        winner = None

    if winner:
        console.print(f"  [green]\u25cf[/green] [bold]{winner.name}[/bold] is healthier overall")
        # Find which dimensions the loser could improve
        dims = [
            ("tests", winner.health.tests, loser.health.tests, "test coverage"),
            ("git_hygiene", winner.health.git_hygiene, loser.health.git_hygiene, "git hygiene"),
            ("documentation", winner.health.documentation, loser.health.documentation, "documentation"),
            ("structure", winner.health.structure, loser.health.structure, "project structure"),
        ]
        for _, w_val, l_val, label in dims:
            gap = w_val - l_val
            if gap > 0.1:
                console.print(
                    f"  [yellow]\u25b6[/yellow] {loser.name} could improve {label} "
                    f"(gap: {int(gap * 100)}%)"
                )
    else:
        console.print("  [green]\u25cf[/green] Both projects have similar health")

    if shared_deps:
        # Check for version mismatches in shared deps
        mismatches = []
        for dep in shared_deps:
            v_a = a.tech_stack.key_deps[dep]
            v_b = b.tech_stack.key_deps[dep]
            if v_a != v_b:
                mismatches.append(f"{dep} ({v_a} vs {v_b})")
        if mismatches:
            console.print(f"  [yellow]\u26a0[/yellow] Version mismatches: {', '.join(mismatches[:3])}")

    console.print()


def _delta_str(delta: int | float, suffix: str = "") -> str:
    """Format a delta value with color and sign."""
    if delta == 0:
        return "[dim]=[/dim]"
    sign = "+" if delta > 0 else ""
    color = "green" if delta > 0 else "red"
    if isinstance(delta, float):
        return f"[{color}]{sign}{delta:.1f}{suffix}[/{color}]"
    return f"[{color}]{sign}{delta}{suffix}[/{color}]"


def _health_icon(score: float) -> str:
    if score >= 0.76:
        return "[green]\u25cf[/green]"
    elif score >= 0.60:
        return "[yellow]\u25cf[/yellow]"
    elif score >= 0.40:
        return "[red]\u25cf[/red]"
    else:
        return "[dim red]\u25cf[/dim red]"


def show_quick_insights(recs: list) -> None:
    """Show top critical/high recommendations inline after dashboard."""
    top = [r for r in recs if r.priority in ("critical", "high")][:3]
    if not top:
        return

    lines = []
    for r in top:
        proj_list = ", ".join(r.projects[:3])
        if len(r.projects) > 3:
            proj_list += f" +{len(r.projects) - 3}"
        lines.append(f"  {r.icon} {r.message}")
        lines.append(f"     [dim]{proj_list}[/dim]")

    remaining = len([r for r in recs if r.priority in ("critical", "high")]) - len(top)
    if remaining > 0:
        lines.append(f"  [dim]... and {remaining} more — run [bold]atlas doctor[/bold] for full report[/dim]")
    else:
        total = len(recs)
        extra = total - len(top)
        if extra > 0:
            lines.append(f"  [dim]{extra} more suggestions — run [bold]atlas doctor[/bold] for full report[/dim]")

    content = "\n".join(lines)
    console.print(Panel(
        content,
        title="[bold white] Quick Insights [/bold white]",
        border_style="yellow",
        padding=(0, 2),
    ))


def _mini_bar(value: float, width: int = 15) -> str:
    """Create a mini progress bar."""
    filled = int(value * width)
    empty = width - filled

    if value >= 0.76:
        color = "green"
    elif value >= 0.60:
        color = "yellow"
    elif value >= 0.40:
        color = "red"
    else:
        color = "dim red"

    bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
    return bar
