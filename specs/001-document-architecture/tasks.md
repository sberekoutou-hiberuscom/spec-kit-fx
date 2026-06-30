---
description: "Tasks for Document Architecture feature (001-document-architecture)"
---

# Tasks: Document Architecture (001-document-architecture)

**Input**: Design documents from `specs/001-document-architecture/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `.specify/memory/constitution.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm baseline files and working structure for phases 1-4 delivery.

- [x] T001 Validate feature registration in `.specify/feature.json`
- [x] T002 [P] Verify architecture docs folder readiness in `docs/architecture/`
- [x] T003 [P] Verify contract docs folder readiness in `docs/contracts/`
- [x] T004 [P] Verify schema workspace readiness in `schemas/` and `schemas/examples/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Complete gating artifacts required before user-story execution.

**CRITICAL**: No user story work starts until these tasks are complete.

- [x] T005 Validate constitution compliance gate in `.specify/memory/constitution.md`
- [x] T006 [P] Validate domain manifest schema in `schemas/domain-manifest.schema.yaml`
- [x] T007 [P] Validate canonical object schema in `schemas/canonical-object.schema.yaml`
- [x] T008 [P] Validate schema examples in `schemas/examples/domain-manifest.example.yaml` and `schemas/examples/canonical-object.example.yaml`
- [x] T009 Run schema smoke validation with `scripts/bash/validate-schemas.sh`
- [x] T010 Run setup prerequisites check with `.specify/scripts/bash/check-prerequisites.sh`
- [x] T011 Run plan setup smoke check with `.specify/scripts/bash/setup-plan.sh`
- [ ] T012 Record baseline validation evidence in `specs/001-document-architecture/quickstart.md`

**Checkpoint**: Foundation complete and user stories may begin.

---

## Phase 3: User Story 1 - Document Current Architecture (Priority: P1) 🎯 MVP

**Goal**: Deliver authoritative architecture documentation for repository structure, pipeline semantics, dependency behavior, and runtime boundaries.

**Independent Test**: A reviewer can validate architecture behavior using only docs in `docs/architecture/` plus `_docs/framework-architecture.md`.

- [ ] T013 [US1] Finalize architecture baseline narrative in `docs/architecture/baseline-v0.1.md`
- [ ] T014 [P] [US1] Finalize architecture glossary definitions in `docs/architecture/glossary.md`
- [ ] T015 [P] [US1] Finalize non-goals boundaries in `docs/architecture/non-goals-v0.1.md`
- [x] T016 [US1] Document pipeline stage semantics in `docs/architecture/pipeline-semantics.md`
- [x] T017 [US1] Document dependency resolution behavior in `docs/architecture/dependency-resolution.md`
- [x] T018 [US1] Document active-domain session model in `docs/architecture/active-domain-model.md`
- [x] T019 [US1] Document orchestrator module boundaries in `docs/architecture/orchestrator-modules.md`
- [x] T020 [US1] Document runtime lifecycle transitions in `docs/architecture/runtime-lifecycle.md`
- [x] T021 [US1] Document runtime error taxonomy in `docs/architecture/error-model.md`
- [ ] T022 [US1] Align architecture narrative with roadmap in `_docs/framework-architecture.md` and `_docs/roadmap-architecture.md`

**Checkpoint**: User Story 1 is independently reviewable and demo-ready.

---

## Phase 4: User Story 2 - Preserve Compatibility (Priority: P2)

**Goal**: Preserve command and template compatibility while documenting explicit mappings and migration rules.

**Independent Test**: Existing command vocabulary and integration inventories remain valid while compatibility docs explain preserved/clarified/deferred behavior.

- [ ] T023 [US2] Finalize compatibility status matrix in `docs/architecture/compatibility-matrix.md`
- [x] T024 [US2] Define domain and object contract requirements in `docs/contracts/domain-contract.md` and `docs/contracts/object-contract.md`
- [x] T025 [P] [US2] Document ID/reference compatibility rules in `docs/contracts/id-and-reference-rules.md`
- [ ] T026 [P] [US2] Update command compatibility references in `README.md` and `docs/quickstart.md`
- [x] T027 [US2] Update integration inventory expectations for schema script in `tests/integrations/test_integration_base_markdown.py`
- [x] T028 [P] [US2] Update integration inventory expectations for schema script in `tests/integrations/test_integration_base_toml.py` and `tests/integrations/test_integration_base_skills.py`
- [ ] T029 [US2] Validate docs smoke workflow coverage in `.github/workflows/docs-smoke.yml`
- [x] T030 [US2] Run compatibility regression subset in `tests/integrations/`

**Checkpoint**: User Story 2 compatibility guarantees are verified.

---

## Phase 5: User Story 3 - Fork Scaffolding (Priority: P3)

**Goal**: Keep fork scaffolding complete and discoverable for contributors.

**Independent Test**: A new contributor can locate governance, architecture, contracts, and quickstart references directly from spec artifacts.

- [ ] T031 [US3] Finalize contract scope and acceptance checks in `specs/001-document-architecture/contracts/phase1-4-contract.md`
- [ ] T032 [P] [US3] Finalize research decision log in `specs/001-document-architecture/research.md`
- [ ] T033 [P] [US3] Finalize phase data model in `specs/001-document-architecture/data-model.md`
- [ ] T034 [US3] Finalize validation workflow and latest results in `specs/001-document-architecture/quickstart.md`
- [ ] T035 [US3] Update requirement checklist completion status in `specs/001-document-architecture/checklists/requirements.md`

**Checkpoint**: User Story 3 scaffolding is independently usable.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final quality gates across all stories.

- [x] T036 [P] Run markdown lint pass for architecture bundle in `_docs/` and `specs/001-document-architecture/`
- [ ] T037 [P] Run Python lint pass for touched runtime/support files in `src/` and `tests/`
- [x] T038 Re-run schema validation smoke checks using `scripts/bash/validate-schemas.sh`
- [ ] T039 Run full regression gate with `.venv/bin/python -m pytest tests/ -q`
- [ ] T040 Capture final validation summary in `specs/001-document-architecture/tasks.md` and `specs/001-document-architecture/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): no dependencies
- Foundational (Phase 2): depends on Phase 1 and blocks all user-story phases
- User Story phases (Phases 3-5): depend on Phase 2 completion
- Polish (Final Phase): depends on completion of selected user stories

