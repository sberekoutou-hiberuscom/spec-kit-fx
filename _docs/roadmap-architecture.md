# Roadmap — Architecture Compatibility & Documentation v0.1

## Purpose

This roadmap defines the implementation work for SOF v0.1 with two primary outcomes:

1. Preserve compatibility with the current architecture direction and command model.
2. Produce architecture documentation detailed enough for an implementation agent to execute work with low ambiguity.

The roadmap assumes the current v0.1 scope remains centered on constitution, product, UX, and UI while keeping the framework core domain-agnostic and plugin-oriented. Manifest-driven plugin systems typically rely on schema validation, explicit dependency declarations, and deterministic load ordering; those practices are included here to reduce ambiguity and prevent plugin-order failures.[cite:16][cite:21][cite:24]

## Planning assumptions

- Canonical source of truth remains YAML; Markdown is generated from canonical specifications rather than authored as the source.
- The orchestrator remains free of domain-specific logic; domain behavior lives in plugins.
- Domain loading remains manifest-driven.
- Pipeline execution order is configurable, not hardcoded.
- External adapters remain non-authoritative sync targets.
- Phase 0 implementation scope remains limited to Constitution, Product, UX, and UI.

## Delivery goals

By the end of v0.1, the project should provide:

- A documented architecture baseline.
- A compatibility contract for repository structure, commands, manifests, and canonical objects.
- A minimal but working orchestration engine.
- A domain plugin contract with validation hooks.
- A versioned roadmap that can guide agent-driven implementation.

## Definition of done for v0.1

v0.1 is complete when the following are true:

- Existing command semantics are preserved or explicitly mapped.
- Core architecture documentation exists and matches the actual implementation structure.
- Pipeline stages for Constitution → Product → UX → UI can execute in order.
- Domain manifests are validated before execution.
- Dependency resolution is deterministic and fails clearly on missing or circular dependencies, which is a standard safeguard in manifest-based plugin systems.[cite:20][cite:21]
- Canonical YAML objects can be validated and rendered to Markdown.
- Validation errors are actionable and tied to identifiable domain objects.

## Workstreams

| Workstream | Objective | Main outputs |
|---|---|---|
| Compatibility | Preserve existing workflow and repository assumptions | Compatibility matrix, migration notes, command mapping |
| Architecture docs | Make architecture executable by agents and developers | Architecture docs, contracts, schemas, glossary |
| Orchestration core | Implement the runtime engine without domain logic leakage | Loader, dependency resolver, pipeline executor |
| Domain system | Standardize plugin/domain behavior | Manifest schema, lifecycle hooks, validators |
| Canonical model | Standardize machine-readable specifications | Object schema, references, IDs, export rules |
| Validation | Catch structural and semantic errors early | Schema validation, graph validation, reference checks |
| Outputs | Turn canonical YAML into human and tool-friendly outputs | Markdown generator, export stubs, adapter interfaces |

## Phase 1 — Baseline and compatibility freeze

### Objectives

Lock the current architecture intent, document compatibility boundaries, and prevent accidental drift during implementation.

### Tasks

- Create a v0.1 architecture baseline document derived from the current architecture text.
- Define the compatibility surface:
  - repository structure;
  - command set (`/init`, `/constitution`, `/spec`, `/plan`, `/tasks`, `/implement`, `/domain`, `/sync`, `/validate`, `/export`);
  - domain directory contract;
  - manifest fields;
  - canonical object fields.
- Create a compatibility matrix with three statuses per item: preserved, clarified, deferred.
- Define non-goals for v0.1 to stop scope creep.
- Establish version tags for documents and schemas.
- Add architecture terminology glossary to avoid synonym drift across docs and implementation.

### Deliverables

- `docs/architecture/baseline-v0.1.md`
- `docs/architecture/compatibility-matrix.md`
- `docs/architecture/glossary.md`
- `docs/architecture/non-goals-v0.1.md`

