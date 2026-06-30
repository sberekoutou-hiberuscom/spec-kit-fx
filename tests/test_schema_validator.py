from pathlib import Path
from tools import schema_validator


def test_validate_domain_manifest_example(tmp_path):
    schema = Path("schemas/domain-manifest.schema.yaml")
    inst = Path("schemas/examples/domain-manifest.example.yaml")
    ok, msg = schema_validator.validate_instance(inst, schema)
    assert ok, msg


def test_validate_canonical_object_example(tmp_path):
    schema = Path("schemas/canonical-object.schema.yaml")
    inst = Path("schemas/examples/canonical-object.example.yaml")
    ok, msg = schema_validator.validate_instance(inst, schema)
    assert ok, msg
