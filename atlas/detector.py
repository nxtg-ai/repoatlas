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
    """Detect database and data store usage."""
    dbs: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            dbs.append(name)

    search_files = [
        "pyproject.toml", "package.json", "docker-compose.yml",
        "docker-compose.yaml", "requirements.txt", "requirements-dev.txt",
        ".env.example", ".env.sample", "Cargo.toml", "go.mod",
        "Gemfile", "pom.xml", "build.gradle",
    ]
    for cfg in search_files:
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            # Relational
            if "postgresql" in content or "psycopg" in content or "postgres" in content:
                _add("PostgreSQL")
            if "mysql" in content or "mariadb" in content:
                _add("MySQL")
            if "sqlite" in content:
                _add("SQLite")
            # Document
            if "mongodb" in content or "pymongo" in content or "mongoose" in content:
                _add("MongoDB")
            if "firestore" in content or "firebase" in content:
                _add("Firestore")
            if "dynamodb" in content or "boto3" in content and "dynamo" in content:
                _add("DynamoDB")
            # Key-value / Cache
            if "redis" in content:
                _add("Redis")
            if "memcached" in content or "pylibmc" in content:
                _add("Memcached")
            # Search
            if "elasticsearch" in content or "opensearch" in content:
                _add("Elasticsearch")
            # Graph
            if "neo4j" in content:
                _add("Neo4j")
            # Time-series
            if "influxdb" in content or "influx" in content and "client" in content:
                _add("InfluxDB")
            # Wide-column
            if "cassandra" in content:
                _add("Cassandra")
            # Vector
            if "pgvector" in content:
                _add("pgvector")
            if "chromadb" in content or "chroma" in content and "vector" in content:
                _add("ChromaDB")
            if "pinecone" in content:
                _add("Pinecone")
            if "qdrant" in content:
                _add("Qdrant")
            if "weaviate" in content:
                _add("Weaviate")
            # Cloud-native
            if "supabase" in content:
                _add("Supabase")
            if "planetscale" in content:
                _add("PlanetScale")
            if "cockroachdb" in content or "cockroach" in content:
                _add("CockroachDB")
            # Message brokers (data infrastructure)
            if "rabbitmq" in content or "amqp" in content:
                _add("RabbitMQ")
            if "kafka" in content:
                _add("Kafka")
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


def detect_infrastructure(project_path: Path) -> list[str]:
    """Detect infrastructure, deployment, and cloud patterns."""
    infra: list[str] = []

    # Docker
    if (project_path / "Dockerfile").exists():
        infra.append("Docker")
    if (project_path / "docker-compose.yml").exists() or (project_path / "docker-compose.yaml").exists():
        if "Docker Compose" not in infra:
            infra.append("Docker Compose")
        if "Docker" not in infra:
            infra.append("Docker")

    # Kubernetes
    k8s_dirs = ("k8s", "kubernetes", "kube", "manifests", "charts", "helm")
    for d in k8s_dirs:
        if (project_path / d).is_dir():
            _check_add(infra, "kubernetes", "kubernetes", "Kubernetes")
            break
    if (project_path / "Chart.yaml").exists() or (project_path / "helmfile.yaml").exists():
        _check_add(infra, "helm", "helm", "Helm")
        _check_add(infra, "kubernetes", "kubernetes", "Kubernetes")

    # Terraform / IaC
    if any(project_path.glob("*.tf")) or (project_path / "terraform").is_dir():
        infra.append("Terraform")
    if (project_path / "Pulumi.yaml").exists():
        infra.append("Pulumi")
    if (project_path / "cdk.json").exists():
        infra.append("AWS CDK")

    # CI/CD
    gh_workflows = project_path / ".github" / "workflows"
    if gh_workflows.is_dir():
        _check_add(infra, "github", "github", "GitHub Actions")
    if (project_path / ".gitlab-ci.yml").exists():
        infra.append("GitLab CI")
    if (project_path / "Jenkinsfile").exists():
        infra.append("Jenkins")
    if (project_path / ".circleci").is_dir():
        infra.append("CircleCI")

    # Serverless / Edge
    if (project_path / "serverless.yml").exists() or (project_path / "serverless.yaml").exists():
        infra.append("Serverless Framework")
    if (project_path / "vercel.json").exists():
        infra.append("Vercel")
    if (project_path / "netlify.toml").exists():
        infra.append("Netlify")
    if (project_path / "wrangler.toml").exists():
        infra.append("Cloudflare Workers")
    if (project_path / "fly.toml").exists():
        infra.append("Fly.io")
    if (project_path / "render.yaml").exists():
        infra.append("Render")

    # Cloud providers (from config files or SDK deps)
    _detect_cloud_from_deps(project_path, infra)

    return infra


def detect_ai_tools(project_path: Path) -> list[str]:
    """Detect AI/ML frameworks, tools, and patterns."""
    tools: list[str] = []

    # Python AI/ML deps
    for cfg in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            _check_add(tools, content, "anthropic", "Anthropic SDK")
            _check_add(tools, content, "openai", "OpenAI SDK")
            _check_add(tools, content, "langchain", "LangChain")
            _check_add(tools, content, "llama-index", "LlamaIndex")
            _check_add(tools, content, "transformers", "Transformers")
            _check_add(tools, content, "torch", "PyTorch")
            _check_add(tools, content, "tensorflow", "TensorFlow")
            _check_add(tools, content, "scikit-learn", "scikit-learn")
            _check_add(tools, content, "mlflow", "MLflow")
            _check_add(tools, content, "wandb", "Weights & Biases")
            _check_add(tools, content, "huggingface", "Hugging Face")
            _check_add(tools, content, "sentence-transformers", "Sentence Transformers")
            _check_add(tools, content, "chromadb", "ChromaDB")
            _check_add(tools, content, "pinecone", "Pinecone")

    # JavaScript AI deps
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            js_ai = {
                "@anthropic-ai/sdk": "Anthropic SDK",
                "openai": "OpenAI SDK",
                "langchain": "LangChain",
                "@langchain/core": "LangChain",
                "llamaindex": "LlamaIndex",
                "@huggingface/inference": "Hugging Face",
                "ai": "Vercel AI SDK",
                "@ai-sdk/anthropic": "Vercel AI SDK",
                "@ai-sdk/openai": "Vercel AI SDK",
            }
            for dep, name in js_ai.items():
                if dep in all_deps and name not in tools:
                    tools.append(name)
        except (json.JSONDecodeError, KeyError):
            pass

    # Jupyter notebooks
    has_notebooks = False
    try:
        for f in walk_files(project_path):
            if f.suffix == ".ipynb":
                has_notebooks = True
                break
    except OSError:
        pass
    if has_notebooks:
        tools.append("Jupyter")

    # ML infrastructure files
    if (project_path / "MLproject").exists():
        _check_add(tools, "mlflow", "mlflow", "MLflow")
    if (project_path / "wandb").is_dir():
        _check_add(tools, "wandb", "wandb", "Weights & Biases")
    if (project_path / "dvc.yaml").exists() or (project_path / ".dvc").is_dir():
        tools.append("DVC")

    return tools


def detect_security_tools(project_path: Path) -> list[str]:
    """Detect security tooling and practices."""
    tools: list[str] = []

    # Security policy
    if (project_path / "SECURITY.md").exists():
        tools.append("SECURITY.md")

    # Dependency scanning / updates
    if (project_path / ".github" / "dependabot.yml").exists():
        tools.append("Dependabot")
    if (project_path / "renovate.json").exists() or (project_path / ".renovaterc").exists():
        tools.append("Renovate")
    if (project_path / ".snyk").exists():
        tools.append("Snyk")

    # Secret scanning
    if (project_path / ".gitleaks.toml").exists():
        tools.append("Gitleaks")
    if (project_path / ".sops.yaml").exists():
        tools.append("SOPS")

    # Pre-commit hooks (security-relevant)
    pre_commit = project_path / ".pre-commit-config.yaml"
    if pre_commit.exists():
        content = pre_commit.read_text(errors="ignore").lower()
        _check_add(tools, content, "detect-secrets", "detect-secrets")
        _check_add(tools, content, "gitleaks", "Gitleaks")
        _check_add(tools, content, "bandit", "Bandit")

    # Python security tools in deps
    for cfg in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            _check_add(tools, content, "bandit", "Bandit")
            _check_add(tools, content, "safety", "Safety")
            _check_add(tools, content, "pip-audit", "pip-audit")

    # CodeQL — config dir or workflow reference
    if (project_path / ".github" / "codeql").is_dir():
        tools.append("CodeQL")
    gh_workflows = project_path / ".github" / "workflows"
    if gh_workflows.is_dir() and "CodeQL" not in tools:
        try:
            for wf in gh_workflows.iterdir():
                if wf.suffix in (".yml", ".yaml"):
                    wf_content = wf.read_text(errors="ignore").lower()
                    if "codeql" in wf_content:
                        tools.append("CodeQL")
                        break
        except OSError:
            pass

    # Trivy
    if (project_path / "trivy.yaml").exists() or (project_path / ".trivy.yaml").exists():
        tools.append("Trivy")

    return tools


def detect_quality_tools(project_path: Path) -> list[str]:
    """Detect code quality tooling — linters, formatters, type checkers."""
    tools: list[str] = []

    # --- Python quality tools ---

    # Ruff (config files)
    if (project_path / ".ruff.toml").exists() or (project_path / "ruff.toml").exists():
        _check_add(tools, "ruff", "ruff", "Ruff")
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        pyproject_content = pyproject.read_text(errors="ignore").lower()
        if "[tool.ruff" in pyproject_content:
            _check_add(tools, "ruff", "ruff", "Ruff")
        if "[tool.pylint" in pyproject_content:
            _check_add(tools, "pylint", "pylint", "Pylint")
        if "[tool.mypy" in pyproject_content:
            _check_add(tools, "mypy", "mypy", "mypy")
        if "[tool.pyright" in pyproject_content:
            _check_add(tools, "pyright", "pyright", "Pyright")
        if "[tool.black" in pyproject_content:
            _check_add(tools, "black", "black", "Black")
        if "[tool.isort" in pyproject_content:
            _check_add(tools, "isort", "isort", "isort")

    # Flake8 config
    if (project_path / ".flake8").exists():
        _check_add(tools, "flake8", "flake8", "Flake8")
    setup_cfg = project_path / "setup.cfg"
    if setup_cfg.exists():
        cfg_content = setup_cfg.read_text(errors="ignore").lower()
        if "[flake8]" in cfg_content:
            _check_add(tools, "flake8", "flake8", "Flake8")

    # Pylint config
    if (project_path / ".pylintrc").exists():
        _check_add(tools, "pylint", "pylint", "Pylint")

    # mypy config
    if (project_path / ".mypy.ini").exists() or (project_path / "mypy.ini").exists():
        _check_add(tools, "mypy", "mypy", "mypy")

    # Pyright config
    if (project_path / "pyrightconfig.json").exists():
        _check_add(tools, "pyright", "pyright", "Pyright")

    # Python deps
    for cfg in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            _check_add(tools, content, "ruff", "Ruff")
            _check_add(tools, content, "flake8", "Flake8")
            _check_add(tools, content, "pylint", "Pylint")
            _check_add(tools, content, "black", "Black")
            _check_add(tools, content, "isort", "isort")
            _check_add(tools, content, "autopep8", "autopep8")
            _check_add(tools, content, "mypy", "mypy")
            _check_add(tools, content, "pyright", "Pyright")

    # --- JavaScript/TypeScript quality tools ---

    # ESLint config
    eslint_configs = (".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.yml",
                      ".eslintrc.yaml", "eslint.config.js", "eslint.config.mjs")
    for cfg in eslint_configs:
        if (project_path / cfg).exists():
            _check_add(tools, "eslint", "eslint", "ESLint")
            break

    # Prettier config
    prettier_configs = (".prettierrc", ".prettierrc.js", ".prettierrc.json",
                        ".prettierrc.yml", ".prettierrc.yaml", "prettier.config.js",
                        "prettier.config.mjs")
    for cfg in prettier_configs:
        if (project_path / cfg).exists():
            _check_add(tools, "prettier", "prettier", "Prettier")
            break

    # TypeScript
    if (project_path / "tsconfig.json").exists():
        _check_add(tools, "typescript", "typescript", "TypeScript")

    # Biome
    if (project_path / "biome.json").exists() or (project_path / "biome.jsonc").exists():
        _check_add(tools, "biome", "biome", "Biome")

    # JS deps
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            js_quality = {
                "eslint": "ESLint",
                "prettier": "Prettier",
                "typescript": "TypeScript",
                "@biomejs/biome": "Biome",
            }
            for dep, name in js_quality.items():
                if dep in all_deps and name not in tools:
                    tools.append(name)
        except (json.JSONDecodeError, KeyError):
            pass

    # --- Go quality tools ---
    if (project_path / ".golangci.yml").exists() or (project_path / ".golangci.yaml").exists():
        tools.append("golangci-lint")

    # --- Rust quality tools ---
    if (project_path / ".clippy.toml").exists() or (project_path / "clippy.toml").exists():
        tools.append("Clippy")

    # --- Pre-commit hooks ---
    pre_commit = project_path / ".pre-commit-config.yaml"
    if pre_commit.exists():
        content = pre_commit.read_text(errors="ignore").lower()
        _check_add(tools, content, "ruff", "Ruff")
        _check_add(tools, content, "black", "Black")
        _check_add(tools, content, "isort", "isort")
        _check_add(tools, content, "mypy", "mypy")
        _check_add(tools, content, "eslint", "ESLint")
        _check_add(tools, content, "prettier", "Prettier")

    return tools


def detect_testing_frameworks(project_path: Path) -> list[str]:
    """Detect testing frameworks and tools."""
    tools: list[str] = []

    # --- Python testing ---
    # pytest (config files)
    if (project_path / "pytest.ini").exists():
        _check_add(tools, "pytest", "pytest", "pytest")
    if (project_path / "conftest.py").exists():
        _check_add(tools, "pytest", "pytest", "pytest")
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(errors="ignore").lower()
        if "[tool.pytest" in content:
            _check_add(tools, "pytest", "pytest", "pytest")

    # tox
    if (project_path / "tox.ini").exists():
        tools.append("tox")

    # nox
    if (project_path / "noxfile.py").exists():
        tools.append("nox")

    # Python deps
    for cfg in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            _check_add(tools, content, "pytest", "pytest")
            _check_add(tools, content, "unittest2", "unittest2")
            _check_add(tools, content, "nose2", "nose2")
            _check_add(tools, content, "hypothesis", "Hypothesis")
            _check_add(tools, content, "coverage", "coverage.py")

    # --- JavaScript/TypeScript testing ---
    # Jest config
    jest_configs = ("jest.config.js", "jest.config.ts", "jest.config.mjs",
                    "jest.config.cjs", "jest.config.json")
    for cfg in jest_configs:
        if (project_path / cfg).exists():
            _check_add(tools, "jest", "jest", "Jest")
            break

    # Vitest config
    vitest_configs = ("vitest.config.ts", "vitest.config.js", "vitest.config.mts",
                      "vitest.config.mjs")
    for cfg in vitest_configs:
        if (project_path / cfg).exists():
            _check_add(tools, "vitest", "vitest", "Vitest")
            break

    # Mocha config
    mocha_configs = (".mocharc.yml", ".mocharc.yaml", ".mocharc.json", ".mocharc.js")
    for cfg in mocha_configs:
        if (project_path / cfg).exists():
            _check_add(tools, "mocha", "mocha", "Mocha")
            break

    # Cypress
    cypress_configs = ("cypress.config.ts", "cypress.config.js", "cypress.config.mjs")
    for cfg in cypress_configs:
        if (project_path / cfg).exists():
            _check_add(tools, "cypress", "cypress", "Cypress")
            break
    if (project_path / "cypress").is_dir():
        _check_add(tools, "cypress", "cypress", "Cypress")

    # Playwright config
    playwright_configs = ("playwright.config.ts", "playwright.config.js")
    for cfg in playwright_configs:
        if (project_path / cfg).exists():
            _check_add(tools, "playwright", "playwright", "Playwright")
            break

    # JS deps
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            js_test = {
                "jest": "Jest",
                "vitest": "Vitest",
                "mocha": "Mocha",
                "cypress": "Cypress",
                "@playwright/test": "Playwright",
                "ava": "AVA",
                "@testing-library/react": "Testing Library",
                "@testing-library/jest-dom": "Testing Library",
            }
            for dep, name in js_test.items():
                if dep in all_deps and name not in tools:
                    tools.append(name)
        except (json.JSONDecodeError, KeyError):
            pass

    # --- Go testing ---
    # go test is built-in; detect by _test.go files
    if (project_path / "go.mod").exists():
        try:
            for f in walk_files(project_path):
                if f.name.endswith("_test.go"):
                    tools.append("go test")
                    break
        except OSError:
            pass

    # --- Rust testing ---
    if (project_path / "Cargo.toml").exists():
        tools.append("cargo test")

    return tools


def _detect_cloud_from_deps(project_path: Path, infra: list[str]) -> None:
    """Detect cloud providers from dependency files."""
    search_files = ("pyproject.toml", "requirements.txt", "package.json")
    for cfg in search_files:
        path = project_path / cfg
        if not path.exists():
            continue
        content = path.read_text(errors="ignore").lower()
        if ("boto3" in content or "aws-sdk" in content or "@aws-sdk" in content) and "AWS" not in infra:
            infra.append("AWS")
        if ("google-cloud" in content or "@google-cloud" in content) and "GCP" not in infra:
            infra.append("GCP")
        if ("azure" in content) and "Azure" not in infra:
            infra.append("Azure")


def _check_add(lst: list[str], content: str, keyword: str, name: str):
    if keyword in content and name not in lst:
        lst.append(name)


