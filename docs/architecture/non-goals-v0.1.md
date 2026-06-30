# Non-Goals — v0.1

These items are explicitly out-of-scope for v0.1 so work stays focused and deliverable.

- Full adapter implementations for external tools (Figma, Notion, Storybook). Adapters are scoped to SDK/contract documentation in v0.1; implementations are Phase 10.
- A fully-featured orchestration runtime with rich event model and plugin sandboxing. v0.1 only requires a skeleton and verification that Phase 0 domains can be ordered and validated.
- Large-scale refactors of the CLI surface that would break downstream templates or installations. Any breaking changes require a separate migration release and explicit opt-in.
- Automated migration tooling that rewrites existing upstream templates or project files. Migration guidance and mapping are delivered in docs; automated migrations are deferred.
