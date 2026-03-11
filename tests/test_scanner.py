"""Tests for the project scanner."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from atlas.models import GitInfo
from atlas.scanner import _get_git_info, scan_project


# ---------------------------------------------------------------------------
# scan_project
# ---------------------------------------------------------------------------
class TestScanProject:
    def test_scan_python_project(self, tmp_project):
        project = scan_project(tmp_project)
        assert project.name == "test-project"
        assert project.source_file_count >= 4
        assert project.test_file_count >= 2
        assert "Python" in project.tech_stack.languages
        assert "FastAPI" in project.tech_stack.frameworks
        assert project.health.grade in ("A", "B+", "B", "C")
        assert project.loc > 0

    def test_scan_js_project(self, tmp_js_project):
        project = scan_project(tmp_js_project)
        assert project.name == "js-project"
        assert "TypeScript" in project.tech_stack.languages
        assert "Next.js" in project.tech_stack.frameworks
        assert project.test_file_count >= 1

    def test_scan_empty_dir(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        project = scan_project(proj)
        assert project.name == "empty"
        assert project.source_file_count == 0
        assert project.health.grade in ("D", "F")

    def test_path_is_resolved(self, tmp_project):
        project = scan_project(tmp_project)
        assert project.path == str(tmp_project.resolve())

    def test_health_is_computed(self, tmp_project):
        project = scan_project(tmp_project)
        assert project.health.overall > 0
        assert project.health.grade != ""

    def test_tech_stack_populated(self, tmp_project):
        project = scan_project(tmp_project)
        assert project.tech_stack.languages != {}
        assert len(project.tech_stack.frameworks) > 0

    def test_scan_rust_project(self, tmp_path):
        proj = tmp_path / "rust-app"
        proj.mkdir()
        (proj / "Cargo.toml").write_text('[package]\nname = "myapp"\n[dependencies]\ntokio = "1.0"\n')
        src = proj / "src"
        src.mkdir()
        (src / "main.rs").write_text('fn main() { println!("hello"); }\n')
        project = scan_project(proj)
        assert "Rust" in project.tech_stack.languages
        assert "Rust" in project.tech_stack.frameworks

    def test_scan_monorepo_like(self, tmp_path):
        proj = tmp_path / "monorepo"
        proj.mkdir()
        # Backend
        backend = proj / "server"
        backend.mkdir()
        (backend / "app.py").write_text("from fastapi import FastAPI\n")
        # Frontend
        frontend = proj / "client"
        frontend.mkdir()
        (frontend / "index.tsx").write_text("export default function App() {}")
        project = scan_project(proj)
        assert "Python" in project.tech_stack.languages
        assert "TypeScript" in project.tech_stack.languages

    def test_total_file_count_gte_source(self, tmp_project):
        project = scan_project(tmp_project)
        assert project.total_file_count >= project.source_file_count

    def test_git_info_populated(self, tmp_project):
        project = scan_project(tmp_project)
        assert isinstance(project.git_info, GitInfo)


# ---------------------------------------------------------------------------
# _get_git_info
# ---------------------------------------------------------------------------
class TestGetGitInfo:
    def test_no_git_dir(self, tmp_path):
        proj = tmp_path / "nogit"
        proj.mkdir()
        info = _get_git_info(proj)
        assert info.branch == ""
        assert info.total_commits == 0
        assert info.has_remote is False

    def test_with_git_dir_but_no_git_binary(self, tmp_path):
        proj = tmp_path / "fakegit"
        proj.mkdir()
        (proj / ".git").mkdir()
        with patch("atlas.scanner.subprocess.run", side_effect=FileNotFoundError):
            info = _get_git_info(proj)
        assert info.branch == "detached"
        assert info.total_commits == 0

    def test_detached_head(self, tmp_path):
        proj = tmp_path / "detached"
        proj.mkdir()
        (proj / ".git").mkdir()
        with patch("atlas.scanner.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = ""
            info = _get_git_info(proj)
        assert info.branch == "detached"

    def test_commit_count_non_digit(self, tmp_path):
        proj = tmp_path / "bad"
        proj.mkdir()
        (proj / ".git").mkdir()
        returns = ["main", "", "not-a-number", "", ""]
        call_count = [0]

        def fake_run(*args, **kwargs):
            class R:
                returncode = 0
                stdout = returns[min(call_count[0], len(returns) - 1)]
            call_count[0] += 1
            return R()

        with patch("atlas.scanner.subprocess.run", side_effect=fake_run):
            info = _get_git_info(proj)
        assert info.total_commits == 0
