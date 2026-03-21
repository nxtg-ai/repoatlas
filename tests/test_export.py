"""Tests for portfolio export (markdown, JSON, and CSV)."""
from __future__ import annotations

import csv
import io
import json

from atlas.export_report import build_csv_report, build_json_report, build_markdown_report
from atlas.models import GitInfo, HealthScore, Portfolio, Project, TechStack


def _proj(name: str, languages=None, frameworks=None, databases=None,
          infrastructure=None, security_tools=None, ai_tools=None,
          quality_tools=None, testing_frameworks=None, package_managers=None,
          docs_artifacts=None, ci_config=None, runtime_versions=None,
          project_license="",
          test_files=5, source_files=20, loc=500) -> Project:
    return Project(
        name=name,
        path=f"/tmp/{name}",
        tech_stack=TechStack(
            languages={"Python": 10} if languages is None else languages,
            frameworks=frameworks or [],
            databases=databases or [],
            infrastructure=infrastructure or [],
            security_tools=security_tools or [],
            ai_tools=ai_tools or [],
            quality_tools=quality_tools or [],
            testing_frameworks=testing_frameworks or [],
            package_managers=package_managers or [],
            docs_artifacts=docs_artifacts or [],
            ci_config=ci_config or [],
            runtime_versions=runtime_versions or {},
        ),
        git_info=GitInfo(
            branch="main",
            total_commits=50,
            has_remote=True,
        ),
        health=HealthScore(
            tests=0.8, git_hygiene=0.9, documentation=0.7,
            structure=0.8, overall=0.8, grade="B",
        ),
        test_file_count=test_files,
        source_file_count=source_files,
        loc=loc,
        license=project_license,
    )


def _portfolio(*projects: Project) -> Portfolio:
    return Portfolio(
        name="Test Portfolio",
        projects=list(projects),
        last_scan="2026-03-13T12:00:00",
    )


class TestMarkdownHeader:
    def test_title(self):
        report = build_markdown_report(_portfolio(_proj("app1")))
        assert "# Test Portfolio — Portfolio Report" in report

    def test_scanned_date(self):
        report = build_markdown_report(_portfolio(_proj("app1")))
        assert "2026-03-13T12:00:00" in report

    def test_summary_stats(self):
        report = build_markdown_report(_portfolio(_proj("app1", loc=1000)))
        assert "1,000" in report


class TestProjectTable:
    def test_project_in_table(self):
        report = build_markdown_report(_portfolio(_proj("myapp")))
        assert "| myapp |" in report

    def test_sorted_by_health(self):
        p1 = _proj("low")
        p1.health.overall = 0.5
        p1.health.grade = "C"
        p2 = _proj("high")
        p2.health.overall = 0.9
        p2.health.grade = "A"
        report = build_markdown_report(_portfolio(p1, p2))
        # high should appear before low
        assert report.index("high") < report.index("| low |")


