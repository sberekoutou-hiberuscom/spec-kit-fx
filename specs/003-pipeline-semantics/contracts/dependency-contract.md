# Dependency Contract

Scope: Defines the contract for domain dependency resolution, graph validation, and error reporting.

## Invariants

- All `depends_on` references in domain manifests must resolve to existing domain IDs.
- The dependency graph must be acyclic; cycles are rejected before execution.
- Self-references in `depends_on` are rejected as circular dependencies.
- Schema version mismatches between domains are detected and reported.
- Topological sort produces a deterministic order using domain ID as tiebreaker.

## Required Inputs

- Domain manifests with `depends_on` declarations
- `schemas/domain-manifest.schema.yaml` (from Phase 2)

## Required Outputs

- Dependency graph representation
- Topologically sorted domain execution order
- Error reports for missing dependencies, cycles, and version mismatches

## Acceptance Checks

1. Missing dependency errors identify the missing domain ID and the referencing domain.
2. Circular dependencies are detected with full cycle path (e.g., `A → B → C → A`).
3. Schema version mismatches report expected vs. actual version.
4. Execution order is reproducible across environments.

## Out of Scope

- Dynamic dependency resolution at runtime
- Dependency version ranges (deferred to v0.2)
- Automatic dependency resolution (manual declaration only)
