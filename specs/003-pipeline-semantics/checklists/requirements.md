# Requirements Checklist: Pipeline Semantics & Dependency Resolution

## Functional Requirements

### FR-001: Pipeline YAML Schema

- [ ] `pipeline.schema.yaml` is created and validated
- [ ] Schema includes `schema_version`, `stages`, `failure_behavior`, `resumable`
- [ ] Stage schema includes `id`, `name`, `execution_order`, `prerequisites`, `validation_gates`
- [ ] Example pipeline file validates against schema

### FR-002: Topological Dependency Resolution

- [ ] Dependency resolver computes topological sort from `depends_on` declarations
- [ ] Sort uses domain ID as tiebreaker for deterministic ordering
- [ ] Resolver handles empty dependency lists correctly
- [ ] Resolver handles single-domain pipelines correctly

### FR-003: Dependency Validation

- [ ] Missing dependencies are detected (references non-existent domain ID)
- [ ] Circular dependencies are detected (including self-references)
- [ ] Cycle path is reported (e.g., `A → B → C → A`)
- [ ] Schema version mismatches are detected and reported
- [ ] Validation fails before any domain execution begins

### FR-004: Configurable Pipeline Execution

- [ ] Pipeline order is configurable via `pipeline.yaml` without code changes
- [ ] Custom `execution_order` is respected when it doesn't violate dependencies
- [ ] Custom order that violates dependencies falls back to topological sort with warning
- [ ] `failure_behavior` is configurable (halt, skip_remaining, continue)
- [ ] `resumable` flag is respected

### FR-005: Active Domain Selection

- [ ] `/domain <name>` command updates active domain
- [ ] Active domain is persisted in session context
- [ ] Active domain persists across session restarts (file persistence)
- [ ] Default domain is first in pipeline order when none is set

### FR-006: Domain-Scoped Commands

- [ ] `/validate` scopes to active domain when set
- [ ] `/export` scopes to active domain when set
- [ ] Other domain-specific commands respect active domain context
- [ ] Commands without active domain default to pipeline-first domain with warning

### FR-007: Resumable Pipelines

- [ ] Pipeline state is persisted to `.specify/pipeline-state.json`
- [ ] Failed pipeline restarts from last failed stage
- [ ] Completed stages are skipped on restart
- [ ] State file is validated on load

### FR-008: Failure Behavior

- [ ] `halt` behavior stops execution immediately
- [ ] `skip_remaining` skips all remaining stages
- [ ] `continue` logs failure and proceeds to next stage
- [ ] Default failure behavior is `halt`

## Success Criteria

### SC-001: Deterministic Execution

- [ ] Same pipeline configuration produces identical execution order in different environments
- [ ] Test verifies order consistency across at least 3 different domain configurations

### SC-002: Circular Dependency Detection

- [ ] Self-reference detection test passes
- [ ] 2-node cycle detection test passes
- [ ] N-node cycle detection test passes
- [ ] Cycle path is correctly reported in all cases

### SC-003: Missing Dependency Errors

- [ ] Error message identifies missing domain ID
- [ ] Error message identifies referencing domain
- [ ] Error is surfaced before any domain execution

### SC-004: Schema Version Mismatches

- [ ] Mismatch is detected and reported
- [ ] Report includes expected version and actual version
- [ ] Pipeline fails before execution

### SC-005: Resumable Pipeline Restart

- [ ] Simulated stage failure is recovered on restart
- [ ] Completed stages are skipped
- [ ] Failed stage is re-executed
- [ ] State file is correctly updated

### SC-006: Active Domain Scoping

- [ ] Commands with active domain target only that domain
- [ ] Commands without active domain use default behavior
- [ ] Active domain persists across session restarts

## Edge Cases

- [ ] `pipeline.yaml` is missing — defaults to single-domain behavior with warning
- [ ] Domain declares dependency on itself — rejected as circular
- [ ] Two domains have identical dependency sets — stable deterministic order
- [ ] Domain `schema_version` incompatible with pipeline — fails fast with clear error
