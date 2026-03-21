"""Tests for code quality tooling detection."""
from __future__ import annotations

import json

from atlas.detector import detect_quality_tools


# ---------------------------------------------------------------------------
# Python linters
# ---------------------------------------------------------------------------
class TestPythonLinters:
    def test_ruff_config_file(self, tmp_path):
        (tmp_path / "ruff.toml").write_text("[lint]\nselect = ['E']\n")
        tools = detect_quality_tools(tmp_path)
        assert "Ruff" in tools

    def test_ruff_dot_config(self, tmp_path):
        (tmp_path / ".ruff.toml").write_text("[lint]\n")
        tools = detect_quality_tools(tmp_path)
        assert "Ruff" in tools

    def test_ruff_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.ruff]\nline-length = 120\n")
        tools = detect_quality_tools(tmp_path)
        assert "Ruff" in tools

    def test_ruff_in_requirements(self, tmp_path):
        (tmp_path / "requirements-dev.txt").write_text("ruff>=0.4.0\n")
        tools = detect_quality_tools(tmp_path)
        assert "Ruff" in tools

    def test_flake8_config(self, tmp_path):
        (tmp_path / ".flake8").write_text("[flake8]\nmax-line-length = 120\n")
        tools = detect_quality_tools(tmp_path)
        assert "Flake8" in tools

    def test_flake8_setup_cfg(self, tmp_path):
        (tmp_path / "setup.cfg").write_text("[flake8]\nmax-line-length = 120\n")
        tools = detect_quality_tools(tmp_path)
        assert "Flake8" in tools

    def test_flake8_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flake8>=7.0.0\n")
        tools = detect_quality_tools(tmp_path)
        assert "Flake8" in tools

    def test_pylint_config(self, tmp_path):
        (tmp_path / ".pylintrc").write_text("[MESSAGES CONTROL]\n")
        tools = detect_quality_tools(tmp_path)
        assert "Pylint" in tools

    def test_pylint_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.pylint]\n")
        tools = detect_quality_tools(tmp_path)
        assert "Pylint" in tools

    def test_pylint_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pylint>=3.0.0\n")
        tools = detect_quality_tools(tmp_path)
        assert "Pylint" in tools


# ---------------------------------------------------------------------------
# Python formatters
# ---------------------------------------------------------------------------
class TestPythonFormatters:
    def test_black_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.black]\nline-length = 88\n")
        tools = detect_quality_tools(tmp_path)
        assert "Black" in tools

    def test_black_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("black>=24.0.0\n")
        tools = detect_quality_tools(tmp_path)
        assert "Black" in tools

    def test_isort_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.isort]\nprofile = 'black'\n")
        tools = detect_quality_tools(tmp_path)
        assert "isort" in tools

    def test_isort_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("isort>=5.0.0\n")
        tools = detect_quality_tools(tmp_path)
        assert "isort" in tools

    def test_autopep8_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("autopep8>=2.0.0\n")
        tools = detect_quality_tools(tmp_path)
        assert "autopep8" in tools


# ---------------------------------------------------------------------------
# Python type checkers
# ---------------------------------------------------------------------------
class TestPythonTypeCheckers:
    def test_mypy_ini(self, tmp_path):
        (tmp_path / "mypy.ini").write_text("[mypy]\nstrict = True\n")
        tools = detect_quality_tools(tmp_path)
        assert "mypy" in tools

    def test_mypy_dot_ini(self, tmp_path):
        (tmp_path / ".mypy.ini").write_text("[mypy]\n")
        tools = detect_quality_tools(tmp_path)
        assert "mypy" in tools

    def test_mypy_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.mypy]\nstrict = true\n")
        tools = detect_quality_tools(tmp_path)
        assert "mypy" in tools

    def test_mypy_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mypy>=1.8.0\n")
        tools = detect_quality_tools(tmp_path)
        assert "mypy" in tools

    def test_pyright_config(self, tmp_path):
        (tmp_path / "pyrightconfig.json").write_text('{"strict": ["src"]}\n')
        tools = detect_quality_tools(tmp_path)
        assert "Pyright" in tools

    def test_pyright_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.pyright]\nstrict = ['src']\n")
        tools = detect_quality_tools(tmp_path)
        assert "Pyright" in tools

    def test_pyright_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyright>=1.1.0\n")
        tools = detect_quality_tools(tmp_path)
        assert "Pyright" in tools