### Acceptance criteria

- Every major concept in the current architecture has one authoritative definition.
- Compatibility-sensitive areas are explicitly listed.
- Deferred topics are documented rather than left implicit.

## Phase 2 — Core contracts and schema design

### Objectives

Turn the conceptual architecture into explicit contracts that an orchestrator and domain plugins can implement consistently.

### Tasks

- Define the domain manifest schema:
  - `name`;
  - `version`;
  - `depends_on`;
  - `entrypoint`;
  - `exports`;
  - `validators`;
  - `adapters`;
  - optional `capabilities` and `schema_version`.
- Define the canonical object schema for v0.1:
  - `id`;
  - `type`;
  - `name`;
  - `description`;
  - `status`;
  - `source`;
  - `references`;
  - `metadata`.
- Add compatibility-safe extensions to the object model without breaking the original shape:
  - `domain_owner`;
  - `schema_version`;
  - `created_from` or `derived_from`;
  - `updated_at`.
- Define identifier conventions for cross-domain traceability.
- Define reference semantics:
  - upstream reference;
  - derived reference;
  - validation reference;
  - export reference.
- Create YAML schemas for manifests and canonical objects because schema-backed validation is the standard mechanism for enforcing manifest structure and preventing broken references in manifest-driven systems.[cite:16][cite:20][cite:24]

### Deliverables

- `schemas/domain-manifest.schema.yaml`
- `schemas/canonical-object.schema.yaml`
- `docs/contracts/domain-contract.md`
- `docs/contracts/object-contract.md`
- `docs/contracts/id-and-reference-rules.md`

### Acceptance criteria

- All required fields are documented and machine-validatable.
- Schema validation can reject malformed manifests and malformed objects.
- Contract docs distinguish required, optional, and deferred fields.

## Phase 3 — Dependency resolution and pipeline semantics

### Objectives

Make pipeline execution deterministic while preserving configurability and future extensibility.

### Tasks

- Define `pipeline.yaml` schema.
- Specify stage semantics:
  - execution order;
  - prerequisites;
  - validation gates;
  - resumability;
  - failure behavior.
- Implement domain dependency resolution based on manifest declarations.
- Topologically sort domain load and execution order from dependencies because dependency graphs are more reliable than implicit or alphabetical plugin loading.[cite:21][cite:25]
- Detect and fail on:
  - missing dependencies;
  - circular dependencies;
  - incompatible schema versions.
- Define how the active domain is selected and persisted within a session context.
- Document how the pipeline differs from domain dependency order when manual commands are invoked.

### Deliverables

- `schemas/pipeline.schema.yaml`
- `docs/architecture/pipeline-semantics.md`
- `docs/architecture/dependency-resolution.md`
- `docs/architecture/active-domain-model.md`

### Acceptance criteria

- Pipeline order can be configured without changing framework code.
- Dependency failures are surfaced before plugin execution.
- Execution order is reproducible across environments.

## Phase 4 — Orchestration engine skeleton

### Objectives

Implement the framework core as an orchestration runtime with no embedded domain logic.

### Tasks

- Implement project bootstrap for loading configuration and locating `specs/`.
- Implement manifest discovery from domain directories; discovery-plus-validation is a common control-plane pattern in plugin architectures.[cite:16][cite:24]
- Implement manifest validation before runtime activation.
- Implement dependency resolver and stage executor.
- Implement lifecycle runner for:
  - Read Upstream;
  - Validate Inputs;
  - Generate Domain Objects;
  - Run Validators;
  - Export Specification;
  - Publish Outputs.
- Implement a runtime event model or structured logs for each lifecycle transition.
- Define error classes:
  - configuration error;
  - schema error;
  - dependency error;
  - validation error;
  - adapter sync error.
- Document the internal engine modules and boundaries.

### Deliverables

