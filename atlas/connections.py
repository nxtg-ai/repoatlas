"""Cross-project intelligence — finds shared deps, version mismatches, reuse candidates."""
from __future__ import annotations

from collections import defaultdict

from atlas.models import Connection, Project


def find_connections(projects: list[Project]) -> list[Connection]:
    """Analyze cross-project patterns and return connections."""
    connections: list[Connection] = []
    connections.extend(_find_shared_deps(projects))
    connections.extend(_find_shared_frameworks(projects))
    connections.extend(_find_version_mismatches(projects))
    connections.extend(_find_health_gaps(projects))
    connections.extend(_find_database_patterns(projects))
    connections.extend(_find_infra_patterns(projects))
    connections.extend(_find_security_patterns(projects))
    connections.extend(_find_quality_patterns(projects))
    connections.extend(_find_ai_patterns(projects))
    connections.extend(_find_testing_patterns(projects))
    connections.extend(_find_package_manager_patterns(projects))
    connections.extend(_find_license_patterns(projects))
    connections.extend(_find_docs_artifact_patterns(projects))
    connections.extend(_find_ci_config_patterns(projects))
    connections.extend(_find_runtime_version_patterns(projects))
    connections.extend(_find_build_tool_patterns(projects))
    connections.extend(_find_api_spec_patterns(projects))
    connections.extend(_find_monitoring_patterns(projects))
    connections.extend(_find_auth_patterns(projects))
    connections.extend(_find_messaging_patterns(projects))
    connections.extend(_find_deploy_target_patterns(projects))
    connections.extend(_find_state_management_patterns(projects))
    connections.extend(_find_css_framework_patterns(projects))
    connections.extend(_find_bundler_patterns(projects))
    connections.extend(_find_orm_patterns(projects))
    connections.extend(_find_i18n_patterns(projects))
    connections.extend(_find_validation_patterns(projects))
    connections.extend(_find_logging_patterns(projects))
    connections.extend(_find_container_orchestration_patterns(projects))
    connections.extend(_find_cloud_provider_patterns(projects))
    connections.extend(_find_task_queue_patterns(projects))
    connections.extend(_find_search_engine_patterns(projects))
    connections.extend(_find_feature_flag_patterns(projects))
    connections.extend(_find_http_client_patterns(projects))
    connections.extend(_find_doc_generator_patterns(projects))
    connections.extend(_find_cli_framework_patterns(projects))
    connections.extend(_find_config_tool_patterns(projects))
    connections.extend(_find_caching_patterns(projects))
    connections.extend(_find_template_engine_patterns(projects))
    connections.extend(_find_serialization_patterns(projects))
    connections.extend(_find_di_patterns(projects))
    connections.extend(_find_websocket_patterns(projects))
    connections.extend(_find_graphql_patterns(projects))
    connections.extend(_find_event_streaming_patterns(projects))
    connections.extend(_find_payment_patterns(projects))
    connections.extend(_find_date_lib_patterns(projects))
    connections.extend(_find_image_lib_patterns(projects))
    connections.extend(_find_data_viz_patterns(projects))
    connections.extend(_find_geo_patterns(projects))
    connections.extend(_find_media_patterns(projects))
    connections.extend(_find_math_patterns(projects))
    connections.extend(_find_async_patterns(projects))
    connections.extend(_find_crypto_patterns(projects))
    connections.extend(_find_pdf_patterns(projects))
    return connections


def _find_shared_deps(projects: list[Project]) -> list[Connection]:
    """Find dependencies used by 2+ projects."""
    dep_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for dep_name in proj.tech_stack.key_deps:
            dep_to_projects[dep_name].append(proj.name)

    connections = []
    important_deps = {
        "fastapi", "react", "next", "express", "sqlalchemy",
        "pydantic", "anthropic", "openai", "django", "flask",
        "pytest", "vitest", "jest", "tailwindcss", "drizzle-orm",
        "prisma", "redis", "celery",
    }

    for dep, projs in sorted(dep_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2 and dep.lower() in important_deps:
            connections.append(Connection(
                type="shared_dep",
                detail=f"{dep} used across {len(projs)} projects",
                projects=projs,
                severity="info",
            ))

    return connections[:10]


def _find_shared_frameworks(projects: list[Project]) -> list[Connection]:
    """Find framework patterns across projects."""
    fw_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for fw in proj.tech_stack.frameworks:
            fw_to_projects[fw].append(proj.name)

    connections = []
    for fw, projs in sorted(fw_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 3:
            connections.append(Connection(
                type="shared_framework",
                detail=f"{fw} in {len(projs)} projects — standardize patterns",
                projects=projs,
                severity="info",
            ))

    return connections[:5]


def _find_version_mismatches(projects: list[Project]) -> list[Connection]:
    """Find dependency version inconsistencies."""
    dep_versions: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))

    for proj in projects:
        for dep, version in proj.tech_stack.key_deps.items():
            dep_versions[dep][version].append(proj.name)

    connections = []
    for dep, versions in dep_versions.items():
        if len(versions) >= 2:
            version_summary = ", ".join(
                f"{v} ({', '.join(ps)})" for v, ps in versions.items()
            )
            all_projects = [p for ps in versions.values() for p in ps]
            connections.append(Connection(
                type="version_mismatch",
                detail=f"{dep}: {version_summary}",
                projects=all_projects,
                severity="warning",
            ))

    return connections[:8]


def _find_health_gaps(projects: list[Project]) -> list[Connection]:
    """Find projects with critical health issues."""
    connections = []

    no_tests = [p.name for p in projects if p.test_file_count == 0 and p.source_file_count > 5]
    if no_tests:
        connections.append(Connection(
            type="health_gap",
            detail=f"{len(no_tests)} projects have zero tests",
            projects=no_tests,
            severity="critical",
        ))

    dirty = [p.name for p in projects if p.git_info.uncommitted_changes > 10]
    if dirty:
        connections.append(Connection(
            type="health_gap",
            detail=f"{len(dirty)} projects have 10+ uncommitted changes",
            projects=dirty,
            severity="warning",
        ))

    stale = [
        p.name for p in projects
        if p.git_info.total_commits > 0 and p.git_info.total_commits < 5
        and p.source_file_count > 5
    ]
    if stale:
        connections.append(Connection(
            type="health_gap",
            detail=f"{len(stale)} projects appear stale (<5 commits)",
            projects=stale,
            severity="warning",
        ))

    return connections


def _find_database_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project database and data store patterns."""
    connections: list[Connection] = []
    db_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for db in proj.tech_stack.databases:
            db_to_projects[db].append(proj.name)

    # Shared databases (2+ projects)
    for db, projs in sorted(db_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_database",
                detail=f"{db} used across {len(projs)} projects — unify connection patterns",
                projects=projs,
                severity="info",
            ))

    # Relational DB divergence
    relational_dbs = {"PostgreSQL", "MySQL", "SQLite", "CockroachDB", "PlanetScale", "Supabase"}
    rel_divergence: dict[str, set[str]] = {}
    for p in projects:
        for db in p.tech_stack.databases:
            if db in relational_dbs:
                rel_divergence.setdefault(db, set()).add(p.name)

    # Only flag if 2+ different relational DBs across portfolio (excluding SQLite for dev)
    prod_rel = {k: v for k, v in rel_divergence.items() if k != "SQLite"}
    if len(prod_rel) >= 2:
        detail_parts = [f"{db} ({', '.join(sorted(projs))})" for db, projs in prod_rel.items()]
        all_projects = sorted({p for projs in prod_rel.values() for p in projs})
        connections.append(Connection(
            type="database_divergence",
            detail=f"Multiple relational DBs: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Vector DB divergence
    vector_dbs = {"pgvector", "ChromaDB", "Pinecone", "Qdrant", "Weaviate"}
    vec_divergence: dict[str, set[str]] = {}
    for p in projects:
        for db in p.tech_stack.databases:
            if db in vector_dbs:
                vec_divergence.setdefault(db, set()).add(p.name)

    if len(vec_divergence) >= 2:
        detail_parts = [f"{db} ({', '.join(sorted(projs))})" for db, projs in vec_divergence.items()]
        all_projects = sorted({p for projs in vec_divergence.values() for p in projs})
        connections.append(Connection(
            type="database_divergence",
            detail=f"Multiple vector DBs: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Message broker divergence
    brokers = {"RabbitMQ", "Kafka"}
    broker_divergence: dict[str, set[str]] = {}
    for p in projects:
        for db in p.tech_stack.databases:
            if db in brokers:
                broker_divergence.setdefault(db, set()).add(p.name)

    if len(broker_divergence) >= 2:
        detail_parts = [f"{db} ({', '.join(sorted(projs))})" for db, projs in broker_divergence.items()]
        all_projects = sorted({p for projs in broker_divergence.values() for p in projs})
        connections.append(Connection(
            type="database_divergence",
            detail=f"Multiple message brokers: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Database gap — web/API projects with no database
    web_frameworks = {"FastAPI", "Django", "Flask", "Express", "Next.js", "Rails", "Spring Boot"}
    no_db = [
        p.name for p in projects
        if not p.tech_stack.databases
        and any(fw in web_frameworks for fw in p.tech_stack.frameworks)
    ]
    if no_db:
        connections.append(Connection(
            type="database_gap",
            detail=f"{len(no_db)} web/API projects have no database detected",
            projects=no_db,
            severity="warning",
        ))

    return connections[:10]


def _find_infra_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project infrastructure patterns."""
    connections: list[Connection] = []
    infra_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for item in proj.tech_stack.infrastructure:
            infra_to_projects[item].append(proj.name)

    # Shared infrastructure (2+ projects)
    for item, projs in sorted(infra_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_infra",
                detail=f"{item} used across {len(projs)} projects — standardize config",
                projects=projs,
                severity="info",
            ))

    # Platform divergence — multiple hosting platforms
    hosting = {"Vercel", "Netlify", "Fly.io", "Render", "Cloudflare Workers", "Serverless Framework"}
    host_found: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for item in proj.tech_stack.infrastructure:
            if item in hosting:
                host_found[proj.name].append(item)
    multi_host = {p: hosts for p, hosts in host_found.items() if len(hosts) >= 2}
    if multi_host:
        for proj_name, hosts in multi_host.items():
            connections.append(Connection(
                type="infra_divergence",
                detail=f"{proj_name} uses {', '.join(hosts)} — consolidate hosting",
                projects=[proj_name],
                severity="warning",
            ))

    # CI divergence — multiple CI systems across portfolio
    ci_systems = {"GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"}
    ci_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for item in proj.tech_stack.infrastructure:
            if item in ci_systems:
                ci_to_projects[item].append(proj.name)
    if len(ci_to_projects) >= 2:
        detail_parts = [f"{ci} ({', '.join(ps[:3])})" for ci, ps in ci_to_projects.items()]
        all_ci_projects = list({p for ps in ci_to_projects.values() for p in ps})
        connections.append(Connection(
            type="infra_divergence",
            detail=f"Multiple CI systems: {', '.join(detail_parts)} — standardize",
            projects=all_ci_projects,
            severity="warning",
        ))

    # No CI detected
    has_ci = {p for ps in ci_to_projects.values() for p in ps}
    no_ci = [p.name for p in projects if p.name not in has_ci and p.source_file_count > 5]
    if no_ci:
        connections.append(Connection(
            type="infra_gap",
            detail=f"{len(no_ci)} projects have no CI/CD detected",
            projects=no_ci,
            severity="critical",
        ))

    # Cloud usage without IaC
    iac_tools = {"Terraform", "Pulumi", "AWS CDK"}
    cloud_providers = {"AWS", "GCP", "Azure"}
    has_iac = any(
        item in iac_tools
        for proj in projects
        for item in proj.tech_stack.infrastructure
    )
    cloud_projects = [
        p.name for p in projects
        if any(item in cloud_providers for item in p.tech_stack.infrastructure)
    ]
    if cloud_projects and not has_iac:
        connections.append(Connection(
            type="infra_gap",
            detail=f"{len(cloud_projects)} projects use cloud services without IaC — add Terraform/Pulumi",
            projects=cloud_projects,
            severity="warning",
        ))

    # Docker without orchestration
    has_docker = [
        p.name for p in projects
        if "Docker" in p.tech_stack.infrastructure
    ]
    has_orch = any(
        item in {"Kubernetes", "Docker Compose"}
        for proj in projects
        for item in proj.tech_stack.infrastructure
    )
    if len(has_docker) >= 3 and not has_orch:
        connections.append(Connection(
            type="infra_gap",
            detail=f"{len(has_docker)} projects use Docker without orchestration — consider Compose/K8s",
            projects=has_docker,
            severity="info",
        ))

    return connections[:10]


