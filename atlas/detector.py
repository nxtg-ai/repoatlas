"""Tech stack detection — scans project files to identify languages, frameworks, databases."""
from __future__ import annotations

import json
from pathlib import Path

SKIP_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "target", "dist", "build", ".next", ".nuxt", "coverage",
    ".pytest_cache", ".mypy_cache", ".tox", ".eggs", ".ruff_cache",
    ".claude", ".asif", ".forge", "egg-info",
})

SOURCE_EXTENSIONS = frozenset({
    ".py", ".js", ".ts", ".tsx", ".jsx", ".rs", ".go", ".java",
    ".rb", ".swift", ".kt", ".cpp", ".c", ".cs", ".php",
})

LANGUAGE_MAP = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".tsx": "TypeScript", ".jsx": "JavaScript", ".rs": "Rust",
    ".go": "Go", ".java": "Java", ".rb": "Ruby", ".swift": "Swift",
    ".kt": "Kotlin", ".cpp": "C++", ".c": "C", ".cs": "C#",
    ".php": "PHP", ".sql": "SQL", ".sh": "Shell",
    ".md": "Markdown", ".mdx": "MDX",
}

TEST_PATTERNS = (
    "test_", "_test.", ".test.", ".spec.", "Test",
)


def walk_files(project_path: Path):
    """Yield non-ignored files in the project."""
    try:
        for item in project_path.rglob("*"):
            if not item.is_file():
                continue
            parts = item.relative_to(project_path).parts
            if any(p in SKIP_DIRS for p in parts):
                continue
            yield item
    except PermissionError:
        pass


def detect_languages(project_path: Path) -> dict[str, int]:
    """Count files by language."""
    counts: dict[str, int] = {}
    for f in walk_files(project_path):
        ext = f.suffix.lower()
        if ext in LANGUAGE_MAP:
            lang = LANGUAGE_MAP[ext]
            counts[lang] = counts.get(lang, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def count_files(project_path: Path) -> tuple[int, int]:
    """Return (source_files, total_files)."""
    source = 0
    total = 0
    for f in walk_files(project_path):
        total += 1
        if f.suffix.lower() in SOURCE_EXTENSIONS:
            source += 1
    return source, total


def count_test_files(project_path: Path) -> int:
    """Count files that look like tests."""
    count = 0
    for f in walk_files(project_path):
        if f.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        name = f.name
        stem = f.stem
        if any(pat in name for pat in TEST_PATTERNS):
            count += 1
        elif any(p in ("tests", "test", "__tests__", "spec") for p in f.relative_to(project_path).parts):
            count += 1
    return count


def count_loc(project_path: Path) -> int:
    """Count lines of source code."""
    total = 0
    for f in walk_files(project_path):
        if f.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        try:
            total += sum(1 for line in f.open(errors="ignore") if line.strip())
        except OSError:
            pass
    return total


def detect_frameworks(project_path: Path) -> list[str]:
    """Detect frameworks from config files."""
    frameworks: list[str] = []

    # Python
    for cfg in ("pyproject.toml", "setup.py", "requirements.txt"):
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            _check_add(frameworks, content, "fastapi", "FastAPI")
            _check_add(frameworks, content, "django", "Django")
            _check_add(frameworks, content, "flask", "Flask")
            _check_add(frameworks, content, "pytest", "pytest")
            _check_add(frameworks, content, "sqlalchemy", "SQLAlchemy")
            _check_add(frameworks, content, "pydantic", "Pydantic")
            _check_add(frameworks, content, "celery", "Celery")
            _check_add(frameworks, content, "anthropic", "Anthropic SDK")

    # JavaScript / TypeScript
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            dep_map = {
                "next": "Next.js", "react": "React", "vue": "Vue",
                "svelte": "Svelte", "express": "Express",
                "tailwindcss": "Tailwind", "vitest": "Vitest",
                "jest": "Jest", "@playwright/test": "Playwright",
                "three": "Three.js", "@react-three/fiber": "R3F",
                "framer-motion": "Framer Motion", "drizzle-orm": "Drizzle",
                "prisma": "Prisma", "vite": "Vite",
            }
            for dep, name in dep_map.items():
                if dep in all_deps and name not in frameworks:
                    frameworks.append(name)
        except (json.JSONDecodeError, KeyError):
            pass

    # Rust
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        content = cargo.read_text(errors="ignore").lower()
        if "Rust" not in frameworks:
            frameworks.append("Rust")
        _check_add(frameworks, content, "tokio", "Tokio")
        _check_add(frameworks, content, "actix", "Actix")
        _check_add(frameworks, content, "axum", "Axum")
        _check_add(frameworks, content, "tauri", "Tauri")
        _check_add(frameworks, content, "ratatui", "Ratatui")

    # Docker
    if (project_path / "Dockerfile").exists() or (project_path / "docker-compose.yml").exists():
        _check_add(frameworks, "docker", "docker", "Docker")

    return frameworks


def detect_databases(project_path: Path) -> list[str]:
    """Detect database usage."""
    dbs: list[str] = []
    search_files = [
        "pyproject.toml", "package.json", "docker-compose.yml",
        "docker-compose.yaml", "requirements.txt", ".env.example",
    ]
    for cfg in search_files:
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            if ("postgresql" in content or "psycopg" in content or "postgres" in content) and "PostgreSQL" not in dbs:
                dbs.append("PostgreSQL")
            if "sqlite" in content and "SQLite" not in dbs:
                dbs.append("SQLite")
            if "redis" in content and "Redis" not in dbs:
                dbs.append("Redis")
            if ("mongodb" in content or "pymongo" in content) and "MongoDB" not in dbs:
                dbs.append("MongoDB")
            if "pgvector" in content and "pgvector" not in dbs:
                dbs.append("pgvector")
    return dbs


def detect_key_deps(project_path: Path) -> dict[str, str]:
    """Extract key dependencies with versions."""
    deps: dict[str, str] = {}

    # Python requirements.txt
    for req_file in ("requirements.txt", "requirements-dev.txt"):
        req_path = project_path / req_file
        if req_path.exists():
            for line in req_path.read_text(errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                for sep in ("==", ">=", "~=", "<="):
                    if sep in line:
                        name, version = line.split(sep, 1)
                        deps[name.strip().lower()] = f"{sep}{version.strip()}"
                        break

    # JavaScript package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            for dep_type in ("dependencies", "devDependencies"):
                for name, version in data.get(dep_type, {}).items():
                    deps[name] = version
        except (json.JSONDecodeError, KeyError):
            pass

    return deps


def _check_add(lst: list[str], content: str, keyword: str, name: str):
    if keyword in content and name not in lst:
        lst.append(name)
