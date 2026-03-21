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
