"""CLI commands — the user-facing interface."""
from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from atlas.connections import find_connections
from atlas.display import console, show_connections, show_project_card, show_scan_complete, show_status
from atlas.models import Portfolio
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

    elapsed = time.time() - start
    show_scan_complete(portfolio, elapsed)


@app.command()
def status():
    """Display the portfolio dashboard."""
    portfolio = _load_portfolio()

    if not portfolio.projects:
        console.print("[yellow]No projects in portfolio.[/yellow]")
        return

    show_status(portfolio)

    # Cross-project intelligence
    if len(portfolio.projects) > 1:
        conns = find_connections(portfolio.projects)
        if conns:
            console.print()
            show_connections(conns)


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
    console.print(f"  Run [cyan]atlas status[/cyan] to see the dashboard\n")


@app.command()
def export(
    format: str = typer.Option("markdown", help="Export format: markdown, json"),
    output: Optional[str] = typer.Option(None, "-o", help="Output file path"),
):
    """Export portfolio report."""
    portfolio = _load_portfolio()

    if format == "json":
        import json
        data = {
            "name": portfolio.name,
            "scanned": portfolio.last_scan,
            "summary": {
                "projects": len(portfolio.projects),
                "test_files": portfolio.total_tests,
                "loc": portfolio.total_loc,
                "health_grade": portfolio.avg_grade,
                "health_percent": int(portfolio.avg_health * 100),
            },
            "projects": [p.to_dict() for p in portfolio.projects],
        }
        content = json.dumps(data, indent=2)
    else:
        lines = [
            f"# {portfolio.name} — Portfolio Report",
            f"",
            f"**Scanned**: {portfolio.last_scan[:19] if portfolio.last_scan else 'Never'}",
            f"**Projects**: {len(portfolio.projects)} | "
            f"**Test Files**: {portfolio.total_tests:,} | "
            f"**LOC**: {portfolio.total_loc:,} | "
            f"**Health**: {portfolio.avg_grade} ({int(portfolio.avg_health * 100)}%)",
            f"",
            f"| Project | Health | Tests | LOC | Stack |",
            f"|---------|--------|-------|-----|-------|",
        ]
        for p in sorted(portfolio.projects, key=lambda x: x.health.overall, reverse=True):
            lines.append(
                f"| {p.name} | {p.health.grade} ({p.health.percent}%) | "
                f"{p.test_file_count:,} | {p.loc:,} | {p.tech_stack.summary} |"
            )

        conns = find_connections(portfolio.projects)
        if conns:
            lines.append(f"\n## Cross-Project Intelligence\n")
            for conn in conns:
                icon = {"info": "i", "warning": "!", "critical": "X"}.get(conn.severity, "-")
                projs = ", ".join(conn.projects[:4])
                lines.append(f"- [{icon}] {conn.detail} ({projs})")

        content = "\n".join(lines)

    if output:
        Path(output).write_text(content)
        console.print(f"  [green]\u2713[/green] Exported to [bold]{output}[/bold]")
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