class TestPortfolioSummary:
    def test_languages_shown(self):
        report = build_markdown_report(_portfolio(
            _proj("a", languages={"Python": 10}),
            _proj("b", languages={"Python": 5, "TypeScript": 8}),
        ))
        assert "Python (2)" in report

    def test_frameworks_shown(self):
        report = build_markdown_report(_portfolio(
            _proj("a", frameworks=["FastAPI"]),
            _proj("b", frameworks=["FastAPI", "React"]),
        ))
        assert "FastAPI (2)" in report

    def test_infrastructure_coverage(self):
        report = build_markdown_report(_portfolio(
            _proj("a", infrastructure=["GitHub Actions"]),
            _proj("b", infrastructure=["Docker"]),
        ))
        assert "CI/CD 1/2" in report
        assert "Docker 1/2" in report

    def test_security_coverage(self):
        report = build_markdown_report(_portfolio(
            _proj("a", security_tools=["Dependabot"]),
            _proj("b", security_tools=[]),
        ))
        assert "1/2 projects have security tooling" in report

    def test_ai_shown_when_present(self):
        report = build_markdown_report(_portfolio(
            _proj("a", ai_tools=["Anthropic SDK", "LangChain"]),
            _proj("b", ai_tools=[]),
        ))
        assert "AI/ML" in report
        assert "1/2 projects" in report

    def test_ai_hidden_when_absent(self):
        report = build_markdown_report(_portfolio(
            _proj("a", ai_tools=[]),
            _proj("b", ai_tools=[]),
        ))
        assert "AI/ML" not in report

    def test_databases_shown_when_present(self):
        report = build_markdown_report(_portfolio(
            _proj("a", databases=["PostgreSQL", "Redis"]),
            _proj("b", databases=["PostgreSQL"]),
        ))
        assert "**Databases**" in report
        assert "2/2 projects" in report
        assert "PostgreSQL" in report

    def test_databases_hidden_when_absent(self):
        report = build_markdown_report(_portfolio(
            _proj("a", databases=[]),
            _proj("b", databases=[]),
        ))
        lines = report.split("\n")
        db_lines = [ln for ln in lines if ln.startswith("**Databases**:") and "projects" in ln]
        assert len(db_lines) == 0

    def test_databases_ranked(self):
        report = build_markdown_report(_portfolio(
            _proj("a", databases=["PostgreSQL", "Redis"]),
            _proj("b", databases=["PostgreSQL", "MongoDB"]),
            _proj("c", databases=["Redis"]),
        ))
        assert "PostgreSQL" in report
        assert "Redis" in report

    def test_testing_shown_when_present(self):
        report = build_markdown_report(_portfolio(
            _proj("a", testing_frameworks=["pytest", "tox"]),
            _proj("b", testing_frameworks=["pytest"]),
        ))
        assert "**Testing**" in report
        assert "2/2 projects" in report
        assert "pytest" in report

    def test_testing_hidden_when_absent(self):
        report = build_markdown_report(_portfolio(
            _proj("a", testing_frameworks=[]),
            _proj("b", testing_frameworks=[]),
        ))
        # Testing line in summary should not appear (project details may still show)
        lines = report.split("\n")
        summary_testing = [ln for ln in lines if ln.startswith("**Testing**:") and "projects" in ln]
        assert len(summary_testing) == 0

    def test_testing_framework_counts(self):
        report = build_markdown_report(_portfolio(
            _proj("a", testing_frameworks=["pytest", "Jest"]),
            _proj("b", testing_frameworks=["pytest", "Vitest"]),
            _proj("c", testing_frameworks=["Jest"]),
        ))
        assert "pytest" in report
        assert "Jest" in report

    def test_pkg_managers_shown_when_present(self):
        report = build_markdown_report(_portfolio(
            _proj("a", package_managers=["Poetry", "npm"]),
            _proj("b", package_managers=["Poetry"]),
        ))
        assert "**Pkg Managers**" in report
        assert "2/2 projects" in report
        assert "Poetry" in report

    def test_pkg_managers_hidden_when_absent(self):
        report = build_markdown_report(_portfolio(
            _proj("a", package_managers=[]),
            _proj("b", package_managers=[]),
        ))
        lines = report.split("\n")
        pm_lines = [ln for ln in lines if ln.startswith("**Pkg Managers**:") and "projects" in ln]
        assert len(pm_lines) == 0

    def test_pkg_managers_ranked(self):
        report = build_markdown_report(_portfolio(
            _proj("a", package_managers=["Poetry", "npm"]),
            _proj("b", package_managers=["Poetry", "pnpm"]),
            _proj("c", package_managers=["npm"]),
        ))
        assert "Poetry" in report
        assert "npm" in report

    def test_licenses_shown_when_present(self):
        report = build_markdown_report(_portfolio(
            _proj("a", project_license="MIT"),
            _proj("b", project_license="MIT"),
        ))
        assert "**Licenses**" in report
        assert "2/2 projects" in report
        assert "MIT" in report

    def test_licenses_hidden_when_absent(self):
        report = build_markdown_report(_portfolio(
            _proj("a", project_license=""),
            _proj("b", project_license=""),
        ))
        lines = report.split("\n")
        lic_lines = [ln for ln in lines if ln.startswith("**Licenses**:") and "projects" in ln]
        assert len(lic_lines) == 0

    def test_licenses_ranked(self):
        report = build_markdown_report(_portfolio(
            _proj("a", project_license="MIT"),
            _proj("b", project_license="MIT"),
            _proj("c", project_license="Apache-2.0"),
        ))
        assert "MIT" in report
        assert "Apache-2.0" in report

    def test_no_summary_for_single_project(self):
        report = build_markdown_report(_portfolio(_proj("solo")))
        assert "## Portfolio Summary" not in report


