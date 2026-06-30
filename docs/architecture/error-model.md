# Error Model

This document defines runtime error classes and reporting expectations.

## Error Classes

- `ConfigurationError`
- `SchemaError`
- `DependencyError`
- `ValidationError`
- `AdapterSyncError`

## Required Fields

Every error should provide:

- `kind`
- `message`
- `object_ref` (when applicable)
- `hint` (actionable remediation)

## Reporting Rules

- Fail fast for configuration, schema, and dependency errors.
- Include deterministic context (domain, stage, object ID).
- Chain underlying exceptions where relevant.

## Severity Mapping

- Error: execution blocking
- Warning: non-blocking but requires attention
- Info: diagnostic context
