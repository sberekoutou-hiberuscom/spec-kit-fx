"""Lifecycle runner — domain lifecycle transitions.

Provides run_lifecycle() to execute a single lifecycle stage and
run_all_stages() to execute all six lifecycle stages for a domain.
"""

from __future__ import annotations

from datetime import datetime, timezone

from core._events import EventStatus, LifecycleEvent, emit_event

# Ordered lifecycle stages
LIFECYCLE_STAGES = [
    "read_upstream",
    "validate_inputs",
    "generate_objects",
    "run_validators",
    "export_spec",
    "publish_outputs",
]


def run_lifecycle(domain_id: str, stage: str) -> LifecycleEvent:
    """Execute a single lifecycle stage for a domain.

    Args:
        domain_id: The domain to execute.
        stage: The lifecycle stage name.

    Returns:
        LifecycleEvent with status and timestamp.
    """
    now = datetime.now(timezone.utc).isoformat()

    started = LifecycleEvent(
        stage_id=stage,
        domain_context=domain_id,
        timestamp=now,
        status=EventStatus.STARTED,
        message=None,
    )
    emit_event(started)

    try:
        # In a real implementation, this would dispatch to a registered handler.
        # For now, all stages pass by default.
        passed = LifecycleEvent(
            stage_id=stage,
            domain_context=domain_id,
            timestamp=now,
            status=EventStatus.PASSED,
            message=None,
        )
        emit_event(passed)
        return passed
    except Exception as exc:
        failed = LifecycleEvent(
            stage_id=stage,
            domain_context=domain_id,
            timestamp=now,
            status=EventStatus.FAILED,
            message=str(exc),
        )
        emit_event(failed)
        return failed


def run_all_stages(domain_id: str) -> list[LifecycleEvent]:
    """Execute all lifecycle stages for a domain in order.

    Stages: Read Upstream → Validate Inputs → Generate Domain Objects →
            Run Validators → Export Specification → Publish Outputs

    Args:
        domain_id: The domain to execute.

    Returns:
        List of LifecycleEvent for each stage.
    """
    events: list[LifecycleEvent] = []
    for stage in LIFECYCLE_STAGES:
        event = run_lifecycle(domain_id, stage)
        events.append(event)
        if event.status == EventStatus.FAILED:
            break
    return events