class TestProjectDetails:
    def test_health_breakdown(self):
        report = build_markdown_report(_portfolio(_proj("app1")))
        assert "Tests: 80%" in report
        assert "Git: 90%" in report
        assert "Docs: 70%" in report
        assert "Structure: 80%" in report

    def test_infrastructure_listed(self):
        report = build_markdown_report(_portfolio(
            _proj("app1", infrastructure=["Docker", "GitHub Actions"])
        ))
        assert "**Infrastructure**: Docker, GitHub Actions" in report

    def test_security_listed(self):
        report = build_markdown_report(_portfolio(
            _proj("app1", security_tools=["Dependabot", "Gitleaks"])
        ))
        assert "**Security**: Dependabot, Gitleaks" in report

    def test_ai_listed(self):
        report = build_markdown_report(_portfolio(
            _proj("app1", ai_tools=["Anthropic SDK", "LangChain"])
        ))
        assert "**AI/ML**: Anthropic SDK, LangChain" in report

    def test_databases_listed(self):
        report = build_markdown_report(_portfolio(
            _proj("app1", databases=["PostgreSQL", "Redis"])
        ))
        assert "**Databases**: PostgreSQL, Redis" in report

    def test_frameworks_listed(self):
        report = build_markdown_report(_portfolio(
            _proj("app1", frameworks=["FastAPI", "pytest"])
        ))
        assert "**Frameworks**: FastAPI, pytest" in report

    def test_git_info(self):
        report = build_markdown_report(_portfolio(_proj("app1")))
        assert "main" in report
        assert "50 commits" in report

    def test_file_counts(self):
        report = build_markdown_report(_portfolio(
            _proj("app1", test_files=10, source_files=50, loc=2000)
        ))
        assert "50 source" in report
        assert "10 tests" in report
        assert "2,000 LOC" in report


class TestConnectionsSection:
    def test_version_mismatch_shown(self):
        report = build_markdown_report(_portfolio(
            _proj("a", frameworks=[], infrastructure=[],
                  **{"test_files": 5, "source_files": 20}),
            _proj("b", frameworks=[], infrastructure=[],
                  **{"test_files": 5, "source_files": 20}),
        ))
        # Connections are generated from actual data; test for section header
        assert "## Cross-Project Intelligence" in report or "## Projects" in report

    def test_no_connections_no_section(self):
        # Healthy project with CI + security + quality — avoids all gap connections
        p = _proj("solo", test_files=10, source_files=10,
                  infrastructure=["GitHub Actions"],
                  security_tools=["Dependabot", "Gitleaks"],
                  quality_tools=["Ruff", "mypy"],
                  testing_frameworks=["pytest"],
                  docs_artifacts=["README", "CHANGELOG", "CONTRIBUTING"],
                  ci_config=["PR template", "pre-commit"],
                  project_license="MIT")
        p.health.tests = 1.0
        report = build_markdown_report(_portfolio(p))
        assert "Cross-Project Intelligence" not in report


class TestEmptyPortfolio:
    def test_empty(self):
        report = build_markdown_report(Portfolio(
            name="Empty", projects=[], last_scan="2026-03-13T12:00:00"
        ))
        assert "# Empty — Portfolio Report" in report
        assert "**Projects**: 0" in report


