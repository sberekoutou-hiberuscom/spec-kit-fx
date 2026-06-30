# Implementation Plan: Pipeline Semantics & Dependency Resolution

**Branch**: `feature/domain-orchestration`
**Date**: 2026-06-30
**Spec**: [spec.md](spec.md)

## Summary

Implement Phase 3 of the SOF v0.1 roadmap: dependency resolution and pipeline semantics. This phase introduces a `pipeline.yaml` schema, a topological dependency resolver, configurable pipeline execution semantics, and active domain management. The implementation builds on the domain manifest and canonical object schemas created in Phase 2.

## Technical Context

- Language/Version: Python 3.11+ for tooling, YAML for configuration
- Primary Dependencies: `PyYAML`, `jsonschema`, `networkx` (for graph operations)
- Storage: Git repository (`schemas/`, `specs/`, `src/`)
- Testing: `pytest`, schema validation, graph algorithm tests
- Target Platform: macOS/Linux/Windows contributors and CI
- Project Type: Configuration-driven pipeline orchestration
- Constraints: Strict backward compatibility for existing command names/templates; pipeline configuration must not require code changes
- Scale/Scope: Pipeline schema, dependency resolver, active domain model, and supporting documentation

## Constitution Check

Constitution principles are satisfied as follows:

- Code Quality & Architecture: pipeline configuration is schema-driven, dependency resolution is deterministic
- Test-Backed Change: graph algorithm tests, schema validation tests, and integration tests are included
- CLI Consistency: command naming/behavior remains unchanged; `/domain` command adds active domain context
- Offline-First: no network-required behavior added to pipeline execution
- Minimal Dependencies: only lightweight validation dependencies are used (`PyYAML`, `jsonschema`, `networkx`)

Result: PASS

## Project Structure

### Documentation (this feature)

```text
specs/003-pipeline-semantics/
├── spec.md
├── plan.md
├── data-model.md
├── research.md
├── contracts/
│   ├── pipeline-contract.md
│   └── dependency-contract.md
└── checklists/
    └── requirements.md
```

### Repository Deliverables Touched by Phase 3

```text
schemas/
├── pipeline.schema.yaml
├── pipeline-state.schema.yaml
└── examples/
    ├── pipeline-example.yaml
    └── pipeline-state-example.yaml

src/core/
├── pipeline/
│   ├── pipeline_config.py
│   ├── pipeline_stage.py
│   └── pipeline_executor.py
├── dependency/
│   ├── dependency_graph.py
│   └── dependency_resolver.py
└── domain/
    └── active_domain.py

tests/
├── test_pipeline_config.py
├── test_dependency_graph.py
├── test_dependency_resolver.py
└── test_active_domain.py
```

## Phase 1: Schema Design

Planned outputs:

1. `pipeline.schema.yaml` — schema for pipeline configuration
2. `pipeline-state.schema.yaml` — schema for persisted pipeline state
3. Example pipeline and pipeline-state files under `schemas/examples/`
4. Schema validation tests for pipeline configuration

## Phase 2: Dependency Resolution

Planned outputs:

1. `DependencyGraph` class — represents domain dependencies as a directed graph
2. `DependencyResolver` class — computes topological sort, detects cycles, validates references
3. Unit tests for graph algorithms (topological sort, cycle detection, missing reference detection)
4. Integration tests for dependency resolution with real domain manifests

## Phase 3: Pipeline Execution Semantics

Planned outputs:

1. `PipelineConfig` class — loads and validates `pipeline.yaml`
2. `PipelineStage` class — represents a pipeline stage with execution semantics
3. `PipelineExecutor` class — executes stages in order, handles failure behavior, supports resumability
4. Unit tests for pipeline execution (normal flow, failure handling, resumability)
5. Integration tests for pipeline execution with real pipeline configurations

## Phase 4: Active Domain Management

Planned outputs:

1. `ActiveDomain` class — tracks and persists the active domain within a session
2. Session state persistence to `.specify/pipeline-state.json`
3. CLI integration for `/domain` command
4. Unit tests for active domain management
5. Integration tests for active domain scoping

## Phase 5: Documentation & Validation

Planned outputs:

1. Architecture docs: `docs/architecture/pipeline-semantics.md`, `docs/architecture/dependency-resolution.md`, `docs/architecture/active-domain-model.md`
2. Contract docs: `docs/contracts/pipeline-contract.md`, `docs/contracts/dependency-contract.md`
3. Lint and smoke checks pass locally
4. CI integration for pipeline schema validation

## Dependencies

- Depends on Phase 2 artifacts: `domain-manifest.schema.yaml`, `canonical-object.schema.yaml`
- Builds on existing domain manifest structure from Phase 2

## Acceptance Criteria

1. Pipeline order is configurable via `pipeline.yaml` without code changes.
2. Dependency failures are surfaced before any domain execution begins.
3. Execution order is reproducible across environments (deterministic topological sort).
4. All circular dependency cases are detected and rejected with clear error messages.
5. Resumable pipelines restart from the last failed stage.
6. Active domain scoping is verified: commands target only the active domain's artifacts.
