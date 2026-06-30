# Orchestrator Modules

This document defines the phase 4 runtime skeleton boundaries.

## Module Boundaries

- `project_bootstrap`: load configuration and locate feature specs
- `manifest_discovery`: discover domain manifests
- `manifest_validation`: schema and semantic validation
- `dependency_resolver`: build graph and determine deterministic order
- `pipeline_executor`: execute configured stages
- `lifecycle_runner`: run domain lifecycle transitions
- `event_logger`: structured runtime events and diagnostics

## Design Constraints

- No embedded domain business logic in orchestrator core.
- Contracts and schemas remain source of truth for runtime checks.
- Failure must be diagnosable from structured events.

## Non-Goals

- Full production adapter ecosystem in phase 4.
- Runtime plugin authoring UX improvements.
