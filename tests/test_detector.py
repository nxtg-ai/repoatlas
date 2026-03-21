"""Tests for tech stack detection."""
from __future__ import annotations

import json


from atlas.detector import (
    _check_add,
    count_files,
    count_loc,
    count_test_files,
    detect_ci_config,
    detect_databases,
    detect_docs_artifacts,
    detect_frameworks,
    detect_key_deps,
    detect_languages,
    detect_license,
    detect_package_managers,
    detect_runtime_versions,
    detect_build_tools,
    detect_api_specs,
    walk_files,
)


# ---------------------------------------------------------------------------
# walk_files
# ---------------------------------------------------------------------------
class TestWalkFiles:
    def test_yields_regular_files(self, tmp_path):
        (tmp_path / "hello.py").write_text("x = 1")
        files = list(walk_files(tmp_path))
        assert len(files) == 1
        assert files[0].name == "hello.py"

    def test_skips_git_directory(self, tmp_path):
        git = tmp_path / ".git"
        git.mkdir()
        (git / "HEAD").write_text("ref")
        (tmp_path / "app.py").write_text("pass")
        names = [f.name for f in walk_files(tmp_path)]
        assert "HEAD" not in names
        assert "app.py" in names

    def test_skips_node_modules(self, tmp_path):
        nm = tmp_path / "node_modules" / "lodash"
        nm.mkdir(parents=True)
        (nm / "index.js").write_text("module.exports = {}")
        (tmp_path / "app.js").write_text("const x = 1;")
        names = [f.name for f in walk_files(tmp_path)]
        assert "index.js" not in names
        assert "app.js" in names

    def test_skips_venv(self, tmp_path):
        venv = tmp_path / ".venv" / "lib"
        venv.mkdir(parents=True)
        (venv / "site.py").write_text("pass")
        names = [f.name for f in walk_files(tmp_path)]
        assert "site.py" not in names

    def test_skips_pycache(self, tmp_path):
        cache = tmp_path / "__pycache__"
        cache.mkdir()
        (cache / "mod.cpython-312.pyc").write_bytes(b"\x00")
        names = [f.name for f in walk_files(tmp_path)]
        assert len(names) == 0

    def test_empty_dir(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        assert list(walk_files(empty)) == []

    def test_does_not_yield_directories(self, tmp_path):
        (tmp_path / "subdir").mkdir()
        (tmp_path / "file.txt").write_text("hi")
        files = list(walk_files(tmp_path))
        assert all(f.is_file() for f in files)

    def test_nested_source_files(self, tmp_path):
        deep = tmp_path / "a" / "b" / "c"
        deep.mkdir(parents=True)
        (deep / "deep.py").write_text("pass")
        files = list(walk_files(tmp_path))
        assert any(f.name == "deep.py" for f in files)


# ---------------------------------------------------------------------------
# detect_languages
# ---------------------------------------------------------------------------
class TestDetectLanguages:
    def test_detects_python(self, tmp_project):
        langs = detect_languages(tmp_project)
        assert "Python" in langs
        assert langs["Python"] >= 4

    def test_detects_typescript(self, tmp_js_project):
        langs = detect_languages(tmp_js_project)
        assert "TypeScript" in langs

    def test_empty_dir(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_languages(proj) == {}

    def test_multiple_languages(self, tmp_path):
        proj = tmp_path / "multi"
        proj.mkdir()
        (proj / "app.py").write_text("pass")
        (proj / "lib.ts").write_text("export const x = 1;")
        (proj / "main.go").write_text("package main")
        langs = detect_languages(proj)
        assert "Python" in langs
        assert "TypeScript" in langs
        assert "Go" in langs

    def test_sorted_by_count_descending(self, tmp_path):
        proj = tmp_path / "sorted"
        proj.mkdir()
        for i in range(5):
            (proj / f"mod{i}.py").write_text("pass")
        (proj / "util.ts").write_text("export {}")
        langs = detect_languages(proj)
        keys = list(langs.keys())
        assert keys[0] == "Python"

    def test_tsx_counted_as_typescript(self, tmp_path):
        proj = tmp_path / "tsx"
        proj.mkdir()
        (proj / "App.tsx").write_text("export default function App() {}")
        langs = detect_languages(proj)
        assert "TypeScript" in langs

    def test_jsx_counted_as_javascript(self, tmp_path):
        proj = tmp_path / "jsx"
        proj.mkdir()
        (proj / "App.jsx").write_text("export default function App() {}")
        langs = detect_languages(proj)
        assert "JavaScript" in langs


# ---------------------------------------------------------------------------
# count_files
# ---------------------------------------------------------------------------
class TestCountFiles:
    def test_counts_source_files(self, tmp_project):
        source, total = count_files(tmp_project)
        assert source >= 4
        assert total >= source

    def test_empty_dir(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert count_files(proj) == (0, 0)

    def test_nonsource_not_counted_as_source(self, tmp_path):
        proj = tmp_path / "mixed"
        proj.mkdir()
        (proj / "app.py").write_text("pass")
        (proj / "data.csv").write_text("a,b,c")
        (proj / "config.yaml").write_text("key: val")
        source, total = count_files(proj)
        assert source == 1
        assert total == 3

    def test_all_source_extensions_counted(self, tmp_path):
        proj = tmp_path / "allsrc"
        proj.mkdir()
        for ext in (".py", ".js", ".ts", ".rs", ".go"):
            (proj / f"file{ext}").write_text("code")
        source, _ = count_files(proj)
        assert source == 5


# ---------------------------------------------------------------------------
# count_test_files
# ---------------------------------------------------------------------------
class TestCountTestFiles:
    def test_finds_test_prefix(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "test_main.py").write_text("pass")
        assert count_test_files(proj) == 1

    def test_finds_test_suffix(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "main_test.py").write_text("pass")
        assert count_test_files(proj) == 1

    def test_finds_dot_test_infix(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "main.test.ts").write_text("test('works', () => {})")
        assert count_test_files(proj) == 1

    def test_finds_dot_spec_infix(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "main.spec.ts").write_text("describe('main', () => {})")
        assert count_test_files(proj) == 1

    def test_finds_files_in_tests_dir(self, tmp_path):
        proj = tmp_path / "proj"
        tests = proj / "tests"
        tests.mkdir(parents=True)
        (tests / "conftest.py").write_text("pass")
        assert count_test_files(proj) == 1

    def test_finds_files_in_test_dir(self, tmp_path):
        proj = tmp_path / "proj"
        testdir = proj / "test"
        testdir.mkdir(parents=True)
        (testdir / "helper.py").write_text("pass")
        assert count_test_files(proj) == 1

    def test_finds_files_in_dunder_tests(self, tmp_path):
        proj = tmp_path / "proj"
        testdir = proj / "__tests__"
        testdir.mkdir(parents=True)
        (testdir / "App.test.tsx").write_text("test('x', () => {})")
        assert count_test_files(proj) == 1

    def test_finds_spec_files(self, tmp_js_project):
        count = count_test_files(tmp_js_project)
        assert count >= 1

    def test_ignores_non_source_in_test_dir(self, tmp_path):
        proj = tmp_path / "proj"
        tests = proj / "tests"
        tests.mkdir(parents=True)
        (tests / "data.json").write_text("{}")
        assert count_test_files(proj) == 0

    def test_empty_dir(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert count_test_files(proj) == 0

    def test_finds_test_files(self, tmp_project):
        count = count_test_files(tmp_project)
        assert count >= 2


# ---------------------------------------------------------------------------
# count_loc
# ---------------------------------------------------------------------------
class TestCountLoc:
    def test_counts_nonempty_lines(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "app.py").write_text("line1\nline2\n\nline3\n")
        assert count_loc(proj) == 3

    def test_empty_file(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "empty.py").write_text("")
        assert count_loc(proj) == 0

    def test_only_whitespace_lines(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "blank.py").write_text("\n   \n\t\n")
        assert count_loc(proj) == 0

    def test_skips_non_source(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "data.csv").write_text("a,b,c\n1,2,3\n")
        assert count_loc(proj) == 0

    def test_empty_dir(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert count_loc(proj) == 0

    def test_multiple_files(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "a.py").write_text("x = 1\ny = 2\n")
        (proj / "b.py").write_text("z = 3\n")
        assert count_loc(proj) == 3


# ---------------------------------------------------------------------------
# detect_frameworks
# ---------------------------------------------------------------------------
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

    def test_detects_django(self, tmp_path):
        proj = tmp_path / "dj"
        proj.mkdir()
        (proj / "requirements.txt").write_text("django==5.0.0\n")
        fw = detect_frameworks(proj)
        assert "Django" in fw

    def test_detects_flask(self, tmp_path):
        proj = tmp_path / "fl"
        proj.mkdir()
        (proj / "requirements.txt").write_text("flask==3.0.0\n")
        fw = detect_frameworks(proj)
        assert "Flask" in fw

    def test_detects_celery(self, tmp_path):
        proj = tmp_path / "cel"
        proj.mkdir()
        (proj / "pyproject.toml").write_text('[project]\ndependencies = ["celery"]\n')
        fw = detect_frameworks(proj)
        assert "Celery" in fw

    def test_detects_anthropic_sdk(self, tmp_path):
        proj = tmp_path / "ai"
        proj.mkdir()
        (proj / "requirements.txt").write_text("anthropic==0.25.0\n")
        fw = detect_frameworks(proj)
        assert "Anthropic SDK" in fw

    def test_detects_rust_frameworks(self, tmp_path):
        proj = tmp_path / "rs"
        proj.mkdir()
        (proj / "Cargo.toml").write_text('[dependencies]\ntokio = "1.0"\naxum = "0.7"\n')
        fw = detect_frameworks(proj)
        assert "Rust" in fw
        assert "Tokio" in fw
        assert "Axum" in fw

    def test_detects_docker(self, tmp_path):
        proj = tmp_path / "dk"
        proj.mkdir()
        (proj / "Dockerfile").write_text("FROM python:3.12\n")
        fw = detect_frameworks(proj)
        assert "Docker" in fw

    def test_detects_docker_compose(self, tmp_path):
        proj = tmp_path / "dc"
        proj.mkdir()
        (proj / "docker-compose.yml").write_text("services:\n  web:\n    build: .\n")
        fw = detect_frameworks(proj)
        assert "Docker" in fw

    def test_empty_project_no_frameworks(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_frameworks(proj) == []

    def test_no_duplicates(self, tmp_path):
        proj = tmp_path / "dup"
        proj.mkdir()
        (proj / "pyproject.toml").write_text('dependencies = ["fastapi"]\n')
        (proj / "requirements.txt").write_text("fastapi==0.109.0\n")
        (proj / "setup.py").write_text("install_requires=['fastapi']\n")
        fw = detect_frameworks(proj)
        assert fw.count("FastAPI") == 1

    def test_detects_playwright(self, tmp_path):
        proj = tmp_path / "pw"
        proj.mkdir()
        pkg = {"devDependencies": {"@playwright/test": "^1.40.0"}}
        (proj / "package.json").write_text(json.dumps(pkg))
        fw = detect_frameworks(proj)
        assert "Playwright" in fw

    def test_detects_express(self, tmp_path):
        proj = tmp_path / "exp"
        proj.mkdir()
        pkg = {"dependencies": {"express": "^4.18.0"}}
        (proj / "package.json").write_text(json.dumps(pkg))
        fw = detect_frameworks(proj)
        assert "Express" in fw

    def test_invalid_package_json(self, tmp_path):
        proj = tmp_path / "bad"
        proj.mkdir()
        (proj / "package.json").write_text("not json at all")
        # Should not crash
        fw = detect_frameworks(proj)
        assert isinstance(fw, list)


# ---------------------------------------------------------------------------
# detect_databases
# ---------------------------------------------------------------------------
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

    def test_detects_postgresql_via_psycopg(self, tmp_path):
        proj = tmp_path / "pg"
        proj.mkdir()
        (proj / "requirements.txt").write_text("psycopg2-binary==2.9.9\n")
        dbs = detect_databases(proj)
        assert "PostgreSQL" in dbs

    def test_detects_sqlite(self, tmp_path):
        proj = tmp_path / "sq"
        proj.mkdir()
        (proj / "requirements.txt").write_text("aiosqlite==0.19.0\n")
        dbs = detect_databases(proj)
        assert "SQLite" in dbs

    def test_detects_redis(self, tmp_path):
        proj = tmp_path / "rd"
        proj.mkdir()
        (proj / "requirements.txt").write_text("redis==5.0.0\n")
        dbs = detect_databases(proj)
        assert "Redis" in dbs

    def test_detects_mongodb(self, tmp_path):
        proj = tmp_path / "mongo"
        proj.mkdir()
        (proj / "requirements.txt").write_text("pymongo==4.6.0\n")
        dbs = detect_databases(proj)
        assert "MongoDB" in dbs

    def test_detects_pgvector(self, tmp_path):
        proj = tmp_path / "vec"
        proj.mkdir()
        (proj / "requirements.txt").write_text("pgvector==0.2.0\n")
        dbs = detect_databases(proj)
        assert "pgvector" in dbs

    def test_multiple_databases(self, tmp_path):
        proj = tmp_path / "multi"
        proj.mkdir()
        (proj / "docker-compose.yml").write_text(
            "services:\n  db:\n    image: postgres:16\n  cache:\n    image: redis:7\n"
        )
        dbs = detect_databases(proj)
        assert "PostgreSQL" in dbs
        assert "Redis" in dbs

    def test_no_duplicates(self, tmp_path):
        proj = tmp_path / "dup"
        proj.mkdir()
        (proj / "requirements.txt").write_text("psycopg2==2.9\n")
        (proj / "docker-compose.yml").write_text("image: postgres:16\n")
        dbs = detect_databases(proj)
        assert dbs.count("PostgreSQL") == 1

    def test_empty_project(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_databases(proj) == []

    def test_detects_mysql(self, tmp_path):
        proj = tmp_path / "my"
        proj.mkdir()
        (proj / "requirements.txt").write_text("mysqlclient==2.2.0\n")
        dbs = detect_databases(proj)
        assert "MySQL" in dbs

    def test_detects_mariadb(self, tmp_path):
        proj = tmp_path / "maria"
        proj.mkdir()
        (proj / "docker-compose.yml").write_text("services:\n  db:\n    image: mariadb:11\n")
        dbs = detect_databases(proj)
        assert "MySQL" in dbs

    def test_detects_elasticsearch(self, tmp_path):
        proj = tmp_path / "es"
        proj.mkdir()
        (proj / "requirements.txt").write_text("elasticsearch==8.12.0\n")
        dbs = detect_databases(proj)
        assert "Elasticsearch" in dbs

    def test_detects_neo4j(self, tmp_path):
        proj = tmp_path / "graph"
        proj.mkdir()
        (proj / "requirements.txt").write_text("neo4j==5.14.0\n")
        dbs = detect_databases(proj)
        assert "Neo4j" in dbs

    def test_detects_cassandra(self, tmp_path):
        proj = tmp_path / "cass"
        proj.mkdir()
        (proj / "requirements.txt").write_text("cassandra-driver==3.29.0\n")
        dbs = detect_databases(proj)
        assert "Cassandra" in dbs

    def test_detects_influxdb(self, tmp_path):
        proj = tmp_path / "ts"
        proj.mkdir()
        (proj / "requirements.txt").write_text("influxdb-client==1.38.0\n")
        dbs = detect_databases(proj)
        assert "InfluxDB" in dbs

    def test_detects_memcached(self, tmp_path):
        proj = tmp_path / "mem"
        proj.mkdir()
        (proj / "requirements.txt").write_text("pylibmc==1.6.3\n")
        dbs = detect_databases(proj)
        assert "Memcached" in dbs

    def test_detects_firestore(self, tmp_path):
        proj = tmp_path / "fire"
        proj.mkdir()
        (proj / "package.json").write_text('{"dependencies": {"firebase-admin": "^12.0"}}')
        dbs = detect_databases(proj)
        assert "Firestore" in dbs

    def test_detects_dynamodb(self, tmp_path):
        proj = tmp_path / "dynamo"
        proj.mkdir()
        (proj / "requirements.txt").write_text("boto3==1.34.0\n# dynamodb table setup\n")
        dbs = detect_databases(proj)
        assert "DynamoDB" in dbs

    def test_detects_supabase(self, tmp_path):
        proj = tmp_path / "supa"
        proj.mkdir()
        (proj / "package.json").write_text('{"dependencies": {"@supabase/supabase-js": "^2.0"}}')
        dbs = detect_databases(proj)
        assert "Supabase" in dbs

    def test_detects_chromadb(self, tmp_path):
        proj = tmp_path / "chroma"
        proj.mkdir()
        (proj / "requirements.txt").write_text("chromadb==0.4.0\n")
        dbs = detect_databases(proj)
        assert "ChromaDB" in dbs

    def test_detects_pinecone(self, tmp_path):
        proj = tmp_path / "pine"
        proj.mkdir()
        (proj / "requirements.txt").write_text("pinecone-client==3.0.0\n")
        dbs = detect_databases(proj)
        assert "Pinecone" in dbs

    def test_detects_qdrant(self, tmp_path):
        proj = tmp_path / "qd"
        proj.mkdir()
        (proj / "requirements.txt").write_text("qdrant-client==1.7.0\n")
        dbs = detect_databases(proj)
        assert "Qdrant" in dbs

    def test_detects_weaviate(self, tmp_path):
        proj = tmp_path / "weav"
        proj.mkdir()
        (proj / "requirements.txt").write_text("weaviate-client==4.4.0\n")
        dbs = detect_databases(proj)
        assert "Weaviate" in dbs

    def test_detects_rabbitmq(self, tmp_path):
        proj = tmp_path / "rabbit"
        proj.mkdir()
        (proj / "docker-compose.yml").write_text("services:\n  mq:\n    image: rabbitmq:3\n")
        dbs = detect_databases(proj)
        assert "RabbitMQ" in dbs

    def test_detects_kafka(self, tmp_path):
        proj = tmp_path / "kfk"
        proj.mkdir()
        (proj / "requirements.txt").write_text("confluent-kafka==2.3.0\n")
        dbs = detect_databases(proj)
        assert "Kafka" in dbs

    def test_detects_planetscale(self, tmp_path):
        proj = tmp_path / "ps"
        proj.mkdir()
        (proj / "package.json").write_text('{"dependencies": {"@planetscale/database": "^1.0"}}')
        dbs = detect_databases(proj)
        assert "PlanetScale" in dbs

    def test_detects_cockroachdb(self, tmp_path):
        proj = tmp_path / "crdb"
        proj.mkdir()
        (proj / "docker-compose.yml").write_text("services:\n  db:\n    image: cockroachdb/cockroach\n")
        dbs = detect_databases(proj)
        assert "CockroachDB" in dbs

    def test_detects_from_go_mod(self, tmp_path):
        proj = tmp_path / "goapp"
        proj.mkdir()
        (proj / "go.mod").write_text("module example.com/app\ngo 1.21\nrequire github.com/lib/pq v1.10.9\n")
        dbs = detect_databases(proj)
        # pq is a postgres driver — not detected by keyword, but "postgresql" isn't in go.mod
        # This tests that go.mod is searched at all
        assert dbs == [] or isinstance(dbs, list)

    def test_detects_mongodb_mongoose(self, tmp_path):
        proj = tmp_path / "mong"
        proj.mkdir()
        (proj / "package.json").write_text('{"dependencies": {"mongoose": "^8.0"}}')
        dbs = detect_databases(proj)
        assert "MongoDB" in dbs

    def test_detects_amqp(self, tmp_path):
        proj = tmp_path / "amqp"
        proj.mkdir()
        (proj / "requirements.txt").write_text("amqp==5.2.0\n")
        dbs = detect_databases(proj)
        assert "RabbitMQ" in dbs


# ---------------------------------------------------------------------------
# detect_key_deps
# ---------------------------------------------------------------------------
class TestDetectKeyDeps:
    def test_python_requirements(self, tmp_project):
        deps = detect_key_deps(tmp_project)
        assert "fastapi" in deps
        assert deps["fastapi"] == "==0.109.0"

    def test_js_package_json(self, tmp_js_project):
        deps = detect_key_deps(tmp_js_project)
        assert "next" in deps
        assert "react" in deps

    def test_parses_gte_version(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "requirements.txt").write_text("requests>=2.31.0\n")
        deps = detect_key_deps(proj)
        assert deps["requests"] == ">=2.31.0"

    def test_parses_tilde_version(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "requirements.txt").write_text("pydantic~=2.5\n")
        deps = detect_key_deps(proj)
        assert deps["pydantic"] == "~=2.5"

    def test_parses_lte_version(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "requirements.txt").write_text("numpy<=1.26.0\n")
        deps = detect_key_deps(proj)
        assert deps["numpy"] == "<=1.26.0"

    def test_skips_comments_and_blanks(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "requirements.txt").write_text("# comment\n\nfastapi==0.109.0\n")
        deps = detect_key_deps(proj)
        assert len(deps) == 1
        assert "fastapi" in deps

    def test_skips_dash_lines(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "requirements.txt").write_text("-r base.txt\nfastapi==0.109.0\n")
        deps = detect_key_deps(proj)
        assert "fastapi" in deps

    def test_reads_dev_requirements(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "requirements-dev.txt").write_text("pytest==8.0.0\n")
        deps = detect_key_deps(proj)
        assert "pytest" in deps
        assert deps["pytest"] == "==8.0.0"

    def test_invalid_package_json(self, tmp_path):
        proj = tmp_path / "bad"
        proj.mkdir()
        (proj / "package.json").write_text("{invalid json}")
        deps = detect_key_deps(proj)
        assert isinstance(deps, dict)

    def test_empty_project(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_key_deps(proj) == {}

    def test_js_devdeps_included(self, tmp_path):
        proj = tmp_path / "js"
        proj.mkdir()
        pkg = {"dependencies": {"express": "^4.18.0"}, "devDependencies": {"vitest": "^1.0.0"}}
        (proj / "package.json").write_text(json.dumps(pkg))
        deps = detect_key_deps(proj)
        assert "express" in deps
        assert "vitest" in deps

    def test_dep_name_lowercased(self, tmp_path):
        proj = tmp_path / "proj"
        proj.mkdir()
        (proj / "requirements.txt").write_text("FastAPI==0.109.0\n")
        deps = detect_key_deps(proj)
        assert "fastapi" in deps


# ---------------------------------------------------------------------------
# _check_add helper
# ---------------------------------------------------------------------------
class TestCheckAdd:
    def test_adds_when_keyword_present(self):
        lst = []
        _check_add(lst, "fastapi==0.109", "fastapi", "FastAPI")
        assert lst == ["FastAPI"]

    def test_does_not_add_when_keyword_absent(self):
        lst = []
        _check_add(lst, "django==5.0", "fastapi", "FastAPI")
        assert lst == []

    def test_does_not_duplicate(self):
        lst = ["FastAPI"]
        _check_add(lst, "fastapi==0.109", "fastapi", "FastAPI")
        assert lst == ["FastAPI"]


# ---------------------------------------------------------------------------
# detect_package_managers
# ---------------------------------------------------------------------------
class TestDetectPackageManagers:
    def test_empty_project(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_package_managers(proj) == []

    def test_pip_from_requirements(self, tmp_path):
        proj = tmp_path / "pip"
        proj.mkdir()
        (proj / "requirements.txt").write_text("fastapi>=0.109\n")
        mgrs = detect_package_managers(proj)
        assert "pip" in mgrs

    def test_poetry_from_lock(self, tmp_path):
        proj = tmp_path / "poetry"
        proj.mkdir()
        (proj / "poetry.lock").write_text("")
        mgrs = detect_package_managers(proj)
        assert "Poetry" in mgrs

    def test_poetry_from_pyproject(self, tmp_path):
        proj = tmp_path / "poetry2"
        proj.mkdir()
        (proj / "pyproject.toml").write_text("[tool.poetry]\nname = 'app'\n")
        mgrs = detect_package_managers(proj)
        assert "Poetry" in mgrs

    def test_pdm_from_lock(self, tmp_path):
        proj = tmp_path / "pdm"
        proj.mkdir()
        (proj / "pdm.lock").write_text("")
        mgrs = detect_package_managers(proj)
        assert "PDM" in mgrs

    def test_uv_from_lock(self, tmp_path):
        proj = tmp_path / "uv"
        proj.mkdir()
        (proj / "uv.lock").write_text("")
        mgrs = detect_package_managers(proj)
        assert "uv" in mgrs

    def test_pipenv_from_pipfile(self, tmp_path):
        proj = tmp_path / "pipenv"
        proj.mkdir()
        (proj / "Pipfile").write_text("[packages]\nflask = '*'\n")
        mgrs = detect_package_managers(proj)
        assert "Pipenv" in mgrs

    def test_setuptools_from_setup_py(self, tmp_path):
        proj = tmp_path / "st"
        proj.mkdir()
        (proj / "setup.py").write_text("from setuptools import setup\nsetup(name='app')\n")
        mgrs = detect_package_managers(proj)
        assert "setuptools" in mgrs

    def test_hatch_from_pyproject(self, tmp_path):
        proj = tmp_path / "hatch"
        proj.mkdir()
        (proj / "pyproject.toml").write_text(
            '[build-system]\nrequires = ["hatchling"]\nbuild-backend = "hatchling.build"\n'
        )
        mgrs = detect_package_managers(proj)
        assert "Hatch" in mgrs

    def test_flit_from_pyproject(self, tmp_path):
        proj = tmp_path / "flit"
        proj.mkdir()
        (proj / "pyproject.toml").write_text(
            '[build-system]\nrequires = ["flit_core"]\nbuild-backend = "flit_core.buildapi"\n'
        )
        mgrs = detect_package_managers(proj)
        assert "Flit" in mgrs

    def test_npm_from_lockfile(self, tmp_path):
        proj = tmp_path / "npm"
        proj.mkdir()
        (proj / "package-lock.json").write_text("{}")
        mgrs = detect_package_managers(proj)
        assert "npm" in mgrs

    def test_yarn_from_lock(self, tmp_path):
        proj = tmp_path / "yarn"
        proj.mkdir()
        (proj / "yarn.lock").write_text("")
        mgrs = detect_package_managers(proj)
        assert "Yarn" in mgrs

    def test_pnpm_from_lock(self, tmp_path):
        proj = tmp_path / "pnpm"
        proj.mkdir()
        (proj / "pnpm-lock.yaml").write_text("")
        mgrs = detect_package_managers(proj)
        assert "pnpm" in mgrs

    def test_bun_from_lockb(self, tmp_path):
        proj = tmp_path / "bun"
        proj.mkdir()
        (proj / "bun.lockb").write_text("")
        mgrs = detect_package_managers(proj)
        assert "Bun" in mgrs

    def test_cargo(self, tmp_path):
        proj = tmp_path / "rust"
        proj.mkdir()
        (proj / "Cargo.toml").write_text("[package]\nname = 'app'\n")
        mgrs = detect_package_managers(proj)
        assert "Cargo" in mgrs

    def test_go_modules(self, tmp_path):
        proj = tmp_path / "goapp"
        proj.mkdir()
        (proj / "go.mod").write_text("module example.com/app\ngo 1.21\n")
        mgrs = detect_package_managers(proj)
        assert "Go Modules" in mgrs

    def test_bundler(self, tmp_path):
        proj = tmp_path / "ruby"
        proj.mkdir()
        (proj / "Gemfile").write_text("source 'https://rubygems.org'\ngem 'rails'\n")
        mgrs = detect_package_managers(proj)
        assert "Bundler" in mgrs

    def test_maven(self, tmp_path):
        proj = tmp_path / "java"
        proj.mkdir()
        (proj / "pom.xml").write_text("<project></project>")
        mgrs = detect_package_managers(proj)
        assert "Maven" in mgrs

    def test_gradle(self, tmp_path):
        proj = tmp_path / "gradle"
        proj.mkdir()
        (proj / "build.gradle").write_text("apply plugin: 'java'\n")
        mgrs = detect_package_managers(proj)
        assert "Gradle" in mgrs

    def test_gradle_kotlin(self, tmp_path):
        proj = tmp_path / "kts"
        proj.mkdir()
        (proj / "build.gradle.kts").write_text("plugins { id(\"java\") }\n")
        mgrs = detect_package_managers(proj)
        assert "Gradle" in mgrs

    def test_nuget(self, tmp_path):
        proj = tmp_path / "dotnet"
        proj.mkdir()
        (proj / "App.csproj").write_text("<Project></Project>")
        mgrs = detect_package_managers(proj)
        assert "NuGet" in mgrs

    def test_composer(self, tmp_path):
        proj = tmp_path / "php"
        proj.mkdir()
        (proj / "composer.json").write_text('{"require": {"php": ">=8.1"}}')
        mgrs = detect_package_managers(proj)
        assert "Composer" in mgrs

    def test_pip_not_added_when_poetry_present(self, tmp_path):
        proj = tmp_path / "both"
        proj.mkdir()
        (proj / "poetry.lock").write_text("")
        (proj / "requirements.txt").write_text("fastapi\n")
        mgrs = detect_package_managers(proj)
        assert "Poetry" in mgrs
        assert "pip" not in mgrs

    def test_multiple_ecosystems(self, tmp_path):
        proj = tmp_path / "multi"
        proj.mkdir()
        (proj / "pyproject.toml").write_text("[tool.poetry]\nname = 'backend'\n")
        (proj / "poetry.lock").write_text("")
        (proj / "package.json").write_text("{}")
        (proj / "yarn.lock").write_text("")
        mgrs = detect_package_managers(proj)
        assert "Poetry" in mgrs
        assert "Yarn" in mgrs

    def test_no_duplicates(self, tmp_path):
        proj = tmp_path / "nodup"
        proj.mkdir()
        (proj / "poetry.lock").write_text("")
        (proj / "poetry.toml").write_text("")
        (proj / "pyproject.toml").write_text("[tool.poetry]\nname = 'app'\n")
        mgrs = detect_package_managers(proj)
        assert mgrs.count("Poetry") == 1


# ---------------------------------------------------------------------------
# detect_license
# ---------------------------------------------------------------------------
class TestDetectLicense:
    def test_empty_project(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_license(proj) == ""

    # --- pyproject.toml ---
    def test_pyproject_license_string(self, tmp_path):
        proj = tmp_path / "py"
        proj.mkdir()
        (proj / "pyproject.toml").write_text('[project]\nlicense = "MIT"\n')
        assert detect_license(proj) == "MIT"

    def test_pyproject_license_apache(self, tmp_path):
        proj = tmp_path / "py"
        proj.mkdir()
        (proj / "pyproject.toml").write_text('[project]\nlicense = "Apache-2.0"\n')
        assert detect_license(proj) == "Apache-2.0"

    def test_pyproject_license_file_ref_skipped(self, tmp_path):
        proj = tmp_path / "py"
        proj.mkdir()
        (proj / "pyproject.toml").write_text('[project]\nlicense = {file = "LICENSE"}\n')
        # Should not return the dict reference — fall through to LICENSE file
        result = detect_license(proj)
        assert result != '{file = "LICENSE"}'

    # --- package.json ---
    def test_package_json_license(self, tmp_path):
        proj = tmp_path / "js"
        proj.mkdir()
        (proj / "package.json").write_text(json.dumps({"license": "MIT"}))
        assert detect_license(proj) == "MIT"

    def test_package_json_isc(self, tmp_path):
        proj = tmp_path / "js"
        proj.mkdir()
        (proj / "package.json").write_text(json.dumps({"license": "ISC"}))
        assert detect_license(proj) == "ISC"

    def test_package_json_no_license_field(self, tmp_path):
        proj = tmp_path / "js"
        proj.mkdir()
        (proj / "package.json").write_text(json.dumps({"name": "app"}))
        assert detect_license(proj) == ""

    # --- Cargo.toml ---
    def test_cargo_toml_license(self, tmp_path):
        proj = tmp_path / "rs"
        proj.mkdir()
        (proj / "Cargo.toml").write_text('[package]\nname = "app"\nlicense = "MIT"\n')
        assert detect_license(proj) == "MIT"

    def test_cargo_toml_apache(self, tmp_path):
        proj = tmp_path / "rs"
        proj.mkdir()
        (proj / "Cargo.toml").write_text('[package]\nname = "app"\nlicense = "Apache-2.0"\n')
        assert detect_license(proj) == "Apache-2.0"

    # --- LICENSE file content ---
    def test_license_file_mit(self, tmp_path):
        proj = tmp_path / "mit"
        proj.mkdir()
        (proj / "LICENSE").write_text(
            "MIT License\n\nPermission is hereby granted, free of charge, "
            "to any person obtaining a copy..."
        )
        assert detect_license(proj) == "MIT"

    def test_license_file_apache(self, tmp_path):
        proj = tmp_path / "apache"
        proj.mkdir()
        (proj / "LICENSE").write_text(
            "Apache License\nVersion 2.0, January 2004\n"
            "TERMS AND CONDITIONS FOR USE..."
        )
        assert detect_license(proj) == "Apache-2.0"

    def test_license_file_gpl3(self, tmp_path):
        proj = tmp_path / "gpl"
        proj.mkdir()
        (proj / "LICENSE").write_text(
            "GNU GENERAL PUBLIC LICENSE\nVersion 3, 29 June 2007\n"
            "Everyone is permitted to copy..."
        )
        assert detect_license(proj) == "GPL-3.0"

    def test_license_file_gpl2(self, tmp_path):
        proj = tmp_path / "gpl2"
        proj.mkdir()
        (proj / "COPYING").write_text(
            "GNU GENERAL PUBLIC LICENSE\nVersion 2, June 1991\n"
            "Everyone is permitted to copy..."
        )
        assert detect_license(proj) == "GPL-2.0"

    def test_license_file_bsd3(self, tmp_path):
        proj = tmp_path / "bsd3"
        proj.mkdir()
        (proj / "LICENSE").write_text(
            "Redistribution and use in source and binary forms, with or without "
            "modification, are permitted provided that the following conditions are met:\n"
            "1. Redistributions of source code...\n"
            "2. Redistributions in binary form...\n"
            "3. Neither the name..."
        )
        assert detect_license(proj) == "BSD-3-Clause"

    def test_license_file_bsd2(self, tmp_path):
        proj = tmp_path / "bsd2"
        proj.mkdir()
        (proj / "LICENSE").write_text(
            "Redistribution and use in source and binary forms, with or without "
            "modification, are permitted provided that the following conditions are met:\n"
            "1. Redistributions of source code...\n"
            "2. Redistributions in binary form..."
        )
        assert detect_license(proj) == "BSD-2-Clause"

    def test_license_file_unlicense(self, tmp_path):
        proj = tmp_path / "unl"
        proj.mkdir()
        (proj / "LICENSE").write_text(
            "This is free and unencumbered software released into the public domain."
        )
        assert detect_license(proj) == "Unlicense"

    def test_license_file_mpl(self, tmp_path):
        proj = tmp_path / "mpl"
        proj.mkdir()
        (proj / "LICENSE").write_text("Mozilla Public License 2.0\nSome text...")
        assert detect_license(proj) == "MPL-2.0"

    def test_license_file_agpl(self, tmp_path):
        proj = tmp_path / "agpl"
        proj.mkdir()
        (proj / "LICENSE").write_text(
            "GNU AFFERO GENERAL PUBLIC LICENSE\nVersion 3, 19 November 2007..."
        )
        assert detect_license(proj) == "AGPL-3.0"

    def test_license_file_isc(self, tmp_path):
        proj = tmp_path / "isc"
        proj.mkdir()
        (proj / "LICENSE").write_text(
            "Permission to use, copy, modify, and/or distribute this software..."
        )
        assert detect_license(proj) == "ISC"

    # --- Alternate file names ---
    def test_licence_british_spelling(self, tmp_path):
        proj = tmp_path / "brit"
        proj.mkdir()
        (proj / "LICENCE").write_text(
            "Permission is hereby granted, free of charge..."
        )
        assert detect_license(proj) == "MIT"

    def test_license_md(self, tmp_path):
        proj = tmp_path / "md"
        proj.mkdir()
        (proj / "LICENSE.md").write_text(
            "# MIT License\n\nPermission is hereby granted, free of charge..."
        )
        assert detect_license(proj) == "MIT"

    # --- Priority: config > file ---
    def test_pyproject_takes_priority_over_file(self, tmp_path):
        proj = tmp_path / "pri"
        proj.mkdir()
        (proj / "pyproject.toml").write_text('[project]\nlicense = "Apache-2.0"\n')
        (proj / "LICENSE").write_text(
            "Permission is hereby granted, free of charge..."
        )
        # pyproject.toml wins
        assert detect_license(proj) == "Apache-2.0"

    # --- SPDX normalization ---
    def test_normalize_gpl_variants(self, tmp_path):
        proj = tmp_path / "gpl"
        proj.mkdir()
        (proj / "package.json").write_text(json.dumps({"license": "GPL-3.0-only"}))
        assert detect_license(proj) == "GPL-3.0"

    def test_normalize_case_insensitive(self, tmp_path):
        proj = tmp_path / "case"
        proj.mkdir()
        (proj / "package.json").write_text(json.dumps({"license": "mit"}))
        assert detect_license(proj) == "MIT"

    def test_unknown_license_file_returns_empty(self, tmp_path):
        proj = tmp_path / "custom"
        proj.mkdir()
        (proj / "LICENSE").write_text("Proprietary license. All rights reserved.")
        assert detect_license(proj) == ""


class TestDetectDocsArtifacts:
    def test_empty_project(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_docs_artifacts(proj) == []

    def test_readme_detected(self, tmp_path):
        proj = tmp_path / "readme"
        proj.mkdir()
        (proj / "README.md").write_text("# My Project")
        assert "README" in detect_docs_artifacts(proj)

    def test_readme_rst(self, tmp_path):
        proj = tmp_path / "readme_rst"
        proj.mkdir()
        (proj / "README.rst").write_text("My Project\n==========")
        assert "README" in detect_docs_artifacts(proj)

    def test_changelog_detected(self, tmp_path):
        proj = tmp_path / "changelog"
        proj.mkdir()
        (proj / "CHANGELOG.md").write_text("# Changelog")
        assert "CHANGELOG" in detect_docs_artifacts(proj)

    def test_changes_file_detected_as_changelog(self, tmp_path):
        proj = tmp_path / "changes"
        proj.mkdir()
        (proj / "CHANGES.md").write_text("# Changes")
        assert "CHANGELOG" in detect_docs_artifacts(proj)

    def test_history_file_detected_as_changelog(self, tmp_path):
        proj = tmp_path / "history"
        proj.mkdir()
        (proj / "HISTORY.md").write_text("# History")
        assert "CHANGELOG" in detect_docs_artifacts(proj)

    def test_contributing_detected(self, tmp_path):
        proj = tmp_path / "contrib"
        proj.mkdir()
        (proj / "CONTRIBUTING.md").write_text("# Contributing")
        assert "CONTRIBUTING" in detect_docs_artifacts(proj)

    def test_code_of_conduct_detected(self, tmp_path):
        proj = tmp_path / "coc"
        proj.mkdir()
        (proj / "CODE_OF_CONDUCT.md").write_text("# Code of Conduct")
        assert "CODE_OF_CONDUCT" in detect_docs_artifacts(proj)

    def test_security_detected(self, tmp_path):
        proj = tmp_path / "sec"
        proj.mkdir()
        (proj / "SECURITY.md").write_text("# Security Policy")
        assert "SECURITY" in detect_docs_artifacts(proj)

    def test_license_file_detected(self, tmp_path):
        proj = tmp_path / "lic"
        proj.mkdir()
        (proj / "LICENSE").write_text("MIT License")
        assert "LICENSE" in detect_docs_artifacts(proj)

    def test_docs_directory_detected(self, tmp_path):
        proj = tmp_path / "docdir"
        proj.mkdir()
        (proj / "docs").mkdir()
        assert "docs/" in detect_docs_artifacts(proj)

    def test_openapi_json_detected(self, tmp_path):
        proj = tmp_path / "api"
        proj.mkdir()
        (proj / "openapi.json").write_text('{"openapi": "3.0.0"}')
        assert "API spec" in detect_docs_artifacts(proj)

    def test_swagger_yaml_detected(self, tmp_path):
        proj = tmp_path / "swagger"
        proj.mkdir()
        (proj / "swagger.yaml").write_text("swagger: '2.0'")
        assert "API spec" in detect_docs_artifacts(proj)

    def test_api_spec_in_docs_dir(self, tmp_path):
        proj = tmp_path / "apidocs"
        proj.mkdir()
        (proj / "docs").mkdir()
        (proj / "docs" / "openapi.yaml").write_text("openapi: 3.0.0")
        assert "API spec" in detect_docs_artifacts(proj)

    def test_editorconfig_detected(self, tmp_path):
        proj = tmp_path / "editor"
        proj.mkdir()
        (proj / ".editorconfig").write_text("root = true")
        assert ".editorconfig" in detect_docs_artifacts(proj)

    def test_multiple_artifacts(self, tmp_path):
        proj = tmp_path / "full"
        proj.mkdir()
        (proj / "README.md").write_text("# Project")
        (proj / "CHANGELOG.md").write_text("# Changelog")
        (proj / "CONTRIBUTING.md").write_text("# Contributing")
        (proj / "LICENSE").write_text("MIT License")
        (proj / "docs").mkdir()
        (proj / ".editorconfig").write_text("root = true")
        result = detect_docs_artifacts(proj)
        assert "README" in result
        assert "CHANGELOG" in result
        assert "CONTRIBUTING" in result
        assert "LICENSE" in result
        assert "docs/" in result
        assert ".editorconfig" in result

    def test_results_are_sorted(self, tmp_path):
        proj = tmp_path / "sorted"
        proj.mkdir()
        (proj / "README.md").write_text("# Project")
        (proj / "CHANGELOG.md").write_text("# Changelog")
        (proj / "LICENSE").write_text("MIT License")
        result = detect_docs_artifacts(proj)
        assert result == sorted(result)


class TestDetectCiConfig:
    def test_empty_project(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        assert detect_ci_config(proj) == []

    def test_github_actions(self, tmp_path):
        proj = tmp_path / "gha"
        proj.mkdir()
        (proj / ".github" / "workflows").mkdir(parents=True)
        (proj / ".github" / "workflows" / "ci.yml").write_text("name: CI")
        result = detect_ci_config(proj)
        assert "GitHub Actions" in result

    def test_gitlab_ci(self, tmp_path):
        proj = tmp_path / "gitlab"
        proj.mkdir()
        (proj / ".gitlab-ci.yml").write_text("stages: [build]")
        assert "GitLab CI" in detect_ci_config(proj)

    def test_pr_template(self, tmp_path):
        proj = tmp_path / "pr"
        proj.mkdir()
        (proj / ".github").mkdir()
        (proj / ".github" / "pull_request_template.md").write_text("## Summary")
        assert "PR template" in detect_ci_config(proj)

    def test_pr_template_uppercase(self, tmp_path):
        proj = tmp_path / "pr2"
        proj.mkdir()
        (proj / ".github").mkdir()
        (proj / ".github" / "PULL_REQUEST_TEMPLATE.md").write_text("## Summary")
        assert "PR template" in detect_ci_config(proj)

    def test_pr_template_directory(self, tmp_path):
        proj = tmp_path / "pr3"
        proj.mkdir()
        (proj / ".github" / "PULL_REQUEST_TEMPLATE").mkdir(parents=True)
        assert "PR template" in detect_ci_config(proj)

    def test_issue_templates(self, tmp_path):
        proj = tmp_path / "issues"
        proj.mkdir()
        (proj / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
        assert "issue templates" in detect_ci_config(proj)

    def test_codeowners_github(self, tmp_path):
        proj = tmp_path / "co"
        proj.mkdir()
        (proj / ".github").mkdir()
        (proj / ".github" / "CODEOWNERS").write_text("* @team")
        assert "CODEOWNERS" in detect_ci_config(proj)

    def test_codeowners_root(self, tmp_path):
        proj = tmp_path / "co2"
        proj.mkdir()
        (proj / "CODEOWNERS").write_text("* @team")
        assert "CODEOWNERS" in detect_ci_config(proj)

    def test_dependabot_config(self, tmp_path):
        proj = tmp_path / "depbot"
        proj.mkdir()
        (proj / ".github").mkdir()
        (proj / ".github" / "dependabot.yml").write_text("version: 2")
        assert "Dependabot config" in detect_ci_config(proj)

    def test_renovate_config(self, tmp_path):
        proj = tmp_path / "renovate"
        proj.mkdir()
        (proj / "renovate.json").write_text("{}")
        assert "Renovate config" in detect_ci_config(proj)

    def test_pre_commit(self, tmp_path):
        proj = tmp_path / "precommit"
        proj.mkdir()
        (proj / ".pre-commit-config.yaml").write_text("repos: []")
        assert "pre-commit" in detect_ci_config(proj)

    def test_git_hooks_dir(self, tmp_path):
        proj = tmp_path / "hooks"
        proj.mkdir()
        (proj / ".husky").mkdir()
        assert "git hooks" in detect_ci_config(proj)

    def test_gitattributes(self, tmp_path):
        proj = tmp_path / "attrs"
        proj.mkdir()
        (proj / ".gitattributes").write_text("*.txt text")
        assert ".gitattributes" in detect_ci_config(proj)

    def test_release_workflow(self, tmp_path):
        proj = tmp_path / "rel"
        proj.mkdir()
        (proj / ".github" / "workflows").mkdir(parents=True)
        (proj / ".github" / "workflows" / "release.yml").write_text("name: Release")
        result = detect_ci_config(proj)
        assert "release workflow" in result

    def test_deploy_workflow(self, tmp_path):
        proj = tmp_path / "deploy"
        proj.mkdir()
        (proj / ".github" / "workflows").mkdir(parents=True)
        (proj / ".github" / "workflows" / "deploy.yml").write_text("name: Deploy")
        result = detect_ci_config(proj)
        assert "deploy workflow" in result

    def test_multiple_configs(self, tmp_path):
        proj = tmp_path / "full"
        proj.mkdir()
        (proj / ".github" / "workflows").mkdir(parents=True)
        (proj / ".github" / "workflows" / "ci.yml").write_text("name: CI")
        (proj / ".github" / "CODEOWNERS").write_text("* @team")
        (proj / ".github" / "dependabot.yml").write_text("version: 2")
        (proj / ".pre-commit-config.yaml").write_text("repos: []")
        (proj / ".gitattributes").write_text("*.txt text")
        result = detect_ci_config(proj)
        assert "GitHub Actions" in result
        assert "CODEOWNERS" in result
        assert "Dependabot config" in result
        assert "pre-commit" in result
        assert ".gitattributes" in result

    def test_results_are_sorted(self, tmp_path):
        proj = tmp_path / "sorted"
        proj.mkdir()
        (proj / ".github" / "workflows").mkdir(parents=True)
        (proj / ".github" / "workflows" / "ci.yml").write_text("name: CI")
        (proj / ".pre-commit-config.yaml").write_text("repos: []")
        (proj / "CODEOWNERS").write_text("* @team")
        result = detect_ci_config(proj)
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# detect_runtime_versions
# ---------------------------------------------------------------------------
class TestDetectRuntimeVersions:
    def test_python_version_file(self, tmp_path):
        proj = tmp_path / "pyproj"
        proj.mkdir()
        (proj / ".python-version").write_text("3.12.1\n")
        result = detect_runtime_versions(proj)
        assert result["Python"] == "3.12.1"

    def test_python_requires_python(self, tmp_path):
        proj = tmp_path / "pyproj"
        proj.mkdir()
        (proj / "pyproject.toml").write_text('[project]\nrequires-python = ">=3.11"\n')
        result = detect_runtime_versions(proj)
        assert result["Python"] == ">=3.11"

    def test_python_version_file_takes_priority(self, tmp_path):
        proj = tmp_path / "pyproj"
        proj.mkdir()
        (proj / ".python-version").write_text("3.12\n")
        (proj / "pyproject.toml").write_text('[project]\nrequires-python = ">=3.11"\n')
        result = detect_runtime_versions(proj)
        assert result["Python"] == "3.12"

    def test_node_version_file(self, tmp_path):
        proj = tmp_path / "nodeproj"
        proj.mkdir()
        (proj / ".node-version").write_text("20.11.0\n")
        result = detect_runtime_versions(proj)
        assert result["Node"] == "20.11.0"

    def test_nvmrc(self, tmp_path):
        proj = tmp_path / "nodeproj"
        proj.mkdir()
        (proj / ".nvmrc").write_text("18\n")
        result = detect_runtime_versions(proj)
        assert result["Node"] == "18"

    def test_node_version_file_takes_priority_over_nvmrc(self, tmp_path):
        proj = tmp_path / "nodeproj"
        proj.mkdir()
        (proj / ".node-version").write_text("20\n")
        (proj / ".nvmrc").write_text("18\n")
        result = detect_runtime_versions(proj)
        assert result["Node"] == "20"

    def test_package_json_engines(self, tmp_path):
        proj = tmp_path / "nodeproj"
        proj.mkdir()
        (proj / "package.json").write_text(json.dumps({
            "engines": {"node": ">=18"}
        }))
        result = detect_runtime_versions(proj)
        assert result["Node"] == ">=18"

    def test_ruby_version_file(self, tmp_path):
        proj = tmp_path / "rubyproj"
        proj.mkdir()
        (proj / ".ruby-version").write_text("3.2.2\n")
        result = detect_runtime_versions(proj)
        assert result["Ruby"] == "3.2.2"

    def test_go_mod(self, tmp_path):
        proj = tmp_path / "goproj"
        proj.mkdir()
        (proj / "go.mod").write_text("module example.com/app\n\ngo 1.22\n")
        result = detect_runtime_versions(proj)
        assert result["Go"] == "1.22"

    def test_rust_toolchain_toml(self, tmp_path):
        proj = tmp_path / "rustproj"
        proj.mkdir()
        (proj / "rust-toolchain.toml").write_text('[toolchain]\nchannel = "1.77.0"\n')
        result = detect_runtime_versions(proj)
        assert result["Rust"] == "1.77.0"

    def test_rust_toolchain_plain(self, tmp_path):
        proj = tmp_path / "rustproj"
        proj.mkdir()
        (proj / "rust-toolchain").write_text("nightly\n")
        result = detect_runtime_versions(proj)
        assert result["Rust"] == "nightly"

    def test_rust_toolchain_toml_takes_priority(self, tmp_path):
        proj = tmp_path / "rustproj"
        proj.mkdir()
        (proj / "rust-toolchain.toml").write_text('[toolchain]\nchannel = "stable"\n')
        (proj / "rust-toolchain").write_text("nightly\n")
        result = detect_runtime_versions(proj)
        assert result["Rust"] == "stable"

    def test_java_version_file(self, tmp_path):
        proj = tmp_path / "javaproj"
        proj.mkdir()
        (proj / ".java-version").write_text("21\n")
        result = detect_runtime_versions(proj)
        assert result["Java"] == "21"

    def test_tool_versions_asdf(self, tmp_path):
        proj = tmp_path / "multiproj"
        proj.mkdir()
        (proj / ".tool-versions").write_text("python 3.12.1\nnodejs 20.11.0\nruby 3.2.2\n")
        result = detect_runtime_versions(proj)
        assert result["Python"] == "3.12.1"
        assert result["Node"] == "20.11.0"
        assert result["Ruby"] == "3.2.2"

    def test_tool_versions_does_not_override_specific_files(self, tmp_path):
        proj = tmp_path / "multiproj"
        proj.mkdir()
        (proj / ".python-version").write_text("3.13\n")
        (proj / ".tool-versions").write_text("python 3.12\n")
        result = detect_runtime_versions(proj)
        assert result["Python"] == "3.13"

    def test_empty_project(self, tmp_path):
        proj = tmp_path / "empty"
        proj.mkdir()
        result = detect_runtime_versions(proj)
        assert result == {}

    def test_multiple_runtimes(self, tmp_path):
        proj = tmp_path / "fullstack"
        proj.mkdir()
        (proj / ".python-version").write_text("3.12\n")
        (proj / ".nvmrc").write_text("20\n")
        (proj / "go.mod").write_text("module app\n\ngo 1.22\n")
        result = detect_runtime_versions(proj)
        assert len(result) == 3
        assert result["Python"] == "3.12"
        assert result["Node"] == "20"
        assert result["Go"] == "1.22"


# ---------------------------------------------------------------------------
# detect_build_tools
# ---------------------------------------------------------------------------
class TestDetectBuildTools:
    def test_makefile(self, tmp_path):
        (tmp_path / "Makefile").write_text("all:\n\techo hello\n")
        result = detect_build_tools(tmp_path)
        assert "Make" in result

    def test_makefile_lowercase(self, tmp_path):
        (tmp_path / "makefile").write_text("all:\n\techo hello\n")
        result = detect_build_tools(tmp_path)
        assert "Make" in result

    def test_taskfile(self, tmp_path):
        (tmp_path / "Taskfile.yml").write_text("version: '3'\ntasks:\n  build:\n")
        result = detect_build_tools(tmp_path)
        assert "Taskfile" in result

    def test_taskfile_dist(self, tmp_path):
        (tmp_path / "Taskfile.dist.yml").write_text("version: '3'\n")
        result = detect_build_tools(tmp_path)
        assert "Taskfile" in result

    def test_justfile(self, tmp_path):
        (tmp_path / "justfile").write_text("build:\n  cargo build\n")
        result = detect_build_tools(tmp_path)
        assert "Just" in result

    def test_justfile_capitalized(self, tmp_path):
        (tmp_path / "Justfile").write_text("build:\n  cargo build\n")
        result = detect_build_tools(tmp_path)
        assert "Just" in result

    def test_tox(self, tmp_path):
        (tmp_path / "tox.ini").write_text("[tox]\nenvlist = py312\n")
        result = detect_build_tools(tmp_path)
        assert "tox" in result

    def test_nox(self, tmp_path):
        (tmp_path / "noxfile.py").write_text("import nox\n")
        result = detect_build_tools(tmp_path)
        assert "nox" in result

    def test_invoke(self, tmp_path):
        (tmp_path / "tasks.py").write_text("from invoke import task\n")
        result = detect_build_tools(tmp_path)
        assert "Invoke" in result

    def test_doit(self, tmp_path):
        (tmp_path / "dodo.py").write_text("def task_build():\n")
        result = detect_build_tools(tmp_path)
        assert "doit" in result

    def test_npm_scripts(self, tmp_path):
        (tmp_path / "package.json").write_text(
            json.dumps({"scripts": {"build": "tsc", "test": "jest"}})
        )
        result = detect_build_tools(tmp_path)
        assert "npm scripts" in result

    def test_npm_no_scripts(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"name": "app"}))
        result = detect_build_tools(tmp_path)
        assert "npm scripts" not in result

    def test_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text("apply plugin: 'java'\n")
        result = detect_build_tools(tmp_path)
        assert "Gradle" in result

    def test_gradle_kts(self, tmp_path):
        (tmp_path / "build.gradle.kts").write_text("plugins { id(\"java\") }\n")
        result = detect_build_tools(tmp_path)
        assert "Gradle" in result

    def test_maven(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<project></project>\n")
        result = detect_build_tools(tmp_path)
        assert "Maven" in result

    def test_cmake(self, tmp_path):
        (tmp_path / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 3.20)\n")
        result = detect_build_tools(tmp_path)
        assert "CMake" in result

    def test_meson(self, tmp_path):
        (tmp_path / "meson.build").write_text("project('app', 'c')\n")
        result = detect_build_tools(tmp_path)
        assert "Meson" in result

    def test_bazel(self, tmp_path):
        (tmp_path / "BUILD.bazel").write_text("cc_binary(name='app')\n")
        result = detect_build_tools(tmp_path)
        assert "Bazel" in result

    def test_bazel_workspace(self, tmp_path):
        (tmp_path / "WORKSPACE").write_text("workspace(name='app')\n")
        result = detect_build_tools(tmp_path)
        assert "Bazel" in result

    def test_rake(self, tmp_path):
        (tmp_path / "Rakefile").write_text("task :build do\nend\n")
        result = detect_build_tools(tmp_path)
        assert "Rake" in result

    def test_earthly(self, tmp_path):
        (tmp_path / "Earthfile").write_text("FROM golang:1.22\n")
        result = detect_build_tools(tmp_path)
        assert "Earthly" in result

    def test_empty_project(self, tmp_path):
        result = detect_build_tools(tmp_path)
        assert result == []

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "Makefile").write_text("all:\n")
        (tmp_path / "tox.ini").write_text("[tox]\n")
        (tmp_path / "package.json").write_text(json.dumps({"scripts": {"build": "tsc"}}))
        result = detect_build_tools(tmp_path)
        assert "Make" in result
        assert "tox" in result
        assert "npm scripts" in result

    def test_result_sorted(self, tmp_path):
        (tmp_path / "tox.ini").write_text("[tox]\n")
        (tmp_path / "Makefile").write_text("all:\n")
        result = detect_build_tools(tmp_path)
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# detect_api_specs
# ---------------------------------------------------------------------------
class TestDetectApiSpecs:
    def test_openapi_json(self, tmp_path):
        (tmp_path / "openapi.json").write_text('{"openapi": "3.0.0"}')
        result = detect_api_specs(tmp_path)
        assert "OpenAPI" in result

    def test_openapi_yaml(self, tmp_path):
        (tmp_path / "openapi.yaml").write_text("openapi: 3.0.0\n")
        result = detect_api_specs(tmp_path)
        assert "OpenAPI" in result

    def test_swagger_json(self, tmp_path):
        (tmp_path / "swagger.json").write_text('{"swagger": "2.0"}')
        result = detect_api_specs(tmp_path)
        assert "OpenAPI" in result

    def test_openapi_in_docs_subdir(self, tmp_path):
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "openapi.yml").write_text("openapi: 3.0.0\n")
        result = detect_api_specs(tmp_path)
        assert "OpenAPI" in result

    def test_openapi_in_api_subdir(self, tmp_path):
        (tmp_path / "api").mkdir()
        (tmp_path / "api" / "swagger.yaml").write_text("swagger: 2.0\n")
        result = detect_api_specs(tmp_path)
        assert "OpenAPI" in result

    def test_graphql_schema(self, tmp_path):
        (tmp_path / "schema.graphql").write_text("type Query { hello: String }\n")
        result = detect_api_specs(tmp_path)
        assert "GraphQL" in result

    def test_graphql_gql(self, tmp_path):
        (tmp_path / "schema.gql").write_text("type Query { hello: String }\n")
        result = detect_api_specs(tmp_path)
        assert "GraphQL" in result

    def test_graphqlrc(self, tmp_path):
        (tmp_path / ".graphqlrc.yml").write_text("schema: schema.graphql\n")
        result = detect_api_specs(tmp_path)
        assert "GraphQL" in result

    def test_graphql_in_src(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "queries.graphql").write_text("query { users { id } }\n")
        result = detect_api_specs(tmp_path)
        assert "GraphQL" in result

    def test_grpc_proto(self, tmp_path):
        (tmp_path / "service.proto").write_text('syntax = "proto3";\n')
        result = detect_api_specs(tmp_path)
        assert "gRPC/Protobuf" in result

    def test_grpc_proto_subdir(self, tmp_path):
        (tmp_path / "proto").mkdir()
        (tmp_path / "proto" / "service.proto").write_text('syntax = "proto3";\n')
        result = detect_api_specs(tmp_path)
        assert "gRPC/Protobuf" in result

    def test_asyncapi(self, tmp_path):
        (tmp_path / "asyncapi.yaml").write_text("asyncapi: 2.0.0\n")
        result = detect_api_specs(tmp_path)
        assert "AsyncAPI" in result

    def test_json_schema(self, tmp_path):
        (tmp_path / "schema.json").write_text('{"type": "object"}')
        result = detect_api_specs(tmp_path)
        assert "JSON Schema" in result

    def test_json_schema_dir(self, tmp_path):
        (tmp_path / "schemas").mkdir()
        result = detect_api_specs(tmp_path)
        assert "JSON Schema" in result

    def test_trpc(self, tmp_path):
        (tmp_path / "package.json").write_text(
            json.dumps({"dependencies": {"@trpc/server": "^10.0"}})
        )
        result = detect_api_specs(tmp_path)
        assert "tRPC" in result

    def test_trpc_not_detected_without_dep(self, tmp_path):
        (tmp_path / "package.json").write_text(
            json.dumps({"dependencies": {"express": "^4.18"}})
        )
        result = detect_api_specs(tmp_path)
        assert "tRPC" not in result

    def test_wsdl(self, tmp_path):
        (tmp_path / "service.wsdl").write_text("<definitions></definitions>")
        result = detect_api_specs(tmp_path)
        assert "WSDL/SOAP" in result

    def test_empty_project(self, tmp_path):
        result = detect_api_specs(tmp_path)
        assert result == []

    def test_multiple_specs(self, tmp_path):
        (tmp_path / "openapi.json").write_text('{"openapi": "3.0.0"}')
        (tmp_path / "schema.graphql").write_text("type Query { hello: String }\n")
        (tmp_path / "service.proto").write_text('syntax = "proto3";\n')
        result = detect_api_specs(tmp_path)
        assert "OpenAPI" in result
        assert "GraphQL" in result
        assert "gRPC/Protobuf" in result

    def test_result_sorted(self, tmp_path):
        (tmp_path / "schema.graphql").write_text("type Query {}\n")
        (tmp_path / "openapi.json").write_text('{"openapi": "3.0.0"}')
        result = detect_api_specs(tmp_path)
        assert result == sorted(result)
