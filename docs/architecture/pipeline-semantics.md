# Pipeline Semantics

This document defines how the phase 0 domain pipeline is configured and executed.

## Goals

- Deterministic execution order.
- Configurable stage sequencing without code edits.
- Clear prerequisites, validation gates, and failure behavior.

## Stage Model

Each stage declares:

- `id`: stable identifier
- `execution_order`: configured stage order
- `prerequisites`: required completed stage IDs
- `validation_gates`: checks executed before stage logic
- `resumable`: whether stage can resume from persisted state

## Execution Rules

1. Load pipeline configuration from `pipeline.yaml`.
2. Validate schema and stage references.
3. Resolve effective stage order.
4. Execute prerequisites and validation gates.
5. Run stage and emit structured lifecycle events.
6. Apply configured failure behavior.

## Failure Behavior

Supported policies:

- `halt`: stop immediately
- `skip_remaining`: end run after current failure
- `continue`: continue with next runnable stage

## Resumability

When enabled, stage status is persisted and reruns begin from the latest failed stage, skipping passed stages.

## Manual Commands vs Pipeline Order

Manual domain commands are scoped by active domain and may execute outside full pipeline sequencing. Full pipeline execution still enforces stage prerequisites and validation gates.
