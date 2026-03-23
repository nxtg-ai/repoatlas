"""CLI commands — the user-facing interface."""
from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from atlas.config import get_value, load_config, set_value, valid_keys
from atlas.connections import find_connections
from atlas.display import console, show_comparison, show_connections, show_project_card, show_quick_insights, show_scan_complete, show_status
from atlas.export_report import build_csv_report, build_json_report, build_markdown_report
from atlas.history import build_scan_entry, compute_trends, load_history, save_scan
from atlas.license_manager import activate as activate_license, get_status as get_license_status
from atlas.models import Portfolio
from atlas.recommendations import generate_recommendations
from atlas.scanner import scan_project

app = typer.Typer(
    name="atlas",
    help="Portfolio intelligence for AI engineering teams.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

DEFAULT_PORTFOLIO_DIR = Path.home() / ".atlas"
DEFAULT_PORTFOLIO_FILE = DEFAULT_PORTFOLIO_DIR / "portfolio.json"


def _load_portfolio() -> Portfolio:
    if not DEFAULT_PORTFOLIO_FILE.exists():
        console.print("[red]No portfolio found.[/red] Run [bold]atlas init[/bold] first.")
        raise typer.Exit(1)
    return Portfolio.load(DEFAULT_PORTFOLIO_FILE)


def _save_portfolio(portfolio: Portfolio):
    portfolio.save(DEFAULT_PORTFOLIO_FILE)


@app.command()
def init(name: str = typer.Option("My Portfolio", help="Portfolio name")):
    """Initialize a new portfolio."""
    if DEFAULT_PORTFOLIO_FILE.exists():
        console.print(f"[yellow]Portfolio already exists at {DEFAULT_PORTFOLIO_FILE}[/yellow]")
        console.print("Use [bold]atlas add[/bold] to add projects.")
        return

    portfolio = Portfolio(
        name=name,
        created=datetime.now(timezone.utc).isoformat(),
    )
    _save_portfolio(portfolio)

    console.print()
    console.print(f"  [green]\u2713[/green] Portfolio [bold]{name}[/bold] initialized")
    console.print(f"  [dim]Config: {DEFAULT_PORTFOLIO_FILE}[/dim]")
    console.print()
    console.print("  Next steps:")
    console.print("    [cyan]atlas add ~/projects/my-app[/cyan]    Add a project")
    console.print("    [cyan]atlas scan[/cyan]                     Scan all projects")
    console.print("    [cyan]atlas status[/cyan]                   View dashboard")
    console.print()


@app.command()
def add(
    path: str = typer.Argument(help="Path to the project directory"),
    name: Optional[str] = typer.Option(None, help="Custom project name"),
):
    """Add a project to the portfolio."""
    portfolio = _load_portfolio()
    project_path = Path(path).expanduser().resolve()

    if not project_path.is_dir():
        console.print(f"[red]Directory not found: {project_path}[/red]")
        raise typer.Exit(1)

    # Check if already added
    for existing in portfolio.projects:
        if existing.path == str(project_path):
            console.print(f"[yellow]Project already in portfolio: {existing.name}[/yellow]")
            return

    project_name = name or project_path.name

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Scanning {project_name}...", total=None)
        project = scan_project(project_path)

    if name:
        project.name = name

    portfolio.projects.append(project)
    _save_portfolio(portfolio)

    show_project_card(project)
    console.print(f"  [green]\u2713[/green] Added [bold]{project.name}[/bold] to portfolio")
    console.print()


@app.command()
def scan():
    """Scan all projects in the portfolio."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow] Run [bold]atlas add[/bold] first.")
        return

    console.print()
    start = time.time()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning projects...", total=len(portfolio.projects))

        updated_projects = []
        for proj in portfolio.projects:
            progress.update(task, description=f"Scanning [cyan]{proj.name}[/cyan]...")
            project_path = Path(proj.path)
            if project_path.is_dir():
                updated = scan_project(project_path)
                updated.name = proj.name  # preserve custom name
                updated_projects.append(updated)
            else:
                console.print(f"  [yellow]\u26a0 Skipping {proj.name} — directory not found[/yellow]")
                updated_projects.append(proj)
            progress.advance(task)

    portfolio.projects = updated_projects
    portfolio.last_scan = datetime.now(timezone.utc).isoformat()
    _save_portfolio(portfolio)

    # Save scan to history for trends
    save_scan(build_scan_entry(portfolio))

    elapsed = time.time() - start
    show_scan_complete(portfolio, elapsed)


@app.command()
def status(
    grade: Optional[str] = typer.Option(None, help="Filter by health grade (A, B+, B, C, D, F)"),
    lang: Optional[str] = typer.Option(None, help="Filter by language (e.g. Python, TypeScript)"),
    has: Optional[str] = typer.Option(None, help="Filter by tech (e.g. Docker, FastAPI, pytest)"),
    min_health: Optional[int] = typer.Option(None, help="Filter projects with health >= N%"),
    max_health: Optional[int] = typer.Option(None, help="Filter projects with health <= N%"),
    format: Optional[str] = typer.Option(None, help="Output format: json or csv"),
    grades: bool = typer.Option(False, "--grades", help="Show grade distribution summary"),
    sort: Optional[str] = typer.Option(None, help="Sort by: name, health, loc, grade"),
    limit: Optional[int] = typer.Option(None, "--limit", "-n", help="Limit number of projects displayed"),
):
    """Display the portfolio dashboard."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    filtered = list(portfolio.projects)
    active_filters: list[str] = []

    if grade:
        grade_upper = grade.upper()
        filtered = [p for p in filtered if p.health.grade == grade_upper]
        active_filters.append(f"grade={grade_upper}")

    if lang:
        lang_lower = lang.lower()
        filtered = [p for p in filtered if any(
            name.lower() == lang_lower for name in p.tech_stack.languages
        )]
        active_filters.append(f"lang={lang}")

    if has:
        has_lower = has.lower()
        filtered = [p for p in filtered if _project_has_tech(p, has_lower)]
        active_filters.append(f"has={has}")

    if min_health is not None:
        filtered = [p for p in filtered if p.health.percent >= min_health]
        active_filters.append(f"health>={min_health}%")

    if max_health is not None:
        filtered = [p for p in filtered if p.health.percent <= max_health]
        active_filters.append(f"health<={max_health}%")

    if active_filters and not filtered:
        if format and format.lower() == "json":
            print('{"projects": [], "total": 0}')
            return
        if format and format.lower() == "csv":
            print("Name,Path,Grade,Health%,Tests%,Git%,Docs%,Structure%,Languages,Frameworks,LOC,Source Files,Test Files,License")
            return
        console.print(f"[yellow]No projects match filters: {', '.join(active_filters)}[/yellow]")
        return

    display_projects = filtered if active_filters else list(portfolio.projects)

    if sort:
        sort_lower = sort.lower()
        grade_rank = {"A": 0, "B+": 1, "B": 2, "C": 3, "D": 4, "F": 5}
        if sort_lower == "name":
            display_projects.sort(key=lambda p: p.name.lower())
        elif sort_lower == "health":
            display_projects.sort(key=lambda p: p.health.percent, reverse=True)
        elif sort_lower == "loc":
            display_projects.sort(key=lambda p: p.loc, reverse=True)
        elif sort_lower == "grade":
            display_projects.sort(key=lambda p: (grade_rank.get(p.health.grade, 99), p.name.lower()))

    if limit is not None and limit > 0:
        display_projects = display_projects[:limit]

    if grades:
        from collections import Counter
        grade_counts: Counter[str] = Counter()
        for p in display_projects:
            grade_counts[p.health.grade] += 1
        if format and format.lower() == "json":
            import json as json_mod
            data = {"total": len(display_projects), "grades": dict(grade_counts.most_common())}
            print(json_mod.dumps(data, indent=2))
            return
        grade_order = ["A", "B+", "B", "C", "D", "F"]
        console.print()
        console.print("  [bold]Grade Distribution[/bold]")
        console.print()
        max_count = max(grade_counts.values()) if grade_counts else 1
        for g in grade_order:
            count = grade_counts.get(g, 0)
            if count == 0:
                continue
            bar_len = int((count / max_count) * 20)
            bar = "\u2588" * bar_len
            color = {"A": "green", "B+": "green", "B": "cyan", "C": "yellow", "D": "red", "F": "bold red"}.get(g, "white")
            console.print(f"  [{color}]{g:2s}[/{color}] [{color}]{bar}[/{color}] {count}")
        console.print()
        console.print(f"  [dim]{len(display_projects)} projects[/dim]")
        console.print()
        return

    if format and format.lower() == "json":
        import json as json_mod
        data = {
            "total": len(display_projects),
            "projects": [
                {
                    "name": p.name,
                    "path": p.path,
                    "health": {
                        "grade": p.health.grade,
                        "percent": p.health.percent,
                        "tests": round(p.health.tests, 2),
                        "git_hygiene": round(p.health.git_hygiene, 2),
                        "documentation": round(p.health.documentation, 2),
                        "structure": round(p.health.structure, 2),
                    },
                    "languages": dict(p.tech_stack.languages),
                    "frameworks": p.tech_stack.frameworks,
                    "loc": p.loc,
                    "source_files": p.source_file_count,
                    "test_files": p.test_file_count,
                    "license": p.license,
                }
                for p in display_projects
            ],
        }
        print(json_mod.dumps(data, indent=2))
        return

    if format and format.lower() == "csv":
        import csv as csv_mod
        import io
        buf = io.StringIO()
        writer = csv_mod.writer(buf)
        writer.writerow(["Name", "Path", "Grade", "Health%", "Tests%", "Git%", "Docs%", "Structure%", "Languages", "Frameworks", "LOC", "Source Files", "Test Files", "License"])
        for p in display_projects:
            writer.writerow([
                p.name, p.path, p.health.grade, p.health.percent,
                round(p.health.tests * 100), round(p.health.git_hygiene * 100),
                round(p.health.documentation * 100), round(p.health.structure * 100),
                "; ".join(p.tech_stack.primary_languages),
                "; ".join(p.tech_stack.frameworks),
                p.loc, p.source_file_count, p.test_file_count, p.license,
            ])
        print(buf.getvalue(), end="")
        return

    if active_filters or sort:
        view = Portfolio(
            name=portfolio.name,
            projects=display_projects,
            created=portfolio.created,
            last_scan=portfolio.last_scan,
        )
        if active_filters:
            console.print(f"  [dim]Filtered: {', '.join(active_filters)} ({len(filtered)}/{len(portfolio.projects)} projects)[/dim]")
        show_status(view, history=load_history())
    else:
        show_status(portfolio, history=load_history())
    if len(display_projects) > 1:
        conns = find_connections(display_projects)
        if conns:
            console.print()
            show_connections(conns)

    # Quick insights — top actionable recommendations
    display_portfolio = Portfolio(
        name=portfolio.name,
        projects=display_projects,
        created=portfolio.created,
        last_scan=portfolio.last_scan,
    ) if active_filters else portfolio
    recs = generate_recommendations(display_portfolio)
    if recs:
        console.print()
        show_quick_insights(recs)


def _project_has_tech(project, term: str) -> bool:
    """Check if a project has a given technology anywhere in its tech stack."""
    ts = project.tech_stack
    all_items = (
        list(ts.languages.keys())
        + ts.frameworks
        + ts.databases
        + ts.infrastructure
        + ts.security_tools
        + ts.ai_tools
        + ts.quality_tools
        + ts.testing_frameworks
        + ts.package_managers
        + ts.docs_artifacts
        + ts.ci_config
        + list(ts.runtime_versions.keys())
        + ts.build_tools
        + ts.api_specs
        + ts.monitoring_tools
        + ts.auth_tools
        + ts.messaging_tools
        + ts.deploy_targets
        + ts.state_management
        + ts.css_frameworks
        + ts.bundlers
        + ts.orm_tools
        + ts.i18n_tools
        + ts.validation_tools
        + ts.logging_tools
        + ts.container_orchestration
        + ts.cloud_providers
        + ts.task_queues
        + ts.search_engines
        + ts.feature_flags
        + ts.http_clients
        + ts.doc_generators
        + ts.cli_frameworks
        + ts.config_tools
        + ts.caching_tools
        + ts.template_engines
        + ts.serialization_formats
        + ts.di_frameworks
        + ts.websocket_libs
        + ts.graphql_libs
        + ts.event_streaming
        + ts.payment_tools
        + ts.date_libs
        + ts.image_libs
        + ts.crypto_libs
        + ts.pdf_libs
        + ts.data_viz_libs
        + ts.geo_libs
        + ts.media_libs
        + ts.math_libs
        + ts.async_libs
    )
    return any(term == item.lower() for item in all_items)


CONNECTION_CATEGORIES = {
    "deps": {"shared_dep", "shared_framework", "version_mismatch", "reuse_candidate"},
    "health": {"health_gap"},
    "infra": {"shared_infra", "infra_divergence", "infra_gap"},
    "security": {"shared_security", "security_divergence", "security_gap"},
    "quality": {"shared_quality", "quality_divergence", "quality_gap"},
    "ai": {"shared_ai", "ai_divergence", "ai_gap"},
    "testing": {"shared_testing", "testing_divergence", "testing_gap"},
    "database": {"shared_database", "database_divergence", "database_gap"},
    "packages": {"shared_pkg_manager", "pkg_manager_divergence"},
    "license": {"shared_license", "license_divergence", "license_gap"},
    "docs": {"shared_docs", "docs_divergence", "docs_gap"},
    "ci": {"shared_ci_config", "ci_config_divergence", "ci_config_gap"},
    "runtime": {"shared_runtime", "runtime_divergence", "runtime_gap"},
    "build": {"shared_build_tool", "build_tool_divergence", "build_tool_gap"},
    "api": {"shared_api_spec", "api_spec_divergence", "api_spec_gap"},
    "monitoring": {"shared_monitoring", "monitoring_divergence", "monitoring_gap"},
    "auth": {"shared_auth", "auth_divergence", "auth_gap"},
    "messaging": {"shared_messaging", "messaging_divergence", "messaging_gap"},
    "deploy": {"shared_deploy", "deploy_divergence", "deploy_gap"},
    "state_mgmt": {"shared_state_mgmt", "state_mgmt_divergence", "state_mgmt_gap"},
    "css": {"shared_css", "css_divergence", "css_gap"},
    "bundler": {"shared_bundler", "bundler_divergence", "bundler_gap"},
    "orm": {"shared_orm", "orm_divergence", "orm_gap"},
    "i18n": {"shared_i18n", "i18n_divergence", "i18n_gap"},
    "validation": {"shared_validation", "validation_divergence", "validation_gap"},
    "logging": {"shared_logging", "logging_divergence", "logging_gap"},
    "containers": {"shared_container_orch", "container_orch_divergence", "container_orch_gap"},
    "cloud": {"shared_cloud", "cloud_divergence", "cloud_gap"},
    "queues": {"shared_task_queue", "task_queue_divergence", "task_queue_gap"},
    "search": {"shared_search", "search_divergence", "search_gap"},
    "flags": {"shared_feature_flag", "feature_flag_divergence", "feature_flag_gap"},
    "http": {"shared_http_client", "http_client_divergence", "http_client_gap"},
    "docgen": {"shared_doc_generator", "doc_generator_divergence", "doc_generator_gap"},
    "cli": {"shared_cli_framework", "cli_framework_divergence"},
    "config": {"shared_config_tool", "config_tool_divergence", "config_tool_gap"},
    "caching": {"shared_caching_tool", "caching_divergence", "caching_gap"},
    "templates": {"shared_template_engine", "template_engine_divergence"},
    "serialization": {"shared_serialization_format", "serialization_divergence"},
    "di": {"shared_di_framework", "di_divergence"},
    "websocket": {"shared_websocket_lib", "websocket_divergence"},
    "graphql": {"shared_graphql_lib", "graphql_divergence"},
    "streaming": {"shared_event_streaming", "event_streaming_divergence"},
    "payments": {"shared_payment_tool", "payment_divergence"},
    "datetime": {"shared_date_lib", "date_lib_divergence"},
    "imaging": {"shared_image_lib", "image_lib_divergence"},
    "dataviz": {"shared_data_viz", "data_viz_divergence"},
    "geo": {"shared_geo_lib", "geo_lib_divergence"},
    "media": {"shared_media_lib", "media_lib_divergence"},
    "math": {"shared_math_lib", "math_lib_divergence"},
    "async": {"shared_async_lib", "async_lib_divergence"},
    "crypto": {"shared_crypto_lib", "crypto_lib_divergence"},
    "pdf": {"shared_pdf_lib", "pdf_lib_divergence"},
    "email": {"shared_email_lib", "email_lib_divergence"},
    "compression": {"shared_compression_lib", "compression_lib_divergence"},
    "a11y": {"shared_a11y_tool", "a11y_divergence"},
    "scraping": {"shared_scraping_lib", "scraping_lib_divergence"},
    "desktop": {"shared_desktop_framework", "desktop_framework_divergence"},
}


@app.command()
def connections(
    type_filter: Optional[str] = typer.Option(None, "--type", "-t", help="Filter by category (use --type list to see all)"),
    severity: Optional[str] = typer.Option(None, "--severity", "-s", help="Filter by severity (info, warning, critical)"),
    project: Optional[str] = typer.Option(None, "--project", "-p", help="Filter connections involving a specific project"),
    format: Optional[str] = typer.Option(None, help="Output format: json or csv for structured output"),
    summary: bool = typer.Option(False, "--summary", help="Show compact category summary table"),
    sort: Optional[str] = typer.Option(None, "--sort", help="Sort by: type, severity, projects"),
    limit: Optional[int] = typer.Option(None, "--limit", "-n", help="Max connections to show"),
):
    """Show cross-project intelligence."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    conns = find_connections(portfolio.projects)

    if type_filter:
        cat = type_filter.lower()
        if cat == "list":
            console.print()
            console.print("  [bold]Available connection categories:[/bold]")
            console.print()
            for name in sorted(CONNECTION_CATEGORIES):
                types = ", ".join(sorted(CONNECTION_CATEGORIES[name]))
                console.print(f"  [cyan]{name:12s}[/cyan] {types}")
            console.print()
            console.print(f"  [dim]{len(CONNECTION_CATEGORIES)} categories available[/dim]")
            console.print()
            return
        if cat not in CONNECTION_CATEGORIES:
            valid = ", ".join(sorted(CONNECTION_CATEGORIES))
            console.print(f"[red]Unknown category '{type_filter}'. Valid: {valid}[/red]")
            raise typer.Exit(1)
        allowed = CONNECTION_CATEGORIES[cat]
        total = len(conns)
        conns = [c for c in conns if c.type in allowed]
        if not (format and format.lower() in ("json", "csv")):
            console.print()
            console.print(f"  [dim]Filtered: {len(conns)}/{total} connections (category: {cat})[/dim]")

    if severity:
        sev = severity.lower()
        valid_severities = {"info", "warning", "critical"}
        if sev not in valid_severities:
            console.print(f"[red]Unknown severity '{severity}'. Valid: info, warning, critical[/red]")
            raise typer.Exit(1)
        total = len(conns)
        conns = [c for c in conns if c.severity == sev]
        if not (format and format.lower() in ("json", "csv")):
            console.print()
            console.print(f"  [dim]Filtered: {len(conns)}/{total} connections (severity: {sev})[/dim]")

    if project:
        proj_lower = project.lower()
        total = len(conns)
        conns = [c for c in conns if any(proj_lower == p.lower() for p in c.projects)]
        if not (format and format.lower() in ("json", "csv")):
            console.print()
            console.print(f"  [dim]Filtered: {len(conns)}/{total} connections (project: {project})[/dim]")

    if sort:
        sort_lower = sort.lower()
        severity_rank = {"critical": 0, "warning": 1, "info": 2}
        if sort_lower == "type":
            conns.sort(key=lambda c: c.type)
        elif sort_lower == "severity":
            conns.sort(key=lambda c: (severity_rank.get(c.severity, 99), c.type))
        elif sort_lower == "projects":
            conns.sort(key=lambda c: len(c.projects), reverse=True)

    if limit is not None and limit > 0:
        conns = conns[:limit]

    if summary:
        from collections import Counter
        cat_counts: dict[str, Counter[str]] = {}
        reverse_map: dict[str, str] = {}
        for cat_name, types in CONNECTION_CATEGORIES.items():
            for t in types:
                reverse_map[t] = cat_name
        for c in conns:
            cat = reverse_map.get(c.type, "other")
            if cat not in cat_counts:
                cat_counts[cat] = Counter()
            cat_counts[cat][c.severity] += 1
        if format and format.lower() == "json":
            import json as json_mod
            data = {
                "total": len(conns),
                "categories": {
                    cat: {"total": sum(sevs.values()), **dict(sevs)}
                    for cat, sevs in sorted(cat_counts.items())
                },
            }
            print(json_mod.dumps(data, indent=2))
            return
        from rich.table import Table
        from rich import box
        table = Table(title="Connection Summary", box=box.SIMPLE)
        table.add_column("Category", style="cyan")
        table.add_column("Total", justify="right")
        table.add_column("Critical", justify="right", style="red")
        table.add_column("Warning", justify="right", style="yellow")
        table.add_column("Info", justify="right", style="cyan")
        for cat in sorted(cat_counts):
            sevs = cat_counts[cat]
            total = sum(sevs.values())
            table.add_row(
                cat,
                str(total),
                str(sevs.get("critical", 0)) if sevs.get("critical") else "",
                str(sevs.get("warning", 0)) if sevs.get("warning") else "",
                str(sevs.get("info", 0)) if sevs.get("info") else "",
            )
        console.print()
        console.print(table)
        console.print(f"\n  [dim]{len(conns)} total connections across {len(cat_counts)} categories[/dim]\n")
        return

    if format and format.lower() == "json":
        import json as json_mod
        sev_counts: dict[str, int] = {}
        for c in conns:
            sev_counts[c.severity] = sev_counts.get(c.severity, 0) + 1
        data = {
            "total": len(conns),
            "connections": [
                {
                    "type": c.type,
                    "detail": c.detail,
                    "projects": c.projects,
                    "severity": c.severity,
                }
                for c in conns
            ],
            "summary": sev_counts,
        }
        print(json_mod.dumps(data, indent=2))
        return

    if format and format.lower() == "csv":
        import csv
        import io
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Type", "Detail", "Projects", "Severity"])
        for c in conns:
            writer.writerow([c.type, c.detail, "; ".join(c.projects), c.severity])
        print(buf.getvalue(), end="")
        return

    console.print()
    show_connections(conns)


@app.command()
def doctor(
    format: Optional[str] = typer.Option(None, help="Output format: json or csv for structured output"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category (e.g. testing, security, infra, deps, docs)"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="Filter by priority (critical, high, medium, low)"),
    sort: Optional[str] = typer.Option(None, "--sort", help="Sort by: priority, category"),
    project: Optional[str] = typer.Option(None, "--project", help="Filter recommendations for a specific project"),
    limit: Optional[int] = typer.Option(None, "--limit", "-n", help="Max recommendations to show"),
):
    """Diagnose portfolio health and suggest fixes."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    recs = generate_recommendations(portfolio)

    if project:
        recs = [r for r in recs if project.lower() in [p.lower() for p in r.projects]]

    if category:
        cat_lower = category.lower()
        recs = [r for r in recs if r.category.lower() == cat_lower]

    if priority:
        valid_priorities = {"critical", "high", "medium", "low"}
        pri_lower = priority.lower()
        if pri_lower not in valid_priorities:
            console.print(f"[red]Unknown priority '{priority}'. Valid: critical, high, medium, low[/red]")
            raise typer.Exit(1)
        recs = [r for r in recs if r.priority == pri_lower]

    if sort:
        sort_lower = sort.lower()
        if sort_lower == "priority":
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            recs.sort(key=lambda r: priority_order.get(r.priority, 99))
        elif sort_lower == "category":
            recs.sort(key=lambda r: r.category)

    if limit is not None and limit > 0:
        recs = recs[:limit]

    if format and format.lower() == "json":
        import json as json_mod
        data = {
            "total": len(recs),
            "recommendations": [
                {
                    "priority": rec.priority,
                    "category": rec.category,
                    "message": rec.message,
                    "projects": rec.projects,
                }
                for rec in recs
            ],
        }
        counts: dict[str, int] = {}
        for rec in recs:
            counts[rec.priority] = counts.get(rec.priority, 0) + 1
        data["summary"] = counts
        cat_counts_j: dict[str, int] = {}
        for rec in recs:
            cat_counts_j[rec.category] = cat_counts_j.get(rec.category, 0) + 1
        data["categories"] = cat_counts_j
        print(json_mod.dumps(data, indent=2))
        return

    if format and format.lower() == "csv":
        import csv
        import io
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Priority", "Category", "Message", "Projects"])
        for rec in recs:
            writer.writerow([rec.priority, rec.category, rec.message, "; ".join(rec.projects)])
        print(buf.getvalue(), end="")
        return

    console.print()
    if not recs:
        console.print("  [green]\u2713[/green] [bold]Portfolio is healthy![/bold] No issues found.")
        console.print()
        return

    console.print(f"  [bold]Found {len(recs)} recommendation{'s' if len(recs) != 1 else ''}:[/bold]")
    console.print()

    for rec in recs:
        proj_list = ", ".join(rec.projects[:3])
        if len(rec.projects) > 3:
            proj_list += f" +{len(rec.projects) - 3}"
        console.print(f"  {rec.icon} [{rec.priority.upper()}] {rec.message}")

    # Summary counts
    counts_r: dict[str, int] = {}
    for rec in recs:
        counts_r[rec.priority] = counts_r.get(rec.priority, 0) + 1
    parts = []
    for p in ("critical", "high", "medium", "low"):
        if p in counts_r:
            parts.append(f"{counts_r[p]} {p}")
    console.print()
    console.print(f"  [dim]Summary: {', '.join(parts)}[/dim]")

    # Category breakdown
    cat_counts: dict[str, int] = {}
    for rec in recs:
        cat_counts[rec.category] = cat_counts.get(rec.category, 0) + 1
    cat_parts = [f"{v} {k}" for k, v in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)]
    console.print(f"  [dim]Categories: {', '.join(cat_parts)}[/dim]")
    console.print()


