# Runtime Lifecycle

This document specifies lifecycle transitions executed by the orchestrator.

## Lifecycle Stages

1. Read Upstream
2. Validate Inputs
3. Generate Domain Objects
4. Run Validators
5. Export Specification
6. Publish Outputs

## Transition Semantics

- A stage can start only when prerequisites pass.
- Validation failures prevent downstream stage execution unless configured otherwise.
- Each stage emits `started`, `passed`, or `failed` events.

## Re-entry

When resumability is enabled, completed stages are skipped and execution resumes at first unresolved failure.

## Observability

Each transition includes stage ID, domain context, timestamp, and status for debugging and CI diagnostics.
