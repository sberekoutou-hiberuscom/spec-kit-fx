# Data Model: Pipeline Semantics & Dependency Resolution

This model defines the entities and relationships for pipeline configuration, dependency resolution, and active domain management.

## Entity: PipelineConfig

Root configuration for pipeline execution.

- schema_version: string (required) — version of the pipeline schema
- stages: array<PipelineStage> (required) — ordered list of pipeline stages
- failure_behavior: enum(halt, skip_remaining, continue) (optional, default: halt)
- resumable: boolean (optional, default: false)
- default_execution_order: integer (optional) — fallback order when no explicit order is set

Validation rules:

- `schema_version` must match the pipeline specification version
- All stage IDs must be unique
- All prerequisite references must resolve to existing stage IDs

## Entity: PipelineStage

A named stage in the pipeline with execution semantics.

- id: string (required) — unique stage identifier
- name: string (required) — human-readable stage name
- execution_order: integer (required) — position in execution sequence
- prerequisites: array<string> (optional) — stage IDs that must complete first
- validation_gates: array<string> (optional) — validator names to run before stage execution
- resumable: boolean (optional, inherits from PipelineConfig)

State transitions:

- planned → runnable → running → passed | failed

## Entity: DomainManifest

Domain-level manifest with dependency declarations.

- id: string (required) — unique domain identifier
- name: string (required) — human-readable domain name
- version: semver string (required)
- schema_version: string (required) — must match pipeline schema_version
- depends_on: array<string> (optional) — domain IDs this domain depends on
- entrypoint: string (optional) — entry point for domain execution
- exports: array<string> (optional) — artifacts this domain produces
- validators: array<string> (optional) — validators associated with this domain

Validation rules:

- `depends_on` references must resolve to existing domain IDs
- `schema_version` must match the pipeline's expected version
- No self-references in `depends_on`

## Entity: DependencyGraph

Directed acyclic graph representing domain dependencies.

- nodes: array<string> — domain IDs
- edges: array<DependencyEdge> — directed edges between domains
- sorted_order: array<string> — topologically sorted domain IDs
- is_acyclic: boolean — true if no cycles detected

Validation rules:

- All nodes must exist in the domain manifest registry
- All edges must reference valid domain IDs
- Cycles must be detected and reported with the full cycle path

## Entity: DependencyEdge

A single dependency relationship between two domains.

- from: string (required) — domain ID that has the dependency
- to: string (required) — domain ID that is depended upon
- schema_version: string (optional) — expected schema version for this dependency

## Entity: ActiveDomain

The currently selected domain for scoped operations.

- domain_id: string (required) — ID of the active domain
- session_id: string (required) — unique session identifier
- updated_at: timestamp (required) — last time the active domain was set
- created_at: timestamp (required) — when the active domain was first set

Validation rules:

- `domain_id` must reference an existing domain in the pipeline
- `session_id` must be unique per session

## Entity: PipelineState

Persisted state for resumable pipelines.

- pipeline_id: string (required) — unique pipeline execution ID
- session_id: string (required) — associated session ID
- current_stage: string (optional) — stage currently being executed
- completed_stages: array<string> (optional) — stages that have passed
- failed_stages: array<string> (optional) — stages that have failed
- status: enum(planned, running, paused, completed, failed) (required)
- updated_at: timestamp (required) — last state update time
- error_message: string (optional) — error details if status is failed

Validation rules:

- `current_stage` must be a valid stage ID
- `completed_stages` and `failed_stages` must not overlap
- `status` transitions must follow valid state machine rules

## Relationships

```mermaid
erDiagram
    PipelineConfig ||--o{ PipelineStage : contains
    PipelineConfig }o--|| DependencyGraph : uses
    PipelineStage ||--o{ string : has prerequisites
    PipelineStage ||--o{ string : has validation_gates
    DomainManifest }o--o{ string : depends_on
    DomainManifest ||--o{ string : has validators
    DependencyGraph ||--o{ DependencyEdge : contains
    DependencyEdge }o--|| DomainManifest : from
    DependencyEdge }o--|| DomainManifest : to
    ActiveDomain }o--|| DomainManifest : references
    PipelineState }o--|| PipelineConfig : belongs_to
    PipelineState }o--|| PipelineStage : tracks current_stage
```

## Validation Rules Summary

| Rule | Entity | Condition |
|------|--------|-----------|
| Unique stage IDs | PipelineConfig | All stage IDs must be unique |
| Resolvable prerequisites | PipelineStage | All prerequisite IDs must exist |
| No circular dependencies | DependencyGraph | Graph must be acyclic |
| Resolvable depends_on | DomainManifest | All depends_on IDs must exist |
| Schema version match | DomainManifest | schema_version must match pipeline |
| Valid domain reference | ActiveDomain | domain_id must exist in pipeline |
| Non-overlapping stages | PipelineState | completed_stages ∩ failed_stages = ∅ |
