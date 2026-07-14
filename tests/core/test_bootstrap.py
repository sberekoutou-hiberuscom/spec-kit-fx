"""Unit tests for core._bootstrap module."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from core._bootstrap import CoreConfig, load_config, locate_specs
from core._errors import ConfigurationError


class TestLoadConfig:
    """Tests for load_config()."""

    def test_valid_config(self) -> None:
        """load_config returns CoreConfig for a project with .specify/."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specify_dir = root / ".specify"
            specify_dir.mkdir()
            config_file = specify_dir / "config.yml"
            config_file.write_text("key: value\nnested:\n  sub: 42\n")

            config = load_config(root)

            assert isinstance(config, CoreConfig)
            assert config.project_root == root.resolve()
            assert config.specs_dir == root.resolve() / "specs"
            assert config.config_data == {"key": "value", "nested": {"sub": 42}}

    def test_missing_specify_dir(self) -> None:
        """load_config raises ConfigurationError when .specify/ is missing."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with pytest.raises(ConfigurationError, match="\\.specify"):
                load_config(root)

    def test_unparseable_config(self) -> None:
        """load_config raises ConfigurationError for invalid YAML."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specify_dir = root / ".specify"
            specify_dir.mkdir()
            config_file = specify_dir / "config.yml"
            config_file.write_text(": invalid yaml : [\n")

            with pytest.raises(ConfigurationError, match="parse|YAML|config"):
                load_config(root)

    def test_missing_config_file(self) -> None:
        """load_config raises ConfigurationError when config.yml is missing."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            specify_dir = root / ".specify"
            specify_dir.mkdir()
            # No config.yml created

            with pytest.raises(ConfigurationError, match="config"):
                load_config(root)


class TestLocateSpecs:
    """Tests for locate_specs()."""

    def test_specs_found(self) -> None:
        """locate_specs returns paths to specs/ directories."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs" / "001-foo").mkdir(parents=True)
            (root / "specs" / "002-bar").mkdir(parents=True)

            result = locate_specs(root)

            assert len(result) == 2
            assert all(p.is_dir() for p in result)
            assert all("specs" in str(p) for p in result)

    def test_empty_result(self) -> None:
        """locate_specs returns empty list when no specs/ directories exist."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = locate_specs(root)
            assert result == []

    def test_non_existent_path(self) -> None:
        """locate_specs returns empty list for non-existent path."""
        result = locate_specs(Path("/nonexistent/path"))
        assert result == []

    def test_specs_is_file_not_dir(self) -> None:
        """locate_specs handles case where specs/ is a file."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "specs").write_text("not a directory")
            result = locate_specs(root)
            assert result == []
