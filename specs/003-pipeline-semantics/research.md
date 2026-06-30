# Research: Pipeline Semantics & Dependency Resolution

This document captures the research findings for Phase 3: dependency resolution and pipeline semantics.

## Research Area 1: Topological Sort Algorithms

### Options Considered

1. **Kahn's Algorithm** — iterative, removes nodes with no incoming edges
2. **DFS-based Topological Sort** — recursive, uses post-order traversal

### Decision: Kahn's Algorithm

**Rationale**: Kahn's algorithm naturally detects cycles (if the sorted result contains fewer nodes than the graph, a cycle exists). This aligns with our requirement to detect and reject circular dependencies. DFS-based approaches require additional cycle detection logic.

**Implementation**: Use `networkx` library's `topological_sort` and `is_directed_acyclic_graph` functions for production code, with custom implementations for unit testing.

## Research Area 2: Cycle Detection

### Options Considered

1. **DFS with coloring** — white/gray/black node states
2. **Kahn's algorithm** — cycle detected when sorted result is incomplete
3. **Tarjan's algorithm** — finds strongly connected components

### Decision: Kahn's algorithm + DFS path reconstruction

**Rationale**: Kahn's algorithm provides the cycle detection we need. For error reporting, we augment with DFS path reconstruction to report the full cycle path (e.g., `A → B → C → A`) as required by the spec.

## Research Area 3: Pipeline State Persistence

### Options Considered

1. **JSON file** — simple, human-readable, easy to parse
2. **SQLite database** — structured, supports queries, but adds dependency
3. **YAML file** — consistent with existing pipeline configuration format

### Decision: JSON file (`.specify/pipeline-state.json`)

**Rationale**: JSON is the most widely supported format across languages and platforms. It's simple, human-readable, and doesn't require additional dependencies. The pipeline state is relatively simple (no complex queries needed), so a database is overkill.

**Format**:

```json
{
  "pipeline_id": "string",
  "session_id": "string",
  "current_stage": "string",
  "completed_stages": ["string"],
  "failed_stages": ["string"],
  "status": "planned|running|paused|completed|failed",
  "updated_at": "ISO 8601 timestamp",
  "error_message": "string (optional)"
}
```

## Research Area 4: Active Domain Session Management

### Options Considered

1. **In-memory with file persistence** — session state in memory, persisted to disk for recovery
2. **Environment variables** — simple, but not persistent across sessions
3. **Dedicated session file** — `.specify/session.json` for session state

### Decision: In-memory with file persistence

**Rationale**: In-memory state provides fast access during a session. File persistence (`.specify/pipeline-state.json`) ensures state survives process restarts. This approach is consistent with the existing `.specify/` directory structure used for feature registration and constitution.

## Research Area 5: Failure Behavior Configuration

### Options Considered

1. **Enum-based configuration** — `halt`, `skip_remaining`, `continue`
2. **Script-based hooks** — allow custom scripts to define failure behavior
3. **YAML-based policy** — complex YAML structure for fine-grained control

### Decision: Enum-based configuration

**Rationale**: Simple enum-based configuration is sufficient for the v0.1 scope. It's easy to understand, validate, and extend. Script-based hooks and complex YAML policies can be added in future phases if needed.

**Values**:

- `halt` (default): Stop pipeline execution immediately on failure
- `skip_remaining`: Skip all remaining stages after a failure
- `continue`: Log the failure and continue with the next stage

## Research Area 6: Schema Version Compatibility

### Options Considered

1. **Exact version match** — domain schema_version must exactly match pipeline schema_version
2. **Semantic versioning with range** — domain schema_version must be within a compatible range
3. **Major version match** — domain schema_version major version must match pipeline major version

### Decision: Exact version match for v0.1

**Rationale**: For v0.1, exact version matching is the safest approach. It ensures complete compatibility between domains and the pipeline. Semantic versioning with ranges or major version matching can be added in future phases as the schema evolves.

## Research Area 7: Tiebreaker for Topological Sort

### Options Considered

1. **Alphabetical by domain ID** — deterministic, easy to understand
2. **Alphabetical by domain name** — more user-friendly, but less stable if names change
3. **Order of appearance in pipeline.yaml** — respects user intent, but requires explicit ordering

### Decision: Alphabetical by domain ID

**Rationale**: Domain IDs are stable identifiers that don't change. Alphabetical ordering by domain ID provides a deterministic tiebreaker that is easy to understand and verify. This is consistent with the existing convention of using domain IDs as primary identifiers.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| NetworkX adds a dependency | Medium | Use only for graph operations; provide fallback implementation if needed |
| Pipeline state file corruption | Medium | Validate state file on load; provide recovery mechanism |
| Large dependency graphs slow to resolve | Low | Topological sort is O(V+E); performance is acceptable for typical domain counts |
| Schema version mismatches break pipelines | High | Fail fast with clear error messages; validate before execution |
