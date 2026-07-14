"""
Core runtime skeleton for the Spec Kit orchestrator.

Provides the orchestrator module boundaries defined in
docs/architecture/orchestrator-modules.md, including project bootstrap,
manifest discovery/validation, dependency resolution, pipeline execution,
lifecycle running, and event logging.
"""

from __future__ import annotations

# Error classes
from core._errors import (
    AdapterSyncError,
    ConfigurationError,
    CoreError,
    DependencyError,
    SchemaError,
    ValidationError,
)

# Event types
from core._events import EventStatus, LifecycleEvent, emit_event, get_events

# Bootstrap
from core._bootstrap import CoreConfig, load_config, locate_specs

# Manifest
from core._manifest import DomainManifest, discover_manifests, validate_manifest

# Resolver
from core._resolver import DependencyGraph, build_graph, resolve_order

# Pipeline
from core._pipeline import PipelineConfig, StageConfig, load_pipeline_config, execute_pipeline

# Lifecycle
from core._lifecycle import run_lifecycle, run_all_stages

__all__ = [
    "AdapterSyncError",
    "ConfigurationError",
    "CoreConfig",
    "CoreError",
    "DependencyError",
    "DependencyGraph",
    "DomainManifest",
    "EventStatus",
    "LifecycleEvent",
    "PipelineConfig",
    "SchemaError",
    "StageConfig",
    "ValidationError",
    "build_graph",
    "discover_manifests",
    "emit_event",
    "execute_pipeline",
    "get_events",
    "load_config",
    "load_pipeline_config",
    "locate_specs",
    "resolve_order",
    "run_all_stages",
    "run_lifecycle",
    "validate_manifest",
]
