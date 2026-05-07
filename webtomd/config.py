"""Config loader — reads ~/.webtomdrc and merges with CLI flags."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    raise RuntimeError("webtomd requires Python 3.11+")

CONFIG_PATH = Path.home() / ".webtomdrc"


@dataclass
class Config:
    output_dir: str | None = None
    copy: bool = False
    metadata: bool = False
    silent: bool = False
    ai_provider: str | None = None   # overrides auto-detection
    ai_model: str | None = None      # overrides provider default
    name_strategy: str = "deterministic"


def load() -> Config:
    """Load ~/.webtomdrc if it exists. Returns defaults if not found."""
    if not CONFIG_PATH.exists():
        return Config()

    with open(CONFIG_PATH, "rb") as f:
        data = tomllib.load(f)

    return Config(
        output_dir=data.get("output_dir"),
        copy=data.get("copy", False),
        metadata=data.get("metadata", False),
        silent=data.get("silent", False),
        ai_provider=data.get("ai_provider"),
        ai_model=data.get("ai_model"),
        name_strategy=data.get("name_strategy", "deterministic"),
    )


def merge(config: Config, **cli_flags) -> Config:
    """Merge CLI flags into config. CLI flags always win."""
    for key, value in cli_flags.items():
        if value is not None and hasattr(config, key):
            setattr(config, key, value)
    return config