def detect_package_managers(project_path: Path) -> list[str]:
    """Detect package managers and build tools."""
    managers: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            managers.append(name)

    # Python
    if (project_path / "poetry.lock").exists() or (project_path / "poetry.toml").exists():
        _add("Poetry")
    if (project_path / "pdm.lock").exists():
        _add("PDM")
    if (project_path / "uv.lock").exists():
        _add("uv")
    if (project_path / "Pipfile").exists() or (project_path / "Pipfile.lock").exists():
        _add("Pipenv")
    if (project_path / "setup.py").exists() or (project_path / "setup.cfg").exists():
        _add("setuptools")
    # pip via requirements.txt (only if no other Python manager found)
    if (project_path / "requirements.txt").exists() and not (seen & {"Poetry", "PDM", "uv", "Pipenv"}):
        _add("pip")
    # pyproject.toml can indicate several managers
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(errors="ignore").lower()
        if "[tool.poetry]" in content and "Poetry" not in seen:
            _add("Poetry")
        if "pdm" in content and "[tool.pdm]" in content and "PDM" not in seen:
            _add("PDM")
        if "[build-system]" in content and "hatchling" in content:
            _add("Hatch")
        if "[build-system]" in content and "flit" in content:
            _add("Flit")

    # JavaScript/TypeScript
    if (project_path / "pnpm-lock.yaml").exists():
        _add("pnpm")
    elif (project_path / "yarn.lock").exists():
        _add("Yarn")
    elif (project_path / "bun.lockb").exists() or (project_path / "bun.lock").exists():
        _add("Bun")
    elif (project_path / "package-lock.json").exists():
        _add("npm")
    elif (project_path / "package.json").exists() and not (seen & {"pnpm", "Yarn", "Bun", "npm"}):
        _add("npm")

    # Rust
    if (project_path / "Cargo.toml").exists():
        _add("Cargo")

    # Go
    if (project_path / "go.mod").exists():
        _add("Go Modules")

    # Ruby
    if (project_path / "Gemfile").exists():
        _add("Bundler")

    # Java/Kotlin
    if (project_path / "pom.xml").exists():
        _add("Maven")
    if (project_path / "build.gradle").exists() or (project_path / "build.gradle.kts").exists():
        _add("Gradle")

    # .NET
    if any(project_path.glob("*.csproj")) or any(project_path.glob("*.sln")):
        _add("NuGet")

    # PHP
    if (project_path / "composer.json").exists():
        _add("Composer")

    return managers


# --- License Detection ---

_LICENSE_FILE_NAMES = (
    "LICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE.rst",
    "LICENCE", "LICENCE.md", "LICENCE.txt",
    "COPYING", "COPYING.md", "COPYING.txt",
)

# Patterns matched against LICENSE file content (order matters — more specific first)
_LICENSE_CONTENT_PATTERNS: list[tuple[str, list[str]]] = [
    ("AGPL-3.0", ["GNU AFFERO GENERAL PUBLIC LICENSE", "Version 3"]),
    ("LGPL-3.0", ["GNU LESSER GENERAL PUBLIC LICENSE", "Version 3"]),
    ("LGPL-2.1", ["GNU LESSER GENERAL PUBLIC LICENSE", "Version 2.1"]),
    ("GPL-3.0", ["GNU GENERAL PUBLIC LICENSE", "Version 3"]),
    ("GPL-2.0", ["GNU GENERAL PUBLIC LICENSE", "Version 2"]),
    ("MPL-2.0", ["Mozilla Public License", "2.0"]),
    ("Apache-2.0", ["Apache License", "Version 2.0"]),
    ("Unlicense", ["This is free and unencumbered software"]),
    ("CC0-1.0", ["CC0 1.0 Universal"]),
    ("ISC", ["Permission to use, copy, modify, and/or distribute"]),
    ("MIT", ["Permission is hereby granted, free of charge"]),
    ("BSD-3-Clause", ["Redistribution and use", "3."]),
    ("BSD-2-Clause", ["Redistribution and use"]),
]

# SPDX expression normalization
_SPDX_NORMALIZE: dict[str, str] = {
    "mit": "MIT",
    "apache-2.0": "Apache-2.0",
    "apache 2.0": "Apache-2.0",
    "gpl-3.0": "GPL-3.0",
    "gpl-3.0-only": "GPL-3.0",
    "gpl-3.0-or-later": "GPL-3.0",
    "gpl-2.0": "GPL-2.0",
    "gpl-2.0-only": "GPL-2.0",
    "gpl-2.0-or-later": "GPL-2.0",
    "lgpl-3.0": "LGPL-3.0",
    "lgpl-3.0-only": "LGPL-3.0",
    "lgpl-2.1": "LGPL-2.1",
    "lgpl-2.1-only": "LGPL-2.1",
    "agpl-3.0": "AGPL-3.0",
    "agpl-3.0-only": "AGPL-3.0",
    "bsd-2-clause": "BSD-2-Clause",
    "bsd-3-clause": "BSD-3-Clause",
    "isc": "ISC",
    "mpl-2.0": "MPL-2.0",
    "unlicense": "Unlicense",
    "cc0-1.0": "CC0-1.0",
}


def _normalize_spdx(raw: str) -> str:
    """Normalize a license string to a standard SPDX identifier."""
    stripped = raw.strip().strip('"').strip("'")
    return _SPDX_NORMALIZE.get(stripped.lower(), stripped)


def detect_license(project_path: Path) -> str:
    """Detect the project license from config files and LICENSE file content."""
    # 1. Check pyproject.toml
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            text = pyproject.read_text(errors="ignore")
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("license") and "=" in stripped:
                    val = stripped.split("=", 1)[1].strip().strip('"').strip("'")
                    # Skip file references like {file = "LICENSE"}
                    if not val.startswith("{"):
                        return _normalize_spdx(val)
        except OSError:
            pass

    # 2. Check package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(errors="ignore"))
            if isinstance(data.get("license"), str) and data["license"]:
                return _normalize_spdx(data["license"])
        except (json.JSONDecodeError, OSError):
            pass

    # 3. Check Cargo.toml
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            text = cargo_toml.read_text(errors="ignore")
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("license") and "=" in stripped:
                    val = stripped.split("=", 1)[1].strip().strip('"').strip("'")
                    if val and not val.startswith("{"):
                        return _normalize_spdx(val)
        except OSError:
            pass

    # 4. Check LICENSE file content
    for name in _LICENSE_FILE_NAMES:
        license_file = project_path / name
        if license_file.exists():
            try:
                content = license_file.read_text(errors="ignore")[:4000]
                upper = content.upper()
                for spdx_id, patterns in _LICENSE_CONTENT_PATTERNS:
                    if all(p.upper() in upper for p in patterns):
                        return spdx_id
            except OSError:
                pass

    return ""


# --- Documentation artifacts ---

_README_NAMES = ("README.md", "README.rst", "README.txt", "README")
_CHANGELOG_NAMES = (
    "CHANGELOG.md", "CHANGELOG.rst", "CHANGELOG.txt", "CHANGELOG",
    "CHANGES.md", "CHANGES.rst", "CHANGES.txt", "CHANGES",
    "HISTORY.md", "HISTORY.rst", "HISTORY.txt",
)
_CONTRIBUTING_NAMES = (
    "CONTRIBUTING.md", "CONTRIBUTING.rst", "CONTRIBUTING.txt", "CONTRIBUTING",
)
_COC_NAMES = (
    "CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.rst", "CODE_OF_CONDUCT.txt",
    "CODE_OF_CONDUCT",
)
_SECURITY_NAMES = (
    "SECURITY.md", "SECURITY.rst", "SECURITY.txt", "SECURITY",
)
_API_SPEC_NAMES = (
    "openapi.json", "openapi.yaml", "openapi.yml",
    "swagger.json", "swagger.yaml", "swagger.yml",
)


def detect_docs_artifacts(project_path: Path) -> list[str]:
    """Detect documentation artifacts present in the project."""
    artifacts: list[str] = []

    # README
    if any((project_path / name).exists() for name in _README_NAMES):
        artifacts.append("README")

    # CHANGELOG
    if any((project_path / name).exists() for name in _CHANGELOG_NAMES):
        artifacts.append("CHANGELOG")

    # CONTRIBUTING
    if any((project_path / name).exists() for name in _CONTRIBUTING_NAMES):
        artifacts.append("CONTRIBUTING")

    # CODE_OF_CONDUCT
    if any((project_path / name).exists() for name in _COC_NAMES):
        artifacts.append("CODE_OF_CONDUCT")

    # SECURITY policy
    if any((project_path / name).exists() for name in _SECURITY_NAMES):
        artifacts.append("SECURITY")

    # LICENSE (already detected separately, but useful as a docs artifact)
    if any((project_path / name).exists() for name in _LICENSE_FILE_NAMES):
        artifacts.append("LICENSE")

    # docs/ directory
    docs_dir = project_path / "docs"
    if docs_dir.is_dir():
        artifacts.append("docs/")

    # API specification
    if any((project_path / name).exists() for name in _API_SPEC_NAMES):
        artifacts.append("API spec")
    else:
        # Check in docs/ subdirectory too
        if docs_dir.is_dir() and any((docs_dir / name).exists() for name in _API_SPEC_NAMES):
            artifacts.append("API spec")

    # .editorconfig
    if (project_path / ".editorconfig").exists():
        artifacts.append(".editorconfig")

    return sorted(artifacts)


# --- CI/CD configuration ---


def detect_ci_config(project_path: Path) -> list[str]:
    """Detect CI/CD configuration and workflow artifacts."""
    config: list[str] = []

    github_dir = project_path / ".github"

    # GitHub Actions workflows
    workflows_dir = github_dir / "workflows"
    if workflows_dir.is_dir():
        workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        if workflow_files:
            config.append("GitHub Actions")
            # Detect specific workflow patterns
            for wf in workflow_files:
                try:
                    content = wf.read_text(errors="ignore")[:4000].lower()
                    if "release" in wf.stem.lower() or "on:\n  release" in content or "on:\n  push:\n    tags" in content:
                        if "release workflow" not in config:
                            config.append("release workflow")
                    if "deploy" in wf.stem.lower() or "deploy" in content:
                        if "deploy workflow" not in config:
                            config.append("deploy workflow")
                except OSError:
                    pass

    # GitLab CI
    if (project_path / ".gitlab-ci.yml").exists():
        config.append("GitLab CI")

    # PR template
    pr_template_locations = [
        github_dir / "pull_request_template.md",
        github_dir / "PULL_REQUEST_TEMPLATE.md",
        project_path / "pull_request_template.md",
        project_path / "PULL_REQUEST_TEMPLATE.md",
    ]
    pr_template_dir = github_dir / "PULL_REQUEST_TEMPLATE"
    if any(p.exists() for p in pr_template_locations) or (pr_template_dir.is_dir()):
        config.append("PR template")

    # Issue templates
    issue_template_dir = github_dir / "ISSUE_TEMPLATE"
    issue_template_locations = [
        github_dir / "issue_template.md",
        github_dir / "ISSUE_TEMPLATE.md",
    ]
    if (issue_template_dir.is_dir()) or any(p.exists() for p in issue_template_locations):
        config.append("issue templates")

    # CODEOWNERS
    codeowners_locations = [
        github_dir / "CODEOWNERS",
        project_path / "CODEOWNERS",
        project_path / "docs" / "CODEOWNERS",
    ]
    if any(p.exists() for p in codeowners_locations):
        config.append("CODEOWNERS")

    # Dependabot config
    if (github_dir / "dependabot.yml").exists() or (github_dir / "dependabot.yaml").exists():
        config.append("Dependabot config")

    # Renovate config
    renovate_locations = [
        project_path / "renovate.json",
        project_path / "renovate.json5",
        project_path / ".renovaterc",
        project_path / ".renovaterc.json",
    ]
    if any(p.exists() for p in renovate_locations):
        config.append("Renovate config")

    # Pre-commit hooks
    if (project_path / ".pre-commit-config.yaml").exists():
        config.append("pre-commit")

    # Git hooks directory
    git_hooks = project_path / ".githooks"
    husky_dir = project_path / ".husky"
    if git_hooks.is_dir() or husky_dir.is_dir():
        config.append("git hooks")

    # .gitattributes
    if (project_path / ".gitattributes").exists():
        config.append(".gitattributes")

    return sorted(config)


def detect_runtime_versions(project_path: Path) -> dict[str, str]:
    """Detect pinned runtime/language versions from config files."""
    versions: dict[str, str] = {}

    # Python: .python-version
    python_version_file = project_path / ".python-version"
    if python_version_file.exists():
        ver = python_version_file.read_text(errors="ignore").strip().split("\n")[0].strip()
        if ver:
            versions["Python"] = ver

    # Python: pyproject.toml requires-python
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists() and "Python" not in versions:
        content = pyproject.read_text(errors="ignore")
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("requires-python"):
                # Extract value after = sign, strip quotes
                _, _, val = stripped.partition("=")
                val = val.strip().strip('"').strip("'")
                if val:
                    versions["Python"] = val
                break

    # Node: .node-version
    node_version_file = project_path / ".node-version"
    if node_version_file.exists():
        ver = node_version_file.read_text(errors="ignore").strip().split("\n")[0].strip()
        if ver:
            versions["Node"] = ver

    # Node: .nvmrc
    nvmrc = project_path / ".nvmrc"
    if nvmrc.exists() and "Node" not in versions:
        ver = nvmrc.read_text(errors="ignore").strip().split("\n")[0].strip()
        if ver:
            versions["Node"] = ver

    # Node: package.json engines.node
    pkg_json = project_path / "package.json"
    if pkg_json.exists() and "Node" not in versions:
        try:
            data = json.loads(pkg_json.read_text())
            node_engine = data.get("engines", {}).get("node", "")
            if node_engine:
                versions["Node"] = node_engine
        except (json.JSONDecodeError, KeyError):
            pass

    # Ruby: .ruby-version
    ruby_version_file = project_path / ".ruby-version"
    if ruby_version_file.exists():
        ver = ruby_version_file.read_text(errors="ignore").strip().split("\n")[0].strip()
        if ver:
            versions["Ruby"] = ver

    # Go: go.mod go directive
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        content = go_mod.read_text(errors="ignore")
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("go ") and not stripped.startswith("go."):
                ver = stripped[3:].strip()
                if ver:
                    versions["Go"] = ver
                break

    # Rust: rust-toolchain.toml or rust-toolchain
    rust_toolchain_toml = project_path / "rust-toolchain.toml"
    rust_toolchain = project_path / "rust-toolchain"
    if rust_toolchain_toml.exists():
        content = rust_toolchain_toml.read_text(errors="ignore")
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("channel"):
                _, _, val = stripped.partition("=")
                val = val.strip().strip('"').strip("'")
                if val:
                    versions["Rust"] = val
                break
    elif rust_toolchain.exists():
        ver = rust_toolchain.read_text(errors="ignore").strip().split("\n")[0].strip()
        if ver:
            versions["Rust"] = ver

    # Java: .java-version
    java_version_file = project_path / ".java-version"
    if java_version_file.exists():
        ver = java_version_file.read_text(errors="ignore").strip().split("\n")[0].strip()
        if ver:
            versions["Java"] = ver

    # asdf: .tool-versions
    tool_versions = project_path / ".tool-versions"
    if tool_versions.exists():
        content = tool_versions.read_text(errors="ignore")
        asdf_map = {
            "python": "Python", "nodejs": "Node", "ruby": "Ruby",
            "golang": "Go", "rust": "Rust", "java": "Java",
        }
        for line in content.split("\n"):
            parts = line.strip().split()
            if len(parts) >= 2:
                tool_name = parts[0].lower()
                if tool_name in asdf_map and asdf_map[tool_name] not in versions:
                    versions[asdf_map[tool_name]] = parts[1]

    return versions


def detect_build_tools(project_path: Path) -> list[str]:
    """Detect build tools, task runners, and project automation."""
    tools: list[str] = []

    def _add(name: str) -> None:
        if name not in tools:
            tools.append(name)

    # Makefile
    if (project_path / "Makefile").exists() or (project_path / "makefile").exists():
        _add("Make")

    # Taskfile (go-task)
    for name in ("Taskfile.yml", "Taskfile.yaml", "Taskfile.dist.yml", "Taskfile.dist.yaml"):
        if (project_path / name).exists():
            _add("Taskfile")
            break

    # Just (justfile)
    if (project_path / "justfile").exists() or (project_path / "Justfile").exists():
        _add("Just")

    # Python — tox
    if (project_path / "tox.ini").exists():
        _add("tox")

    # Python — nox
    if (project_path / "noxfile.py").exists():
        _add("nox")

    # Python — Invoke
    if (project_path / "tasks.py").exists():
        _add("Invoke")

    # Python — doit
    if (project_path / "dodo.py").exists():
        _add("doit")

    # JavaScript/TypeScript — npm scripts (check package.json for scripts section)
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(errors="ignore"))
            scripts = data.get("scripts", {})
            if scripts:
                _add("npm scripts")
        except (json.JSONDecodeError, OSError):
            pass

    # Gradle
    if (project_path / "build.gradle").exists() or (project_path / "build.gradle.kts").exists():
        _add("Gradle")

    # Maven
    if (project_path / "pom.xml").exists():
        _add("Maven")

    # CMake
    if (project_path / "CMakeLists.txt").exists():
        _add("CMake")

    # Meson
    if (project_path / "meson.build").exists():
        _add("Meson")

    # Bazel
    if (project_path / "BUILD").exists() or (project_path / "BUILD.bazel").exists() or (project_path / "WORKSPACE").exists():
        _add("Bazel")

    # Rake (Ruby)
    if (project_path / "Rakefile").exists():
        _add("Rake")

    # Earthly
    if (project_path / "Earthfile").exists():
        _add("Earthly")

    return sorted(tools)


def detect_api_specs(project_path: Path) -> list[str]:
    """Detect API specification formats and protocols."""
    specs: list[str] = []

    def _add(name: str) -> None:
        if name not in specs:
            specs.append(name)

    # OpenAPI / Swagger — check common file names and locations
    openapi_names = [
        "openapi.json", "openapi.yaml", "openapi.yml",
        "swagger.json", "swagger.yaml", "swagger.yml",
    ]
    for name in openapi_names:
        if (project_path / name).exists():
            _add("OpenAPI")
            break
    # Also check docs/ and api/ subdirectories
    if "OpenAPI" not in specs:
        for subdir in ("docs", "api", "spec"):
            d = project_path / subdir
            if d.is_dir():
                for name in openapi_names:
                    if (d / name).exists():
                        _add("OpenAPI")
                        break
            if "OpenAPI" in specs:
                break

    # GraphQL — schema files and config
    graphql_indicators = [
        "schema.graphql", "schema.gql",
        ".graphqlrc", ".graphqlrc.yml", ".graphqlrc.yaml", ".graphqlrc.json",
        "codegen.yml", "codegen.yaml", "codegen.ts",
    ]
    for name in graphql_indicators:
        if (project_path / name).exists():
            _add("GraphQL")
            break
    # Check for .graphql files in src/
    if "GraphQL" not in specs:
        src = project_path / "src"
        if src.is_dir():
            for f in src.rglob("*.graphql"):
                _add("GraphQL")
                break

    # gRPC / Protocol Buffers
    proto_found = False
    for pattern_dir in [project_path, project_path / "proto", project_path / "protos"]:
        if pattern_dir.is_dir():
            for f in pattern_dir.glob("*.proto"):
                proto_found = True
                break
        if proto_found:
            break
    if proto_found:
        _add("gRPC/Protobuf")

    # AsyncAPI — event-driven API specs
    asyncapi_names = [
        "asyncapi.json", "asyncapi.yaml", "asyncapi.yml",
    ]
    for name in asyncapi_names:
        if (project_path / name).exists():
            _add("AsyncAPI")
            break

    # JSON Schema — standalone schema definitions
    for name in ("schema.json", "schemas"):
        p = project_path / name
        if p.exists():
            _add("JSON Schema")
            break

    # tRPC — check package.json dependencies
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(errors="ignore"))
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if any(k.startswith("@trpc/") for k in all_deps):
                _add("tRPC")
        except (json.JSONDecodeError, OSError):
            pass

    # WSDL — SOAP web services
    for f in project_path.glob("*.wsdl"):
        _add("WSDL/SOAP")
        break

    return sorted(specs)


