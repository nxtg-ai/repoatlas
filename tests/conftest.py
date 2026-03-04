"""Test fixtures for Atlas."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a minimal project directory for testing."""
    proj = tmp_path / "test-project"
    proj.mkdir()

    # Create .git directory (marks as git repo)
    (proj / ".git").mkdir()

    # Create Python source files
    src = proj / "src"
    src.mkdir()
    (src / "__init__.py").write_text("# App module")
    (src / "main.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/')\ndef root():\n    return {'status': 'ok'}\n")
    (src / "models.py").write_text("from pydantic import BaseModel\n\nclass User(BaseModel):\n    name: str\n    email: str\n")
    (src / "utils.py").write_text("def add(a, b):\n    return a + b\n")

    # Create test files
    tests = proj / "tests"
    tests.mkdir()
    (tests / "__init__.py").write_text("")
    (tests / "test_main.py").write_text("def test_root():\n    assert True\n")
    (tests / "test_models.py").write_text("def test_user():\n    assert True\n")

    # Create pyproject.toml
    (proj / "pyproject.toml").write_text(
        '[project]\nname = "test-project"\nversion = "0.1.0"\n'
        'dependencies = ["fastapi>=0.100.0", "pydantic>=2.0"]\n\n'
        '[project.optional-dependencies]\ndev = ["pytest>=7.0"]\n'
    )

    # Create requirements.txt
    (proj / "requirements.txt").write_text("fastapi==0.109.0\npydantic==2.5.0\nuvicorn==0.27.0\n")

    # Create README
    (proj / "README.md").write_text("# Test Project\nA test project for Atlas.\n")

    # Create .gitignore
    (proj / ".gitignore").write_text("__pycache__/\n*.pyc\n.venv/\n")

    # Create CI
    workflows = proj / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("name: CI\non: push\njobs:\n  test:\n    runs-on: ubuntu-latest\n")

    return proj


@pytest.fixture
def tmp_js_project(tmp_path: Path) -> Path:
    """Create a minimal JavaScript project for testing."""
    proj = tmp_path / "js-project"
    proj.mkdir()

    (proj / ".git").mkdir()

    # package.json
    pkg = {
        "name": "js-project",
        "version": "1.0.0",
        "dependencies": {
            "next": "^14.0.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
        },
        "devDependencies": {
            "vitest": "^1.0.0",
            "tailwindcss": "^3.4.0",
            "@playwright/test": "^1.40.0",
        },
    }
    (proj / "package.json").write_text(json.dumps(pkg))

    # Source files
    src = proj / "src"
    src.mkdir()
    (src / "page.tsx").write_text("export default function Home() { return <h1>Home</h1>; }")
    (src / "layout.tsx").write_text("export default function Layout({ children }) { return children; }")
    (src / "utils.ts").write_text("export function add(a: number, b: number) { return a + b; }")

    # Tests
    tests = proj / "__tests__"
    tests.mkdir()
    (tests / "page.test.tsx").write_text("test('renders', () => { expect(true).toBe(true); })")

    (proj / "README.md").write_text("# JS Project")
    (proj / ".gitignore").write_text("node_modules/\n.next/\n")

    return proj


@pytest.fixture
def tmp_portfolio_file(tmp_path: Path) -> Path:
    """Create a temporary portfolio file path."""
    return tmp_path / "portfolio.json"
