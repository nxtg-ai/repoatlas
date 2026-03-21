from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TechStack:
    languages: dict[str, int] = field(default_factory=dict)
    frameworks: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    key_deps: dict[str, str] = field(default_factory=dict)
    infrastructure: list[str] = field(default_factory=list)
    security_tools: list[str] = field(default_factory=list)
    ai_tools: list[str] = field(default_factory=list)
    quality_tools: list[str] = field(default_factory=list)
    testing_frameworks: list[str] = field(default_factory=list)
    package_managers: list[str] = field(default_factory=list)
    docs_artifacts: list[str] = field(default_factory=list)
    ci_config: list[str] = field(default_factory=list)
    runtime_versions: dict[str, str] = field(default_factory=dict)
    build_tools: list[str] = field(default_factory=list)
    api_specs: list[str] = field(default_factory=list)
    monitoring_tools: list[str] = field(default_factory=list)
    auth_tools: list[str] = field(default_factory=list)
    messaging_tools: list[str] = field(default_factory=list)
    deploy_targets: list[str] = field(default_factory=list)
    state_management: list[str] = field(default_factory=list)
    css_frameworks: list[str] = field(default_factory=list)
    bundlers: list[str] = field(default_factory=list)
    orm_tools: list[str] = field(default_factory=list)

    @property
    def primary_languages(self) -> list[str]:
        sorted_langs = sorted(self.languages.items(), key=lambda x: x[1], reverse=True)
        return [lang for lang, _ in sorted_langs[:3] if lang not in ("Markdown", "MDX", "Shell")]

    @property
    def summary(self) -> str:
        parts = self.primary_languages[:2]
        if self.frameworks:
            top_fw = [f for f in self.frameworks if f not in ("Docker",)][:2]
            parts.extend(top_fw)
        return " · ".join(parts[:3]) if parts else "Unknown"


@dataclass
class GitInfo:
    branch: str = ""
    last_commit_date: str = ""
    last_commit_msg: str = ""
    uncommitted_changes: int = 0
    total_commits: int = 0
    has_remote: bool = False


@dataclass
class HealthScore:
    tests: float = 0.0
    git_hygiene: float = 0.0
    documentation: float = 0.0
    structure: float = 0.0
    overall: float = 0.0
    grade: str = "F"

    def compute(self):
        self.overall = (
            self.tests * 0.35
            + self.git_hygiene * 0.20
            + self.documentation * 0.20
            + self.structure * 0.25
        )
        if self.overall >= 0.90:
            self.grade = "A"
        elif self.overall >= 0.83:
            self.grade = "B+"
        elif self.overall >= 0.76:
            self.grade = "B"
        elif self.overall >= 0.60:
            self.grade = "C"
        elif self.overall >= 0.40:
            self.grade = "D"
        else:
            self.grade = "F"

    @property
    def percent(self) -> int:
        return int(self.overall * 100)

    @property
    def icon(self) -> str:
        if self.overall >= 0.76:
            return "[green]●[/green]"
        elif self.overall >= 0.60:
            return "[yellow]●[/yellow]"
        elif self.overall >= 0.40:
            return "[red]●[/red]"
        else:
            return "[dim red]●[/dim red]"


