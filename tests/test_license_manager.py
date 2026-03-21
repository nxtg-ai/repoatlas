"""Tests for license_manager — key validation, activation, status."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from atlas.license_manager import (
    FREE_PROJECT_LIMIT,
    PRO_FEATURES,
    _validate_key,
    activate,
    deactivate,
    generate_key,
    get_status,
    is_pro,
)


# ---------------------------------------------------------------------------
# Key generation helper — used across tests
# ---------------------------------------------------------------------------

def _make_valid_key() -> str:
    """Generate a valid license key for testing."""
    return generate_key("test-seed")


def _make_key_from_prefix(prefix: str) -> str:
    """Build a valid key from a known prefix (ATLAS-XXXX-XXXX-XXXX)."""
    checksum = hashlib.sha256(prefix.encode()).hexdigest()[:4].upper()
    return f"{prefix}-{checksum}"


# ===========================================================================
# _validate_key
# ===========================================================================


class TestValidateKey:
    """Key format: ATLAS-XXXX-XXXX-XXXX-XXXX where last 4 = sha256[:4] of rest."""

    def test_valid_generated_key(self):
        key = _make_valid_key()
        assert _validate_key(key)

    def test_valid_deterministic_key(self):
        prefix = "ATLAS-AAAA-BBBB-CCCC"
        key = _make_key_from_prefix(prefix)
        assert _validate_key(key)

    def test_wrong_prefix(self):
        assert not _validate_key("WRONG-AAAA-BBBB-CCCC-DDDD")

    def test_empty_string(self):
        assert not _validate_key("")

    def test_too_few_parts(self):
        assert not _validate_key("ATLAS-AAAA-BBBB")

    def test_too_many_parts(self):
        assert not _validate_key("ATLAS-AAAA-BBBB-CCCC-DDDD-EEEE")

    def test_bad_checksum(self):
        prefix = "ATLAS-AAAA-BBBB-CCCC"
        assert not _validate_key(f"{prefix}-0000")

    def test_checksum_is_case_sensitive(self):
        prefix = "ATLAS-AAAA-BBBB-CCCC"
        expected = hashlib.sha256(prefix.encode()).hexdigest()[:4].upper()
        lower_key = f"{prefix}-{expected.lower()}"
        # Keys should use uppercase checksum
        if expected != expected.lower():
            assert not _validate_key(lower_key)

    def test_multiple_generated_keys_are_unique(self):
        keys = {generate_key(f"seed-{i}") for i in range(20)}
        assert len(keys) == 20

    def test_all_generated_keys_validate(self):
        for i in range(20):
            key = generate_key(f"seed-{i}")
            assert _validate_key(key), f"Key {key} failed validation"


# ===========================================================================
# generate_key
# ===========================================================================


class TestGenerateKey:
    def test_format(self):
        key = generate_key("test")
        parts = key.split("-")
        assert len(parts) == 5
        assert parts[0] == "ATLAS"

    def test_validates(self):
        assert _validate_key(generate_key("anything"))

    def test_randomness(self):
        # Two calls with same seed should still produce different keys (uses secrets)
        k1 = generate_key("same")
        k2 = generate_key("same")
        assert k1 != k2


# ===========================================================================
# activate / deactivate / is_pro
# ===========================================================================


class TestActivation:
    def test_activate_valid_key(self, tmp_path):
        license_file = tmp_path / "license.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            key = _make_valid_key()
            assert activate(key)
            assert license_file.exists()
            data = json.loads(license_file.read_text())
            assert data["key"] == key
            assert data["activated"] is True

    def test_activate_invalid_key(self, tmp_path):
        license_file = tmp_path / "license.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            assert not activate("INVALID-KEY")
            assert not license_file.exists()

    def test_is_pro_after_activation(self, tmp_path):
        license_file = tmp_path / "license.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            assert not is_pro()
            activate(_make_valid_key())
            assert is_pro()

    def test_deactivate(self, tmp_path):
        license_file = tmp_path / "license.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            activate(_make_valid_key())
            assert is_pro()
            deactivate()
            assert not is_pro()
            assert not license_file.exists()

    def test_deactivate_no_file(self, tmp_path):
        license_file = tmp_path / "license.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            deactivate()  # should not raise

    def test_is_pro_no_file(self, tmp_path):
        license_file = tmp_path / "nonexistent.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            assert not is_pro()

    def test_is_pro_corrupt_json(self, tmp_path):
        license_file = tmp_path / "license.json"
        license_file.write_text("not json")
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            assert not is_pro()

    def test_is_pro_empty_json(self, tmp_path):
        license_file = tmp_path / "license.json"
        license_file.write_text("{}")
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            assert not is_pro()

    def test_is_pro_invalid_key_in_file(self, tmp_path):
        license_file = tmp_path / "license.json"
        license_file.write_text(json.dumps({"key": "ATLAS-BAD-KEY", "activated": True}))
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            assert not is_pro()

    def test_activate_creates_parent_dirs(self, tmp_path):
        license_file = tmp_path / "deep" / "nested" / "license.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            key = _make_valid_key()
            assert activate(key)
            assert license_file.exists()


# ===========================================================================
# get_status
# ===========================================================================


class TestGetStatus:
    def test_free_tier(self, tmp_path):
        license_file = tmp_path / "license.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            status = get_status()
            assert status["tier"] == "Free"
            assert status["project_limit"] == str(FREE_PROJECT_LIMIT)
            assert status["cross_project"] is False
            assert status["export"] is False
            assert status["batch_add"] is False

    def test_pro_tier(self, tmp_path):
        license_file = tmp_path / "license.json"
        with patch("atlas.license_manager.LICENSE_FILE", license_file):
            activate(_make_valid_key())
            status = get_status()
            assert status["tier"] == "Pro"
            assert status["project_limit"] == "Unlimited"
            assert status["cross_project"] is True
            assert status["export"] is True
            assert status["batch_add"] is True


# ===========================================================================
# Constants
# ===========================================================================


class TestConstants:
    def test_free_project_limit(self):
        assert FREE_PROJECT_LIMIT == 3

    def test_pro_features_contains_expected(self):
        expected = {"cross_project", "batch_add", "export", "health_breakdown", "unlimited_projects"}
        assert PRO_FEATURES == expected
