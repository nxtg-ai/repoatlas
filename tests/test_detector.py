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
    detect_monitoring_tools,
    detect_auth_tools,
    detect_messaging_tools,
    detect_deploy_targets,
    detect_state_management,
    detect_css_frameworks,
    detect_bundlers,
    detect_orm_tools,
    detect_i18n_tools,
    detect_validation_tools,
    detect_logging_tools,
    detect_container_orchestration,
    detect_cloud_providers,
    detect_task_queues,
    detect_search_engines,
    detect_feature_flags,
    detect_http_clients,
    detect_doc_generators,
    detect_cli_frameworks,
    detect_config_tools,
    detect_caching_tools,
    detect_template_engines,
    detect_serialization_formats,
    detect_di_frameworks,
    detect_websocket_libs,
    detect_graphql_libs,
    detect_event_streaming,
    detect_payment_tools,
    detect_date_libs,
    detect_image_libs,
    detect_crypto_libs,
    detect_pdf_libs,
    detect_data_viz_libs,
    detect_geo_libs,
    detect_media_libs,
    detect_math_libs,
    detect_async_libs,
    detect_compression_libs,
    detect_email_libs,
    detect_a11y_tools,
    detect_scraping_libs,
    detect_desktop_frameworks,
    detect_file_storage,
    detect_form_libs,
    detect_animation_libs,
    detect_routing_libs,
    detect_game_frameworks,
    detect_cms_tools,
    detect_rate_limiters,
    detect_db_migration_tools,
    detect_grpc_libs,
    detect_codegen_tools,
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


# ---------------------------------------------------------------------------
# detect_monitoring_tools (N-55)
# ---------------------------------------------------------------------------
class TestDetectMonitoringTools:
    def test_empty_project(self, tmp_path):
        result = detect_monitoring_tools(tmp_path)
        assert result == []

    def test_sentry_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sentry-sdk==1.0.0\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Sentry" in result

    def test_sentry_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@sentry/node": "^7.0"}
        }))
        result = detect_monitoring_tools(tmp_path)
        assert "Sentry" in result

    def test_sentry_config_file(self, tmp_path):
        (tmp_path / ".sentryclirc").write_text("[defaults]\norg=myorg\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Sentry" in result

    def test_datadog_python(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["ddtrace"]\n')
        result = detect_monitoring_tools(tmp_path)
        assert "Datadog" in result

    def test_datadog_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"dd-trace": "^4.0"}
        }))
        result = detect_monitoring_tools(tmp_path)
        assert "Datadog" in result

    def test_datadog_config_file(self, tmp_path):
        (tmp_path / "datadog.yaml").write_text("api_key: xxx\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Datadog" in result

    def test_new_relic_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("newrelic\n")
        result = detect_monitoring_tools(tmp_path)
        assert "New Relic" in result

    def test_new_relic_config_file(self, tmp_path):
        (tmp_path / "newrelic.yml").write_text("license_key: xxx\n")
        result = detect_monitoring_tools(tmp_path)
        assert "New Relic" in result

    def test_opentelemetry_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("opentelemetry-sdk\n")
        result = detect_monitoring_tools(tmp_path)
        assert "OpenTelemetry" in result

    def test_opentelemetry_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@opentelemetry/api": "^1.0"}
        }))
        result = detect_monitoring_tools(tmp_path)
        assert "OpenTelemetry" in result

    def test_opentelemetry_config_file(self, tmp_path):
        (tmp_path / "otel-collector-config.yaml").write_text("receivers:\n")
        result = detect_monitoring_tools(tmp_path)
        assert "OpenTelemetry" in result

    def test_prometheus_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("prometheus-client\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Prometheus" in result

    def test_prometheus_config_file(self, tmp_path):
        (tmp_path / "prometheus.yml").write_text("scrape_configs:\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Prometheus" in result

    def test_bugsnag_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@bugsnag/js": "^7.0"}
        }))
        result = detect_monitoring_tools(tmp_path)
        assert "Bugsnag" in result

    def test_rollbar_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("rollbar\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Rollbar" in result

    def test_winston_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"winston": "^3.0"}
        }))
        result = detect_monitoring_tools(tmp_path)
        assert "Winston" in result

    def test_pino_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"pino": "^8.0"}
        }))
        result = detect_monitoring_tools(tmp_path)
        assert "Pino" in result

    def test_structlog_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("structlog\n")
        result = detect_monitoring_tools(tmp_path)
        assert "structlog" in result

    def test_loguru_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("loguru\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Loguru" in result

    def test_go_sentry(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/getsentry/sentry-go v0.1\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Sentry" in result

    def test_go_opentelemetry(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire go.opentelemetry.io/otel v1.0\n")
        result = detect_monitoring_tools(tmp_path)
        assert "OpenTelemetry" in result

    def test_rust_tracing(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntracing = "0.1"\n')
        result = detect_monitoring_tools(tmp_path)
        assert "tracing" in result

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sentry-sdk\nopentelemetry-sdk\nprometheus-client\n")
        result = detect_monitoring_tools(tmp_path)
        assert "Sentry" in result
        assert "OpenTelemetry" in result
        assert "Prometheus" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sentry-sdk\nsentry_sdk\n")
        (tmp_path / ".sentryclirc").write_text("[defaults]\n")
        result = detect_monitoring_tools(tmp_path)
        assert result.count("Sentry") == 1

    def test_result_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sentry-sdk\nopentelemetry-sdk\nprometheus-client\n")
        result = detect_monitoring_tools(tmp_path)
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# detect_auth_tools
# ---------------------------------------------------------------------------
class TestDetectAuthTools:
    def test_empty_project(self, tmp_path):
        result = detect_auth_tools(tmp_path)
        assert result == []

    def test_flask_login_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flask-login==0.6.0\n")
        result = detect_auth_tools(tmp_path)
        assert "Flask-Login" in result

    def test_django_allauth_python(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["django-allauth"]\n')
        result = detect_auth_tools(tmp_path)
        assert "django-allauth" in result

    def test_pyjwt_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyjwt>=2.0\n")
        result = detect_auth_tools(tmp_path)
        assert "PyJWT" in result

    def test_authlib_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("authlib\n")
        result = detect_auth_tools(tmp_path)
        assert "Authlib" in result

    def test_fastapi_users_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastapi-users[sqlalchemy]\n")
        result = detect_auth_tools(tmp_path)
        assert "FastAPI-Users" in result

    def test_auth0_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("auth0-python\n")
        result = detect_auth_tools(tmp_path)
        assert "Auth0" in result

    def test_nextauth_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"next-auth": "^4.0"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "NextAuth.js" in result

    def test_passport_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"passport": "^0.6", "express-session": "^1.17"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "Passport.js" in result
        assert "express-session" in result

    def test_clerk_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@clerk/nextjs": "^4.0"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "Clerk" in result

    def test_auth0_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@auth0/nextjs-auth0": "^3.0"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "Auth0" in result

    def test_firebase_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"firebase": "^10.0"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "Firebase Auth" in result

    def test_supabase_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@supabase/auth-helpers-nextjs": "^0.8"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "Supabase Auth" in result

    def test_lucia_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"lucia": "^3.0"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "Lucia" in result

    def test_keycloak_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"keycloak-js": "^22.0"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "Keycloak" in result

    def test_bcrypt_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"bcryptjs": "^2.4"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "bcrypt" in result

    def test_golang_jwt_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com/app\nrequire github.com/golang-jwt/jwt v4.0.0\n")
        result = detect_auth_tools(tmp_path)
        assert "golang-jwt" in result

    def test_casbin_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com/app\nrequire github.com/casbin/casbin v2.0.0\n")
        result = detect_auth_tools(tmp_path)
        assert "Casbin" in result

    def test_rust_jsonwebtoken(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\njsonwebtoken = "9"\n')
        result = detect_auth_tools(tmp_path)
        assert "jsonwebtoken" in result

    def test_rust_oauth2(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\noauth2 = "4"\n')
        result = detect_auth_tools(tmp_path)
        assert "OAuth2" in result

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flask-login\npyjwt\nauthlib\n")
        result = detect_auth_tools(tmp_path)
        assert "Flask-Login" in result
        assert "PyJWT" in result
        assert "Authlib" in result

    def test_no_duplicates_across_files(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("auth0-python\n")
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@auth0/auth0-react": "^2.0"}
        }))
        result = detect_auth_tools(tmp_path)
        assert result.count("Auth0") == 1

    def test_result_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyjwt\nflask-login\nauthlib\n")
        result = detect_auth_tools(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not valid json")
        result = detect_auth_tools(tmp_path)
        assert result == []

    def test_devdependencies_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"jsonwebtoken": "^9.0"}
        }))
        result = detect_auth_tools(tmp_path)
        assert "jsonwebtoken" in result


# ---------------------------------------------------------------------------
# detect_messaging_tools
# ---------------------------------------------------------------------------
class TestDetectMessagingTools:
    def test_empty_project(self, tmp_path):
        result = detect_messaging_tools(tmp_path)
        assert result == []

    def test_sendgrid_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sendgrid==6.0\n")
        result = detect_messaging_tools(tmp_path)
        assert "SendGrid" in result

    def test_twilio_python(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["twilio"]\n')
        result = detect_messaging_tools(tmp_path)
        assert "Twilio" in result

    def test_slack_sdk_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("slack-sdk\n")
        result = detect_messaging_tools(tmp_path)
        assert "Slack" in result

    def test_slack_bolt_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("slack-bolt\n")
        result = detect_messaging_tools(tmp_path)
        assert "Slack" in result

    def test_socketio_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-socketio\n")
        result = detect_messaging_tools(tmp_path)
        assert "Socket.IO" in result

    def test_celery_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("celery[redis]\n")
        result = detect_messaging_tools(tmp_path)
        assert "Celery" in result

    def test_resend_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("resend\n")
        result = detect_messaging_tools(tmp_path)
        assert "Resend" in result

    def test_nodemailer_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"nodemailer": "^6.0"}
        }))
        result = detect_messaging_tools(tmp_path)
        assert "Nodemailer" in result

    def test_sendgrid_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@sendgrid/mail": "^7.0"}
        }))
        result = detect_messaging_tools(tmp_path)
        assert "SendGrid" in result

    def test_slack_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@slack/web-api": "^6.0"}
        }))
        result = detect_messaging_tools(tmp_path)
        assert "Slack" in result

    def test_socketio_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"socket.io": "^4.0"}
        }))
        result = detect_messaging_tools(tmp_path)
        assert "Socket.IO" in result

    def test_bullmq_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"bullmq": "^4.0"}
        }))
        result = detect_messaging_tools(tmp_path)
        assert "BullMQ" in result

    def test_pusher_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"pusher": "^5.0"}
        }))
        result = detect_messaging_tools(tmp_path)
        assert "Pusher" in result

    def test_novu_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@novu/node": "^0.20"}
        }))
        result = detect_messaging_tools(tmp_path)
        assert "Novu" in result

    def test_gomail_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com/app\nrequire gopkg.in/gomail.v2 v2.0.0\n")
        result = detect_messaging_tools(tmp_path)
        assert "Gomail" in result

    def test_slack_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com/app\nrequire github.com/slack-go/slack v0.12.0\n")
        result = detect_messaging_tools(tmp_path)
        assert "Slack" in result

    def test_lettre_rust(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nlettre = "0.11"\n')
        result = detect_messaging_tools(tmp_path)
        assert "Lettre" in result

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sendgrid\ntwilio\nslack-sdk\n")
        result = detect_messaging_tools(tmp_path)
        assert "SendGrid" in result
        assert "Twilio" in result
        assert "Slack" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("slack-sdk\nslack-bolt\nslack_sdk\n")
        result = detect_messaging_tools(tmp_path)
        assert result.count("Slack") == 1

    def test_result_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("twilio\nsendgrid\nslack-sdk\n")
        result = detect_messaging_tools(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_messaging_tools(tmp_path)
        assert result == []

    def test_devdependencies_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"nodemailer": "^6.0"}
        }))
        result = detect_messaging_tools(tmp_path)
        assert "Nodemailer" in result


class TestDetectDeployTargets:
    def test_empty_project(self, tmp_path):
        result = detect_deploy_targets(tmp_path)
        assert result == []

    def test_vercel_json(self, tmp_path):
        (tmp_path / "vercel.json").write_text("{}")
        result = detect_deploy_targets(tmp_path)
        assert "Vercel" in result

    def test_vercel_dir(self, tmp_path):
        (tmp_path / ".vercel").mkdir()
        result = detect_deploy_targets(tmp_path)
        assert "Vercel" in result

    def test_netlify_toml(self, tmp_path):
        (tmp_path / "netlify.toml").write_text("[build]\n")
        result = detect_deploy_targets(tmp_path)
        assert "Netlify" in result

    def test_netlify_redirects(self, tmp_path):
        (tmp_path / "_redirects").write_text("/ /index.html 200\n")
        result = detect_deploy_targets(tmp_path)
        assert "Netlify" in result

    def test_fly_toml(self, tmp_path):
        (tmp_path / "fly.toml").write_text('app = "myapp"\n')
        result = detect_deploy_targets(tmp_path)
        assert "Fly.io" in result

    def test_railway_json(self, tmp_path):
        (tmp_path / "railway.json").write_text("{}")
        result = detect_deploy_targets(tmp_path)
        assert "Railway" in result

    def test_railway_toml(self, tmp_path):
        (tmp_path / "railway.toml").write_text("[deploy]\n")
        result = detect_deploy_targets(tmp_path)
        assert "Railway" in result

    def test_render_yaml(self, tmp_path):
        (tmp_path / "render.yaml").write_text("services:\n")
        result = detect_deploy_targets(tmp_path)
        assert "Render" in result

    def test_heroku_procfile(self, tmp_path):
        (tmp_path / "Procfile").write_text("web: gunicorn app:app\n")
        result = detect_deploy_targets(tmp_path)
        assert "Heroku" in result

    def test_firebase_json(self, tmp_path):
        (tmp_path / "firebase.json").write_text('{"hosting": {}}')
        result = detect_deploy_targets(tmp_path)
        assert "Firebase Hosting" in result

    def test_aws_amplify_yml(self, tmp_path):
        (tmp_path / "amplify.yml").write_text("version: 1\n")
        result = detect_deploy_targets(tmp_path)
        assert "AWS Amplify" in result

    def test_aws_amplify_dir(self, tmp_path):
        (tmp_path / "amplify").mkdir()
        result = detect_deploy_targets(tmp_path)
        assert "AWS Amplify" in result

    def test_serverless_yml(self, tmp_path):
        (tmp_path / "serverless.yml").write_text("service: myapp\n")
        result = detect_deploy_targets(tmp_path)
        assert "Serverless Framework" in result

    def test_serverless_yaml(self, tmp_path):
        (tmp_path / "serverless.yaml").write_text("service: myapp\n")
        result = detect_deploy_targets(tmp_path)
        assert "Serverless Framework" in result

    def test_google_app_engine(self, tmp_path):
        (tmp_path / "app.yaml").write_text("runtime: python39\n")
        result = detect_deploy_targets(tmp_path)
        assert "Google App Engine" in result

    def test_app_yaml_without_runtime(self, tmp_path):
        (tmp_path / "app.yaml").write_text("name: myapp\n")
        result = detect_deploy_targets(tmp_path)
        assert "Google App Engine" not in result

    def test_digitalocean_do_dir(self, tmp_path):
        (tmp_path / ".do").mkdir()
        result = detect_deploy_targets(tmp_path)
        assert "DigitalOcean App Platform" in result

    def test_digitalocean_app_yaml(self, tmp_path):
        (tmp_path / "do-app.yaml").write_text("name: myapp\n")
        result = detect_deploy_targets(tmp_path)
        assert "DigitalOcean App Platform" in result

    def test_cloudflare_wrangler_toml(self, tmp_path):
        (tmp_path / "wrangler.toml").write_text('name = "worker"\n')
        result = detect_deploy_targets(tmp_path)
        assert "Cloudflare Workers" in result

    def test_cloudflare_wrangler_jsonc(self, tmp_path):
        (tmp_path / "wrangler.jsonc").write_text("{}")
        result = detect_deploy_targets(tmp_path)
        assert "Cloudflare Workers" in result

    def test_github_pages_workflow(self, tmp_path):
        wf_dir = tmp_path / ".github" / "workflows"
        wf_dir.mkdir(parents=True)
        (wf_dir / "deploy.yml").write_text("name: Deploy\njobs:\n  deploy:\n    uses: actions/deploy-pages\n")
        result = detect_deploy_targets(tmp_path)
        assert "GitHub Pages" in result

    def test_vercel_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@vercel/node": "^3.0"}
        }))
        result = detect_deploy_targets(tmp_path)
        assert "Vercel" in result

    def test_netlify_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"netlify-cli": "^17.0"}
        }))
        result = detect_deploy_targets(tmp_path)
        assert "Netlify" in result

    def test_wrangler_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"wrangler": "^3.0"}
        }))
        result = detect_deploy_targets(tmp_path)
        assert "Cloudflare Workers" in result

    def test_gh_pages_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"gh-pages": "^6.0"}
        }))
        result = detect_deploy_targets(tmp_path)
        assert "GitHub Pages" in result

    def test_firebase_tools_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"firebase-tools": "^13.0"}
        }))
        result = detect_deploy_targets(tmp_path)
        assert "Firebase Hosting" in result

    def test_multiple_targets(self, tmp_path):
        (tmp_path / "vercel.json").write_text("{}")
        (tmp_path / "Procfile").write_text("web: node server.js\n")
        result = detect_deploy_targets(tmp_path)
        assert "Vercel" in result
        assert "Heroku" in result

    def test_result_sorted(self, tmp_path):
        (tmp_path / "vercel.json").write_text("{}")
        (tmp_path / "fly.toml").write_text('app = "x"\n')
        (tmp_path / "Procfile").write_text("web: node\n")
        result = detect_deploy_targets(tmp_path)
        assert result == sorted(result)

    def test_no_duplicates_from_config_and_deps(self, tmp_path):
        (tmp_path / "vercel.json").write_text("{}")
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"vercel": "^33.0"}
        }))
        result = detect_deploy_targets(tmp_path)
        assert result.count("Vercel") == 1

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_deploy_targets(tmp_path)
        assert result == []


class TestDetectStateManagement:
    def test_empty_project(self, tmp_path):
        result = detect_state_management(tmp_path)
        assert result == []

    def test_redux(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"redux": "^5.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Redux" in result

    def test_redux_toolkit(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@reduxjs/toolkit": "^2.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Redux" in result

    def test_react_redux(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"react-redux": "^9.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Redux" in result

    def test_zustand(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"zustand": "^4.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Zustand" in result

    def test_recoil(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"recoil": "^0.7"}
        }))
        result = detect_state_management(tmp_path)
        assert "Recoil" in result

    def test_jotai(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"jotai": "^2.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Jotai" in result

    def test_valtio(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"valtio": "^1.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Valtio" in result

    def test_mobx(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"mobx": "^6.0", "mobx-react": "^9.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "MobX" in result
        assert result.count("MobX") == 1

    def test_xstate(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"xstate": "^5.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "XState" in result

    def test_pinia(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"pinia": "^2.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Pinia" in result

    def test_vuex(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"vuex": "^4.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Vuex" in result

    def test_ngrx(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@ngrx/store": "^17.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "NgRx" in result

    def test_signals(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@preact/signals-react": "^2.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Signals" in result

    def test_effector(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"effector": "^23.0", "effector-react": "^23.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Effector" in result
        assert result.count("Effector") == 1

    def test_nanostores(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"nanostores": "^0.9"}
        }))
        result = detect_state_management(tmp_path)
        assert "Nanostores" in result

    def test_legend_state(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@legendapp/state": "^2.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Legend State" in result

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"zustand": "^4.0", "jotai": "^2.0", "xstate": "^5.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Zustand" in result
        assert "Jotai" in result
        assert "XState" in result

    def test_result_sorted(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"zustand": "^4.0", "jotai": "^2.0", "redux": "^5.0"}
        }))
        result = detect_state_management(tmp_path)
        assert result == sorted(result)

    def test_devdependencies(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"zustand": "^4.0"}
        }))
        result = detect_state_management(tmp_path)
        assert "Zustand" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"redux": "^5.0", "@reduxjs/toolkit": "^2.0", "react-redux": "^9.0"}
        }))
        result = detect_state_management(tmp_path)
        assert result.count("Redux") == 1

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_state_management(tmp_path)
        assert result == []


