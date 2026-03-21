"""Tests for scan history and trends tracking."""
from __future__ import annotations

from unittest.mock import patch

import pytest

from atlas.history import (
    MAX_ENTRIES,
    ProjectSnapshot,
    ScanEntry,
    build_scan_entry,
    compute_trends,
    load_history,
    save_scan,
)
from atlas.models import GitInfo, HealthScore, Portfolio, Project, TechStack


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_snapshot(name: str = "proj", health: float = 0.8, grade: str = "B+",
                   tests: int = 5, loc: int = 1000) -> ProjectSnapshot:
    return ProjectSnapshot(name=name, health=health, grade=grade, tests=tests, loc=loc)


def _make_entry(
    health: float = 0.8,
    grade: str = "B+",
    projects: list[ProjectSnapshot] | None = None,
    timestamp: str = "2026-03-13T00:00:00+00:00",
    total_projects: int = 1,
    total_tests: int = 5,
    total_loc: int = 1000,
) -> ScanEntry:
    return ScanEntry(
        timestamp=timestamp,
        portfolio_health=health,
        portfolio_grade=grade,
        total_projects=total_projects,
        total_tests=total_tests,
        total_loc=total_loc,
        projects=projects or [_make_snapshot()],
    )


def _make_project(name: str = "proj", path: str = "/tmp/proj") -> Project:
    hs = HealthScore(tests=0.8, git_hygiene=0.9, documentation=0.7, structure=0.8)
    hs.compute()
    return Project(
        name=name,
        path=path,
        tech_stack=TechStack(languages={"Python": 10}),
        git_info=GitInfo(branch="main", total_commits=50, has_remote=True),
        health=hs,
        test_file_count=5,
        source_file_count=20,
        total_file_count=30,
        loc=1000,
    )


# ===========================================================================
# ProjectSnapshot / ScanEntry dataclasses
# ===========================================================================


class TestDataclasses:
    def test_project_snapshot_fields(self):
        snap = _make_snapshot("alpha", 0.95, "A", 10, 2000)
        assert snap.name == "alpha"
        assert snap.health == 0.95
        assert snap.grade == "A"
        assert snap.tests == 10
        assert snap.loc == 2000

    def test_scan_entry_defaults(self):
        entry = ScanEntry(
            timestamp="t", portfolio_health=0.5, portfolio_grade="C",
            total_projects=1, total_tests=3, total_loc=500,
        )
        assert entry.projects == []

    def test_scan_entry_with_projects(self):
        snaps = [_make_snapshot("a"), _make_snapshot("b")]
        entry = _make_entry(projects=snaps)
        assert len(entry.projects) == 2
        assert entry.projects[0].name == "a"


# ===========================================================================
# save_scan / load_history
# ===========================================================================


class TestSaveLoad:
    def test_save_and_load(self, tmp_path):
        hfile = tmp_path / "history.json"
        with patch("atlas.history.HISTORY_FILE", hfile):
            entry = _make_entry()
            save_scan(entry)
            entries = load_history()
        assert len(entries) == 1
        assert entries[0].portfolio_health == 0.8
        assert entries[0].portfolio_grade == "B+"
        assert len(entries[0].projects) == 1
        assert entries[0].projects[0].name == "proj"

    def test_load_empty(self, tmp_path):
        hfile = tmp_path / "history.json"
        with patch("atlas.history.HISTORY_FILE", hfile):
            entries = load_history()
        assert entries == []

    def test_load_corrupt_json(self, tmp_path):
        hfile = tmp_path / "history.json"
        hfile.write_text("not valid json{{{")
        with patch("atlas.history.HISTORY_FILE", hfile):
            entries = load_history()
        assert entries == []

    def test_save_multiple(self, tmp_path):
        hfile = tmp_path / "history.json"
        with patch("atlas.history.HISTORY_FILE", hfile):
            save_scan(_make_entry(health=0.7, timestamp="2026-03-01T00:00:00+00:00"))
            save_scan(_make_entry(health=0.8, timestamp="2026-03-02T00:00:00+00:00"))
            save_scan(_make_entry(health=0.9, timestamp="2026-03-03T00:00:00+00:00"))
            entries = load_history()
        assert len(entries) == 3
        assert entries[0].portfolio_health == 0.7
        assert entries[2].portfolio_health == 0.9

    def test_max_entries_cap(self, tmp_path):
        hfile = tmp_path / "history.json"
        with patch("atlas.history.HISTORY_FILE", hfile):
            for i in range(MAX_ENTRIES + 10):
                save_scan(_make_entry(health=i / 200, timestamp=f"2026-03-{i:03d}"))
            entries = load_history()
        assert len(entries) == MAX_ENTRIES

    def test_save_creates_parent_dirs(self, tmp_path):
        hfile = tmp_path / "deep" / "nested" / "history.json"
        with patch("atlas.history.HISTORY_FILE", hfile):
            save_scan(_make_entry())
        assert hfile.exists()

    def test_roundtrip_preserves_projects(self, tmp_path):
        hfile = tmp_path / "history.json"
        snaps = [
            _make_snapshot("alpha", 0.9, "A", 10, 5000),
            _make_snapshot("beta", 0.6, "C", 2, 300),
        ]
        entry = _make_entry(projects=snaps, total_projects=2)
        with patch("atlas.history.HISTORY_FILE", hfile):
            save_scan(entry)
            loaded = load_history()
        assert len(loaded[0].projects) == 2
        assert loaded[0].projects[0].name == "alpha"
        assert loaded[0].projects[1].health == 0.6


