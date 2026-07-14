"""Manifest discovery and validation.

Provides discover_manifests() to find domain manifests in domain directories
and validate_manifest() to validate them against the domain manifest schema.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from core._errors import ConfigurationError, SchemaError

_ID_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
_SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass
class DomainManifest:
    """A parsed domain manifest YAML file.

    Attributes:
        path: Filesystem path to the manifest file.
        id: Unique domain identifier.
        name: Human-friendly domain name.
        version: Semantic version string.
        depends_on: List of domain IDs this domain depends on.
        entrypoint: Module path to the domain entrypoint.
        exports: List of exported object types.
        validators: List of validator module paths.
        adapters: List of adapter module paths.
        capabilities: List of declared capabilities.
        schema_version: Manifest schema version.
    """

    path: Path
    id: str
    name: str
    version: str
    depends_on: list[str] = field(default_factory=list)
    entrypoint: str | None = None
    exports: list[str] = field(default_factory=list)
    validators: list[str] = field(default_factory=list)
    adapters: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    schema_version: str | None = None


def discover_manifests(domain_dirs: list[Path]) -> list[DomainManifest]:
    """Discover domain manifests from domain directories.

    Scans each directory for domain.yaml and parses it.

    Args:
        domain_dirs: List of directory paths to scan.

    Returns:
        List of DomainManifest objects. Skips directories without
        a valid domain.yaml without raising errors.
    """
    manifests: list[DomainManifest] = []
    for directory in domain_dirs:
        if not directory.is_dir():
            continue
        manifest_path = directory / "domain.yaml"
        if not manifest_path.is_file():
            continue
        try:
            raw = manifest_path.read_text(encoding="utf-8")
            data = yaml.safe_load(raw)
            if not isinstance(data, dict):
                continue
            manifest = DomainManifest(
                path=manifest_path,
                id=data.get("id", ""),
                name=data.get("name", ""),
                version=data.get("version", ""),
                depends_on=data.get("depends_on", []),
                entrypoint=data.get("entrypoint"),
                exports=data.get("exports", []),
                validators=data.get("validators", []),
                adapters=data.get("adapters", []),
                capabilities=data.get("capabilities", []),
                schema_version=data.get("schema_version"),
            )
            manifests.append(manifest)
        except (yaml.YAMLError, OSError):
            continue
    return manifests


def validate_manifest(manifest: DomainManifest) -> None:
    """Validate a domain manifest against the schema.

    Args:
        manifest: The DomainManifest to validate.

    Raises:
        SchemaError: If manifest fails validation.
        ConfigurationError: If manifest path does not exist.
    """
    if not manifest.path.exists():
        raise ConfigurationError(
            f"Manifest path does not exist: {manifest.path}"
        )

    if not manifest.id:
        raise SchemaError(
            f"Manifest at {manifest.path}: 'id' is required and must be non-empty"
        )
    if not _ID_PATTERN.match(manifest.id):
        raise SchemaError(
            f"Manifest at {manifest.path}: 'id' '{manifest.id}' must match "
            f"pattern {_ID_PATTERN.pattern}"
        )

    if not manifest.name:
        raise SchemaError(
            f"Manifest at {manifest.path}: 'name' is required and must be non-empty"
        )

    if not manifest.version:
        raise SchemaError(
            f"Manifest at {manifest.path}: 'version' is required and must be non-empty"
        )
    if not _SEMVER_PATTERN.match(manifest.version):
        raise SchemaError(
            f"Manifest at {manifest.path}: 'version' '{manifest.version}' "
            f"must match semantic versioning pattern {_SEMVER_PATTERN.pattern}"
        )

    if manifest.id in manifest.depends_on:
        raise SchemaError(
            f"Manifest at {manifest.path}: 'depends_on' contains self-reference "
            f"to domain '{manifest.id}'"
        )
