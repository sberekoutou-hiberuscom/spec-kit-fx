# Dependency Resolution

This document specifies domain dependency resolution for deterministic load and execution order.

## Inputs

Dependencies are declared in domain manifests via `depends_on`.

## Rules

- All dependency IDs must resolve to known domains.
- Self-dependencies are invalid.
- Cycles are invalid and must fail before execution.
- Schema version compatibility is checked before activation.

## Resolution Algorithm

1. Build directed graph from `depends_on` edges.
2. Validate all nodes/edges.
3. Detect cycles.
4. Topologically sort domains.
5. Apply deterministic tie-breaker by domain ID.

## Error Cases

- Missing dependency: include missing ID and referencing domain.
- Circular dependency: include cycle path.
- Version mismatch: include expected and actual versions.

## Output

A reproducible domain order used by pipeline execution and startup validation.
