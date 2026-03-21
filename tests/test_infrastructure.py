"""Tests for infrastructure and deployment detection."""
from __future__ import annotations

import json

from atlas.detector import detect_infrastructure


class TestDockerDetection:
    def test_dockerfile(self, tmp_path):
        (tmp_path / "Dockerfile").write_text("FROM python:3.12")
        infra = detect_infrastructure(tmp_path)
        assert "Docker" in infra

    def test_docker_compose_yml(self, tmp_path):
        (tmp_path / "docker-compose.yml").write_text("version: '3'")
        infra = detect_infrastructure(tmp_path)
        assert "Docker Compose" in infra
        assert "Docker" in infra

    def test_docker_compose_yaml(self, tmp_path):
        (tmp_path / "docker-compose.yaml").write_text("version: '3'")
        infra = detect_infrastructure(tmp_path)
        assert "Docker Compose" in infra

    def test_no_docker(self, tmp_path):
        (tmp_path / "main.py").write_text("print('hello')")
        infra = detect_infrastructure(tmp_path)
        assert "Docker" not in infra


class TestKubernetesDetection:
    def test_k8s_dir(self, tmp_path):
        (tmp_path / "k8s").mkdir()
        infra = detect_infrastructure(tmp_path)
        assert "Kubernetes" in infra

    def test_kubernetes_dir(self, tmp_path):
        (tmp_path / "kubernetes").mkdir()
        infra = detect_infrastructure(tmp_path)
        assert "Kubernetes" in infra

    def test_helm_chart(self, tmp_path):
        (tmp_path / "Chart.yaml").write_text("apiVersion: v2\nname: myapp")
        infra = detect_infrastructure(tmp_path)
        assert "Helm" in infra
        assert "Kubernetes" in infra

    def test_helmfile(self, tmp_path):
        (tmp_path / "helmfile.yaml").write_text("releases: []")
        infra = detect_infrastructure(tmp_path)
        assert "Helm" in infra


class TestIaCDetection:
    def test_terraform(self, tmp_path):
        (tmp_path / "main.tf").write_text('provider "aws" {}')
        infra = detect_infrastructure(tmp_path)
        assert "Terraform" in infra

    def test_terraform_dir(self, tmp_path):
        (tmp_path / "terraform").mkdir()
        infra = detect_infrastructure(tmp_path)
        assert "Terraform" in infra

    def test_pulumi(self, tmp_path):
        (tmp_path / "Pulumi.yaml").write_text("name: mystack")
        infra = detect_infrastructure(tmp_path)
        assert "Pulumi" in infra

    def test_aws_cdk(self, tmp_path):
        (tmp_path / "cdk.json").write_text('{"app": "npx ts-node"}')
        infra = detect_infrastructure(tmp_path)
        assert "AWS CDK" in infra


class TestCICDDetection:
    def test_github_actions(self, tmp_path):
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "ci.yml").write_text("name: CI")
        infra = detect_infrastructure(tmp_path)
        assert "GitHub Actions" in infra

    def test_gitlab_ci(self, tmp_path):
        (tmp_path / ".gitlab-ci.yml").write_text("stages: [build]")
        infra = detect_infrastructure(tmp_path)
        assert "GitLab CI" in infra

    def test_jenkinsfile(self, tmp_path):
        (tmp_path / "Jenkinsfile").write_text("pipeline { agent any }")
        infra = detect_infrastructure(tmp_path)
        assert "Jenkins" in infra

    def test_circleci(self, tmp_path):
        (tmp_path / ".circleci").mkdir()
        infra = detect_infrastructure(tmp_path)
        assert "CircleCI" in infra


class TestServerlessDetection:
    def test_vercel(self, tmp_path):
        (tmp_path / "vercel.json").write_text("{}")
        infra = detect_infrastructure(tmp_path)
        assert "Vercel" in infra

    def test_netlify(self, tmp_path):
        (tmp_path / "netlify.toml").write_text("[build]")
        infra = detect_infrastructure(tmp_path)
        assert "Netlify" in infra

    def test_cloudflare_workers(self, tmp_path):
        (tmp_path / "wrangler.toml").write_text('name = "worker"')
        infra = detect_infrastructure(tmp_path)
        assert "Cloudflare Workers" in infra

    def test_fly_io(self, tmp_path):
        (tmp_path / "fly.toml").write_text('app = "myapp"')
        infra = detect_infrastructure(tmp_path)
        assert "Fly.io" in infra

    def test_render(self, tmp_path):
        (tmp_path / "render.yaml").write_text("services: []")
        infra = detect_infrastructure(tmp_path)
        assert "Render" in infra

    def test_serverless_framework(self, tmp_path):
        (tmp_path / "serverless.yml").write_text("service: myservice")
        infra = detect_infrastructure(tmp_path)
        assert "Serverless Framework" in infra


class TestCloudProviderDetection:
    def test_aws_from_python_deps(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("boto3==1.34.0\n")
        infra = detect_infrastructure(tmp_path)
        assert "AWS" in infra

    def test_aws_from_js_deps(self, tmp_path):
        pkg = {"dependencies": {"@aws-sdk/client-s3": "^3.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        infra = detect_infrastructure(tmp_path)
        assert "AWS" in infra

    def test_gcp_from_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("google-cloud-storage==2.0.0\n")
        infra = detect_infrastructure(tmp_path)
        assert "GCP" in infra

    def test_azure_from_python(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("azure-storage-blob==12.0.0\n")
        infra = detect_infrastructure(tmp_path)
        assert "Azure" in infra


class TestEmptyProject:
    def test_empty_dir(self, tmp_path):
        infra = detect_infrastructure(tmp_path)
        assert infra == []

    def test_combined_stack(self, tmp_path):
        """A project with multiple infra tools."""
        (tmp_path / "Dockerfile").write_text("FROM node:20")
        (tmp_path / "docker-compose.yml").write_text("version: '3'")
        (tmp_path / "k8s").mkdir()
        wf = tmp_path / ".github" / "workflows"
        wf.mkdir(parents=True)
        (wf / "ci.yml").write_text("name: CI")
        (tmp_path / "vercel.json").write_text("{}")
        infra = detect_infrastructure(tmp_path)
        assert "Docker" in infra
        assert "Docker Compose" in infra
        assert "Kubernetes" in infra
        assert "GitHub Actions" in infra
        assert "Vercel" in infra