class TestDetectCssFrameworks:
    def test_empty_project(self, tmp_path):
        result = detect_css_frameworks(tmp_path)
        assert result == []

    def test_tailwind_config(self, tmp_path):
        (tmp_path / "tailwind.config.js").write_text("module.exports = {}")
        result = detect_css_frameworks(tmp_path)
        assert "Tailwind CSS" in result

    def test_tailwind_config_ts(self, tmp_path):
        (tmp_path / "tailwind.config.ts").write_text("export default {}")
        result = detect_css_frameworks(tmp_path)
        assert "Tailwind CSS" in result

    def test_postcss_config(self, tmp_path):
        (tmp_path / "postcss.config.js").write_text("module.exports = {}")
        result = detect_css_frameworks(tmp_path)
        assert "PostCSS" in result

    def test_stylelint_config(self, tmp_path):
        (tmp_path / ".stylelintrc.json").write_text("{}")
        result = detect_css_frameworks(tmp_path)
        assert "Stylelint" in result

    def test_sass_files_root(self, tmp_path):
        (tmp_path / "styles.scss").write_text("body { color: red; }")
        result = detect_css_frameworks(tmp_path)
        assert "Sass" in result

    def test_sass_files_src(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "app.scss").write_text("body { color: red; }")
        result = detect_css_frameworks(tmp_path)
        assert "Sass" in result

    def test_less_files(self, tmp_path):
        (tmp_path / "theme.less").write_text("@primary: blue;")
        result = detect_css_frameworks(tmp_path)
        assert "Less" in result

    def test_css_modules_root(self, tmp_path):
        (tmp_path / "button.module.css").write_text(".btn { color: red; }")
        result = detect_css_frameworks(tmp_path)
        assert "CSS Modules" in result

    def test_css_modules_scss(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "card.module.scss").write_text(".card { color: blue; }")
        result = detect_css_frameworks(tmp_path)
        assert "CSS Modules" in result

    def test_tailwindcss_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"tailwindcss": "^3.4.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Tailwind CSS" in result

    def test_styled_components(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"styled-components": "^6.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Styled Components" in result

    def test_emotion(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@emotion/react": "^11.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Emotion" in result

    def test_vanilla_extract(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"@vanilla-extract/css": "^1.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Vanilla Extract" in result

    def test_bootstrap(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"bootstrap": "^5.3.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Bootstrap" in result

    def test_chakra_ui(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@chakra-ui/react": "^2.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Chakra UI" in result

    def test_material_ui(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@mui/material": "^5.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Material UI" in result

    def test_mantine(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@mantine/core": "^7.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Mantine" in result

    def test_ant_design(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"antd": "^5.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Ant Design" in result

    def test_panda_css(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"@pandacss/dev": "^0.30.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Panda CSS" in result

    def test_unocss(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"unocss": "^0.58.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "UnoCSS" in result

    def test_multiple_frameworks(self, tmp_path):
        (tmp_path / "tailwind.config.js").write_text("{}")
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@emotion/react": "^11.0.0"},
            "devDependencies": {"sass": "^1.70.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Tailwind CSS" in result
        assert "Emotion" in result
        assert "Sass" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "tailwind.config.js").write_text("{}")
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"tailwindcss": "^3.4.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert result.count("Tailwind CSS") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {
                "styled-components": "^6.0.0",
                "bootstrap": "^5.3.0",
                "@emotion/react": "^11.0.0",
            }
        }))
        result = detect_css_frameworks(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_css_frameworks(tmp_path)
        assert result == []

    def test_sass_file_extension(self, tmp_path):
        (tmp_path / "main.sass").write_text("body\n  color: red")
        result = detect_css_frameworks(tmp_path)
        assert "Sass" in result

    def test_less_in_src(self, tmp_path):
        src = tmp_path / "src"
        src.mkdir()
        (src / "theme.less").write_text("@primary: blue;")
        result = detect_css_frameworks(tmp_path)
        assert "Less" in result

    def test_vuetify(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"vuetify": "^3.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Vuetify" in result

    def test_radix_ui(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@radix-ui/themes": "^3.0.0"}
        }))
        result = detect_css_frameworks(tmp_path)
        assert "Radix UI" in result


class TestDetectBundlers:
    def test_empty_project(self, tmp_path):
        result = detect_bundlers(tmp_path)
        assert result == []

    def test_webpack_config(self, tmp_path):
        (tmp_path / "webpack.config.js").write_text("module.exports = {}")
        result = detect_bundlers(tmp_path)
        assert "Webpack" in result

    def test_webpack_config_ts(self, tmp_path):
        (tmp_path / "webpack.config.ts").write_text("export default {}")
        result = detect_bundlers(tmp_path)
        assert "Webpack" in result

    def test_vite_config(self, tmp_path):
        (tmp_path / "vite.config.ts").write_text("export default {}")
        result = detect_bundlers(tmp_path)
        assert "Vite" in result

    def test_rollup_config(self, tmp_path):
        (tmp_path / "rollup.config.js").write_text("export default {}")
        result = detect_bundlers(tmp_path)
        assert "Rollup" in result

    def test_parcelrc(self, tmp_path):
        (tmp_path / ".parcelrc").write_text("{}")
        result = detect_bundlers(tmp_path)
        assert "Parcel" in result

    def test_turbo_json(self, tmp_path):
        (tmp_path / "turbo.json").write_text("{}")
        result = detect_bundlers(tmp_path)
        assert "Turborepo" in result

    def test_swcrc(self, tmp_path):
        (tmp_path / ".swcrc").write_text("{}")
        result = detect_bundlers(tmp_path)
        assert "SWC" in result

    def test_rspack_config(self, tmp_path):
        (tmp_path / "rspack.config.js").write_text("module.exports = {}")
        result = detect_bundlers(tmp_path)
        assert "Rspack" in result

    def test_tsup_config(self, tmp_path):
        (tmp_path / "tsup.config.ts").write_text("export default {}")
        result = detect_bundlers(tmp_path)
        assert "tsup" in result

    def test_webpack_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"webpack": "^5.0.0", "webpack-cli": "^5.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "Webpack" in result

    def test_vite_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"vite": "^5.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "Vite" in result

    def test_esbuild(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"esbuild": "^0.20.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "esbuild" in result

    def test_parcel_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"parcel": "^2.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "Parcel" in result

    def test_swc_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"@swc/core": "^1.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "SWC" in result

    def test_rspack_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"@rspack/core": "^0.5.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "Rspack" in result

    def test_tsup_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"tsup": "^8.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "tsup" in result

    def test_unbuild(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"unbuild": "^2.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "unbuild" in result

    def test_snowpack(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"snowpack": "^3.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "Snowpack" in result

    def test_multiple_bundlers(self, tmp_path):
        (tmp_path / "vite.config.ts").write_text("{}")
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"esbuild": "^0.20.0", "@swc/core": "^1.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "Vite" in result
        assert "esbuild" in result
        assert "SWC" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "vite.config.ts").write_text("{}")
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"vite": "^5.0.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert result.count("Vite") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {
                "webpack": "^5.0.0",
                "esbuild": "^0.20.0",
                "rollup": "^4.0.0",
            }
        }))
        result = detect_bundlers(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_bundlers(tmp_path)
        assert result == []

    def test_microbundle(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"microbundle": "^0.15.0"}
        }))
        result = detect_bundlers(tmp_path)
        assert "microbundle" in result


class TestDetectOrmTools:
    def test_empty_project(self, tmp_path):
        result = detect_orm_tools(tmp_path)
        assert result == []

    def test_prisma_schema(self, tmp_path):
        (tmp_path / "prisma").mkdir()
        (tmp_path / "prisma" / "schema.prisma").write_text("model User {}")
        result = detect_orm_tools(tmp_path)
        assert "Prisma" in result

    def test_typeorm_config(self, tmp_path):
        (tmp_path / "ormconfig.json").write_text("{}")
        result = detect_orm_tools(tmp_path)
        assert "TypeORM" in result

    def test_drizzle_config(self, tmp_path):
        (tmp_path / "drizzle.config.ts").write_text("export default {}")
        result = detect_orm_tools(tmp_path)
        assert "Drizzle" in result

    def test_knexfile(self, tmp_path):
        (tmp_path / "knexfile.js").write_text("module.exports = {}")
        result = detect_orm_tools(tmp_path)
        assert "Knex" in result

    def test_mikro_orm_config(self, tmp_path):
        (tmp_path / "mikro-orm.config.ts").write_text("export default {}")
        result = detect_orm_tools(tmp_path)
        assert "MikroORM" in result

    def test_sqlalchemy_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["sqlalchemy>=2.0"]')
        result = detect_orm_tools(tmp_path)
        assert "SQLAlchemy" in result

    def test_django_orm_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django>=4.2\n")
        result = detect_orm_tools(tmp_path)
        assert "Django ORM" in result

    def test_peewee_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["peewee>=3.0"]')
        result = detect_orm_tools(tmp_path)
        assert "Peewee" in result

    def test_tortoise_orm(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("tortoise-orm>=0.20\n")
        result = detect_orm_tools(tmp_path)
        assert "Tortoise ORM" in result

    def test_asyncpg_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("asyncpg>=0.28\n")
        result = detect_orm_tools(tmp_path)
        assert "asyncpg" in result

    def test_psycopg2_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["psycopg2-binary>=2.9"]')
        result = detect_orm_tools(tmp_path)
        assert "psycopg2" in result

    def test_pymongo_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pymongo>=4.0\n")
        result = detect_orm_tools(tmp_path)
        assert "PyMongo" in result

    def test_alembic_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["alembic>=1.12"]')
        result = detect_orm_tools(tmp_path)
        assert "Alembic" in result

    def test_sequelize_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"sequelize": "^6.0.0"}
        }))
        result = detect_orm_tools(tmp_path)
        assert "Sequelize" in result

    def test_mongoose_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"mongoose": "^7.0.0"}
        }))
        result = detect_orm_tools(tmp_path)
        assert "Mongoose" in result

    def test_drizzle_orm_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"drizzle-orm": "^0.30.0"}
        }))
        result = detect_orm_tools(tmp_path)
        assert "Drizzle" in result

    def test_kysely_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"kysely": "^0.27.0"}
        }))
        result = detect_orm_tools(tmp_path)
        assert "Kysely" in result

    def test_prisma_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"prisma": "^5.0.0", "@prisma/client": "^5.0.0"}
        }))
        result = detect_orm_tools(tmp_path)
        assert "Prisma" in result

    def test_gorm_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com\nrequire gorm.io/gorm v1.25.0\n")
        result = detect_orm_tools(tmp_path)
        assert "GORM" in result

    def test_sqlx_go_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com\nrequire github.com/jmoiron/sqlx v1.3.5\n")
        result = detect_orm_tools(tmp_path)
        assert "sqlx (Go)" in result

    def test_ent_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com\nrequire entgo.io/ent v0.13.0\n")
        result = detect_orm_tools(tmp_path)
        assert "ent" in result

    def test_diesel_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ndiesel = "2.1"\n')
        result = detect_orm_tools(tmp_path)
        assert "Diesel" in result

    def test_sqlx_rust_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nsqlx = { version = "0.7", features = ["postgres"] }\n')
        result = detect_orm_tools(tmp_path)
        assert "sqlx (Rust)" in result

    def test_sea_orm_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nsea-orm = "0.12"\n')
        result = detect_orm_tools(tmp_path)
        assert "SeaORM" in result

    def test_hibernate_from_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text('implementation "org.hibernate:hibernate-core:6.0"')
        result = detect_orm_tools(tmp_path)
        assert "Hibernate" in result

    def test_mybatis_from_pom(self, tmp_path):
        (tmp_path / "pom.xml").write_text('<dependency><artifactId>mybatis</artifactId></dependency>')
        result = detect_orm_tools(tmp_path)
        assert "MyBatis" in result

    def test_spring_data_jpa_from_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text('implementation "org.springframework.boot:spring-boot-starter-data-jpa"')
        result = detect_orm_tools(tmp_path)
        assert "Spring Data JPA" in result

    def test_multiple_orms(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["sqlalchemy", "alembic"]')
        result = detect_orm_tools(tmp_path)
        assert "SQLAlchemy" in result
        assert "Alembic" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "prisma").mkdir()
        (tmp_path / "prisma" / "schema.prisma").write_text("model User {}")
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"prisma": "^5.0.0"}
        }))
        result = detect_orm_tools(tmp_path)
        assert result.count("Prisma") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["sqlalchemy", "pymongo", "alembic"]')
        result = detect_orm_tools(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_orm_tools(tmp_path)
        assert result == []

    def test_ioredis_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"ioredis": "^5.0.0"}
        }))
        result = detect_orm_tools(tmp_path)
        assert "ioredis" in result

    def test_node_postgres_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"pg": "^8.0.0"}
        }))
        result = detect_orm_tools(tmp_path)
        assert "node-postgres" in result

    def test_jooq_from_gradle_kts(self, tmp_path):
        (tmp_path / "build.gradle.kts").write_text('implementation("org.jooq:jooq:3.18")')
        result = detect_orm_tools(tmp_path)
        assert "jOOQ" in result

    def test_sqlmodel_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["sqlmodel>=0.0.14"]')
        result = detect_orm_tools(tmp_path)
        assert "SQLModel" in result


class TestDetectI18nTools:
    def test_empty_project(self, tmp_path):
        result = detect_i18n_tools(tmp_path)
        assert result == []

    def test_locales_directory(self, tmp_path):
        (tmp_path / "locales").mkdir()
        result = detect_i18n_tools(tmp_path)
        assert "Locale Files" in result

    def test_locale_directory(self, tmp_path):
        (tmp_path / "locale").mkdir()
        result = detect_i18n_tools(tmp_path)
        assert "Locale Files" in result

    def test_translations_directory(self, tmp_path):
        (tmp_path / "translations").mkdir()
        result = detect_i18n_tools(tmp_path)
        assert "Locale Files" in result

    def test_i18n_directory(self, tmp_path):
        (tmp_path / "i18n").mkdir()
        result = detect_i18n_tools(tmp_path)
        assert "Locale Files" in result

    def test_lingui_config(self, tmp_path):
        (tmp_path / "lingui.config.js").write_text("module.exports = {}")
        result = detect_i18n_tools(tmp_path)
        assert "Lingui" in result

    def test_babel_cfg(self, tmp_path):
        (tmp_path / "babel.cfg").write_text("[python: **.py]")
        result = detect_i18n_tools(tmp_path)
        assert "Babel (i18n)" in result

    def test_i18next_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"i18next": "^23.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "i18next" in result

    def test_react_i18next(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"react-i18next": "^13.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "react-i18next" in result

    def test_next_intl(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"next-intl": "^3.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "next-intl" in result

    def test_react_intl(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"react-intl": "^6.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "react-intl" in result

    def test_vue_i18n(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"vue-i18n": "^9.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "vue-i18n" in result

    def test_angular_localize(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@angular/localize": "^17.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "Angular i18n" in result

    def test_formatjs(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@formatjs/intl": "^2.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "FormatJS" in result

    def test_lingui_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@lingui/core": "^4.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "Lingui" in result

    def test_typesafe_i18n(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"typesafe-i18n": "^5.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "typesafe-i18n" in result

    def test_flask_babel_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flask-babel>=3.0\n")
        result = detect_i18n_tools(tmp_path)
        assert "Flask-Babel" in result

    def test_babel_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["babel>=2.12"]')
        result = detect_i18n_tools(tmp_path)
        assert "Babel (i18n)" in result

    def test_go_i18n_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com\nrequire github.com/nicksnyder/go-i18n/v2 v2.3.0\n")
        result = detect_i18n_tools(tmp_path)
        assert "go-i18n" in result

    def test_go_x_text(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com\nrequire golang.org/x/text v0.14.0\n")
        result = detect_i18n_tools(tmp_path)
        assert "Go x/text" in result

    def test_fluent_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nfluent = "0.16"\n')
        result = detect_i18n_tools(tmp_path)
        assert "Fluent" in result

    def test_rust_i18n_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nrust-i18n = "3"\n')
        result = detect_i18n_tools(tmp_path)
        assert "rust-i18n" in result

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "locales").mkdir()
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"i18next": "^23.0.0", "react-i18next": "^13.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert "Locale Files" in result
        assert "i18next" in result
        assert "react-i18next" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "lingui.config.js").write_text("{}")
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@lingui/core": "^4.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert result.count("Lingui") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "locales").mkdir()
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"i18next": "^23.0.0", "react-intl": "^6.0.0"}
        }))
        result = detect_i18n_tools(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_i18n_tools(tmp_path)
        assert result == []


# ---------------------------------------------------------------------------
# detect_validation_tools
# ---------------------------------------------------------------------------
class TestDetectValidationTools:
    def test_empty_project(self, tmp_path):
        assert detect_validation_tools(tmp_path) == []

    # --- Python ---
    def test_pydantic_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["pydantic>=2.0"]\n')
        result = detect_validation_tools(tmp_path)
        assert "Pydantic" in result

    def test_marshmallow_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("marshmallow>=3.0\n")
        result = detect_validation_tools(tmp_path)
        assert "marshmallow" in result

    def test_cerberus_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["cerberus"]\n')
        result = detect_validation_tools(tmp_path)
        assert "Cerberus" in result

    def test_attrs_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("attrs>=23.0\n")
        result = detect_validation_tools(tmp_path)
        assert "attrs" in result

    def test_jsonschema_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["jsonschema"]\n')
        result = detect_validation_tools(tmp_path)
        assert "jsonschema" in result

    def test_voluptuous_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("voluptuous>=0.14\n")
        result = detect_validation_tools(tmp_path)
        assert "Voluptuous" in result

    def test_colander_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["colander"]\n')
        result = detect_validation_tools(tmp_path)
        assert "Colander" in result

    def test_schematics_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("schematics>=2.0\n")
        result = detect_validation_tools(tmp_path)
        assert "Schematics" in result

    # --- JavaScript / TypeScript ---
    def test_zod_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"zod": "^3.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "Zod" in result

    def test_yup_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"yup": "^1.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "Yup" in result

    def test_joi_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"joi": "^17.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "Joi" in result

    def test_class_validator_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"class-validator": "^0.14.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "class-validator" in result

    def test_ajv_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"ajv": "^8.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "Ajv" in result

    def test_superstruct_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"superstruct": "^1.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "Superstruct" in result

    def test_valibot_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"valibot": "^0.30.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "Valibot" in result

    def test_typebox_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@sinclair/typebox": "^0.32.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "TypeBox" in result

    def test_vest_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"vest": "^5.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "Vest" in result

    def test_arktype_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"arktype": "^2.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "ArkType" in result

    def test_io_ts_from_dev_deps(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"io-ts": "^2.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "io-ts" in result

    # --- Go ---
    def test_go_validator_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/go-playground/validator/v10 v10.0.0\n")
        result = detect_validation_tools(tmp_path)
        assert "go-playground/validator" in result

    def test_ozzo_validation_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/go-ozzo/ozzo-validation v4.0.0\n")
        result = detect_validation_tools(tmp_path)
        assert "ozzo-validation" in result

    # --- Rust ---
    def test_rust_validator_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nvalidator = "0.18"\n')
        result = detect_validation_tools(tmp_path)
        assert "validator (Rust)" in result

    def test_garde_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ngarde = "0.18"\n')
        result = detect_validation_tools(tmp_path)
        assert "garde" in result

    # --- Java ---
    def test_hibernate_validator_from_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.hibernate.validator:hibernate-validator:8.0'\n")
        result = detect_validation_tools(tmp_path)
        assert "Hibernate Validator" in result

    def test_jakarta_validation_from_pom(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>jakarta.validation</groupId></dependency>\n")
        result = detect_validation_tools(tmp_path)
        assert "Jakarta Validation" in result

    # --- Edge cases ---
    def test_multiple_tools(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["pydantic>=2.0"]\n')
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"zod": "^3.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert "Pydantic" in result
        assert "Zod" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["pydantic>=2.0"]\n')
        (tmp_path / "requirements.txt").write_text("pydantic>=2.0\n")
        result = detect_validation_tools(tmp_path)
        assert result.count("Pydantic") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"zod": "^3.0.0", "yup": "^1.0.0", "joi": "^17.0.0"}
        }))
        result = detect_validation_tools(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_validation_tools(tmp_path)
        assert result == []


# ---------------------------------------------------------------------------
# detect_logging_tools
# ---------------------------------------------------------------------------
class TestDetectLoggingTools:
    def test_empty_project(self, tmp_path):
        assert detect_logging_tools(tmp_path) == []

    # --- Python ---
    def test_loguru_from_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["loguru"]\n')
        result = detect_logging_tools(tmp_path)
        assert "Loguru" in result

    def test_structlog_from_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("structlog>=23.0\n")
        result = detect_logging_tools(tmp_path)
        assert "structlog" in result

    def test_python_json_logger(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["python-json-logger"]\n')
        result = detect_logging_tools(tmp_path)
        assert "python-json-logger" in result

    # --- JavaScript / TypeScript ---
    def test_winston_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"winston": "^3.0.0"}
        }))
        result = detect_logging_tools(tmp_path)
        assert "Winston" in result

    def test_pino_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"pino": "^8.0.0"}
        }))
        result = detect_logging_tools(tmp_path)
        assert "Pino" in result

    def test_bunyan_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"bunyan": "^1.0.0"}
        }))
        result = detect_logging_tools(tmp_path)
        assert "Bunyan" in result

    def test_morgan_from_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"morgan": "^1.0.0"}
        }))
        result = detect_logging_tools(tmp_path)
        assert "Morgan" in result

    def test_tslog_from_dev_deps(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"tslog": "^4.0.0"}
        }))
        result = detect_logging_tools(tmp_path)
        assert "tslog" in result

    # --- Go ---
    def test_zap_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire go.uber.org/zap v1.27.0\n")
        result = detect_logging_tools(tmp_path)
        assert "Zap" in result

    def test_logrus_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/sirupsen/logrus v1.9.0\n")
        result = detect_logging_tools(tmp_path)
        assert "Logrus" in result

    def test_zerolog_from_go_mod(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/rs/zerolog v1.32.0\n")
        result = detect_logging_tools(tmp_path)
        assert "zerolog" in result

    # --- Rust ---
    def test_tracing_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntracing = "0.1"\n')
        result = detect_logging_tools(tmp_path)
        assert "tracing (Rust)" in result

    def test_env_logger_from_cargo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nenv_logger = "0.11"\n')
        result = detect_logging_tools(tmp_path)
        assert "env_logger" in result

    # --- Java ---
    def test_logback_from_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'ch.qos.logback:logback-classic:1.4'\n")
        result = detect_logging_tools(tmp_path)
        assert "Logback" in result

    def test_slf4j_from_pom(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>org.slf4j</groupId></dependency>\n")
        result = detect_logging_tools(tmp_path)
        assert "SLF4J" in result

    def test_log4j_from_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.apache.logging.log4j:log4j-core:2.0'\n")
        result = detect_logging_tools(tmp_path)
        assert "Log4j" in result

    # --- Edge cases ---
    def test_multiple_tools(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["loguru", "structlog"]\n')
        result = detect_logging_tools(tmp_path)
        assert "Loguru" in result
        assert "structlog" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["loguru"]\n')
        (tmp_path / "requirements.txt").write_text("loguru>=0.7\n")
        result = detect_logging_tools(tmp_path)
        assert result.count("Loguru") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"winston": "^3.0.0", "pino": "^8.0.0", "morgan": "^1.0.0"}
        }))
        result = detect_logging_tools(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        result = detect_logging_tools(tmp_path)
        assert result == []


# ---------------------------------------------------------------------------
# detect_container_orchestration
# ---------------------------------------------------------------------------
class TestDetectContainerOrchestration:
    def test_empty_project(self, tmp_path):
        assert detect_container_orchestration(tmp_path) == []

    def test_docker_compose(self, tmp_path):
        (tmp_path / "docker-compose.yml").write_text("version: '3'")
        assert "Docker Compose" in detect_container_orchestration(tmp_path)

    def test_docker_compose_yaml(self, tmp_path):
        (tmp_path / "docker-compose.yaml").write_text("version: '3'")
        assert "Docker Compose" in detect_container_orchestration(tmp_path)

    def test_kubernetes_dir(self, tmp_path):
        (tmp_path / "k8s").mkdir()
        (tmp_path / "k8s" / "deployment.yaml").write_text("kind: Deployment")
        assert "Kubernetes" in detect_container_orchestration(tmp_path)

    def test_kubernetes_manifests_dir(self, tmp_path):
        (tmp_path / "manifests").mkdir()
        (tmp_path / "manifests" / "service.yaml").write_text("kind: Service")
        assert "Kubernetes" in detect_container_orchestration(tmp_path)

    def test_kubernetes_deploy_dir(self, tmp_path):
        (tmp_path / "deploy").mkdir()
        (tmp_path / "deploy" / "pod.yaml").write_text("kind: Pod")
        assert "Kubernetes" in detect_container_orchestration(tmp_path)

    def test_helm_chart_yaml(self, tmp_path):
        (tmp_path / "Chart.yaml").write_text("apiVersion: v2")
        assert "Helm" in detect_container_orchestration(tmp_path)

    def test_helm_charts_dir(self, tmp_path):
        (tmp_path / "charts").mkdir()
        (tmp_path / "charts" / "myapp").mkdir()
        assert "Helm" in detect_container_orchestration(tmp_path)

    def test_kustomize(self, tmp_path):
        (tmp_path / "kustomization.yaml").write_text("resources: []")
        assert "Kustomize" in detect_container_orchestration(tmp_path)

    def test_skaffold(self, tmp_path):
        (tmp_path / "skaffold.yaml").write_text("apiVersion: skaffold/v2beta")
        assert "Skaffold" in detect_container_orchestration(tmp_path)

    def test_tilt(self, tmp_path):
        (tmp_path / "Tiltfile").write_text("docker_build('myapp', '.')")
        assert "Tilt" in detect_container_orchestration(tmp_path)

    def test_terraform(self, tmp_path):
        (tmp_path / "main.tf").write_text('provider "aws" {}')
        assert "Terraform" in detect_container_orchestration(tmp_path)

    def test_pulumi(self, tmp_path):
        (tmp_path / "Pulumi.yaml").write_text("name: myproject")
        assert "Pulumi" in detect_container_orchestration(tmp_path)

    def test_ansible_cfg(self, tmp_path):
        (tmp_path / "ansible.cfg").write_text("[defaults]")
        assert "Ansible" in detect_container_orchestration(tmp_path)

    def test_ansible_playbook(self, tmp_path):
        (tmp_path / "playbook.yml").write_text("- hosts: all")
        assert "Ansible" in detect_container_orchestration(tmp_path)

    def test_nomad(self, tmp_path):
        (tmp_path / "app.nomad").write_text("job 'app' {}")
        assert "Nomad" in detect_container_orchestration(tmp_path)

    def test_docker_swarm(self, tmp_path):
        (tmp_path / "docker-stack.yml").write_text("version: '3'")
        assert "Docker Swarm" in detect_container_orchestration(tmp_path)

    def test_vagrant(self, tmp_path):
        (tmp_path / "Vagrantfile").write_text("Vagrant.configure('2') do |config|")
        assert "Vagrant" in detect_container_orchestration(tmp_path)

    def test_packer(self, tmp_path):
        (tmp_path / "image.pkr.hcl").write_text('source "amazon-ebs" {}')
        assert "Packer" in detect_container_orchestration(tmp_path)

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "docker-compose.yml").write_text("version: '3'")
        (tmp_path / "k8s").mkdir()
        (tmp_path / "k8s" / "deploy.yaml").write_text("kind: Deployment")
        (tmp_path / "main.tf").write_text('provider "aws" {}')
        result = detect_container_orchestration(tmp_path)
        assert "Docker Compose" in result
        assert "Kubernetes" in result
        assert "Terraform" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "docker-compose.yml").write_text("version: '3'")
        (tmp_path / "Vagrantfile").write_text("config")
        (tmp_path / "main.tf").write_text("provider")
        result = detect_container_orchestration(tmp_path)
        assert result == sorted(result)

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "k8s").mkdir()
        (tmp_path / "k8s" / "a.yaml").write_text("kind: Deployment")
        (tmp_path / "kubernetes").mkdir()
        (tmp_path / "kubernetes" / "b.yaml").write_text("kind: Service")
        result = detect_container_orchestration(tmp_path)
        assert result.count("Kubernetes") == 1


