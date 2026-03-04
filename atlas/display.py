"""Rich terminal display — the visual wow factor."""
from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.tree import Tree
from rich import box

from atlas.models import Connection, Portfolio, Project

console = Console()

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
}


def show_status(portfolio: Portfolio):
    """Display the full portfolio dashboard."""
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

        table.add_row(icon, proj.name, health_str, tests_str, loc_str, tech, branch, commits)

    console.print(table)


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
    }

    lines = []
    for conn_type, conns in groups.items():
        label = type_labels.get(conn_type, conn_type)
        icon = CONNECTION_ICONS.get(conn_type, " ")
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
    lines.append(f"  [bold]Health Breakdown:[/bold]")
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


def _health_icon(score: float) -> str:
    if score >= 0.76:
        return "[green]\u25cf[/green]"
    elif score >= 0.60:
        return "[yellow]\u25cf[/yellow]"
    elif score >= 0.40:
        return "[red]\u25cf[/red]"
    else:
        return "[dim red]\u25cf[/dim red]"


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
