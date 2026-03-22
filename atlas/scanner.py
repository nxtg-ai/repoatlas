"""Project scanner — orchestrates detection and produces Project objects."""
from __future__ import annotations

import subprocess
from pathlib import Path

from atlas.detector import (
    count_files,
    count_loc,
    count_test_files,
    detect_ai_tools,
    detect_databases,
    detect_frameworks,
    detect_infrastructure,
    detect_key_deps,
    detect_languages,
    detect_quality_tools,
    detect_security_tools,
    detect_testing_frameworks,
    detect_package_managers,
    detect_license,
    detect_docs_artifacts,
    detect_ci_config,
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
)
from atlas.health import compute_health
from atlas.models import GitInfo, Project, TechStack


def scan_project(project_path: Path) -> Project:
    """Scan a single project directory and return a Project object."""
    path = project_path.resolve()
    name = path.name

    languages = detect_languages(path)
    frameworks = detect_frameworks(path)
    databases = detect_databases(path)
    key_deps = detect_key_deps(path)
    infrastructure = detect_infrastructure(path)
    security_tools = detect_security_tools(path)
    ai_tools = detect_ai_tools(path)
    quality_tools = detect_quality_tools(path)
    testing_frameworks = detect_testing_frameworks(path)
    package_managers = detect_package_managers(path)
    project_license = detect_license(path)
    docs_artifacts = detect_docs_artifacts(path)
    ci_config = detect_ci_config(path)
    runtime_versions = detect_runtime_versions(path)
    build_tools = detect_build_tools(path)
    api_specs = detect_api_specs(path)
    monitoring_tools = detect_monitoring_tools(path)
    auth_tools = detect_auth_tools(path)
    messaging_tools = detect_messaging_tools(path)
    deploy_targets = detect_deploy_targets(path)
    state_management = detect_state_management(path)
    css_frameworks = detect_css_frameworks(path)
    bundlers = detect_bundlers(path)
    orm_tools = detect_orm_tools(path)
    i18n_tools = detect_i18n_tools(path)
    validation_tools = detect_validation_tools(path)
    logging_tools = detect_logging_tools(path)
    container_orchestration = detect_container_orchestration(path)
    cloud_providers = detect_cloud_providers(path)
    task_queues = detect_task_queues(path)
    search_engines = detect_search_engines(path)
    feature_flags = detect_feature_flags(path)
    http_clients = detect_http_clients(path)
    doc_generators = detect_doc_generators(path)
    cli_frameworks = detect_cli_frameworks(path)
    config_tools = detect_config_tools(path)
    caching_tools = detect_caching_tools(path)
    template_engines = detect_template_engines(path)
    serialization_formats = detect_serialization_formats(path)
    di_frameworks = detect_di_frameworks(path)
    websocket_libs = detect_websocket_libs(path)
    graphql_libs = detect_graphql_libs(path)
    event_streaming = detect_event_streaming(path)
    payment_tools = detect_payment_tools(path)
    date_libs = detect_date_libs(path)
    image_libs = detect_image_libs(path)
    crypto_libs = detect_crypto_libs(path)
    pdf_libs = detect_pdf_libs(path)
    data_viz_libs = detect_data_viz_libs(path)
    geo_libs = detect_geo_libs(path)
    media_libs = detect_media_libs(path)
    math_libs = detect_math_libs(path)
    async_libs = detect_async_libs(path)
    compression_libs = detect_compression_libs(path)
    email_libs = detect_email_libs(path)
    a11y_tools = detect_a11y_tools(path)
    source_files, total_files = count_files(path)
    test_files = count_test_files(path)
    loc = count_loc(path)
    git_info = _get_git_info(path)

    tech_stack = TechStack(
        languages=languages,
        frameworks=frameworks,
        databases=databases,
        key_deps=key_deps,
        infrastructure=infrastructure,
        security_tools=security_tools,
        ai_tools=ai_tools,
        quality_tools=quality_tools,
        testing_frameworks=testing_frameworks,
        package_managers=package_managers,
        docs_artifacts=docs_artifacts,
        ci_config=ci_config,
        runtime_versions=runtime_versions,
        build_tools=build_tools,
        api_specs=api_specs,
        monitoring_tools=monitoring_tools,
        auth_tools=auth_tools,
        messaging_tools=messaging_tools,
        deploy_targets=deploy_targets,
        state_management=state_management,
        css_frameworks=css_frameworks,
        bundlers=bundlers,
        orm_tools=orm_tools,
        i18n_tools=i18n_tools,
        validation_tools=validation_tools,
        logging_tools=logging_tools,
        container_orchestration=container_orchestration,
        cloud_providers=cloud_providers,
        task_queues=task_queues,
        search_engines=search_engines,
        feature_flags=feature_flags,
        http_clients=http_clients,
        doc_generators=doc_generators,
        cli_frameworks=cli_frameworks,
        config_tools=config_tools,
        caching_tools=caching_tools,
        template_engines=template_engines,
        serialization_formats=serialization_formats,
        di_frameworks=di_frameworks,
        websocket_libs=websocket_libs,
        graphql_libs=graphql_libs,
        event_streaming=event_streaming,
        payment_tools=payment_tools,
        date_libs=date_libs,
        image_libs=image_libs,
        crypto_libs=crypto_libs,
        pdf_libs=pdf_libs,
        data_viz_libs=data_viz_libs,
        geo_libs=geo_libs,
        media_libs=media_libs,
        math_libs=math_libs,
        async_libs=async_libs,
        compression_libs=compression_libs,
        email_libs=email_libs,
        a11y_tools=a11y_tools,
    )

    project = Project(
        name=name,
        path=str(path),
        tech_stack=tech_stack,
        git_info=git_info,
        test_file_count=test_files,
        source_file_count=source_files,
        total_file_count=total_files,
        loc=loc,
        license=project_license,
    )

    project.health = compute_health(project)
    return project


def _get_git_info(project_path: Path) -> GitInfo:
    """Extract git information from the project."""
    info = GitInfo()
    git_dir = project_path / ".git"
    if not git_dir.exists():
        return info

    def _run(cmd: list[str]) -> str:
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                cwd=project_path, timeout=10,
            )
            return result.stdout.strip() if result.returncode == 0 else ""
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return ""

    info.branch = _run(["git", "branch", "--show-current"]) or "detached"

    log_output = _run(["git", "log", "-1", "--format=%ci|||%s"])
    if "|||" in log_output:
        date, msg = log_output.split("|||", 1)
        info.last_commit_date = date.strip()
        info.last_commit_msg = msg.strip()[:80]

    commit_count = _run(["git", "rev-list", "--count", "HEAD"])
    if commit_count.isdigit():
        info.total_commits = int(commit_count)

    status = _run(["git", "status", "--porcelain"])
    info.uncommitted_changes = len(status.splitlines()) if status else 0

    remotes = _run(["git", "remote"])
    info.has_remote = bool(remotes)

    return info