- `docs/architecture/orchestrator-modules.md`
- `docs/architecture/runtime-lifecycle.md`
- `docs/architecture/error-model.md`
- `src/core/` runtime skeleton

### Acceptance criteria

- The engine can discover, validate, order, and execute Phase 0 domains.
- Domain logic remains outside the orchestrator.
- Runtime logs make stage failures diagnosable.

## Phase 5 — Domain plugin SDK and repository conventions

### Objectives

Standardize how domains are authored so new domains can be added without changing framework core.

### Tasks

- Define the domain plugin interface.
- Define minimum required folder structure:
  - `domain.yaml`;
  - `spec.md`;
  - `objects/`;
  - `validation/`;
  - `artifacts/`;
  - `exports/`.
- Specify domain plugin responsibilities versus framework responsibilities.
- Define validator contract:
  - input;
  - output;
  - severity;
  - object references;
  - fix hints.
- Define export contract:
  - generated Markdown;
  - JSON;
  - future external formats.
- Create starter templates for Constitution, Product, UX, and UI domains.
- Document authoring rules for future domains so extension is additive and not duplicative.

### Deliverables

- `docs/plugins/domain-sdk.md`
- `docs/plugins/validator-sdk.md`
- `docs/plugins/export-sdk.md`
- `templates/domains/constitution/`
- `templates/domains/product/`
- `templates/domains/ux/`
- `templates/domains/ui/`

### Acceptance criteria

- A new domain can be scaffolded from templates.
- Validators and exporters can be added without changing core runtime.
- Plugin docs are sufficient for agent-based generation of new domains.

## Phase 6 — Canonical YAML authoring and Markdown generation

### Objectives

Operationalize the “structured before generated” principle end to end.

### Tasks

- Define canonical storage layout for YAML objects inside each domain.
- Define object aggregation rules for domain-level and project-level views.
- Implement Markdown generation from canonical YAML.
- Define deterministic rendering rules so repeated generation produces stable outputs.
- Document traceability rendering from upstream references into generated Markdown.
- Define how generated Markdown should mark provenance and source object IDs.
- Create examples for Constitution, Product, UX, and UI outputs.
- Validate that the schema remains the source of truth and Markdown stays derived, which aligns with schema-first documentation pipelines.[cite:17]

### Deliverables

- `docs/architecture/yaml-to-markdown-flow.md`
- `docs/exports/markdown-rendering-rules.md`
- `src/generators/markdown/`
- sample generated docs for each Phase 0 domain

### Acceptance criteria

- YAML objects can be transformed into readable Markdown consistently.
- Generated docs preserve IDs and references.
- Markdown generation does not introduce new canonical data.

## Phase 7 — Validation engine and architecture guardrails

### Objectives

Prevent broken references, orphan objects, invalid manifests, and architecture drift.

### Tasks

- Implement schema validation for manifests, pipeline files, and canonical objects.
- Implement graph validation:
  - orphan object detection;
  - broken references;
  - circular references where disallowed;
  - missing upstream objects.
- Implement domain dependency validation.
- Implement repository structure validation.
- Define severity levels:
  - error;
  - warning;
  - info.
- Produce machine-readable validation reports.
- Add architecture linting rules that encode allowed dependency directions because explicit graph validation is a practical way to keep intended architecture enforceable over time.[cite:22][cite:26][cite:28]

### Deliverables

- `docs/validation/validation-taxonomy.md`
- `docs/validation/validation-report-format.md`
- `src/validation/`
- validation fixtures and failing examples

### Acceptance criteria

- Invalid structures fail before generation or sync.
- Validation results identify the failing object and rule.
- Architectural constraints can be automated rather than manually reviewed.

## Phase 8 — Command behavior and user workflow preservation

### Objectives

Preserve the familiar SDD interaction model while making it pipeline-aware.

### Tasks

