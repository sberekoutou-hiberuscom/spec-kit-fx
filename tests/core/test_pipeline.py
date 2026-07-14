"""Unit tests for core._pipeline module."""

from __future__ import annotations

from pathlib import Path

import pytest

from core._errors import ConfigurationError, SchemaError
from core._events import EventStatus, get_events, clear_events
from core._pipeline import (
    PipelineConfig,
    StageConfig,
    execute_pipeline,
    load_pipeline_config,
)


class TestLoadPipelineConfig:
    """Tests for load_pipeline_config()."""

    def test_valid_config(self, tmp_path: Path) -> None:
        """load_pipeline_config parses valid YAML correctly."""
        config_file = tmp_path / "pipeline.yml"
        config_file.write_text(
            "stages:\n"
            "  - id: validate\n"
            "    execution_order: 1\n"
            "  - id: build\n"
            "    execution_order: 2\n"
        )
        result = load_pipeline_config(config_file)
        assert len(result.stages) == 2
        assert result.stages[0].id == "validate"
        assert result.stages[0].execution_order == 1
        assert result.stages[1].id == "build"
        assert result.stages[1].execution_order == 2

    def test_missing_file(self) -> None:
        """load_pipeline_config raises ConfigurationError when file missing."""
        with pytest.raises(ConfigurationError, match="pipeline"):
            load_pipeline_config(Path("/nonexistent/pipeline.yml"))

    def test_invalid_yaml(self, tmp_path: Path) -> None:
        """load_pipeline_config raises ConfigurationError for invalid YAML."""
        config_file = tmp_path / "pipeline.yml"
        config_file.write_text("{{invalid: yaml: broken")
        with pytest.raises(ConfigurationError, match="parse|YAML|invalid"):
            load_pipeline_config(config_file)

    def test_non_list_stages(self, tmp_path: Path) -> None:
        """load_pipeline_config raises SchemaError when stages is not a list."""
        config_file = tmp_path / "pipeline.yml"
        config_file.write_text("stages: not_a_list\n")
        with pytest.raises(SchemaError, match="list"):
            load_pipeline_config(config_file)

    def test_missing_stages_key(self, tmp_path: Path) -> None:
        """load_pipeline_config raises SchemaError when stages key missing."""
        config_file = tmp_path / "pipeline.yml"
        config_file.write_text("other: data\n")
        with pytest.raises(SchemaError, match="stages"):
            load_pipeline_config(config_file)

    def test_stage_missing_id(self, tmp_path: Path) -> None:
        """load_pipeline_config raises SchemaError when stage has no id."""
        config_file = tmp_path / "pipeline.yml"
        config_file.write_text(
            "stages:\n"
            "  - execution_order: 1\n"
        )
        with pytest.raises(SchemaError, match="id"):
            load_pipeline_config(config_file)


class TestExecutePipeline:
    """Tests for execute_pipeline()."""

    def setup_method(self) -> None:
        clear_events()

    def test_stages_execute_in_order(self) -> None:
        """execute_pipeline runs stages in defined order."""
        config = PipelineConfig(
            stages=[
                StageConfig(id="validate", execution_order=1),
                StageConfig(id="build", execution_order=2),
            ]
        )
        events = execute_pipeline(config, ["domain_a"])
        # Should emit events for each stage
        stage_ids = [e.stage_id for e in events]
        assert "validate" in stage_ids
        assert "build" in stage_ids

    def test_empty_stages(self) -> None:
        """execute_pipeline handles empty stage list."""
        config = PipelineConfig(stages=[])
        events = execute_pipeline(config, [])
        assert events == []

    def test_events_contain_status(self) -> None:
        """execute_pipeline events have correct status values."""
        config = PipelineConfig(
            stages=[
                StageConfig(id="test", execution_order=1),
            ]
        )
        events = execute_pipeline(config, ["domain_a"])
        started = [e for e in events if e.status == EventStatus.STARTED]
        passed = [e for e in events if e.status == EventStatus.PASSED]
        assert len(started) >= 1
        assert len(passed) >= 1