# ===========================================================================
# build_scan_entry
# ===========================================================================


class TestBuildScanEntry:
    def test_build_from_portfolio(self):
        p1 = _make_project("proj-a", "/tmp/a")
        p2 = _make_project("proj-b", "/tmp/b")
        portfolio = Portfolio(name="Test", created="2026-01-01", projects=[p1, p2])
        entry = build_scan_entry(portfolio)
        assert entry.total_projects == 2
        assert entry.total_tests == 10  # 5 + 5
        assert entry.total_loc == 2000  # 1000 + 1000
        assert len(entry.projects) == 2
        assert entry.projects[0].name == "proj-a"
        assert entry.timestamp  # non-empty

    def test_build_empty_portfolio(self):
        portfolio = Portfolio(name="Empty", created="2026-01-01", projects=[])
        entry = build_scan_entry(portfolio)
        assert entry.total_projects == 0
        assert entry.projects == []


# ===========================================================================
# compute_trends
# ===========================================================================


class TestComputeTrends:
    def test_less_than_two_entries(self):
        assert compute_trends([]) == []
        assert compute_trends([_make_entry()]) == []

    def test_stable_project(self):
        prev = _make_entry(projects=[_make_snapshot("a", 0.8)])
        curr = _make_entry(projects=[_make_snapshot("a", 0.8)])
        trends = compute_trends([prev, curr])
        assert len(trends) == 1
        assert trends[0]["direction"] == "stable"
        assert trends[0]["name"] == "a"

    def test_improving_project(self):
        prev = _make_entry(projects=[_make_snapshot("a", 0.6)])
        curr = _make_entry(projects=[_make_snapshot("a", 0.9)])
        trends = compute_trends([prev, curr])
        assert trends[0]["direction"] == "up"
        assert trends[0]["delta"] == pytest.approx(0.3)

    def test_declining_project(self):
        prev = _make_entry(projects=[_make_snapshot("a", 0.9)])
        curr = _make_entry(projects=[_make_snapshot("a", 0.6)])
        trends = compute_trends([prev, curr])
        assert trends[0]["direction"] == "down"
        assert trends[0]["delta"] == pytest.approx(-0.3)

    def test_new_project(self):
        prev = _make_entry(projects=[_make_snapshot("a", 0.8)])
        curr = _make_entry(projects=[_make_snapshot("a", 0.8), _make_snapshot("b", 0.7)])
        trends = compute_trends([prev, curr])
        new = [t for t in trends if t["direction"] == "new"]
        assert len(new) == 1
        assert new[0]["name"] == "b"
        assert new[0]["previous"] is None

    def test_removed_project(self):
        prev = _make_entry(projects=[_make_snapshot("a", 0.8), _make_snapshot("b", 0.7)])
        curr = _make_entry(projects=[_make_snapshot("a", 0.8)])
        trends = compute_trends([prev, curr])
        removed = [t for t in trends if t["direction"] == "removed"]
        assert len(removed) == 1
        assert removed[0]["name"] == "b"
        assert removed[0]["current"] is None

    def test_uses_last_two_entries(self):
        e1 = _make_entry(projects=[_make_snapshot("a", 0.5)])
        e2 = _make_entry(projects=[_make_snapshot("a", 0.7)])
        e3 = _make_entry(projects=[_make_snapshot("a", 0.9)])
        trends = compute_trends([e1, e2, e3])
        # Should compare e3 vs e2, not e1
        assert trends[0]["delta"] == pytest.approx(0.2)
        assert trends[0]["previous"] == 0.7

    def test_small_delta_is_stable(self):
        prev = _make_entry(projects=[_make_snapshot("a", 0.800)])
        curr = _make_entry(projects=[_make_snapshot("a", 0.804)])
        trends = compute_trends([prev, curr])
        assert trends[0]["direction"] == "stable"

    def test_multiple_projects_mixed(self):
        prev = _make_entry(projects=[
            _make_snapshot("up", 0.5),
            _make_snapshot("down", 0.9),
            _make_snapshot("same", 0.7),
        ])
        curr = _make_entry(projects=[
            _make_snapshot("up", 0.8),
            _make_snapshot("down", 0.6),
            _make_snapshot("same", 0.7),
        ])
        trends = compute_trends([prev, curr])
        by_name = {t["name"]: t for t in trends}
        assert by_name["up"]["direction"] == "up"
        assert by_name["down"]["direction"] == "down"
        assert by_name["same"]["direction"] == "stable"