- Define command routing behavior for each command.
- Document input/output behavior by active domain.
- Specify command preconditions and postconditions.
- Define how `/domain` changes or reports active domain.
- Define how `/validate` scopes current domain versus full pipeline.
- Define how `/export` selects targets and formats.
- Define how `/sync` delegates to adapters without changing source authority.
- Create a command compatibility table mapping legacy expectations to v0.1 behavior.

### Deliverables

- `docs/commands/command-contracts.md`
- `docs/commands/compatibility-mapping.md`
- `docs/commands/examples.md`

### Acceptance criteria

- Users can keep using the same command vocabulary.
- Domain-aware behavior is documented and predictable.
- Command docs are implementation-ready for an agent.

## Phase 9 — Phase 0 domain implementation pack

### Objectives

Deliver the first working vertical slice across Constitution, Product, UX, and UI.

### Tasks

- Scaffold each Phase 0 domain using the domain SDK.
- Define sample objects and references across the four domains.
- Implement validators for:
  - missing upstream objects;
  - orphan screens;
  - missing components;
  - invalid references.
- Implement domain-specific Markdown generation rules.
- Produce end-to-end sample project demonstrating traceability:
  - constitution principle;
  - product requirement;
  - UX journey;
  - UI screen/component.
- Verify the traceability chain remains navigable through IDs and references.

### Deliverables

- `specs/constitution/`
- `specs/product/`
- `specs/ux/`
- `specs/ui/`
- end-to-end sample project in repository

### Acceptance criteria

- A sample project can run through all four domains.
- References resolve correctly across domains.
- Generated Markdown is coherent and traceable.

## Phase 10 — Adapter foundations and non-authoritative sync

### Objectives

Prepare integration points for external tools while preserving canonical control inside SOF.

### Tasks

- Define adapter interface:
  - import;
  - export;
  - validate;
  - reconcile.
- Define adapter metadata and capability declaration in manifests.
- Specify directionality per adapter:
  - import-only;
  - export-only;
  - bidirectional with reconciliation.
- Define sync transaction flow:
  - import changes;
  - validate;
  - update YAML;
  - regenerate Markdown.
- Create stubs for Phase 0 adapters:
  - Product: Markdown, Notion, Confluence;
  - UX: FigJam, Miro;
  - UI: Figma, Penpot, Storybook.
- Document source-of-truth safeguards so adapter data cannot silently overwrite canonical data.

### Deliverables

- `docs/adapters/adapter-sdk.md`
- `docs/adapters/sync-lifecycle.md`
- `docs/adapters/source-of-truth-rules.md`
- adapter stubs for listed Phase 0 tools

### Acceptance criteria

- Adapter contracts are explicit before implementation deepens.
- Sync flow preserves canonical YAML authority.
- Adapter work can proceed independently of core orchestration work.

## Phase 11 — Agent-ready implementation package

### Objectives

Package the roadmap and architecture so implementation agents can execute work in bounded slices.

### Tasks

- Break every phase into agent-sized tasks with file targets and expected outputs.
- Add task dependencies and parallelization notes.
- Add acceptance criteria for each task.
- Add “definition of ready” and “definition of done” templates.
- Add implementation order recommendation:
  1. schemas;
  2. dependency resolver;
  3. orchestrator skeleton;
  4. validator engine;
  5. markdown generator;
  6. Phase 0 domains;
  7. adapter stubs.
- Create a task board view in Markdown for ingestion by an implementation agent.

### Deliverables

- `docs/roadmap/agent-task-pack.md`
- `docs/roadmap/task-dependency-map.md`
- `docs/roadmap/implementation-order.md`

### Acceptance criteria

- An implementation agent can pick a task with clear inputs, outputs, and constraints.
- Task sequencing minimizes rework.
- Parallelizable work is clearly identified.

## Task backlog by phase

