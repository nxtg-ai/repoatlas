"""Tests for user configuration module."""
from __future__ import annotations

from unittest.mock import patch

from atlas.config import (
    DEFAULTS,
    get_value,
    load_config,
    set_value,
    valid_keys,
)


class TestLoadConfig:
    def test_defaults_when_no_file(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            cfg = load_config()
        assert cfg["ci"]["min_health"] == 0
        assert cfg["ci"]["min_project_health"] == 0
        assert cfg["export"]["format"] == "markdown"

    def test_load_user_overrides(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        cfg_file.write_text('[ci]\nmin_health = 70\n')
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            cfg = load_config()
        assert cfg["ci"]["min_health"] == 70
        # Other defaults preserved
        assert cfg["ci"]["min_project_health"] == 0
        assert cfg["export"]["format"] == "markdown"

    def test_load_corrupt_toml(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        cfg_file.write_text("not valid {{{{ toml")
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            cfg = load_config()
        # Falls back to defaults
        assert cfg == {k: dict(v) for k, v in DEFAULTS.items()}

    def test_partial_override(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        cfg_file.write_text('[export]\nformat = "json"\n')
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            cfg = load_config()
        assert cfg["export"]["format"] == "json"
        assert cfg["ci"]["min_health"] == 0


class TestGetValue:
    def test_get_existing(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            val = get_value("ci.min_health")
        assert val == 0

    def test_get_unknown_key(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            val = get_value("nonexistent.key")
        assert val is None

    def test_get_bad_format(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            val = get_value("nodot")
        assert val is None


class TestSetValue:
    def test_set_int_value(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            result = set_value("ci.min_health", "70")
            assert result is True
            assert get_value("ci.min_health") == 70

    def test_set_string_value(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            result = set_value("export.format", "json")
            assert result is True
            assert get_value("export.format") == "json"

    def test_set_invalid_key(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            result = set_value("bogus.key", "val")
        assert result is False

    def test_set_invalid_int(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            result = set_value("ci.min_health", "notanumber")
        assert result is False

    def test_set_creates_parent_dirs(self, tmp_path):
        cfg_file = tmp_path / "deep" / "nested" / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            set_value("ci.min_health", "50")
        assert cfg_file.exists()

    def test_set_preserves_other_values(self, tmp_path):
        cfg_file = tmp_path / "config.toml"
        with patch("atlas.config.CONFIG_FILE", cfg_file):
            set_value("ci.min_health", "70")
            set_value("ci.min_project_health", "50")
            assert get_value("ci.min_health") == 70
            assert get_value("ci.min_project_health") == 50


class TestValidKeys:
    def test_returns_list(self):
        keys = valid_keys()
        assert isinstance(keys, list)
        assert "ci.min_health" in keys
        assert "ci.min_project_health" in keys
        assert "export.format" in keys

    def test_sorted(self):
        keys = valid_keys()
        assert keys == sorted(keys)
