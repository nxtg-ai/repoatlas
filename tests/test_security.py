"""Tests for security posture detection."""
from __future__ import annotations

from atlas.detector import detect_security_tools


class TestSecurityPolicy:
    def test_security_md(self, tmp_path):
        (tmp_path / "SECURITY.md").write_text("# Security Policy")
        tools = detect_security_tools(tmp_path)
        assert "SECURITY.md" in tools

    def test_no_security_md(self, tmp_path):
        (tmp_path / "README.md").write_text("# Hello")
        tools = detect_security_tools(tmp_path)
        assert "SECURITY.md" not in tools


class TestDependencyScanning:
    def test_dependabot(self, tmp_path):
        gh = tmp_path / ".github"
        gh.mkdir()
        (gh / "dependabot.yml").write_text("version: 2")
        tools = detect_security_tools(tmp_path)
        assert "Dependabot" in tools

    def test_renovate_json(self, tmp_path):
        (tmp_path / "renovate.json").write_text("{}")
        tools = detect_security_tools(tmp_path)
        assert "Renovate" in tools

    def test_renovaterc(self, tmp_path):
        (tmp_path / ".renovaterc").write_text("{}")
        tools = detect_security_tools(tmp_path)
        assert "Renovate" in tools

    def test_snyk(self, tmp_path):
        (tmp_path / ".snyk").write_text("version: v1.25.0")
        tools = detect_security_tools(tmp_path)
        assert "Snyk" in tools


class TestSecretScanning:
    def test_gitleaks(self, tmp_path):
        (tmp_path / ".gitleaks.toml").write_text("[allowlist]")
        tools = detect_security_tools(tmp_path)
        assert "Gitleaks" in tools

    def test_sops(self, tmp_path):
        (tmp_path / ".sops.yaml").write_text("creation_rules: []")
        tools = detect_security_tools(tmp_path)
        assert "SOPS" in tools


class TestPreCommitSecurity:
    def test_detect_secrets_in_pre_commit(self, tmp_path):
        (tmp_path / ".pre-commit-config.yaml").write_text(
            "repos:\n  - repo: detect-secrets\n    hooks:\n      - id: detect-secrets"
        )
        tools = detect_security_tools(tmp_path)
        assert "detect-secrets" in tools

    def test_gitleaks_in_pre_commit(self, tmp_path):
        (tmp_path / ".pre-commit-config.yaml").write_text(
            "repos:\n  - repo: gitleaks\n    hooks:\n      - id: gitleaks"
        )
        tools = detect_security_tools(tmp_path)
        assert "Gitleaks" in tools

    def test_bandit_in_pre_commit(self, tmp_path):
        (tmp_path / ".pre-commit-config.yaml").write_text(
            "repos:\n  - repo: bandit\n    hooks:\n      - id: bandit"
        )
        tools = detect_security_tools(tmp_path)
        assert "Bandit" in tools

    def test_no_security_hooks(self, tmp_path):
        (tmp_path / ".pre-commit-config.yaml").write_text(
            "repos:\n  - repo: black\n    hooks:\n      - id: black"
        )
        tools = detect_security_tools(tmp_path)
        assert "detect-secrets" not in tools
        assert "Gitleaks" not in tools
        assert "Bandit" not in tools


class TestPythonSecurityDeps:
    def test_bandit_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("bandit==1.7.0\n")
        tools = detect_security_tools(tmp_path)
        assert "Bandit" in tools

    def test_safety_in_requirements(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("safety==3.0.0\n")
        tools = detect_security_tools(tmp_path)
        assert "Safety" in tools

    def test_pip_audit_in_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project.optional-dependencies]\ndev = ["pip-audit"]\n'
        )
        tools = detect_security_tools(tmp_path)
        assert "pip-audit" in tools

    def test_bandit_in_dev_requirements(self, tmp_path):
        (tmp_path / "requirements-dev.txt").write_text("bandit>=1.7\n")
        tools = detect_security_tools(tmp_path)
        assert "Bandit" in tools

    def test_no_security_deps(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastapi==0.109.0\n")
        tools = detect_security_tools(tmp_path)
        assert "Bandit" not in tools
        assert "Safety" not in tools
        assert "pip-audit" not in tools


class TestCodeQL:
    def test_codeql_dir(self, tmp_path):
        (tmp_path / ".github" / "codeql").mkdir(parents=True)
        tools = detect_security_tools(tmp_path)
        assert "CodeQL" in tools

    def test_codeql_in_workflow(self, tmp_path):
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "codeql.yml").write_text(
            "name: CodeQL\njobs:\n  analyze:\n    uses: github/codeql-action/analyze@v3"
        )
        tools = detect_security_tools(tmp_path)
        assert "CodeQL" in tools

    def test_no_codeql(self, tmp_path):
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "ci.yml").write_text("name: CI\njobs:\n  test:\n    run: pytest")
        tools = detect_security_tools(tmp_path)
        assert "CodeQL" not in tools

    def test_codeql_not_duplicated(self, tmp_path):
        """CodeQL dir + workflow reference should not duplicate."""
        (tmp_path / ".github" / "codeql").mkdir(parents=True)
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True, exist_ok=True)
        (wf / "codeql.yml").write_text("uses: github/codeql-action")
        tools = detect_security_tools(tmp_path)
        assert tools.count("CodeQL") == 1


class TestTrivy:
    def test_trivy_yaml(self, tmp_path):
        (tmp_path / "trivy.yaml").write_text("severity: HIGH")
        tools = detect_security_tools(tmp_path)
        assert "Trivy" in tools

    def test_trivy_dot_yaml(self, tmp_path):
        (tmp_path / ".trivy.yaml").write_text("severity: HIGH")
        tools = detect_security_tools(tmp_path)
        assert "Trivy" in tools


class TestEmptyProject:
    def test_empty_dir(self, tmp_path):
        tools = detect_security_tools(tmp_path)
        assert tools == []

    def test_combined_security_stack(self, tmp_path):
        """A project with multiple security tools."""
        (tmp_path / "SECURITY.md").write_text("# Security Policy")
        gh = tmp_path / ".github"
        gh.mkdir()
        (gh / "dependabot.yml").write_text("version: 2")
        (tmp_path / ".gitleaks.toml").write_text("[allowlist]")
        (tmp_path / "requirements.txt").write_text("bandit==1.7.0\nsafety==3.0\n")
        tools = detect_security_tools(tmp_path)
        assert "SECURITY.md" in tools
        assert "Dependabot" in tools
        assert "Gitleaks" in tools
        assert "Bandit" in tools
        assert "Safety" in tools
        assert len(tools) == 5

    def test_no_duplicate_bandit(self, tmp_path):
        """Bandit in both requirements and pre-commit should not duplicate."""
        (tmp_path / "requirements.txt").write_text("bandit==1.7.0\n")
        (tmp_path / ".pre-commit-config.yaml").write_text(
            "repos:\n  - repo: bandit\n    hooks:\n      - id: bandit"
        )
        tools = detect_security_tools(tmp_path)
        assert tools.count("Bandit") == 1