def detect_monitoring_tools(project_path: Path) -> list[str]:
    """Detect monitoring, observability, and error tracking tools."""
    tools: list[str] = []

    def _add(name: str) -> None:
        if name not in tools:
            tools.append(name)

    # Python dependencies
    for cfg in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            _check_add(tools, content, "sentry-sdk", "Sentry")
            _check_add(tools, content, "sentry_sdk", "Sentry")
            _check_add(tools, content, "ddtrace", "Datadog")
            _check_add(tools, content, "datadog", "Datadog")
            _check_add(tools, content, "newrelic", "New Relic")
            _check_add(tools, content, "opentelemetry", "OpenTelemetry")
            _check_add(tools, content, "prometheus-client", "Prometheus")
            _check_add(tools, content, "prometheus_client", "Prometheus")
            _check_add(tools, content, "grafana", "Grafana")
            _check_add(tools, content, "elastic-apm", "Elastic APM")
            _check_add(tools, content, "bugsnag", "Bugsnag")
            _check_add(tools, content, "rollbar", "Rollbar")
            _check_add(tools, content, "honeycomb", "Honeycomb")
            _check_add(tools, content, "loguru", "Loguru")
            _check_add(tools, content, "structlog", "structlog")

    # JavaScript/TypeScript dependencies
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(errors="ignore"))
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            js_monitoring = {
                "@sentry/node": "Sentry",
                "@sentry/browser": "Sentry",
                "@sentry/react": "Sentry",
                "@sentry/nextjs": "Sentry",
                "dd-trace": "Datadog",
                "newrelic": "New Relic",
                "@opentelemetry/api": "OpenTelemetry",
                "@opentelemetry/sdk-node": "OpenTelemetry",
                "prom-client": "Prometheus",
                "@bugsnag/js": "Bugsnag",
                "@bugsnag/node": "Bugsnag",
                "rollbar": "Rollbar",
                "@honeycombio/opentelemetry-node": "Honeycomb",
                "pino": "Pino",
                "winston": "Winston",
                "@logtail/node": "Logtail",
                "logrocket": "LogRocket",
            }
            for dep, name in js_monitoring.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    # Go dependencies
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        content = go_mod.read_text(errors="ignore").lower()
        _check_add(tools, content, "sentry-go", "Sentry")
        _check_add(tools, content, "opentelemetry", "OpenTelemetry")
        _check_add(tools, content, "prometheus", "Prometheus")
        _check_add(tools, content, "datadog", "Datadog")

    # Rust dependencies
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        content = cargo_toml.read_text(errors="ignore").lower()
        _check_add(tools, content, "sentry", "Sentry")
        _check_add(tools, content, "opentelemetry", "OpenTelemetry")
        _check_add(tools, content, "tracing", "tracing")
        _check_add(tools, content, "prometheus", "Prometheus")

    # Config files for monitoring services
    if (project_path / "sentry.properties").exists() or (project_path / ".sentryclirc").exists():
        _add("Sentry")
    if (project_path / "newrelic.yml").exists() or (project_path / "newrelic.js").exists():
        _add("New Relic")
    if (project_path / "datadog.yaml").exists() or (project_path / "dd-conf.yaml").exists():
        _add("Datadog")
    if (project_path / "prometheus.yml").exists() or (project_path / "prometheus.yaml").exists():
        _add("Prometheus")
    if (project_path / "otel-collector-config.yaml").exists():
        _add("OpenTelemetry")

    return sorted(tools)


def detect_auth_tools(project_path: Path) -> list[str]:
    """Detect authentication and authorization frameworks."""
    tools: list[str] = []

    def _add(name: str) -> None:
        if name not in tools:
            tools.append(name)

    # Python dependencies
    for cfg in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            _check_add(tools, content, "flask-login", "Flask-Login")
            _check_add(tools, content, "flask-security", "Flask-Security")
            _check_add(tools, content, "django-allauth", "django-allauth")
            _check_add(tools, content, "django-rest-framework", "DRF Auth")
            _check_add(tools, content, "djangorestframework-simplejwt", "DRF SimpleJWT")
            _check_add(tools, content, "authlib", "Authlib")
            _check_add(tools, content, "python-jose", "python-jose")
            _check_add(tools, content, "pyjwt", "PyJWT")
            _check_add(tools, content, "passlib", "Passlib")
            _check_add(tools, content, "python-oauth2", "OAuth2")
            _check_add(tools, content, "fastapi-users", "FastAPI-Users")
            _check_add(tools, content, "auth0-python", "Auth0")
            _check_add(tools, content, "firebase-admin", "Firebase Auth")
            _check_add(tools, content, "clerk-backend-api", "Clerk")
            _check_add(tools, content, "supabase", "Supabase Auth")

    # JavaScript/TypeScript dependencies
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(errors="ignore"))
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            js_auth = {
                "next-auth": "NextAuth.js",
                "@auth/core": "Auth.js",
                "passport": "Passport.js",
                "express-session": "express-session",
                "jsonwebtoken": "jsonwebtoken",
                "@clerk/nextjs": "Clerk",
                "@clerk/clerk-react": "Clerk",
                "@clerk/express": "Clerk",
                "auth0-js": "Auth0",
                "@auth0/auth0-react": "Auth0",
                "@auth0/nextjs-auth0": "Auth0",
                "firebase": "Firebase Auth",
                "@supabase/supabase-js": "Supabase Auth",
                "@supabase/auth-helpers-nextjs": "Supabase Auth",
                "lucia": "Lucia",
                "lucia-auth": "Lucia",
                "@lucia-auth/adapter-prisma": "Lucia",
                "bcryptjs": "bcrypt",
                "bcrypt": "bcrypt",
                "keycloak-js": "Keycloak",
                "@keycloak/keycloak-admin-client": "Keycloak",
                "oidc-client-ts": "OIDC",
                "openid-client": "OIDC",
                "grant": "Grant",
            }
            for dep, name in js_auth.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    # Go dependencies
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        content = go_mod.read_text(errors="ignore").lower()
        _check_add(tools, content, "golang-jwt", "golang-jwt")
        _check_add(tools, content, "casbin", "Casbin")
        _check_add(tools, content, "authelia", "Authelia")
        _check_add(tools, content, "coreos/go-oidc", "OIDC")

    # Rust dependencies
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        content = cargo_toml.read_text(errors="ignore").lower()
        _check_add(tools, content, "jsonwebtoken", "jsonwebtoken")
        _check_add(tools, content, "oauth2", "OAuth2")
        _check_add(tools, content, "actix-identity", "Actix Identity")
        _check_add(tools, content, "axum-login", "axum-login")

    return sorted(tools)


def detect_messaging_tools(project_path: Path) -> list[str]:
    """Detect messaging, email, SMS, push notification, and real-time tools."""
    tools: list[str] = []

    def _add(name: str) -> None:
        if name not in tools:
            tools.append(name)

    # Python dependencies
    for cfg in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        path = project_path / cfg
        if path.exists():
            content = path.read_text(errors="ignore").lower()
            _check_add(tools, content, "sendgrid", "SendGrid")
            _check_add(tools, content, "postmarker", "Postmark")
            _check_add(tools, content, "mailgun", "Mailgun")
            _check_add(tools, content, "resend", "Resend")
            _check_add(tools, content, "twilio", "Twilio")
            _check_add(tools, content, "slack-sdk", "Slack")
            _check_add(tools, content, "slack-bolt", "Slack")
            _check_add(tools, content, "slack_sdk", "Slack")
            _check_add(tools, content, "slack_bolt", "Slack")
            _check_add(tools, content, "python-socketio", "Socket.IO")
            _check_add(tools, content, "pusher", "Pusher")
            _check_add(tools, content, "firebase-admin", "Firebase Cloud Messaging")
            _check_add(tools, content, "web-push", "Web Push")
            _check_add(tools, content, "celery", "Celery")

    # JavaScript/TypeScript dependencies
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(errors="ignore"))
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            js_messaging = {
                "@sendgrid/mail": "SendGrid",
                "nodemailer": "Nodemailer",
                "@resend/node": "Resend",
                "resend": "Resend",
                "twilio": "Twilio",
                "@slack/web-api": "Slack",
                "@slack/bolt": "Slack",
                "pusher": "Pusher",
                "pusher-js": "Pusher",
                "socket.io": "Socket.IO",
                "socket.io-client": "Socket.IO",
                "firebase-admin": "Firebase Cloud Messaging",
                "web-push": "Web Push",
                "bullmq": "BullMQ",
                "bull": "Bull",
                "@novu/node": "Novu",
                "postmark": "Postmark",
            }
            for dep, name in js_messaging.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    # Go dependencies
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        content = go_mod.read_text(errors="ignore").lower()
        _check_add(tools, content, "slack-go/slack", "Slack")
        _check_add(tools, content, "gomail", "Gomail")
        _check_add(tools, content, "twilio-go", "Twilio")

    # Rust dependencies
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        content = cargo_toml.read_text(errors="ignore").lower()
        _check_add(tools, content, "lettre", "Lettre")
        _check_add(tools, content, "slack-morphism", "Slack")

    return sorted(tools)


def detect_deploy_targets(project_path: Path) -> list[str]:
    """Detect deployment platforms and hosting targets."""
    targets: list[str] = []

    def _add(name: str) -> None:
        if name not in targets:
            targets.append(name)

    # Vercel
    if (project_path / "vercel.json").exists() or (project_path / ".vercel").is_dir():
        _add("Vercel")

    # Netlify
    if (project_path / "netlify.toml").exists() or (project_path / "_redirects").exists():
        _add("Netlify")

    # Fly.io
    if (project_path / "fly.toml").exists():
        _add("Fly.io")

    # Railway
    if (project_path / "railway.json").exists() or (project_path / "railway.toml").exists():
        _add("Railway")

    # Render
    if (project_path / "render.yaml").exists():
        _add("Render")

    # Heroku
    if (project_path / "Procfile").exists():
        _add("Heroku")

    # Firebase Hosting
    if (project_path / "firebase.json").exists():
        _add("Firebase Hosting")

    # AWS Amplify
    if (project_path / "amplify.yml").exists() or (project_path / "amplify").is_dir():
        _add("AWS Amplify")

    # Serverless Framework
    if (project_path / "serverless.yml").exists() or (project_path / "serverless.yaml").exists():
        _add("Serverless Framework")

    # Google App Engine
    app_yaml = project_path / "app.yaml"
    if app_yaml.exists():
        try:
            content = app_yaml.read_text(errors="ignore")
            if "runtime:" in content:
                _add("Google App Engine")
        except OSError:
            pass

    # DigitalOcean App Platform
    if (project_path / ".do").is_dir() or (project_path / "do-app.yaml").exists():
        _add("DigitalOcean App Platform")

    # Cloudflare Workers
    if (project_path / "wrangler.toml").exists() or (project_path / "wrangler.jsonc").exists():
        _add("Cloudflare Workers")

    # GitHub Pages
    gh_workflows = project_path / ".github" / "workflows"
    if gh_workflows.is_dir():
        try:
            for wf in gh_workflows.iterdir():
                if wf.suffix in (".yml", ".yaml"):
                    content = wf.read_text(errors="ignore").lower()
                    if "pages" in content and ("deploy" in content or "gh-pages" in content):
                        _add("GitHub Pages")
                        break
        except OSError:
            pass

    # Package.json deploy hints
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(errors="ignore"))
            scripts = data.get("scripts", {})
            all_scripts = " ".join(str(v) for v in scripts.values()).lower()
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "@vercel/node" in deps or "vercel" in deps:
                _add("Vercel")
            if "netlify-cli" in deps or "@netlify/functions" in deps:
                _add("Netlify")
            if "wrangler" in deps:
                _add("Cloudflare Workers")
            if "firebase-tools" in deps:
                _add("Firebase Hosting")
            if "gh-pages" in deps or "gh-pages" in all_scripts:
                _add("GitHub Pages")
        except (json.JSONDecodeError, OSError):
            pass

    return sorted(targets)


def detect_state_management(project_path: Path) -> list[str]:
    """Detect frontend state management libraries."""
    tools: list[str] = []

    def _add(name: str) -> None:
        if name not in tools:
            tools.append(name)

    # JavaScript/TypeScript dependencies
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text(errors="ignore"))
            all_deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            js_state = {
                # React ecosystem
                "redux": "Redux",
                "@reduxjs/toolkit": "Redux",
                "react-redux": "Redux",
                "zustand": "Zustand",
                "recoil": "Recoil",
                "jotai": "Jotai",
                "valtio": "Valtio",
                "mobx": "MobX",
                "mobx-react": "MobX",
                "mobx-react-lite": "MobX",
                "xstate": "XState",
                "@xstate/react": "XState",
                # Vue ecosystem
                "pinia": "Pinia",
                "vuex": "Vuex",
                # Angular ecosystem
                "@ngrx/store": "NgRx",
                "@ngrx/effects": "NgRx",
                # Signals
                "@preact/signals-react": "Signals",
                "@preact/signals": "Signals",
                "@angular/core": None,  # handled separately
                # Other
                "effector": "Effector",
                "effector-react": "Effector",
                "nanostores": "Nanostores",
                "@nanostores/react": "Nanostores",
                "legend-state": "Legend State",
                "@legendapp/state": "Legend State",
            }
            for dep, name in js_state.items():
                if dep in all_deps and name is not None:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    return sorted(tools)


def detect_css_frameworks(project_path: Path) -> list[str]:
    """Detect CSS and styling frameworks."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Config file detection
    config_files = {
        "tailwind.config.js": "Tailwind CSS",
        "tailwind.config.ts": "Tailwind CSS",
        "tailwind.config.mjs": "Tailwind CSS",
        "tailwind.config.cjs": "Tailwind CSS",
        "postcss.config.js": "PostCSS",
        "postcss.config.cjs": "PostCSS",
        "postcss.config.mjs": "PostCSS",
        ".postcssrc": "PostCSS",
        ".postcssrc.json": "PostCSS",
        "stylelint.config.js": "Stylelint",
        "stylelint.config.cjs": "Stylelint",
        "stylelint.config.mjs": "Stylelint",
        ".stylelintrc": "Stylelint",
        ".stylelintrc.json": "Stylelint",
    }
    for filename, name in config_files.items():
        if (project_path / filename).exists():
            _add(name)

    # Sass detection — .scss/.sass files or config
    sass_extensions = {".scss", ".sass"}
    for child in project_path.iterdir():
        if child.is_file() and child.suffix in sass_extensions:
            _add("Sass")
            break
    # Also check src/ for Sass
    src_dir = project_path / "src"
    if src_dir.is_dir() and "Sass" not in seen:
        for child in src_dir.iterdir():
            if child.is_file() and child.suffix in sass_extensions:
                _add("Sass")
                break

    # Less detection
    for child in project_path.iterdir():
        if child.is_file() and child.suffix == ".less":
            _add("Less")
            break
    if (project_path / "src").is_dir() and "Less" not in seen:
        for child in (project_path / "src").iterdir():
            if child.is_file() and child.suffix == ".less":
                _add("Less")
                break

    # CSS Modules detection — *.module.css or *.module.scss
    for check_dir in [project_path, src_dir]:
        if check_dir.is_dir() and "CSS Modules" not in seen:
            for child in check_dir.iterdir():
                if child.is_file() and (".module.css" in child.name or ".module.scss" in child.name):
                    _add("CSS Modules")
                    break

    # package.json dependency detection
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps: set[str] = set()
            for key in ("dependencies", "devDependencies"):
                all_deps.update(data.get(key, {}).keys())

            js_css = {
                "tailwindcss": "Tailwind CSS",
                "@tailwindcss/typography": "Tailwind CSS",
                "styled-components": "Styled Components",
                "@emotion/react": "Emotion",
                "@emotion/styled": "Emotion",
                "@emotion/css": "Emotion",
                "sass": "Sass",
                "node-sass": "Sass",
                "less": "Less",
                "stylus": "Stylus",
                "postcss": "PostCSS",
                "autoprefixer": "PostCSS",
                "stylelint": "Stylelint",
                "@vanilla-extract/css": "Vanilla Extract",
                "@vanilla-extract/recipes": "Vanilla Extract",
                "linaria": "Linaria",
                "@linaria/core": "Linaria",
                "twin.macro": "Twin Macro",
                "stitches": "Stitches",
                "@stitches/react": "Stitches",
                "panda-css": "Panda CSS",
                "@pandacss/dev": "Panda CSS",
                "unocss": "UnoCSS",
                "@unocss/preset-uno": "UnoCSS",
                "windicss": "Windi CSS",
                "bootstrap": "Bootstrap",
                "react-bootstrap": "Bootstrap",
                "@ng-bootstrap/ng-bootstrap": "Bootstrap",
                "bulma": "Bulma",
                "@chakra-ui/react": "Chakra UI",
                "@mantine/core": "Mantine",
                "@mui/material": "Material UI",
                "@mui/system": "Material UI",
                "vuetify": "Vuetify",
                "ant-design-vue": "Ant Design",
                "antd": "Ant Design",
                "@radix-ui/themes": "Radix UI",
                "shadcn-ui": "shadcn/ui",
            }
            for dep, name in js_css.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    return sorted(tools)


def detect_bundlers(project_path: Path) -> list[str]:
    """Detect JavaScript/TypeScript bundlers and module tools."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Config file detection
    config_files = {
        "webpack.config.js": "Webpack",
        "webpack.config.ts": "Webpack",
        "webpack.config.cjs": "Webpack",
        "webpack.config.mjs": "Webpack",
        "vite.config.js": "Vite",
        "vite.config.ts": "Vite",
        "vite.config.mjs": "Vite",
        "rollup.config.js": "Rollup",
        "rollup.config.ts": "Rollup",
        "rollup.config.mjs": "Rollup",
        ".parcelrc": "Parcel",
        "turbo.json": "Turborepo",
        ".swcrc": "SWC",
        "rspack.config.js": "Rspack",
        "rspack.config.ts": "Rspack",
        "tsup.config.ts": "tsup",
        "tsup.config.js": "tsup",
    }
    for filename, name in config_files.items():
        if (project_path / filename).exists():
            _add(name)

    # package.json dependency detection
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps: set[str] = set()
            for key in ("dependencies", "devDependencies"):
                all_deps.update(data.get(key, {}).keys())

            js_bundlers = {
                "webpack": "Webpack",
                "webpack-cli": "Webpack",
                "vite": "Vite",
                "esbuild": "esbuild",
                "rollup": "Rollup",
                "parcel": "Parcel",
                "parcel-bundler": "Parcel",
                "@swc/core": "SWC",
                "@swc/cli": "SWC",
                "turbopack": "Turbopack",
                "@rspack/core": "Rspack",
                "@rspack/cli": "Rspack",
                "tsup": "tsup",
                "unbuild": "unbuild",
                "microbundle": "microbundle",
                "bun": "Bun",
                "rome": "Rome",
                "snowpack": "Snowpack",
                "wmr": "WMR",
            }
            for dep, name in js_bundlers.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    return sorted(tools)


