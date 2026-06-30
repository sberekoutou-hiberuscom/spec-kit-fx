# Canonical Object Contract (v0.1)

This contract defines the canonical object model used by domains and adapters.

## Required Fields

- `id`
- `type`
- `name`
- `description`
- `status`
- `source`
- `references`
- `metadata`

## Compatibility Extensions

- `domain_owner`
- `schema_version`
- `created_from` or `derived_from`
- `updated_at`

## Rules

- Required fields must remain stable unless a versioned breaking change is declared.
- References must resolve to known objects or documented external sources.
- Schema validation is mandatory before generation/export.