@app.command()
def search(
    query: str = typer.Argument(help="Search term (matches name, language, framework, or tech)"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format: json"),
    sort: Optional[str] = typer.Option(None, "--sort", help="Sort by: name, health, loc"),
    limit: Optional[int] = typer.Option(None, "--limit", "-n", help="Max results to show"),
):
    """Search portfolio projects by name, language, framework, or technology."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    term = query.lower()
    matches = []
    for p in portfolio.projects:
        # Match against name
        if term in p.name.lower():
            matches.append(p)
            continue
        # Match against languages
        if any(term == lang.lower() for lang in p.tech_stack.languages):
            matches.append(p)
            continue
        # Match against all tech fields
        if _project_has_tech(p, term):
            matches.append(p)
            continue

    if sort:
        sort_lower = sort.lower()
        if sort_lower == "name":
            matches.sort(key=lambda p: p.name.lower())
        elif sort_lower == "health":
            matches.sort(key=lambda p: p.health.overall, reverse=True)
        elif sort_lower == "loc":
            matches.sort(key=lambda p: p.loc, reverse=True)

    if limit is not None and limit > 0:
        matches = matches[:limit]

    if format == "json":
        import json as json_mod
        data = {
            "query": query,
            "total": len(matches),
            "projects": [
                {
                    "name": p.name,
                    "path": p.path,
                    "health_grade": p.health.grade,
                    "health_percent": p.health.percent,
                    "languages": dict(p.tech_stack.languages),
                    "frameworks": p.tech_stack.frameworks,
                    "loc": p.loc,
                    "license": p.license,
                }
                for p in matches
            ],
        }
        console.print(json_mod.dumps(data, indent=2))
        return

    console.print()
    if not matches:
        console.print(f"  [yellow]No projects match '{query}'[/yellow]")
        console.print()
        return

    console.print(f"  [bold]{len(matches)} project{'s' if len(matches) != 1 else ''} matching '{query}':[/bold]")
    console.print()
    for p in matches:
        grade_color = {"A": "green", "B+": "green", "B": "cyan", "C": "yellow", "D": "red", "F": "bold red"}.get(p.health.grade, "white")
        console.print(f"  [{grade_color}]{p.health.grade:>2}[/{grade_color}] {p.health.percent:>3}%  [bold]{p.name}[/bold]  [dim]{p.tech_stack.summary}[/dim]")
    console.print()


@app.command()
def ci(
    min_health: int = typer.Option(0, help="Minimum portfolio health % (0-100). Fail if below."),
    min_project_health: int = typer.Option(0, help="Minimum per-project health %. Fail if any project below."),
    format: str = typer.Option("json", help="Output format: json, summary"),
):
    """Run health checks for CI pipelines. Exits non-zero on violations."""
    import json as json_mod

    # Apply config defaults when CLI flags aren't explicitly set
    cfg = load_config()
    if min_health == 0:
        min_health = int(cfg.get("ci", {}).get("min_health", 0))
    if min_project_health == 0:
        min_project_health = int(cfg.get("ci", {}).get("min_project_health", 0))

    portfolio = _load_portfolio()

    if not portfolio.projects:
        if format == "json":
            print(json_mod.dumps({"status": "error", "message": "No projects in portfolio"}))
        else:
            console.print("[red]No projects in portfolio.[/red]")
        raise typer.Exit(1)

    # Re-scan all projects
    updated_projects = []
    for proj in portfolio.projects:
        project_path = Path(proj.path)
        if project_path.is_dir():
            updated = scan_project(project_path)
            updated.name = proj.name
            updated_projects.append(updated)
        else:
            updated_projects.append(proj)

    portfolio.projects = updated_projects
    portfolio.last_scan = datetime.now(timezone.utc).isoformat()
    _save_portfolio(portfolio)
    save_scan(build_scan_entry(portfolio))

    # Check violations
    violations = []
    portfolio_pct = int(portfolio.avg_health * 100)

    if min_health > 0 and portfolio_pct < min_health:
        violations.append({
            "type": "portfolio_health",
            "threshold": min_health,
            "actual": portfolio_pct,
            "message": f"Portfolio health {portfolio_pct}% < {min_health}% minimum",
        })

    if min_project_health > 0:
        for p in portfolio.projects:
            pct = p.health.percent
            if pct < min_project_health:
                violations.append({
                    "type": "project_health",
                    "project": p.name,
                    "threshold": min_project_health,
                    "actual": pct,
                    "message": f"{p.name} health {pct}% < {min_project_health}% minimum",
                })

    passed = len(violations) == 0

    if format == "json":
        result = {
            "status": "pass" if passed else "fail",
            "portfolio": {
                "name": portfolio.name,
                "health": portfolio_pct,
                "grade": portfolio.avg_grade,
                "projects": len(portfolio.projects),
                "test_files": portfolio.total_tests,
                "loc": portfolio.total_loc,
            },
            "projects": [
                {
                    "name": p.name,
                    "health": p.health.percent,
                    "grade": p.health.grade,
                    "tests": p.test_file_count,
                    "loc": p.loc,
                }
                for p in portfolio.projects
            ],
            "violations": violations,
        }
        print(json_mod.dumps(result, indent=2))
    else:
        # Summary format — one-liner for CI logs
        status = "PASS" if passed else "FAIL"
        console.print(
            f"atlas ci: {status} | {portfolio.name} | "
            f"{portfolio.avg_grade} ({portfolio_pct}%) | "
            f"{len(portfolio.projects)} projects | "
            f"{portfolio.total_tests} test files | "
            f"{portfolio.total_loc:,} LOC"
        )
        if violations:
            for v in violations:
                console.print(f"  [red]FAIL[/red] {v['message']}")

    if not passed:
        raise typer.Exit(1)


@app.command()
def trends():
    """Show health trends across scans."""
    entries = load_history()

    if len(entries) == 0:
        console.print("[yellow]No scan history.[/yellow] Run [bold]atlas scan[/bold] first.")
        return

    if len(entries) < 2:
        console.print("[yellow]Need at least 2 scans for trends.[/yellow] Run [bold]atlas scan[/bold] again after making changes.")
        return

    latest = entries[-1]
    previous = entries[-2]
    project_trends = compute_trends(entries)

    console.print()
    console.print("  [bold]Portfolio Trends[/bold]")
    console.print()

    # Portfolio-level delta
    health_delta = latest.portfolio_health - previous.portfolio_health
    if abs(health_delta) < 0.005:
        arrow = "[dim]=[/dim]"
    elif health_delta > 0:
        arrow = f"[green]\u2191 +{health_delta:.0%}[/green]"
    else:
        arrow = f"[red]\u2193 {health_delta:.0%}[/red]"

    console.print(f"  Health: {latest.portfolio_grade} ({latest.portfolio_health:.0%}) {arrow}")
    console.print(f"  Tests: {latest.total_tests:,}  |  LOC: {latest.total_loc:,}  |  Projects: {latest.total_projects}")

    test_delta = latest.total_tests - previous.total_tests
    if test_delta != 0:
        sign = "+" if test_delta > 0 else ""
        color = "green" if test_delta > 0 else "red"
        console.print(f"  [dim]Tests delta:[/dim] [{color}]{sign}{test_delta}[/{color}]")

    console.print()
    console.print("  [bold]Per-Project Changes[/bold] [dim](vs previous scan)[/dim]")
    console.print()

    direction_icons = {
        "up": "[green]\u2191[/green]",
        "down": "[red]\u2193[/red]",
        "stable": "[dim]=[/dim]",
        "new": "[cyan]+[/cyan]",
        "removed": "[red]-[/red]",
    }

    for t in sorted(project_trends, key=lambda x: x["direction"] != "down"):
        icon = direction_icons.get(t["direction"], " ")
        name = t["name"]
        if t["direction"] == "new":
            console.print(f"  {icon} {name} — [cyan]new[/cyan] ({t['current']:.0%})")
        elif t["direction"] == "removed":
            console.print(f"  {icon} {name} — [red]removed[/red]")
        elif t["direction"] == "stable":
            console.print(f"  {icon} {name} — {t['current']:.0%} [dim](stable)[/dim]")
        else:
            delta = t["delta"]
            sign = "+" if delta > 0 else ""
            color = "green" if delta > 0 else "red"
            console.print(f"  {icon} {name} — {t['current']:.0%} [{color}]({sign}{delta:.0%})[/{color}]")

    console.print()
    console.print(f"  [dim]{len(entries)} scans in history | Latest: {latest.timestamp[:19]}[/dim]")
    console.print()


@app.command()
def remove(name: str = typer.Argument(help="Project name to remove")):
    """Remove a project from the portfolio."""
    portfolio = _load_portfolio()
    project = portfolio.find_project(name)

    if not project:
        console.print(f"[red]Project not found: {name}[/red]")
        available = ", ".join(p.name for p in portfolio.projects)
        console.print(f"[dim]Available: {available}[/dim]")
        raise typer.Exit(1)

    portfolio.projects.remove(project)
    _save_portfolio(portfolio)
    console.print(f"  [green]\u2713[/green] Removed [bold]{name}[/bold] from portfolio")


@app.command()
def rename(
    old_name: str = typer.Argument(help="Current project name"),
    new_name: str = typer.Argument(help="New project name"),
):
    """Rename a project in the portfolio."""
    portfolio = _load_portfolio()
    project = portfolio.find_project(old_name)

    if not project:
        console.print(f"[red]Project not found: {old_name}[/red]")
        available = ", ".join(p.name for p in portfolio.projects)
        console.print(f"[dim]Available: {available}[/dim]")
        raise typer.Exit(1)

    existing = portfolio.find_project(new_name)
    if existing:
        console.print(f"[red]Name already in use: {new_name}[/red]")
        raise typer.Exit(1)

    project.name = new_name
    _save_portfolio(portfolio)
    console.print(f"  [green]\u2713[/green] Renamed [bold]{old_name}[/bold] \u2192 [bold]{new_name}[/bold]")


@app.command(name="batch-remove")
def batch_remove():
    """Remove projects whose directories no longer exist on disk."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    stale = [p for p in portfolio.projects if not Path(p.path).is_dir()]

    if not stale:
        console.print()
        console.print("  [green]\u2713[/green] All projects still exist on disk. Nothing to remove.")
        console.print()
        return

    console.print()
    console.print(f"  Found [bold]{len(stale)}[/bold] stale project{'s' if len(stale) != 1 else ''}:")
    console.print()
    for p in stale:
        console.print(f"    [red]\u2717[/red] {p.name}  [dim]{p.path}[/dim]")
    console.print()

    portfolio.projects = [p for p in portfolio.projects if Path(p.path).is_dir()]
    _save_portfolio(portfolio)
    console.print(f"  [green]\u2713[/green] Removed {len(stale)} stale project{'s' if len(stale) != 1 else ''}")
    console.print()


@app.command()
def inspect(name: str = typer.Argument(help="Project name to inspect")):
    """Show detailed info for a single project."""
    portfolio = _load_portfolio()
    project = portfolio.find_project(name)

    if not project:
        console.print(f"[red]Project not found: {name}[/red]")
        available = ", ".join(p.name for p in portfolio.projects)
        console.print(f"[dim]Available: {available}[/dim]")
        raise typer.Exit(1)

    show_project_card(project)


@app.command()
def compare(
    project_a: str = typer.Argument(help="First project name"),
    project_b: str = typer.Argument(help="Second project name"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format: json or csv"),
):
    """Compare two projects side by side."""
    portfolio = _load_portfolio()
    available = ", ".join(p.name for p in portfolio.projects)

    a = portfolio.find_project(project_a)
    if not a:
        console.print(f"[red]Project not found: {project_a}[/red]")
        console.print(f"[dim]Available: {available}[/dim]")
        raise typer.Exit(1)

    b = portfolio.find_project(project_b)
    if not b:
        console.print(f"[red]Project not found: {project_b}[/red]")
        console.print(f"[dim]Available: {available}[/dim]")
        raise typer.Exit(1)

    if a.name == b.name:
        console.print("[yellow]Cannot compare a project with itself.[/yellow]")
        raise typer.Exit(1)

    if format == "json":
        import json as json_mod

        def _proj_summary(p: Project) -> dict:
            return {
                "name": p.name,
                "path": p.path,
                "health": {
                    "grade": p.health.grade,
                    "percent": p.health.percent,
                    "tests": round(p.health.tests, 2),
                    "git_hygiene": round(p.health.git_hygiene, 2),
                    "documentation": round(p.health.documentation, 2),
                    "structure": round(p.health.structure, 2),
                },
                "loc": p.loc,
                "source_files": p.source_file_count,
                "test_files": p.test_file_count,
                "commits": p.git_info.total_commits,
                "languages": dict(p.tech_stack.languages),
                "frameworks": p.tech_stack.frameworks,
                "license": p.license,
            }

        fw_a = set(a.tech_stack.frameworks)
        fw_b = set(b.tech_stack.frameworks)
        deps_a = set(a.tech_stack.key_deps.keys())
        deps_b = set(b.tech_stack.key_deps.keys())

        data = {
            "project_a": _proj_summary(a),
            "project_b": _proj_summary(b),
            "deltas": {
                "health_percent": a.health.percent - b.health.percent,
                "loc": a.loc - b.loc,
                "source_files": a.source_file_count - b.source_file_count,
                "test_files": a.test_file_count - b.test_file_count,
                "commits": a.git_info.total_commits - b.git_info.total_commits,
            },
            "shared_frameworks": sorted(fw_a & fw_b),
            "unique_frameworks_a": sorted(fw_a - fw_b),
            "unique_frameworks_b": sorted(fw_b - fw_a),
            "shared_deps": sorted(deps_a & deps_b),
        }
        console.print(json_mod.dumps(data, indent=2))
        return

    if format == "csv":
        import csv as csv_mod
        import io
        buf = io.StringIO()
        writer = csv_mod.writer(buf)
        writer.writerow(["Metric", a.name, b.name, "Delta"])
        writer.writerow(["Grade", a.health.grade, b.health.grade, ""])
        writer.writerow(["Health%", a.health.percent, b.health.percent, a.health.percent - b.health.percent])
        writer.writerow(["Tests%", round(a.health.tests * 100), round(b.health.tests * 100), round(a.health.tests * 100) - round(b.health.tests * 100)])
        writer.writerow(["Git%", round(a.health.git_hygiene * 100), round(b.health.git_hygiene * 100), round(a.health.git_hygiene * 100) - round(b.health.git_hygiene * 100)])
        writer.writerow(["Docs%", round(a.health.documentation * 100), round(b.health.documentation * 100), round(a.health.documentation * 100) - round(b.health.documentation * 100)])
        writer.writerow(["Structure%", round(a.health.structure * 100), round(b.health.structure * 100), round(a.health.structure * 100) - round(b.health.structure * 100)])
        writer.writerow(["LOC", a.loc, b.loc, a.loc - b.loc])
        writer.writerow(["Source Files", a.source_file_count, b.source_file_count, a.source_file_count - b.source_file_count])
        writer.writerow(["Test Files", a.test_file_count, b.test_file_count, a.test_file_count - b.test_file_count])
        writer.writerow(["Commits", a.git_info.total_commits, b.git_info.total_commits, a.git_info.total_commits - b.git_info.total_commits])
        writer.writerow(["Languages", "; ".join(a.tech_stack.primary_languages), "; ".join(b.tech_stack.primary_languages), ""])
        writer.writerow(["Frameworks", "; ".join(a.tech_stack.frameworks), "; ".join(b.tech_stack.frameworks), ""])
        writer.writerow(["License", a.license, b.license, ""])
        print(buf.getvalue(), end="")
        return

    show_comparison(a, b)


@app.command(name="batch-add")
def batch_add(
    directory: str = typer.Argument(help="Parent directory containing projects"),
    exclude: Optional[str] = typer.Option(None, help="Comma-separated project names to skip"),
):
    """Add all git repos in a directory."""
    portfolio = _load_portfolio()
    parent = Path(directory).expanduser().resolve()

    if not parent.is_dir():
        console.print(f"[red]Directory not found: {parent}[/red]")
        raise typer.Exit(1)

    skip = set()
    if exclude:
        skip = {s.strip().lower() for s in exclude.split(",")}

    # Find all subdirs with .git
    candidates = []
    existing_paths = {p.path for p in portfolio.projects}
    for child in sorted(parent.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith(".") or child.name.startswith("_"):
            continue
        if child.name.lower() in skip:
            continue
        if (child / ".git").exists() and str(child.resolve()) not in existing_paths:
            candidates.append(child)

    if not candidates:
        console.print("[yellow]No new git repos found.[/yellow]")
        return

    console.print(f"\n  Found [bold]{len(candidates)}[/bold] new repos to add\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Adding projects...", total=len(candidates))

        for child in candidates:
            progress.update(task, description=f"Scanning [cyan]{child.name}[/cyan]...")
            project = scan_project(child)
            portfolio.projects.append(project)
            progress.advance(task)

    _save_portfolio(portfolio)
    console.print(f"\n  [green]\u2713[/green] Added [bold]{len(candidates)}[/bold] projects to portfolio")
    console.print("  Run [cyan]atlas status[/cyan] to see the dashboard\n")


@app.command()
def export(
    format: Optional[str] = typer.Option(None, help="Export format: markdown, json, csv (auto-detected from -o extension)"),
    output: Optional[str] = typer.Option(None, "-o", help="Output file path (.md/.json/.csv auto-detects format)"),
    grade: Optional[str] = typer.Option(None, help="Filter by health grade (A, B+, B, C, D, F)"),
    lang: Optional[str] = typer.Option(None, help="Filter by language (e.g. Python, TypeScript)"),
    has: Optional[str] = typer.Option(None, help="Filter by tech (e.g. Docker, FastAPI, pytest)"),
    min_health: Optional[int] = typer.Option(None, help="Filter projects with health >= N%"),
    max_health: Optional[int] = typer.Option(None, help="Filter projects with health <= N%"),
    sort: Optional[str] = typer.Option(None, "--sort", help="Sort by: name, health, loc"),
    limit: Optional[int] = typer.Option(None, "--limit", "-n", help="Limit number of projects in output"),
):
    """Export portfolio report."""
    portfolio = _load_portfolio()

    # Apply filters
    filtered = portfolio.projects
    if grade:
        grade_upper = grade.upper()
        filtered = [p for p in filtered if p.health.grade == grade_upper]
    if lang:
        lang_lower = lang.lower()
        filtered = [p for p in filtered
                    if any(name.lower() == lang_lower for name in p.tech_stack.languages)]
    if has:
        has_lower = has.lower()
        filtered = [p for p in filtered if _project_has_tech(p, has_lower)]
    if min_health is not None:
        filtered = [p for p in filtered if p.health.percent >= min_health]
    if max_health is not None:
        filtered = [p for p in filtered if p.health.percent <= max_health]

    if sort:
        sort_lower = sort.lower()
        if sort_lower == "name":
            filtered.sort(key=lambda p: p.name.lower())
        elif sort_lower == "health":
            filtered.sort(key=lambda p: p.health.overall, reverse=True)
        elif sort_lower == "loc":
            filtered.sort(key=lambda p: p.loc, reverse=True)

    if limit is not None and limit > 0:
        filtered = filtered[:limit]

    if len(filtered) != len(portfolio.projects) or sort or limit:
        portfolio = Portfolio(
            name=portfolio.name,
            projects=filtered,
            created=portfolio.created,
            last_scan=portfolio.last_scan,
        )

    # Auto-detect format from output file extension
    ext_map = {".json": "json", ".csv": "csv", ".md": "markdown"}
    if format is None:
        if output:
            ext = Path(output).suffix.lower()
            format = ext_map.get(ext, "markdown")
        else:
            format = "markdown"

    if format == "json":
        content = build_json_report(portfolio)
    elif format == "csv":
        content = build_csv_report(portfolio)
    else:
        content = build_markdown_report(portfolio)

    if output:
        Path(output).write_text(content)
        console.print(f"  [green]\u2713[/green] Exported to [bold]{output}[/bold] ({format})")
    elif format in ("json", "csv"):
        print(content)
    else:
        console.print(content)


@app.command()
def support():
    """Show how to support this project."""
    console.print()
    console.print("  [bold]Atlas is 100% free and open source (MIT).[/bold]")
    console.print()
    console.print("  If atlas saves you time, consider supporting development:")
    console.print()
    console.print("    [cyan]https://github.com/sponsors/nxtg-ai[/cyan]")
    console.print()
    console.print("  Supporters get:")
    console.print("    [green]\u2713[/green] Name in SUPPORTERS.md")
    console.print("    [green]\u2713[/green] Priority GitHub issues")
    console.print("    [green]\u2713[/green] Early access to new features")
    console.print("    [green]\u2713[/green] The good feeling of funding open source")
    console.print()


@app.command()
def config(
    key: Optional[str] = typer.Argument(None, help="Config key to get (e.g. ci.min_health)"),
    set_val: Optional[str] = typer.Option(None, "--set", help="Value to set"),
):
    """View or update configuration."""
    if key is None:
        # Show all config
        cfg = load_config()
        console.print()
        console.print("  [bold]Atlas Configuration[/bold]")
        console.print()
        for section, values in sorted(cfg.items()):
            console.print(f"  [cyan][{section}][/cyan]")
            for k, v in sorted(values.items()):
                console.print(f"    {k} = [bold]{v}[/bold]")
        console.print()
        console.print("  [dim]Config file: ~/.atlas/config.toml[/dim]")
        console.print(f"  [dim]Valid keys: {', '.join(valid_keys())}[/dim]")
        console.print()
        return

    if set_val is not None:
        # Set a value
        if set_value(key, set_val):
            console.print(f"  [green]\u2713[/green] Set [bold]{key}[/bold] = {set_val}")
        else:
            console.print("  [red]Invalid key or value.[/red]")
            console.print(f"  [dim]Valid keys: {', '.join(valid_keys())}[/dim]")
            raise typer.Exit(1)
    else:
        # Get a value
        val = get_value(key)
        if val is not None:
            console.print(f"  {key} = [bold]{val}[/bold]")
        else:
            console.print(f"  [red]Unknown key: {key}[/red]")
            console.print(f"  [dim]Valid keys: {', '.join(valid_keys())}[/dim]")
            raise typer.Exit(1)


@app.command()
def license():
    """Show current license status."""
    status = get_license_status()
    console.print()
    console.print(f"  [bold]Tier:[/bold] {status['tier']}")
    console.print(f"  [bold]Project limit:[/bold] {status['project_limit']}")
    console.print(f"  [bold]Cross-project intelligence:[/bold] {'Yes' if status['cross_project'] else 'Pro only'}")
    console.print(f"  [bold]Export:[/bold] {'Yes' if status['export'] else 'Pro only'}")
    console.print(f"  [bold]Batch add:[/bold] {'Yes' if status['batch_add'] else 'Pro only'}")
    console.print()
    if status["tier"] == "Free":
        console.print("  [dim]Activate Pro: atlas activate <key>[/dim]")
        console.print()


@app.command()
def activate(key: str = typer.Argument(help="Pro license key (ATLAS-XXXX-XXXX-XXXX-XXXX)")):
    """Activate a Pro license."""
    if activate_license(key):
        console.print()
        console.print("  [green]\u2713[/green] [bold]Pro license activated![/bold]")
        console.print("  Unlimited projects, cross-project intelligence, export, batch-add.")
        console.print()
    else:
        console.print()
        console.print("  [red]\u2717[/red] Invalid license key.")
        console.print("  [dim]Format: ATLAS-XXXX-XXXX-XXXX-XXXX[/dim]")
        console.print()
        raise typer.Exit(1)


@app.command()
def badge(
    output: Optional[str] = typer.Option(None, "-o", help="Output file path"),
):
    """Generate markdown badges for your portfolio README."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects scanned yet. Run `atlas scan` first.[/yellow]")
        raise typer.Exit(1)

    badges = generate_badges(portfolio)
    content = "\n".join(badges)

    if output:
        Path(output).write_text(content + "\n")
        console.print(f"  [green]\u2713[/green] Badges exported to [bold]{output}[/bold]")
    else:
        console.print()
        for line in badges:
            console.print(f"  {line}")
        console.print()
        console.print("  [dim]Copy the lines above into your README.md[/dim]")


def generate_badges(portfolio: Portfolio) -> list[str]:
    """Generate shields.io-style markdown badge strings for a portfolio."""
    badges: list[str] = []

    # Health grade badge
    grade = portfolio.avg_grade
    pct = int(portfolio.avg_health * 100)
    grade_colors = {"A": "brightgreen", "B+": "green", "B": "blue",
                    "C": "yellow", "D": "orange", "F": "red"}
    color = grade_colors.get(grade, "lightgrey")
    badges.append(
        f"![Health](https://img.shields.io/badge/health-{grade}%20({pct}%25)-{color})"
    )

    # Projects count
    n = len(portfolio.projects)
    badges.append(
        f"![Projects](https://img.shields.io/badge/projects-{n}-blue)"
    )

    # Test files count
    tests = portfolio.total_tests
    test_color = "brightgreen" if tests > 50 else "green" if tests > 10 else "yellow" if tests > 0 else "red"
    badges.append(
        f"![Tests](https://img.shields.io/badge/test%20files-{tests:,}-{test_color})"
    )

    # LOC
    loc = portfolio.total_loc
    if loc >= 1_000_000:
        loc_label = f"{loc / 1_000_000:.1f}M"
    elif loc >= 1_000:
        loc_label = f"{loc / 1_000:.1f}K"
    else:
        loc_label = str(loc)
    badges.append(
        f"![LOC](https://img.shields.io/badge/LOC-{loc_label}-informational)"
    )

    # Top languages
    from collections import Counter
    lang_counter: Counter[str] = Counter()
    for p in portfolio.projects:
        for lang in p.tech_stack.primary_languages:
            lang_counter[lang] += 1
    if lang_counter:
        top_lang = lang_counter.most_common(1)[0][0]
        badges.append(
            f"![Language](https://img.shields.io/badge/primary-{top_lang}-blueviolet)"
        )

    return badges


@app.command()
def top(
    n: int = typer.Option(5, "--limit", "-n", help="Number of projects to show"),
    by: str = typer.Option("health", help="Sort by: health, loc, tests, commits"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format: json or csv"),
    lang: Optional[str] = typer.Option(None, help="Filter by language (e.g. Python, TypeScript)"),
    has: Optional[str] = typer.Option(None, help="Filter by tech (e.g. Docker, FastAPI, pytest)"),
):
    """Show top projects by a metric."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    candidates = portfolio.projects
    if lang:
        lang_lower = lang.lower()
        candidates = [p for p in candidates
                      if any(name.lower() == lang_lower for name in p.tech_stack.languages)]
    if has:
        has_lower = has.lower()
        candidates = [p for p in candidates if _project_has_tech(p, has_lower)]

    if not candidates:
        console.print("[yellow]No projects match the filters.[/yellow]")
        return

    sort_keys = {
        "health": lambda p: p.health.overall,
        "loc": lambda p: p.loc,
        "tests": lambda p: p.test_file_count,
        "commits": lambda p: p.git_info.total_commits,
    }

    if by not in sort_keys:
        valid = ", ".join(sorted(sort_keys))
        console.print(f"[red]Unknown metric '{by}'. Valid: {valid}[/red]")
        raise typer.Exit(1)

    projects = sorted(candidates, key=sort_keys[by], reverse=True)[:n]

    if format == "json":
        import json as json_mod
        metric_fns = {
            "health": lambda p: p.health.percent,
            "loc": lambda p: p.loc,
            "tests": lambda p: p.test_file_count,
            "commits": lambda p: p.git_info.total_commits,
        }
        data = {
            "metric": by,
            "limit": n,
            "projects": [
                {
                    "rank": i,
                    "name": p.name,
                    "value": metric_fns[by](p),
                    "health_grade": p.health.grade,
                    "stack": p.tech_stack.summary,
                }
                for i, p in enumerate(projects, 1)
            ],
        }
        console.print(json_mod.dumps(data, indent=2))
        return

    if format == "csv":
        import csv as csv_mod
        import io
        metric_fns_csv = {
            "health": lambda p: p.health.percent,
            "loc": lambda p: p.loc,
            "tests": lambda p: p.test_file_count,
            "commits": lambda p: p.git_info.total_commits,
        }
        buf = io.StringIO()
        writer = csv_mod.writer(buf)
        writer.writerow(["Rank", "Name", by.capitalize(), "Grade", "Stack"])
        for i, p in enumerate(projects, 1):
            writer.writerow([i, p.name, metric_fns_csv[by](p), p.health.grade, p.tech_stack.summary])
        print(buf.getvalue(), end="")
        return

    console.print()
    console.print(f"  [bold]Top {len(projects)} by {by}[/bold]")
    console.print()

    for i, p in enumerate(projects, 1):
        grade_color = {"A": "green", "B+": "green", "B": "cyan", "C": "yellow", "D": "red", "F": "bold red"}.get(p.health.grade, "white")
        if by == "health":
            metric = f"[{grade_color}]{p.health.grade} ({p.health.percent}%)[/{grade_color}]"
        elif by == "loc":
            metric = f"{p.loc:,} LOC"
        elif by == "tests":
            metric = f"{p.test_file_count:,} test files"
        else:
            metric = f"{p.git_info.total_commits:,} commits"
        console.print(f"  {i:>2}. [bold]{p.name}[/bold]  {metric}  [dim]{p.tech_stack.summary}[/dim]")

    console.print()


@app.command()
def version():
    """Show the installed atlas version."""
    try:
        from importlib.metadata import version as pkg_version
        ver = pkg_version("nxtg-atlas")
    except Exception:
        ver = "dev"
    console.print(f"atlas {ver}")


@app.command()
def reset():
    """Reset the portfolio (delete all data)."""
    if DEFAULT_PORTFOLIO_FILE.exists():
        confirm = typer.confirm("Delete portfolio and all data?")
        if confirm:
            DEFAULT_PORTFOLIO_FILE.unlink()
            console.print("[green]\u2713[/green] Portfolio reset.")
        else:
            console.print("[dim]Cancelled.[/dim]")
    else:
        console.print("[dim]No portfolio to reset.[/dim]")


if __name__ == "__main__":
    app()