def detect_orm_tools(project_path: Path) -> list[str]:
    """Detect ORM and database client libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Config file detection
    config_files = {
        "ormconfig.js": "TypeORM",
        "ormconfig.ts": "TypeORM",
        "ormconfig.json": "TypeORM",
        "mikro-orm.config.ts": "MikroORM",
        "mikro-orm.config.js": "MikroORM",
        "drizzle.config.ts": "Drizzle",
        "drizzle.config.js": "Drizzle",
        "knexfile.js": "Knex",
        "knexfile.ts": "Knex",
    }
    for filename, name in config_files.items():
        if (project_path / filename).exists():
            _add(name)

    # Prisma schema
    prisma_schema = project_path / "prisma" / "schema.prisma"
    if prisma_schema.exists():
        _add("Prisma")

    # Python deps (pyproject.toml, requirements.txt)
    py_orm_deps = {
        "sqlalchemy": "SQLAlchemy",
        "sqlmodel": "SQLModel",
        "django": "Django ORM",
        "peewee": "Peewee",
        "tortoise-orm": "Tortoise ORM",
        "pony": "Pony ORM",
        "asyncpg": "asyncpg",
        "psycopg2": "psycopg2",
        "psycopg2-binary": "psycopg2",
        "psycopg": "psycopg",
        "pymongo": "PyMongo",
        "motor": "Motor",
        "mongoengine": "MongoEngine",
        "redis": "redis-py",
        "aioredis": "aioredis",
        "databases": "databases",
        "alembic": "Alembic",
    }
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text().lower()
            for dep, name in py_orm_deps.items():
                if dep in content:
                    _add(name)
        except OSError:
            pass

    for req_file in ("requirements.txt", "requirements-dev.txt", "requirements.in"):
        req_path = project_path / req_file
        if req_path.exists():
            try:
                content = req_path.read_text().lower()
                for dep, name in py_orm_deps.items():
                    if dep in content:
                        _add(name)
            except OSError:
                pass

    # package.json dependency detection
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps: set[str] = set()
            for key in ("dependencies", "devDependencies"):
                all_deps.update(data.get(key, {}).keys())

            js_orm_deps = {
                "prisma": "Prisma",
                "@prisma/client": "Prisma",
                "typeorm": "TypeORM",
                "sequelize": "Sequelize",
                "drizzle-orm": "Drizzle",
                "knex": "Knex",
                "mongoose": "Mongoose",
                "bookshelf": "Bookshelf",
                "objection": "Objection.js",
                "@mikro-orm/core": "MikroORM",
                "kysely": "Kysely",
                "better-sqlite3": "better-sqlite3",
                "pg": "node-postgres",
                "ioredis": "ioredis",
                "mongodb": "MongoDB Driver",
            }
            for dep, name in js_orm_deps.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    # Go modules (go.mod)
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            go_orm_deps = {
                "gorm.io/gorm": "GORM",
                "github.com/jmoiron/sqlx": "sqlx (Go)",
                "entgo.io/ent": "ent",
                "github.com/jackc/pgx": "pgx",
                "github.com/sqlc-dev/sqlc": "sqlc",
                "github.com/uptrace/bun": "Bun (Go)",
            }
            for dep, name in go_orm_deps.items():
                if dep in content:
                    _add(name)
        except OSError:
            pass

    # Rust (Cargo.toml)
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            rust_orm_deps = {
                "diesel": "Diesel",
                "sqlx": "sqlx (Rust)",
                "sea-orm": "SeaORM",
                "rusqlite": "Rusqlite",
            }
            for dep, name in rust_orm_deps.items():
                if dep in content:
                    _add(name)
        except OSError:
            pass

    # Java (build.gradle, pom.xml)
    for gradle_file in ("build.gradle", "build.gradle.kts"):
        gradle = project_path / gradle_file
        if gradle.exists():
            try:
                content = gradle.read_text().lower()
                if "hibernate" in content:
                    _add("Hibernate")
                if "mybatis" in content:
                    _add("MyBatis")
                if "jooq" in content:
                    _add("jOOQ")
                if "spring-data-jpa" in content or "spring-boot-starter-data-jpa" in content:
                    _add("Spring Data JPA")
                if "jdbi" in content:
                    _add("JDBI")
            except OSError:
                pass
    pom = project_path / "pom.xml"
    if pom.exists():
        try:
            content = pom.read_text().lower()
            if "hibernate" in content:
                _add("Hibernate")
            if "mybatis" in content:
                _add("MyBatis")
            if "jooq" in content:
                _add("jOOQ")
            if "spring-data-jpa" in content:
                _add("Spring Data JPA")
            if "jdbi" in content:
                _add("JDBI")
        except OSError:
            pass

    return sorted(tools)


def detect_i18n_tools(project_path: Path) -> list[str]:
    """Detect internationalization and localization tools."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Directory-based detection
    i18n_dirs = ("locales", "locale", "translations", "i18n", "lang", "messages")
    for d in i18n_dirs:
        if (project_path / d).is_dir():
            _add("Locale Files")
            break

    # Config file detection
    config_files = {
        "lingui.config.js": "Lingui",
        "lingui.config.ts": "Lingui",
        ".linguirc": "Lingui",
        "babel.cfg": "Babel (i18n)",
        "i18next-parser.config.js": "i18next",
        "i18next-parser.config.ts": "i18next",
    }
    for filename, name in config_files.items():
        if (project_path / filename).exists():
            _add(name)

    # Python deps
    py_i18n_deps = {
        "babel": "Babel (i18n)",
        "flask-babel": "Flask-Babel",
        "django-modeltranslation": "django-modeltranslation",
        "django-rosetta": "django-rosetta",
        "python-i18n": "python-i18n",
    }
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text().lower()
            for dep, name in py_i18n_deps.items():
                if dep in content:
                    _add(name)
        except OSError:
            pass

    for req_file in ("requirements.txt", "requirements-dev.txt"):
        req_path = project_path / req_file
        if req_path.exists():
            try:
                content = req_path.read_text().lower()
                for dep, name in py_i18n_deps.items():
                    if dep in content:
                        _add(name)
            except OSError:
                pass

    # package.json dependency detection
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps: set[str] = set()
            for key in ("dependencies", "devDependencies"):
                all_deps.update(data.get(key, {}).keys())

            js_i18n_deps = {
                "i18next": "i18next",
                "react-i18next": "react-i18next",
                "next-i18next": "next-i18next",
                "next-intl": "next-intl",
                "react-intl": "react-intl",
                "@formatjs/intl": "FormatJS",
                "vue-i18n": "vue-i18n",
                "@angular/localize": "Angular i18n",
                "@lingui/core": "Lingui",
                "@lingui/react": "Lingui",
                "typesafe-i18n": "typesafe-i18n",
                "rosetta": "rosetta",
                "polyglot": "Polyglot",
                "globalize": "Globalize",
            }
            for dep, name in js_i18n_deps.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    # Go modules
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            if "golang.org/x/text" in content:
                _add("Go x/text")
            if "github.com/nicksnyder/go-i18n" in content:
                _add("go-i18n")
        except OSError:
            pass

    # Rust (Cargo.toml)
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "fluent" in content:
                _add("Fluent")
            if "rust-i18n" in content:
                _add("rust-i18n")
        except OSError:
            pass

    return sorted(tools)


def detect_validation_tools(project_path: Path) -> list[str]:
    """Detect validation and schema libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Python deps
    py_deps = {
        "pydantic": "Pydantic",
        "marshmallow": "marshmallow",
        "cerberus": "Cerberus",
        "attrs": "attrs",
        "cattrs": "cattrs",
        "voluptuous": "Voluptuous",
        "schema": "schema",
        "jsonschema": "jsonschema",
        "colander": "Colander",
        "schematics": "Schematics",
    }
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text().lower()
            for dep, name in py_deps.items():
                if dep in content:
                    _add(name)
        except OSError:
            pass

    for req_file in ("requirements.txt", "requirements-dev.txt"):
        req_path = project_path / req_file
        if req_path.exists():
            try:
                content = req_path.read_text().lower()
                for dep, name in py_deps.items():
                    if dep in content:
                        _add(name)
            except OSError:
                pass

    # package.json dependency detection
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps: set[str] = set()
            for key in ("dependencies", "devDependencies"):
                all_deps.update(data.get(key, {}).keys())

            js_deps = {
                "zod": "Zod",
                "yup": "Yup",
                "joi": "Joi",
                "class-validator": "class-validator",
                "class-transformer": "class-transformer",
                "ajv": "Ajv",
                "superstruct": "Superstruct",
                "valibot": "Valibot",
                "io-ts": "io-ts",
                "@sinclair/typebox": "TypeBox",
                "vest": "Vest",
                "myzod": "myZod",
                "@effect/schema": "Effect Schema",
                "arktype": "ArkType",
            }
            for dep, name in js_deps.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    # Go modules
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            if "github.com/go-playground/validator" in content:
                _add("go-playground/validator")
            if "github.com/go-ozzo/ozzo-validation" in content:
                _add("ozzo-validation")
        except OSError:
            pass

    # Rust (Cargo.toml)
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "validator" in content:
                _add("validator (Rust)")
            if "garde" in content:
                _add("garde")
        except OSError:
            pass

    # Java (build.gradle, pom.xml)
    for gradle_file in ("build.gradle", "build.gradle.kts"):
        gradle = project_path / gradle_file
        if gradle.exists():
            try:
                content = gradle.read_text().lower()
                if "hibernate-validator" in content:
                    _add("Hibernate Validator")
                if "jakarta.validation" in content or "javax.validation" in content:
                    _add("Jakarta Validation")
            except OSError:
                pass
    pom = project_path / "pom.xml"
    if pom.exists():
        try:
            content = pom.read_text().lower()
            if "hibernate-validator" in content:
                _add("Hibernate Validator")
            if "jakarta.validation" in content or "javax.validation" in content:
                _add("Jakarta Validation")
        except OSError:
            pass

    return sorted(tools)


def detect_logging_tools(project_path: Path) -> list[str]:
    """Detect logging and structured logging frameworks."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str):
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Python (pyproject.toml, requirements.txt)
    py_deps = {
        "loguru": "Loguru",
        "structlog": "structlog",
        "python-json-logger": "python-json-logger",
        "logging-tree": "logging-tree",
        "coloredlogs": "coloredlogs",
        "rich": "Rich (logging)",
        "logbook": "Logbook",
        "eliot": "Eliot",
        "twiggy": "Twiggy",
    }
    for cfg in ("pyproject.toml", "requirements.txt"):
        f = project_path / cfg
        if f.exists():
            try:
                content = f.read_text().lower()
                for dep, name in py_deps.items():
                    if dep in content:
                        _add(name)
            except OSError:
                pass

    # JavaScript / TypeScript (package.json)
    pkg = project_path / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text())
            all_deps = set()
            for section in ("dependencies", "devDependencies"):
                all_deps.update(data.get(section, {}).keys())

            js_deps = {
                "winston": "Winston",
                "pino": "Pino",
                "bunyan": "Bunyan",
                "log4js": "log4js",
                "loglevel": "loglevel",
                "signale": "Signale",
                "consola": "Consola",
                "roarr": "Roarr",
                "tslog": "tslog",
                "winston-daily-rotate-file": "Winston Rotate",
                "morgan": "Morgan",
                "debug": "debug",
            }
            for dep, name in js_deps.items():
                if dep in all_deps:
                    _add(name)
        except (json.JSONDecodeError, OSError):
            pass

    # Go (go.mod)
    gomod = project_path / "go.mod"
    if gomod.exists():
        try:
            content = gomod.read_text()
            go_deps = {
                "go.uber.org/zap": "Zap",
                "github.com/sirupsen/logrus": "Logrus",
                "github.com/rs/zerolog": "zerolog",
                "log/slog": "slog",
                "golang.org/x/exp/slog": "slog",
            }
            for dep, name in go_deps.items():
                if dep in content:
                    _add(name)
        except OSError:
            pass

    # Rust (Cargo.toml)
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "tracing" in content:
                _add("tracing (Rust)")
            if "env_logger" in content:
                _add("env_logger")
            if "log4rs" in content:
                _add("log4rs")
            if "fern" in content:
                _add("fern")
            if "slog" in content:
                _add("slog (Rust)")
        except OSError:
            pass

    # Java (build.gradle, pom.xml)
    java_deps = {
        "logback": "Logback",
        "log4j": "Log4j",
        "slf4j": "SLF4J",
    }
    for gradle_file in ("build.gradle", "build.gradle.kts"):
        gradle = project_path / gradle_file
        if gradle.exists():
            try:
                content = gradle.read_text().lower()
                for dep, name in java_deps.items():
                    if dep in content:
                        _add(name)
            except OSError:
                pass
    pom = project_path / "pom.xml"
    if pom.exists():
        try:
            content = pom.read_text().lower()
            for dep, name in java_deps.items():
                if dep in content:
                    _add(name)
        except OSError:
            pass

    return sorted(tools)


def detect_container_orchestration(project_path: Path) -> list[str]:
    """Detect container orchestration and infrastructure-as-code tools."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str):
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Docker Compose
    for name in ("docker-compose.yml", "docker-compose.yaml",
                 "compose.yml", "compose.yaml"):
        if (project_path / name).exists():
            _add("Docker Compose")
            break

    # Kubernetes manifests
    k8s_dirs = ("k8s", "kubernetes", "kube", "manifests", "deploy")
    for d in k8s_dirs:
        if (project_path / d).is_dir():
            _add("Kubernetes")
            break

    # Helm charts
    if (project_path / "Chart.yaml").exists() or (project_path / "charts").is_dir():
        _add("Helm")

    # Kustomize
    if (project_path / "kustomization.yaml").exists() or (project_path / "kustomization.yml").exists():
        _add("Kustomize")

    # Skaffold
    if (project_path / "skaffold.yaml").exists() or (project_path / "skaffold.yml").exists():
        _add("Skaffold")

    # Tilt
    if (project_path / "Tiltfile").exists():
        _add("Tilt")

    # Terraform
    for f in project_path.iterdir():
        if f.suffix == ".tf" and f.is_file():
            _add("Terraform")
            break

    # Pulumi
    if (project_path / "Pulumi.yaml").exists() or (project_path / "Pulumi.yml").exists():
        _add("Pulumi")

    # Ansible
    for name in ("ansible.cfg", "playbook.yml", "playbook.yaml"):
        if (project_path / name).exists():
            _add("Ansible")
            break
    if (project_path / "playbooks").is_dir() or (project_path / "roles").is_dir():
        _add("Ansible")

    # Nomad
    for f in project_path.iterdir():
        if f.suffix == ".nomad" and f.is_file():
            _add("Nomad")
            break
    if (project_path / "nomad").is_dir():
        _add("Nomad")

    # Docker Swarm (docker-stack.yml)
    for name in ("docker-stack.yml", "docker-stack.yaml"):
        if (project_path / name).exists():
            _add("Docker Swarm")
            break

    # Vagrant
    if (project_path / "Vagrantfile").exists():
        _add("Vagrant")

    # Packer
    for f in project_path.iterdir():
        if f.name.endswith(".pkr.hcl") and f.is_file():
            _add("Packer")
            break

    return sorted(tools)


def detect_cloud_providers(project_path: Path) -> list[str]:
    """Detect cloud provider SDKs and services."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str):
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Python deps
    pyproject = project_path / "pyproject.toml"
    reqs_txt = project_path / "requirements.txt"
    py_deps: set[str] = set()
    if pyproject.exists():
        try:
            content = pyproject.read_text()
            for line in content.splitlines():
                cleaned = line.strip().strip('",\' ').lower()
                if cleaned:
                    dep = cleaned.split("[")[0].split(">=")[0].split("==")[0].split("<")[0].split(">")[0].split("~=")[0].strip()
                    if dep and not dep.startswith(("[", "#", "{")) and "=" not in dep:
                        py_deps.add(dep)
        except Exception:
            pass
    if reqs_txt.exists():
        try:
            for line in reqs_txt.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    dep = line.split(">=")[0].split("==")[0].split("<")[0].split(">")[0].split("[")[0].strip()
                    py_deps.add(dep.lower())
        except Exception:
            pass

    # AWS
    aws_py = {"boto3", "botocore", "aws-cdk-lib", "aws-cdk.core", "moto", "aiobotocore",
              "aws-lambda-powertools", "troposphere", "sagemaker"}
    if py_deps & aws_py:
        _add("AWS")

    # GCP
    gcp_py = {"google-cloud-storage", "google-cloud-bigquery", "google-cloud-firestore",
              "google-cloud-pubsub", "google-cloud-logging", "google-cloud-compute",
              "google-api-python-client", "firebase-admin", "google-cloud-aiplatform"}
    if py_deps & gcp_py:
        _add("GCP")

    # Azure
    azure_py = {"azure-storage-blob", "azure-identity", "azure-cosmos", "azure-functions",
                "azure-mgmt-compute", "azure-servicebus", "azure-keyvault-secrets",
                "azure-ai-ml", "azure-core"}
    if py_deps & azure_py:
        _add("Azure")

    # JS/TS deps
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = __import__("json").loads(pkg_json.read_text())
            all_deps: set[str] = set()
            for key in ("dependencies", "devDependencies"):
                all_deps.update(data.get(key, {}).keys())

            # AWS
            aws_js = {"@aws-sdk/client-s3", "@aws-sdk/client-dynamodb", "@aws-sdk/client-lambda",
                       "@aws-sdk/client-sqs", "aws-sdk", "aws-cdk-lib", "aws-amplify",
                       "@aws-amplify/core", "sst"}
            if all_deps & aws_js:
                _add("AWS")

            # GCP
            gcp_js = {"@google-cloud/storage", "@google-cloud/bigquery", "@google-cloud/pubsub",
                       "@google-cloud/firestore", "firebase", "firebase-admin",
                       "@google-cloud/functions-framework"}
            if all_deps & gcp_js:
                _add("GCP")

            # Azure
            azure_js = {"@azure/storage-blob", "@azure/identity", "@azure/cosmos",
                         "@azure/service-bus", "@azure/keyvault-secrets",
                         "@azure/functions"}
            if all_deps & azure_js:
                _add("Azure")

            # Cloudflare
            cf_js = {"wrangler", "@cloudflare/workers-types", "@cloudflare/kv-asset-handler",
                      "hono"}
            if all_deps & cf_js:
                _add("Cloudflare")

            # DigitalOcean
            if "do-wrapper" in all_deps or "@digitalocean/openapi" in all_deps:
                _add("DigitalOcean")

        except (ValueError, KeyError):
            pass

    # Go deps
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "github.com/aws/aws-sdk-go" in content:
                _add("AWS")
            if "cloud.google.com/go" in content:
                _add("GCP")
            if "github.com/azure/azure-sdk-for-go" in content:
                _add("Azure")
        except Exception:
            pass

    # Rust deps
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "aws-sdk-" in content or "rusoto" in content:
                _add("AWS")
            if "google-cloud" in content:
                _add("GCP")
            if "azure_" in content:
                _add("Azure")
        except Exception:
            pass

    # Java deps
    pom = project_path / "pom.xml"
    if pom.exists():
        try:
            content = pom.read_text().lower()
            if "software.amazon.awssdk" in content or "com.amazonaws" in content:
                _add("AWS")
            if "com.google.cloud" in content:
                _add("GCP")
            if "com.azure" in content:
                _add("Azure")
        except Exception:
            pass

    build_gradle = project_path / "build.gradle"
    if build_gradle.exists():
        try:
            content = build_gradle.read_text().lower()
            if "software.amazon.awssdk" in content or "com.amazonaws" in content:
                _add("AWS")
            if "com.google.cloud" in content:
                _add("GCP")
            if "com.azure" in content:
                _add("Azure")
        except Exception:
            pass

    # Config files
    if (project_path / "wrangler.toml").exists() or (project_path / "wrangler.jsonc").exists():
        _add("Cloudflare")

    if (project_path / "fly.toml").exists():
        _add("Fly.io")

    if (project_path / "railway.json").exists() or (project_path / "railway.toml").exists():
        _add("Railway")

    if (project_path / "render.yaml").exists():
        _add("Render")

    return sorted(tools)


