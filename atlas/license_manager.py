"""License management for Pro features."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

LICENSE_FILE = Path.home() / ".atlas" / "license.json"

# Pro-gated features
PRO_FEATURES = {
    "cross_project",     # connections, shared deps, version mismatches
    "batch_add",         # batch-add command
    "export",            # export command
    "health_breakdown",  # detailed 4-dimension health in inspect
    "unlimited_projects", # free tier limited to 3 projects
}

FREE_PROJECT_LIMIT = 3


def is_pro() -> bool:
    """Check if a valid Pro license is active."""
    if not LICENSE_FILE.exists():
        return False
    try:
        data = json.loads(LICENSE_FILE.read_text())
        key = data.get("key", "")
        return _validate_key(key)
    except (json.JSONDecodeError, KeyError):
        return False


def activate(key: str) -> bool:
    """Activate a Pro license key."""
    if not _validate_key(key):
        return False
    LICENSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    LICENSE_FILE.write_text(json.dumps({"key": key, "activated": True}))
    return True


def deactivate():
    """Remove the active license."""
    if LICENSE_FILE.exists():
        LICENSE_FILE.unlink()


def get_status() -> dict:
    """Get current license status."""
    pro = is_pro()
    return {
        "tier": "Pro" if pro else "Free",
        "project_limit": "Unlimited" if pro else str(FREE_PROJECT_LIMIT),
        "cross_project": pro,
        "export": pro,
        "batch_add": pro,
    }


def _validate_key(key: str) -> bool:
    """Validate a license key format.

    Key format: ATLAS-XXXX-XXXX-XXXX-XXXX
    Validation: last 4 chars = first 4 of SHA-256 of the rest.
    """
    if not key.startswith("ATLAS-"):
        return False
    parts = key.split("-")
    if len(parts) != 5:
        return False
    # Checksum: hash of first 4 parts, compare to 5th
    payload = "-".join(parts[:4])
    expected = hashlib.sha256(payload.encode()).hexdigest()[:4].upper()
    return parts[4] == expected


def generate_key(seed: str) -> str:
    """Generate a valid license key from a seed string."""
    import secrets
    mid = secrets.token_hex(6).upper()
    prefix = f"ATLAS-{mid[:4]}-{mid[4:8]}-{mid[8:12]}"
    checksum = hashlib.sha256(prefix.encode()).hexdigest()[:4].upper()
    return f"{prefix}-{checksum}"
