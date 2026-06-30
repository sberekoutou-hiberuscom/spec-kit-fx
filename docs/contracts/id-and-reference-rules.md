# ID and Reference Rules

This document standardizes identifiers and cross-domain reference semantics.

## Identifier Rules

- IDs are stable, unique, and immutable within a version.
- IDs should be machine-friendly and deterministic.
- Versioned changes must preserve traceability to prior IDs.

## Reference Types

- Upstream reference
- Derived reference
- Validation reference
- Export reference

## Constraints

- References must be explicit and resolvable.
- Broken references are validation errors.
- Circular references are rejected where disallowed by contract.

## Traceability

Generated outputs should preserve source object IDs and reference links for auditability.