def detect_task_queues(project_path: Path) -> list[str]:
    """Detect task queue and background job frameworks."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str):
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # Python deps
    py_deps = _collect_python_deps(project_path)
    py_map = {
        "celery": "Celery", "rq": "RQ", "dramatiq": "Dramatiq",
        "huey": "Huey", "arq": "arq", "taskiq": "TaskIQ",
        "temporalio": "Temporal", "prefect": "Prefect",
        "airflow": "Airflow", "apache-airflow": "Airflow",
        "luigi": "Luigi", "dagster": "Dagster",
    }
    for dep, name in py_map.items():
        if dep in py_deps:
            _add(name)

    # JS/TS deps
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = __import__("json").loads(pkg_json.read_text())
            all_deps: set[str] = set()
            for key in ("dependencies", "devDependencies"):
                all_deps.update(data.get(key, {}).keys())

            js_map = {
                "bullmq": "BullMQ", "bull": "Bull", "bee-queue": "Bee-Queue",
                "agenda": "Agenda", "node-cron": "node-cron",
                "cron": "node-cron", "@temporalio/client": "Temporal",
                "@temporalio/worker": "Temporal", "graphile-worker": "Graphile Worker",
                "pg-boss": "pg-boss", "quirrel": "Quirrel",
            }
            for dep, name in js_map.items():
                if dep in all_deps:
                    _add(name)
        except (ValueError, KeyError):
            pass

    # Go deps
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "github.com/hibiken/asynq" in content:
                _add("Asynq")
            if "go.temporal.io" in content:
                _add("Temporal")
            if "github.com/robfig/cron" in content:
                _add("robfig/cron")
            if "github.com/gocraft/work" in content:
                _add("gocraft/work")
        except Exception:
            pass

    # Rust deps
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "tokio-cron-scheduler" in content:
                _add("tokio-cron-scheduler")
            if "apalis" in content:
                _add("Apalis")
        except Exception:
            pass

    # Java deps
    pom = project_path / "pom.xml"
    if pom.exists():
        try:
            content = pom.read_text().lower()
            if "quartz" in content:
                _add("Quartz")
            if "spring-batch" in content:
                _add("Spring Batch")
        except Exception:
            pass

    build_gradle = project_path / "build.gradle"
    if build_gradle.exists():
        try:
            content = build_gradle.read_text().lower()
            if "quartz" in content:
                _add("Quartz")
            if "spring-batch" in content:
                _add("Spring Batch")
        except Exception:
            pass

    return sorted(tools)


def detect_search_engines(project_path: Path) -> list[str]:
    """Detect search engine and full-text search tools."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # Python search engines
    py_map = {
        "elasticsearch": "Elasticsearch",
        "opensearch-py": "OpenSearch",
        "opensearchpy": "OpenSearch",
        "meilisearch": "Meilisearch",
        "typesense": "Typesense",
        "pysolr": "Solr",
        "algoliasearch": "Algolia",
        "whoosh": "Whoosh",
        "tantivy": "Tantivy",
        "django-haystack": "Haystack",
        "django-watson": "Watson",
    }
    for dep, name in py_map.items():
        if dep in py_deps:
            _add(name)

    # package.json — JS/TS
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps = set()
            for section in ("dependencies", "devDependencies"):
                all_deps.update(data.get(section, {}).keys())

            js_map = {
                "@elastic/elasticsearch": "Elasticsearch",
                "elasticsearch": "Elasticsearch",
                "@opensearch-project/opensearch": "OpenSearch",
                "meilisearch": "Meilisearch",
                "typesense": "Typesense",
                "algoliasearch": "Algolia",
                "react-instantsearch": "Algolia",
                "instantsearch.js": "Algolia",
                "lunr": "Lunr",
                "flexsearch": "FlexSearch",
                "fuse.js": "Fuse.js",
                "minisearch": "MiniSearch",
                "solr-client": "Solr",
            }
            for dep, name in js_map.items():
                if dep in all_deps:
                    _add(name)
        except Exception:
            pass

    # go.mod — Go
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            go_map = {
                "olivere/elastic": "Elasticsearch",
                "elastic/go-elasticsearch": "Elasticsearch",
                "opensearch-project/opensearch-go": "OpenSearch",
                "meilisearch/meilisearch-go": "Meilisearch",
                "typesense/typesense-go": "Typesense",
                "algolia/algoliasearch-client-go": "Algolia",
                "blevesearch/bleve": "Bleve",
            }
            for dep, name in go_map.items():
                if dep.lower() in content:
                    _add(name)
        except Exception:
            pass

    # Cargo.toml — Rust
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text().lower()
            if "tantivy" in content:
                _add("Tantivy")
            if "meilisearch-sdk" in content:
                _add("Meilisearch")
            if "elasticsearch" in content:
                _add("Elasticsearch")
        except Exception:
            pass

    # pom.xml / build.gradle — Java
    pom = project_path / "pom.xml"
    if pom.exists():
        try:
            content = pom.read_text().lower()
            if "elasticsearch" in content:
                _add("Elasticsearch")
            if "opensearch" in content:
                _add("OpenSearch")
            if "solr" in content:
                _add("Solr")
            if "algolia" in content:
                _add("Algolia")
            if "lucene" in content:
                _add("Lucene")
        except Exception:
            pass

    gradle = project_path / "build.gradle"
    if gradle.exists():
        try:
            content = gradle.read_text().lower()
            if "elasticsearch" in content:
                _add("Elasticsearch")
            if "opensearch" in content:
                _add("OpenSearch")
            if "solr" in content:
                _add("Solr")
            if "lucene" in content:
                _add("Lucene")
        except Exception:
            pass

    return sorted(tools)


def detect_feature_flags(project_path: Path) -> list[str]:
    """Detect feature flag and experimentation tools."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # Python
    py_map = {
        "launchdarkly-server-sdk": "LaunchDarkly",
        "ldclient-py": "LaunchDarkly",
        "unleashclient": "Unleash",
        "flagsmith": "Flagsmith",
        "growthbook": "GrowthBook",
        "split-python": "Split",
        "flipper-client": "Flipper",
        "posthog": "PostHog",
        "statsig": "Statsig",
        "openfeature-sdk": "OpenFeature",
        "django-waffle": "Waffle",
        "flask-featureflags": "Flask-FeatureFlags",
    }
    for dep, name in py_map.items():
        if dep in py_deps:
            _add(name)

    # package.json — JS/TS
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            all_deps = set()
            for section in ("dependencies", "devDependencies"):
                all_deps.update(data.get(section, {}).keys())

            js_map = {
                "launchdarkly-js-client-sdk": "LaunchDarkly",
                "launchdarkly-node-server-sdk": "LaunchDarkly",
                "@launchdarkly/node-server-sdk": "LaunchDarkly",
                "unleash-client": "Unleash",
                "unleash-proxy-client": "Unleash",
                "flagsmith": "Flagsmith",
                "@growthbook/growthbook": "GrowthBook",
                "@growthbook/growthbook-react": "GrowthBook",
                "@splitio/splitio": "Split",
                "@split-software/splitio": "Split",
                "posthog-js": "PostHog",
                "posthog-node": "PostHog",
                "statsig-js": "Statsig",
                "statsig-node": "Statsig",
                "@openfeature/js-sdk": "OpenFeature",
                "@openfeature/react-sdk": "OpenFeature",
                "@happykit/flags": "HappyKit",
                "@vercel/flags": "Vercel Flags",
                "@configcat/sdk": "ConfigCat",
            }
            for dep, name in js_map.items():
                if dep in all_deps:
                    _add(name)
        except Exception:
            pass

    # go.mod — Go
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            go_map = {
                "launchdarkly/go-server-sdk": "LaunchDarkly",
                "unleash/unleash-client-go": "Unleash",
                "growthbook/growthbook-golang": "GrowthBook",
                "open-feature/go-sdk": "OpenFeature",
                "posthog/posthog-go": "PostHog",
            }
            for dep, name in go_map.items():
                if dep.lower() in content:
                    _add(name)
        except Exception:
            pass

    # Cargo.toml — Rust
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text().lower()
            if "launchdarkly" in content:
                _add("LaunchDarkly")
            if "unleash-api-client" in content:
                _add("Unleash")
            if "openfeature" in content:
                _add("OpenFeature")
        except Exception:
            pass

    # pom.xml / build.gradle — Java
    for jfile in ("pom.xml", "build.gradle"):
        jpath = project_path / jfile
        if jpath.exists():
            try:
                content = jpath.read_text().lower()
                if "launchdarkly" in content:
                    _add("LaunchDarkly")
                if "unleash" in content and "getunleash" in content:
                    _add("Unleash")
                if "flagsmith" in content:
                    _add("Flagsmith")
                if "growthbook" in content:
                    _add("GrowthBook")
                if "split" in content and "splitio" in content:
                    _add("Split")
                if "openfeature" in content:
                    _add("OpenFeature")
                if "togglz" in content:
                    _add("Togglz")
                if "ff4j" in content:
                    _add("FF4J")
            except Exception:
                pass

    return sorted(tools)


def detect_http_clients(project_path: Path) -> list[str]:
    """Detect HTTP client libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # Python HTTP clients
    py_mapping = {
        "requests": "Requests",
        "httpx": "HTTPX",
        "aiohttp": "aiohttp",
        "urllib3": "urllib3",
        "httplib2": "httplib2",
        "pycurl": "PycURL",
        "treq": "treq",
        "asks": "asks",
        "niquests": "niquests",
        "uplink": "Uplink",
    }
    for dep, name in py_mapping.items():
        if dep in py_deps:
            _add(name)

    # JS/TS HTTP clients — package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "\"axios\"" in content:
                _add("Axios")
            if "\"node-fetch\"" in content:
                _add("node-fetch")
            if "\"got\"" in content and "\"got\":" in content:
                _add("Got")
            if "\"ky\"" in content and "\"ky\":" in content:
                _add("Ky")
            if "\"superagent\"" in content:
                _add("SuperAgent")
            if "\"undici\"" in content:
                _add("Undici")
            if "\"ofetch\"" in content:
                _add("ofetch")
            if "\"wretch\"" in content:
                _add("Wretch")
            if "\"needle\"" in content:
                _add("Needle")
            if "\"cross-fetch\"" in content:
                _add("cross-fetch")
            if "\"isomorphic-fetch\"" in content:
                _add("isomorphic-fetch")
        except Exception:
            pass

    # Go HTTP clients — go.mod
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "go-resty/resty" in content:
                _add("Resty")
            if "hashicorp/go-retryablehttp" in content:
                _add("go-retryablehttp")
            if "go-resty/gentleman" in content or "h2non/gentleman" in content:
                _add("Gentleman")
            if "sling" in content and "dghubble/sling" in content:
                _add("Sling")
            if "heimdall" in content and "gojek/heimdall" in content:
                _add("Heimdall")
            if "req" in content and "imroc/req" in content:
                _add("Req")
        except Exception:
            pass

    # Rust HTTP clients — Cargo.toml
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "reqwest" in content:
                _add("reqwest")
            if "hyper" in content:
                _add("hyper")
            if "ureq" in content:
                _add("ureq")
            if "surf" in content:
                _add("surf")
            if "isahc" in content:
                _add("isahc")
            if "attohttpc" in content:
                _add("attohttpc")
        except Exception:
            pass

    # Java HTTP clients — pom.xml / build.gradle
    for jpath in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if jpath.exists():
            try:
                content = jpath.read_text().lower()
                if "okhttp" in content:
                    _add("OkHttp")
                if "httpclient" in content and "apache" in content:
                    _add("Apache HttpClient")
                if "retrofit" in content:
                    _add("Retrofit")
                if "unirest" in content:
                    _add("Unirest")
                if "webclient" in content or "webflux" in content:
                    _add("WebClient")
                if "resttemplate" in content:
                    _add("RestTemplate")
                if "feign" in content:
                    _add("Feign")
            except Exception:
                pass

    return sorted(tools)


def detect_doc_generators(project_path: Path) -> list[str]:
    """Detect documentation generation tools."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # Python doc generators
    if "sphinx" in py_deps or (project_path / "docs" / "conf.py").exists():
        _add("Sphinx")
    if "mkdocs" in py_deps or (project_path / "mkdocs.yml").exists() or (project_path / "mkdocs.yaml").exists():
        _add("MkDocs")
    if "pdoc" in py_deps or "pdoc3" in py_deps:
        _add("pdoc")
    if "pydoctor" in py_deps:
        _add("pydoctor")

    # JS/TS doc generators — package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "\"docusaurus" in content or "\"@docusaurus/" in content:
                _add("Docusaurus")
            if "\"storybook\"" in content or "\"@storybook/" in content:
                _add("Storybook")
            if "\"vitepress\"" in content:
                _add("VitePress")
            if "\"typedoc\"" in content:
                _add("TypeDoc")
            if "\"jsdoc\"" in content:
                _add("JSDoc")
            if "\"nextra\"" in content:
                _add("Nextra")
            if "\"gitbook\"" in content:
                _add("GitBook")
            if "\"docsify" in content:
                _add("Docsify")
            if "\"@mintlify/" in content or "\"mintlify\"" in content:
                _add("Mintlify")
            if "\"@astrojs/starlight\"" in content:
                _add("Starlight")
            if "\"documentation.js\"" in content or "\"documentation\":" in content and "documentationjs" in content:
                _add("documentation.js")
        except Exception:
            pass

    # Config file detection (framework-agnostic)
    if (project_path / "docusaurus.config.js").exists() or (project_path / "docusaurus.config.ts").exists():
        _add("Docusaurus")
    if (project_path / ".storybook").exists():
        _add("Storybook")
    if (project_path / "typedoc.json").exists():
        _add("TypeDoc")
    if (project_path / "jsdoc.json").exists() or (project_path / ".jsdoc.json").exists():
        _add("JSDoc")
    if (project_path / "book.toml").exists():
        _add("mdBook")

    # Go doc generators
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "swaggo/swag" in content:
                _add("Swag")
        except Exception:
            pass

    # Rust doc generators — Cargo.toml (rustdoc is built-in)
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "rustdoc" in content or "[package.metadata.docs.rs]" in content.lower():
                _add("rustdoc")
        except Exception:
            pass

    # Java doc generators — pom.xml / build.gradle
    for jpath in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if jpath.exists():
            try:
                content = jpath.read_text().lower()
                if "javadoc" in content:
                    _add("Javadoc")
                if "dokka" in content:
                    _add("Dokka")
            except Exception:
                pass

    # Generic — Doxygen
    if (project_path / "Doxyfile").exists() or (project_path / "doxygen.cfg").exists():
        _add("Doxygen")

    return sorted(tools)


def detect_cli_frameworks(project_path: Path) -> list[str]:
    """Detect CLI framework libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # Python CLI frameworks
    py_mapping = {
        "click": "Click",
        "typer": "Typer",
        "fire": "Fire",
        "rich": "Rich",
        "cement": "Cement",
        "cliff": "cliff",
        "docopt": "docopt",
        "plac": "plac",
        "cleo": "Cleo",
        "textual": "Textual",
        "prompt-toolkit": "prompt_toolkit",
        "prompt_toolkit": "prompt_toolkit",
        "questionary": "Questionary",
        "inquirer": "InquirerPy",
        "inquirerpy": "InquirerPy",
        "trogon": "Trogon",
    }
    for dep, name in py_mapping.items():
        if dep in py_deps:
            _add(name)

    # JS/TS CLI frameworks — package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "\"commander\"" in content:
                _add("Commander.js")
            if "\"yargs\"" in content:
                _add("Yargs")
            if "\"meow\"" in content:
                _add("meow")
            if "\"oclif\"" in content or "\"@oclif/" in content:
                _add("oclif")
            if "\"vorpal\"" in content:
                _add("Vorpal")
            if "\"caporal\"" in content:
                _add("Caporal")
            if "\"inquirer\"" in content or "\"@inquirer/" in content:
                _add("Inquirer.js")
            if "\"prompts\"" in content:
                _add("prompts")
            if "\"chalk\"" in content:
                _add("Chalk")
            if "\"ora\"" in content and "\"ora\":" in content:
                _add("Ora")
            if "\"ink\"" in content and "\"ink\":" in content:
                _add("Ink")
            if "\"citty\"" in content:
                _add("citty")
            if "\"clipanion\"" in content:
                _add("Clipanion")
            if "\"gluegun\"" in content:
                _add("Gluegun")
        except Exception:
            pass

    # Go CLI frameworks — go.mod
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "spf13/cobra" in content:
                _add("Cobra")
            if "urfave/cli" in content:
                _add("urfave/cli")
            if "spf13/pflag" in content:
                _add("pflag")
            if "alecthomas/kong" in content:
                _add("Kong")
            if "charmbracelet/bubbletea" in content:
                _add("Bubbletea")
            if "charmbracelet/lipgloss" in content:
                _add("Lip Gloss")
            if "charmbracelet/huh" in content:
                _add("Huh")
            if "jessevdk/go-flags" in content:
                _add("go-flags")
        except Exception:
            pass

    # Rust CLI frameworks — Cargo.toml
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "clap" in content:
                _add("clap")
            if "structopt" in content:
                _add("StructOpt")
            if "argh" in content:
                _add("argh")
            if "dialoguer" in content:
                _add("dialoguer")
            if "indicatif" in content:
                _add("indicatif")
            if "console" in content and "console =" in content:
                _add("console")
            if "ratatui" in content:
                _add("Ratatui")
        except Exception:
            pass

    # Java CLI frameworks — pom.xml / build.gradle
    for jpath in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if jpath.exists():
            try:
                content = jpath.read_text().lower()
                if "picocli" in content:
                    _add("picocli")
                if "jcommander" in content:
                    _add("JCommander")
                if "airline" in content and "airlift" in content:
                    _add("Airline")
                if "spring-shell" in content:
                    _add("Spring Shell")
            except Exception:
                pass

    return sorted(tools)


