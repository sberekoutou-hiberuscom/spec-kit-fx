# Pipeline Contract

Scope: Defines the contract for pipeline configuration, execution, and state management.

## Invariants

- Pipeline configuration is defined in `pipeline.yaml` and validated against `schemas/pipeline.schema.yaml`.
- Pipeline execution order is deterministic: same configuration always produces same execution order.
- Domain logic remains outside the pipeline executor.
- Pipeline state is persisted to `.specify/pipeline-state.json` for resumability.
- Schema version mismatches between domains and pipeline are rejected before execution.

## Required Inputs

- `specs/003-pipeline-semantics/spec.md`
- `schemas/pipeline.schema.yaml`
- `schemas/pipeline-state.schema.yaml`
- Domain manifests from `specs/*/` directories

## Required Outputs

- Pipeline configuration validated against schema
- Topologically sorted execution order
- Pipeline state file for resumability
- Execution logs for each stage transition

## Acceptance Checks

1. Pipeline configuration validates against `pipeline.schema.yaml`.
2. Execution order is deterministic across environments.
3. Resumable pipelines restart from the last failed stage.
4. Failure behavior is configurable and respected.
5. Active domain scoping works for all domain-specific commands.

## Out of Scope

- Parallel stage execution
- Distributed pipeline execution
- Real-time pipeline monitoring dashboard
- Pipeline versioning (deferred to v0.2)
