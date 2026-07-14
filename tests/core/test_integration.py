"""End-to-end integration tests for core runtime.

Tests the full pipeline: bootstrap → manifest discovery → dependency
resolution → pipeline execution.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from core._bootstrap import CoreConfig, load_config, locate_specs
from core._events import clear_events
from core._manifest import discover_manifests, validate_manifest
from core._pipeline import (
    PipelineConfig,
    StageConfig,
    execute_pipeline,
    load_pipeline_config,
)
from core._resolver import build_graph, resolve_order


class TestBootstrapToPipeline:
    """End-to-end integration test."""

    def test_full_pipeline(self, tmp_path: Path) -> None:
        """bootstrap → manifest → resolver → pipeline runs end-to-end."""
        clear_events()

        # --- Bootstrap ---
        # Create .specify/config.yml
        specify_dir = tmp_path / ".specify"
        specify_dir.mkdir()
        config_file = specify_dir / "config.yml"
        config_file.write_text("project: test\nversion: 1.0.0\n")

        config = load_config(tmp_path)
        assert isinstance(config, CoreConfig)
        assert config.project_root.resolve() == tmp_path.resolve()

        # --- Manifest discovery ---
        # Create a domain directory with a valid manifest
        domains_dir = tmp_path / "domains"
        domains_dir.mkdir()
        core_dir = domains_dir / "core"
        core_dir.mkdir()
        core_manifest = core_dir / "domain.yaml"
        core_manifest.write_text(
            "id: core\n"
            "name: Core Domain\n"
            "version: 1.0.0\n"
        )

        manifests = discover_manifests([core_dir])
        assert len(manifests) == 1
        assert manifests[0].id == "core"

        # Validate
        validate_manifest(manifests[0])  # should not raise

        # --- Dependency resolution ---
        graph = build_graph(manifests)
        order = resolve_order(graph)
        assert order == ["core"]

        # --- Pipeline execution ---
        pipeline_file = specify_dir / "pipeline.yml"
        pipeline_file.write_text(
            "stages:\n"
            "  - id: validate\n"
            "    execution_order: 1\n"
            "  - id: build\n"
            "    execution_order: 2\n"
        )
        pipeline_config = load_pipeline_config(pipeline_file)
        assert len(pipeline_config.stages) == 2

        events = execute_pipeline(pipeline_config, order)
        assert len(events) == 4  # 2 stages × 2 events (STARTED + PASSED) × 1 domain

    def test_with_dependencies(self, tmp_path: Path) -> None:
        """Integration with dependent domains."""
        clear_events()

        # Create manifests for two domains with a dependency
        domains_dir = tmp_path / "domains"
        domains_dir.mkdir()

        core_dir = domains_dir / "core"
        core_dir.mkdir()
        (core_dir / "domain.yaml").write_text(
            "id: core\nname: Core\nversion: 1.0.0\n"
        )

        plugin_dir = domains_dir / "plugin"
        plugin_dir.mkdir()
        (plugin_dir / "domain.yaml").write_text(
            "id: plugin\nname: Plugin\nversion: 1.0.0\n"
            "depends_on:\n  - core\n"
        )

        manifests = discover_manifests([core_dir, plugin_dir])
        assert len(manifests) == 2

        for m in manifests:
            validate_manifest(m)

        graph = build_graph(manifests)
        order = resolve_order(graph)
        assert order == ["core", "plugin"]

    def test_missing_config_fails_gracefully(self, tmp_path: Path) -> None:
        """Bootstrap raises error for missing config."""
        from core._errors import ConfigurationError

        with pytest.raises(ConfigurationError):
            load_config(tmp_path / "nonexistent")