def detect_config_tools(project_path: Path) -> list[str]:
    """Detect configuration management tools."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # Python config tools
    py_mapping = {
        "python-dotenv": "python-dotenv",
        "dynaconf": "Dynaconf",
        "hydra-core": "Hydra",
        "omegaconf": "OmegaConf",
        "pydantic-settings": "Pydantic Settings",
        "python-decouple": "python-decouple",
        "environs": "environs",
        "everett": "Everett",
        "configparser": "configparser",
        "confuse": "Confuse",
        "configobj": "ConfigObj",
    }
    for dep, name in py_mapping.items():
        if dep in py_deps:
            _add(name)

    # File-based config detection
    if (project_path / ".env").exists() or (project_path / ".env.example").exists():
        _add("dotenv")

    # JS/TS config tools — package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "\"dotenv\"" in content:
                _add("dotenv")
            if "\"convict\"" in content:
                _add("Convict")
            if "\"config\"" in content and "\"config\":" in content:
                _add("node-config")
            if "\"envalid\"" in content:
                _add("envalid")
            if "\"env-cmd\"" in content:
                _add("env-cmd")
            if "\"cross-env\"" in content:
                _add("cross-env")
            if "\"nconf\"" in content:
                _add("nconf")
            if "\"cosmiconfig\"" in content:
                _add("cosmiconfig")
            if "\"rc\"" in content and "\"rc\":" in content:
                _add("rc")
            if "\"@t3-oss/env" in content:
                _add("t3-env")
        except Exception:
            pass

    # Go config tools — go.mod
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "spf13/viper" in content:
                _add("Viper")
            if "kelseyhightower/envconfig" in content:
                _add("envconfig")
            if "joho/godotenv" in content:
                _add("godotenv")
            if "koanf" in content and "knadh/koanf" in content:
                _add("koanf")
            if "caarlos0/env" in content:
                _add("env")
            if "ilyakaznacheev/cleanenv" in content:
                _add("cleanenv")
        except Exception:
            pass

    # Rust config tools — Cargo.toml
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "config" in content and "config =" in content:
                _add("config-rs")
            if "dotenv" in content or "dotenvy" in content:
                _add("dotenvy")
            if "figment" in content:
                _add("Figment")
            if "envy" in content:
                _add("envy")
        except Exception:
            pass

    # Java config tools — pom.xml / build.gradle
    for jpath in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if jpath.exists():
            try:
                content = jpath.read_text().lower()
                if "spring-boot" in content and "configuration" in content:
                    _add("Spring Config")
                if "typesafe" in content and "config" in content:
                    _add("Typesafe Config")
                if "apache" in content and "commons-configuration" in content:
                    _add("Commons Configuration")
                if "dotenv-java" in content:
                    _add("dotenv-java")
            except Exception:
                pass

    return sorted(tools)


def detect_caching_tools(project_path: Path) -> list[str]:
    """Detect caching libraries and tools."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # Python caching tools
    py_mapping = {
        "redis": "redis-py",
        "cachetools": "cachetools",
        "diskcache": "DiskCache",
        "django-redis": "django-redis",
        "flask-caching": "Flask-Caching",
        "aiocache": "aiocache",
        "cashews": "cashews",
        "dogpile.cache": "dogpile.cache",
        "pymemcache": "pymemcache",
        "pylibmc": "pylibmc",
        "cachecontrol": "CacheControl",
    }
    for dep, name in py_mapping.items():
        if dep in py_deps:
            _add(name)

    # JS/TS caching tools — package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "\"ioredis\"" in content:
                _add("ioredis")
            if "\"redis\"" in content and "\"redis\":" in content:
                _add("redis (Node)")
            if "\"node-cache\"" in content:
                _add("node-cache")
            if "\"lru-cache\"" in content:
                _add("lru-cache")
            if "\"keyv\"" in content:
                _add("Keyv")
            if "\"cache-manager\"" in content:
                _add("cache-manager")
            if "\"memcached\"" in content or "\"memjs\"" in content:
                _add("Memcached (Node)")
            if "\"catbox\"" in content:
                _add("catbox")
        except Exception:
            pass

    # Go caching tools — go.mod
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "go-redis" in content:
                _add("go-redis")
            if "ristretto" in content:
                _add("Ristretto")
            if "bigcache" in content:
                _add("BigCache")
            if "groupcache" in content:
                _add("groupcache")
            if "freecache" in content:
                _add("FreeCache")
            if "gcache" in content:
                _add("GCache")
            if "bradfitz/gomemcache" in content:
                _add("gomemcache")
        except Exception:
            pass

    # Rust caching tools — Cargo.toml
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "moka" in content:
                _add("moka")
            if "cached" in content and "cached =" in content:
                _add("cached")
            if "redis" in content and "redis =" in content:
                _add("redis-rs")
            if "mini-moka" in content:
                _add("mini-moka")
        except Exception:
            pass

    # Java caching tools — pom.xml / build.gradle
    for jpath in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if jpath.exists():
            try:
                content = jpath.read_text().lower()
                if "caffeine" in content:
                    _add("Caffeine")
                if "ehcache" in content:
                    _add("Ehcache")
                if "spring-boot" in content and "cache" in content:
                    _add("Spring Cache")
                if "jedis" in content:
                    _add("Jedis")
                if "lettuce" in content and "lettuce-core" in content:
                    _add("Lettuce")
                if "redisson" in content:
                    _add("Redisson")
                if "guava" in content:
                    _add("Guava Cache")
                if "hazelcast" in content:
                    _add("Hazelcast")
            except Exception:
                pass

    return sorted(tools)


def detect_template_engines(project_path: Path) -> list[str]:
    """Detect template engines and rendering libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # Python template engines
    py_mapping = {
        "jinja2": "Jinja2",
        "mako": "Mako",
        "chameleon": "Chameleon",
        "genshi": "Genshi",
        "cheetah3": "Cheetah",
        "airspeed": "Airspeed",
    }
    for dep, name in py_mapping.items():
        if dep in py_deps:
            _add(name)

    # Django templates (implicit if Django is a dep)
    if "django" in py_deps:
        _add("Django Templates")

    # JS/TS template engines — package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "\"handlebars\"" in content or "\"hbs\"" in content:
                _add("Handlebars")
            if "\"ejs\"" in content:
                _add("EJS")
            if "\"pug\"" in content:
                _add("Pug")
            if "\"nunjucks\"" in content:
                _add("Nunjucks")
            if "\"mustache\"" in content:
                _add("Mustache")
            if "\"liquid\"" in content or "\"liquidjs\"" in content:
                _add("Liquid")
            if "\"eta\"" in content and "\"eta\":" in content:
                _add("Eta")
            if "\"marko\"" in content:
                _add("Marko")
            if "\"edge.js\"" in content or "\"@adonisjs/view\"" in content:
                _add("Edge.js")
            if "\"@vue/compiler-sfc\"" in content:
                _add("Vue SFC")
            if "\"svelte\"" in content:
                _add("Svelte")
            if "\"solid-js\"" in content:
                _add("Solid")
            if "\"astro\"" in content:
                _add("Astro")
        except Exception:
            pass

    # Go template engines — go.mod
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "html/template" in content or "text/template" in content:
                _add("Go Templates")
            if "pongo2" in content:
                _add("Pongo2")
            if "raymond" in content:
                _add("Raymond")
            if "jet" in content and "cloudykit/jet" in content:
                _add("Jet")
            if "amber" in content and "eknkc/amber" in content:
                _add("Amber")
        except Exception:
            pass

    # Rust template engines — Cargo.toml
    cargo = project_path / "Cargo.toml"
    if cargo.exists():
        try:
            content = cargo.read_text().lower()
            if "tera" in content and "tera =" in content:
                _add("Tera")
            if "askama" in content:
                _add("Askama")
            if "handlebars" in content and "handlebars =" in content:
                _add("Handlebars (Rust)")
            if "minijinja" in content:
                _add("MiniJinja")
            if "maud" in content and "maud =" in content:
                _add("Maud")
        except Exception:
            pass

    # Java template engines — pom.xml / build.gradle
    for jpath in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if jpath.exists():
            try:
                content = jpath.read_text().lower()
                if "thymeleaf" in content:
                    _add("Thymeleaf")
                if "freemarker" in content:
                    _add("FreeMarker")
                if "velocity" in content and "velocity-engine" in content:
                    _add("Velocity")
                if "mustache" in content and "jmustache" in content:
                    _add("Mustache (Java)")
                if "pebble" in content and "pebble" in content:
                    _add("Pebble")
            except Exception:
                pass

    return sorted(tools)


def detect_serialization_formats(project_path: Path) -> list[str]:
    """Detect serialization formats and data interchange libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # --- Python ---
    if "protobuf" in py_deps or "grpcio" in py_deps:
        _add("Protocol Buffers")
    if "msgpack" in py_deps or "msgpack-python" in py_deps:
        _add("MessagePack")
    if "avro-python3" in py_deps or "avro" in py_deps or "fastavro" in py_deps:
        _add("Apache Avro")
    if "thrift" in py_deps:
        _add("Apache Thrift")
    if "flatbuffers" in py_deps:
        _add("FlatBuffers")
    if "cbor2" in py_deps or "cbor" in py_deps:
        _add("CBOR")
    if "pyyaml" in py_deps:
        _add("YAML")
    if "toml" in py_deps or "tomli" in py_deps or "tomllib" in py_deps or "tomli-w" in py_deps:
        _add("TOML")
    if "orjson" in py_deps:
        _add("orjson")
    if "ujson" in py_deps:
        _add("ujson")
    if "pydantic" in py_deps:
        _add("Pydantic")
    if "marshmallow" in py_deps:
        _add("Marshmallow")
    if "cattrs" in py_deps:
        _add("cattrs")
    if "pickle5" in py_deps or "cloudpickle" in py_deps or "dill" in py_deps:
        _add("Pickle")
    if "arrow" in py_deps and "pyarrow" in py_deps:
        _add("Apache Arrow")
    elif "pyarrow" in py_deps:
        _add("Apache Arrow")
    if "parquet" in py_deps or "fastparquet" in py_deps:
        _add("Parquet")
    if "bson" in py_deps or "pymongo" in py_deps:
        _add("BSON")

    # --- JS/TS ---
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "protobufjs" in content or "google-protobuf" in content or "@grpc/" in content:
                _add("Protocol Buffers")
            if "msgpack" in content or "@msgpack/" in content:
                _add("MessagePack")
            if "avro" in content or "avsc" in content:
                _add("Apache Avro")
            if "flatbuffers" in content:
                _add("FlatBuffers")
            if "cbor" in content:
                _add("CBOR")
            if "js-yaml" in content or "yaml" in content:
                _add("YAML")
            if '"toml"' in content or "@iarna/toml" in content:
                _add("TOML")
            if "superjson" in content:
                _add("superjson")
            if "ajv" in content or "zod" in content or "joi" in content or "yup" in content:
                pass  # validation, not serialization
            if "apache-arrow" in content or "arquero" in content:
                _add("Apache Arrow")
            if "bson" in content:
                _add("BSON")
        except Exception:
            pass

    # --- Go ---
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "google.golang.org/protobuf" in content or "google.golang.org/grpc" in content:
                _add("Protocol Buffers")
            if "msgpack" in content or "vmihailenco/msgpack" in content:
                _add("MessagePack")
            if "linkedin/goavro" in content:
                _add("Apache Avro")
            if "google/flatbuffers" in content:
                _add("FlatBuffers")
            if "fxamacker/cbor" in content:
                _add("CBOR")
            if "go-yaml" in content or "gopkg.in/yaml" in content:
                _add("YAML")
            if "burntsushi/toml" in content or "pelletier/go-toml" in content:
                _add("TOML")
            if "json-iterator" in content or "goccy/go-json" in content:
                _add("go-json")
            if "apache/arrow" in content:
                _add("Apache Arrow")
        except Exception:
            pass

    # --- Rust ---
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text().lower()
            if "prost" in content or "protobuf" in content or "tonic" in content:
                _add("Protocol Buffers")
            if "rmp" in content or "rmp-serde" in content or "msgpack" in content:
                _add("MessagePack")
            if "apache-avro" in content:
                _add("Apache Avro")
            if "flatbuffers" in content:
                _add("FlatBuffers")
            if "ciborium" in content or "cbor" in content:
                _add("CBOR")
            if "serde_yaml" in content:
                _add("YAML")
            if "toml " in content or "toml_edit" in content or 'toml"' in content:
                _add("TOML")
            if "serde_json" in content:
                _add("serde_json")
            if "simd-json" in content:
                _add("simd-json")
            if "bincode" in content:
                _add("Bincode")
            if "postcard" in content:
                _add("Postcard")
            if "arrow" in content and "arrow-rs" in content:
                _add("Apache Arrow")
        except Exception:
            pass

    # --- Java ---
    for pom in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if pom.exists():
            try:
                content = pom.read_text().lower()
                if "protobuf" in content or "grpc" in content:
                    _add("Protocol Buffers")
                if "msgpack" in content:
                    _add("MessagePack")
                if "avro" in content:
                    _add("Apache Avro")
                if "flatbuffers" in content:
                    _add("FlatBuffers")
                if "cbor" in content:
                    _add("CBOR")
                if "snakeyaml" in content or "jackson-dataformat-yaml" in content:
                    _add("YAML")
                if "jackson-dataformat-toml" in content:
                    _add("TOML")
                if "jackson" in content:
                    _add("Jackson")
                if "gson" in content:
                    _add("Gson")
                if "thrift" in content:
                    _add("Apache Thrift")
                if "arrow" in content and "apache" in content:
                    _add("Apache Arrow")
                if "parquet" in content:
                    _add("Parquet")
                if "kryo" in content:
                    _add("Kryo")
            except Exception:
                pass

    # --- .proto files ---
    for proto in project_path.rglob("*.proto"):
        _add("Protocol Buffers")
        break

    # --- .avro / .avsc files ---
    for avro_file in project_path.rglob("*.avsc"):
        _add("Apache Avro")
        break

    return sorted(tools)


