CI Policy (Conditional)

This repository uses a conditional CI policy (Option D) for performance and developer convenience.

Policy summary

- Documentation-only changes (paths under `_docs/`, `docs/`, `specs/`, or `.specify/`) trigger a lightweight smoke CI that runs:
  - `ruff` (Python linter) — quick static checks
  - `markdownlint` — Markdown quality checks
  - Template-resolution smoke (scripts/bash/setup-plan.sh and scripts/bash/check-prerequisites.sh)

- Changes that modify templates, CLI command code, or runtime files run the full CI matrix (pytest across supported platforms and versions, full linters, security checks).

Why

- Avoids expensive matrix runs for small documentation edits.
- Ensures documentation changes still pass fast validations and do not introduce template regressions.

How PR authors should indicate intent

- If your PR only touches documentation paths, no extra action is required — the docs-smoke workflow will run automatically.
- If your PR touches templates or CLI/runtime code, the repository's full CI will run automatically. Ensure tests and linters pass locally before pushing.

Local reproduction

Run the smoke checks locally with these commands:

```
python -m pip install --upgrade ruff
ruff check src/ || true

npm install -g markdownlint-cli@0.30.0
markdownlint _docs specs || true

bash scripts/bash/setup-plan.sh --json
bash scripts/bash/check-prerequisites.sh --json --paths-only
```

If you need the full CI locally, run the repository's test suite and linters:

```
ruff check src/
pytest -q
markdownlint _docs
```