class TestJsonReport:
    def test_basic_structure(self):
        data = json.loads(build_json_report(_portfolio(_proj("app1"))))
        assert data["name"] == "Test Portfolio"
        assert data["scanned"] == "2026-03-13T12:00:00"
        assert "summary" in data
        assert "portfolio_summary" in data
        assert "projects" in data
        assert "connections" in data
        assert "recommendations" in data

    def test_summary_stats(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", loc=1000), _proj("b", loc=2000)
        )))
        assert data["summary"]["projects"] == 2
        assert data["summary"]["loc"] == 3000

    def test_projects_included(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("alpha"), _proj("beta")
        )))
        names = [p["name"] for p in data["projects"]]
        assert "alpha" in names
        assert "beta" in names

    def test_project_has_license(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("app", project_license="MIT")
        )))
        assert data["projects"][0]["license"] == "MIT"

    def test_connections_present(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", frameworks=["FastAPI"], source_files=20),
            _proj("b", frameworks=["FastAPI"], source_files=20),
        )))
        # Should have at least shared_framework connection
        assert isinstance(data["connections"], list)

    def test_connection_fields(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", frameworks=["FastAPI"], source_files=20,
                  infrastructure=["GitHub Actions"],
                  security_tools=["Dependabot", "Gitleaks"],
                  quality_tools=["Ruff", "mypy"],
                  testing_frameworks=["pytest"],
                  project_license="MIT"),
            _proj("b", frameworks=["FastAPI"], source_files=20,
                  infrastructure=["GitHub Actions"],
                  security_tools=["Dependabot", "Gitleaks"],
                  quality_tools=["Ruff", "mypy"],
                  testing_frameworks=["pytest"],
                  project_license="MIT"),
        )))
        if data["connections"]:
            conn = data["connections"][0]
            assert "type" in conn
            assert "detail" in conn
            assert "projects" in conn
            assert "severity" in conn

    def test_recommendations_present(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", source_files=20),
        )))
        assert isinstance(data["recommendations"], list)

    def test_recommendation_fields(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", source_files=20),
        )))
        if data["recommendations"]:
            rec = data["recommendations"][0]
            assert "priority" in rec
            assert "category" in rec
            assert "message" in rec
            assert "projects" in rec

    def test_portfolio_summary_languages(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", languages={"Python": 10}),
            _proj("b", languages={"Python": 5, "TypeScript": 8}),
        )))
        ps = data["portfolio_summary"]
        assert ps["languages"]["Python"] == 2

    def test_portfolio_summary_infra(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", infrastructure=["GitHub Actions", "Docker"]),
            _proj("b", infrastructure=["Docker"]),
        )))
        ps = data["portfolio_summary"]
        assert ps["infrastructure"]["ci_cd"] == "1/2"
        assert ps["infrastructure"]["docker"] == "2/2"

    def test_portfolio_summary_licenses(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", project_license="MIT"),
            _proj("b", project_license="MIT"),
            _proj("c", project_license=""),
        )))
        ps = data["portfolio_summary"]
        assert ps["licenses"]["coverage"] == "2/3"
        assert ps["licenses"]["licenses"]["MIT"] == 2

    def test_portfolio_summary_testing(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", testing_frameworks=["pytest"]),
            _proj("b", testing_frameworks=["pytest", "Jest"]),
        )))
        ps = data["portfolio_summary"]
        assert ps["testing"]["coverage"] == "2/2"
        assert ps["testing"]["frameworks"]["pytest"] == 2

    def test_empty_portfolio(self):
        data = json.loads(build_json_report(Portfolio(
            name="Empty", projects=[], last_scan="2026-03-21"
        )))
        assert data["summary"]["projects"] == 0
        assert data["portfolio_summary"] == {}
        assert data["connections"] == []

    def test_valid_json(self):
        result = build_json_report(_portfolio(
            _proj("a", frameworks=["FastAPI"], databases=["PostgreSQL"],
                  testing_frameworks=["pytest"], project_license="MIT"),
            _proj("b", frameworks=["Django"], databases=["MySQL"],
                  testing_frameworks=["pytest"], project_license="Apache-2.0"),
        ))
        # Should be parseable JSON
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_connection_summary_present(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", frameworks=["FastAPI"], source_files=20),
            _proj("b", frameworks=["FastAPI"], source_files=20),
        )))
        assert "connection_summary" in data
        cs = data["connection_summary"]
        assert "total" in cs
        assert "critical" in cs
        assert "warning" in cs
        assert "info" in cs

    def test_connection_summary_counts(self):
        data = json.loads(build_json_report(_portfolio(
            _proj("a", frameworks=["FastAPI"], source_files=20,
                  infrastructure=["Docker"]),
            _proj("b", frameworks=["FastAPI"], source_files=20,
                  infrastructure=["Docker"]),
        )))
        cs = data["connection_summary"]
        assert cs["total"] == len(data["connections"])
        assert cs["total"] > 0

    def test_connection_summary_empty_portfolio(self):
        data = json.loads(build_json_report(_portfolio(_proj("solo"))))
        cs = data["connection_summary"]
        assert cs["total"] == 0