def detect_di_frameworks(project_path: Path) -> list[str]:
    """Detect dependency injection frameworks and IoC containers."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # --- Python ---
    if "dependency-injector" in py_deps:
        _add("dependency-injector")
    if "inject" in py_deps:
        _add("python-inject")
    if "lagom" in py_deps:
        _add("Lagom")
    if "punq" in py_deps:
        _add("punq")
    if "wireup" in py_deps:
        _add("wireup")
    if "svcs" in py_deps:
        _add("svcs")
    if "dishka" in py_deps:
        _add("dishka")
    if "fastapi" in py_deps:
        _add("FastAPI Depends")

    # --- JS/TS ---
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "inversify" in content:
                _add("InversifyJS")
            if "tsyringe" in content:
                _add("tsyringe")
            if "typedi" in content:
                _add("TypeDI")
            if "awilix" in content:
                _add("Awilix")
            if "bottlejs" in content:
                _add("BottleJS")
            if "injection-js" in content:
                _add("injection-js")
            if "@angular/core" in content:
                _add("Angular DI")
            if "@nestjs/core" in content or "@nestjs/common" in content:
                _add("NestJS DI")
        except Exception:
            pass

    # --- Go ---
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "uber.org/fx" in content or "go.uber.org/fx" in content:
                _add("Uber Fx")
            if "uber.org/dig" in content or "go.uber.org/dig" in content:
                _add("Uber Dig")
            if "google/wire" in content:
                _add("Wire")
            if "samber/do" in content:
                _add("do")
        except Exception:
            pass

    # --- Rust ---
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text().lower()
            if "shaku" in content:
                _add("Shaku")
            if "inject" in content and "waiter_di" not in content:
                _add("inject")
        except Exception:
            pass

    # --- Java ---
    for build_file in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if build_file.exists():
            try:
                content = build_file.read_text().lower()
                if "spring" in content and ("context" in content or "boot" in content):
                    _add("Spring DI")
                if "guice" in content:
                    _add("Google Guice")
                if "dagger" in content:
                    _add("Dagger")
                if "javax.inject" in content or "jakarta.inject" in content:
                    _add("CDI")
                if "micronaut" in content:
                    _add("Micronaut DI")
                if "quarkus" in content:
                    _add("Quarkus CDI")
            except Exception:
                pass

    return sorted(tools)


def detect_websocket_libs(project_path: Path) -> list[str]:
    """Detect WebSocket libraries and real-time communication frameworks."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # --- Python ---
    if "websockets" in py_deps:
        _add("websockets")
    if "python-socketio" in py_deps or "socketio" in py_deps:
        _add("python-socketio")
    if "channels" in py_deps or "daphne" in py_deps:
        _add("Django Channels")
    if "starlette" in py_deps or "fastapi" in py_deps:
        _add("Starlette WebSocket")
    if "tornado" in py_deps:
        _add("Tornado WebSocket")
    if "autobahn" in py_deps:
        _add("Autobahn")
    if "aiohttp" in py_deps:
        _add("aiohttp WebSocket")
    if "wsproto" in py_deps:
        _add("wsproto")

    # --- JS/TS ---
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text().lower()
            if "socket.io" in content:
                _add("Socket.IO")
            if '"ws"' in content or "'ws'" in content:
                _add("ws")
            if "sockjs" in content:
                _add("SockJS")
            if "primus" in content:
                _add("Primus")
            if "@trpc/server" in content:
                _add("tRPC WebSocket")
            if "graphql-ws" in content:
                _add("graphql-ws")
            if "pusher" in content:
                _add("Pusher")
            if "ably" in content:
                _add("Ably")
            if "phoenix" in content and "channel" in content:
                _add("Phoenix Channels")
            if "actioncable" in content or "@rails/actioncable" in content:
                _add("Action Cable")
            if "centrifuge" in content:
                _add("Centrifugo")
        except Exception:
            pass

    # --- Go ---
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text().lower()
            if "gorilla/websocket" in content:
                _add("Gorilla WebSocket")
            if "nhooyr.io/websocket" in content or "nhooyr" in content:
                _add("nhooyr/websocket")
            if "gobwas/ws" in content:
                _add("gobwas/ws")
            if "centrifugal/centrifuge" in content:
                _add("Centrifugo")
            if "olahol/melody" in content:
                _add("Melody")
        except Exception:
            pass

    # --- Rust ---
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text().lower()
            if "tokio-tungstenite" in content or "tungstenite" in content:
                _add("Tungstenite")
            if "axum" in content and "ws" in content:
                _add("Axum WebSocket")
            if "actix-web-actors" in content or "actix-ws" in content:
                _add("Actix WebSocket")
            if "warp" in content and "ws" in content:
                _add("Warp WebSocket")
        except Exception:
            pass

    # --- Java ---
    for build_file in [project_path / "pom.xml", project_path / "build.gradle", project_path / "build.gradle.kts"]:
        if build_file.exists():
            try:
                content = build_file.read_text().lower()
                if "spring-websocket" in content or "spring-boot-starter-websocket" in content:
                    _add("Spring WebSocket")
                if "javax.websocket" in content or "jakarta.websocket" in content:
                    _add("Jakarta WebSocket")
                if "tyrus" in content:
                    _add("Tyrus")
                if "netty" in content and "websocket" in content:
                    _add("Netty WebSocket")
                if "undertow" in content and "websocket" in content:
                    _add("Undertow WebSocket")
            except Exception:
                pass

    return sorted(tools)


def _collect_python_deps(project_path: Path) -> set[str]:
    """Collect Python dependency names from pyproject.toml and requirements.txt."""
    py_deps: set[str] = set()
    pyproject = project_path / "pyproject.toml"
    if pyproject.exists():
        try:
            for line in pyproject.read_text().splitlines():
                cleaned = line.strip().strip('",\' ').lower()
                if cleaned:
                    dep = cleaned.split("[")[0].split(">=")[0].split("==")[0].split("<")[0].split(">")[0].split("~=")[0].strip()
                    if dep and not dep.startswith(("[", "#", "{")) and "=" not in dep:
                        py_deps.add(dep)
        except Exception:
            pass
    reqs_txt = project_path / "requirements.txt"
    if reqs_txt.exists():
        try:
            for line in reqs_txt.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    dep = line.split(">=")[0].split("==")[0].split("<")[0].split(">")[0].split("[")[0].strip()
                    py_deps.add(dep.lower())
        except Exception:
            pass
    return py_deps


def detect_graphql_libs(project_path: Path) -> list[str]:
    """Detect GraphQL libraries and tools."""
    import json as _json

    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # --- Python ---
    py_map = {
        "graphene": "Graphene",
        "graphene-django": "Graphene-Django",
        "ariadne": "Ariadne",
        "strawberry-graphql": "Strawberry",
        "sgqlc": "sgqlc",
        "gql": "gql",
        "graphql-core": "graphql-core",
        "tartiflette": "Tartiflette",
    }
    for dep, name in py_map.items():
        if dep in py_deps:
            _add(name)

    # --- JS/TS ---
    pkg_json_path = project_path / "package.json"
    pkg_json: dict = {}
    if pkg_json_path.exists():
        try:
            pkg_json = _json.loads(pkg_json_path.read_text())
        except Exception:
            pass
    all_js = set(pkg_json.get("dependencies", {}).keys()) | set(pkg_json.get("devDependencies", {}).keys())
    js_map = {
        "graphql": "graphql-js",
        "apollo-server": "Apollo Server",
        "apollo-server-express": "Apollo Server",
        "apollo-server-core": "Apollo Server",
        "@apollo/server": "Apollo Server",
        "apollo-client": "Apollo Client",
        "@apollo/client": "Apollo Client",
        "graphql-yoga": "GraphQL Yoga",
        "type-graphql": "TypeGraphQL",
        "nexus": "Nexus",
        "@graphql-codegen/cli": "GraphQL Code Generator",
        "graphql-request": "graphql-request",
        "urql": "URQL",
        "@urql/core": "URQL",
        "relay-runtime": "Relay",
        "react-relay": "Relay",
        "mercurius": "Mercurius",
        "pothos": "Pothos",
        "@pothos/core": "Pothos",
        "graphql-tools": "graphql-tools",
        "graphql-tag": "graphql-tag",
    }
    for dep, name in js_map.items():
        if dep in all_js:
            _add(name)

    # --- Go ---
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            go_map = {
                "github.com/99designs/gqlgen": "gqlgen",
                "github.com/graphql-go/graphql": "graphql-go",
                "github.com/graph-gophers/graphql-go": "graph-gophers",
                "github.com/samsarahq/thunder": "Thunder",
                "github.com/Khan/genqlient": "genqlient",
            }
            for mod, name in go_map.items():
                if mod in content:
                    _add(name)
        except Exception:
            pass

    # --- Rust ---
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text()
            rust_map = {
                "juniper": "Juniper",
                "async-graphql": "async-graphql",
                "graphql-client": "graphql-client",
                "cynic": "Cynic",
            }
            for crate, name in rust_map.items():
                if crate in content:
                    _add(name)
        except Exception:
            pass

    # --- Java ---
    java_deps = set()
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps.add(bf.read_text())
            except Exception:
                pass
    java_content = " ".join(java_deps)
    java_map = {
        "graphql-java": "graphql-java",
        "graphql-spring": "GraphQL Spring",
        "netflix.dgs": "Netflix DGS",
        "smallrye-graphql": "SmallRye GraphQL",
        "graphql-kotlin": "graphql-kotlin",
    }
    for dep, name in java_map.items():
        if dep in java_content:
            _add(name)

    # --- Schema files ---
    for ext in ("*.graphql", "*.gql"):
        if list(project_path.glob(ext)):
            _add("GraphQL Schema")
            break

    return sorted(tools)


def detect_event_streaming(project_path: Path) -> list[str]:
    """Detect event streaming and message broker libraries."""
    import json as _json

    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    py_deps = _collect_python_deps(project_path)

    # --- Python ---
    py_map = {
        "confluent-kafka": "Confluent Kafka",
        "kafka-python": "kafka-python",
        "aiokafka": "aiokafka",
        "pika": "RabbitMQ (pika)",
        "aio-pika": "RabbitMQ (aio-pika)",
        "kombu": "Kombu",
        "nats-py": "NATS",
        "pulsar-client": "Apache Pulsar",
        "faust-streaming": "Faust",
        "faust": "Faust",
    }
    for dep, name in py_map.items():
        if dep in py_deps:
            _add(name)

    # --- JS/TS ---
    pkg_json_path = project_path / "package.json"
    pkg_json: dict = {}
    if pkg_json_path.exists():
        try:
            pkg_json = _json.loads(pkg_json_path.read_text())
        except Exception:
            pass
    all_js = set(pkg_json.get("dependencies", {}).keys()) | set(pkg_json.get("devDependencies", {}).keys())
    js_map = {
        "kafkajs": "KafkaJS",
        "amqplib": "RabbitMQ (amqplib)",
        "rhea": "AMQP (rhea)",
        "nats": "NATS",
        "pulsar-client": "Apache Pulsar",
        "bullmq": "BullMQ",
        "@google-cloud/pubsub": "Google Pub/Sub",
        "@aws-sdk/client-sqs": "AWS SQS",
        "@aws-sdk/client-sns": "AWS SNS",
        "@aws-sdk/client-kinesis": "AWS Kinesis",
        "@azure/event-hubs": "Azure Event Hubs",
        "@azure/service-bus": "Azure Service Bus",
    }
    for dep, name in js_map.items():
        if dep in all_js:
            _add(name)

    # --- Go ---
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            go_map = {
                "github.com/segmentio/kafka-go": "kafka-go",
                "github.com/confluentinc/confluent-kafka-go": "Confluent Kafka (Go)",
                "github.com/Shopify/sarama": "Sarama",
                "github.com/IBM/sarama": "Sarama",
                "github.com/streadway/amqp": "RabbitMQ (Go)",
                "github.com/rabbitmq/amqp091-go": "RabbitMQ (Go)",
                "github.com/nats-io/nats.go": "NATS (Go)",
                "github.com/apache/pulsar-client-go": "Apache Pulsar (Go)",
                "github.com/ThreeDotsLabs/watermill": "Watermill",
            }
            for mod, name in go_map.items():
                if mod in content:
                    _add(name)
        except Exception:
            pass

    # --- Rust ---
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text()
            rust_map = {
                "rdkafka": "rdkafka",
                "lapin": "RabbitMQ (lapin)",
                "async-nats": "NATS (Rust)",
                "pulsar": "Apache Pulsar (Rust)",
            }
            for crate, name in rust_map.items():
                if crate in content:
                    _add(name)
        except Exception:
            pass

    # --- Java ---
    java_deps = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps.append(bf.read_text())
            except Exception:
                pass
    java_content = " ".join(java_deps)
    java_map = {
        "spring-kafka": "Spring Kafka",
        "kafka-clients": "Kafka Clients",
        "spring-amqp": "Spring AMQP",
        "spring-rabbit": "Spring RabbitMQ",
        "nats-client": "NATS (Java)",
        "azure-messaging-eventhubs": "Azure Event Hubs",
        "azure-messaging-servicebus": "Azure Service Bus",
    }
    for dep, name in java_map.items():
        if dep in java_content:
            _add(name)

    return sorted(tools)


def detect_payment_tools(project_path: Path) -> list[str]:
    """Detect payment and billing libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # --- Python ---
    py_deps = _collect_python_deps(project_path)
    py_map = {
        "stripe": "Stripe",
        "paypalrestsdk": "PayPal",
        "paypal-checkout-serversdk": "PayPal",
        "braintree": "Braintree",
        "square": "Square",
        "adyen": "Adyen",
        "paddle-python-sdk": "Paddle",
        "razorpay": "Razorpay",
        "mollie-api-python": "Mollie",
        "coinbase-commerce": "Coinbase Commerce",
        "gocardless-pro": "GoCardless",
        "paystack": "Paystack",
        "flutterwave-python": "Flutterwave",
        "lemonsqueezy": "Lemon Squeezy",
    }
    for dep, name in py_map.items():
        if dep in py_deps:
            _add(name)

    # --- JS/TS ---
    pkg_json = project_path / "package.json"
    all_js: set[str] = set()
    if pkg_json.exists():
        try:
            import json as _json
            data = _json.loads(pkg_json.read_text())
            for section in ("dependencies", "devDependencies"):
                all_js.update(data.get(section, {}).keys())
        except Exception:
            pass
    js_map = {
        "stripe": "Stripe",
        "@stripe/stripe-js": "Stripe",
        "@stripe/react-stripe-js": "Stripe",
        "paypal-rest-sdk": "PayPal",
        "@paypal/checkout-server-sdk": "PayPal",
        "@paypal/react-paypal-js": "PayPal",
        "braintree": "Braintree",
        "braintree-web": "Braintree",
        "square": "Square",
        "@adyen/adyen-web": "Adyen",
        "@adyen/api-library": "Adyen",
        "@paddle/paddle-js": "Paddle",
        "@paddle/paddle-node-sdk": "Paddle",
        "razorpay": "Razorpay",
        "@mollie/api-client": "Mollie",
        "coinbase-commerce-node": "Coinbase Commerce",
        "gocardless-nodejs": "GoCardless",
        "@lemonsqueezy/lemonsqueezy.js": "Lemon Squeezy",
        "recurly": "Recurly",
        "chargebee": "Chargebee",
    }
    for dep, name in js_map.items():
        if dep in all_js:
            _add(name)

    # --- Go ---
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            go_map = {
                "github.com/stripe/stripe-go": "Stripe",
                "github.com/plutov/paypal": "PayPal",
                "github.com/braintree-go/braintree-go": "Braintree",
                "github.com/adyen/adyen-go-api-library": "Adyen",
                "github.com/razorpay/razorpay-go": "Razorpay",
            }
            for mod, name in go_map.items():
                if mod in content:
                    _add(name)
        except Exception:
            pass

    # --- Rust ---
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text()
            rust_map = {
                "async-stripe": "Stripe",
                "stripe-rust": "Stripe",
            }
            for crate, name in rust_map.items():
                if crate in content:
                    _add(name)
        except Exception:
            pass

    # --- Java ---
    java_deps = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps.append(bf.read_text())
            except Exception:
                pass
    java_content = " ".join(java_deps)
    java_map = {
        "stripe-java": "Stripe",
        "paypal-sdk": "PayPal",
        "checkout-sdk": "PayPal",
        "braintree-java": "Braintree",
        "adyen-java-api-library": "Adyen",
        "square": "Square",
        "razorpay-java": "Razorpay",
    }
    for dep, name in java_map.items():
        if dep in java_content:
            _add(name)

    return sorted(tools)


def detect_date_libs(project_path: Path) -> list[str]:
    """Detect date and time libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # --- Python ---
    py_deps = _collect_python_deps(project_path)
    py_map = {
        "arrow": "Arrow",
        "pendulum": "Pendulum",
        "python-dateutil": "python-dateutil",
        "dateutil": "python-dateutil",
        "delorean": "Delorean",
        "maya": "Maya",
        "pytz": "pytz",
        "humanize": "humanize",
        "dateparser": "dateparser",
        "iso8601": "iso8601",
        "ciso8601": "ciso8601",
    }
    for dep, name in py_map.items():
        if dep in py_deps:
            _add(name)

    # --- JS/TS ---
    pkg_json = project_path / "package.json"
    all_js: set[str] = set()
    if pkg_json.exists():
        try:
            import json as _json
            data = _json.loads(pkg_json.read_text())
            for section in ("dependencies", "devDependencies"):
                all_js.update(data.get(section, {}).keys())
        except Exception:
            pass
    js_map = {
        "dayjs": "Day.js",
        "date-fns": "date-fns",
        "luxon": "Luxon",
        "moment": "Moment.js",
        "moment-timezone": "Moment.js",
        "spacetime": "Spacetime",
        "fecha": "Fecha",
        "tempo": "Tempo",
        "@js-temporal/polyfill": "Temporal",
        "timeago.js": "timeago.js",
        "ms": "ms",
        "chrono-node": "chrono-node",
    }
    for dep, name in js_map.items():
        if dep in all_js:
            _add(name)

    # --- Go ---
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            go_map = {
                "github.com/jinzhu/now": "jinzhu/now",
                "github.com/araddon/dateparse": "dateparse",
                "github.com/relvacode/iso8601": "iso8601 (Go)",
                "github.com/rickb777/date": "rickb777/date",
            }
            for mod, name in go_map.items():
                if mod in content:
                    _add(name)
        except Exception:
            pass

    # --- Rust ---
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text()
            rust_map = {
                "chrono": "chrono",
                "time": "time (Rust)",
                "humantime": "humantime",
            }
            for crate, name in rust_map.items():
                if crate in content:
                    _add(name)
        except Exception:
            pass

    # --- Java ---
    java_deps = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps.append(bf.read_text())
            except Exception:
                pass
    java_content = " ".join(java_deps)
    java_map = {
        "joda-time": "Joda-Time",
        "threeten-extra": "ThreeTen-Extra",
        "prettytime": "PrettyTime",
    }
    for dep, name in java_map.items():
        if dep in java_content:
            _add(name)

    return sorted(tools)