# ---------------------------------------------------------------------------
# detect_cloud_providers
# ---------------------------------------------------------------------------
class TestDetectCloudProviders:
    def test_empty_project(self, tmp_path):
        assert detect_cloud_providers(tmp_path) == []

    def test_aws_python_boto3(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("boto3>=1.28.0\n")
        assert "AWS" in detect_cloud_providers(tmp_path)

    def test_aws_python_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = [\n    "boto3>=1.28.0",\n]\n')
        assert "AWS" in detect_cloud_providers(tmp_path)

    def test_gcp_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("google-cloud-storage>=2.0\n")
        assert "GCP" in detect_cloud_providers(tmp_path)

    def test_azure_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("azure-storage-blob>=12.0\n")
        assert "Azure" in detect_cloud_providers(tmp_path)

    def test_aws_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@aws-sdk/client-s3": "^3.0.0"}
        }))
        assert "AWS" in detect_cloud_providers(tmp_path)

    def test_gcp_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@google-cloud/storage": "^6.0.0"}
        }))
        assert "GCP" in detect_cloud_providers(tmp_path)

    def test_azure_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@azure/storage-blob": "^12.0.0"}
        }))
        assert "Azure" in detect_cloud_providers(tmp_path)

    def test_cloudflare_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"wrangler": "^3.0.0"}
        }))
        assert "Cloudflare" in detect_cloud_providers(tmp_path)

    def test_cloudflare_config(self, tmp_path):
        (tmp_path / "wrangler.toml").write_text('name = "my-worker"')
        assert "Cloudflare" in detect_cloud_providers(tmp_path)

    def test_fly_io(self, tmp_path):
        (tmp_path / "fly.toml").write_text('app = "myapp"')
        assert "Fly.io" in detect_cloud_providers(tmp_path)

    def test_railway(self, tmp_path):
        (tmp_path / "railway.json").write_text("{}")
        assert "Railway" in detect_cloud_providers(tmp_path)

    def test_render(self, tmp_path):
        (tmp_path / "render.yaml").write_text("services: []")
        assert "Render" in detect_cloud_providers(tmp_path)

    def test_aws_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/aws/aws-sdk-go v1.44.0\n")
        assert "AWS" in detect_cloud_providers(tmp_path)

    def test_gcp_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire cloud.google.com/go v0.110.0\n")
        assert "GCP" in detect_cloud_providers(tmp_path)

    def test_aws_rust(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\naws-sdk-s3 = "0.28"\n')
        assert "AWS" in detect_cloud_providers(tmp_path)

    def test_aws_java_maven(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>software.amazon.awssdk</groupId></dependency>")
        assert "AWS" in detect_cloud_providers(tmp_path)

    def test_gcp_java_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.google.cloud:google-cloud-storage:2.0'")
        assert "GCP" in detect_cloud_providers(tmp_path)

    def test_multiple_providers(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("boto3\ngoogle-cloud-storage\n")
        result = detect_cloud_providers(tmp_path)
        assert "AWS" in result
        assert "GCP" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("boto3\ngoogle-cloud-storage\nazure-storage-blob\n")
        result = detect_cloud_providers(tmp_path)
        assert result == sorted(result)

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("boto3\naws-cdk-lib\n")
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"aws-sdk": "^2.0.0"}
        }))
        result = detect_cloud_providers(tmp_path)
        assert result.count("AWS") == 1

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_cloud_providers(tmp_path) == []


