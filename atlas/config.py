"""User configuration — persistent settings for Atlas CLI."""
from __future__ import annotations

import tomllib
from pathlib import Path

CONFIG_FILE = Path.home() / ".atlas" / "config.toml"

DEFAULTS: dict[str, dict[str, int | str]] = {
    "ci": {
        "min_health": 0,
        "min_project_health": 0,
    },
    "export": {
        "format": "markdown",
    },
}

# Valid keys and their types for validation
_KEY_TYPES: dict[str, type] = {
    "ci.min_health": int,
    "ci.min_project_health": int,
    "export.format": str,
}


def load_config() -> dict:
    """Load config from disk, merged with defaults."""
    config = _deep_copy_defaults()
    if not CONFIG_FILE.exists():
        return config
    try:
        with open(CONFIG_FILE, "rb") as f:
            user = tomllib.load(f)
        _merge(config, user)
    except (tomllib.TOMLDecodeError, OSError):
        pass
    return config


def get_value(key: str) -> int | str | None:
    """Get a config value by dotted key (e.g. 'ci.min_health')."""
    config = load_config()
    parts = key.split(".", 1)
    if len(parts) != 2:
        return None
    section, field = parts
    return config.get(section, {}).get(field)


def set_value(key: str, value: str) -> bool:
    """Set a config value by dotted key. Returns True on success."""
    if key not in _KEY_TYPES:
        return False

    expected_type = _KEY_TYPES[key]
    if expected_type is int:
        try:
            typed_value: int | str = int(value)
        except ValueError:
            return False
    else:
        typed_value = value

    config = load_config()
    section, field = key.split(".", 1)
    if section not in config:
        config[section] = {}
    config[section][field] = typed_value

    _write_config(config)
    return True


def valid_keys() -> list[str]:
    """Return list of valid config keys."""
    return sorted(_KEY_TYPES.keys())


def _write_config(config: dict) -> None:
    """Write config to TOML file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for section, values in sorted(config.items()):
        lines.append(f"[{section}]")
        for k, v in sorted(values.items()):
            if isinstance(v, str):
                lines.append(f'{k} = "{v}"')
            else:
                lines.append(f"{k} = {v}")
        lines.append("")
    CONFIG_FILE.write_text("\n".join(lines))


def _deep_copy_defaults() -> dict:
    return {k: dict(v) for k, v in DEFAULTS.items()}


def _merge(base: dict, override: dict) -> None:
    """Merge override into base (one level deep)."""
    for section, values in override.items():
        if isinstance(values, dict) and section in base:
            base[section].update(values)