def detect_image_libs(project_path: Path) -> list[str]:
    """Detect image processing libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    # --- Python ---
    py_deps = _collect_python_deps(project_path)
    py_map = {
        "pillow": "Pillow",
        "pil": "Pillow",
        "opencv-python": "OpenCV",
        "opencv-python-headless": "OpenCV",
        "opencv-contrib-python": "OpenCV",
        "scikit-image": "scikit-image",
        "imageio": "imageio",
        "wand": "Wand",
        "cairosvg": "CairoSVG",
        "pyvips": "pyvips",
        "rawpy": "rawpy",
    }
    for dep, name in py_map.items():
        if dep in py_deps:
            _add(name)

    # --- JS/TS ---
    pkg_json = project_path / "package.json"
    all_js: set[str] = set()
    if pkg_json.exists():
        try:
            import json as _json
            data = _json.loads(pkg_json.read_text())
            for section in ("dependencies", "devDependencies"):
                all_js.update(data.get(section, {}).keys())
        except Exception:
            pass
    js_map = {
        "sharp": "Sharp",
        "jimp": "Jimp",
        "canvas": "node-canvas",
        "@napi-rs/canvas": "napi-canvas",
        "gm": "GraphicsMagick",
        "image-size": "image-size",
        "pngjs": "pngjs",
        "pixelmatch": "pixelmatch",
        "blurhash": "BlurHash",
        "plaiceholder": "Plaiceholder",
        "@imgly/background-removal-node": "IMG.LY",
        "cropperjs": "Cropper.js",
    }
    for dep, name in js_map.items():
        if dep in all_js:
            _add(name)

    # --- Go ---
    go_mod = project_path / "go.mod"
    if go_mod.exists():
        try:
            content = go_mod.read_text()
            go_map = {
                "github.com/disintegration/imaging": "imaging",
                "github.com/fogleman/gg": "gg",
                "github.com/nfnt/resize": "nfnt/resize",
                "github.com/anthonynsimon/bild": "bild",
                "gocv.io/x/gocv": "GoCV",
                "golang.org/x/image": "x/image",
            }
            for mod, name in go_map.items():
                if mod in content:
                    _add(name)
        except Exception:
            pass

    # --- Rust ---
    cargo_toml = project_path / "Cargo.toml"
    if cargo_toml.exists():
        try:
            content = cargo_toml.read_text()
            rust_map = {
                "image": "image (Rust)",
                "imageproc": "imageproc",
                "resvg": "resvg",
                "opencv": "OpenCV (Rust)",
            }
            for crate, name in rust_map.items():
                if crate in content:
                    _add(name)
        except Exception:
            pass

    # --- Java ---
    java_deps = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps.append(bf.read_text())
            except Exception:
                pass
    java_content = " ".join(java_deps)
    java_map = {
        "thumbnailator": "Thumbnailator",
        "imgscalr": "imgscalr",
        "twelvemonkeys": "TwelveMonkeys",
        "scrimage": "Scrimage",
    }
    for dep, name in java_map.items():
        if dep in java_content:
            _add(name)

    return sorted(tools)


def detect_crypto_libs(project_path: Path) -> list[str]:
    """Detect cryptography and encryption libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    python_deps = _collect_python_deps(project_path)

    py_map = {
        "cryptography": "cryptography",
        "pycryptodome": "PyCryptodome",
        "pycryptodomex": "PyCryptodome",
        "pynacl": "PyNaCl",
        "bcrypt": "bcrypt",
        "passlib": "Passlib",
        "argon2-cffi": "Argon2",
        "hashlib": "hashlib",
        "hmac": "hmac",
        "jwcrypto": "jwcrypto",
        "paramiko": "Paramiko",
        "pyopenssl": "pyOpenSSL",
        "certifi": "certifi",
        "truststore": "truststore",
    }
    for dep, name in py_map.items():
        if dep in python_deps:
            _add(name)

    # JS/TS
    pkg_json = project_path / "package.json"
    js_content = ""
    if pkg_json.exists():
        try:
            js_content = pkg_json.read_text().lower()
        except OSError:
            pass

    js_map = {
        "crypto-js": "CryptoJS",
        "bcryptjs": "bcrypt.js",
        "bcrypt": "bcrypt",
        "argon2": "Argon2",
        "jose": "jose",
        "jsonwebtoken": "jsonwebtoken",
        "node-forge": "node-forge",
        "tweetnacl": "TweetNaCl",
        "libsodium-wrappers": "libsodium",
        "openpgp": "OpenPGP.js",
        "noble-curves": "noble-curves",
        "@noble/hashes": "noble-hashes",
        "scrypt-js": "scrypt-js",
        "webcrypto": "WebCrypto",
    }
    for dep, name in js_map.items():
        if dep in js_content:
            _add(name)

    # Go
    go_sum = project_path / "go.sum"
    go_content = ""
    if go_sum.exists():
        try:
            go_content = go_sum.read_text().lower()
        except OSError:
            pass

    go_map = {
        "golang.org/x/crypto": "x/crypto",
        "filippo.io/age": "age",
        "github.com/cloudflare/circl": "CIRCL",
        "golang.org/x/oauth2": "x/oauth2",
    }
    for dep, name in go_map.items():
        if dep.lower() in go_content:
            _add(name)

    # Rust
    cargo_toml = project_path / "Cargo.toml"
    rust_content = ""
    if cargo_toml.exists():
        try:
            rust_content = cargo_toml.read_text().lower()
        except OSError:
            pass

    rust_map = {
        "ring": "ring",
        "rustls": "rustls",
        "rcgen": "rcgen",
        "rust-crypto": "rust-crypto",
        "orion": "Orion",
        "sodiumoxide": "sodiumoxide",
        "argon2": "Argon2",
        "bcrypt": "bcrypt",
        "sha2": "sha2",
        "aes-gcm": "aes-gcm",
    }
    for dep, name in rust_map.items():
        if dep in rust_content:
            _add(name)

    # Java
    java_deps = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps.append(bf.read_text())
            except Exception:
                pass
    java_content = " ".join(java_deps)

    java_map = {
        "bouncycastle": "Bouncy Castle",
        "jasypt": "Jasypt",
        "tink": "Tink",
        "conscrypt": "Conscrypt",
        "spring-security-crypto": "Spring Security Crypto",
    }
    for dep, name in java_map.items():
        if dep in java_content:
            _add(name)

    return sorted(tools)


def detect_pdf_libs(project_path: Path) -> list[str]:
    """Detect PDF and document generation libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    python_deps = _collect_python_deps(project_path)

    py_map = {
        "reportlab": "ReportLab",
        "fpdf2": "FPDF2",
        "fpdf": "FPDF",
        "weasyprint": "WeasyPrint",
        "xhtml2pdf": "xhtml2pdf",
        "pypdf": "pypdf",
        "pypdf2": "PyPDF2",
        "pdfplumber": "pdfplumber",
        "pymupdf": "PyMuPDF",
        "fitz": "PyMuPDF",
        "pdfminer": "PDFMiner",
        "pdfminer.six": "PDFMiner",
        "camelot-py": "Camelot",
        "tabula-py": "tabula-py",
        "pikepdf": "pikepdf",
        "borb": "borb",
        "python-docx": "python-docx",
        "openpyxl": "openpyxl",
        "xlsxwriter": "XlsxWriter",
        "python-pptx": "python-pptx",
        "pandoc": "Pandoc",
    }
    for dep, name in py_map.items():
        if dep in python_deps:
            _add(name)

    # JS/TS
    pkg_json = project_path / "package.json"
    js_content = ""
    if pkg_json.exists():
        try:
            js_content = pkg_json.read_text().lower()
        except OSError:
            pass

    js_map = {
        "pdfkit": "PDFKit",
        "pdf-lib": "pdf-lib",
        "jspdf": "jsPDF",
        "puppeteer": "Puppeteer",
        "playwright": "Playwright",
        "@react-pdf/renderer": "React-PDF",
        "react-pdf": "react-pdf",
        "pdfjs-dist": "PDF.js",
        "pdfmake": "pdfmake",
        "docx": "docx",
        "exceljs": "ExcelJS",
        "xlsx": "SheetJS",
        "papaparse": "PapaParse",
        "csv-parse": "csv-parse",
        "handlebars": "Handlebars",
    }
    for dep, name in js_map.items():
        if dep in js_content:
            _add(name)

    # Go
    go_sum = project_path / "go.sum"
    go_content = ""
    if go_sum.exists():
        try:
            go_content = go_sum.read_text().lower()
        except OSError:
            pass

    go_map = {
        "unidoc/unipdf": "UniPDF",
        "jung-kurt/gofpdf": "gofpdf",
        "signintech/gopdf": "goPDF",
        "pdfcpu": "pdfcpu",
        "excelize": "Excelize",
    }
    for dep, name in go_map.items():
        if dep.lower() in go_content:
            _add(name)

    # Rust
    cargo_toml = project_path / "Cargo.toml"
    rust_content = ""
    if cargo_toml.exists():
        try:
            rust_content = cargo_toml.read_text().lower()
        except OSError:
            pass

    rust_map = {
        "printpdf": "printpdf",
        "genpdf": "genpdf",
        "lopdf": "lopdf",
        "pdf-extract": "pdf-extract",
        "calamine": "calamine",
    }
    for dep, name in rust_map.items():
        if dep in rust_content:
            _add(name)

    # Java
    java_deps = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps.append(bf.read_text())
            except Exception:
                pass
    java_content = " ".join(java_deps)

    java_map = {
        "itext": "iText",
        "pdfbox": "Apache PDFBox",
        "openpdf": "OpenPDF",
        "jasperreports": "JasperReports",
        "apache-poi": "Apache POI",
        "poi": "Apache POI",
    }
    for dep, name in java_map.items():
        if dep in java_content:
            _add(name)

    return sorted(tools)


def detect_data_viz_libs(project_path: Path) -> list[str]:
    """Detect data visualization and charting libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    python_deps = _collect_python_deps(project_path)

    py_map = {
        "matplotlib": "Matplotlib",
        "plotly": "Plotly",
        "seaborn": "Seaborn",
        "bokeh": "Bokeh",
        "altair": "Altair",
        "folium": "Folium",
        "plotnine": "plotnine",
        "pygal": "Pygal",
        "holoviews": "HoloViews",
        "hvplot": "hvPlot",
        "panel": "Panel",
        "dash": "Dash",
        "streamlit": "Streamlit",
        "gradio": "Gradio",
        "pydeck": "pydeck",
        "bqplot": "bqplot",
        "mayavi": "Mayavi",
        "vispy": "VisPy",
        "pyecharts": "pyecharts",
        "plotext": "Plotext",
    }
    for dep, name in py_map.items():
        if dep in python_deps:
            _add(name)

    # JS/TS
    pkg_json = project_path / "package.json"
    js_content = ""
    if pkg_json.exists():
        try:
            js_content = pkg_json.read_text().lower()
        except OSError:
            pass

    js_map = {
        "d3": "D3.js",
        "chart.js": "Chart.js",
        "recharts": "Recharts",
        "@nivo/": "Nivo",
        "victory": "Victory",
        "@visx/": "Visx",
        "echarts": "ECharts",
        "highcharts": "Highcharts",
        "apexcharts": "ApexCharts",
        "plotly.js": "Plotly.js",
        "three": "Three.js",
        "@deck.gl/": "Deck.gl",
        "@observablehq/plot": "Observable Plot",
        "@tremor/": "Tremor",
        "frappe-charts": "Frappe Charts",
        "uplot": "uPlot",
        "vega": "Vega",
        "vega-lite": "Vega-Lite",
        "lightweight-charts": "Lightweight Charts",
        "@ant-design/charts": "Ant Charts",
    }
    for dep, name in js_map.items():
        if dep in js_content:
            _add(name)

    # Go
    go_sum = project_path / "go.sum"
    go_content = ""
    if go_sum.exists():
        try:
            go_content = go_sum.read_text().lower()
        except OSError:
            pass

    go_map = {
        "go-echarts": "go-echarts",
        "gonum.org/v1/plot": "Gonum Plot",
        "go-chart": "go-chart",
        "termui": "termui",
        "asciigraph": "asciigraph",
    }
    for dep, name in go_map.items():
        if dep.lower() in go_content:
            _add(name)

    # Rust
    cargo_toml = project_path / "Cargo.toml"
    rust_content = ""
    if cargo_toml.exists():
        try:
            rust_content = cargo_toml.read_text().lower()
        except OSError:
            pass

    rust_map = {
        "plotters": "Plotters",
        "plotlib": "plotlib",
        "charming": "charming",
        "textplots": "textplots",
    }
    for dep, name in rust_map.items():
        if dep in rust_content:
            _add(name)

    # Java
    java_deps_dv = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps_dv.append(bf.read_text())
            except Exception:
                pass
    java_content_dv = " ".join(java_deps_dv)

    java_map_dv = {
        "jfreechart": "JFreeChart",
        "xchart": "XChart",
        "javafx": "JavaFX Charts",
        "processing": "Processing",
    }
    for dep, name in java_map_dv.items():
        if dep in java_content_dv:
            _add(name)

    return sorted(tools)


def detect_geo_libs(project_path: Path) -> list[str]:
    """Detect geospatial and mapping libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    python_deps = _collect_python_deps(project_path)

    py_map = {
        "geopandas": "GeoPandas",
        "shapely": "Shapely",
        "fiona": "Fiona",
        "rasterio": "rasterio",
        "pyproj": "pyproj",
        "gdal": "GDAL",
        "osgeo": "GDAL",
        "geopy": "geopy",
        "geoalchemy2": "GeoAlchemy2",
        "h3": "H3",
        "s2sphere": "S2",
        "geojson": "GeoJSON",
        "osmnx": "OSMnx",
        "xarray": "xarray",
        "cartopy": "Cartopy",
        "keplergl": "Kepler.gl",
    }
    for dep, name in py_map.items():
        if dep in python_deps:
            _add(name)

    # JS/TS
    pkg_json = project_path / "package.json"
    js_content = ""
    if pkg_json.exists():
        try:
            js_content = pkg_json.read_text().lower()
        except OSError:
            pass

    js_map = {
        "leaflet": "Leaflet",
        "mapbox-gl": "Mapbox GL",
        "maplibre-gl": "MapLibre GL",
        "ol": "OpenLayers",
        "cesium": "Cesium",
        "@turf/": "Turf.js",
        "@googlemaps/": "Google Maps",
        "@react-google-maps/": "Google Maps",
        "react-leaflet": "React Leaflet",
        "react-map-gl": "react-map-gl",
        "@mapbox/": "Mapbox",
        "h3-js": "H3",
        "geojson": "GeoJSON",
        "@here/": "HERE Maps",
    }
    for dep, name in js_map.items():
        if dep in js_content:
            _add(name)

    # Go
    go_sum = project_path / "go.sum"
    go_content = ""
    if go_sum.exists():
        try:
            go_content = go_sum.read_text().lower()
        except OSError:
            pass

    go_map = {
        "paulmach/orb": "orb",
        "golang/geo": "S2 Geometry",
        "twpayne/go-geom": "go-geom",
        "tidwall/tile38": "Tile38",
        "uber/h3-go": "H3",
    }
    for dep, name in go_map.items():
        if dep.lower() in go_content:
            _add(name)

    # Rust
    cargo_toml = project_path / "Cargo.toml"
    rust_content = ""
    if cargo_toml.exists():
        try:
            rust_content = cargo_toml.read_text().lower()
        except OSError:
            pass

    rust_map = {
        "geo": "geo",
        "geozero": "geozero",
        "proj": "proj",
        "h3o": "H3",
        "s2": "S2",
    }
    for dep, name in rust_map.items():
        if dep in rust_content:
            _add(name)

    # Java
    java_deps_geo = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps_geo.append(bf.read_text())
            except Exception:
                pass
    java_content_geo = " ".join(java_deps_geo)

    java_map_geo = {
        "geotools": "GeoTools",
        "jts-core": "JTS",
        "spatial4j": "Spatial4j",
        "h3-java": "H3",
        "graphhopper": "GraphHopper",
    }
    for dep, name in java_map_geo.items():
        if dep in java_content_geo:
            _add(name)

    return sorted(tools)


def detect_media_libs(project_path: Path) -> list[str]:
    """Detect audio/video and media processing libraries."""
    tools: list[str] = []
    seen: set[str] = set()

    def _add(name: str) -> None:
        if name not in seen:
            seen.add(name)
            tools.append(name)

    python_deps = _collect_python_deps(project_path)

    py_map = {
        "ffmpeg-python": "FFmpeg",
        "ffmpeg": "FFmpeg",
        "moviepy": "MoviePy",
        "pydub": "Pydub",
        "librosa": "Librosa",
        "soundfile": "SoundFile",
        "pyaudio": "PyAudio",
        "audioread": "audioread",
        "sounddevice": "sounddevice",
        "pedalboard": "Pedalboard",
        "torchaudio": "torchaudio",
        "av": "PyAV",
        "decord": "Decord",
        "vidgear": "VidGear",
        "imageio-ffmpeg": "FFmpeg",
        "aubio": "aubio",
        "madmom": "madmom",
        "essentia": "Essentia",
        "music21": "music21",
    }
    for dep, name in py_map.items():
        if dep in python_deps:
            _add(name)

    # JS/TS
    pkg_json = project_path / "package.json"
    js_content = ""
    if pkg_json.exists():
        try:
            js_content = pkg_json.read_text().lower()
        except OSError:
            pass

    js_map = {
        "fluent-ffmpeg": "FFmpeg",
        "ffmpeg-static": "FFmpeg",
        "tone": "Tone.js",
        "howler": "Howler.js",
        "wavesurfer.js": "WaveSurfer.js",
        "pizzicato": "Pizzicato",
        "video.js": "Video.js",
        "plyr": "Plyr",
        "hls.js": "HLS.js",
        "dash.js": "DASH.js",
        "shaka-player": "Shaka Player",
        "mediasoup": "Mediasoup",
        "simple-peer": "SimplePeer",
        "peerjs": "PeerJS",
        "@ffmpeg/ffmpeg": "FFmpeg.wasm",
        "music-metadata": "music-metadata",
    }
    for dep, name in js_map.items():
        if dep in js_content:
            _add(name)

    # Go
    go_sum = project_path / "go.sum"
    go_content = ""
    if go_sum.exists():
        try:
            go_content = go_sum.read_text().lower()
        except OSError:
            pass

    go_map = {
        "faiface/beep": "Beep",
        "hajimehoshi/oto": "Oto",
        "hajimehoshi/ebiten": "Ebiten",
        "zencoder/go-dash": "go-dash",
        "giorgisio/goav": "GoAV",
    }
    for dep, name in go_map.items():
        if dep.lower() in go_content:
            _add(name)

    # Rust
    cargo_toml = project_path / "Cargo.toml"
    rust_content = ""
    if cargo_toml.exists():
        try:
            rust_content = cargo_toml.read_text().lower()
        except OSError:
            pass

    rust_map = {
        "rodio": "Rodio",
        "cpal": "CPAL",
        "symphonia": "Symphonia",
        "gstreamer": "GStreamer",
        "ffmpeg-next": "FFmpeg",
        "dasp": "dasp",
    }
    for dep, name in rust_map.items():
        if dep in rust_content:
            _add(name)

    # Java
    java_deps_media: list[str] = []
    for build_file in ("build.gradle", "build.gradle.kts", "pom.xml"):
        bf = project_path / build_file
        if bf.exists():
            try:
                java_deps_media.append(bf.read_text())
            except Exception:
                pass
    java_content_media = " ".join(java_deps_media)

    java_map_media = {
        "javacv": "JavaCV",
        "jcodec": "JCodec",
        "xuggler": "Xuggler",
        "jave2": "JAVE",
        "tarsosdsp": "TarsosDSP",
        "tritonus": "Tritonus",
        "jlayer": "JLayer",
    }
    for dep, name in java_map_media.items():
        if dep in java_content_media:
            _add(name)

    return sorted(tools)