# ---------------------------------------------------------------------------
# JavaScript/TypeScript quality tools
# ---------------------------------------------------------------------------
class TestJSQualityTools:
    def test_eslint_config(self, tmp_path):
        (tmp_path / ".eslintrc.json").write_text('{"extends": "next"}\n')
        tools = detect_quality_tools(tmp_path)
        assert "ESLint" in tools

    def test_eslint_flat_config(self, tmp_path):
        (tmp_path / "eslint.config.js").write_text("export default [];\n")
        tools = detect_quality_tools(tmp_path)
        assert "ESLint" in tools

    def test_eslint_in_package_json(self, tmp_path):
        pkg = {"devDependencies": {"eslint": "^9.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_quality_tools(tmp_path)
        assert "ESLint" in tools

    def test_prettier_config(self, tmp_path):
        (tmp_path / ".prettierrc").write_text('{"semi": false}\n')
        tools = detect_quality_tools(tmp_path)
        assert "Prettier" in tools

    def test_prettier_js_config(self, tmp_path):
        (tmp_path / "prettier.config.js").write_text("module.exports = {};\n")
        tools = detect_quality_tools(tmp_path)
        assert "Prettier" in tools

    def test_prettier_in_package_json(self, tmp_path):
        pkg = {"devDependencies": {"prettier": "^3.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_quality_tools(tmp_path)
        assert "Prettier" in tools

    def test_typescript_tsconfig(self, tmp_path):
        (tmp_path / "tsconfig.json").write_text('{"compilerOptions": {"strict": true}}\n')
        tools = detect_quality_tools(tmp_path)
        assert "TypeScript" in tools

    def test_typescript_in_package_json(self, tmp_path):
        pkg = {"devDependencies": {"typescript": "^5.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_quality_tools(tmp_path)
        assert "TypeScript" in tools

    def test_biome_config(self, tmp_path):
        (tmp_path / "biome.json").write_text('{"linter": {"enabled": true}}\n')
        tools = detect_quality_tools(tmp_path)
        assert "Biome" in tools

    def test_biome_jsonc(self, tmp_path):
        (tmp_path / "biome.jsonc").write_text('{"linter": {"enabled": true}}\n')
        tools = detect_quality_tools(tmp_path)
        assert "Biome" in tools

    def test_biome_in_package_json(self, tmp_path):
        pkg = {"devDependencies": {"@biomejs/biome": "^1.5.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_quality_tools(tmp_path)
        assert "Biome" in tools


# ---------------------------------------------------------------------------
# Go and Rust quality tools
# ---------------------------------------------------------------------------
class TestGoRustQualityTools:
    def test_golangci_lint_yml(self, tmp_path):
        (tmp_path / ".golangci.yml").write_text("linters:\n  enable:\n    - govet\n")
        tools = detect_quality_tools(tmp_path)
        assert "golangci-lint" in tools

    def test_golangci_lint_yaml(self, tmp_path):
        (tmp_path / ".golangci.yaml").write_text("linters:\n")
        tools = detect_quality_tools(tmp_path)
        assert "golangci-lint" in tools

    def test_clippy_config(self, tmp_path):
        (tmp_path / "clippy.toml").write_text("cognitive-complexity-threshold = 25\n")
        tools = detect_quality_tools(tmp_path)
        assert "Clippy" in tools

    def test_clippy_dot_config(self, tmp_path):
        (tmp_path / ".clippy.toml").write_text("")
        tools = detect_quality_tools(tmp_path)
        assert "Clippy" in tools


# ---------------------------------------------------------------------------
# Pre-commit hooks
# ---------------------------------------------------------------------------
class TestPreCommitHooks:
    def test_ruff_in_precommit(self, tmp_path):
        (tmp_path / ".pre-commit-config.yaml").write_text(
            "repos:\n  - repo: https://github.com/astral-sh/ruff-pre-commit\n"
            "    hooks:\n      - id: ruff\n"
        )
        tools = detect_quality_tools(tmp_path)
        assert "Ruff" in tools

    def test_black_in_precommit(self, tmp_path):
        (tmp_path / ".pre-commit-config.yaml").write_text(
            "repos:\n  - repo: https://github.com/psf/black\n"
            "    hooks:\n      - id: black\n"
        )
        tools = detect_quality_tools(tmp_path)
        assert "Black" in tools

    def test_mypy_in_precommit(self, tmp_path):
        (tmp_path / ".pre-commit-config.yaml").write_text(
            "repos:\n  - repo: https://github.com/pre-commit/mirrors-mypy\n"
            "    hooks:\n      - id: mypy\n"
        )
        tools = detect_quality_tools(tmp_path)
        assert "mypy" in tools


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_dir(self, tmp_path):
        tools = detect_quality_tools(tmp_path)
        assert tools == []

    def test_no_quality_tools(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastapi>=0.109.0\nrich>=13.0\n")
        tools = detect_quality_tools(tmp_path)
        assert tools == []

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "ruff.toml").write_text("[lint]\n")
        (tmp_path / "pyproject.toml").write_text("[tool.ruff]\n")
        (tmp_path / "requirements.txt").write_text("ruff>=0.4.0\n")
        (tmp_path / ".pre-commit-config.yaml").write_text("- id: ruff\n")
        tools = detect_quality_tools(tmp_path)
        assert tools.count("Ruff") == 1

    def test_combined_stack(self, tmp_path):
        """Project with full quality tooling stack."""
        (tmp_path / "pyproject.toml").write_text(
            "[tool.ruff]\nline-length = 120\n\n"
            "[tool.mypy]\nstrict = true\n\n"
            "[tool.black]\nline-length = 120\n"
        )
        tools = detect_quality_tools(tmp_path)
        assert "Ruff" in tools
        assert "mypy" in tools
        assert "Black" in tools
        assert len(tools) == 3

    def test_js_full_stack(self, tmp_path):
        """JS project with ESLint + Prettier + TypeScript."""
        pkg = {"devDependencies": {
            "eslint": "^9.0.0", "prettier": "^3.0.0", "typescript": "^5.0.0"
        }}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        (tmp_path / "tsconfig.json").write_text("{}")
        tools = detect_quality_tools(tmp_path)
        assert "ESLint" in tools
        assert "Prettier" in tools
        assert "TypeScript" in tools
