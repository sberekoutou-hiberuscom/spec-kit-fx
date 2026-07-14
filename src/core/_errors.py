"""Error classes for the core runtime skeleton.

All error classes inherit from CoreError(Exception), providing a common
base for callers to catch all core errors with a single ``except CoreError``.
"""

from __future__ import annotations


class CoreError(Exception):
    """Base for all core runtime errors."""


class ConfigurationError(CoreError):
    """Invalid or missing configuration."""


class SchemaError(CoreError):
    """Manifest or config fails schema validation."""


class DependencyError(CoreError):
    """Missing, circular, or self-referencing dependencies."""


class ValidationError(CoreError):
    """Domain validation failure."""


class AdapterSyncError(CoreError):
    """Adapter synchronization failure."""
