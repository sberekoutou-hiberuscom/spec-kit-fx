#!/usr/bin/env bash
set -euo pipefail

# Validate example schema instances using the repository validator
PYTHON=${PYTHON:-python3}

echo "Installing validator dependencies..."
$PYTHON -m pip install --user --upgrade PyYAML jsonschema >/dev/null

echo "Validating domain manifest example..."
$PYTHON tools/schema_validator.py validate --schema schemas/domain-manifest.schema.yaml schemas/examples/domain-manifest.example.yaml

echo "Validating canonical object example..."
$PYTHON tools/schema_validator.py validate --schema schemas/canonical-object.schema.yaml schemas/examples/canonical-object.example.yaml

echo "All schema examples validated successfully."
