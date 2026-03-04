"""Tests for tech stack detection."""
from atlas.detector import (
    count_files,
    count_test_files,
    detect_databases,
    detect_frameworks,
    detect_key_deps,
    detect_languages,
)


class TestDetectLanguages:
    def test_detects_python(self, tmp_project):
        langs = detect_languages(tmp_project)
        assert "Python" in langs
        assert langs["Python"] >= 4  # __init__.py, main.py, models.py, utils.py

    def test_detects_typescript(self, tmp_js_project):
        langs = detect_languages(tmp_js_project)
        assert "TypeScript" in langs

    def test_empty_dir(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_languages(proj) == {}


class TestCountFiles:
    def test_counts_source_files(self, tmp_project):
        source, total = count_files(tmp_project)
        assert source >= 4  # py files
        assert total >= source

    def test_empty_dir(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert count_files(proj) == (0, 0)


class TestCountTestFiles:
    def test_finds_test_files(self, tmp_project):
        count = count_test_files(tmp_project)
        assert count >= 2  # test_main.py, test_models.py

    def test_finds_spec_files(self, tmp_js_project):
        count = count_test_files(tmp_js_project)
        assert count >= 1  # page.test.tsx


class TestDetectFrameworks:
    def test_detects_python_frameworks(self, tmp_project):
        frameworks = detect_frameworks(tmp_project)
        assert "FastAPI" in frameworks
        assert "pytest" in frameworks

    def test_detects_js_frameworks(self, tmp_js_project):
        frameworks = detect_frameworks(tmp_js_project)
        assert "Next.js" in frameworks
        assert "React" in frameworks
        assert "Tailwind" in frameworks
        assert "Vitest" in frameworks


class TestDetectDatabases:
    def test_no_databases(self, tmp_project):
        dbs = detect_databases(tmp_project)
        assert dbs == []

    def test_detects_from_docker_compose(self, tmp_path):
        proj = tmp_path / "db-project"
        proj.mkdir()
        (proj / "docker-compose.yml").write_text("services:\n  db:\n    image: postgres:16\n")
        dbs = detect_databases(proj)
        assert "PostgreSQL" in dbs


class TestDetectKeyDeps:
    def test_python_requirements(self, tmp_project):
        deps = detect_key_deps(tmp_project)
        assert "fastapi" in deps
        assert deps["fastapi"] == "==0.109.0"

    def test_js_package_json(self, tmp_js_project):
        deps = detect_key_deps(tmp_js_project)
        assert "next" in deps
        assert "react" in deps
