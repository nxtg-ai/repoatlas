"""Tests for AI/ML tooling detection."""
from __future__ import annotations

import json

from atlas.detector import detect_ai_tools


class TestPythonAIDeps:
    def test_anthropic(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("anthropic==0.40.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "Anthropic SDK" in tools

    def test_openai(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("openai>=1.0.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "OpenAI SDK" in tools

    def test_langchain(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("langchain>=0.1.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "LangChain" in tools

    def test_llama_index(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("llama-index>=0.10.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "LlamaIndex" in tools

    def test_transformers(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("transformers>=4.30.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "Transformers" in tools

    def test_pytorch(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("torch>=2.0.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "PyTorch" in tools

    def test_tensorflow(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("tensorflow>=2.15.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "TensorFlow" in tools

    def test_scikit_learn(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("scikit-learn>=1.3.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "scikit-learn" in tools

    def test_mlflow(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("mlflow>=2.0.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "MLflow" in tools

    def test_wandb(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("wandb>=0.16.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "Weights & Biases" in tools

    def test_chromadb(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("chromadb>=0.4.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "ChromaDB" in tools

    def test_pinecone(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("pinecone-client>=3.0.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "Pinecone" in tools

    def test_sentence_transformers(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("sentence-transformers>=2.0.0\n")
        tools = detect_ai_tools(tmp_path)
        assert "Sentence Transformers" in tools

    def test_pyproject_toml(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\ndependencies = ["anthropic>=0.40", "langchain"]\n'
        )
        tools = detect_ai_tools(tmp_path)
        assert "Anthropic SDK" in tools
        assert "LangChain" in tools

    def test_no_ai_deps(self, tmp_path):
        (tmp_path / "requirements.txt").write_text("fastapi>=0.109.0\nrich>=13.0\n")
        tools = detect_ai_tools(tmp_path)
        assert tools == []


class TestJavaScriptAIDeps:
    def test_anthropic_js(self, tmp_path):
        pkg = {"dependencies": {"@anthropic-ai/sdk": "^0.30.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_ai_tools(tmp_path)
        assert "Anthropic SDK" in tools

    def test_openai_js(self, tmp_path):
        pkg = {"dependencies": {"openai": "^4.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_ai_tools(tmp_path)
        assert "OpenAI SDK" in tools

    def test_langchain_js(self, tmp_path):
        pkg = {"dependencies": {"@langchain/core": "^0.2.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_ai_tools(tmp_path)
        assert "LangChain" in tools

    def test_vercel_ai_sdk(self, tmp_path):
        pkg = {"dependencies": {"ai": "^3.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_ai_tools(tmp_path)
        assert "Vercel AI SDK" in tools

    def test_vercel_ai_anthropic(self, tmp_path):
        pkg = {"dependencies": {"@ai-sdk/anthropic": "^0.1.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_ai_tools(tmp_path)
        assert "Vercel AI SDK" in tools

    def test_huggingface_js(self, tmp_path):
        pkg = {"dependencies": {"@huggingface/inference": "^2.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_ai_tools(tmp_path)
        assert "Hugging Face" in tools

    def test_no_ai_js_deps(self, tmp_path):
        pkg = {"dependencies": {"next": "^14.0.0", "react": "^18.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_ai_tools(tmp_path)
        assert tools == []


class TestJupyterNotebooks:
    def test_notebook_detected(self, tmp_path):
        (tmp_path / "analysis.ipynb").write_text('{"cells": []}')
        tools = detect_ai_tools(tmp_path)
        assert "Jupyter" in tools

    def test_no_notebooks(self, tmp_path):
        (tmp_path / "main.py").write_text("print('hello')")
        tools = detect_ai_tools(tmp_path)
        assert "Jupyter" not in tools

    def test_notebook_in_subdir(self, tmp_path):
        nb_dir = tmp_path / "notebooks"
        nb_dir.mkdir()
        (nb_dir / "train.ipynb").write_text('{"cells": []}')
        tools = detect_ai_tools(tmp_path)
        assert "Jupyter" in tools


class TestMLInfraFiles:
    def test_mlproject(self, tmp_path):
        (tmp_path / "MLproject").write_text("name: myproject")
        tools = detect_ai_tools(tmp_path)
        assert "MLflow" in tools

    def test_wandb_dir(self, tmp_path):
        (tmp_path / "wandb").mkdir()
        tools = detect_ai_tools(tmp_path)
        assert "Weights & Biases" in tools

    def test_dvc_yaml(self, tmp_path):
        (tmp_path / "dvc.yaml").write_text("stages:\n  train:\n    cmd: python train.py")
        tools = detect_ai_tools(tmp_path)
        assert "DVC" in tools

    def test_dvc_dir(self, tmp_path):
        (tmp_path / ".dvc").mkdir()
        tools = detect_ai_tools(tmp_path)
        assert "DVC" in tools


class TestEmptyProject:
    def test_empty_dir(self, tmp_path):
        tools = detect_ai_tools(tmp_path)
        assert tools == []

    def test_combined_ai_stack(self, tmp_path):
        """A project with multiple AI tools."""
        (tmp_path / "requirements.txt").write_text(
            "anthropic>=0.40.0\nlangchain>=0.1.0\nchromadb>=0.4.0\n"
        )
        (tmp_path / "train.ipynb").write_text('{"cells": []}')
        tools = detect_ai_tools(tmp_path)
        assert "Anthropic SDK" in tools
        assert "LangChain" in tools
        assert "ChromaDB" in tools
        assert "Jupyter" in tools
        assert len(tools) == 4

    def test_no_duplicate_from_python_and_js(self, tmp_path):
        """Same tool in Python and JS deps should not duplicate."""
        (tmp_path / "requirements.txt").write_text("openai>=1.0.0\n")
        pkg = {"dependencies": {"openai": "^4.0.0"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        tools = detect_ai_tools(tmp_path)
        assert tools.count("OpenAI SDK") == 1