@dataclass
class Project:
    name: str
    path: str
    tech_stack: TechStack = field(default_factory=TechStack)
    git_info: GitInfo = field(default_factory=GitInfo)
    health: HealthScore = field(default_factory=HealthScore)
    test_file_count: int = 0
    source_file_count: int = 0
    total_file_count: int = 0
    loc: int = 0
    license: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "tech_stack": {
                "languages": self.tech_stack.languages,
                "frameworks": self.tech_stack.frameworks,
                "databases": self.tech_stack.databases,
                "key_deps": self.tech_stack.key_deps,
                "infrastructure": self.tech_stack.infrastructure,
                "security_tools": self.tech_stack.security_tools,
                "ai_tools": self.tech_stack.ai_tools,
                "quality_tools": self.tech_stack.quality_tools,
                "testing_frameworks": self.tech_stack.testing_frameworks,
                "package_managers": self.tech_stack.package_managers,
                "docs_artifacts": self.tech_stack.docs_artifacts,
                "ci_config": self.tech_stack.ci_config,
                "runtime_versions": self.tech_stack.runtime_versions,
                "build_tools": self.tech_stack.build_tools,
                "api_specs": self.tech_stack.api_specs,
                "monitoring_tools": self.tech_stack.monitoring_tools,
                "auth_tools": self.tech_stack.auth_tools,
                "messaging_tools": self.tech_stack.messaging_tools,
                "deploy_targets": self.tech_stack.deploy_targets,
                "state_management": self.tech_stack.state_management,
                "css_frameworks": self.tech_stack.css_frameworks,
                "bundlers": self.tech_stack.bundlers,
                "orm_tools": self.tech_stack.orm_tools,
            },
            "git_info": {
                "branch": self.git_info.branch,
                "last_commit_date": self.git_info.last_commit_date,
                "last_commit_msg": self.git_info.last_commit_msg,
                "uncommitted_changes": self.git_info.uncommitted_changes,
                "total_commits": self.git_info.total_commits,
                "has_remote": self.git_info.has_remote,
            },
            "health": {
                "tests": self.health.tests,
                "git_hygiene": self.health.git_hygiene,
                "documentation": self.health.documentation,
                "structure": self.health.structure,
                "overall": self.health.overall,
                "grade": self.health.grade,
            },
            "test_file_count": self.test_file_count,
            "source_file_count": self.source_file_count,
            "total_file_count": self.total_file_count,
            "loc": self.loc,
            "license": self.license,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Project:
        ts = data.get("tech_stack", {})
        gi = data.get("git_info", {})
        hs = data.get("health", {})
        p = cls(
            name=data["name"],
            path=data["path"],
            tech_stack=TechStack(
                languages=ts.get("languages", {}),
                frameworks=ts.get("frameworks", []),
                databases=ts.get("databases", []),
                key_deps=ts.get("key_deps", {}),
                infrastructure=ts.get("infrastructure", []),
                security_tools=ts.get("security_tools", []),
                ai_tools=ts.get("ai_tools", []),
                quality_tools=ts.get("quality_tools", []),
                testing_frameworks=ts.get("testing_frameworks", []),
                package_managers=ts.get("package_managers", []),
                docs_artifacts=ts.get("docs_artifacts", []),
                ci_config=ts.get("ci_config", []),
                runtime_versions=ts.get("runtime_versions", {}),
                build_tools=ts.get("build_tools", []),
                api_specs=ts.get("api_specs", []),
                monitoring_tools=ts.get("monitoring_tools", []),
                auth_tools=ts.get("auth_tools", []),
                messaging_tools=ts.get("messaging_tools", []),
                deploy_targets=ts.get("deploy_targets", []),
                state_management=ts.get("state_management", []),
                css_frameworks=ts.get("css_frameworks", []),
                bundlers=ts.get("bundlers", []),
                orm_tools=ts.get("orm_tools", []),
            ),
            git_info=GitInfo(
                branch=gi.get("branch", ""),
                last_commit_date=gi.get("last_commit_date", ""),
                last_commit_msg=gi.get("last_commit_msg", ""),
                uncommitted_changes=gi.get("uncommitted_changes", 0),
                total_commits=gi.get("total_commits", 0),
                has_remote=gi.get("has_remote", False),
            ),
            health=HealthScore(
                tests=hs.get("tests", 0),
                git_hygiene=hs.get("git_hygiene", 0),
                documentation=hs.get("documentation", 0),
                structure=hs.get("structure", 0),
                overall=hs.get("overall", 0),
                grade=hs.get("grade", "F"),
            ),
            test_file_count=data.get("test_file_count", 0),
            source_file_count=data.get("source_file_count", 0),
            total_file_count=data.get("total_file_count", 0),
            loc=data.get("loc", 0),
            license=data.get("license", ""),
        )
        return p


@dataclass
class Connection:
    type: str  # shared_dep, version_mismatch, reuse_candidate, health_gap
    detail: str
    projects: list[str] = field(default_factory=list)
    severity: str = "info"  # info, warning, critical


@dataclass
class Portfolio:
    name: str
    projects: list[Project] = field(default_factory=list)
    created: str = ""
    last_scan: str = ""

    @property
    def total_tests(self) -> int:
        return sum(p.test_file_count for p in self.projects)

    @property
    def total_loc(self) -> int:
        return sum(p.loc for p in self.projects)

    @property
    def avg_health(self) -> float:
        if not self.projects:
            return 0.0
        return sum(p.health.overall for p in self.projects) / len(self.projects)

    @property
    def avg_grade(self) -> str:
        avg = self.avg_health
        if avg >= 0.90:
            return "A"
        elif avg >= 0.83:
            return "B+"
        elif avg >= 0.76:
            return "B"
        elif avg >= 0.60:
            return "C"
        elif avg >= 0.40:
            return "D"
        return "F"

    def save(self, path: Path):
        data = {
            "name": self.name,
            "created": self.created,
            "last_scan": self.last_scan,
            "projects": [p.to_dict() for p in self.projects],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2))

    @classmethod
    def load(cls, path: Path) -> Portfolio:
        data = json.loads(path.read_text())
        portfolio = cls(
            name=data["name"],
            created=data.get("created", ""),
            last_scan=data.get("last_scan", ""),
        )
        portfolio.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return portfolio

    def find_project(self, name: str) -> Project | None:
        for p in self.projects:
            if p.name.lower() == name.lower():
                return p
        return None