def _find_security_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project security patterns."""
    connections: list[Connection] = []
    sec_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for tool in proj.tech_stack.security_tools:
            sec_to_projects[tool].append(proj.name)

    # Shared security tools (2+ projects)
    for tool, projs in sorted(sec_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_security",
                detail=f"{tool} used across {len(projs)} projects — standardize config",
                projects=projs,
                severity="info",
            ))

    # No security tooling at all
    no_security = [p.name for p in projects if not p.tech_stack.security_tools and p.source_file_count > 5]
    if no_security:
        connections.append(Connection(
            type="security_gap",
            detail=f"{len(no_security)} projects have no security tooling",
            projects=no_security,
            severity="critical",
        ))

    # Missing dependency scanning
    dep_scanners = {"Dependabot", "Renovate", "Snyk", "pip-audit", "Safety"}
    no_dep_scan = [
        p.name for p in projects
        if p.tech_stack.security_tools
        and not any(t in dep_scanners for t in p.tech_stack.security_tools)
        and p.source_file_count > 5
    ]
    if no_dep_scan:
        connections.append(Connection(
            type="security_gap",
            detail=f"{len(no_dep_scan)} projects lack dependency scanning — add Dependabot/Renovate",
            projects=no_dep_scan,
            severity="warning",
        ))

    # Missing secret scanning
    secret_scanners = {"Gitleaks", "detect-secrets", "SOPS"}
    no_secret_scan = [
        p.name for p in projects
        if p.tech_stack.security_tools
        and not any(t in secret_scanners for t in p.tech_stack.security_tools)
        and p.source_file_count > 5
    ]
    if no_secret_scan:
        connections.append(Connection(
            type="security_gap",
            detail=f"{len(no_secret_scan)} projects lack secret scanning — add Gitleaks/detect-secrets",
            projects=no_secret_scan,
            severity="warning",
        ))

    # Dep scanner divergence — multiple dep scanners across portfolio
    dep_scan_tools = {"Dependabot", "Renovate", "Snyk"}
    dep_scan_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for tool in proj.tech_stack.security_tools:
            if tool in dep_scan_tools:
                dep_scan_to_projects[tool].append(proj.name)
    if len(dep_scan_to_projects) >= 2:
        detail_parts = [f"{tool} ({', '.join(ps[:3])})" for tool, ps in dep_scan_to_projects.items()]
        all_projects = list({p for ps in dep_scan_to_projects.values() for p in ps})
        connections.append(Connection(
            type="security_divergence",
            detail=f"Multiple dep scanners: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    return connections[:10]


def _find_quality_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project code quality patterns."""
    connections: list[Connection] = []
    qt_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for tool in proj.tech_stack.quality_tools:
            qt_to_projects[tool].append(proj.name)

    # Shared quality tools (2+ projects)
    for tool, projs in sorted(qt_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_quality",
                detail=f"{tool} used across {len(projs)} projects — share config",
                projects=projs,
                severity="info",
            ))

    # No quality tooling at all
    no_quality = [p.name for p in projects if not p.tech_stack.quality_tools and p.source_file_count > 5]
    if no_quality:
        connections.append(Connection(
            type="quality_gap",
            detail=f"{len(no_quality)} projects have no code quality tooling",
            projects=no_quality,
            severity="critical",
        ))

    # Missing linting
    linters = {"Ruff", "Flake8", "Pylint", "ESLint", "Biome", "golangci-lint", "Clippy"}
    no_linting = [
        p.name for p in projects
        if p.tech_stack.quality_tools
        and not any(t in linters for t in p.tech_stack.quality_tools)
        and p.source_file_count > 5
    ]
    if no_linting:
        connections.append(Connection(
            type="quality_gap",
            detail=f"{len(no_linting)} projects lack linting — add Ruff/ESLint",
            projects=no_linting,
            severity="warning",
        ))

    # Missing type checking
    type_checkers = {"mypy", "Pyright", "TypeScript"}
    no_types = [
        p.name for p in projects
        if p.tech_stack.quality_tools
        and not any(t in type_checkers for t in p.tech_stack.quality_tools)
        and p.source_file_count > 5
    ]
    if no_types:
        connections.append(Connection(
            type="quality_gap",
            detail=f"{len(no_types)} projects lack type checking — add mypy/Pyright/TypeScript",
            projects=no_types,
            severity="warning",
        ))

    # Linter divergence — multiple linters across portfolio
    linter_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for tool in proj.tech_stack.quality_tools:
            if tool in linters:
                linter_to_projects[tool].append(proj.name)
    if len(linter_to_projects) >= 2:
        detail_parts = [f"{tool} ({', '.join(ps[:3])})" for tool, ps in linter_to_projects.items()]
        all_projects = list({p for ps in linter_to_projects.values() for p in ps})
        connections.append(Connection(
            type="quality_divergence",
            detail=f"Multiple linters: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    return connections[:10]


def _find_ai_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project AI/ML patterns."""
    connections: list[Connection] = []
    ai_to_projects: dict[str, list[str]] = defaultdict(list)

    for proj in projects:
        for tool in proj.tech_stack.ai_tools:
            ai_to_projects[tool].append(proj.name)

    # Shared AI/ML tools (2+ projects)
    for tool, projs in sorted(ai_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_ai",
                detail=f"{tool} used across {len(projs)} projects — share patterns",
                projects=projs,
                severity="info",
            ))

    # LLM provider divergence — multiple providers across portfolio
    llm_providers = {"Anthropic SDK", "OpenAI"}
    llm_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for tool in proj.tech_stack.ai_tools:
            if tool in llm_providers:
                llm_to_projects[tool].append(proj.name)
    if len(llm_to_projects) >= 2:
        detail_parts = [f"{p} ({', '.join(ps[:3])})" for p, ps in llm_to_projects.items()]
        all_projects = list({p for ps in llm_to_projects.values() for p in ps})
        connections.append(Connection(
            type="ai_divergence",
            detail=f"Multiple LLM providers: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Vector DB divergence — multiple vector DBs across portfolio
    vector_dbs = {"ChromaDB", "Pinecone", "Sentence Transformers"}
    vdb_to_projects: dict[str, list[str]] = defaultdict(list)
    for proj in projects:
        for tool in proj.tech_stack.ai_tools:
            if tool in vector_dbs:
                vdb_to_projects[tool].append(proj.name)
    if len(vdb_to_projects) >= 2:
        detail_parts = [f"{db} ({', '.join(ps[:3])})" for db, ps in vdb_to_projects.items()]
        all_projects = list({p for ps in vdb_to_projects.values() for p in ps})
        connections.append(Connection(
            type="ai_divergence",
            detail=f"Multiple vector DBs: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # ML projects without experiment tracking
    ml_frameworks = {"PyTorch", "TensorFlow", "Transformers", "scikit-learn"}
    experiment_tracking = {"MLflow", "W&B", "DVC"}
    ml_no_tracking = [
        p.name for p in projects
        if any(t in ml_frameworks for t in p.tech_stack.ai_tools)
        and not any(t in experiment_tracking for t in p.tech_stack.ai_tools)
    ]
    if ml_no_tracking:
        connections.append(Connection(
            type="ai_gap",
            detail=f"{len(ml_no_tracking)} ML projects lack experiment tracking — add MLflow/W&B",
            projects=ml_no_tracking,
            severity="warning",
        ))

    return connections[:10]


def _find_testing_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project testing framework patterns."""
    connections: list[Connection] = []

    # Shared testing frameworks (2+ projects)
    from collections import Counter
    tf_counter: Counter[str] = Counter()
    tf_projects: dict[str, list[str]] = {}
    for p in projects:
        for tf in p.tech_stack.testing_frameworks:
            tf_counter[tf] += 1
            tf_projects.setdefault(tf, []).append(p.name)

    for tf, count in tf_counter.most_common():
        if count >= 2:
            connections.append(Connection(
                type="shared_testing",
                detail=f"{tf} used in {count} projects — reuse configs/fixtures",
                projects=tf_projects[tf],
                severity="info",
            ))

    # Testing framework divergence within same language
    # JS: Jest vs Vitest vs Mocha
    js_unit_frameworks = {"Jest", "Vitest", "Mocha", "AVA"}
    js_divergence: dict[str, set[str]] = {}
    for p in projects:
        js_tfs = [tf for tf in p.tech_stack.testing_frameworks if tf in js_unit_frameworks]
        for tf in js_tfs:
            js_divergence.setdefault(tf, set()).add(p.name)

    if len(js_divergence) >= 2:
        detail_parts = [f"{tf} ({', '.join(sorted(projs))})" for tf, projs in js_divergence.items()]
        all_projects = sorted({p for projs in js_divergence.values() for p in projs})
        connections.append(Connection(
            type="testing_divergence",
            detail=f"Multiple JS test runners: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Python: pytest vs nose2 vs unittest2
    py_test_frameworks = {"pytest", "nose2", "unittest2"}
    py_divergence: dict[str, set[str]] = {}
    for p in projects:
        py_tfs = [tf for tf in p.tech_stack.testing_frameworks if tf in py_test_frameworks]
        for tf in py_tfs:
            py_divergence.setdefault(tf, set()).add(p.name)

    if len(py_divergence) >= 2:
        detail_parts = [f"{tf} ({', '.join(sorted(projs))})" for tf, projs in py_divergence.items()]
        all_projects = sorted({p for projs in py_divergence.values() for p in projs})
        connections.append(Connection(
            type="testing_divergence",
            detail=f"Multiple Python test runners: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Testing gap — projects with code but no testing framework
    no_testing = [
        p.name for p in projects
        if not p.tech_stack.testing_frameworks and p.source_file_count > 5
    ]
    if no_testing:
        connections.append(Connection(
            type="testing_gap",
            detail=f"{len(no_testing)} projects have no testing framework — add pytest/Jest",
            projects=no_testing,
            severity="critical",
        ))

    return connections[:10]


def _find_package_manager_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project package manager patterns."""
    connections: list[Connection] = []

    # Shared package managers (2+ projects)
    from collections import Counter
    pm_counter: Counter[str] = Counter()
    pm_projects: dict[str, list[str]] = {}
    for p in projects:
        for pm in p.tech_stack.package_managers:
            pm_counter[pm] += 1
            pm_projects.setdefault(pm, []).append(p.name)

    for pm, count in pm_counter.most_common():
        if count >= 2:
            connections.append(Connection(
                type="shared_pkg_manager",
                detail=f"{pm} used in {count} projects — share configs/scripts",
                projects=pm_projects[pm],
                severity="info",
            ))

    # JS package manager divergence (npm vs yarn vs pnpm vs bun)
    js_managers = {"npm", "Yarn", "pnpm", "Bun"}
    js_divergence: dict[str, set[str]] = {}
    for p in projects:
        for pm in p.tech_stack.package_managers:
            if pm in js_managers:
                js_divergence.setdefault(pm, set()).add(p.name)

    if len(js_divergence) >= 2:
        detail_parts = [f"{pm} ({', '.join(sorted(projs))})" for pm, projs in js_divergence.items()]
        all_projects = sorted({p for projs in js_divergence.values() for p in projs})
        connections.append(Connection(
            type="pkg_manager_divergence",
            detail=f"Multiple JS package managers: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Python package manager divergence (pip vs Poetry vs PDM vs uv vs Pipenv)
    py_managers = {"pip", "Poetry", "PDM", "uv", "Pipenv"}
    py_divergence: dict[str, set[str]] = {}
    for p in projects:
        for pm in p.tech_stack.package_managers:
            if pm in py_managers:
                py_divergence.setdefault(pm, set()).add(p.name)

    if len(py_divergence) >= 2:
        detail_parts = [f"{pm} ({', '.join(sorted(projs))})" for pm, projs in py_divergence.items()]
        all_projects = sorted({p for projs in py_divergence.values() for p in projs})
        connections.append(Connection(
            type="pkg_manager_divergence",
            detail=f"Multiple Python package managers: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # Java build tool divergence (Maven vs Gradle)
    java_managers = {"Maven", "Gradle"}
    java_divergence: dict[str, set[str]] = {}
    for p in projects:
        for pm in p.tech_stack.package_managers:
            if pm in java_managers:
                java_divergence.setdefault(pm, set()).add(p.name)

    if len(java_divergence) >= 2:
        detail_parts = [f"{pm} ({', '.join(sorted(projs))})" for pm, projs in java_divergence.items()]
        all_projects = sorted({p for projs in java_divergence.values() for p in projs})
        connections.append(Connection(
            type="pkg_manager_divergence",
            detail=f"Multiple Java build tools: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    return connections[:10]


def _find_license_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project license patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared licenses — same license used in 2+ projects
    license_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        if p.license:
            license_to_projects[p.license].append(p.name)

    for lic, projs in license_to_projects.items():
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_license",
                detail=f"{lic} used across {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # License divergence — multiple license types in portfolio
    distinct_licenses = set(license_to_projects.keys())
    if len(distinct_licenses) >= 2:
        copyleft = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0"}
        has_copyleft = distinct_licenses & copyleft
        permissive = distinct_licenses - copyleft
        if has_copyleft and permissive:
            parts = []
            for lic in sorted(distinct_licenses):
                projs = license_to_projects[lic]
                parts.append(f"{lic} ({', '.join(projs[:3])})")
            all_projects = sorted({p for projs in license_to_projects.values() for p in projs})
            connections.append(Connection(
                type="license_divergence",
                detail=f"Copyleft/permissive mix: {', '.join(parts)} — review compatibility",
                projects=all_projects,
                severity="critical",
            ))
        else:
            parts = []
            for lic in sorted(distinct_licenses):
                projs = license_to_projects[lic]
                parts.append(f"{lic} ({', '.join(projs[:3])})")
            all_projects = sorted({p for projs in license_to_projects.values() for p in projs})
            connections.append(Connection(
                type="license_divergence",
                detail=f"Multiple licenses: {', '.join(parts)} — consider standardizing",
                projects=all_projects,
                severity="warning",
            ))

    # License gaps — projects with source files but no detected license
    unlicensed = [p.name for p in projects if not p.license and p.source_file_count > 5]
    if unlicensed:
        connections.append(Connection(
            type="license_gap",
            detail=f"{len(unlicensed)} project(s) have no detected license — add a LICENSE file",
            projects=sorted(unlicensed),
            severity="warning",
        ))

    return connections[:10]


def _find_ci_config_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project CI/CD configuration patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared CI config items — same item in 2+ projects
    config_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for item in p.tech_stack.ci_config:
            config_to_projects[item].append(p.name)

    for item, projs in sorted(config_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_ci_config",
                detail=f"{item} in {len(projs)} projects — share config templates",
                projects=sorted(projs),
                severity="info",
            ))

    # Dep update strategy divergence — Dependabot config vs Renovate config
    dep_update_tools = {"Dependabot config", "Renovate config"}
    dep_update_found: dict[str, set[str]] = {}
    for p in projects:
        for item in p.tech_stack.ci_config:
            if item in dep_update_tools:
                dep_update_found.setdefault(item, set()).add(p.name)

    if len(dep_update_found) >= 2:
        detail_parts = [f"{tool} ({', '.join(sorted(projs))})"
                        for tool, projs in dep_update_found.items()]
        all_projects = sorted({p for projs in dep_update_found.values() for p in projs})
        connections.append(Connection(
            type="ci_config_divergence",
            detail=f"Multiple dep update strategies: {', '.join(detail_parts)} — standardize",
            projects=all_projects,
            severity="warning",
        ))

    # PR template gap — projects with CI but no PR template
    ci_systems = {"GitHub Actions", "GitLab CI", "Jenkins", "CircleCI"}
    no_pr_template = [
        p.name for p in projects
        if any(i in ci_systems for i in p.tech_stack.infrastructure)
        and "PR template" not in p.tech_stack.ci_config
        and p.source_file_count > 10
    ]
    if no_pr_template:
        connections.append(Connection(
            type="ci_config_gap",
            detail=f"{len(no_pr_template)} project(s) with CI but no PR template",
            projects=sorted(no_pr_template),
            severity="warning",
        ))

    # CODEOWNERS gap — larger projects without CODEOWNERS
    no_codeowners = [
        p.name for p in projects
        if "CODEOWNERS" not in p.tech_stack.ci_config
        and p.source_file_count > 20
    ]
    if no_codeowners:
        connections.append(Connection(
            type="ci_config_gap",
            detail=f"{len(no_codeowners)} project(s) missing CODEOWNERS",
            projects=sorted(no_codeowners),
            severity="warning",
        ))

    # Pre-commit gap — projects with quality tools but no pre-commit hooks
    no_precommit = [
        p.name for p in projects
        if p.tech_stack.quality_tools
        and "pre-commit" not in p.tech_stack.ci_config
        and p.source_file_count > 5
    ]
    if no_precommit:
        connections.append(Connection(
            type="ci_config_gap",
            detail=f"{len(no_precommit)} project(s) have quality tools but no pre-commit hooks",
            projects=sorted(no_precommit),
            severity="warning",
        ))

    return connections[:10]


def _find_docs_artifact_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project documentation artifact patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared docs artifacts — same artifact in 2+ projects
    artifact_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for artifact in p.tech_stack.docs_artifacts:
            artifact_to_projects[artifact].append(p.name)

    for artifact, projs in artifact_to_projects.items():
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_docs",
                detail=f"{artifact} present in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Docs coverage divergence — projects with rich docs vs minimal docs
    rich_docs = [p.name for p in projects if len(p.tech_stack.docs_artifacts) >= 5]
    minimal_docs = [p.name for p in projects if 0 < len(p.tech_stack.docs_artifacts) <= 1
                    and p.source_file_count > 5]
    if rich_docs and minimal_docs:
        connections.append(Connection(
            type="docs_divergence",
            detail=(
                f"{len(rich_docs)} project(s) have rich documentation "
                f"while {len(minimal_docs)} have minimal — consider standardizing"
            ),
            projects=sorted(rich_docs + minimal_docs),
            severity="warning",
        ))

    # Docs gaps — projects missing critical artifacts
    # README gap
    no_readme = [p.name for p in projects
                 if "README" not in p.tech_stack.docs_artifacts
                 and p.source_file_count > 5]
    if no_readme:
        connections.append(Connection(
            type="docs_gap",
            detail=f"{len(no_readme)} project(s) missing README",
            projects=sorted(no_readme),
            severity="critical",
        ))

    # CHANGELOG gap
    no_changelog = [p.name for p in projects
                    if "CHANGELOG" not in p.tech_stack.docs_artifacts
                    and p.source_file_count > 10]
    if no_changelog:
        connections.append(Connection(
            type="docs_gap",
            detail=f"{len(no_changelog)} project(s) missing CHANGELOG",
            projects=sorted(no_changelog),
            severity="warning",
        ))

    # CONTRIBUTING gap (only flag for larger projects)
    no_contributing = [p.name for p in projects
                       if "CONTRIBUTING" not in p.tech_stack.docs_artifacts
                       and p.source_file_count > 20]
    if no_contributing:
        connections.append(Connection(
            type="docs_gap",
            detail=f"{len(no_contributing)} project(s) missing CONTRIBUTING guide",
            projects=sorted(no_contributing),
            severity="warning",
        ))

    return connections[:10]


def _find_runtime_version_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project runtime version patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared runtime versions — same language pinned in 2+ projects
    lang_to_projects: dict[str, list[str]] = defaultdict(list)
    lang_to_versions: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for p in projects:
        for lang, ver in p.tech_stack.runtime_versions.items():
            lang_to_projects[lang].append(p.name)
            lang_to_versions[lang][ver].append(p.name)

    for lang, projs in sorted(lang_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_runtime",
                detail=f"{lang} version pinned in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Runtime version divergence — same language, different versions across projects
    for lang, ver_map in lang_to_versions.items():
        if len(ver_map) >= 2:
            detail_parts = [f"{ver} ({', '.join(sorted(projs))})"
                            for ver, projs in sorted(ver_map.items())]
            all_projs = sorted({p for projs in ver_map.values() for p in projs})
            connections.append(Connection(
                type="runtime_divergence",
                detail=f"{lang} version mismatch: {', '.join(detail_parts)} — standardize",
                projects=all_projs,
                severity="warning",
            ))

    # Runtime version pinning gap — projects with source files but no pinned runtime
    has_runtime = {p.name for p in projects if p.tech_stack.runtime_versions}
    if has_runtime:
        no_runtime = [p.name for p in projects
                      if not p.tech_stack.runtime_versions
                      and p.source_file_count > 5]
        if no_runtime:
            connections.append(Connection(
                type="runtime_gap",
                detail=f"{len(no_runtime)} project(s) have no pinned runtime version",
                projects=sorted(no_runtime),
                severity="warning",
            ))

    return connections[:10]


def _find_build_tool_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project build tool patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared build tools — same tool in 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.build_tools:
            tool_to_projects[tool].append(p.name)

    for tool, projs in sorted(tool_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_build_tool",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Build tool divergence — multiple task runners of same category
    # Python task runners: tox vs nox vs Invoke vs doit
    py_runners = {"tox", "nox", "Invoke", "doit"}
    py_found: dict[str, set[str]] = {}
    for p in projects:
        for tool in p.tech_stack.build_tools:
            if tool in py_runners:
                py_found.setdefault(tool, set()).add(p.name)
    if len(py_found) >= 2:
        detail_parts = [f"{t} ({', '.join(sorted(ps))})" for t, ps in py_found.items()]
        all_projs = sorted({p for ps in py_found.values() for p in ps})
        connections.append(Connection(
            type="build_tool_divergence",
            detail=f"Multiple Python task runners: {', '.join(detail_parts)} — standardize",
            projects=all_projs,
            severity="warning",
        ))

    # Java build tool divergence: Gradle vs Maven
    java_tools = {"Gradle", "Maven"}
    java_found: dict[str, set[str]] = {}
    for p in projects:
        for tool in p.tech_stack.build_tools:
            if tool in java_tools:
                java_found.setdefault(tool, set()).add(p.name)
    if len(java_found) >= 2:
        detail_parts = [f"{t} ({', '.join(sorted(ps))})" for t, ps in java_found.items()]
        all_projs = sorted({p for ps in java_found.values() for p in ps})
        connections.append(Connection(
            type="build_tool_divergence",
            detail=f"Multiple Java build tools: {', '.join(detail_parts)} — standardize",
            projects=all_projs,
            severity="warning",
        ))

    # Build automation gap — projects with source files but no build tool
    has_build = {p.name for p in projects if p.tech_stack.build_tools}
    if has_build:
        no_build = [p.name for p in projects
                    if not p.tech_stack.build_tools
                    and p.source_file_count > 10]
        if no_build:
            connections.append(Connection(
                type="build_tool_gap",
                detail=f"{len(no_build)} project(s) have no build/task automation",
                projects=sorted(no_build),
                severity="warning",
            ))

    return connections[:10]


def _find_api_spec_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project API specification patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared API specs — same spec in 2+ projects
    spec_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for spec in p.tech_stack.api_specs:
            spec_to_projects[spec].append(p.name)

    for spec, projs in sorted(spec_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_api_spec",
                detail=f"{spec} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # API protocol divergence — REST vs GraphQL vs gRPC across portfolio
    rest_specs = {"OpenAPI", "AsyncAPI"}
    graph_specs = {"GraphQL"}
    rpc_specs = {"gRPC/Protobuf", "tRPC"}
    categories_found: dict[str, set[str]] = {}
    category_labels = {"REST": rest_specs, "GraphQL": graph_specs, "RPC": rpc_specs}
    for p in projects:
        for cat_name, cat_specs in category_labels.items():
            if any(s in cat_specs for s in p.tech_stack.api_specs):
                categories_found.setdefault(cat_name, set()).add(p.name)
    if len(categories_found) >= 2:
        detail_parts = [f"{cat} ({', '.join(sorted(ps))})"
                        for cat, ps in categories_found.items()]
        all_projs = sorted({p for ps in categories_found.values() for p in ps})
        connections.append(Connection(
            type="api_spec_divergence",
            detail=f"Multiple API paradigms: {', '.join(detail_parts)} — consider standardizing",
            projects=all_projs,
            severity="info",
        ))

    # API spec gap — projects with web frameworks but no API spec
    web_frameworks = {
        "FastAPI", "Django", "Flask", "Express", "Koa", "NestJS",
        "Spring Boot", "Rails", "Gin", "Echo", "Fiber", "Actix",
    }
    has_api = {p.name for p in projects if p.tech_stack.api_specs}
    if has_api:
        no_api = [p.name for p in projects
                  if not p.tech_stack.api_specs
                  and any(fw in web_frameworks for fw in p.tech_stack.frameworks)
                  and p.source_file_count > 5]
        if no_api:
            connections.append(Connection(
                type="api_spec_gap",
                detail=f"{len(no_api)} project(s) with web frameworks but no API spec",
                projects=sorted(no_api),
                severity="warning",
            ))

    return connections[:10]


def _find_monitoring_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project monitoring & observability patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared monitoring tools — same tool in 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.monitoring_tools:
            tool_to_projects[tool].append(p.name)

    for tool, projs in sorted(tool_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_monitoring",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Error tracking divergence — multiple error trackers across portfolio
    error_trackers = {"Sentry", "Bugsnag", "Rollbar", "Elastic APM"}
    et_found: dict[str, set[str]] = {}
    for p in projects:
        for tool in p.tech_stack.monitoring_tools:
            if tool in error_trackers:
                et_found.setdefault(tool, set()).add(p.name)
    if len(et_found) >= 2:
        detail_parts = [f"{t} ({', '.join(sorted(ps))})" for t, ps in et_found.items()]
        all_projs = sorted({p for ps in et_found.values() for p in ps})
        connections.append(Connection(
            type="monitoring_divergence",
            detail=f"Multiple error trackers: {', '.join(detail_parts)} — standardize",
            projects=all_projs,
            severity="warning",
        ))

    # APM divergence — multiple APM tools
    apm_tools = {"Datadog", "New Relic", "Elastic APM", "Honeycomb"}
    apm_found: dict[str, set[str]] = {}
    for p in projects:
        for tool in p.tech_stack.monitoring_tools:
            if tool in apm_tools:
                apm_found.setdefault(tool, set()).add(p.name)
    if len(apm_found) >= 2:
        detail_parts = [f"{t} ({', '.join(sorted(ps))})" for t, ps in apm_found.items()]
        all_projs = sorted({p for ps in apm_found.values() for p in ps})
        connections.append(Connection(
            type="monitoring_divergence",
            detail=f"Multiple APM tools: {', '.join(detail_parts)} — standardize",
            projects=all_projs,
            severity="warning",
        ))

    # Monitoring gap — projects with source files but no monitoring when others have it
    has_monitoring = {p.name for p in projects if p.tech_stack.monitoring_tools}
    if has_monitoring:
        no_monitoring = [p.name for p in projects
                         if not p.tech_stack.monitoring_tools
                         and p.source_file_count > 10]
        if no_monitoring:
            connections.append(Connection(
                type="monitoring_gap",
                detail=f"{len(no_monitoring)} project(s) have no monitoring/observability tooling",
                projects=sorted(no_monitoring),
                severity="warning",
            ))

    return connections[:10]


def _find_auth_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project authentication patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared auth tools — same tool in 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.auth_tools:
            tool_to_projects[tool].append(p.name)

    for tool, projs in sorted(tool_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_auth",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Auth provider divergence — multiple hosted auth providers across portfolio
    auth_providers = {"Auth0", "Clerk", "Firebase Auth", "Supabase Auth", "Keycloak"}
    provider_found: dict[str, set[str]] = {}
    for p in projects:
        for tool in p.tech_stack.auth_tools:
            if tool in auth_providers:
                provider_found.setdefault(tool, set()).add(p.name)
    if len(provider_found) >= 2:
        detail_parts = [f"{t} ({', '.join(sorted(ps))})" for t, ps in provider_found.items()]
        all_projs = sorted({p for ps in provider_found.values() for p in ps})
        connections.append(Connection(
            type="auth_divergence",
            detail=f"Multiple auth providers: {', '.join(detail_parts)} — standardize",
            projects=all_projs,
            severity="warning",
        ))

    # Auth framework divergence — multiple auth frameworks (session-based vs token-based)
    session_auth = {"Passport.js", "Flask-Login", "express-session", "django-allauth", "Lucia"}
    token_auth = {"NextAuth.js", "Auth.js", "PyJWT", "jsonwebtoken", "golang-jwt", "Authlib"}
    session_found: set[str] = set()
    token_found: set[str] = set()
    for p in projects:
        for tool in p.tech_stack.auth_tools:
            if tool in session_auth:
                session_found.add(p.name)
            if tool in token_auth:
                token_found.add(p.name)
    if session_found and token_found:
        session_only = session_found - token_found
        token_only = token_found - session_found
        if session_only and token_only:
            all_projs = sorted(session_only | token_only)
            connections.append(Connection(
                type="auth_divergence",
                detail=f"Mixed auth strategies: session-based ({', '.join(sorted(session_only))}) vs token-based ({', '.join(sorted(token_only))})",
                projects=all_projs,
                severity="info",
            ))

    # Auth gap — projects with web frameworks but no auth
    web_frameworks = {"FastAPI", "Django", "Flask", "Express", "Next.js", "Nuxt",
                      "Rails", "Spring Boot", "Actix", "Axum", "Gin", "Echo", "Fiber"}
    has_auth = {p.name for p in projects if p.tech_stack.auth_tools}
    if has_auth:
        no_auth = [p.name for p in projects
                   if not p.tech_stack.auth_tools
                   and any(fw in web_frameworks for fw in p.tech_stack.frameworks)
                   and p.source_file_count > 5]
        if no_auth:
            connections.append(Connection(
                type="auth_gap",
                detail=f"{len(no_auth)} web project(s) have no authentication tooling",
                projects=sorted(no_auth),
                severity="warning",
            ))

    return connections[:10]


def _find_messaging_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project messaging & notification patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared messaging tools — same tool in 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.messaging_tools:
            tool_to_projects[tool].append(p.name)

    for tool, projs in sorted(tool_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_messaging",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Email provider divergence — multiple transactional email services
    email_providers = {"SendGrid", "Postmark", "Mailgun", "Resend", "Nodemailer", "Gomail", "Lettre"}
    ep_found: dict[str, set[str]] = {}
    for p in projects:
        for tool in p.tech_stack.messaging_tools:
            if tool in email_providers:
                ep_found.setdefault(tool, set()).add(p.name)
    if len(ep_found) >= 2:
        detail_parts = [f"{t} ({', '.join(sorted(ps))})" for t, ps in ep_found.items()]
        all_projs = sorted({p for ps in ep_found.values() for p in ps})
        connections.append(Connection(
            type="messaging_divergence",
            detail=f"Multiple email providers: {', '.join(detail_parts)} — standardize",
            projects=all_projs,
            severity="warning",
        ))

    # Real-time divergence — multiple real-time/push services
    realtime_tools = {"Socket.IO", "Pusher", "Firebase Cloud Messaging", "Web Push", "Novu"}
    rt_found: dict[str, set[str]] = {}
    for p in projects:
        for tool in p.tech_stack.messaging_tools:
            if tool in realtime_tools:
                rt_found.setdefault(tool, set()).add(p.name)
    if len(rt_found) >= 2:
        detail_parts = [f"{t} ({', '.join(sorted(ps))})" for t, ps in rt_found.items()]
        all_projs = sorted({p for ps in rt_found.values() for p in ps})
        connections.append(Connection(
            type="messaging_divergence",
            detail=f"Multiple real-time/push services: {', '.join(detail_parts)} — standardize",
            projects=all_projs,
            severity="info",
        ))

    # Messaging gap — web projects with no messaging when others have it
    web_frameworks = {"FastAPI", "Django", "Flask", "Express", "Next.js", "Nuxt",
                      "Rails", "Spring Boot", "Actix", "Axum", "Gin", "Echo", "Fiber"}
    has_messaging = {p.name for p in projects if p.tech_stack.messaging_tools}
    if has_messaging:
        no_messaging = [p.name for p in projects
                        if not p.tech_stack.messaging_tools
                        and any(fw in web_frameworks for fw in p.tech_stack.frameworks)
                        and p.source_file_count > 10]
        if no_messaging:
            connections.append(Connection(
                type="messaging_gap",
                detail=f"{len(no_messaging)} web project(s) have no messaging/notification tooling",
                projects=sorted(no_messaging),
                severity="warning",
            ))

    return connections[:10]


def _find_deploy_target_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project deployment target patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared deploy targets — same platform in 2+ projects
    target_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for target in p.tech_stack.deploy_targets:
            target_to_projects[target].append(p.name)

    for target, projs in sorted(target_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_deploy",
                detail=f"{target} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Platform divergence — projects using different hosting categories
    serverless_paas = {"Vercel", "Netlify", "Cloudflare Workers", "AWS Amplify",
                       "Firebase Hosting", "GitHub Pages"}
    container_paas = {"Fly.io", "Railway", "Render", "Heroku",
                      "Google App Engine", "DigitalOcean App Platform"}
    iaas_serverless = {"Serverless Framework"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "serverless/edge": {}, "container PaaS": {}, "IaC serverless": {},
    }
    cat_sets = [
        ("serverless/edge", serverless_paas),
        ("container PaaS", container_paas),
        ("IaC serverless", iaas_serverless),
    ]
    for p in projects:
        for target in p.tech_stack.deploy_targets:
            for cat_name, cat_set in cat_sets:
                if target in cat_set:
                    cat_found[cat_name].setdefault(target, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys()))
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="deploy_divergence",
            detail=f"Mixed hosting strategies: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Deploy gap — web projects with frameworks but no deploy target configured
    web_frameworks = {"FastAPI", "Django", "Flask", "Express", "Next.js", "Nuxt",
                      "Rails", "Spring Boot", "Actix", "Axum", "Gin", "Echo", "Fiber"}
    has_deploy = {p.name for p in projects if p.tech_stack.deploy_targets}
    if has_deploy:
        no_deploy = [p.name for p in projects
                     if not p.tech_stack.deploy_targets
                     and any(fw in web_frameworks for fw in p.tech_stack.frameworks)
                     and p.source_file_count > 5]
        if no_deploy:
            connections.append(Connection(
                type="deploy_gap",
                detail=f"{len(no_deploy)} web project(s) have no deployment target configured",
                projects=sorted(no_deploy),
                severity="warning",
            ))

    return connections[:10]


def _find_state_management_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project state management patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared state management — same library in 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.state_management:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_state_mgmt",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # State management divergence — projects using different paradigm families
    flux_libs = {"Redux", "Zustand"}
    proxy_libs = {"MobX", "Valtio", "Legend State"}
    atomic_libs = {"Recoil", "Jotai", "Nanostores", "Signals"}
    machine_libs = {"XState"}
    vue_libs = {"Pinia", "Vuex"}
    angular_libs = {"NgRx"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "flux/store": {}, "proxy-based": {}, "atomic": {},
        "state machines": {}, "Vue": {}, "Angular": {},
    }
    cat_sets = [
        ("flux/store", flux_libs),
        ("proxy-based", proxy_libs),
        ("atomic", atomic_libs),
        ("state machines", machine_libs),
        ("Vue", vue_libs),
        ("Angular", angular_libs),
    ]
    for p in projects:
        for lib in p.tech_stack.state_management:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys()))
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="state_mgmt_divergence",
            detail=f"Mixed state management paradigms: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # State management gap — frontend projects with React/Vue/Angular but no state management
    frontend_frameworks = {"React", "Next.js", "Vue", "Nuxt", "Angular", "Svelte", "SvelteKit",
                           "Solid", "Preact", "Remix", "Gatsby", "Astro"}
    has_state = {p.name for p in projects if p.tech_stack.state_management}
    if has_state:
        no_state = [p.name for p in projects
                    if not p.tech_stack.state_management
                    and any(fw in frontend_frameworks for fw in p.tech_stack.frameworks)
                    and p.source_file_count > 10]
        if no_state:
            connections.append(Connection(
                type="state_mgmt_gap",
                detail=f"{len(no_state)} frontend project(s) have no state management library",
                projects=sorted(no_state),
                severity="warning",
            ))

    return connections[:10]


def _find_css_framework_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project CSS/styling patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared CSS frameworks — same framework in 2+ projects
    fw_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for fw in p.tech_stack.css_frameworks:
            fw_to_projects[fw].append(p.name)

    for fw, projs in sorted(fw_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_css",
                detail=f"{fw} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # CSS paradigm divergence — utility-first vs CSS-in-JS vs component library
    utility_first = {"Tailwind CSS", "UnoCSS", "Windi CSS", "Twin Macro"}
    css_in_js = {"Styled Components", "Emotion", "Vanilla Extract", "Linaria",
                 "Stitches", "Panda CSS"}
    component_libs = {"Bootstrap", "Bulma", "Chakra UI", "Mantine", "Material UI",
                      "Vuetify", "Ant Design", "Radix UI", "shadcn/ui"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "utility-first": {}, "CSS-in-JS": {}, "component library": {},
    }
    cat_sets = [
        ("utility-first", utility_first),
        ("CSS-in-JS", css_in_js),
        ("component library", component_libs),
    ]
    for p in projects:
        for fw in p.tech_stack.css_frameworks:
            for cat_name, cat_set in cat_sets:
                if fw in cat_set:
                    cat_found[cat_name].setdefault(fw, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys()))
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="css_divergence",
            detail=f"Mixed CSS paradigms: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # CSS gap — frontend projects with frameworks but no CSS/styling tools
    frontend_frameworks = {"React", "Next.js", "Vue", "Nuxt", "Angular", "Svelte", "SvelteKit",
                           "Solid", "Preact", "Remix", "Gatsby", "Astro"}
    has_css = {p.name for p in projects if p.tech_stack.css_frameworks}
    if has_css:
        no_css = [p.name for p in projects
                  if not p.tech_stack.css_frameworks
                  and any(fw in frontend_frameworks for fw in p.tech_stack.frameworks)
                  and p.source_file_count > 10]
        if no_css:
            connections.append(Connection(
                type="css_gap",
                detail=f"{len(no_css)} frontend project(s) have no CSS/styling framework",
                projects=sorted(no_css),
                severity="warning",
            ))

    return connections[:10]


def _find_bundler_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project bundler patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared bundlers — same tool in 2+ projects
    bnd_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for bnd in p.tech_stack.bundlers:
            bnd_to_projects[bnd].append(p.name)

    for bnd, projs in sorted(bnd_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_bundler",
                detail=f"{bnd} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Bundler divergence — projects using different bundler generations
    modern_fast = {"Vite", "esbuild", "SWC", "Turbopack", "Rspack", "Bun"}
    legacy_full = {"Webpack", "Rollup", "Parcel", "Snowpack"}
    lib_bundlers = {"tsup", "unbuild", "microbundle"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "modern/fast": {}, "traditional": {}, "library": {},
    }
    cat_sets = [
        ("modern/fast", modern_fast),
        ("traditional", legacy_full),
        ("library", lib_bundlers),
    ]
    for p in projects:
        for bnd in p.tech_stack.bundlers:
            for cat_name, cat_set in cat_sets:
                if bnd in cat_set:
                    cat_found[cat_name].setdefault(bnd, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys()))
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="bundler_divergence",
            detail=f"Mixed bundler generations: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Bundler gap — JS/TS projects with package.json but no bundler
    has_bundler = {p.name for p in projects if p.tech_stack.bundlers}
    if has_bundler:
        js_langs = {"JavaScript", "TypeScript"}
        no_bundler = [p.name for p in projects
                      if not p.tech_stack.bundlers
                      and any(lang in js_langs for lang in p.tech_stack.languages)
                      and p.source_file_count > 10]
        if no_bundler:
            connections.append(Connection(
                type="bundler_gap",
                detail=f"{len(no_bundler)} JS/TS project(s) have no bundler configured",
                projects=sorted(no_bundler),
                severity="warning",
            ))

    return connections[:10]


def _find_orm_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project ORM/database client patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared ORM tools — same tool in 2+ projects
    orm_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for orm in p.tech_stack.orm_tools:
            orm_to_projects[orm].append(p.name)

    for orm, projs in sorted(orm_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_orm",
                detail=f"{orm} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # ORM divergence — projects using different data access paradigms
    full_orm = {"SQLAlchemy", "Django ORM", "Peewee", "Tortoise ORM", "SQLModel",
                "Pony ORM", "TypeORM", "Sequelize", "Prisma", "Drizzle", "MikroORM",
                "Mongoose", "Bookshelf", "Objection.js", "Kysely", "MongoEngine",
                "GORM", "ent", "Diesel", "SeaORM", "Hibernate", "MyBatis", "jOOQ",
                "Spring Data JPA"}
    raw_client = {"asyncpg", "psycopg2", "psycopg", "node-postgres", "pg",
                  "better-sqlite3", "ioredis", "redis-py", "aioredis",
                  "PyMongo", "Motor", "MongoDB Driver", "databases",
                  "pgx", "sqlx (Go)", "sqlx (Rust)", "Rusqlite", "sqlc",
                  "Bun (Go)", "JDBI"}
    migration_tool = {"Alembic"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "ORM": {}, "raw client": {}, "migration": {},
    }
    cat_sets = [
        ("ORM", full_orm),
        ("raw client", raw_client),
        ("migration", migration_tool),
    ]
    for p in projects:
        for orm in p.tech_stack.orm_tools:
            for cat_name, cat_set in cat_sets:
                if orm in cat_set:
                    cat_found[cat_name].setdefault(orm, set()).add(p.name)

    # Only flag ORM vs raw client divergence (migration is fine alongside either)
    orm_projects = cat_found["ORM"]
    raw_projects = cat_found["raw client"]
    if orm_projects and raw_projects:
        parts = []
        all_projs: set[str] = set()
        orm_names = ", ".join(sorted(orm_projects.keys())[:4])
        parts.append(f"ORM ({orm_names})")
        for ps in orm_projects.values():
            all_projs.update(ps)
        raw_names = ", ".join(sorted(raw_projects.keys())[:4])
        parts.append(f"raw client ({raw_names})")
        for ps in raw_projects.values():
            all_projs.update(ps)
        connections.append(Connection(
            type="orm_divergence",
            detail=f"Mixed data access strategies: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # ORM gap — projects with databases but no ORM/client detected
    has_orm = {p.name for p in projects if p.tech_stack.orm_tools}
    if has_orm:
        no_orm = [p.name for p in projects
                  if not p.tech_stack.orm_tools
                  and p.tech_stack.databases
                  and p.source_file_count > 10]
        if no_orm:
            connections.append(Connection(
                type="orm_gap",
                detail=f"{len(no_orm)} project(s) use databases but have no ORM/client library detected",
                projects=sorted(no_orm),
                severity="warning",
            ))

    return connections[:10]


def _find_i18n_patterns(projects: list[Project]) -> list[Connection]:
    """Detect cross-project i18n/localization patterns: shared, divergence, gaps."""
    connections: list[Connection] = []

    # Shared i18n tools — same tool in 2+ projects
    i18n_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.i18n_tools:
            i18n_to_projects[tool].append(p.name)

    for tool, projs in sorted(i18n_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_i18n",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # i18n divergence — different i18n strategies across projects
    icu_message = {"react-intl", "FormatJS", "Globalize"}
    key_based = {"i18next", "react-i18next", "next-i18next", "next-intl", "vue-i18n",
                 "typesafe-i18n", "rosetta", "Polyglot", "go-i18n", "rust-i18n"}
    extraction = {"Lingui", "Babel (i18n)", "Flask-Babel", "django-modeltranslation",
                  "django-rosetta", "python-i18n", "Angular i18n", "Fluent"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "ICU/message format": {}, "key-based": {}, "extraction-based": {},
    }
    cat_sets = [
        ("ICU/message format", icu_message),
        ("key-based", key_based),
        ("extraction-based", extraction),
    ]
    for p in projects:
        for tool in p.tech_stack.i18n_tools:
            for cat_name, cat_set in cat_sets:
                if tool in cat_set:
                    cat_found[cat_name].setdefault(tool, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="i18n_divergence",
            detail=f"Mixed i18n strategies: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # i18n gap — web projects with no i18n detected
    has_i18n = {p.name for p in projects if p.tech_stack.i18n_tools}
    if has_i18n:
        web_frameworks = {"React", "Next.js", "Vue", "Nuxt", "Angular", "Svelte",
                          "Django", "Flask", "FastAPI", "Rails", "Express"}
        no_i18n = [p.name for p in projects
                   if not p.tech_stack.i18n_tools
                   and any(fw in web_frameworks for fw in p.tech_stack.frameworks)
                   and p.source_file_count > 10]
        if no_i18n:
            connections.append(Connection(
                type="i18n_gap",
                detail=f"{len(no_i18n)} web project(s) have no i18n/localization detected",
                projects=sorted(no_i18n),
                severity="warning",
            ))

    return connections[:10]


def _find_validation_patterns(projects: list[Project]) -> list[Connection]:
    """Detect shared validation libraries, paradigm divergence, and validation gaps."""
    connections: list[Connection] = []

    # Shared validation tools — same tool in 2+ projects
    val_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.validation_tools:
            val_to_projects[tool].append(p.name)

    for tool, projs in sorted(val_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_validation",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Validation divergence — schema-first vs model-based strategies
    schema_first = {"Zod", "Yup", "Joi", "Superstruct", "Valibot", "io-ts", "TypeBox",
                    "ArkType", "Effect Schema", "myZod", "Ajv", "jsonschema"}
    model_based = {"Pydantic", "marshmallow", "attrs", "cattrs", "Cerberus", "Colander",
                   "Schematics", "Voluptuous", "schema", "class-validator", "class-transformer",
                   "Hibernate Validator", "Jakarta Validation", "go-playground/validator",
                   "ozzo-validation", "validator (Rust)", "garde"}
    form_validation = {"Vest"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "schema-first": {}, "model/decorator-based": {}, "form validation": {},
    }
    cat_sets = [
        ("schema-first", schema_first),
        ("model/decorator-based", model_based),
        ("form validation", form_validation),
    ]
    for p in projects:
        for tool in p.tech_stack.validation_tools:
            for cat_name, cat_set in cat_sets:
                if tool in cat_set:
                    cat_found[cat_name].setdefault(tool, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="validation_divergence",
            detail=f"Mixed validation strategies: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Validation gap — API/backend projects with no validation detected
    has_val = {p.name for p in projects if p.tech_stack.validation_tools}
    if has_val:
        api_frameworks = {"FastAPI", "Flask", "Django", "Express", "Koa", "Hapi",
                          "NestJS", "Rails", "Spring Boot", "Gin", "Echo", "Actix"}
        no_val = [p.name for p in projects
                  if not p.tech_stack.validation_tools
                  and any(fw in api_frameworks for fw in p.tech_stack.frameworks)
                  and p.source_file_count > 10]
        if no_val:
            connections.append(Connection(
                type="validation_gap",
                detail=f"{len(no_val)} API/backend project(s) have no validation library detected",
                projects=sorted(no_val),
                severity="critical",
            ))

    return connections[:10]


def _find_logging_patterns(projects: list[Project]) -> list[Connection]:
    """Detect shared logging tools, paradigm divergence, and logging gaps."""
    connections: list[Connection] = []

    # Shared logging tools — same tool in 2+ projects
    log_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.logging_tools:
            log_to_projects[tool].append(p.name)

    for tool, projs in sorted(log_to_projects.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_logging",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Logging divergence — structured vs traditional vs HTTP-request logging
    structured = {"structlog", "Pino", "Bunyan", "zerolog", "Zap", "Loguru",
                  "python-json-logger", "tracing (Rust)", "Roarr", "tslog"}
    traditional = {"Winston", "log4js", "loglevel", "Logback", "Log4j", "SLF4J",
                   "Logrus", "env_logger", "log4rs", "Logbook", "Signale", "Consola",
                   "fern", "slog (Rust)", "Eliot", "Twiggy", "coloredlogs",
                   "logging-tree", "Rich (logging)", "debug"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "structured": {}, "traditional": {},
    }
    cat_sets = [
        ("structured", structured),
        ("traditional", traditional),
    ]
    for p in projects:
        for tool in p.tech_stack.logging_tools:
            for cat_name, cat_set in cat_sets:
                if tool in cat_set:
                    cat_found[cat_name].setdefault(tool, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="logging_divergence",
            detail=f"Mixed logging strategies: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Logging gap — backend projects with no logging detected
    has_log = {p.name for p in projects if p.tech_stack.logging_tools}
    if has_log:
        backend_frameworks = {"FastAPI", "Flask", "Django", "Express", "Koa", "Hapi",
                              "NestJS", "Rails", "Spring Boot", "Gin", "Echo", "Actix",
                              "Rocket", "Axum"}
        no_log = [p.name for p in projects
                  if not p.tech_stack.logging_tools
                  and any(fw in backend_frameworks for fw in p.tech_stack.frameworks)
                  and p.source_file_count > 10]
        if no_log:
            connections.append(Connection(
                type="logging_gap",
                detail=f"{len(no_log)} backend project(s) have no logging framework detected",
                projects=sorted(no_log),
                severity="warning",
            ))

    return connections[:10]


def _find_container_orchestration_patterns(projects: list[Project]) -> list[Connection]:
    """Find container orchestration patterns across projects."""
    connections: list[Connection] = []

    # Shared container orchestration tools
    tool_to_projs: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.container_orchestration:
            tool_to_projs[tool].append(p.name)

    for tool, projs in sorted(tool_to_projs.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_container_orch",
                detail=f"{tool} used across {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Container orchestration divergence — different deployment strategies
    iac = {"Terraform", "Pulumi", "Ansible", "Packer", "Vagrant"}
    k8s_native = {"Kubernetes", "Helm", "Kustomize", "Skaffold", "Tilt"}
    compose = {"Docker Compose", "Docker Swarm"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "iac": {}, "k8s": {}, "compose": {},
    }
    cat_sets = [
        ("iac", iac),
        ("k8s", k8s_native),
        ("compose", compose),
    ]
    for p in projects:
        for tool in p.tech_stack.container_orchestration:
            for cat_name, cat_set in cat_sets:
                if tool in cat_set:
                    cat_found[cat_name].setdefault(tool, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="container_orch_divergence",
            detail=f"Mixed orchestration strategies: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Container orchestration gap — projects with Docker but no orchestration
    has_orch = {p.name for p in projects if p.tech_stack.container_orchestration}
    if has_orch:
        no_orch = [p.name for p in projects
                   if not p.tech_stack.container_orchestration
                   and "Docker" in p.tech_stack.infrastructure
                   and p.source_file_count > 10]
        if no_orch:
            connections.append(Connection(
                type="container_orch_gap",
                detail=f"{len(no_orch)} Docker project(s) have no orchestration tooling",
                projects=sorted(no_orch),
                severity="warning",
            ))

    return connections[:10]


def _find_cloud_provider_patterns(projects: list[Project]) -> list[Connection]:
    """Find cloud provider patterns across projects."""
    connections: list[Connection] = []

    # Shared cloud providers
    provider_to_projs: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for cp in p.tech_stack.cloud_providers:
            provider_to_projs[cp].append(p.name)

    for provider, projs in sorted(provider_to_projs.items(), key=lambda x: len(x[1]), reverse=True):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_cloud",
                detail=f"{provider} used across {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Cloud provider divergence — different cloud strategies
    hyperscalers = {"AWS", "GCP", "Azure"}
    edge_paas = {"Cloudflare", "Fly.io", "Railway", "Render", "DigitalOcean"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "hyperscaler": {}, "edge_paas": {},
    }
    cat_sets = [
        ("hyperscaler", hyperscalers),
        ("edge_paas", edge_paas),
    ]
    for p in projects:
        for cp in p.tech_stack.cloud_providers:
            for cat_name, cat_set in cat_sets:
                if cp in cat_set:
                    cat_found[cat_name].setdefault(cp, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, providers in active_cats.items():
            provider_names = ", ".join(sorted(providers.keys())[:3])
            parts.append(f"{cat_name} ({provider_names})")
            for ps in providers.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="cloud_divergence",
            detail=f"Mixed cloud strategies: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Multi-hyperscaler divergence within hyperscalers
    hyper_found: dict[str, set[str]] = {}
    for p in projects:
        for cp in p.tech_stack.cloud_providers:
            if cp in hyperscalers:
                hyper_found.setdefault(cp, set()).add(p.name)
    if len(hyper_found) >= 2:
        parts = [f"{cp} ({len(ps)})" for cp, ps in sorted(hyper_found.items())]
        all_projs_h: set[str] = set()
        for ps in hyper_found.values():
            all_projs_h.update(ps)
        connections.append(Connection(
            type="cloud_divergence",
            detail=f"Multiple hyperscalers in use: {', '.join(parts)} — watch for vendor lock-in complexity",
            projects=sorted(all_projs_h),
            severity="warning",
        ))

    # Cloud gap — deployed projects with no cloud provider detected
    has_cloud = {p.name for p in projects if p.tech_stack.cloud_providers}
    if has_cloud:
        no_cloud = [p.name for p in projects
                    if not p.tech_stack.cloud_providers
                    and (p.tech_stack.deploy_targets or p.tech_stack.container_orchestration)
                    and p.source_file_count > 10]
        if no_cloud:
            connections.append(Connection(
                type="cloud_gap",
                detail=f"{len(no_cloud)} deployed project(s) have no cloud provider SDK detected",
                projects=sorted(no_cloud),
                severity="info",
            ))

    return connections[:10]


def _find_task_queue_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project task queue and background job patterns."""
    connections: list[Connection] = []

    # Shared task queues — same queue framework used by 2+ projects
    queue_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for q in p.tech_stack.task_queues:
            queue_to_projects[q].append(p.name)

    for q, projs in sorted(queue_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_task_queue",
                detail=f"{q} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Task queue divergence — different queue paradigms across portfolio
    traditional = {"Celery", "RQ", "Dramatiq", "Huey", "arq", "TaskIQ",
                   "BullMQ", "Bull", "Bee-Queue", "Agenda", "Asynq",
                   "gocraft/work", "Quartz", "Spring Batch",
                   "tokio-cron-scheduler", "Apalis", "pg-boss",
                   "Graphile Worker", "Quirrel"}
    workflow = {"Temporal", "Prefect", "Airflow", "Luigi", "Dagster"}
    cron_based = {"node-cron", "robfig/cron"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "traditional": {}, "workflow": {}, "cron": {},
    }
    cat_sets = [
        ("traditional", traditional),
        ("workflow", workflow),
        ("cron", cron_based),
    ]
    for p in projects:
        for q in p.tech_stack.task_queues:
            for cat_name, cat_set in cat_sets:
                if q in cat_set:
                    cat_found[cat_name].setdefault(q, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, queues in active_cats.items():
            queue_names = ", ".join(sorted(queues.keys())[:3])
            parts.append(f"{cat_name} ({queue_names})")
            for ps in queues.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="task_queue_divergence",
            detail=f"Mixed task queue paradigms: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Task queue gap — backend projects with no task queue detected
    has_queues = {p.name for p in projects if p.tech_stack.task_queues}
    if has_queues:
        no_queues = [p.name for p in projects
                     if not p.tech_stack.task_queues
                     and p.source_file_count > 20
                     and any(f in p.tech_stack.frameworks
                             for f in ("FastAPI", "Django", "Flask", "Express",
                                       "NestJS", "Spring", "Gin", "Echo",
                                       "Actix", "Rails"))]
        if no_queues:
            connections.append(Connection(
                type="task_queue_gap",
                detail=f"{len(no_queues)} backend project(s) have no task queue/background jobs detected",
                projects=sorted(no_queues),
                severity="warning",
            ))

    return connections[:10]


def _find_search_engine_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project search engine patterns."""
    connections: list[Connection] = []

    # Shared search engines — same engine used by 2+ projects
    engine_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for e in p.tech_stack.search_engines:
            engine_to_projects[e].append(p.name)

    for e, projs in sorted(engine_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_search",
                detail=f"{e} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Search engine divergence — different search paradigms
    server_side = {"Elasticsearch", "OpenSearch", "Solr", "Meilisearch",
                   "Typesense", "Lucene", "Bleve", "Tantivy", "Whoosh",
                   "Haystack", "Watson"}
    client_side = {"Lunr", "FlexSearch", "Fuse.js", "MiniSearch"}
    saas = {"Algolia"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "server": {}, "client": {}, "saas": {},
    }
    cat_sets = [
        ("server", server_side),
        ("client", client_side),
        ("saas", saas),
    ]
    for p in projects:
        for e in p.tech_stack.search_engines:
            for cat_name, cat_set in cat_sets:
                if e in cat_set:
                    cat_found[cat_name].setdefault(e, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, engines in active_cats.items():
            engine_names = ", ".join(sorted(engines.keys())[:3])
            parts.append(f"{cat_name} ({engine_names})")
            for ps in engines.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="search_divergence",
            detail=f"Mixed search paradigms: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Search gap — data-heavy projects with no search engine
    has_search = {p.name for p in projects if p.tech_stack.search_engines}
    if has_search:
        no_search = [p.name for p in projects
                     if not p.tech_stack.search_engines
                     and p.source_file_count > 20
                     and (p.tech_stack.databases or p.tech_stack.orm_tools)]
        if no_search:
            connections.append(Connection(
                type="search_gap",
                detail=f"{len(no_search)} database-backed project(s) have no search engine detected",
                projects=sorted(no_search),
                severity="info",
            ))

    return connections[:10]


def _find_feature_flag_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project feature flag patterns."""
    connections: list[Connection] = []

    # Shared feature flag tools — same tool used by 2+ projects
    flag_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for f in p.tech_stack.feature_flags:
            flag_to_projects[f].append(p.name)

    for f, projs in sorted(flag_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_feature_flag",
                detail=f"{f} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Feature flag divergence — different flag paradigms
    saas = {"LaunchDarkly", "Split", "Statsig", "ConfigCat", "HappyKit",
            "Vercel Flags"}
    self_hosted = {"Unleash", "Flagsmith", "GrowthBook", "Flipper",
                   "Togglz", "FF4J", "Waffle", "Flask-FeatureFlags"}
    analytics = {"PostHog"}
    standard = {"OpenFeature"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "saas": {}, "self_hosted": {}, "analytics": {}, "standard": {},
    }
    cat_sets = [
        ("saas", saas),
        ("self_hosted", self_hosted),
        ("analytics", analytics),
        ("standard", standard),
    ]
    for p in projects:
        for f in p.tech_stack.feature_flags:
            for cat_name, cat_set in cat_sets:
                if f in cat_set:
                    cat_found[cat_name].setdefault(f, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, flags in active_cats.items():
            flag_names = ", ".join(sorted(flags.keys())[:3])
            parts.append(f"{cat_name} ({flag_names})")
            for ps in flags.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="feature_flag_divergence",
            detail=f"Mixed feature flag approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Feature flag gap — web projects with no feature flags
    has_flags = {p.name for p in projects if p.tech_stack.feature_flags}
    if has_flags:
        no_flags = [p.name for p in projects
                    if not p.tech_stack.feature_flags
                    and p.source_file_count > 20
                    and any(f in p.tech_stack.frameworks
                            for f in ("Next.js", "React", "Vue.js", "Angular",
                                      "Svelte", "Nuxt", "Remix", "FastAPI",
                                      "Django", "Express", "NestJS"))]
        if no_flags:
            connections.append(Connection(
                type="feature_flag_gap",
                detail=f"{len(no_flags)} web project(s) have no feature flag tooling detected",
                projects=sorted(no_flags),
                severity="info",
            ))

    return connections[:10]


def _find_http_client_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project HTTP client patterns."""
    connections: list[Connection] = []

    # Shared HTTP clients — same client used by 2+ projects
    client_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for c in p.tech_stack.http_clients:
            client_to_projects[c].append(p.name)

    for c, projs in sorted(client_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_http_client",
                detail=f"{c} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # HTTP client divergence — different paradigms across portfolio
    sync_clients = {"Requests", "urllib3", "httplib2", "PycURL", "Got",
                    "SuperAgent", "Needle", "ureq", "attohttpc", "OkHttp",
                    "Apache HttpClient", "Unirest", "RestTemplate"}
    async_clients = {"HTTPX", "aiohttp", "treq", "asks", "niquests",
                     "Undici", "reqwest", "hyper", "surf", "isahc",
                     "WebClient"}
    fetch_based = {"node-fetch", "cross-fetch", "isomorphic-fetch", "ofetch",
                   "Ky", "Wretch"}
    rpc_style = {"Retrofit", "Feign", "Resty", "Uplink", "Sling",
                 "go-retryablehttp", "Heimdall", "Req", "Gentleman", "Axios"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "sync": {}, "async": {}, "fetch": {}, "rpc": {},
    }
    cat_sets = [
        ("sync", sync_clients),
        ("async", async_clients),
        ("fetch", fetch_based),
        ("rpc", rpc_style),
    ]
    for p in projects:
        for c in p.tech_stack.http_clients:
            for cat_name, cat_set in cat_sets:
                if c in cat_set:
                    cat_found[cat_name].setdefault(c, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, clients in active_cats.items():
            client_names = ", ".join(sorted(clients.keys())[:3])
            parts.append(f"{cat_name} ({client_names})")
            for ps in clients.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="http_client_divergence",
            detail=f"Mixed HTTP client approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # HTTP client gap — backend projects with no HTTP client
    has_clients = {p.name for p in projects if p.tech_stack.http_clients}
    if has_clients:
        no_clients = [p.name for p in projects
                      if not p.tech_stack.http_clients
                      and p.source_file_count > 20
                      and any(f in p.tech_stack.frameworks
                              for f in ("FastAPI", "Django", "Flask", "Express",
                                        "NestJS", "Spring Boot", "Gin", "Echo",
                                        "Actix", "Axum", "Fiber"))]
        if no_clients:
            connections.append(Connection(
                type="http_client_gap",
                detail=f"{len(no_clients)} backend project(s) have no HTTP client library detected",
                projects=sorted(no_clients),
                severity="info",
            ))

    return connections[:10]


def _find_doc_generator_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project documentation generator patterns."""
    connections: list[Connection] = []

    # Shared doc generators — same tool used by 2+ projects
    gen_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for g in p.tech_stack.doc_generators:
            gen_to_projects[g].append(p.name)

    for g, projs in sorted(gen_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_doc_generator",
                detail=f"{g} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Doc generator divergence — different paradigms
    static_site = {"Docusaurus", "VitePress", "Nextra", "GitBook", "Docsify",
                   "Mintlify", "Starlight", "mdBook"}
    api_docs = {"Sphinx", "TypeDoc", "JSDoc", "pdoc", "pydoctor", "Javadoc",
                "Dokka", "Doxygen", "Swag", "rustdoc", "documentation.js"}
    component_docs = {"Storybook"}
    config_docs = {"MkDocs"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "static_site": {}, "api_docs": {}, "component_docs": {}, "config_docs": {},
    }
    cat_sets = [
        ("static_site", static_site),
        ("api_docs", api_docs),
        ("component_docs", component_docs),
        ("config_docs", config_docs),
    ]
    for p in projects:
        for g in p.tech_stack.doc_generators:
            for cat_name, cat_set in cat_sets:
                if g in cat_set:
                    cat_found[cat_name].setdefault(g, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, gens in active_cats.items():
            gen_names = ", ".join(sorted(gens.keys())[:3])
            parts.append(f"{cat_name} ({gen_names})")
            for ps in gens.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="doc_generator_divergence",
            detail=f"Mixed doc generation approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Doc generator gap — projects with 20+ source files but no doc generator
    has_docs = {p.name for p in projects if p.tech_stack.doc_generators}
    if has_docs:
        no_docs = [p.name for p in projects
                   if not p.tech_stack.doc_generators
                   and p.source_file_count > 20]
        if no_docs:
            connections.append(Connection(
                type="doc_generator_gap",
                detail=f"{len(no_docs)} project(s) with 20+ source files have no documentation generation tooling",
                projects=sorted(no_docs),
                severity="info",
            ))

    return connections[:10]


def _find_cli_framework_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project CLI framework patterns."""
    connections: list[Connection] = []

    # Shared CLI frameworks — same framework used by 2+ projects
    fw_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for f in p.tech_stack.cli_frameworks:
            fw_to_projects[f].append(p.name)

    for f, projs in sorted(fw_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_cli_framework",
                detail=f"{f} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # CLI framework divergence — different paradigms
    declarative = {"Click", "Typer", "Cobra", "clap", "StructOpt", "Commander.js",
                   "Yargs", "oclif", "picocli", "JCommander", "urfave/cli",
                   "Kong", "argh", "meow", "Caporal", "Clipanion", "pflag",
                   "go-flags", "Fire", "Airline", "Spring Shell", "citty",
                   "docopt", "plac", "Cement", "cliff", "Cleo", "Vorpal",
                   "Gluegun"}
    tui = {"Rich", "Textual", "Bubbletea", "Lip Gloss", "Huh", "Ink",
           "Ratatui", "dialoguer", "indicatif", "console", "Chalk", "Ora",
           "prompt_toolkit", "Questionary", "InquirerPy", "Inquirer.js",
           "prompts", "Trogon"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "declarative": {}, "tui": {},
    }
    cat_sets = [("declarative", declarative), ("tui", tui)]
    for p in projects:
        for f in p.tech_stack.cli_frameworks:
            for cat_name, cat_set in cat_sets:
                if f in cat_set:
                    cat_found[cat_name].setdefault(f, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, fws in active_cats.items():
            fw_names = ", ".join(sorted(fws.keys())[:3])
            parts.append(f"{cat_name} ({fw_names})")
            for ps in fws.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="cli_framework_divergence",
            detail=f"Mixed CLI approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_config_tool_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project configuration management patterns."""
    connections: list[Connection] = []

    # Shared config tools — same tool used by 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for t in p.tech_stack.config_tools:
            tool_to_projects[t].append(p.name)

    for t, projs in sorted(tool_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_config_tool",
                detail=f"{t} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Config tool divergence — different paradigms
    env_based = {"python-dotenv", "dotenv", "godotenv", "dotenvy", "dotenv-java",
                 "python-decouple", "environs", "envalid", "env-cmd", "cross-env",
                 "envconfig", "env", "cleanenv", "envy", "t3-env"}
    structured = {"Dynaconf", "Hydra", "OmegaConf", "Pydantic Settings", "Convict",
                  "node-config", "Viper", "koanf", "config-rs", "Figment",
                  "Spring Config", "Typesafe Config", "Commons Configuration",
                  "ConfigObj", "Confuse", "Everett", "nconf", "cosmiconfig", "rc"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "env_based": {}, "structured": {},
    }
    cat_sets = [("env_based", env_based), ("structured", structured)]
    for p in projects:
        for t in p.tech_stack.config_tools:
            for cat_name, cat_set in cat_sets:
                if t in cat_set:
                    cat_found[cat_name].setdefault(t, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, fws in active_cats.items():
            fw_names = ", ".join(sorted(fws.keys())[:3])
            parts.append(f"{cat_name} ({fw_names})")
            for ps in fws.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="config_tool_divergence",
            detail=f"Mixed config approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Config tool gap — backend projects without config management
    for p in projects:
        has_backend = (
            any(lang in p.tech_stack.languages for lang in ("Python", "Go", "Java", "Rust"))
            or any(fw in p.tech_stack.frameworks for fw in ("FastAPI", "Django", "Flask", "Express", "NestJS", "Spring Boot", "Gin", "Echo", "Actix", "Rails"))
        )
        if has_backend and not p.tech_stack.config_tools and p.source_file_count >= 5:
            connections.append(Connection(
                type="config_tool_gap",
                detail=f"{p.name} is a backend project with no config management tool detected",
                projects=[p.name],
                severity="info",
            ))

    return connections[:10]


def _find_caching_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project caching library patterns."""
    connections: list[Connection] = []

    # Shared caching tools — same tool used by 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for t in p.tech_stack.caching_tools:
            tool_to_projects[t].append(p.name)

    for t, projs in sorted(tool_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_caching_tool",
                detail=f"{t} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Caching divergence — different paradigms
    redis_based = {"redis-py", "ioredis", "redis (Node)", "go-redis", "redis-rs",
                   "django-redis", "Jedis", "Lettuce", "Redisson"}
    in_memory = {"cachetools", "DiskCache", "node-cache", "lru-cache", "Ristretto",
                 "BigCache", "FreeCache", "GCache", "groupcache", "moka", "cached",
                 "mini-moka", "Caffeine", "Ehcache", "Guava Cache", "Hazelcast",
                 "cache-manager", "catbox", "Keyv"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "redis_based": {}, "in_memory": {},
    }
    cat_sets = [("redis_based", redis_based), ("in_memory", in_memory)]
    for p in projects:
        for t in p.tech_stack.caching_tools:
            for cat_name, cat_set in cat_sets:
                if t in cat_set:
                    cat_found[cat_name].setdefault(t, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, fws in active_cats.items():
            fw_names = ", ".join(sorted(fws.keys())[:3])
            parts.append(f"{cat_name} ({fw_names})")
            for ps in fws.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="caching_divergence",
            detail=f"Mixed caching approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    # Caching gap — backend projects with databases but no caching
    for p in projects:
        has_backend = (
            any(lang in p.tech_stack.languages for lang in ("Python", "Go", "Java", "Rust"))
            or any(fw in p.tech_stack.frameworks for fw in ("FastAPI", "Django", "Flask", "Express", "NestJS", "Spring Boot", "Gin", "Echo", "Actix", "Rails"))
        )
        has_db = bool(p.tech_stack.databases)
        if has_backend and has_db and not p.tech_stack.caching_tools and p.source_file_count >= 10:
            connections.append(Connection(
                type="caching_gap",
                detail=f"{p.name} uses databases but has no caching layer detected",
                projects=[p.name],
                severity="info",
            ))

    return connections[:10]


def _find_template_engine_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project template engine patterns."""
    connections: list[Connection] = []

    # Shared template engines — same engine used by 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for t in p.tech_stack.template_engines:
            tool_to_projects[t].append(p.name)

    for t, projs in sorted(tool_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_template_engine",
                detail=f"{t} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Template engine divergence — different paradigms
    string_based = {"Jinja2", "Mako", "Chameleon", "Genshi", "Cheetah", "Django Templates",
                    "Handlebars", "EJS", "Pug", "Nunjucks", "Mustache", "Liquid", "Eta",
                    "Edge.js", "Marko", "Tera", "Askama", "Handlebars (Rust)", "MiniJinja",
                    "Pongo2", "Raymond", "Jet", "Amber", "Thymeleaf", "FreeMarker",
                    "Velocity", "Mustache (Java)", "Pebble", "Go Templates"}
    component_based = {"Vue SFC", "Svelte", "Solid", "Astro", "Maud"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "string_based": {}, "component_based": {},
    }
    cat_sets = [("string_based", string_based), ("component_based", component_based)]
    for p in projects:
        for t in p.tech_stack.template_engines:
            for cat_name, cat_set in cat_sets:
                if t in cat_set:
                    cat_found[cat_name].setdefault(t, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, fws in active_cats.items():
            fw_names = ", ".join(sorted(fws.keys())[:3])
            parts.append(f"{cat_name} ({fw_names})")
            for ps in fws.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="template_engine_divergence",
            detail=f"Mixed template approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_serialization_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project serialization format patterns."""
    connections: list[Connection] = []

    # Shared serialization formats — same format used by 2+ projects
    fmt_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for f in p.tech_stack.serialization_formats:
            fmt_to_projects[f].append(p.name)

    for f, projs in sorted(fmt_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_serialization_format",
                detail=f"{f} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Serialization divergence — binary vs text-based formats
    binary_formats = {"Protocol Buffers", "MessagePack", "Apache Avro", "Apache Thrift",
                      "FlatBuffers", "CBOR", "Bincode", "Postcard", "Pickle", "Apache Arrow",
                      "Parquet", "BSON", "Kryo"}
    text_formats = {"YAML", "TOML", "Jackson", "Gson", "orjson", "ujson", "serde_json",
                    "simd-json", "go-json", "superjson"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "binary": {}, "text_based": {},
    }
    cat_sets = [("binary", binary_formats), ("text_based", text_formats)]
    for p in projects:
        for f in p.tech_stack.serialization_formats:
            for cat_name, cat_set in cat_sets:
                if f in cat_set:
                    cat_found[cat_name].setdefault(f, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, fws in active_cats.items():
            fw_names = ", ".join(sorted(fws.keys())[:3])
            parts.append(f"{cat_name} ({fw_names})")
            for ps in fws.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="serialization_divergence",
            detail=f"Mixed serialization approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_di_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project dependency injection patterns."""
    connections: list[Connection] = []

    # Shared DI frameworks — same framework used by 2+ projects
    fw_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for f in p.tech_stack.di_frameworks:
            fw_to_projects[f].append(p.name)

    for f, projs in sorted(fw_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_di_framework",
                detail=f"{f} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # DI divergence — container-based vs implicit/manual
    container_based = {"dependency-injector", "InversifyJS", "tsyringe", "TypeDI", "Awilix",
                       "BottleJS", "injection-js", "Angular DI", "NestJS DI", "Spring DI",
                       "Google Guice", "Dagger", "CDI", "Micronaut DI", "Quarkus CDI",
                       "Uber Fx", "Uber Dig", "Shaku"}
    implicit_based = {"FastAPI Depends", "python-inject", "Lagom", "punq", "wireup",
                      "svcs", "dishka", "Wire", "do", "inject"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "container_based": {}, "implicit": {},
    }
    cat_sets = [("container_based", container_based), ("implicit", implicit_based)]
    for p in projects:
        for f in p.tech_stack.di_frameworks:
            for cat_name, cat_set in cat_sets:
                if f in cat_set:
                    cat_found[cat_name].setdefault(f, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, fws in active_cats.items():
            fw_names = ", ".join(sorted(fws.keys())[:3])
            parts.append(f"{cat_name} ({fw_names})")
            for ps in fws.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="di_divergence",
            detail=f"Mixed DI approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_websocket_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project WebSocket library patterns."""
    connections: list[Connection] = []

    # Shared WebSocket libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.websocket_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_websocket_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # WebSocket divergence — managed/hosted vs self-hosted
    managed_services = {"Pusher", "Ably", "Centrifugo", "Action Cable", "Phoenix Channels"}
    self_hosted = {"websockets", "Socket.IO", "ws", "SockJS", "Primus", "Gorilla WebSocket",
                   "nhooyr/websocket", "gobwas/ws", "Tungstenite", "Spring WebSocket",
                   "Jakarta WebSocket", "Django Channels", "python-socketio",
                   "Starlette WebSocket", "Tornado WebSocket", "Autobahn", "aiohttp WebSocket",
                   "wsproto", "Melody", "Axum WebSocket", "Actix WebSocket", "Warp WebSocket",
                   "tRPC WebSocket", "graphql-ws", "Tyrus", "Netty WebSocket", "Undertow WebSocket"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "managed": {}, "self_hosted": {},
    }
    cat_sets = [("managed", managed_services), ("self_hosted", self_hosted)]
    for p in projects:
        for lib in p.tech_stack.websocket_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, libs in active_cats.items():
            lib_names = ", ".join(sorted(libs.keys())[:3])
            parts.append(f"{cat_name} ({lib_names})")
            for ps in libs.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="websocket_divergence",
            detail=f"Mixed WebSocket approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_graphql_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project GraphQL library patterns."""
    connections: list[Connection] = []

    # Shared GraphQL libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.graphql_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_graphql_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # GraphQL divergence — server-first vs client-first
    server_libs = {"Apollo Server", "GraphQL Yoga", "Mercurius", "TypeGraphQL", "Nexus", "Pothos",
                   "Graphene", "Graphene-Django", "Ariadne", "Strawberry", "Tartiflette",
                   "gqlgen", "graphql-go", "graph-gophers", "Thunder",
                   "Juniper", "async-graphql",
                   "graphql-java", "GraphQL Spring", "Netflix DGS", "SmallRye GraphQL"}
    client_libs = {"Apollo Client", "URQL", "Relay", "graphql-request", "gql", "sgqlc",
                   "graphql-client", "Cynic", "genqlient", "graphql-kotlin"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "server_first": {}, "client_first": {},
    }
    cat_sets = [("server_first", server_libs), ("client_first", client_libs)]
    for p in projects:
        for lib in p.tech_stack.graphql_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, libs in active_cats.items():
            lib_names = ", ".join(sorted(libs.keys())[:3])
            parts.append(f"{cat_name} ({lib_names})")
            for ps in libs.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="graphql_divergence",
            detail=f"Mixed GraphQL approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_event_streaming_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project event streaming patterns."""
    connections: list[Connection] = []

    # Shared event streaming tools — same tool used by 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.event_streaming:
            tool_to_projects[tool].append(p.name)

    for tool, projs in sorted(tool_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_event_streaming",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Event streaming divergence — kafka-based vs amqp-based vs cloud-managed
    kafka_tools = {"Confluent Kafka", "kafka-python", "aiokafka", "KafkaJS", "kafka-go",
                   "Confluent Kafka (Go)", "Sarama", "rdkafka", "Spring Kafka", "Kafka Clients",
                   "Faust"}
    amqp_tools = {"RabbitMQ (pika)", "RabbitMQ (aio-pika)", "Kombu", "RabbitMQ (amqplib)",
                  "AMQP (rhea)", "RabbitMQ (Go)", "RabbitMQ (lapin)", "Spring AMQP",
                  "Spring RabbitMQ", "BullMQ"}
    cloud_tools = {"Google Pub/Sub", "AWS SQS", "AWS SNS", "AWS Kinesis",
                   "Azure Event Hubs", "Azure Service Bus", "AWS SQS (Java)",
                   "AWS Kinesis (Java)"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "kafka_based": {}, "amqp_based": {}, "cloud_managed": {},
    }
    cat_sets = [("kafka_based", kafka_tools), ("amqp_based", amqp_tools), ("cloud_managed", cloud_tools)]
    for p in projects:
        for tool in p.tech_stack.event_streaming:
            for cat_name, cat_set in cat_sets:
                if tool in cat_set:
                    cat_found[cat_name].setdefault(tool, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="event_streaming_divergence",
            detail=f"Mixed streaming approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_payment_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project payment and billing patterns."""
    connections: list[Connection] = []

    # Shared payment tools — same tool used by 2+ projects
    tool_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for tool in p.tech_stack.payment_tools:
            tool_to_projects[tool].append(p.name)

    for tool, projs in sorted(tool_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_payment_tool",
                detail=f"{tool} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Payment divergence — traditional vs merchant-of-record
    traditional = {"Stripe", "PayPal", "Braintree", "Square", "Adyen", "Razorpay",
                   "Mollie", "GoCardless", "Paystack", "Flutterwave", "Coinbase Commerce"}
    merchant_of_record = {"Paddle", "Lemon Squeezy", "Chargebee", "Recurly"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "traditional": {}, "merchant_of_record": {},
    }
    cat_sets = [("traditional", traditional), ("merchant_of_record", merchant_of_record)]
    for p in projects:
        for tool in p.tech_stack.payment_tools:
            for cat_name, cat_set in cat_sets:
                if tool in cat_set:
                    cat_found[cat_name].setdefault(tool, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="payment_divergence",
            detail=f"Mixed payment approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_date_lib_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project date/time library patterns."""
    connections: list[Connection] = []

    # Shared date libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.date_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_date_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Date lib divergence — modern vs legacy
    modern = {"Day.js", "date-fns", "Luxon", "Temporal", "Tempo", "Arrow", "Pendulum",
              "chrono", "time", "Spacetime"}
    legacy = {"Moment.js", "Joda-Time", "python-dateutil", "pytz"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "modern": {}, "legacy": {},
    }
    cat_sets = [("modern", modern), ("legacy", legacy)]
    for p in projects:
        for lib in p.tech_stack.date_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="date_lib_divergence",
            detail=f"Mixed date/time approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_image_lib_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project image processing library patterns."""
    connections: list[Connection] = []

    # Shared image libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.image_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_image_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Image lib divergence — native/low-level vs high-level/managed
    high_level = {"Pillow", "Sharp", "Jimp", "imaging", "image", "Thumbnailator",
                  "imgscalr", "Scrimage", "imageio", "Wand", "BlurHash", "Plaiceholder"}
    low_level = {"OpenCV", "GoCV", "scikit-image", "imageproc", "pyvips", "rawpy",
                 "node-canvas", "napi-canvas", "CairoSVG", "resvg"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "high_level": {}, "low_level": {},
    }
    cat_sets = [("high_level", high_level), ("low_level", low_level)]
    for p in projects:
        for lib in p.tech_stack.image_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="image_lib_divergence",
            detail=f"Mixed imaging approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_data_viz_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project data visualization library patterns."""
    connections: list[Connection] = []

    # Shared data viz libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.data_viz_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_data_viz",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Data viz divergence — dashboard/interactive vs static/notebook
    interactive = {"Dash", "Streamlit", "Gradio", "Panel", "Bokeh", "D3.js",
                   "ECharts", "Highcharts", "ApexCharts", "Recharts", "Nivo",
                   "Victory", "Visx", "Three.js", "Deck.gl", "Tremor",
                   "go-echarts", "pyecharts", "Plotly", "Plotly.js", "Chart.js",
                   "Ant Charts", "Lightweight Charts", "Observable Plot"}
    static = {"Matplotlib", "Seaborn", "Altair", "plotnine", "Pygal",
              "Plotext", "Gonum Plot", "Plotters", "plotlib", "JFreeChart",
              "XChart", "textplots", "charming"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "interactive": {}, "static": {},
    }
    cat_sets = [("interactive", interactive), ("static", static)]
    for p in projects:
        for lib in p.tech_stack.data_viz_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="data_viz_divergence",
            detail=f"Mixed visualization approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_geo_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project geospatial library patterns."""
    connections: list[Connection] = []

    # Shared geo libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.geo_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_geo_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Geo lib divergence — mapping/visualization vs analysis/computation
    mapping = {"Leaflet", "Mapbox GL", "MapLibre GL", "OpenLayers", "Cesium",
               "Google Maps", "React Leaflet", "react-map-gl", "Mapbox",
               "HERE Maps", "Kepler.gl"}
    analysis = {"GeoPandas", "Shapely", "Fiona", "rasterio", "GDAL", "pyproj",
                "GeoAlchemy2", "Turf.js", "orb", "go-geom", "geo", "geozero",
                "GeoTools", "JTS", "Spatial4j", "Cartopy", "xarray"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "mapping": {}, "analysis": {},
    }
    cat_sets = [("mapping", mapping), ("analysis", analysis)]
    for p in projects:
        for lib in p.tech_stack.geo_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="geo_lib_divergence",
            detail=f"Mixed geo approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_media_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project audio/video media library patterns."""
    connections: list[Connection] = []

    # Shared media libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.media_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_media_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Media lib divergence — audio processing vs video/streaming
    audio = {"Pydub", "Librosa", "SoundFile", "PyAudio", "audioread", "sounddevice",
             "Pedalboard", "torchaudio", "aubio", "madmom", "Essentia", "music21",
             "Tone.js", "Howler.js", "WaveSurfer.js", "Pizzicato", "music-metadata",
             "Beep", "Oto", "Rodio", "CPAL", "Symphonia", "dasp",
             "TarsosDSP", "Tritonus", "JLayer"}
    video = {"MoviePy", "PyAV", "Decord", "VidGear",
             "Video.js", "Plyr", "HLS.js", "DASH.js", "Shaka Player",
             "Mediasoup", "SimplePeer", "PeerJS",
             "Ebiten", "GoAV", "go-dash", "GStreamer",
             "JavaCV", "JCodec", "Xuggler", "JAVE"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "audio": {}, "video": {},
    }
    cat_sets = [("audio", audio), ("video", video)]
    for p in projects:
        for lib in p.tech_stack.media_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="media_lib_divergence",
            detail=f"Mixed media approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_math_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project math and scientific computing library patterns."""
    connections: list[Connection] = []

    # Shared math libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.math_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_math_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Math lib divergence — numerical/array vs statistical/ML
    numerical = {"NumPy", "SciPy", "Numba", "CuPy", "JAX", "Dask", "Modin", "Vaex",
                 "Polars", "math.js", "Numeric.js", "ndarray", "stdlib",
                 "Gonum", "sparse", "nalgebra", "ndarray", "peroxide",
                 "Commons Math", "EJML", "ND4J"}
    statistical = {"statsmodels", "scikit-learn", "PyMC", "ArviZ", "CVXPY",
                   "simple-statistics", "jStat", "ML-Matrix",
                   "stats", "statrs", "Linfa", "Smile", "Tablesaw",
                   "TensorFlow.js", "Danfo.js", "Arquero", "NetworkX"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "numerical": {}, "statistical": {},
    }
    cat_sets = [("numerical", numerical), ("statistical", statistical)]
    for p in projects:
        for lib in p.tech_stack.math_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="math_lib_divergence",
            detail=f"Mixed math/sci approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_async_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project concurrency and async library patterns."""
    connections: list[Connection] = []

    # Shared async libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.async_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_async_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Async lib divergence — event-loop/reactive vs thread-pool/parallel
    reactive = {"Twisted", "trio", "AnyIO", "Gevent", "uvloop", "Curio",
                "RxJS", "Bluebird", "observable-fns",
                "Tokio", "async-std", "smol", "futures",
                "RxJava", "Project Reactor", "Akka", "Vert.x",
                "Kotlin Coroutines"}
    parallel = {"Celery", "multiprocessing", "concurrent.futures", "Greenlet",
                "aiomultiprocess", "workerpool", "threads.js", "Comlink",
                "Piscina", "Tinypool", "p-queue", "p-limit",
                "x/sync", "conc", "ants", "pond",
                "Rayon", "Crossbeam", "flume", "Quasar"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "reactive": {}, "parallel": {},
    }
    cat_sets = [("reactive", reactive), ("parallel", parallel)]
    for p in projects:
        for lib in p.tech_stack.async_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="async_lib_divergence",
            detail=f"Mixed async approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_crypto_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project cryptography library patterns."""
    connections: list[Connection] = []

    # Shared crypto libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.crypto_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_crypto_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # Crypto lib divergence — high-level/password hashing vs low-level/primitives
    high_level = {"bcrypt", "Passlib", "Argon2", "bcrypt.js", "argon2",
                  "Bouncy Castle", "Jasypt", "Tink", "Conscrypt",
                  "Spring Security Crypto", "jose", "jsonwebtoken",
                  "PyNaCl", "libsodium", "TweetNaCl", "OpenPGP.js",
                  "noble-curves", "noble-hashes", "age", "CIRCL"}
    low_level = {"cryptography", "PyCryptodome", "pyOpenSSL",
                 "CryptoJS", "node-forge", "WebCrypto", "scrypt-js",
                 "x/crypto", "ring", "rustls", "Orion", "sodiumoxide",
                 "sha2", "aes-gcm", "rust-crypto", "rcgen",
                 "x/oauth2", "Paramiko", "certifi", "truststore",
                 "hmac", "hashlib", "jwcrypto"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "high-level": {}, "low-level": {},
    }
    cat_sets = [("high-level", high_level), ("low-level", low_level)]
    for p in projects:
        for lib in p.tech_stack.crypto_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="crypto_lib_divergence",
            detail=f"Mixed crypto approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]


def _find_pdf_patterns(projects: list[Project]) -> list[Connection]:
    """Find cross-project PDF and document library patterns."""
    connections: list[Connection] = []

    # Shared PDF/doc libs — same lib used by 2+ projects
    lib_to_projects: dict[str, list[str]] = defaultdict(list)
    for p in projects:
        for lib in p.tech_stack.pdf_libs:
            lib_to_projects[lib].append(p.name)

    for lib, projs in sorted(lib_to_projects.items()):
        if len(projs) >= 2:
            connections.append(Connection(
                type="shared_pdf_lib",
                detail=f"{lib} used in {len(projs)} projects",
                projects=sorted(projs),
                severity="info",
            ))

    # PDF lib divergence — generation/creation vs parsing/extraction
    generation = {"ReportLab", "FPDF2", "FPDF", "WeasyPrint", "xhtml2pdf",
                  "borb", "python-docx", "openpyxl", "XlsxWriter", "python-pptx",
                  "PDFKit", "pdf-lib", "jsPDF", "pdfmake", "React-PDF",
                  "docx", "ExcelJS", "gofpdf", "goPDF", "UniPDF",
                  "printpdf", "genpdf", "iText", "OpenPDF", "JasperReports",
                  "Apache POI", "Excelize", "Pandoc"}
    extraction = {"pypdf", "PyPDF2", "pdfplumber", "PyMuPDF", "PDFMiner",
                  "Camelot", "tabula-py", "pikepdf",
                  "PDF.js", "pdfjs-dist", "SheetJS", "PapaParse", "csv-parse",
                  "Puppeteer", "Playwright", "react-pdf",
                  "pdfcpu", "lopdf", "pdf-extract", "calamine",
                  "Apache PDFBox"}

    cat_found: dict[str, dict[str, set[str]]] = {
        "generation": {}, "extraction": {},
    }
    cat_sets = [("generation", generation), ("extraction", extraction)]
    for p in projects:
        for lib in p.tech_stack.pdf_libs:
            for cat_name, cat_set in cat_sets:
                if lib in cat_set:
                    cat_found[cat_name].setdefault(lib, set()).add(p.name)

    active_cats = {k: v for k, v in cat_found.items() if v}
    if len(active_cats) >= 2:
        parts = []
        all_projs: set[str] = set()
        for cat_name, tools in active_cats.items():
            tool_names = ", ".join(sorted(tools.keys())[:3])
            parts.append(f"{cat_name} ({tool_names})")
            for ps in tools.values():
                all_projs.update(ps)
        connections.append(Connection(
            type="pdf_lib_divergence",
            detail=f"Mixed PDF approaches: {'; '.join(parts)} — consider standardizing",
            projects=sorted(all_projs),
            severity="warning",
        ))

    return connections[:10]
