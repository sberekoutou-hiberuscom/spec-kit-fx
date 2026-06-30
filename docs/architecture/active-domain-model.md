# Active Domain Model

This document defines how the active domain is selected and persisted for command scoping.

## Purpose

Active domain state lets domain-specific commands operate predictably in multi-domain projects.

## Data

- `domain_id`
- `session_id`
- `updated_at`

## Behavior

- `/domain <name>` sets active domain.
- Domain-scoped commands (`/validate`, `/export`, and related operations) use active domain when set.
- If unset, tooling defaults to the first domain in resolved dependency order and emits a warning.

## Persistence

State is persisted in `.specify/pipeline-state.json` for resumability across process restarts.

## Validation

- Active domain must exist in discovered manifests.
- Invalid active domain state is rejected and replaced with default resolution.
