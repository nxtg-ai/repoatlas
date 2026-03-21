"""Scan history — tracks portfolio health over time."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

HISTORY_FILE = Path.home() / ".atlas" / "history.json"
MAX_ENTRIES = 100


@dataclass
class ProjectSnapshot:
    name: str
    health: float
    grade: str
    tests: int
    loc: int


@dataclass
class ScanEntry:
    timestamp: str
    portfolio_health: float
    portfolio_grade: str
    total_projects: int
    total_tests: int
    total_loc: int
    projects: list[ProjectSnapshot] = field(default_factory=list)


def save_scan(entry: ScanEntry) -> None:
    """Append a scan entry to history."""
    entries = load_history()
    entries.append(entry)
    # Keep only the most recent entries
    if len(entries) > MAX_ENTRIES:
        entries = entries[-MAX_ENTRIES:]
    _write_history(entries)


def load_history() -> list[ScanEntry]:
    """Load scan history from disk."""
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text())
        return [_entry_from_dict(d) for d in data]
    except (json.JSONDecodeError, KeyError):
        return []


def build_scan_entry(portfolio: "Portfolio") -> ScanEntry:  # noqa: F821
    """Build a ScanEntry from a Portfolio object."""
    projects = [
        ProjectSnapshot(
            name=p.name,
            health=p.health.overall,
            grade=p.health.grade,
            tests=p.test_file_count,
            loc=p.loc,
        )
        for p in portfolio.projects
    ]

    return ScanEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        portfolio_health=portfolio.avg_health,
        portfolio_grade=portfolio.avg_grade,
        total_projects=len(portfolio.projects),
        total_tests=portfolio.total_tests,
        total_loc=portfolio.total_loc,
        projects=projects,
    )


def compute_trends(entries: list[ScanEntry]) -> list[dict]:
    """Compute per-project health trends from history.

    Returns a list of dicts: {name, current, previous, delta, direction}
    """
    if len(entries) < 2:
        return []

    current = entries[-1]
    previous = entries[-2]

    prev_map = {p.name: p for p in previous.projects}
    trends = []

    for proj in current.projects:
        prev = prev_map.get(proj.name)
        if prev is None:
            trends.append({
                "name": proj.name,
                "current": proj.health,
                "previous": None,
                "delta": None,
                "direction": "new",
            })
        else:
            delta = proj.health - prev.health
            if abs(delta) < 0.005:
                direction = "stable"
            elif delta > 0:
                direction = "up"
            else:
                direction = "down"
            trends.append({
                "name": proj.name,
                "current": proj.health,
                "previous": prev.health,
                "delta": delta,
                "direction": direction,
            })

    # Flag removed projects
    current_names = {p.name for p in current.projects}
    for prev_proj in previous.projects:
        if prev_proj.name not in current_names:
            trends.append({
                "name": prev_proj.name,
                "current": None,
                "previous": prev_proj.health,
                "delta": None,
                "direction": "removed",
            })

    return trends


def _write_history(entries: list[ScanEntry]) -> None:
    """Write entries to history file."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = [_entry_to_dict(e) for e in entries]
    HISTORY_FILE.write_text(json.dumps(data, indent=2))


def _entry_to_dict(entry: ScanEntry) -> dict:
    return {
        "timestamp": entry.timestamp,
        "portfolio_health": entry.portfolio_health,
        "portfolio_grade": entry.portfolio_grade,
        "total_projects": entry.total_projects,
        "total_tests": entry.total_tests,
        "total_loc": entry.total_loc,
        "projects": [asdict(p) for p in entry.projects],
    }


def _entry_from_dict(data: dict) -> ScanEntry:
    return ScanEntry(
        timestamp=data["timestamp"],
        portfolio_health=data["portfolio_health"],
        portfolio_grade=data["portfolio_grade"],
        total_projects=data["total_projects"],
        total_tests=data["total_tests"],
        total_loc=data["total_loc"],
        projects=[
            ProjectSnapshot(**p) for p in data.get("projects", [])
        ],
    )