### User Story Dependencies

- US1 (P1): can start immediately after Phase 2 and is the MVP scope
- US2 (P2): depends on US1 outputs for compatibility references and validation context
- US3 (P3): depends on foundational outputs and can run in parallel with late US2 tasks when files do not overlap

### Within Each User Story

- Define/refresh docs and contracts before running validation commands
- Validate target outputs before marking story complete
- Keep each story independently testable via its stated test criteria

---

## Parallel Opportunities

- Phase 1: T002, T003, T004
- Phase 2: T006, T007, T008
- US1: T014, T015
- US2: T025, T026, T028
- US3: T032, T033
- Polish: T036, T037

---

## Parallel Example: User Story 1

```text
Run in parallel:
- T014 update docs/architecture/glossary.md
- T015 update docs/architecture/non-goals-v0.1.md
```

## Parallel Example: User Story 2

```text
Run in parallel:
- T025 update docs/contracts/id-and-reference-rules.md
- T026 update README.md and docs/quickstart.md
- T028 update tests/integrations/test_integration_base_toml.py and tests/integrations/test_integration_base_skills.py
```

## Parallel Example: User Story 3

```text
Run in parallel:
- T032 update specs/001-document-architecture/research.md
- T033 update specs/001-document-architecture/data-model.md
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete US1 tasks (T013-T022).
3. Validate US1 independently via architecture document review.

### Incremental Delivery

1. Deliver US1 architecture package.
2. Deliver US2 compatibility package.
3. Deliver US3 scaffolding package.
4. Run final polish and regression gates.

### Parallel Team Strategy

1. Contributor A: US1 architecture docs (`docs/architecture/`).
2. Contributor B: US2 compatibility/docs/tests (`docs/contracts/`, `tests/integrations/`).
3. Contributor C: US3 feature artifacts (`specs/001-document-architecture/`).
