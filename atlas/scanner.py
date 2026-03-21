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