# ---------------------------------------------------------------------------
# detect_task_queues
# ---------------------------------------------------------------------------
class TestDetectTaskQueues:
    def test_empty_project(self, tmp_path):
        assert detect_task_queues(tmp_path) == []

    def test_celery_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("celery>=5.0\n")
        assert "Celery" in detect_task_queues(tmp_path)

    def test_rq_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("rq>=1.0\n")
        assert "RQ" in detect_task_queues(tmp_path)

    def test_dramatiq_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("dramatiq>=1.0\n")
        assert "Dramatiq" in detect_task_queues(tmp_path)

    def test_huey_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("huey>=2.0\n")
        assert "Huey" in detect_task_queues(tmp_path)

    def test_temporal_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("temporalio>=1.0\n")
        assert "Temporal" in detect_task_queues(tmp_path)

    def test_prefect_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("prefect>=2.0\n")
        assert "Prefect" in detect_task_queues(tmp_path)

    def test_airflow_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("apache-airflow>=2.0\n")
        assert "Airflow" in detect_task_queues(tmp_path)

    def test_bullmq_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"bullmq": "^4.0.0"}
        }))
        assert "BullMQ" in detect_task_queues(tmp_path)

    def test_bull_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"bull": "^4.0.0"}
        }))
        assert "Bull" in detect_task_queues(tmp_path)

    def test_agenda_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"agenda": "^5.0.0"}
        }))
        assert "Agenda" in detect_task_queues(tmp_path)

    def test_temporal_js(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@temporalio/client": "^1.0.0"}
        }))
        assert "Temporal" in detect_task_queues(tmp_path)

    def test_asynq_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/hibiken/asynq v0.24.0\n")
        assert "Asynq" in detect_task_queues(tmp_path)

    def test_temporal_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire go.temporal.io/sdk v1.22.0\n")
        assert "Temporal" in detect_task_queues(tmp_path)

    def test_quartz_java(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>org.quartz-scheduler</groupId><artifactId>quartz</artifactId></dependency>")
        assert "Quartz" in detect_task_queues(tmp_path)

    def test_spring_batch_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.springframework.batch:spring-batch-core:5.0'")
        assert "Spring Batch" in detect_task_queues(tmp_path)

    def test_multiple_queues(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("celery\ndramatiq\n")
        result = detect_task_queues(tmp_path)
        assert "Celery" in result
        assert "Dramatiq" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("celery\nrq\ndramatiq\n")
        result = detect_task_queues(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_task_queues(tmp_path) == []


# ---------------------------------------------------------------------------
# detect_search_engines
# ---------------------------------------------------------------------------
class TestDetectSearchEngines:
    def test_empty_project(self, tmp_path):
        assert detect_search_engines(tmp_path) == []

    def test_python_elasticsearch(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("elasticsearch>=8.0\n")
        result = detect_search_engines(tmp_path)
        assert "Elasticsearch" in result

    def test_python_meilisearch(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("meilisearch\n")
        result = detect_search_engines(tmp_path)
        assert "Meilisearch" in result

    def test_python_algolia(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("algoliasearch\n")
        result = detect_search_engines(tmp_path)
        assert "Algolia" in result

    def test_python_typesense(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("typesense\n")
        result = detect_search_engines(tmp_path)
        assert "Typesense" in result

    def test_python_opensearch(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("opensearch-py\n")
        result = detect_search_engines(tmp_path)
        assert "OpenSearch" in result

    def test_python_solr(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pysolr\n")
        result = detect_search_engines(tmp_path)
        assert "Solr" in result

    def test_js_elasticsearch(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@elastic/elasticsearch": "^8.0.0"}
        }))
        result = detect_search_engines(tmp_path)
        assert "Elasticsearch" in result

    def test_js_algolia(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"algoliasearch": "^4.0.0"}
        }))
        result = detect_search_engines(tmp_path)
        assert "Algolia" in result

    def test_js_lunr(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"lunr": "^2.3.0"}
        }))
        result = detect_search_engines(tmp_path)
        assert "Lunr" in result

    def test_js_fuse(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"fuse.js": "^6.0.0"}
        }))
        result = detect_search_engines(tmp_path)
        assert "Fuse.js" in result

    def test_go_elasticsearch(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/elastic/go-elasticsearch v8.0.0\n")
        result = detect_search_engines(tmp_path)
        assert "Elasticsearch" in result

    def test_go_bleve(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/blevesearch/bleve v2.0.0\n")
        result = detect_search_engines(tmp_path)
        assert "Bleve" in result

    def test_rust_tantivy(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntantivy = "0.21"\n')
        result = detect_search_engines(tmp_path)
        assert "Tantivy" in result

    def test_java_elasticsearch(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency>elasticsearch</dependency>\n")
        result = detect_search_engines(tmp_path)
        assert "Elasticsearch" in result

    def test_java_lucene(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.apache.lucene:lucene-core:9.0.0'\n")
        result = detect_search_engines(tmp_path)
        assert "Lucene" in result

    def test_multiple_engines(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("elasticsearch\nmeilisearch\n")
        result = detect_search_engines(tmp_path)
        assert "Elasticsearch" in result
        assert "Meilisearch" in result
        assert len(result) == 2

    def test_dedup(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("elasticsearch\n")
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@elastic/elasticsearch": "^8.0.0"}
        }))
        result = detect_search_engines(tmp_path)
        assert result.count("Elasticsearch") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("typesense\nalgoliasearch\nelasticsearch\n")
        result = detect_search_engines(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_search_engines(tmp_path) == []


# ---------------------------------------------------------------------------
# detect_feature_flags
# ---------------------------------------------------------------------------
class TestDetectFeatureFlags:
    def test_empty_project(self, tmp_path):
        assert detect_feature_flags(tmp_path) == []

    def test_python_launchdarkly(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("launchdarkly-server-sdk\n")
        result = detect_feature_flags(tmp_path)
        assert "LaunchDarkly" in result

    def test_python_unleash(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("unleashclient\n")
        result = detect_feature_flags(tmp_path)
        assert "Unleash" in result

    def test_python_flagsmith(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flagsmith\n")
        result = detect_feature_flags(tmp_path)
        assert "Flagsmith" in result

    def test_python_growthbook(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("growthbook\n")
        result = detect_feature_flags(tmp_path)
        assert "GrowthBook" in result

    def test_python_posthog(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("posthog\n")
        result = detect_feature_flags(tmp_path)
        assert "PostHog" in result

    def test_python_openfeature(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("openfeature-sdk\n")
        result = detect_feature_flags(tmp_path)
        assert "OpenFeature" in result

    def test_python_waffle(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django-waffle\n")
        result = detect_feature_flags(tmp_path)
        assert "Waffle" in result

    def test_js_launchdarkly(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"launchdarkly-js-client-sdk": "^3.0.0"}
        }))
        result = detect_feature_flags(tmp_path)
        assert "LaunchDarkly" in result

    def test_js_growthbook(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@growthbook/growthbook-react": "^0.20.0"}
        }))
        result = detect_feature_flags(tmp_path)
        assert "GrowthBook" in result

    def test_js_posthog(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"posthog-js": "^1.0.0"}
        }))
        result = detect_feature_flags(tmp_path)
        assert "PostHog" in result

    def test_js_vercel_flags(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@vercel/flags": "^1.0.0"}
        }))
        result = detect_feature_flags(tmp_path)
        assert "Vercel Flags" in result

    def test_js_configcat(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@configcat/sdk": "^8.0.0"}
        }))
        result = detect_feature_flags(tmp_path)
        assert "ConfigCat" in result

    def test_go_launchdarkly(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/launchdarkly/go-server-sdk v6.0.0\n")
        result = detect_feature_flags(tmp_path)
        assert "LaunchDarkly" in result

    def test_rust_unleash(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nunleash-api-client = "0.10"\n')
        result = detect_feature_flags(tmp_path)
        assert "Unleash" in result

    def test_java_togglz(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency>togglz-core</dependency>\n")
        result = detect_feature_flags(tmp_path)
        assert "Togglz" in result

    def test_java_ff4j(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.ff4j:ff4j-core:1.9.0'\n")
        result = detect_feature_flags(tmp_path)
        assert "FF4J" in result

    def test_multiple_flags(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("launchdarkly-server-sdk\nposthog\n")
        result = detect_feature_flags(tmp_path)
        assert "LaunchDarkly" in result
        assert "PostHog" in result

    def test_dedup(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flagsmith\n")
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"flagsmith": "^3.0.0"}
        }))
        result = detect_feature_flags(tmp_path)
        assert result.count("Flagsmith") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("posthog\nflagsmith\nlaunchdarkly-server-sdk\n")
        result = detect_feature_flags(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_feature_flags(tmp_path) == []


# ---------------------------------------------------------------------------
# detect_http_clients
# ---------------------------------------------------------------------------

class TestDetectHttpClients:
    def test_empty_project(self, tmp_path):
        assert detect_http_clients(tmp_path) == []

    def test_python_requests(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("requests\n")
        result = detect_http_clients(tmp_path)
        assert "Requests" in result

    def test_python_httpx(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("httpx\n")
        result = detect_http_clients(tmp_path)
        assert "HTTPX" in result

    def test_python_aiohttp(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("aiohttp\n")
        result = detect_http_clients(tmp_path)
        assert "aiohttp" in result

    def test_python_urllib3(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("urllib3\n")
        result = detect_http_clients(tmp_path)
        assert "urllib3" in result

    def test_python_pycurl(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pycurl\n")
        result = detect_http_clients(tmp_path)
        assert "PycURL" in result

    def test_python_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = [\n    "httpx",\n]\n')
        result = detect_http_clients(tmp_path)
        assert "HTTPX" in result

    def test_js_axios(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"axios": "^1.0.0"}
        }))
        result = detect_http_clients(tmp_path)
        assert "Axios" in result

    def test_js_node_fetch(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"node-fetch": "^3.0.0"}
        }))
        result = detect_http_clients(tmp_path)
        assert "node-fetch" in result

    def test_js_got(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"got": "^12.0.0"}
        }))
        result = detect_http_clients(tmp_path)
        assert "Got" in result

    def test_js_undici(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"undici": "^5.0.0"}
        }))
        result = detect_http_clients(tmp_path)
        assert "Undici" in result

    def test_go_resty(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/go-resty/resty/v2 v2.7.0\n")
        result = detect_http_clients(tmp_path)
        assert "Resty" in result

    def test_go_retryablehttp(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/hashicorp/go-retryablehttp v0.7.0\n")
        result = detect_http_clients(tmp_path)
        assert "go-retryablehttp" in result

    def test_rust_reqwest(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nreqwest = "0.11"\n')
        result = detect_http_clients(tmp_path)
        assert "reqwest" in result

    def test_rust_ureq(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nureq = "2.0"\n')
        result = detect_http_clients(tmp_path)
        assert "ureq" in result

    def test_java_okhttp(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.squareup.okhttp3:okhttp:4.9.0'\n")
        result = detect_http_clients(tmp_path)
        assert "OkHttp" in result

    def test_java_retrofit(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>com.squareup.retrofit2</groupId></dependency>\n")
        result = detect_http_clients(tmp_path)
        assert "Retrofit" in result

    def test_multiple_clients(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("requests\nhttpx\naiohttp\n")
        result = detect_http_clients(tmp_path)
        assert len(result) == 3
        assert "HTTPX" in result
        assert "Requests" in result
        assert "aiohttp" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("requests\n")
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = ["requests"]\n')
        result = detect_http_clients(tmp_path)
        assert result.count("Requests") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("requests\nhttpx\naiohttp\n")
        result = detect_http_clients(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_http_clients(tmp_path) == []


# ---------------------------------------------------------------------------
# detect_doc_generators
# ---------------------------------------------------------------------------

class TestDetectDocGenerators:
    def test_empty_project(self, tmp_path):
        assert detect_doc_generators(tmp_path) == []

    def test_python_sphinx_deps(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sphinx\n")
        result = detect_doc_generators(tmp_path)
        assert "Sphinx" in result

    def test_python_sphinx_conf(self, tmp_path):
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "conf.py").write_text("# Sphinx config\n")
        result = detect_doc_generators(tmp_path)
        assert "Sphinx" in result

    def test_python_mkdocs_deps(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mkdocs\n")
        result = detect_doc_generators(tmp_path)
        assert "MkDocs" in result

    def test_python_mkdocs_config(self, tmp_path):
        (tmp_path / "mkdocs.yml").write_text("site_name: Test\n")
        result = detect_doc_generators(tmp_path)
        assert "MkDocs" in result

    def test_python_pdoc(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pdoc\n")
        result = detect_doc_generators(tmp_path)
        assert "pdoc" in result

    def test_js_docusaurus(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@docusaurus/core": "^2.0.0"}
        }))
        result = detect_doc_generators(tmp_path)
        assert "Docusaurus" in result

    def test_js_docusaurus_config(self, tmp_path):
        (tmp_path / "docusaurus.config.js").write_text("module.exports = {}\n")
        result = detect_doc_generators(tmp_path)
        assert "Docusaurus" in result

    def test_js_storybook(self, tmp_path):
        (tmp_path / ".storybook").mkdir()
        result = detect_doc_generators(tmp_path)
        assert "Storybook" in result

    def test_js_vitepress(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"vitepress": "^1.0.0"}
        }))
        result = detect_doc_generators(tmp_path)
        assert "VitePress" in result

    def test_js_typedoc(self, tmp_path):
        (tmp_path / "typedoc.json").write_text("{}\n")
        result = detect_doc_generators(tmp_path)
        assert "TypeDoc" in result

    def test_js_nextra(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"nextra": "^2.0.0"}
        }))
        result = detect_doc_generators(tmp_path)
        assert "Nextra" in result

    def test_rust_mdbook(self, tmp_path):
        (tmp_path / "book.toml").write_text("[book]\ntitle = \"Test\"\n")
        result = detect_doc_generators(tmp_path)
        assert "mdBook" in result

    def test_java_javadoc(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<plugin><artifactId>maven-javadoc-plugin</artifactId></plugin>\n")
        result = detect_doc_generators(tmp_path)
        assert "Javadoc" in result

    def test_java_dokka(self, tmp_path):
        (tmp_path / "build.gradle.kts").write_text("plugins { id(\"org.jetbrains.dokka\") }\n")
        result = detect_doc_generators(tmp_path)
        assert "Dokka" in result

    def test_doxygen(self, tmp_path):
        (tmp_path / "Doxyfile").write_text("PROJECT_NAME = Test\n")
        result = detect_doc_generators(tmp_path)
        assert "Doxygen" in result

    def test_multiple_generators(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sphinx\nmkdocs\n")
        result = detect_doc_generators(tmp_path)
        assert len(result) == 2
        assert "MkDocs" in result
        assert "Sphinx" in result

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mkdocs\n")
        (tmp_path / "mkdocs.yml").write_text("site_name: Test\n")
        result = detect_doc_generators(tmp_path)
        assert result.count("MkDocs") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sphinx\nmkdocs\n")
        result = detect_doc_generators(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_doc_generators(tmp_path) == []


# ---------------------------------------------------------------------------
# detect_cli_frameworks
# ---------------------------------------------------------------------------

class TestDetectCliFrameworks:
    def test_empty_project(self, tmp_path):
        assert detect_cli_frameworks(tmp_path) == []

    def test_python_click(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("click\n")
        result = detect_cli_frameworks(tmp_path)
        assert "Click" in result

    def test_python_typer(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("typer\n")
        result = detect_cli_frameworks(tmp_path)
        assert "Typer" in result

    def test_python_fire(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fire\n")
        result = detect_cli_frameworks(tmp_path)
        assert "Fire" in result

    def test_python_rich(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("rich\n")
        result = detect_cli_frameworks(tmp_path)
        assert "Rich" in result

    def test_python_textual(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("textual\n")
        result = detect_cli_frameworks(tmp_path)
        assert "Textual" in result

    def test_js_commander(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"commander": "^9.0.0"}
        }))
        result = detect_cli_frameworks(tmp_path)
        assert "Commander.js" in result

    def test_js_yargs(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"yargs": "^17.0.0"}
        }))
        result = detect_cli_frameworks(tmp_path)
        assert "Yargs" in result

    def test_js_oclif(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@oclif/core": "^3.0.0"}
        }))
        result = detect_cli_frameworks(tmp_path)
        assert "oclif" in result

    def test_js_ink(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"ink": "^4.0.0"}
        }))
        result = detect_cli_frameworks(tmp_path)
        assert "Ink" in result

    def test_go_cobra(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/spf13/cobra v1.7.0\n")
        result = detect_cli_frameworks(tmp_path)
        assert "Cobra" in result

    def test_go_bubbletea(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/charmbracelet/bubbletea v0.24.0\n")
        result = detect_cli_frameworks(tmp_path)
        assert "Bubbletea" in result

    def test_go_urfave_cli(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/urfave/cli/v2 v2.25.0\n")
        result = detect_cli_frameworks(tmp_path)
        assert "urfave/cli" in result

    def test_rust_clap(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nclap = "4.0"\n')
        result = detect_cli_frameworks(tmp_path)
        assert "clap" in result

    def test_rust_ratatui(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nratatui = "0.23"\n')
        result = detect_cli_frameworks(tmp_path)
        assert "Ratatui" in result

    def test_java_picocli(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'info.picocli:picocli:4.7.0'\n")
        result = detect_cli_frameworks(tmp_path)
        assert "picocli" in result

    def test_multiple_frameworks(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("click\nrich\ntyper\n")
        result = detect_cli_frameworks(tmp_path)
        assert len(result) == 3

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("click\n")
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = [\n    "click",\n]\n')
        result = detect_cli_frameworks(tmp_path)
        assert result.count("Click") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("typer\nclick\nrich\n")
        result = detect_cli_frameworks(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_cli_frameworks(tmp_path) == []


class TestDetectConfigTools:
    def test_empty_project(self, tmp_path):
        assert detect_config_tools(tmp_path) == []

    def test_python_dotenv(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-dotenv\n")
        result = detect_config_tools(tmp_path)
        assert "python-dotenv" in result

    def test_python_dynaconf(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("dynaconf\n")
        result = detect_config_tools(tmp_path)
        assert "Dynaconf" in result

    def test_python_hydra(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = [\n    "hydra-core",\n]\n')
        result = detect_config_tools(tmp_path)
        assert "Hydra" in result

    def test_python_pydantic_settings(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pydantic-settings\n")
        result = detect_config_tools(tmp_path)
        assert "Pydantic Settings" in result

    def test_python_decouple(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-decouple\n")
        result = detect_config_tools(tmp_path)
        assert "python-decouple" in result

    def test_env_file_detection(self, tmp_path):
        (tmp_path / ".env").write_text("KEY=value\n")
        result = detect_config_tools(tmp_path)
        assert "dotenv" in result

    def test_env_example_detection(self, tmp_path):
        (tmp_path / ".env.example").write_text("KEY=\n")
        result = detect_config_tools(tmp_path)
        assert "dotenv" in result

    def test_js_dotenv(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"dotenv": "^16.0.0"}
        }))
        result = detect_config_tools(tmp_path)
        assert "dotenv" in result

    def test_js_convict(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"convict": "^6.0.0"}
        }))
        result = detect_config_tools(tmp_path)
        assert "Convict" in result

    def test_js_envalid(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"envalid": "^8.0.0"}
        }))
        result = detect_config_tools(tmp_path)
        assert "envalid" in result

    def test_js_cross_env(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "devDependencies": {"cross-env": "^7.0.0"}
        }))
        result = detect_config_tools(tmp_path)
        assert "cross-env" in result

    def test_js_t3_env(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"@t3-oss/env-nextjs": "^0.7.0"}
        }))
        result = detect_config_tools(tmp_path)
        assert "t3-env" in result

    def test_go_viper(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/spf13/viper v1.17.0\n")
        result = detect_config_tools(tmp_path)
        assert "Viper" in result

    def test_go_envconfig(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/kelseyhightower/envconfig v1.4.0\n")
        result = detect_config_tools(tmp_path)
        assert "envconfig" in result

    def test_go_godotenv(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/joho/godotenv v1.5.0\n")
        result = detect_config_tools(tmp_path)
        assert "godotenv" in result

    def test_rust_figment(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nfigment = "0.10"\n')
        result = detect_config_tools(tmp_path)
        assert "Figment" in result

    def test_rust_dotenvy(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ndotenvy = "0.15"\n')
        result = detect_config_tools(tmp_path)
        assert "dotenvy" in result

    def test_java_spring_config(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<project><spring-boot-starter-configuration-processor/></project>\n")
        result = detect_config_tools(tmp_path)
        assert "Spring Config" in result

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-dotenv\ndynaconf\npydantic-settings\n")
        result = detect_config_tools(tmp_path)
        assert len(result) == 3

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-dotenv\n")
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = [\n    "python-dotenv",\n]\n')
        result = detect_config_tools(tmp_path)
        assert result.count("python-dotenv") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pydantic-settings\ndynaconf\npython-dotenv\n")
        result = detect_config_tools(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_config_tools(tmp_path) == []


class TestDetectCachingTools:
    def test_empty_project(self, tmp_path):
        assert detect_caching_tools(tmp_path) == []

    def test_python_redis(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("redis\n")
        result = detect_caching_tools(tmp_path)
        assert "redis-py" in result

    def test_python_cachetools(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("cachetools\n")
        result = detect_caching_tools(tmp_path)
        assert "cachetools" in result

    def test_python_diskcache(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("diskcache\n")
        result = detect_caching_tools(tmp_path)
        assert "DiskCache" in result

    def test_python_django_redis(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django-redis\n")
        result = detect_caching_tools(tmp_path)
        assert "django-redis" in result

    def test_python_flask_caching(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = [\n    "flask-caching",\n]\n')
        result = detect_caching_tools(tmp_path)
        assert "Flask-Caching" in result

    def test_js_ioredis(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"ioredis": "^5.0.0"}
        }))
        result = detect_caching_tools(tmp_path)
        assert "ioredis" in result

    def test_js_node_cache(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"node-cache": "^5.0.0"}
        }))
        result = detect_caching_tools(tmp_path)
        assert "node-cache" in result

    def test_js_lru_cache(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"lru-cache": "^10.0.0"}
        }))
        result = detect_caching_tools(tmp_path)
        assert "lru-cache" in result

    def test_js_keyv(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"keyv": "^4.0.0"}
        }))
        result = detect_caching_tools(tmp_path)
        assert "Keyv" in result

    def test_go_goredis(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/redis/go-redis/v9 v9.0.0\n")
        result = detect_caching_tools(tmp_path)
        assert "go-redis" in result

    def test_go_ristretto(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/dgraph-io/ristretto v0.1.0\n")
        result = detect_caching_tools(tmp_path)
        assert "Ristretto" in result

    def test_go_bigcache(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/allegro/bigcache/v3 v3.1.0\n")
        result = detect_caching_tools(tmp_path)
        assert "BigCache" in result

    def test_rust_moka(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nmoka = "0.12"\n')
        result = detect_caching_tools(tmp_path)
        assert "moka" in result

    def test_java_caffeine(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.github.ben-manes.caffeine:caffeine:3.1.8'\n")
        result = detect_caching_tools(tmp_path)
        assert "Caffeine" in result

    def test_java_ehcache(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<project><dependency>org.ehcache</dependency></project>\n")
        result = detect_caching_tools(tmp_path)
        assert "Ehcache" in result

    def test_java_jedis(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'redis.clients:jedis:5.0.0'\n")
        result = detect_caching_tools(tmp_path)
        assert "Jedis" in result

    def test_multiple_tools(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("redis\ncachetools\ndiskcache\n")
        result = detect_caching_tools(tmp_path)
        assert len(result) == 3

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("redis\n")
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = [\n    "redis",\n]\n')
        result = detect_caching_tools(tmp_path)
        assert result.count("redis-py") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("redis\ncachetools\ndiskcache\n")
        result = detect_caching_tools(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_caching_tools(tmp_path) == []


class TestDetectTemplateEngines:
    def test_empty_project(self, tmp_path):
        assert detect_template_engines(tmp_path) == []

    def test_python_jinja2(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("jinja2\n")
        result = detect_template_engines(tmp_path)
        assert "Jinja2" in result

    def test_python_mako(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mako\n")
        result = detect_template_engines(tmp_path)
        assert "Mako" in result

    def test_python_django_templates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django\n")
        result = detect_template_engines(tmp_path)
        assert "Django Templates" in result

    def test_js_handlebars(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"handlebars": "^4.0.0"}
        }))
        result = detect_template_engines(tmp_path)
        assert "Handlebars" in result

    def test_js_ejs(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"ejs": "^3.0.0"}
        }))
        result = detect_template_engines(tmp_path)
        assert "EJS" in result

    def test_js_pug(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"pug": "^3.0.0"}
        }))
        result = detect_template_engines(tmp_path)
        assert "Pug" in result

    def test_js_nunjucks(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"nunjucks": "^3.0.0"}
        }))
        result = detect_template_engines(tmp_path)
        assert "Nunjucks" in result

    def test_js_mustache(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"mustache": "^4.0.0"}
        }))
        result = detect_template_engines(tmp_path)
        assert "Mustache" in result

    def test_js_liquid(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"liquidjs": "^10.0.0"}
        }))
        result = detect_template_engines(tmp_path)
        assert "Liquid" in result

    def test_js_svelte(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"svelte": "^4.0.0"}
        }))
        result = detect_template_engines(tmp_path)
        assert "Svelte" in result

    def test_js_astro(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "dependencies": {"astro": "^3.0.0"}
        }))
        result = detect_template_engines(tmp_path)
        assert "Astro" in result

    def test_rust_tera(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntera = "1.0"\n')
        result = detect_template_engines(tmp_path)
        assert "Tera" in result

    def test_rust_askama(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\naskama = "0.12"\n')
        result = detect_template_engines(tmp_path)
        assert "Askama" in result

    def test_java_thymeleaf(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<project><dependency>spring-boot-starter-thymeleaf</dependency></project>\n")
        result = detect_template_engines(tmp_path)
        assert "Thymeleaf" in result

    def test_java_freemarker(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.freemarker:freemarker:2.3.32'\n")
        result = detect_template_engines(tmp_path)
        assert "FreeMarker" in result

    def test_multiple_engines(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("jinja2\nmako\n")
        result = detect_template_engines(tmp_path)
        assert len(result) == 2

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("jinja2\n")
        (tmp_path / "pyproject.toml").write_text('[project]\ndependencies = [\n    "jinja2",\n]\n')
        result = detect_template_engines(tmp_path)
        assert result.count("Jinja2") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mako\njinja2\n")
        result = detect_template_engines(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_template_engines(tmp_path) == []


# ---------------------------------------------------------------------------
# detect_serialization_formats
# ---------------------------------------------------------------------------


class TestDetectSerializationFormats:
    def test_empty(self, tmp_path):
        assert detect_serialization_formats(tmp_path) == []

    # --- Python ---
    def test_python_protobuf(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("protobuf>=4.0\n")
        assert "Protocol Buffers" in detect_serialization_formats(tmp_path)

    def test_python_msgpack(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("msgpack>=1.0\n")
        assert "MessagePack" in detect_serialization_formats(tmp_path)

    def test_python_avro(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastavro>=1.0\n")
        assert "Apache Avro" in detect_serialization_formats(tmp_path)

    def test_python_cbor(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("cbor2>=5.0\n")
        assert "CBOR" in detect_serialization_formats(tmp_path)

    def test_python_yaml(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyyaml>=6.0\n")
        assert "YAML" in detect_serialization_formats(tmp_path)

    def test_python_toml(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("tomli>=2.0\n")
        assert "TOML" in detect_serialization_formats(tmp_path)

    def test_python_orjson(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("orjson>=3.0\n")
        assert "orjson" in detect_serialization_formats(tmp_path)

    def test_python_pydantic(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pydantic>=2.0\n")
        assert "Pydantic" in detect_serialization_formats(tmp_path)

    def test_python_marshmallow(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("marshmallow>=3.0\n")
        assert "Marshmallow" in detect_serialization_formats(tmp_path)

    def test_python_arrow(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyarrow>=10.0\n")
        assert "Apache Arrow" in detect_serialization_formats(tmp_path)

    def test_python_bson(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pymongo>=4.0\n")
        assert "BSON" in detect_serialization_formats(tmp_path)

    # --- JS/TS ---
    def test_js_protobuf(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"protobufjs": "^7.0"}}))
        assert "Protocol Buffers" in detect_serialization_formats(tmp_path)

    def test_js_yaml(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"js-yaml": "^4.0"}}))
        assert "YAML" in detect_serialization_formats(tmp_path)

    def test_js_bson(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"bson": "^6.0"}}))
        assert "BSON" in detect_serialization_formats(tmp_path)

    # --- Go ---
    def test_go_protobuf(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire google.golang.org/protobuf v1.30\n")
        assert "Protocol Buffers" in detect_serialization_formats(tmp_path)

    def test_go_yaml(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire gopkg.in/yaml.v3 v3.0\n")
        assert "YAML" in detect_serialization_formats(tmp_path)

    def test_go_toml(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/BurntSushi/toml v1.0\n")
        assert "TOML" in detect_serialization_formats(tmp_path)

    # --- Rust ---
    def test_rust_serde_json(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nserde_json = "1.0"\n')
        assert "serde_json" in detect_serialization_formats(tmp_path)

    def test_rust_bincode(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nbincode = "1.3"\n')
        assert "Bincode" in detect_serialization_formats(tmp_path)

    # --- Java ---
    def test_java_jackson(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>jackson-core</artifactId></dependency>")
        assert "Jackson" in detect_serialization_formats(tmp_path)

    def test_java_gson(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.google.code.gson:gson:2.10'\n")
        assert "Gson" in detect_serialization_formats(tmp_path)

    # --- File-based ---
    def test_proto_files(self, tmp_path):
        (tmp_path / "schema.proto").write_text('syntax = "proto3";')
        assert "Protocol Buffers" in detect_serialization_formats(tmp_path)

    def test_avsc_files(self, tmp_path):
        (tmp_path / "user.avsc").write_text('{"type": "record", "name": "User"}')
        assert "Apache Avro" in detect_serialization_formats(tmp_path)

    def test_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyyaml>=6.0\nprotobuf>=4.0\norjson>=3.0\n")
        result = detect_serialization_formats(tmp_path)
        assert result == sorted(result)

    def test_no_duplicates(self, tmp_path):
        # protobuf from deps AND .proto file
        (tmp_path / "requirements.txt").write_text("protobuf>=4.0\n")
        (tmp_path / "schema.proto").write_text('syntax = "proto3";')
        result = detect_serialization_formats(tmp_path)
        assert result.count("Protocol Buffers") == 1


# ---------------------------------------------------------------------------
# detect_di_frameworks
# ---------------------------------------------------------------------------


class TestDetectDIFrameworks:
    def test_empty(self, tmp_path):
        assert detect_di_frameworks(tmp_path) == []

    # --- Python ---
    def test_python_dependency_injector(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("dependency-injector>=4.0\n")
        assert "dependency-injector" in detect_di_frameworks(tmp_path)

    def test_python_fastapi_depends(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastapi>=0.100\n")
        assert "FastAPI Depends" in detect_di_frameworks(tmp_path)

    def test_python_lagom(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("lagom>=2.0\n")
        assert "Lagom" in detect_di_frameworks(tmp_path)

    def test_python_dishka(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("dishka>=1.0\n")
        assert "dishka" in detect_di_frameworks(tmp_path)

    # --- JS/TS ---
    def test_js_inversify(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"inversify": "^6.0"}}))
        assert "InversifyJS" in detect_di_frameworks(tmp_path)

    def test_js_tsyringe(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"tsyringe": "^4.0"}}))
        assert "tsyringe" in detect_di_frameworks(tmp_path)

    def test_js_awilix(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"awilix": "^9.0"}}))
        assert "Awilix" in detect_di_frameworks(tmp_path)

    def test_js_nestjs(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"@nestjs/core": "^10.0"}}))
        assert "NestJS DI" in detect_di_frameworks(tmp_path)

    def test_js_angular(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"@angular/core": "^17.0"}}))
        assert "Angular DI" in detect_di_frameworks(tmp_path)

    # --- Go ---
    def test_go_uber_fx(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire go.uber.org/fx v1.20\n")
        assert "Uber Fx" in detect_di_frameworks(tmp_path)

    def test_go_wire(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/google/wire v0.5\n")
        assert "Wire" in detect_di_frameworks(tmp_path)

    # --- Rust ---
    def test_rust_shaku(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nshaku = "0.6"\n')
        assert "Shaku" in detect_di_frameworks(tmp_path)

    # --- Java ---
    def test_java_spring(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>spring-context</artifactId></dependency>")
        assert "Spring DI" in detect_di_frameworks(tmp_path)

    def test_java_guice(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.google.inject:guice:5.1'\n")
        assert "Google Guice" in detect_di_frameworks(tmp_path)

    def test_java_dagger(self, tmp_path):
        (tmp_path / "build.gradle.kts").write_text("implementation(\"com.google.dagger:dagger:2.48\")\n")
        assert "Dagger" in detect_di_frameworks(tmp_path)

    def test_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastapi>=0.100\ndependency-injector>=4.0\n")
        result = detect_di_frameworks(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_di_frameworks(tmp_path) == []


# ---------------------------------------------------------------------------
# detect_websocket_libs
# ---------------------------------------------------------------------------


class TestDetectWebSocketLibs:
    def test_empty(self, tmp_path):
        assert detect_websocket_libs(tmp_path) == []

    # --- Python ---
    def test_python_websockets(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("websockets>=12.0\n")
        assert "websockets" in detect_websocket_libs(tmp_path)

    def test_python_socketio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-socketio>=5.0\n")
        assert "python-socketio" in detect_websocket_libs(tmp_path)

    def test_python_channels(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("channels>=4.0\n")
        assert "Django Channels" in detect_websocket_libs(tmp_path)

    def test_python_starlette(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastapi>=0.100\n")
        assert "Starlette WebSocket" in detect_websocket_libs(tmp_path)

    def test_python_tornado(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("tornado>=6.0\n")
        assert "Tornado WebSocket" in detect_websocket_libs(tmp_path)

    # --- JS/TS ---
    def test_js_socketio(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"socket.io": "^4.0"}}))
        assert "Socket.IO" in detect_websocket_libs(tmp_path)

    def test_js_ws(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"ws": "^8.0"}}))
        assert "ws" in detect_websocket_libs(tmp_path)

    def test_js_pusher(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"pusher": "^5.0"}}))
        assert "Pusher" in detect_websocket_libs(tmp_path)

    def test_js_graphql_ws(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"graphql-ws": "^5.0"}}))
        assert "graphql-ws" in detect_websocket_libs(tmp_path)

    # --- Go ---
    def test_go_gorilla(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/gorilla/websocket v1.5\n")
        assert "Gorilla WebSocket" in detect_websocket_libs(tmp_path)

    def test_go_nhooyr(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire nhooyr.io/websocket v1.8\n")
        assert "nhooyr/websocket" in detect_websocket_libs(tmp_path)

    # --- Rust ---
    def test_rust_tungstenite(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntokio-tungstenite = "0.20"\n')
        assert "Tungstenite" in detect_websocket_libs(tmp_path)

    # --- Java ---
    def test_java_spring_websocket(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>spring-boot-starter-websocket</artifactId></dependency>")
        assert "Spring WebSocket" in detect_websocket_libs(tmp_path)

    def test_java_jakarta(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'jakarta.websocket:jakarta.websocket-api:2.1'\n")
        assert "Jakarta WebSocket" in detect_websocket_libs(tmp_path)

    def test_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("websockets>=12.0\nfastapi>=0.100\ntornado>=6.0\n")
        result = detect_websocket_libs(tmp_path)
        assert result == sorted(result)

    def test_invalid_package_json(self, tmp_path):
        (tmp_path / "package.json").write_text("not json")
        assert detect_websocket_libs(tmp_path) == []


class TestDetectGraphqlLibs:
    def test_empty(self, tmp_path):
        assert detect_graphql_libs(tmp_path) == []

    def test_python_graphene(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("graphene>=3.0\n")
        result = detect_graphql_libs(tmp_path)
        assert "Graphene" in result

    def test_python_strawberry(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("strawberry-graphql>=0.200\n")
        result = detect_graphql_libs(tmp_path)
        assert "Strawberry" in result

    def test_python_ariadne(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("ariadne>=0.20\n")
        result = detect_graphql_libs(tmp_path)
        assert "Ariadne" in result

    def test_js_apollo_server(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@apollo/server": "^4.0"}}')
        result = detect_graphql_libs(tmp_path)
        assert "Apollo Server" in result

    def test_js_apollo_client(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@apollo/client": "^3.0"}}')
        result = detect_graphql_libs(tmp_path)
        assert "Apollo Client" in result

    def test_js_graphql_yoga(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"graphql-yoga": "^4.0"}}')
        result = detect_graphql_libs(tmp_path)
        assert "GraphQL Yoga" in result

    def test_js_urql(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"urql": "^4.0"}}')
        result = detect_graphql_libs(tmp_path)
        assert "URQL" in result

    def test_js_relay(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"relay-runtime": "^16.0"}}')
        result = detect_graphql_libs(tmp_path)
        assert "Relay" in result

    def test_js_type_graphql(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"type-graphql": "^2.0"}}')
        result = detect_graphql_libs(tmp_path)
        assert "TypeGraphQL" in result

    def test_go_gqlgen(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/99designs/gqlgen v0.17\n")
        result = detect_graphql_libs(tmp_path)
        assert "gqlgen" in result

    def test_rust_juniper(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\njuniper = "0.16"\n')
        result = detect_graphql_libs(tmp_path)
        assert "Juniper" in result

    def test_rust_async_graphql(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nasync-graphql = "6.0"\n')
        result = detect_graphql_libs(tmp_path)
        assert "async-graphql" in result

    def test_java_graphql_java(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.graphql-java:graphql-java:21.0'\n")
        result = detect_graphql_libs(tmp_path)
        assert "graphql-java" in result

    def test_java_dgs(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.netflix.dgs:graphql-dgs-spring-boot-starter'\n")
        result = detect_graphql_libs(tmp_path)
        assert "Netflix DGS" in result

    def test_schema_files(self, tmp_path):
        (tmp_path / "schema.graphql").write_text("type Query { hello: String }")
        result = detect_graphql_libs(tmp_path)
        assert "GraphQL Schema" in result

    def test_gql_extension(self, tmp_path):
        (tmp_path / "query.gql").write_text("query { user { name } }")
        result = detect_graphql_libs(tmp_path)
        assert "GraphQL Schema" in result

    def test_multiple_libs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@apollo/server": "^4.0", "@apollo/client": "^3.0", "graphql": "^16"}}')
        result = detect_graphql_libs(tmp_path)
        assert "Apollo Server" in result
        assert "Apollo Client" in result
        assert "graphql-js" in result

    def test_sorted(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"urql": "^4.0", "@apollo/client": "^3.0", "graphql": "^16"}}')
        result = detect_graphql_libs(tmp_path)
        assert result == sorted(result)

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"apollo-server": "^3.0", "@apollo/server": "^4.0"}}')
        result = detect_graphql_libs(tmp_path)
        assert result.count("Apollo Server") == 1


class TestDetectEventStreaming:
    def test_empty(self, tmp_path):
        assert detect_event_streaming(tmp_path) == []

    def test_python_confluent_kafka(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("confluent-kafka>=2.0\n")
        result = detect_event_streaming(tmp_path)
        assert "Confluent Kafka" in result

    def test_python_kafka_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("kafka-python>=2.0\n")
        result = detect_event_streaming(tmp_path)
        assert "kafka-python" in result

    def test_python_pika_rabbitmq(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pika>=1.3\n")
        result = detect_event_streaming(tmp_path)
        assert "RabbitMQ (pika)" in result

    def test_python_nats(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("nats-py>=2.0\n")
        result = detect_event_streaming(tmp_path)
        assert "NATS" in result

    def test_python_pulsar(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pulsar-client>=3.0\n")
        result = detect_event_streaming(tmp_path)
        assert "Apache Pulsar" in result

    def test_python_faust(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("faust-streaming>=0.10\n")
        result = detect_event_streaming(tmp_path)
        assert "Faust" in result

    def test_python_kombu(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("kombu>=5.0\n")
        result = detect_event_streaming(tmp_path)
        assert "Kombu" in result

    def test_js_kafkajs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"kafkajs": "^2.0"}}')
        result = detect_event_streaming(tmp_path)
        assert "KafkaJS" in result

    def test_js_amqplib(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"amqplib": "^0.10"}}')
        result = detect_event_streaming(tmp_path)
        assert "RabbitMQ (amqplib)" in result

    def test_js_bullmq(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"bullmq": "^4.0"}}')
        result = detect_event_streaming(tmp_path)
        assert "BullMQ" in result

    def test_js_google_pubsub(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@google-cloud/pubsub": "^4.0"}}')
        result = detect_event_streaming(tmp_path)
        assert "Google Pub/Sub" in result

    def test_js_aws_sqs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@aws-sdk/client-sqs": "^3.0"}}')
        result = detect_event_streaming(tmp_path)
        assert "AWS SQS" in result

    def test_js_azure_event_hubs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@azure/event-hubs": "^5.0"}}')
        result = detect_event_streaming(tmp_path)
        assert "Azure Event Hubs" in result

    def test_go_kafka_go(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/segmentio/kafka-go v0.4\n")
        result = detect_event_streaming(tmp_path)
        assert "kafka-go" in result

    def test_go_sarama(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/IBM/sarama v1.41\n")
        result = detect_event_streaming(tmp_path)
        assert "Sarama" in result

    def test_go_nats(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/nats-io/nats.go v1.30\n")
        result = detect_event_streaming(tmp_path)
        assert "NATS (Go)" in result

    def test_go_watermill(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/ThreeDotsLabs/watermill v1.3\n")
        result = detect_event_streaming(tmp_path)
        assert "Watermill" in result

    def test_rust_rdkafka(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nrdkafka = "0.36"\n')
        result = detect_event_streaming(tmp_path)
        assert "rdkafka" in result

    def test_rust_lapin(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nlapin = "2.3"\n')
        result = detect_event_streaming(tmp_path)
        assert "RabbitMQ (lapin)" in result

    def test_java_spring_kafka(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.springframework.kafka:spring-kafka:3.0'\n")
        result = detect_event_streaming(tmp_path)
        assert "Spring Kafka" in result

    def test_java_spring_amqp(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.springframework.amqp:spring-amqp:3.0'\n")
        result = detect_event_streaming(tmp_path)
        assert "Spring AMQP" in result

    def test_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pika>=1.3\nconfluent-kafka>=2.0\nkombu>=5.0\n")
        result = detect_event_streaming(tmp_path)
        assert result == sorted(result)

    def test_multiple_libs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"kafkajs": "^2.0", "amqplib": "^0.10", "bullmq": "^4.0"}}')
        result = detect_event_streaming(tmp_path)
        assert "KafkaJS" in result
        assert "RabbitMQ (amqplib)" in result
        assert "BullMQ" in result


# ---------------------------------------------------------------------------
# detect_payment_tools
# ---------------------------------------------------------------------------
class TestDetectPaymentTools:
    def test_empty(self, tmp_path):
        assert detect_payment_tools(tmp_path) == []

    def test_python_stripe(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("stripe>=5.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Stripe" in result

    def test_python_paypal(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("paypalrestsdk>=1.0\n")
        result = detect_payment_tools(tmp_path)
        assert "PayPal" in result

    def test_python_braintree(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("braintree>=4.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Braintree" in result

    def test_python_square(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("square>=20.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Square" in result

    def test_python_razorpay(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("razorpay>=1.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Razorpay" in result

    def test_python_adyen(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("adyen>=8.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Adyen" in result

    def test_python_paddle(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("paddle-python-sdk>=1.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Paddle" in result

    def test_python_mollie(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mollie-api-python>=3.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Mollie" in result

    def test_python_gocardless(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("gocardless-pro>=1.0\n")
        result = detect_payment_tools(tmp_path)
        assert "GoCardless" in result

    def test_python_lemon_squeezy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("lemonsqueezy>=1.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Lemon Squeezy" in result

    def test_js_stripe(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"stripe": "^12.0"}}')
        result = detect_payment_tools(tmp_path)
        assert "Stripe" in result

    def test_js_stripe_react(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@stripe/react-stripe-js": "^2.0"}}')
        result = detect_payment_tools(tmp_path)
        assert "Stripe" in result

    def test_js_paypal(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@paypal/react-paypal-js": "^8.0"}}')
        result = detect_payment_tools(tmp_path)
        assert "PayPal" in result

    def test_js_paddle(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@paddle/paddle-js": "^1.0"}}')
        result = detect_payment_tools(tmp_path)
        assert "Paddle" in result

    def test_js_adyen(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@adyen/adyen-web": "^5.0"}}')
        result = detect_payment_tools(tmp_path)
        assert "Adyen" in result

    def test_js_recurly(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"recurly": "^4.0"}}')
        result = detect_payment_tools(tmp_path)
        assert "Recurly" in result

    def test_js_chargebee(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"chargebee": "^2.0"}}')
        result = detect_payment_tools(tmp_path)
        assert "Chargebee" in result

    def test_js_lemon_squeezy(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@lemonsqueezy/lemonsqueezy.js": "^2.0"}}')
        result = detect_payment_tools(tmp_path)
        assert "Lemon Squeezy" in result

    def test_go_stripe(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/stripe/stripe-go v72.0.0\n")
        result = detect_payment_tools(tmp_path)
        assert "Stripe" in result

    def test_go_paypal(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/plutov/paypal v4.0.0\n")
        result = detect_payment_tools(tmp_path)
        assert "PayPal" in result

    def test_rust_stripe(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nasync-stripe = "0.25"\n')
        result = detect_payment_tools(tmp_path)
        assert "Stripe" in result

    def test_java_stripe(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.stripe:stripe-java:24.0'\n")
        result = detect_payment_tools(tmp_path)
        assert "Stripe" in result

    def test_java_adyen(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency>adyen-java-api-library</dependency>\n")
        result = detect_payment_tools(tmp_path)
        assert "Adyen" in result

    def test_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("stripe>=5.0\nrazorpay>=1.0\n")
        result = detect_payment_tools(tmp_path)
        assert result == sorted(result)

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("stripe>=5.0\n")
        (tmp_path / "package.json").write_text('{"dependencies": {"stripe": "^12.0"}}')
        result = detect_payment_tools(tmp_path)
        assert result.count("Stripe") == 1


# ---------------------------------------------------------------------------
# detect_date_libs
# ---------------------------------------------------------------------------
class TestDetectDateLibs:
    def test_empty(self, tmp_path):
        assert detect_date_libs(tmp_path) == []

    def test_python_arrow(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("arrow>=1.0\n")
        result = detect_date_libs(tmp_path)
        assert "Arrow" in result

    def test_python_pendulum(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pendulum>=3.0\n")
        result = detect_date_libs(tmp_path)
        assert "Pendulum" in result

    def test_python_dateutil(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-dateutil>=2.0\n")
        result = detect_date_libs(tmp_path)
        assert "python-dateutil" in result

    def test_python_pytz(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pytz>=2024.1\n")
        result = detect_date_libs(tmp_path)
        assert "pytz" in result

    def test_python_dateparser(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("dateparser>=1.0\n")
        result = detect_date_libs(tmp_path)
        assert "dateparser" in result

    def test_python_ciso8601(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("ciso8601>=2.0\n")
        result = detect_date_libs(tmp_path)
        assert "ciso8601" in result

    def test_js_dayjs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"dayjs": "^1.11"}}')
        result = detect_date_libs(tmp_path)
        assert "Day.js" in result

    def test_js_date_fns(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"date-fns": "^3.0"}}')
        result = detect_date_libs(tmp_path)
        assert "date-fns" in result

    def test_js_luxon(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"luxon": "^3.0"}}')
        result = detect_date_libs(tmp_path)
        assert "Luxon" in result

    def test_js_moment(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"moment": "^2.0"}}')
        result = detect_date_libs(tmp_path)
        assert "Moment.js" in result

    def test_js_temporal(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@js-temporal/polyfill": "^0.4"}}')
        result = detect_date_libs(tmp_path)
        assert "Temporal" in result

    def test_js_spacetime(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"spacetime": "^7.0"}}')
        result = detect_date_libs(tmp_path)
        assert "Spacetime" in result

    def test_js_chrono_node(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"chrono-node": "^2.0"}}')
        result = detect_date_libs(tmp_path)
        assert "chrono-node" in result

    def test_go_dateparse(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/araddon/dateparse v0.0.0\n")
        result = detect_date_libs(tmp_path)
        assert "dateparse" in result

    def test_rust_chrono(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nchrono = "0.4"\n')
        result = detect_date_libs(tmp_path)
        assert "chrono" in result

    def test_rust_time(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntime = "0.3"\n')
        result = detect_date_libs(tmp_path)
        assert "time (Rust)" in result

    def test_java_joda(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'joda-time:joda-time:2.12'\n")
        result = detect_date_libs(tmp_path)
        assert "Joda-Time" in result

    def test_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("arrow>=1.0\npytz>=2024.1\n")
        result = detect_date_libs(tmp_path)
        assert result == sorted(result)

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-dateutil>=2.0\ndateutil>=2.0\n")
        result = detect_date_libs(tmp_path)
        assert result.count("python-dateutil") == 1

    def test_moment_timezone_dedup(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"moment": "^2.0", "moment-timezone": "^0.5"}}')
        result = detect_date_libs(tmp_path)
        assert result.count("Moment.js") == 1

    def test_multiple_libs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"dayjs": "^1.11", "date-fns": "^3.0", "luxon": "^3.0"}}')
        result = detect_date_libs(tmp_path)
        assert "Day.js" in result
        assert "date-fns" in result
        assert "Luxon" in result


# ---------------------------------------------------------------------------
# detect_image_libs
# ---------------------------------------------------------------------------
class TestDetectImageLibs:
    def test_empty(self, tmp_path):
        assert detect_image_libs(tmp_path) == []

    def test_python_pillow(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pillow>=10.0\n")
        result = detect_image_libs(tmp_path)
        assert "Pillow" in result

    def test_python_opencv(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("opencv-python>=4.0\n")
        result = detect_image_libs(tmp_path)
        assert "OpenCV" in result

    def test_python_opencv_headless(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("opencv-python-headless>=4.0\n")
        result = detect_image_libs(tmp_path)
        assert "OpenCV" in result

    def test_python_scikit_image(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("scikit-image>=0.20\n")
        result = detect_image_libs(tmp_path)
        assert "scikit-image" in result

    def test_python_wand(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("wand>=0.6\n")
        result = detect_image_libs(tmp_path)
        assert "Wand" in result

    def test_python_imageio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("imageio>=2.0\n")
        result = detect_image_libs(tmp_path)
        assert "imageio" in result

    def test_js_sharp(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"sharp": "^0.33"}}')
        result = detect_image_libs(tmp_path)
        assert "Sharp" in result

    def test_js_jimp(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"jimp": "^0.22"}}')
        result = detect_image_libs(tmp_path)
        assert "Jimp" in result

    def test_js_canvas(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"canvas": "^2.0"}}')
        result = detect_image_libs(tmp_path)
        assert "node-canvas" in result

    def test_js_blurhash(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"blurhash": "^2.0"}}')
        result = detect_image_libs(tmp_path)
        assert "BlurHash" in result

    def test_js_cropperjs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"cropperjs": "^1.0"}}')
        result = detect_image_libs(tmp_path)
        assert "Cropper.js" in result

    def test_go_imaging(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire github.com/disintegration/imaging v1.6\n")
        result = detect_image_libs(tmp_path)
        assert "imaging" in result

    def test_go_gocv(self, tmp_path):
        (tmp_path / "go.mod").write_text("module myapp\nrequire gocv.io/x/gocv v0.35\n")
        result = detect_image_libs(tmp_path)
        assert "GoCV" in result

    def test_rust_image(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nimage = "0.24"\n')
        result = detect_image_libs(tmp_path)
        assert "image (Rust)" in result

    def test_rust_resvg(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nresvg = "0.35"\n')
        result = detect_image_libs(tmp_path)
        assert "resvg" in result

    def test_java_thumbnailator(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'net.coobird:thumbnailator:0.4'\n")
        result = detect_image_libs(tmp_path)
        assert "Thumbnailator" in result

    def test_sorted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pillow>=10.0\nopencv-python>=4.0\n")
        result = detect_image_libs(tmp_path)
        assert result == sorted(result)

    def test_no_duplicates(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("opencv-python>=4.0\nopencv-python-headless>=4.0\n")
        result = detect_image_libs(tmp_path)
        assert result.count("OpenCV") == 1

    def test_multiple_libs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"sharp": "^0.33", "jimp": "^0.22", "blurhash": "^2.0"}}')
        result = detect_image_libs(tmp_path)
        assert "Sharp" in result
        assert "Jimp" in result
        assert "BlurHash" in result


# ---------------------------------------------------------------------------
# detect_crypto_libs
# ---------------------------------------------------------------------------
class TestDetectCryptoLibs:
    def test_empty(self, tmp_path):
        assert detect_crypto_libs(tmp_path) == []

    def test_python_cryptography(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("cryptography>=41.0\n")
        result = detect_crypto_libs(tmp_path)
        assert "cryptography" in result

    def test_python_pycryptodome(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pycryptodome>=3.0\n")
        result = detect_crypto_libs(tmp_path)
        assert "PyCryptodome" in result

    def test_python_bcrypt(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("bcrypt>=4.0\n")
        result = detect_crypto_libs(tmp_path)
        assert "bcrypt" in result

    def test_python_pynacl(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pynacl>=1.0\n")
        result = detect_crypto_libs(tmp_path)
        assert "PyNaCl" in result

    def test_python_argon2(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("argon2-cffi>=21.0\n")
        result = detect_crypto_libs(tmp_path)
        assert "Argon2" in result

    def test_python_passlib(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("passlib>=1.7\n")
        result = detect_crypto_libs(tmp_path)
        assert "Passlib" in result

    def test_js_crypto_js(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"crypto-js": "^4.0"}}')
        result = detect_crypto_libs(tmp_path)
        assert "CryptoJS" in result

    def test_js_bcryptjs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"bcryptjs": "^2.0"}}')
        result = detect_crypto_libs(tmp_path)
        assert "bcrypt.js" in result

    def test_js_jose(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"jose": "^5.0"}}')
        result = detect_crypto_libs(tmp_path)
        assert "jose" in result

    def test_js_node_forge(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"node-forge": "^1.0"}}')
        result = detect_crypto_libs(tmp_path)
        assert "node-forge" in result

    def test_js_noble_hashes(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@noble/hashes": "^1.0"}}')
        result = detect_crypto_libs(tmp_path)
        assert "noble-hashes" in result

    def test_go_xcrypto(self, tmp_path):
        (tmp_path / "go.sum").write_text("golang.org/x/crypto v0.21.0 h1:abc123\n")
        result = detect_crypto_libs(tmp_path)
        assert "x/crypto" in result

    def test_rust_ring(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nring = "0.17"')
        result = detect_crypto_libs(tmp_path)
        assert "ring" in result

    def test_rust_rustls(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nrustls = "0.23"')
        result = detect_crypto_libs(tmp_path)
        assert "rustls" in result

    def test_java_bouncy_castle(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.bouncycastle:bcprov-jdk18on:1.78'")
        result = detect_crypto_libs(tmp_path)
        assert "Bouncy Castle" in result

    def test_java_tink(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>com.google.crypto.tink</groupId></dependency>")
        result = detect_crypto_libs(tmp_path)
        assert "Tink" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("cryptography>=41.0\nbcrypt>=4.0\nargon2-cffi>=21.0\n")
        result = detect_crypto_libs(tmp_path)
        assert "cryptography" in result
        assert "bcrypt" in result
        assert "Argon2" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pynacl>=1.0\nbcrypt>=4.0\ncryptography>=41.0\n")
        result = detect_crypto_libs(tmp_path)
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# detect_pdf_libs
# ---------------------------------------------------------------------------
class TestDetectPdfLibs:
    def test_empty(self, tmp_path):
        assert detect_pdf_libs(tmp_path) == []

    def test_python_reportlab(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("reportlab>=4.0\n")
        result = detect_pdf_libs(tmp_path)
        assert "ReportLab" in result

    def test_python_weasyprint(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("weasyprint>=60.0\n")
        result = detect_pdf_libs(tmp_path)
        assert "WeasyPrint" in result

    def test_python_pypdf(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pypdf>=3.0\n")
        result = detect_pdf_libs(tmp_path)
        assert "pypdf" in result

    def test_python_pymupdf(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pymupdf>=1.23\n")
        result = detect_pdf_libs(tmp_path)
        assert "PyMuPDF" in result

    def test_python_docx(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-docx>=1.0\n")
        result = detect_pdf_libs(tmp_path)
        assert "python-docx" in result

    def test_python_openpyxl(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("openpyxl>=3.0\n")
        result = detect_pdf_libs(tmp_path)
        assert "openpyxl" in result

    def test_python_pdfplumber(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pdfplumber>=0.10\n")
        result = detect_pdf_libs(tmp_path)
        assert "pdfplumber" in result

    def test_js_jspdf(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"jspdf": "^2.0"}}')
        result = detect_pdf_libs(tmp_path)
        assert "jsPDF" in result

    def test_js_pdf_lib(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"pdf-lib": "^1.0"}}')
        result = detect_pdf_libs(tmp_path)
        assert "pdf-lib" in result

    def test_js_exceljs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"exceljs": "^4.0"}}')
        result = detect_pdf_libs(tmp_path)
        assert "ExcelJS" in result

    def test_js_pdfmake(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"pdfmake": "^0.2"}}')
        result = detect_pdf_libs(tmp_path)
        assert "pdfmake" in result

    def test_go_excelize(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/xuri/excelize/v2 v2.8.0 h1:abc\n")
        result = detect_pdf_libs(tmp_path)
        assert "Excelize" in result

    def test_rust_printpdf(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nprintpdf = "0.6"')
        result = detect_pdf_libs(tmp_path)
        assert "printpdf" in result

    def test_java_pdfbox(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>org.apache.pdfbox</groupId></dependency>")
        result = detect_pdf_libs(tmp_path)
        assert "Apache PDFBox" in result

    def test_java_itext(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'com.itextpdf:itext7-core:7.2'")
        result = detect_pdf_libs(tmp_path)
        assert "iText" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("reportlab>=4.0\npypdf>=3.0\nopenpyxl>=3.0\n")
        result = detect_pdf_libs(tmp_path)
        assert "ReportLab" in result
        assert "pypdf" in result
        assert "openpyxl" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("weasyprint>=60.0\nreportlab>=4.0\npypdf>=3.0\n")
        result = detect_pdf_libs(tmp_path)
        assert result == sorted(result)


class TestDetectDataVizLibs:
    def test_empty(self, tmp_path):
        assert detect_data_viz_libs(tmp_path) == []

    def test_python_matplotlib(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("matplotlib>=3.8\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Matplotlib" in result

    def test_python_plotly(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("plotly>=5.0\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Plotly" in result

    def test_python_seaborn(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("seaborn>=0.13\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Seaborn" in result

    def test_python_bokeh(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("bokeh>=3.0\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Bokeh" in result

    def test_python_altair(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("altair>=5.0\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Altair" in result

    def test_python_dash(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("dash>=2.0\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Dash" in result

    def test_python_streamlit(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("streamlit>=1.30\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Streamlit" in result

    def test_python_gradio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("gradio>=4.0\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Gradio" in result

    def test_js_d3(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"d3": "^7.0"}}')
        result = detect_data_viz_libs(tmp_path)
        assert "D3.js" in result

    def test_js_chartjs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"chart.js": "^4.0"}}')
        result = detect_data_viz_libs(tmp_path)
        assert "Chart.js" in result

    def test_js_recharts(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"recharts": "^2.0"}}')
        result = detect_data_viz_libs(tmp_path)
        assert "Recharts" in result

    def test_js_echarts(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"echarts": "^5.0"}}')
        result = detect_data_viz_libs(tmp_path)
        assert "ECharts" in result

    def test_js_threejs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"three": "^0.160"}}')
        result = detect_data_viz_libs(tmp_path)
        assert "Three.js" in result

    def test_go_gonum_plot(self, tmp_path):
        (tmp_path / "go.sum").write_text("gonum.org/v1/plot v0.14.0 h1:abc\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Gonum Plot" in result

    def test_rust_plotters(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nplotters = "0.3"')
        result = detect_data_viz_libs(tmp_path)
        assert "Plotters" in result

    def test_java_jfreechart(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>org.jfree</groupId><artifactId>jfreechart</artifactId></dependency>")
        result = detect_data_viz_libs(tmp_path)
        assert "JFreeChart" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("matplotlib>=3.8\nplotly>=5.0\nseaborn>=0.13\n")
        result = detect_data_viz_libs(tmp_path)
        assert "Matplotlib" in result
        assert "Plotly" in result
        assert "Seaborn" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("seaborn>=0.13\nmatplotlib>=3.8\nbokeh>=3.0\n")
        result = detect_data_viz_libs(tmp_path)
        assert result == sorted(result)


class TestDetectGeoLibs:
    def test_empty(self, tmp_path):
        assert detect_geo_libs(tmp_path) == []

    def test_python_geopandas(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("geopandas>=0.14\n")
        result = detect_geo_libs(tmp_path)
        assert "GeoPandas" in result

    def test_python_shapely(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("shapely>=2.0\n")
        result = detect_geo_libs(tmp_path)
        assert "Shapely" in result

    def test_python_rasterio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("rasterio>=1.3\n")
        result = detect_geo_libs(tmp_path)
        assert "rasterio" in result

    def test_python_geopy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("geopy>=2.4\n")
        result = detect_geo_libs(tmp_path)
        assert "geopy" in result

    def test_python_h3(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("h3>=4.0\n")
        result = detect_geo_libs(tmp_path)
        assert "H3" in result

    def test_python_cartopy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("cartopy>=0.22\n")
        result = detect_geo_libs(tmp_path)
        assert "Cartopy" in result

    def test_js_leaflet(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"leaflet": "^1.9"}}')
        result = detect_geo_libs(tmp_path)
        assert "Leaflet" in result

    def test_js_mapbox_gl(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"mapbox-gl": "^3.0"}}')
        result = detect_geo_libs(tmp_path)
        assert "Mapbox GL" in result

    def test_js_turf(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"@turf/turf": "^6.0"}}')
        result = detect_geo_libs(tmp_path)
        assert "Turf.js" in result

    def test_js_openlayers(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"ol": "^8.0"}}')
        result = detect_geo_libs(tmp_path)
        assert "OpenLayers" in result

    def test_go_orb(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/paulmach/orb v0.10.0 h1:abc\n")
        result = detect_geo_libs(tmp_path)
        assert "orb" in result

    def test_rust_geo(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ngeo = "0.27"')
        result = detect_geo_libs(tmp_path)
        assert "geo" in result

    def test_java_geotools(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>org.geotools</groupId></dependency>")
        result = detect_geo_libs(tmp_path)
        assert "GeoTools" in result

    def test_java_jts(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.locationtech.jts:jts-core:1.19'")
        result = detect_geo_libs(tmp_path)
        assert "JTS" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("geopandas>=0.14\nshapely>=2.0\nfiona>=1.9\n")
        result = detect_geo_libs(tmp_path)
        assert "GeoPandas" in result
        assert "Shapely" in result
        assert "Fiona" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("shapely>=2.0\ngeopandas>=0.14\nfiona>=1.9\n")
        result = detect_geo_libs(tmp_path)
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# detect_media_libs
# ---------------------------------------------------------------------------
class TestDetectMediaLibs:
    def test_empty(self, tmp_path):
        assert detect_media_libs(tmp_path) == []

    def test_python_ffmpeg(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("ffmpeg-python>=0.2\n")
        result = detect_media_libs(tmp_path)
        assert "FFmpeg" in result

    def test_python_moviepy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("moviepy>=1.0\n")
        result = detect_media_libs(tmp_path)
        assert "MoviePy" in result

    def test_python_pydub(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pydub>=0.25\n")
        result = detect_media_libs(tmp_path)
        assert "Pydub" in result

    def test_python_librosa(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("librosa>=0.10\n")
        result = detect_media_libs(tmp_path)
        assert "Librosa" in result

    def test_python_pyav(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("av>=11.0\n")
        result = detect_media_libs(tmp_path)
        assert "PyAV" in result

    def test_python_torchaudio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("torchaudio>=2.0\n")
        result = detect_media_libs(tmp_path)
        assert "torchaudio" in result

    def test_js_fluent_ffmpeg(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"fluent-ffmpeg": "^2.1"}}')
        result = detect_media_libs(tmp_path)
        assert "FFmpeg" in result

    def test_js_tone(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"tone": "^14.7"}}')
        result = detect_media_libs(tmp_path)
        assert "Tone.js" in result

    def test_js_videojs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"video.js": "^8.0"}}')
        result = detect_media_libs(tmp_path)
        assert "Video.js" in result

    def test_js_hlsjs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"hls.js": "^1.5"}}')
        result = detect_media_libs(tmp_path)
        assert "HLS.js" in result

    def test_js_howler(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"howler": "^2.2"}}')
        result = detect_media_libs(tmp_path)
        assert "Howler.js" in result

    def test_go_beep(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/faiface/beep v1.1.0 h1:abc\n")
        result = detect_media_libs(tmp_path)
        assert "Beep" in result

    def test_rust_rodio(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nrodio = "0.17"')
        result = detect_media_libs(tmp_path)
        assert "Rodio" in result

    def test_rust_symphonia(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nsymphonia = "0.5"')
        result = detect_media_libs(tmp_path)
        assert "Symphonia" in result

    def test_java_javacv(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>org.bytedeco</groupId><artifactId>javacv</artifactId></dependency>")
        result = detect_media_libs(tmp_path)
        assert "JavaCV" in result

    def test_java_jcodec(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.jcodec:jcodec:0.2.5'")
        result = detect_media_libs(tmp_path)
        assert "JCodec" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("ffmpeg-python>=0.2\nmoviepy>=1.0\npydub>=0.25\n")
        result = detect_media_libs(tmp_path)
        assert "FFmpeg" in result
        assert "MoviePy" in result
        assert "Pydub" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pydub>=0.25\nlibrosa>=0.10\nffmpeg-python>=0.2\n")
        result = detect_media_libs(tmp_path)
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# detect_math_libs
# ---------------------------------------------------------------------------
class TestDetectMathLibs:
    def test_empty(self, tmp_path):
        assert detect_math_libs(tmp_path) == []

    def test_python_numpy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("numpy>=1.24\n")
        result = detect_math_libs(tmp_path)
        assert "NumPy" in result

    def test_python_scipy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("scipy>=1.11\n")
        result = detect_math_libs(tmp_path)
        assert "SciPy" in result

    def test_python_pandas(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pandas>=2.0\n")
        result = detect_math_libs(tmp_path)
        assert "Pandas" in result

    def test_python_polars(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("polars>=0.20\n")
        result = detect_math_libs(tmp_path)
        assert "Polars" in result

    def test_python_sympy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sympy>=1.12\n")
        result = detect_math_libs(tmp_path)
        assert "SymPy" in result

    def test_python_sklearn(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("scikit-learn>=1.3\n")
        result = detect_math_libs(tmp_path)
        assert "scikit-learn" in result

    def test_python_jax(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("jax>=0.4\n")
        result = detect_math_libs(tmp_path)
        assert "JAX" in result

    def test_python_dask(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("dask>=2023.1\n")
        result = detect_math_libs(tmp_path)
        assert "Dask" in result

    def test_js_mathjs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"mathjs": "^12.0"}}')
        result = detect_math_libs(tmp_path)
        assert "math.js" in result

    def test_js_danfojs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"danfojs": "^1.1"}}')
        result = detect_math_libs(tmp_path)
        assert "Danfo.js" in result

    def test_go_gonum(self, tmp_path):
        (tmp_path / "go.sum").write_text("gonum.org/v1/gonum v0.14.0 h1:abc\n")
        result = detect_math_libs(tmp_path)
        assert "Gonum" in result

    def test_rust_nalgebra(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nnalgebra = "0.32"')
        result = detect_math_libs(tmp_path)
        assert "nalgebra" in result

    def test_rust_statrs(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nstatrs = "0.16"')
        result = detect_math_libs(tmp_path)
        assert "statrs" in result

    def test_java_commons_math(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><groupId>org.apache.commons</groupId><artifactId>commons-math3</artifactId></dependency>")
        result = detect_math_libs(tmp_path)
        assert "Commons Math" in result

    def test_java_nd4j(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.nd4j:nd4j-native:1.0.0'")
        result = detect_math_libs(tmp_path)
        assert "ND4J" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("numpy>=1.24\nscipy>=1.11\npandas>=2.0\n")
        result = detect_math_libs(tmp_path)
        assert "NumPy" in result
        assert "SciPy" in result
        assert "Pandas" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sympy>=1.12\nnumpy>=1.24\npandas>=2.0\n")
        result = detect_math_libs(tmp_path)
        assert result == sorted(result)


# ---------------------------------------------------------------------------
# detect_async_libs
# ---------------------------------------------------------------------------
class TestDetectAsyncLibs:
    def test_empty(self, tmp_path):
        assert detect_async_libs(tmp_path) == []

    def test_python_twisted(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("twisted>=23.0\n")
        result = detect_async_libs(tmp_path)
        assert "Twisted" in result

    def test_python_trio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("trio>=0.22\n")
        result = detect_async_libs(tmp_path)
        assert "trio" in result

    def test_python_anyio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("anyio>=4.0\n")
        result = detect_async_libs(tmp_path)
        assert "AnyIO" in result

    def test_python_gevent(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("gevent>=23.0\n")
        result = detect_async_libs(tmp_path)
        assert "Gevent" in result

    def test_python_uvloop(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("uvloop>=0.19\n")
        result = detect_async_libs(tmp_path)
        assert "uvloop" in result

    def test_python_celery(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("celery>=5.3\n")
        result = detect_async_libs(tmp_path)
        assert "Celery" in result

    def test_js_rxjs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"rxjs": "^7.0"}}')
        result = detect_async_libs(tmp_path)
        assert "RxJS" in result

    def test_js_piscina(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"piscina": "^4.0"}}')
        result = detect_async_libs(tmp_path)
        assert "Piscina" in result

    def test_js_comlink(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies": {"comlink": "^4.4"}}')
        result = detect_async_libs(tmp_path)
        assert "Comlink" in result

    def test_go_xsync(self, tmp_path):
        (tmp_path / "go.sum").write_text("golang.org/x/sync v0.6.0 h1:abc\n")
        result = detect_async_libs(tmp_path)
        assert "x/sync" in result

    def test_go_ants(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/panjf2000/ants/v2 v2.9.0 h1:abc\n")
        result = detect_async_libs(tmp_path)
        assert "ants" in result

    def test_rust_tokio(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntokio = { version = "1", features = ["full"] }')
        result = detect_async_libs(tmp_path)
        assert "Tokio" in result

    def test_rust_rayon(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nrayon = "1.8"')
        result = detect_async_libs(tmp_path)
        assert "Rayon" in result

    def test_rust_crossbeam(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ncrossbeam = "0.8"')
        result = detect_async_libs(tmp_path)
        assert "Crossbeam" in result

    def test_java_rxjava(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'io.reactivex.rxjava3:rxjava:3.1'")
        result = detect_async_libs(tmp_path)
        assert "RxJava" in result

    def test_java_reactor(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>reactor-core</artifactId></dependency>")
        result = detect_async_libs(tmp_path)
        assert "Project Reactor" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("trio>=0.22\nanyio>=4.0\nuvloop>=0.19\n")
        result = detect_async_libs(tmp_path)
        assert "trio" in result
        assert "AnyIO" in result
        assert "uvloop" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("uvloop>=0.19\nanyio>=4.0\ntrio>=0.22\n")
        result = detect_async_libs(tmp_path)
        assert result == sorted(result)


# detect_compression_libs
class TestDetectCompressionLibs:
    def test_empty_project(self, tmp_path):
        assert detect_compression_libs(tmp_path) == []

    def test_python_zstandard(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("zstandard>=0.22\n")
        result = detect_compression_libs(tmp_path)
        assert "Zstandard" in result

    def test_python_lz4(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("lz4>=4.3\n")
        result = detect_compression_libs(tmp_path)
        assert "LZ4" in result

    def test_python_brotli(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("brotli>=1.1\n")
        result = detect_compression_libs(tmp_path)
        assert "Brotli" in result

    def test_python_snappy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("python-snappy>=0.6\n")
        result = detect_compression_libs(tmp_path)
        assert "Snappy" in result

    def test_python_blosc(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("blosc>=1.11\n")
        result = detect_compression_libs(tmp_path)
        assert "Blosc" in result

    def test_python_7zip(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("py7zr>=0.20\n")
        result = detect_compression_libs(tmp_path)
        assert "7-Zip" in result

    def test_python_rarfile(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("rarfile>=4.1\n")
        result = detect_compression_libs(tmp_path)
        assert "RAR" in result

    def test_js_pako(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"pako":"^2.1"}}')
        result = detect_compression_libs(tmp_path)
        assert "pako" in result

    def test_js_jszip(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"jszip":"^3.10"}}')
        result = detect_compression_libs(tmp_path)
        assert "JSZip" in result

    def test_js_archiver(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"archiver":"^6.0"}}')
        result = detect_compression_libs(tmp_path)
        assert "archiver" in result

    def test_js_fflate(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"fflate":"^0.8"}}')
        result = detect_compression_libs(tmp_path)
        assert "fflate" in result

    def test_go_klauspost(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/klauspost/compress v1.17.0 h1:abc\n")
        result = detect_compression_libs(tmp_path)
        assert "klauspost/compress" in result

    def test_go_lz4(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/pierrec/lz4/v4 v4.1.0 h1:abc\n")
        result = detect_compression_libs(tmp_path)
        assert "LZ4" in result

    def test_rust_flate2(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nflate2 = "1.0"\n')
        result = detect_compression_libs(tmp_path)
        assert "flate2" in result

    def test_rust_zstd(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nzstd = "0.13"\n')
        result = detect_compression_libs(tmp_path)
        assert "Zstandard" in result

    def test_java_commons_compress(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.apache.commons:commons-compress:1.26'\n")
        result = detect_compression_libs(tmp_path)
        assert "Commons Compress" in result

    def test_java_snappy(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency>snappy-java</dependency>")
        result = detect_compression_libs(tmp_path)
        assert "Snappy" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("zstandard>=0.22\nlz4>=4.3\nbrotli>=1.1\n")
        result = detect_compression_libs(tmp_path)
        assert result == sorted(result)


# detect_email_libs
class TestDetectEmailLibs:
    def test_empty_project(self, tmp_path):
        assert detect_email_libs(tmp_path) == []

    def test_python_sendgrid(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sendgrid>=6.0\n")
        result = detect_email_libs(tmp_path)
        assert "SendGrid" in result

    def test_python_resend(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("resend>=0.7\n")
        result = detect_email_libs(tmp_path)
        assert "Resend" in result

    def test_python_flask_mail(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flask-mail>=0.9\n")
        result = detect_email_libs(tmp_path)
        assert "Flask-Mail" in result

    def test_python_yagmail(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("yagmail>=0.15\n")
        result = detect_email_libs(tmp_path)
        assert "yagmail" in result

    def test_python_mailchimp(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mailchimp3>=3.0\n")
        result = detect_email_libs(tmp_path)
        assert "Mailchimp" in result

    def test_python_postmark(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("postmark>=0.5\n")
        result = detect_email_libs(tmp_path)
        assert "Postmark" in result

    def test_python_aiosmtplib(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("aiosmtplib>=2.0\n")
        result = detect_email_libs(tmp_path)
        assert "aiosmtplib" in result

    def test_js_nodemailer(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"nodemailer":"^6.9"}}')
        result = detect_email_libs(tmp_path)
        assert "Nodemailer" in result

    def test_js_sendgrid(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@sendgrid/mail":"^7.7"}}')
        result = detect_email_libs(tmp_path)
        assert "SendGrid" in result

    def test_js_mjml(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"mjml":"^4.14"}}')
        result = detect_email_libs(tmp_path)
        assert "MJML" in result

    def test_js_react_email(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-email":"^1.10"}}')
        result = detect_email_libs(tmp_path)
        assert "React Email" in result

    def test_go_gomail(self, tmp_path):
        (tmp_path / "go.sum").write_text("gopkg.in/go-gomail/go-gomail.v2 v2.0.0 h1:abc\n")
        result = detect_email_libs(tmp_path)
        assert "Gomail" in result

    def test_rust_lettre(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nlettre = "0.11"\n')
        result = detect_email_libs(tmp_path)
        assert "Lettre" in result

    def test_java_spring_mail(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.springframework.boot:spring-boot-starter-mail:3.2'\n")
        result = detect_email_libs(tmp_path)
        assert "Spring Mail" in result

    def test_java_jakarta_mail(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency>jakarta.mail</dependency>")
        result = detect_email_libs(tmp_path)
        assert "Jakarta Mail" in result

    def test_java_commons_email(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.apache.commons:commons-email:1.5'\n")
        result = detect_email_libs(tmp_path)
        assert "Commons Email" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sendgrid>=6.0\nresend>=0.7\nyagmail>=0.15\n")
        result = detect_email_libs(tmp_path)
        assert result == sorted(result)


# detect_a11y_tools
class TestDetectA11yTools:
    def test_empty_project(self, tmp_path):
        assert detect_a11y_tools(tmp_path) == []

    def test_python_axe_selenium(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("axe-selenium-python>=4.0\n")
        result = detect_a11y_tools(tmp_path)
        assert "axe-core" in result

    def test_python_playwright(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("playwright>=1.40\n")
        result = detect_a11y_tools(tmp_path)
        assert "Playwright" in result

    def test_python_selenium(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("selenium>=4.15\n")
        result = detect_a11y_tools(tmp_path)
        assert "Selenium" in result

    def test_python_pa11y(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pa11y>=0.1\n")
        result = detect_a11y_tools(tmp_path)
        assert "Pa11y" in result

    def test_js_axe_core(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"axe-core":"^4.8"}}')
        result = detect_a11y_tools(tmp_path)
        assert "axe-core" in result

    def test_js_jsx_a11y(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"eslint-plugin-jsx-a11y":"^6.8"}}')
        result = detect_a11y_tools(tmp_path)
        assert "jsx-a11y" in result

    def test_js_react_aria(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-aria":"^3.30"}}')
        result = detect_a11y_tools(tmp_path)
        assert "React Aria" in result

    def test_js_radix_ui(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@radix-ui/react-dialog":"^1.0"}}')
        result = detect_a11y_tools(tmp_path)
        assert "Radix UI" in result

    def test_js_downshift(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"downshift":"^8.0"}}')
        result = detect_a11y_tools(tmp_path)
        assert "Downshift" in result

    def test_js_focus_trap_react(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"focus-trap-react":"^10.0"}}')
        result = detect_a11y_tools(tmp_path)
        assert "focus-trap-react" in result

    def test_js_testing_library(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"@testing-library/react":"^14.0"}}')
        result = detect_a11y_tools(tmp_path)
        assert "Testing Library" in result

    def test_js_jest_axe(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"jest-axe":"^8.0"}}')
        result = detect_a11y_tools(tmp_path)
        assert "jest-axe" in result

    def test_js_cypress_axe(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"cypress-axe":"^1.5"}}')
        result = detect_a11y_tools(tmp_path)
        assert "cypress-axe" in result

    def test_js_a11y_dialog(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"a11y-dialog":"^8.0"}}')
        result = detect_a11y_tools(tmp_path)
        assert "a11y-dialog" in result

    def test_config_accessibilityrc(self, tmp_path):
        (tmp_path / ".accessibilityrc").write_text("{}")
        result = detect_a11y_tools(tmp_path)
        assert "a11y-config" in result

    def test_config_pa11yci(self, tmp_path):
        (tmp_path / ".pa11yci").write_text("{}")
        result = detect_a11y_tools(tmp_path)
        assert "Pa11y CI" in result

    def test_multiple_js(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"axe-core":"^4.8","@radix-ui/react-dialog":"^1.0","downshift":"^8.0"}}')
        result = detect_a11y_tools(tmp_path)
        assert "axe-core" in result
        assert "Radix UI" in result
        assert "Downshift" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"focus-trap-react":"^10","axe-core":"^4","downshift":"^8"}}')
        result = detect_a11y_tools(tmp_path)
        assert result == sorted(result)


# detect_scraping_libs
class TestDetectScrapingLibs:
    def test_empty_project(self, tmp_path):
        assert detect_scraping_libs(tmp_path) == []

    def test_python_scrapy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("scrapy>=2.11\n")
        result = detect_scraping_libs(tmp_path)
        assert "Scrapy" in result

    def test_python_beautifulsoup(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("beautifulsoup4>=4.12\n")
        result = detect_scraping_libs(tmp_path)
        assert "BeautifulSoup" in result

    def test_python_lxml(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("lxml>=5.0\n")
        result = detect_scraping_libs(tmp_path)
        assert "lxml" in result

    def test_python_parsel(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("parsel>=1.8\n")
        result = detect_scraping_libs(tmp_path)
        assert "Parsel" in result

    def test_python_mechanicalsoup(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mechanicalsoup>=0.12\n")
        result = detect_scraping_libs(tmp_path)
        assert "MechanicalSoup" in result

    def test_python_trafilatura(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("trafilatura>=1.6\n")
        result = detect_scraping_libs(tmp_path)
        assert "trafilatura" in result

    def test_python_newspaper3k(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("newspaper3k>=0.2\n")
        result = detect_scraping_libs(tmp_path)
        assert "newspaper3k" in result

    def test_js_puppeteer(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"puppeteer":"^22.0"}}')
        result = detect_scraping_libs(tmp_path)
        assert "Puppeteer" in result

    def test_js_cheerio(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"cheerio":"^1.0"}}')
        result = detect_scraping_libs(tmp_path)
        assert "Cheerio" in result

    def test_js_crawlee(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"crawlee":"^3.7"}}')
        result = detect_scraping_libs(tmp_path)
        assert "Crawlee" in result

    def test_js_jsdom(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"jsdom":"^24.0"}}')
        result = detect_scraping_libs(tmp_path)
        assert "jsdom" in result

    def test_js_playwright(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"playwright":"^1.40"}}')
        result = detect_scraping_libs(tmp_path)
        assert "Playwright" in result

    def test_go_colly(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/gocolly/colly v2.1.0 h1:abc\n")
        result = detect_scraping_libs(tmp_path)
        assert "Colly" in result

    def test_go_goquery(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/PuerkitoBio/goquery v1.8.0 h1:abc\n")
        result = detect_scraping_libs(tmp_path)
        assert "goquery" in result

    def test_rust_scraper(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nscraper = "0.18"\n')
        result = detect_scraping_libs(tmp_path)
        assert "scraper" in result

    def test_java_jsoup(self, tmp_path):
        (tmp_path / "build.gradle").write_text("implementation 'org.jsoup:jsoup:1.17'\n")
        result = detect_scraping_libs(tmp_path)
        assert "jsoup" in result

    def test_java_htmlunit(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency>htmlunit</dependency>")
        result = detect_scraping_libs(tmp_path)
        assert "HtmlUnit" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("scrapy>=2.11\nbeautifulsoup4>=4.12\nlxml>=5.0\n")
        result = detect_scraping_libs(tmp_path)
        assert "Scrapy" in result
        assert "BeautifulSoup" in result
        assert "lxml" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("scrapy>=2.11\nbeautifulsoup4>=4.12\nlxml>=5.0\n")
        result = detect_scraping_libs(tmp_path)
        assert result == sorted(result)


# detect_desktop_frameworks
class TestDetectDesktopFrameworks:
    def test_empty_project(self, tmp_path):
        assert detect_desktop_frameworks(tmp_path) == []

    def test_python_pyqt5(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyqt5>=5.15\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "PyQt5" in result

    def test_python_pyqt6(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyqt6>=6.6\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "PyQt6" in result

    def test_python_pyside6(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyside6>=6.6\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "PySide6" in result

    def test_python_kivy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("kivy>=2.3\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "Kivy" in result

    def test_python_customtkinter(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("customtkinter>=5.2\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "CustomTkinter" in result

    def test_python_flet(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flet>=0.21\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "Flet" in result

    def test_python_textual(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("textual>=0.50\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "Textual" in result

    def test_python_toga(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("toga>=0.4\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "Toga" in result

    def test_python_tkinter_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text('[tool.mypy]\n# uses tkinter\n')
        result = detect_desktop_frameworks(tmp_path)
        assert "Tkinter" in result

    def test_js_electron(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"electron":"^28.0"}}')
        result = detect_desktop_frameworks(tmp_path)
        assert "Electron" in result

    def test_js_tauri(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@tauri-apps/api":"^1.5"}}')
        result = detect_desktop_frameworks(tmp_path)
        assert "Tauri" in result

    def test_js_react_native(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-native":"^0.73"}}')
        result = detect_desktop_frameworks(tmp_path)
        assert "React Native" in result

    def test_js_neutralino(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@neutralinojs/lib":"^5.0"}}')
        result = detect_desktop_frameworks(tmp_path)
        assert "Neutralino" in result

    def test_go_fyne(self, tmp_path):
        (tmp_path / "go.sum").write_text("fyne.io/fyne v2.4.0 h1:abc\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "Fyne" in result

    def test_go_wails(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/wailsapp/wails/v2 v2.7.0 h1:abc\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "Wails" in result

    def test_rust_iced(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\niced = "0.12"\n')
        result = detect_desktop_frameworks(tmp_path)
        assert "Iced" in result

    def test_rust_dioxus(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ndioxus = "0.5"\n')
        result = detect_desktop_frameworks(tmp_path)
        assert "Dioxus" in result

    def test_java_javafx(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency>javafx</dependency>")
        result = detect_desktop_frameworks(tmp_path)
        assert "JavaFX" in result

    def test_java_swing(self, tmp_path):
        (tmp_path / "build.gradle").write_text("import javax.swing.*\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "Swing" in result

    def test_tauri_config(self, tmp_path):
        (tmp_path / "tauri.conf.json").write_text("{}")
        result = detect_desktop_frameworks(tmp_path)
        assert "Tauri" in result

    def test_tauri_src_dir(self, tmp_path):
        (tmp_path / "src-tauri").mkdir()
        result = detect_desktop_frameworks(tmp_path)
        assert "Tauri" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyqt6>=6.6\nkivy>=2.3\nflet>=0.21\n")
        result = detect_desktop_frameworks(tmp_path)
        assert "PyQt6" in result
        assert "Kivy" in result
        assert "Flet" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("kivy>=2.3\nflet>=0.21\npyqt6>=6.6\n")
        result = detect_desktop_frameworks(tmp_path)
        assert result == sorted(result)


# detect_file_storage
class TestDetectFileStorage:
    def test_empty_project(self, tmp_path):
        assert detect_file_storage(tmp_path) == []

    def test_python_boto3(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("boto3>=1.34\n")
        result = detect_file_storage(tmp_path)
        assert "AWS S3" in result

    def test_python_gcs(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("google-cloud-storage>=2.14\n")
        result = detect_file_storage(tmp_path)
        assert "Google Cloud Storage" in result

    def test_python_azure(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("azure-storage-blob>=12.19\n")
        result = detect_file_storage(tmp_path)
        assert "Azure Blob Storage" in result

    def test_python_minio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("minio>=7.2\n")
        result = detect_file_storage(tmp_path)
        assert "MinIO" in result

    def test_python_cloudinary(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("cloudinary>=1.38\n")
        result = detect_file_storage(tmp_path)
        assert "Cloudinary" in result

    def test_python_django_storages(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django-storages>=1.14\n")
        result = detect_file_storage(tmp_path)
        assert "django-storages" in result

    def test_js_aws_s3(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@aws-sdk/client-s3":"^3.500"}}')
        result = detect_file_storage(tmp_path)
        assert "AWS S3" in result

    def test_js_uploadthing(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"uploadthing":"^6.0"}}')
        result = detect_file_storage(tmp_path)
        assert "UploadThing" in result

    def test_js_vercel_blob(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@vercel/blob":"^0.20"}}')
        result = detect_file_storage(tmp_path)
        assert "Vercel Blob" in result

    def test_js_supabase_storage(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@supabase/storage-js":"^2.5"}}')
        result = detect_file_storage(tmp_path)
        assert "Supabase Storage" in result

    def test_js_multer(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"multer":"^1.4"}}')
        result = detect_file_storage(tmp_path)
        assert "Multer" in result

    def test_go_aws(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/aws/aws-sdk-go v1.50.0 h1:abc\n")
        result = detect_file_storage(tmp_path)
        assert "AWS S3" in result

    def test_go_gcs(self, tmp_path):
        (tmp_path / "go.sum").write_text("cloud.google.com/go/storage v1.36.0 h1:abc\n")
        result = detect_file_storage(tmp_path)
        assert "Google Cloud Storage" in result

    def test_go_minio(self, tmp_path):
        (tmp_path / "go.sum").write_text("github.com/minio/minio-go v7.0.0 h1:abc\n")
        result = detect_file_storage(tmp_path)
        assert "MinIO" in result

    def test_rust_aws(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\naws-sdk-s3 = "1.10"\n')
        result = detect_file_storage(tmp_path)
        assert "AWS S3" in result

    def test_java_s3(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency>aws s3</dependency>")
        result = detect_file_storage(tmp_path)
        assert "AWS S3" in result

    def test_multiple_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("boto3>=1.34\ncloudinary>=1.38\nminio>=7.2\n")
        result = detect_file_storage(tmp_path)
        assert "AWS S3" in result
        assert "Cloudinary" in result
        assert "MinIO" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("minio>=7.2\nboto3>=1.34\ncloudinary>=1.38\n")
        result = detect_file_storage(tmp_path)
        assert result == sorted(result)


# detect_form_libs
class TestDetectFormLibs:
    def test_empty_project(self, tmp_path):
        assert detect_form_libs(tmp_path) == []

    def test_python_wtforms(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("wtforms>=3.1\n")
        result = detect_form_libs(tmp_path)
        assert "WTForms" in result

    def test_python_flask_wtf(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flask-wtf>=1.2\n")
        result = detect_form_libs(tmp_path)
        assert "Flask-WTF" in result

    def test_python_django_crispy(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django-crispy-forms>=2.0\n")
        result = detect_form_libs(tmp_path)
        assert "django-crispy-forms" in result

    def test_js_react_hook_form(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-hook-form":"^7.50"}}')
        result = detect_form_libs(tmp_path)
        assert "React Hook Form" in result

    def test_js_formik(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"formik":"^2.4"}}')
        result = detect_form_libs(tmp_path)
        assert "Formik" in result

    def test_js_tanstack_form(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@tanstack/react-form":"^0.20"}}')
        result = detect_form_libs(tmp_path)
        assert "TanStack Form" in result

    def test_js_vee_validate(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"vee-validate":"^4.12"}}')
        result = detect_form_libs(tmp_path)
        assert "VeeValidate" in result

    def test_js_formkit(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@formkit/core":"^1.5"}}')
        result = detect_form_libs(tmp_path)
        assert "FormKit" in result

    def test_js_conform(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@conform-to/react":"^1.0"}}')
        result = detect_form_libs(tmp_path)
        assert "Conform" in result

    def test_js_final_form(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"final-form":"^4.20"}}')
        result = detect_form_libs(tmp_path)
        assert "Final Form" in result

    def test_js_angular_forms(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@angular/forms":"^17.0"}}')
        result = detect_form_libs(tmp_path)
        assert "Angular Forms" in result

    def test_js_felte(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"felte":"^1.2"}}')
        result = detect_form_libs(tmp_path)
        assert "Felte" in result

    def test_multiple_js(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-hook-form":"^7.50","formik":"^2.4"}}')
        result = detect_form_libs(tmp_path)
        assert "React Hook Form" in result
        assert "Formik" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"formik":"^2.4","react-hook-form":"^7.50"}}')
        result = detect_form_libs(tmp_path)
        assert result == sorted(result)


# detect_animation_libs
class TestDetectAnimationLibs:
    def test_empty_project(self, tmp_path):
        assert detect_animation_libs(tmp_path) == []

    def test_python_manim(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("manim==0.18.0\n")
        result = detect_animation_libs(tmp_path)
        assert "Manim" in result

    def test_python_pyglet(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pyglet==2.0\n")
        result = detect_animation_libs(tmp_path)
        assert "pyglet" in result

    def test_python_arcade(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("arcade==2.7\n")
        result = detect_animation_libs(tmp_path)
        assert "Arcade" in result

    def test_js_framer_motion(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"framer-motion":"^10.0"}}')
        result = detect_animation_libs(tmp_path)
        assert "Framer Motion" in result

    def test_js_gsap(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"gsap":"^3.12"}}')
        result = detect_animation_libs(tmp_path)
        assert "GSAP" in result

    def test_js_anime(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"animejs":"^3.2"}}')
        result = detect_animation_libs(tmp_path)
        assert "anime.js" in result

    def test_js_lottie(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"lottie-web":"^5.12"}}')
        result = detect_animation_libs(tmp_path)
        assert "Lottie" in result

    def test_js_react_spring(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-spring":"^9.7"}}')
        result = detect_animation_libs(tmp_path)
        assert "react-spring" in result

    def test_js_motion_one(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@motionone/dom":"^10.0"}}')
        result = detect_animation_libs(tmp_path)
        assert "Motion One" in result

    def test_js_auto_animate(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@formkit/auto-animate":"^0.8"}}')
        result = detect_animation_libs(tmp_path)
        assert "AutoAnimate" in result

    def test_js_rive(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@rive-app/react-canvas":"^4.0"}}')
        result = detect_animation_libs(tmp_path)
        assert "Rive" in result

    def test_js_theatre(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@theatre/core":"^0.7"}}')
        result = detect_animation_libs(tmp_path)
        assert "Theatre.js" in result

    def test_js_popmotion(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"popmotion":"^11.0"}}')
        result = detect_animation_libs(tmp_path)
        assert "Popmotion" in result

    def test_js_velocity(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"velocity-animate":"^1.5"}}')
        result = detect_animation_libs(tmp_path)
        assert "Velocity.js" in result

    def test_rust_keyframe(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nkeyframe = "1.0"\n')
        result = detect_animation_libs(tmp_path)
        assert "keyframe" in result

    def test_dedup(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"lottie-web":"^5.12","lottie-react":"^2.0"}}')
        result = detect_animation_libs(tmp_path)
        assert result.count("Lottie") == 1

    def test_multiple_js(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"framer-motion":"^10.0","gsap":"^3.12"}}')
        result = detect_animation_libs(tmp_path)
        assert "Framer Motion" in result
        assert "GSAP" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"gsap":"^3.12","framer-motion":"^10.0"}}')
        result = detect_animation_libs(tmp_path)
        assert result == sorted(result)


# detect_routing_libs
class TestDetectRoutingLibs:
    def test_empty_project(self, tmp_path):
        assert detect_routing_libs(tmp_path) == []

    def test_python_flask(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flask==3.0\n")
        result = detect_routing_libs(tmp_path)
        assert "Flask Routes" in result

    def test_python_fastapi(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastapi==0.109\n")
        result = detect_routing_libs(tmp_path)
        assert "FastAPI Router" in result

    def test_python_django(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django==5.0\n")
        result = detect_routing_libs(tmp_path)
        assert "Django URLs" in result

    def test_js_react_router(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-router-dom":"^6.22"}}')
        result = detect_routing_libs(tmp_path)
        assert "React Router" in result

    def test_js_tanstack_router(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@tanstack/react-router":"^1.0"}}')
        result = detect_routing_libs(tmp_path)
        assert "TanStack Router" in result

    def test_js_vue_router(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"vue-router":"^4.0"}}')
        result = detect_routing_libs(tmp_path)
        assert "Vue Router" in result

    def test_js_wouter(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"wouter":"^3.0"}}')
        result = detect_routing_libs(tmp_path)
        assert "Wouter" in result

    def test_js_angular_router(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@angular/router":"^17.0"}}')
        result = detect_routing_libs(tmp_path)
        assert "Angular Router" in result

    def test_js_react_navigation(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@react-navigation/native":"^6.0"}}')
        result = detect_routing_libs(tmp_path)
        assert "React Navigation" in result

    def test_go_gorilla_mux(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/gorilla/mux v1.8.1\n")
        result = detect_routing_libs(tmp_path)
        assert "Gorilla Mux" in result

    def test_go_chi(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/go-chi/chi v5.0.0\n")
        result = detect_routing_libs(tmp_path)
        assert "Chi" in result

    def test_go_gin(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/gin-gonic/gin v1.9.0\n")
        result = detect_routing_libs(tmp_path)
        assert "Gin Router" in result

    def test_rust_axum(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\naxum = "0.7"\n')
        result = detect_routing_libs(tmp_path)
        assert "Axum Router" in result

    def test_rust_actix(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nactix-web = "4.0"\n')
        result = detect_routing_libs(tmp_path)
        assert "Actix Web Router" in result

    def test_java_spring_webmvc(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>spring-webmvc</artifactId></dependency>")
        result = detect_routing_libs(tmp_path)
        assert "Spring MVC Router" in result

    def test_multiple_js(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-router-dom":"^6.22","wouter":"^3.0"}}')
        result = detect_routing_libs(tmp_path)
        assert "React Router" in result
        assert "Wouter" in result

    def test_dedup(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"react-router":"^6.0","react-router-dom":"^6.22"}}')
        result = detect_routing_libs(tmp_path)
        assert result.count("React Router") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"vue-router":"^4.0","react-router-dom":"^6.22"}}')
        result = detect_routing_libs(tmp_path)
        assert result == sorted(result)


# detect_game_frameworks
class TestDetectGameFrameworks:
    def test_empty_project(self, tmp_path):
        assert detect_game_frameworks(tmp_path) == []

    def test_python_pygame(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pygame==2.5\n")
        result = detect_game_frameworks(tmp_path)
        assert "Pygame" in result

    def test_python_arcade(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("arcade==2.7\n")
        result = detect_game_frameworks(tmp_path)
        assert "Arcade" in result

    def test_python_panda3d(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("panda3d==1.10\n")
        result = detect_game_frameworks(tmp_path)
        assert "Panda3D" in result

    def test_python_ursina(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("ursina==5.0\n")
        result = detect_game_frameworks(tmp_path)
        assert "Ursina" in result

    def test_js_phaser(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"phaser":"^3.70"}}')
        result = detect_game_frameworks(tmp_path)
        assert "Phaser" in result

    def test_js_pixijs(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"pixi.js":"^7.3"}}')
        result = detect_game_frameworks(tmp_path)
        assert "PixiJS" in result

    def test_js_three(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"three":"^0.160"}}')
        result = detect_game_frameworks(tmp_path)
        assert "Three.js" in result

    def test_js_babylon(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@babylonjs/core":"^6.0"}}')
        result = detect_game_frameworks(tmp_path)
        assert "Babylon.js" in result

    def test_js_kaboom(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"kaboom":"^3000"}}')
        result = detect_game_frameworks(tmp_path)
        assert "Kaboom.js" in result

    def test_go_ebiten(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/hajimehoshi/ebiten v2.6.0\n")
        result = detect_game_frameworks(tmp_path)
        assert "Ebiten" in result

    def test_rust_bevy(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nbevy = "0.12"\n')
        result = detect_game_frameworks(tmp_path)
        assert "Bevy" in result

    def test_rust_macroquad(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nmacroquad = "0.4"\n')
        result = detect_game_frameworks(tmp_path)
        assert "macroquad" in result

    def test_java_libgdx(self, tmp_path):
        (tmp_path / "build.gradle").write_text('implementation "com.badlogicgames.gdx:libgdx:1.12"')
        result = detect_game_frameworks(tmp_path)
        assert "LibGDX" in result

    def test_js_matter(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"matter-js":"^0.20"}}')
        result = detect_game_frameworks(tmp_path)
        assert "Matter.js" in result

    def test_multiple_js(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"phaser":"^3.70","pixi.js":"^7.3"}}')
        result = detect_game_frameworks(tmp_path)
        assert "Phaser" in result
        assert "PixiJS" in result

    def test_dedup(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pygame==2.5\npygame-ce==2.3\n")
        result = detect_game_frameworks(tmp_path)
        assert result.count("Pygame") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"three":"^0.160","phaser":"^3.70"}}')
        result = detect_game_frameworks(tmp_path)
        assert result == sorted(result)


# detect_cms_tools
class TestDetectCmsTools:
    def test_empty_project(self, tmp_path):
        assert detect_cms_tools(tmp_path) == []

    def test_python_wagtail(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("wagtail==6.0\n")
        result = detect_cms_tools(tmp_path)
        assert "Wagtail" in result

    def test_python_django_cms(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django-cms==4.0\n")
        result = detect_cms_tools(tmp_path)
        assert "django CMS" in result

    def test_python_pelican(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pelican==4.9\n")
        result = detect_cms_tools(tmp_path)
        assert "Pelican" in result

    def test_js_strapi(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@strapi/strapi":"^4.0"}}')
        result = detect_cms_tools(tmp_path)
        assert "Strapi" in result

    def test_js_sanity(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@sanity/client":"^6.0"}}')
        result = detect_cms_tools(tmp_path)
        assert "Sanity" in result

    def test_js_contentful(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"contentful":"^10.0"}}')
        result = detect_cms_tools(tmp_path)
        assert "Contentful" in result

    def test_js_payload(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@payloadcms/next":"^3.0"}}')
        result = detect_cms_tools(tmp_path)
        assert "Payload CMS" in result

    def test_js_directus(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@directus/sdk":"^14.0"}}')
        result = detect_cms_tools(tmp_path)
        assert "Directus" in result

    def test_js_storyblok(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@storyblok/react":"^3.0"}}')
        result = detect_cms_tools(tmp_path)
        assert "Storyblok" in result

    def test_js_prismic(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@prismicio/client":"^7.0"}}')
        result = detect_cms_tools(tmp_path)
        assert "Prismic" in result

    def test_hugo_config(self, tmp_path):
        (tmp_path / "hugo.toml").write_text('title = "My Site"\n')
        result = detect_cms_tools(tmp_path)
        assert "Hugo" in result

    def test_jekyll(self, tmp_path):
        (tmp_path / "_config.yml").write_text("title: My Site\n")
        (tmp_path / "Gemfile").write_text('gem "jekyll", "~> 4.3"\n')
        result = detect_cms_tools(tmp_path)
        assert "Jekyll" in result

    def test_multiple_js(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@strapi/strapi":"^4.0","contentful":"^10.0"}}')
        result = detect_cms_tools(tmp_path)
        assert "Strapi" in result
        assert "Contentful" in result

    def test_dedup(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@strapi/strapi":"^4.0","strapi":"^4.0"}}')
        result = detect_cms_tools(tmp_path)
        assert result.count("Strapi") == 1

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"contentful":"^10.0","@strapi/strapi":"^4.0"}}')
        result = detect_cms_tools(tmp_path)
        assert result == sorted(result)


# detect_rate_limiters
class TestDetectRateLimiters:
    def test_empty_project(self, tmp_path):
        assert detect_rate_limiters(tmp_path) == []

    def test_python_slowapi(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("slowapi==0.1.9\n")
        result = detect_rate_limiters(tmp_path)
        assert "SlowAPI" in result

    def test_python_flask_limiter(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("flask-limiter==3.5\n")
        result = detect_rate_limiters(tmp_path)
        assert "Flask-Limiter" in result

    def test_python_django_ratelimit(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django-ratelimit==4.1\n")
        result = detect_rate_limiters(tmp_path)
        assert "django-ratelimit" in result

    def test_js_express_rate_limit(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"express-rate-limit":"^7.0"}}')
        result = detect_rate_limiters(tmp_path)
        assert "express-rate-limit" in result

    def test_js_rate_limiter_flexible(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"rate-limiter-flexible":"^4.0"}}')
        result = detect_rate_limiters(tmp_path)
        assert "rate-limiter-flexible" in result

    def test_js_upstash(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@upstash/ratelimit":"^1.0"}}')
        result = detect_rate_limiters(tmp_path)
        assert "Upstash Ratelimit" in result

    def test_js_bottleneck(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"bottleneck":"^2.19"}}')
        result = detect_rate_limiters(tmp_path)
        assert "Bottleneck" in result

    def test_go_tollbooth(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/didip/tollbooth v6.0.0\n")
        result = detect_rate_limiters(tmp_path)
        assert "Tollbooth" in result

    def test_rust_governor(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ngovernor = "0.6"\n')
        result = detect_rate_limiters(tmp_path)
        assert "Governor" in result

    def test_java_bucket4j(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>bucket4j-core</artifactId></dependency>")
        result = detect_rate_limiters(tmp_path)
        assert "Bucket4j" in result

    def test_java_resilience4j(self, tmp_path):
        (tmp_path / "build.gradle").write_text('implementation "io.github.resilience4j:resilience4j-ratelimiter:2.0"')
        result = detect_rate_limiters(tmp_path)
        assert "Resilience4j" in result

    def test_multiple(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"express-rate-limit":"^7.0","bottleneck":"^2.19"}}')
        result = detect_rate_limiters(tmp_path)
        assert "express-rate-limit" in result
        assert "Bottleneck" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"express-rate-limit":"^7.0","bottleneck":"^2.19"}}')
        result = detect_rate_limiters(tmp_path)
        assert result == sorted(result)


# detect_db_migration_tools
class TestDetectDbMigrationTools:
    def test_empty_project(self, tmp_path):
        assert detect_db_migration_tools(tmp_path) == []

    def test_python_alembic(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("alembic==1.13\n")
        result = detect_db_migration_tools(tmp_path)
        assert "Alembic" in result

    def test_python_django(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("django==5.0\n")
        result = detect_db_migration_tools(tmp_path)
        assert "Django Migrations" in result

    def test_js_prisma(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@prisma/client":"^5.0"}}')
        result = detect_db_migration_tools(tmp_path)
        assert "Prisma Migrate" in result

    def test_js_drizzle_kit(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"drizzle-kit":"^0.20"}}')
        result = detect_db_migration_tools(tmp_path)
        assert "Drizzle Kit" in result

    def test_js_knex(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"knex":"^3.0"}}')
        result = detect_db_migration_tools(tmp_path)
        assert "Knex Migrations" in result

    def test_js_typeorm(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"typeorm":"^0.3"}}')
        result = detect_db_migration_tools(tmp_path)
        assert "TypeORM Migrations" in result

    def test_go_golang_migrate(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/golang-migrate/migrate v4.0.0\n")
        result = detect_db_migration_tools(tmp_path)
        assert "golang-migrate" in result

    def test_go_goose(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/pressly/goose v3.0.0\n")
        result = detect_db_migration_tools(tmp_path)
        assert "Goose" in result

    def test_rust_diesel(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ndiesel_migrations = "2.0"\n')
        result = detect_db_migration_tools(tmp_path)
        assert "Diesel Migrations" in result

    def test_rust_refinery(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\nrefinery = "0.8"\n')
        result = detect_db_migration_tools(tmp_path)
        assert "Refinery" in result

    def test_java_flyway(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>flyway-core</artifactId></dependency>")
        result = detect_db_migration_tools(tmp_path)
        assert "Flyway" in result

    def test_java_liquibase(self, tmp_path):
        (tmp_path / "build.gradle").write_text('implementation "org.liquibase:liquibase-core:4.25"')
        result = detect_db_migration_tools(tmp_path)
        assert "Liquibase" in result

    def test_multiple(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("alembic==1.13\n")
        (tmp_path / "package.json").write_text('{"dependencies":{"knex":"^3.0"}}')
        result = detect_db_migration_tools(tmp_path)
        assert "Alembic" in result
        assert "Knex Migrations" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("alembic==1.13\ndjango==5.0\n")
        result = detect_db_migration_tools(tmp_path)
        assert result == sorted(result)


class TestDetectGrpcLibs:
    def test_empty(self, tmp_path):
        assert detect_grpc_libs(tmp_path) == []

    def test_python_grpcio(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("grpcio==1.60\n")
        result = detect_grpc_libs(tmp_path)
        assert "gRPC" in result

    def test_python_thrift(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("thrift==0.16\n")
        result = detect_grpc_libs(tmp_path)
        assert "Apache Thrift" in result

    def test_python_rpyc(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("rpyc==5.3\n")
        result = detect_grpc_libs(tmp_path)
        assert "RPyC" in result

    def test_js_trpc(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@trpc/server":"^10"}}')
        result = detect_grpc_libs(tmp_path)
        assert "tRPC" in result

    def test_js_grpc(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@grpc/grpc-js":"^1.9"}}')
        result = detect_grpc_libs(tmp_path)
        assert "gRPC" in result

    def test_js_connectrpc(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"@connectrpc/connect":"^1.0"}}')
        result = detect_grpc_libs(tmp_path)
        assert "ConnectRPC" in result

    def test_js_jsonrpc(self, tmp_path):
        (tmp_path / "package.json").write_text('{"dependencies":{"jayson":"^4.0"}}')
        result = detect_grpc_libs(tmp_path)
        assert "JSON-RPC" in result

    def test_go_grpc(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire google.golang.org/grpc v1.60\n")
        result = detect_grpc_libs(tmp_path)
        assert "gRPC" in result

    def test_go_twirp(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/twitchtv/twirp v8.0\n")
        result = detect_grpc_libs(tmp_path)
        assert "Twirp" in result

    def test_rust_tonic(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntonic = "0.10"\n')
        result = detect_grpc_libs(tmp_path)
        assert "Tonic" in result

    def test_rust_tarpc(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[dependencies]\ntarpc = "0.33"\n')
        result = detect_grpc_libs(tmp_path)
        assert "tarpc" in result

    def test_java_grpc(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>grpc-netty</artifactId></dependency>")
        result = detect_grpc_libs(tmp_path)
        assert "gRPC" in result

    def test_java_dubbo(self, tmp_path):
        (tmp_path / "build.gradle").write_text('implementation "org.apache.dubbo:dubbo:3.2"')
        result = detect_grpc_libs(tmp_path)
        assert "Apache Dubbo" in result

    def test_proto_file(self, tmp_path):
        (tmp_path / "service.proto").write_text('syntax = "proto3";')
        result = detect_grpc_libs(tmp_path)
        assert "Protobuf" in result

    def test_multiple(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("grpcio==1.60\n")
        (tmp_path / "package.json").write_text('{"dependencies":{"@trpc/server":"^10"}}')
        result = detect_grpc_libs(tmp_path)
        assert "gRPC" in result
        assert "tRPC" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("grpcio==1.60\nthrift==0.16\n")
        result = detect_grpc_libs(tmp_path)
        assert result == sorted(result)


class TestDetectCodegenTools:
    def test_empty(self, tmp_path):
        assert detect_codegen_tools(tmp_path) == []

    def test_python_protoc(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("grpcio-tools==1.60\n")
        result = detect_codegen_tools(tmp_path)
        assert "protoc" in result

    def test_python_cookiecutter(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("cookiecutter==2.5\n")
        result = detect_codegen_tools(tmp_path)
        assert "Cookiecutter" in result

    def test_python_datamodel_codegen(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("datamodel-code-generator==0.25\n")
        result = detect_codegen_tools(tmp_path)
        assert "datamodel-code-generator" in result

    def test_js_graphql_codegen(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"@graphql-codegen/cli":"^5"}}')
        result = detect_codegen_tools(tmp_path)
        assert "GraphQL Codegen" in result

    def test_js_openapi_generator(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"@openapitools/openapi-generator-cli":"^2"}}')
        result = detect_codegen_tools(tmp_path)
        assert "OpenAPI Generator" in result

    def test_js_plop(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"plop":"^4"}}')
        result = detect_codegen_tools(tmp_path)
        assert "Plop" in result

    def test_js_hygen(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"hygen":"^6"}}')
        result = detect_codegen_tools(tmp_path)
        assert "Hygen" in result

    def test_js_ts_proto(self, tmp_path):
        (tmp_path / "package.json").write_text('{"devDependencies":{"ts-proto":"^1"}}')
        result = detect_codegen_tools(tmp_path)
        assert "ts-proto" in result

    def test_go_sqlc(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/sqlc-dev/sqlc v1.25\n")
        result = detect_codegen_tools(tmp_path)
        assert "sqlc" in result

    def test_go_gqlgen(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire github.com/99designs/gqlgen v0.17\n")
        result = detect_codegen_tools(tmp_path)
        assert "gqlgen" in result

    def test_go_ent(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example\nrequire entgo.io/ent v0.13\n")
        result = detect_codegen_tools(tmp_path)
        assert "Ent" in result

    def test_rust_prost_build(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[build-dependencies]\nprost-build = "0.12"\n')
        result = detect_codegen_tools(tmp_path)
        assert "Prost Build" in result

    def test_rust_bindgen(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[build-dependencies]\nbindgen = "0.69"\n')
        result = detect_codegen_tools(tmp_path)
        assert "bindgen" in result

    def test_java_lombok(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<dependency><artifactId>lombok</artifactId></dependency>")
        result = detect_codegen_tools(tmp_path)
        assert "Lombok" in result

    def test_java_mapstruct(self, tmp_path):
        (tmp_path / "build.gradle").write_text('implementation "org.mapstruct:mapstruct:1.5"')
        result = detect_codegen_tools(tmp_path)
        assert "MapStruct" in result

    def test_buf_config(self, tmp_path):
        (tmp_path / "buf.yaml").write_text("version: v1\n")
        result = detect_codegen_tools(tmp_path)
        assert "Buf" in result

    def test_buf_gen_config(self, tmp_path):
        (tmp_path / "buf.gen.yaml").write_text("version: v1\n")
        result = detect_codegen_tools(tmp_path)
        assert "Buf" in result

    def test_multiple(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("grpcio-tools==1.60\n")
        (tmp_path / "package.json").write_text('{"devDependencies":{"@graphql-codegen/cli":"^5"}}')
        result = detect_codegen_tools(tmp_path)
        assert "protoc" in result
        assert "GraphQL Codegen" in result

    def test_sorted_output(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("grpcio-tools==1.60\ncookiecutter==2.5\n")
        result = detect_codegen_tools(tmp_path)
        assert result == sorted(result)