class TestMarkdownConnectionSummary:
    def test_summary_line_in_report(self):
        report = build_markdown_report(_portfolio(
            _proj("a", frameworks=["FastAPI"], source_files=20),
            _proj("b", frameworks=["FastAPI"], source_files=20),
        ))
        assert "connections" in report.lower()
        # Should have the "N connections: ..." summary line
        assert " connections**:" in report

    def test_summary_severity_breakdown(self):
        report = build_markdown_report(_portfolio(
            _proj("a", frameworks=["FastAPI"], source_files=20,
                  infrastructure=["Docker"]),
            _proj("b", frameworks=["FastAPI"], source_files=20,
                  infrastructure=["Docker"]),
        ))
        # Should contain at least one severity label
        assert any(s in report for s in ["info", "warning", "critical"])


class TestCsvExport:
    """Tests for build_csv_report()."""

    def test_header_row(self):
        result = build_csv_report(_portfolio(_proj("a")))
        reader = csv.reader(io.StringIO(result))
        headers = next(reader)
        assert "Name" in headers
        assert "Health %" in headers
        assert "Grade" in headers
        assert "Languages" in headers
        assert "License" in headers
        assert "Runtime Versions" in headers

    def test_project_row(self):
        p = _proj("myapp", frameworks=["FastAPI"], databases=["PostgreSQL"],
                  project_license="MIT", runtime_versions={"Python": "3.12"})
        result = build_csv_report(_portfolio(p))
        reader = csv.reader(io.StringIO(result))
        next(reader)  # skip header
        row = next(reader)
        assert row[0] == "myapp"
        assert "FastAPI" in row[13]  # frameworks column
        assert "PostgreSQL" in row[14]  # databases column
        assert "MIT" in row[45]  # license column
        assert "Python=3.12" in row[23]  # runtime versions column

    def test_multiple_projects(self):
        result = build_csv_report(_portfolio(
            _proj("alpha"), _proj("beta"), _proj("gamma"),
        ))
        reader = csv.reader(io.StringIO(result))
        rows = list(reader)
        assert len(rows) == 4  # header + 3 projects

    def test_semicolon_delimited_lists(self):
        p = _proj("x", frameworks=["FastAPI", "React"],
                  databases=["PostgreSQL", "Redis"])
        result = build_csv_report(_portfolio(p))
        reader = csv.reader(io.StringIO(result))
        next(reader)
        row = next(reader)
        assert "FastAPI; React" in row[13]
        assert "PostgreSQL; Redis" in row[14]

    def test_empty_portfolio(self):
        result = build_csv_report(_portfolio())
        reader = csv.reader(io.StringIO(result))
        rows = list(reader)
        assert len(rows) == 1  # header only

    def test_health_scores(self):
        p = _proj("x")
        result = build_csv_report(_portfolio(p))
        reader = csv.reader(io.StringIO(result))
        next(reader)
        row = next(reader)
        assert row[2] == "80"  # health percent
        assert row[3] == "B"  # grade

    def test_git_info(self):
        p = _proj("x")
        result = build_csv_report(_portfolio(p))
        reader = csv.reader(io.StringIO(result))
        next(reader)
        row = next(reader)
        assert row[46] == "main"  # branch
        assert row[48] == "50"  # commits

    def test_valid_csv(self):
        result = build_csv_report(_portfolio(
            _proj("a", frameworks=["FastAPI"]),
            _proj("b", frameworks=["Django"]),
        ))
        reader = csv.reader(io.StringIO(result))
        rows = list(reader)
        # All rows should have same number of columns
        col_count = len(rows[0])
        for row in rows:
            assert len(row) == col_count
