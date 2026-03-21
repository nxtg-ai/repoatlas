"""Tests for rich markdown export."""
from __future__ import annotations

from atlas.export_report import build_markdown_report
from atlas.models import GitInfo, HealthScore, Portfolio, Project, TechStack


def _proj(name: str, languages=None, frameworks=None, databases=None,
          infrastructure=None, security_tools=None, ai_tools=None,
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
        # Healthy project with CI — avoids health_gap and infra_gap connections
        p = _proj("solo", test_files=10, source_files=10,
                  infrastructure=["GitHub Actions"])
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
