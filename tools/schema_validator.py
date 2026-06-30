#!/usr/bin/env python3
"""Simple schema validator CLI using PyYAML and jsonschema.

Usage:
  python tools/schema_validator.py validate --schema schemas/domain-manifest.schema.yaml schemas/examples/domain-manifest.example.yaml
  python tools/schema_validator.py validate --schema schemas/canonical-object.schema.yaml schemas/examples/canonical-object.example.yaml
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

try:
    import jsonschema
except Exception:
    jsonschema = None


def load_file(path: Path):
    txt = path.read_text(encoding="utf-8")
    if path.suffix in (".json",):
        return json.loads(txt)
    if yaml is not None:
        return yaml.safe_load(txt)
    # fallback: try json
    try:
        return json.loads(txt)
    except Exception:
        raise RuntimeError("Cannot parse YAML/JSON; install PyYAML")


def validate_instance(instance_path: Path, schema_path: Path) -> tuple[bool, str]:
    if jsonschema is None:
        return False, "jsonschema is not installed"
    try:
        schema = load_file(schema_path)
        instance = load_file(instance_path)
        resolver = jsonschema.RefResolver(base_uri=f"file://{schema_path.resolve()}", referrer=schema)
        jsonschema.validate(instance=instance, schema=schema, resolver=resolver)
        return True, "ok"
    except Exception as e:
        return False, str(e)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="schema-validator")
    sub = p.add_subparsers(dest="cmd")
    v = sub.add_parser("validate")
    v.add_argument("instances", nargs="+", help="Instance files to validate")
    v.add_argument("--schema", required=True, help="Schema file to validate against")

    args = p.parse_args(argv)
    if args.cmd != "validate":
        p.print_help()
        return 2

    schema_path = Path(args.schema)
    if not schema_path.exists():
        print(f"Schema not found: {schema_path}")
        return 2

    failed = 0
    for inst in args.instances:
        inst_path = Path(inst)
        if not inst_path.exists():
            print(f"MISSING: {inst_path}")
            failed += 1
            continue
        ok, msg = validate_instance(inst_path, schema_path)
        if ok:
            print(f"VALID: {inst_path}")
        else:
            print(f"INVALID: {inst_path} -> {msg}")
            failed += 1

    return 0 if failed == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
