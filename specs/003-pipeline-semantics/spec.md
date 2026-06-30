# Feature Specification: Pipeline Semantics & Dependency Resolution

**Feature Branch**: `003-pipeline-semantics`

**Created**: 2026-06-30

**Status**: Draft

**Input**: User description: "phase 3 Dependency resolution and pipeline semantics"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deterministic Pipeline Execution (Priority: P1)

As a pipeline operator, I need domain execution order to be determined by dependency declarations rather than filesystem order or alphabetical sorting, so that pipelines are reproducible across environments and contributors.

**Why this priority**: Non-deterministic execution order causes flaky builds, silent data corruption, and environment-specific failures.

**Independent Test**: Create two domains with a circular dependency declaration and verify the pipeline rejects them with a clear error. Create three domains with a linear dependency chain and verify execution order matches the topological sort.

**Acceptance Scenarios**:

1. **Given** a set of domain manifests with `depends_on` declarations, **When** the pipeline executor runs, **Then** domains execute in topological order derived from the dependency graph.
2. **Given** a `pipeline.yaml` with a custom stage order, **When** the pipeline runs, **Then** the custom order is respected unless it violates dependency constraints.
3. **Given** a domain with a missing dependency, **When** the pipeline starts, **Then** execution halts before any domain runs and a clear error identifies the missing dependency.

---

### User Story 2 - Pipeline Configuration Without Code Changes (Priority: P1)

As a framework maintainer, I need to configure pipeline stages, validation gates, and failure behavior through `pipeline.yaml` without modifying framework source code.

**Why this priority**: Configuration-driven pipelines enable rapid iteration and per-project customization without requiring framework releases.

**Independent Test**: Modify `pipeline.yaml` to add a new stage, change validation gate severity, and toggle resumability; verify the pipeline respects all changes without recompilation.

**Acceptance Scenarios**:

1. **Given** a `pipeline.yaml` with a new stage definition, **When** the orchestrator loads the pipeline, **Then** the new stage is included in execution without code changes.
2. **Given** a `pipeline.yaml` with `resumable: true`, **When** a stage fails and the pipeline is restarted, **Then** execution resumes from the last failed stage instead of restarting from the beginning.
3. **Given** a `pipeline.yaml` with a custom failure behavior (e.g., `on_failure: skip_remaining`), **When** a stage fails, **Then** the pipeline behaves according to the configured policy.

---

### User Story 3 - Active Domain Selection & Session Context (Priority: P2)

As a developer working on a specific domain, I need the system to track and persist the active domain within a session so that commands operate on the correct context.

**Why this priority**: Multi-domain projects require clear context boundaries; without an active domain model, commands operate ambiguously.

**Independent Test**: Switch active domain via `/domain` command, verify subsequent commands target the new domain, and confirm the active domain persists across session restarts.

**Acceptance Scenarios**:

1. **Given** a multi-domain project, **When** the user runs `/domain <name>`, **Then** the active domain is updated and persisted in session state.
2. **Given** an active domain is set, **When** the user runs `/validate`, **Then** validation is scoped to the active domain only.
3. **Given** no active domain is set, **When** the user runs a domain-specific command, **Then** the system defaults to the first domain in pipeline order and warns the user.

---

### Edge Cases

- What if `pipeline.yaml` is missing? The orchestrator should default to single-domain behavior with a warning log.
- What if a domain declares a dependency on itself? The dependency resolver must detect and reject self-references as circular.
- What if two domains have identical dependency sets? The topological sort must produce a stable, deterministic order (e.g., by domain ID as tiebreaker).
- What if a domain's `schema_version` is incompatible with the pipeline's expected version? The resolver must fail fast with a clear version mismatch error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST define a `pipeline.yaml` schema that declares pipeline stages, their execution order, prerequisites, validation gates, resumability, and failure behavior.
- **FR-002**: The dependency resolver MUST compute a topological sort of domain execution order based on `depends_on` declarations in domain manifests.
- **FR-003**: The dependency resolver MUST detect and reject:
  - Missing dependencies (a domain references a non-existent domain ID).
  - Circular dependencies (any cycle in the dependency graph, including self-references).
  - Incompatible schema versions (domain `schema_version` does not match the pipeline's expected version).
- **FR-004**: Pipeline execution order MUST be configurable via `pipeline.yaml` without requiring source code changes.
- **FR-005**: The active domain MUST be selectable via command (e.g., `/domain <name>`) and persisted within the session context.
- **FR-006**: Domain-specific commands (e.g., `/validate`, `/export`) MUST scope their behavior to the active domain when one is set.
- **FR-007**: The pipeline MUST support resumability: when `resumable: true` is set in `pipeline.yaml`, a failed pipeline restarts from the last failed stage.
- **FR-008**: The pipeline MUST support configurable failure behavior (e.g., `on_failure: halt`, `on_failure: skip_remaining`, `on_failure: continue`) defined in `pipeline.yaml`.

### Key Entities

- **PipelineConfig**: Root pipeline configuration (attributes: `stages`, `failure_behavior`, `resumable`, `schema_version`).
- **PipelineStage**: A named stage in the pipeline (attributes: `id`, `name`, `prerequisites`, `validation_gates`, `execution_order`).
- **DomainDependency**: A dependency edge between domains (attributes: `domain_id`, `depends_on`, `schema_version`).
- **ActiveDomain**: The currently selected domain for scoped operations (attributes: `domain_id`, `session_id`, `updated_at`).
- **DependencyGraph**: Directed acyclic graph of domain dependencies used for topological sorting (attributes: `nodes`, `edges`, `sorted_order`).

### Validation Rules

- `pipeline.yaml` MUST include `schema_version` matching the pipeline specification version.
- All `depends_on` references MUST resolve to existing domain IDs.
- The dependency graph MUST be acyclic; cycles are rejected before execution.
- `execution_order` values MUST be unique integers within a pipeline.
- `validation_gates` MUST reference valid validator names defined in domain manifests.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Pipeline execution order is deterministic: running the same `pipeline.yaml` and domain manifests in different environments produces identical execution order.
- **SC-002**: All circular dependency cases are detected and rejected before any domain execution begins (measured by unit tests covering self-references, 2-node cycles, and N-node cycles).
- **SC-003**: Missing dependency errors identify the missing domain ID and the domain that references it.
- **SC-004**: Schema version mismatches are detected and reported with the expected version and the actual version.
- **SC-005**: Resumable pipelines restart from the last failed stage (verified by simulating a stage failure and confirming the restart skips completed stages).
- **SC-006**: Active domain scoping is verified: commands run with an active domain target only that domain's artifacts.

## Assumptions

- Domain manifests are already validated against their schema before dependency resolution begins.
- The pipeline executor runs in a single-threaded context for simplicity; parallel execution is deferred.
- Session state is stored in-memory during a session and persisted to disk for recovery.

## Clarifications

### Session 2026-06-30

- Q: Should pipeline order override dependency order? → A: Pipeline `execution_order` takes precedence when it does not violate dependency constraints; if a custom order violates dependencies, the resolver falls back to topological sort and warns.
- Q: How should circular dependencies be reported? → A: Report the full cycle path (e.g., `A → B → C → A`) so developers can identify the root cause.
- Q: Should resumability persist across process restarts? → A: Yes — resumability state is persisted to a `.specify/pipeline-state.json` file so pipelines can survive process restarts.
