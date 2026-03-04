"""Tests for the project scanner."""
from atlas.scanner import scan_project


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
