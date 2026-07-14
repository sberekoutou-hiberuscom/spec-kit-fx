"""Structured lifecycle events for the core runtime.

Provides the LifecycleEvent dataclass, EventStatus enum, and emit_event
function used by pipeline execution and lifecycle runners to record
structured runtime events.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EventStatus(Enum):
    """Status of a lifecycle stage execution."""

    STARTED = "started"
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class LifecycleEvent:
    """A structured event emitted during lifecycle transitions.

    Attributes:
        stage_id: Lifecycle stage identifier.
        domain_context: Domain ID if applicable, or None for pipeline-level events.
        timestamp: ISO 8601 timestamp string.
        status: One of STARTED, PASSED, FAILED.
        message: Human-readable detail (may be None for STARTED events).
    """

    stage_id: str
    domain_context: str | None
    timestamp: str  # ISO 8601
    status: EventStatus
    message: str | None


_events: list[LifecycleEvent] = []


def emit_event(event: LifecycleEvent) -> None:
    """Record a lifecycle event for diagnostics and debugging.

    Args:
        event: The LifecycleEvent to record.
    """
    _events.append(event)


def get_events() -> list[LifecycleEvent]:
    """Return all recorded lifecycle events.

    Returns:
        A copy of the internal event list.
    """
    return list(_events)


def clear_events() -> None:
    """Clear all recorded lifecycle events.

    Useful for resetting state between test runs.
    """
    _events.clear()
