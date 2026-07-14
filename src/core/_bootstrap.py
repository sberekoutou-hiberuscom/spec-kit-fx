"""Project bootstrap — config loading and specs discovery.

Provides load_config() to load configuration from .specify/ and
locate_specs() to discover specs/ directories under a project root.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from core._errors import ConfigurationError


@dataclass
class CoreConfig:
    """Loaded project configuration from .specify/.

    Attributes:
        project_root: Absolute path to the project root.
        specs_dir: Absolute path to the specs/ directory.
        config_data: Parsed configuration values.
    """

    project_root: Path
    specs_dir: Path
    config_data: dict[str, Any] = field(default_factory=dict)


def load_config(project_root: Path) -> CoreConfig:
    """Load configuration from .specify/ directory.

    Args:
        project_root: Absolute path to the project root.

    Returns:
        CoreConfig with parsed configuration.

    Raises:
        ConfigurationError: If .specify/ is missing or config is unparseable.
    """
    specify_dir = project_root / ".specify"
    if not specify_dir.is_dir():
        raise ConfigurationError(
            f"Project root {project_root} does not contain a .specify/ directory"
        )

    config_file = specify_dir / "config.yml"
    if not config_file.is_file():
        raise ConfigurationError(
            f"Configuration file not found at {config_file}"
        )

    try:
        raw = config_file.read_text(encoding="utf-8")
        config_data = yaml.safe_load(raw) or {}
    except (yaml.YAMLError, OSError) as exc:
        raise ConfigurationError(
            f"Failed to parse configuration at {config_file}: {exc}"
        ) from exc

    return CoreConfig(
        project_root=project_root.resolve(),
        specs_dir=project_root.resolve() / "specs",
        config_data=config_data,
    )


def locate_specs(project_root: Path) -> list[Path]:
    """Locate all specs/ directories under the project root.

    Args:
        project_root: Absolute path to the project root.

    Returns:
        List of absolute paths to specs/ directories.
        Returns empty list if none found.
    """
    specs_dir = project_root / "specs"
    if not specs_dir.is_dir():
        return []

    return sorted(
        [p for p in specs_dir.iterdir() if p.is_dir()],
        key=lambda p: p.name,
    )
