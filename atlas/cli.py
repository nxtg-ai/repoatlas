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
from atlas.display import console, show_comparison, show_connections, show_project_card, show_scan_complete, show_status
from atlas.export_report import build_json_report, build_markdown_report
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
):
    """Display the portfolio dashboard."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    filtered = portfolio.projects
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
        console.print(f"[yellow]No projects match filters: {', '.join(active_filters)}[/yellow]")
        return

    if active_filters:
        view = Portfolio(
            name=portfolio.name,
            projects=filtered,
            created=portfolio.created,
            last_scan=portfolio.last_scan,
        )
        console.print(f"  [dim]Filtered: {', '.join(active_filters)} ({len(filtered)}/{len(portfolio.projects)} projects)[/dim]")
        show_status(view)
    else:
        show_status(portfolio)

    # Cross-project intelligence
    display_projects = filtered if active_filters else portfolio.projects
    if len(display_projects) > 1:
        conns = find_connections(display_projects)
        if conns:
            console.print()
            show_connections(conns)


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
    )
    return any(term == item.lower() for item in all_items)


@app.command()
def connections():
    """Show cross-project intelligence."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    conns = find_connections(portfolio.projects)
    console.print()
    show_connections(conns)


@app.command()
def doctor():
    """Diagnose portfolio health and suggest fixes."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    recs = generate_recommendations(portfolio)

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
    counts = {}
    for rec in recs:
        counts[rec.priority] = counts.get(rec.priority, 0) + 1
    parts = []
    for p in ("critical", "high", "medium", "low"):
        if p in counts:
            parts.append(f"{counts[p]} {p}")
    console.print()
    console.print(f"  [dim]Summary: {', '.join(parts)}[/dim]")
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
    format: str = typer.Option("markdown", help="Export format: markdown, json"),
    output: Optional[str] = typer.Option(None, "-o", help="Output file path"),
):
    """Export portfolio report."""
    portfolio = _load_portfolio()

    if format == "json":
        content = build_json_report(portfolio)
    else:
        content = build_markdown_report(portfolio)

    if output:
        Path(output).write_text(content)
        console.print(f"  [green]\u2713[/green] Exported to [bold]{output}[/bold]")
    elif format == "json":
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
