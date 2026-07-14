"""Unit tests for the plugin loader module."""

from __future__ import annotations

import sys
from types import ModuleType

import pytest

from core._plugin_loader import _run_exporters, _run_validators, load_plugin


class TestLoadPlugin:
    """Tests for load_plugin()."""

    def test_load_stdlib_module(self) -> None:
        """Loading a stdlib module returns the module."""
        mod = load_plugin("json")
        assert isinstance(mod, ModuleType)
        assert hasattr(mod, "dumps")

    def test_load_core_module(self) -> None:
        """Loading a core module returns the module."""
        mod = load_plugin("core._manifest")
        assert isinstance(mod, ModuleType)
        assert hasattr(mod, "DomainManifest")

    def test_load_nonexistent_module_raises(self) -> None:
        """Loading a non-existent module raises ModuleNotFoundError."""
        with pytest.raises(ModuleNotFoundError):
            load_plugin("nonexistent.module.that.does.not.exist")

    def test_load_module_with_import_error(self) -> None:
        """Loading a module that raises ImportError propagates it."""
        # Create a synthetic module that fails on import
        bad_name = "_test_bad_import_module"
        if bad_name in sys.modules:
            del sys.modules[bad_name]

        # We can't easily create a module that raises ImportError on import
        # without a real file, so test that a broken dotted path raises
        with pytest.raises((ModuleNotFoundError, ImportError)):
            load_plugin("core._nonexistent_sub_module_xyz")


class TestRunValidators:
    """Tests for _run_validators()."""

    def test_empty_validators_list(self) -> None:
        """An empty validators list returns an empty result list."""
        results = _run_validators([], {})
        assert results == []

    def test_missing_validator_module(self) -> None:
        """A missing validator module returns an error result."""
        results = _run_validators(["nonexistent.validator"], {})
        assert len(results) == 1
        assert results[0]["severity"] == "error"
        assert "nonexistent.validator" in str(results[0]["object_id"])

    def test_validator_without_run_function(self) -> None:
        """A validator module without a 'run' function returns an error."""
        results = _run_validators(["json"], {})
        assert len(results) == 1
        assert results[0]["severity"] == "error"
        assert "no 'run' function" in str(results[0]["message"])


class TestRunExporters:
    """Tests for _run_exporters()."""

    def test_empty_exports_list(self, tmp_path) -> None:
        """An empty exports list returns an empty output list."""
        outputs = _run_exporters([], {}, tmp_path)
        assert outputs == []

    def test_missing_exporter_module(self) -> None:
        """A missing exporter module is silently skipped."""
        outputs = _run_exporters(["nonexistent.exporter"], {}, None)  # type: ignore[arg-type]
        assert outputs == []

    def test_exporter_without_run_function(self) -> None:
        """An exporter module without a 'run' function is silently skipped."""
        outputs = _run_exporters(["json"], {}, None)  # type: ignore[arg-type]
        assert outputs == []
