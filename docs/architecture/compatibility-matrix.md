# Compatibility Matrix — v0.1

This matrix records the compatibility status for important repository, CLI, and schema items for the v0.1 freeze. Status meanings:

- Preserved: Behavior/format intentionally preserved for backward compatibility.
- Clarified: Behavior preserved but documented with explicit expectations or options.
- Deferred: Decision or migration deferred to a future version.

| Area | Item | Status | Notes |
|---|---:|---|---|
| Repository layout | specs/ directory structure | Preserved | Domains under specs/ remain canonical locations |
| CLI | Core command names (`specify`, `speckit.*`) | Preserved | Strict backward compatibility (Option A). Breaking changes require migration path. |
| Templates | Built-in templates resolution | Clarified | Template override order documented; maintainers may update templates with migration notes. |
| Manifest schema | `schemas/domain-manifest.schema.yaml` shape | Preserved | Schema provided in repo; validator enforces structure. |
| Canonical object schema | `schemas/canonical-object.schema.yaml` shape | Preserved | Versioned schema; breaking changes need version bump. |
| Pipeline semantics | `pipeline.yaml` ordering and semantics | Clarified | Pipeline is configurable; orchestrator must respect ordering declared in pipeline.yaml. |
| Adapters | Adapter directionality metadata | Deferred | Adapter SDK and contracts are Phase 5 deliverable. |
| Markdown generation | YAML → Markdown rendering rules | Deferred | Stable rendering rules are Phase 6 work; Phase 1 documents intent only. |

If you disagree with any status, open a PR that updates this matrix and provides the migration notes or rationale.
