# Quickstart Guide: Pipeline Semantics & Dependency Resolution

## Overview

This guide provides a quick way to validate the Phase 3 artifacts for pipeline semantics and dependency resolution.

## Prerequisites

- Python 3.11+
- `PyYAML` and `jsonschema` installed
- `networkx` installed (for graph operations)

## Validation Steps

### 1. Schema Validation

Validate the pipeline schema against the example:

```bash
python3 tools/schema_validator.py validate \
  --instance schemas/examples/pipeline-example.yaml \
  --schema schemas/pipeline.schema.yaml
```

Expected output: `VALID`

### 2. Pipeline State Schema Validation

```bash
python3 tools/schema_validator.py validate \
  --instance schemas/examples/pipeline-state-example.yaml \
  --schema schemas/pipeline-state.schema.yaml
```

Expected output: `VALID`

### 3. Dependency Graph Tests

Run unit tests for the dependency resolver:

```bash
.venv/bin/python -m pytest tests/test_dependency_graph.py -v
.venv/bin/python -m pytest tests/test_dependency_resolver.py -v
```

Expected: All tests pass.

### 4. Pipeline Configuration Tests

```bash
.venv/bin/python -m pytest tests/test_pipeline_config.py -v
```

Expected: All tests pass.

### 5. Active Domain Tests

```bash
.venv/bin/python -m pytest tests/test_active_domain.py -v
```

Expected: All tests pass.

## Expected Outcomes

| Test Category | Expected Result |
|--------------|-----------------|
| Schema validation | All examples validate against schemas |
| Dependency resolution | Topological sort is deterministic |
| Cycle detection | All cycle cases detected and reported |
| Pipeline execution | Stages execute in correct order |
| Resumability | Failed pipelines restart from last failed stage |
| Active domain | Commands scope to active domain correctly |

## Lint Checks

Run linters before committing:

```bash
ruff check src/core/pipeline/ src/core/dependency/ src/core/domain/
markdownlint specs/003-pipeline-semantics/
```

## CI Integration

The pipeline schema validation is integrated into the `docs-smoke` GitHub Actions workflow. PRs that modify `schemas/pipeline.schema.yaml` or `schemas/pipeline-state.schema.yaml` will trigger schema validation checks.
