# Architecture Baseline — v0.1

Version: 0.1
Date: 2026-06-30

This document is the authoritative architecture baseline for spec-kit-fx v0.1. It records the core assumptions, pipeline shape, repository layout, and compatibility commitments that guide implementation work and agent-driven automation.

Overview

- Orchestration model: manifest-driven, plugin-oriented. The orchestrator is intentionally domain-agnostic and executes a pipeline of domain stages declared in a repository-level manifest.
- Canonical source: YAML; Markdown is a generated, human-readable representation derived from canonical YAML objects.
- Domains: constitution, product, ux, ui (Phase 0). Additional domains may be added with the same contract.
- Validation: schema-first validation for manifests and canonical objects; a validator CLI and CI smoke checks are provided.

Pipeline (example)

```yaml
pipeline:
  - constitution
  - product
  - ux
  - ui
```

Repository layout (selected)

- specs/: feature specs and domain artifacts
- schemas/: JSON/YAML schemas for manifests and canonical objects
- _docs/: hand-authored docs (architecture, roadmap)
- .specify/: project metadata, templates, and scripts

Compatibility commitments

See docs/architecture/compatibility-matrix.md for the detailed compatibility surface and the preserved/clarified/deferred status for each item.

Ratification

This baseline was ratified as the Phase 1 freeze on 2026-06-30 (see specs/001-document-architecture/spec.md Clarifications). Changes to this baseline require a documented amendment and a PR with maintainer approval.
