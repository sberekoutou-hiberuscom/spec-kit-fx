"""Unit tests for core._manifest module."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
import yaml

from core._errors import ConfigurationError, SchemaError
from core._manifest import DomainManifest, discover_manifests, validate_manifest


def _make_manifest(dir_path: Path, data: dict) -> Path:
    """Write a domain.yaml file and return its path."""
    path = dir_path / "domain.yaml"
    path.write_text(yaml.safe_dump(data))
    return path


class TestDiscoverManifests:
    """Tests for discover_manifests()."""

    def test_manifests_found(self) -> None:
        """discover_manifests returns DomainManifest for each domain.yaml."""
        with tempfile.TemporaryDirectory() as tmp:
            d1 = Path(tmp) / "domain-a"
            d1.mkdir()
            _make_manifest(d1, {"id": "a", "name": "A", "version": "1.0.0"})

            d2 = Path(tmp) / "domain-b"
            d2.mkdir()
            _make_manifest(d2, {"id": "b", "name": "B", "version": "2.0.0"})

            result = discover_manifests([d1, d2])
            assert len(result) == 2
            ids = {m.id for m in result}
            assert ids == {"a", "b"}

    def test_empty_directory(self) -> None:
        """discover_manifests returns empty list for dirs with no domain.yaml."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "empty-domain"
            d.mkdir()
            result = discover_manifests([d])
            assert result == []

    def test_non_existent_path(self) -> None:
        """discover_manifests returns empty list for non-existent dirs."""
        result = discover_manifests([Path("/nonexistent")])
        assert result == []

    def test_invalid_yaml_skipped(self) -> None:
        """discover_manifests skips dirs with unparseable domain.yaml."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "bad-domain"
            d.mkdir()
            (d / "domain.yaml").write_text(": invalid: [\n")
            result = discover_manifests([d])
            assert result == []

    def test_mixed_results(self) -> None:
        """discover_manifests returns only valid manifests, skips bad ones."""
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good"
            good.mkdir()
            _make_manifest(good, {"id": "g", "name": "G", "version": "1.0.0"})

            bad = Path(tmp) / "bad"
            bad.mkdir()
            (bad / "domain.yaml").write_text(": invalid\n")

            result = discover_manifests([good, bad])
            assert len(result) == 1
            assert result[0].id == "g"


class TestValidateManifest:
    """Tests for validate_manifest()."""

    def _make_manifest(self, data: dict) -> DomainManifest:
        """Create a DomainManifest backed by a real temp file."""
        tmp = tempfile.mktemp(suffix=".yaml")
        Path(tmp).write_text(yaml.safe_dump(data))
        return DomainManifest(
            path=Path(tmp),
            id=data.get("id", ""),
            name=data.get("name", ""),
            version=data.get("version", ""),
            depends_on=data.get("depends_on", []),
            entrypoint=data.get("entrypoint"),
            exports=data.get("exports", []),
            validators=data.get("validators", []),
            adapters=data.get("adapters", []),
            capabilities=data.get("capabilities", []),
            schema_version=data.get("schema_version"),
        )

    def test_valid_manifest(self) -> None:
        """validate_manifest passes for a valid manifest."""
        manifest = self._make_manifest(
            {"id": "test-domain", "name": "Test Domain", "version": "1.2.3"}
        )
        validate_manifest(manifest)  # should not raise

    def test_valid_manifest_with_all_fields(self) -> None:
        """validate_manifest passes with all optional fields."""
        manifest = self._make_manifest(
            {
                "id": "test-domain",
                "name": "Test Domain",
                "version": "1.2.3",
                "depends_on": ["other-domain"],
                "entrypoint": "test.module",
                "exports": ["TypeA", "TypeB"],
                "validators": ["val1"],
                "adapters": ["adp1"],
                "capabilities": ["cap1"],
                "schema_version": "1.0",
            }
        )
        validate_manifest(manifest)

    def test_missing_id(self) -> None:
        """validate_manifest raises SchemaError when id is missing."""
        manifest = self._make_manifest({"id": "", "name": "Test", "version": "1.0.0"})
        with pytest.raises(SchemaError, match="id"):
            validate_manifest(manifest)

    def test_missing_name(self) -> None:
        """validate_manifest raises SchemaError when name is missing."""
        manifest = self._make_manifest({"id": "test", "name": "", "version": "1.0.0"})
        with pytest.raises(SchemaError, match="name"):
            validate_manifest(manifest)

    def test_missing_version(self) -> None:
        """validate_manifest raises SchemaError when version is missing."""
        manifest = self._make_manifest({"id": "test", "name": "Test", "version": ""})
        with pytest.raises(SchemaError, match="version"):
            validate_manifest(manifest)

    def test_invalid_id_pattern(self) -> None:
        """validate_manifest raises SchemaError for invalid id format."""
        manifest = self._make_manifest(
            {"id": "123-invalid-start", "name": "Test", "version": "1.0.0"}
        )
        with pytest.raises(SchemaError, match="id"):
            validate_manifest(manifest)

    def test_invalid_version_format(self) -> None:
        """validate_manifest raises SchemaError for non-semver version."""
        manifest = self._make_manifest(
            {"id": "test", "name": "Test", "version": "not-a-version"}
        )
        with pytest.raises(SchemaError, match="version"):
            validate_manifest(manifest)

    def test_self_referencing_dependency(self) -> None:
        """validate_manifest raises SchemaError for self-referencing depends_on."""
        manifest = self._make_manifest(
            {
                "id": "test",
                "name": "Test",
                "version": "1.0.0",
                "depends_on": ["test"],
            }
        )
        with pytest.raises(SchemaError, match="self-referenc|depends_on"):
            validate_manifest(manifest)

    def test_non_existent_path(self) -> None:
        """validate_manifest raises ConfigurationError for non-existent path."""
        manifest = DomainManifest(
            path=Path("/nonexistent/manifest.yaml"),
            id="test",
            name="Test",
            version="1.0.0",
        )
        with pytest.raises(ConfigurationError, match="path|exist"):
            validate_manifest(manifest)

    def test_validators_non_empty_strings(self) -> None:
        """validate_manifest passes when validators entries are non-empty strings."""
        manifest = self._make_manifest(
            {
                "id": "test",
                "name": "Test",
                "version": "1.0.0",
                "validators": ["my_domain.validators.size_check"],
            }
        )
        validate_manifest(manifest)  # should not raise

    def test_validators_empty_string(self) -> None:
        """validate_manifest raises SchemaError when a validators entry is empty."""
        manifest = self._make_manifest(
            {
                "id": "test",
                "name": "Test",
                "version": "1.0.0",
                "validators": [""],
            }
        )
        with pytest.raises(SchemaError, match="validators"):
            validate_manifest(manifest)

    def test_exports_non_empty_strings(self) -> None:
        """validate_manifest passes when exports entries are non-empty strings."""
        manifest = self._make_manifest(
            {
                "id": "test",
                "name": "Test",
                "version": "1.0.0",
                "exports": ["TypeA", "TypeB"],
            }
        )
        validate_manifest(manifest)  # should not raise

    def test_exports_empty_string(self) -> None:
        """validate_manifest raises SchemaError when an exports entry is empty."""
        manifest = self._make_manifest(
            {
                "id": "test",
                "name": "Test",
                "version": "1.0.0",
                "exports": ["valid_type", ""],
            }
        )
        with pytest.raises(SchemaError, match="exports"):
            validate_manifest(manifest)
