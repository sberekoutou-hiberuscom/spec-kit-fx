---
description: "Tasks for Document Architecture feature (001-document-architecture)"
---

# Tasks: Document Architecture (001-document-architecture)

**Input**: Design documents from `specs/001-document-architecture/`

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Confirm active feature registration in `.specify/feature.json`
- [x] T002 [P] Verify Phase 1 baseline docs exist in `docs/architecture/baseline-v0.1.md`
- [x] T003 [P] Verify compatibility matrix exists in `docs/architecture/compatibility-matrix.md`
- [x] T004 [P] Verify glossary and non-goals docs in `docs/architecture/glossary.md` and `docs/architecture/non-goals-v0.1.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T005 [P] Validate constitution gate alignment against `.specify/memory/constitution.md`
- [x] T006 [P] Validate schema artifacts exist in `schemas/domain-manifest.schema.yaml` and `schemas/canonical-object.schema.yaml`
- [x] T007 [P] Validate schema examples in `schemas/examples/domain-manifest.example.yaml` and `schemas/examples/canonical-object.example.yaml`
- [x] T008 Run schema smoke script `scripts/bash/validate-schemas.sh`
- [x] T009 Run lint checks (`ruff`, `markdownlint`) and record results in `specs/001-document-architecture/quickstart.md`
- [x] T010 Validate template/path smoke checks via `scripts/bash/setup-plan.sh` and `scripts/bash/check-prerequisites.sh`
- [ ] T035 Run pytest regression checks for affected scope (`python3 -m pytest tests/ -q`) and require a passing result before PR readiness

**Checkpoint**: Foundation ready - user story work can proceed.

---

## Phase 3: User Story 1 - Document Current Architecture (Priority: P1) 🎯 MVP

**Goal**: Deliver authoritative architecture documentation with phase 1-4 boundaries and deterministic pipeline semantics.

**Independent Test**: Verify architecture docs describe pipeline, domains, repository layout, dependency semantics, and orchestration boundaries without needing code changes.

- [ ] T011 [US1] Finalize architecture narrative in `_docs/framework-architecture.md`
- [ ] T012 [P] [US1] Finalize combined phases plan in `specs/001-document-architecture/plan.md`
- [ ] T013 [P] [US1] Finalize research decisions in `specs/001-document-architecture/research.md`
- [ ] T014 [P] [US1] Finalize phase 1-4 data model in `specs/001-document-architecture/data-model.md`
- [ ] T015 [US1] Add pipeline semantics design doc at `docs/architecture/pipeline-semantics.md`
- [ ] T016 [US1] Add dependency resolution design doc at `docs/architecture/dependency-resolution.md`
- [ ] T017 [US1] Add active domain model doc at `docs/architecture/active-domain-model.md`
- [ ] T018 [US1] Add orchestrator module boundaries doc at `docs/architecture/orchestrator-modules.md`
- [ ] T019 [US1] Add runtime lifecycle doc at `docs/architecture/runtime-lifecycle.md`
- [ ] T020 [US1] Add error model doc at `docs/architecture/error-model.md`

**Checkpoint**: User Story 1 independently reviewable and testable via docs.

---

## Phase 4: User Story 2 - Preserve Compatibility (Priority: P2)

**Goal**: Preserve command/template compatibility while documenting migration and CI policy for safe evolution.

**Independent Test**: Confirm legacy command vocabulary still maps correctly and smoke checks detect regressions.

- [ ] T021 [US2] Verify core command naming consistency in `src/specify_cli/integrations/` and `templates/commands/`
- [ ] T022 [P] [US2] Add compatibility mapping notes to `docs/architecture/compatibility-matrix.md`
- [ ] T023 [US2] Add migration guidance at `docs/migration.md`
- [ ] T024 [US2] Document command contracts in `docs/commands/command-contracts.md`
- [ ] T025 [P] [US2] Document command compatibility mapping in `docs/commands/compatibility-mapping.md`
- [ ] T026 [P] [US2] Add command examples in `docs/commands/examples.md`
- [ ] T027 [US2] Confirm docs-smoke workflow coverage in `.github/workflows/docs-smoke.yml`

**Checkpoint**: User Story 2 compatibility checks and docs complete.

---

## Phase 5: User Story 3 - Fork Scaffolding (Priority: P3)

**Goal**: Keep fork scaffolding complete and discoverable for new contributors.

**Independent Test**: New contributor can locate constitution, spec, contract, and quickstart files and run smoke validation.

- [ ] T028 [US3] Finalize quickstart validation steps in `specs/001-document-architecture/quickstart.md`
- [ ] T029 [P] [US3] Finalize contracts index in `specs/001-document-architecture/contracts/README.md`
- [ ] T030 [P] [US3] Finalize phase contract in `specs/001-document-architecture/contracts/phase1-4-contract.md`
- [ ] T031 [US3] Update checklist progress in `specs/001-document-architecture/checklists/requirements.md`

**Checkpoint**: User Story 3 scaffolding complete.

---

## Phase N: Polish & Cross-Cutting Concerns

- [ ] T032 [P] Ensure markdown consistency across `_docs/` and `specs/001-document-architecture/`
- [ ] T033 [P] Re-run full local validation bundle from `specs/001-document-architecture/quickstart.md`
- [ ] T034 Prepare PR summary with phase 1-4 outcomes in `specs/001-document-architecture/tasks.md`
- [ ] T036 Execute integration/regression verification run and capture evidence (command output summary + pass/fail) in PR summary/checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) -> Foundational (Phase 2) -> User Stories (Phases 3-5) -> Polish
- No user story work should start before foundational checks (T005-T010) pass.

### User Story Dependencies

- User Story 1 (P1): starts after foundational completion; no dependency on US2/US3
- User Story 2 (P2): starts after foundational completion; depends on US1 artifacts for compatibility references
- User Story 3 (P3): starts after foundational completion; may run in parallel with US2 where files do not overlap

### Parallel Opportunities

- Phase 1: T002, T003, T004
- Phase 2: T005, T006, T007
- US1: T012, T013, T014
- US2: T022, T025, T026
- US3: T029, T030
- Polish: T032, T033

---

## Parallel Example: User Story 1

```text
Run in parallel:
- T012 update specs/001-document-architecture/plan.md
- T013 update specs/001-document-architecture/research.md
- T014 update specs/001-document-architecture/data-model.md
```

## Parallel Example: User Story 2

```text
Run in parallel:
- T022 update docs/architecture/compatibility-matrix.md
- T025 create docs/commands/compatibility-mapping.md
- T026 create docs/commands/examples.md
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2
2. Complete User Story 1 tasks (T011-T020)
3. Validate User Story 1 deliverables independently

### Incremental Delivery

1. Deliver User Story 1 docs package
2. Deliver User Story 2 compatibility package
3. Deliver User Story 3 scaffolding package
4. Run final polish and validation

### Parallel Team Strategy

1. Contributor A: User Story 1 architecture documentation outputs
2. Contributor B: User Story 2 compatibility and command documentation
3. Contributor C: User Story 3 scaffolding and checklist updates
