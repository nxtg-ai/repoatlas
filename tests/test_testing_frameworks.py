"""Tests for testing framework detection."""
from __future__ import annotations

from pathlib import Path

from atlas.detector import detect_testing_frameworks


def _write(tmp_path: Path, name: str, content: str = ""):
    p = tmp_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return p


# ===========================================================================
# Python testing frameworks
# ===========================================================================


class TestPythonTestFrameworks:
    def test_pytest_ini(self, tmp_path):
        _write(tmp_path, "pytest.ini", "[pytest]\naddopts = -v")
        tools = detect_testing_frameworks(tmp_path)
        assert "pytest" in tools

    def test_conftest(self, tmp_path):
        _write(tmp_path, "conftest.py", "import pytest")
        tools = detect_testing_frameworks(tmp_path)
        assert "pytest" in tools

    def test_pyproject_tool_pytest(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[tool.pytest.ini_options]\naddopts = '-v'")
        tools = detect_testing_frameworks(tmp_path)
        assert "pytest" in tools

    def test_pytest_from_deps(self, tmp_path):
        _write(tmp_path, "requirements.txt", "pytest>=7.0\nrequests")
        tools = detect_testing_frameworks(tmp_path)
        assert "pytest" in tools

    def test_pytest_from_pyproject_deps(self, tmp_path):
        _write(tmp_path, "pyproject.toml",
               '[project]\ndependencies = ["fastapi"]\n[project.optional-dependencies]\ndev = ["pytest"]')
        tools = detect_testing_frameworks(tmp_path)
        assert "pytest" in tools

    def test_tox(self, tmp_path):
        _write(tmp_path, "tox.ini", "[tox]\nenvlist = py311")
        tools = detect_testing_frameworks(tmp_path)
        assert "tox" in tools

    def test_nox(self, tmp_path):
        _write(tmp_path, "noxfile.py", "import nox")
        tools = detect_testing_frameworks(tmp_path)
        assert "nox" in tools

    def test_hypothesis(self, tmp_path):
        _write(tmp_path, "requirements-dev.txt", "hypothesis>=6.0\npytest")
        tools = detect_testing_frameworks(tmp_path)
        assert "Hypothesis" in tools

    def test_coverage(self, tmp_path):
        _write(tmp_path, "requirements.txt", "coverage>=7.0")
        tools = detect_testing_frameworks(tmp_path)
        assert "coverage.py" in tools

    def test_no_duplicates(self, tmp_path):
        _write(tmp_path, "pytest.ini", "[pytest]")
        _write(tmp_path, "conftest.py", "")
        _write(tmp_path, "requirements.txt", "pytest>=7.0")
        _write(tmp_path, "pyproject.toml", "[tool.pytest.ini_options]\naddopts = '-v'")
        tools = detect_testing_frameworks(tmp_path)
        assert tools.count("pytest") == 1


# ===========================================================================
# JavaScript/TypeScript testing frameworks
# ===========================================================================


class TestJSTestFrameworks:
    def test_jest_config(self, tmp_path):
        _write(tmp_path, "jest.config.js", "module.exports = {}")
        tools = detect_testing_frameworks(tmp_path)
        assert "Jest" in tools

    def test_jest_config_ts(self, tmp_path):
        _write(tmp_path, "jest.config.ts", "export default {}")
        tools = detect_testing_frameworks(tmp_path)
        assert "Jest" in tools

    def test_vitest_config(self, tmp_path):
        _write(tmp_path, "vitest.config.ts", "export default {}")
        tools = detect_testing_frameworks(tmp_path)
        assert "Vitest" in tools

    def test_mocha_config(self, tmp_path):
        _write(tmp_path, ".mocharc.yml", "timeout: 5000")
        tools = detect_testing_frameworks(tmp_path)
        assert "Mocha" in tools

    def test_cypress_config(self, tmp_path):
        _write(tmp_path, "cypress.config.ts", "export default {}")
        tools = detect_testing_frameworks(tmp_path)
        assert "Cypress" in tools

    def test_cypress_dir(self, tmp_path):
        (tmp_path / "cypress").mkdir()
        _write(tmp_path, "cypress/e2e/test.cy.ts", "")
        tools = detect_testing_frameworks(tmp_path)
        assert "Cypress" in tools

    def test_playwright_config(self, tmp_path):
        _write(tmp_path, "playwright.config.ts", "export default {}")
        tools = detect_testing_frameworks(tmp_path)
        assert "Playwright" in tools

    def test_jest_from_package_json(self, tmp_path):
        _write(tmp_path, "package.json", '{"devDependencies": {"jest": "^29.0"}}')
        tools = detect_testing_frameworks(tmp_path)
        assert "Jest" in tools

    def test_vitest_from_package_json(self, tmp_path):
        _write(tmp_path, "package.json", '{"devDependencies": {"vitest": "^1.0"}}')
        tools = detect_testing_frameworks(tmp_path)
        assert "Vitest" in tools

    def test_playwright_from_package_json(self, tmp_path):
        _write(tmp_path, "package.json", '{"devDependencies": {"@playwright/test": "^1.40"}}')
        tools = detect_testing_frameworks(tmp_path)
        assert "Playwright" in tools

    def test_testing_library_from_package_json(self, tmp_path):
        _write(tmp_path, "package.json",
               '{"devDependencies": {"@testing-library/react": "^14.0"}}')
        tools = detect_testing_frameworks(tmp_path)
        assert "Testing Library" in tools

    def test_ava_from_package_json(self, tmp_path):
        _write(tmp_path, "package.json", '{"devDependencies": {"ava": "^5.0"}}')
        tools = detect_testing_frameworks(tmp_path)
        assert "AVA" in tools

    def test_multiple_js_frameworks(self, tmp_path):
        _write(tmp_path, "package.json",
               '{"devDependencies": {"jest": "^29.0", "@playwright/test": "^1.40"}}')
        tools = detect_testing_frameworks(tmp_path)
        assert "Jest" in tools
        assert "Playwright" in tools


# ===========================================================================
# Go and Rust
# ===========================================================================


class TestGoRustTestFrameworks:
    def test_go_test_detected(self, tmp_path):
        _write(tmp_path, "go.mod", "module example.com/app\ngo 1.21")
        _write(tmp_path, "main_test.go", "package main\nimport \"testing\"")
        tools = detect_testing_frameworks(tmp_path)
        assert "go test" in tools

    def test_go_no_test_files(self, tmp_path):
        _write(tmp_path, "go.mod", "module example.com/app\ngo 1.21")
        _write(tmp_path, "main.go", "package main")
        tools = detect_testing_frameworks(tmp_path)
        assert "go test" not in tools

    def test_cargo_test(self, tmp_path):
        _write(tmp_path, "Cargo.toml", "[package]\nname = \"myapp\"")
        tools = detect_testing_frameworks(tmp_path)
        assert "cargo test" in tools


# ===========================================================================
# Edge cases
# ===========================================================================


class TestEdgeCases:
    def test_empty_project(self, tmp_path):
        tools = detect_testing_frameworks(tmp_path)
        assert tools == []

    def test_no_testing_python_project(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[project]\nname = \"myapp\"")
        _write(tmp_path, "main.py", "print('hello')")
        tools = detect_testing_frameworks(tmp_path)
        assert tools == []

    def test_full_stack_project(self, tmp_path):
        _write(tmp_path, "pytest.ini", "[pytest]")
        _write(tmp_path, "tox.ini", "[tox]")
        _write(tmp_path, "package.json",
               '{"devDependencies": {"jest": "^29.0", "cypress": "^13.0"}}')
        tools = detect_testing_frameworks(tmp_path)
        assert "pytest" in tools
        assert "tox" in tools
        assert "Jest" in tools
        assert "Cypress" in tools

    def test_invalid_package_json(self, tmp_path):
        _write(tmp_path, "package.json", "not json")
        tools = detect_testing_frameworks(tmp_path)
        assert tools == []
