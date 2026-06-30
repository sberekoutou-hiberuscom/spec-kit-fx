# Domain Contract (v0.1)

This contract defines required and optional fields for domain manifests.

## Required Fields

- `name`
- `version`
- `depends_on`
- `entrypoint`
- `exports`
- `validators`
- `adapters`

## Optional Fields

- `capabilities`
- `schema_version`

## Rules

- `depends_on` must reference known domains.
- Dependency cycles are invalid.
- Manifest schema version must be compatible with pipeline/schema expectations.

## Validation Outcome

Invalid manifests fail before pipeline/domain execution.