| ID | Phase | Task | Depends on |
|---|---|---|---|
| A1 | 1 | Freeze v0.1 architecture baseline | None |
| A2 | 1 | Create compatibility matrix | A1 |
| A3 | 1 | Define non-goals and glossary | A1 |
| B1 | 2 | Draft manifest schema | A1 |
| B2 | 2 | Draft canonical object schema | A1 |
| B3 | 2 | Define ID/reference rules | B1, B2 |
| C1 | 3 | Draft pipeline schema | B1 |
| C2 | 3 | Implement dependency resolver | B1, C1 |
| C3 | 3 | Define active-domain model | C1 |
| D1 | 4 | Implement manifest discovery and validation | B1 |
| D2 | 4 | Implement lifecycle runner | C2, D1 |
| D3 | 4 | Define runtime logs and error model | D1 |
| E1 | 5 | Write domain SDK | B1, D2 |
| E2 | 5 | Write validator/export SDKs | E1 |
| E3 | 5 | Build Phase 0 domain templates | E1 |
| F1 | 6 | Define YAML storage rules | B2 |
| F2 | 6 | Build Markdown generator | F1, D2 |
| F3 | 6 | Add traceability rendering | F2, B3 |
| G1 | 7 | Build schema validation engine | B1, B2, C1 |
| G2 | 7 | Build graph/reference validation | B3, G1 |
| G3 | 7 | Add architecture guardrails | G2 |
| H1 | 8 | Specify command contracts | A2, C3 |
| H2 | 8 | Write command compatibility mapping | H1 |
| I1 | 9 | Scaffold Constitution/Product/UX/UI domains | E3, F2 |
| I2 | 9 | Implement Phase 0 validators | I1, G2 |
| I3 | 9 | Produce sample end-to-end project | I1, I2, F3 |
| J1 | 10 | Write adapter SDK | E1 |
| J2 | 10 | Define sync lifecycle and safeguards | J1, G1 |
| J3 | 10 | Build adapter stubs | J1 |
| K1 | 11 | Build agent task pack | A2, B3, C2, D2 |
| K2 | 11 | Build task dependency map | K1 |
| K3 | 11 | Finalize implementation order | K1, K2 |

## Suggested execution order

### Track 1 — Documentation first

- Phase 1
- Phase 2
- Phase 3
- Phase 8
- Phase 11

### Track 2 — Runtime core

- Phase 4
- Phase 7
- Phase 6

### Track 3 — Domain delivery

- Phase 5
- Phase 9
- Phase 10

This ordering keeps architecture and compatibility documentation ahead of deep implementation, which is important when roadmap and documentation need to stay synchronized with product decisions.[cite:18]

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Architecture doc drifts from code | High | Treat schemas and contracts as versioned artifacts reviewed alongside implementation changes.[cite:18] |
| Plugin order bugs | High | Resolve dependencies explicitly and topologically sort execution before activation.[cite:21] |
| Manifest inconsistency across domains | High | Enforce schema validation and version checks at load time.[cite:16][cite:20] |
| Domain duplication | Medium | Add ownership rules and ID/reference conventions in contract docs. |
| Adapter overwrites canonical data | High | Make adapter reconciliation explicit and preserve YAML as source of truth. |
| Validation noise reduces trust | Medium | Define severity taxonomy and actionable error reporting. |

## Agent execution guidance

Each implementation task should include:

- objective;
- input files;
- output files;
- invariants;
- acceptance criteria;
- examples;
- blocking dependencies.

Recommended task template:

```md
### Task: <id>
Objective:
Inputs:
Outputs:
Constraints:
Steps:
Acceptance criteria:
```

## Immediate next tasks

1. Freeze the baseline architecture text into versioned docs.
2. Write manifest, pipeline, and canonical object schemas.
3. Document dependency resolution and active-domain semantics.
4. Implement manifest discovery, validation, and pipeline execution skeleton.
5. Add Markdown generation and validation engine.
6. Scaffold Constitution, Product, UX, and UI domains.
7. Package work into an agent task pack.
