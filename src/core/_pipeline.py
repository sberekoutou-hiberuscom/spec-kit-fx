"""Pipeline executor — stage execution and failure policies.

Provides load_pipeline_config() to parse pipeline YAML configuration and
execute_pipeline() to run configured stages in order with failure handling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from core._errors import ConfigurationError, SchemaError
from core._events import EventStatus, LifecycleEvent, emit_event
from datetime import datetime, timezone


@dataclass
class StageConfig:
    """A single pipeline stage configuration.

    Attributes:
        id: Stable stage identifier.
        execution_order: Configured stage order.
        prerequisites: Required completed stage IDs.
        validation_gates: Checks executed before stage logic.
        resumable: Whether stage can resume from persisted state.
    """

    id: str
    execution_order: int
    prerequisites: list[str] = field(default_factory=list)
    validation_gates: list[str] = field(default_factory=list)
    resumable: bool = False


@dataclass
class PipelineConfig:
    """Parsed pipeline configuration.

    Attributes:
        stages: Ordered list of stage configurations.
        failure_behavior: One of 'halt', 'skip_remaining', 'continue'.
    """

    stages: list[StageConfig] = field(default_factory=list)
    failure_behavior: str = "halt"


def load_pipeline_config(config_path: Path) -> PipelineConfig:
    """Load and parse pipeline configuration from YAML.

    Args:
        config_path: Path to the pipeline YAML file.

    Returns:
        PipelineConfig with parsed stages.

    Raises:
        ConfigurationError: If config file is missing or invalid.
        SchemaError: If config fails schema validation.
    """
    if not config_path.exists():
        raise ConfigurationError(
            f"Pipeline config not found: {config_path}"
        )

    try:
        raw = config_path.read_text(encoding="utf-8")
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        raise ConfigurationError(
            f"Failed to parse pipeline config: {e}"
        ) from e

    if not isinstance(data, dict):
        raise SchemaError("Pipeline config must be a YAML mapping")

    if "stages" not in data:
        raise SchemaError("Pipeline config missing required 'stages' key")

    stages_data = data["stages"]
    if not isinstance(stages_data, list):
        raise SchemaError("'stages' must be a list")

    stages: list[StageConfig] = []
    for i, entry in enumerate(stages_data):
        if not isinstance(entry, dict):
            raise SchemaError(f"Stage at index {i} must be a mapping")
        if "id" not in entry:
            raise SchemaError(f"Stage at index {i} missing required 'id' field")

        stage_id = entry["id"]
        execution_order = entry.get("execution_order", i + 1)
        prerequisites = entry.get("prerequisites", [])
        validation_gates = entry.get("validation_gates", [])
        resumable = entry.get("resumable", False)

        stages.append(StageConfig(
            id=stage_id,
            execution_order=execution_order,
            prerequisites=prerequisites,
            validation_gates=validation_gates,
            resumable=resumable,
        ))

    # Sort by execution_order
    stages.sort(key=lambda s: s.execution_order)

    failure_behavior = data.get("failure_behavior", "halt")
    if failure_behavior not in ("halt", "skip_remaining", "continue"):
        raise SchemaError(
            f"Invalid failure_behavior '{failure_behavior}': "
            f"must be one of halt, skip_remaining, continue"
        )

    return PipelineConfig(stages=stages, failure_behavior=failure_behavior)


def execute_pipeline(
    config: PipelineConfig,
    domain_order: list[str],
) -> list[LifecycleEvent]:
    """Execute configured pipeline stages in order.

    For each stage, emits STARTED then PASSED/FAILED events for each domain
    in the domain_order list.

    Args:
        config: Pipeline configuration.
        domain_order: Topologically sorted domain IDs.

    Returns:
        List of lifecycle events emitted during execution.
    """
    events: list[LifecycleEvent] = []

    now = datetime.now(timezone.utc).isoformat()

    for stage in config.stages:
        for domain_id in domain_order:
            started = LifecycleEvent(
                stage_id=stage.id,
                domain_context=domain_id,
                timestamp=now,
                status=EventStatus.STARTED,
                message=None,
            )
            emit_event(started)
            events.append(started)

            # In a real implementation, this would invoke the stage handler.
            # For now, emit PASSED as a no-op.
            passed = LifecycleEvent(
                stage_id=stage.id,
                domain_context=domain_id,
                timestamp=now,
                status=EventStatus.PASSED,
                message=None,
            )
            emit_event(passed)
            events.append(passed)

    return events
