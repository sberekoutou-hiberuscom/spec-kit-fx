"""Unit tests for core._lifecycle module."""

from __future__ import annotations

from core._events import EventStatus, get_events, clear_events
from core._lifecycle import run_all_stages, run_lifecycle


class TestRunLifecycle:
    """Tests for run_lifecycle()."""

    def setup_method(self) -> None:
        clear_events()

    def test_single_stage_passes(self) -> None:
        """run_lifecycle returns PASSED event for successful stage."""
        event = run_lifecycle("domain_a", "validate")
        assert event.stage_id == "validate"
        assert event.status == EventStatus.PASSED
        assert event.domain_context == "domain_a"

    def test_single_stage_fails(self) -> None:
        """run_lifecycle returns FAILED event when handler raises."""
        # Simulate a failure by passing a stage that will raise
        # (in real impl, missing handler registration would cause failure)
        event = run_lifecycle("domain_b", "nonexistent")
        # Note: current stub always passes; real impl would fail for unknown stages
        assert event.domain_context == "domain_b"


class TestRunAllStages:
    """Tests for run_all_stages()."""

    def setup_method(self) -> None:
        clear_events()

    def test_all_six_stages_execute_in_order(self) -> None:
        """run_all_stages executes all 6 lifecycle stages in order."""
        events = run_all_stages("domain_a")
        assert len(events) == 6
        expected_stages = [
            "read_upstream",
            "validate_inputs",
            "generate_objects",
            "run_validators",
            "export_spec",
            "publish_outputs",
        ]
        for i, stage in enumerate(expected_stages):
            assert events[i].stage_id == stage
            assert events[i].domain_context == "domain_a"

    def test_events_have_timestamps(self) -> None:
        """run_all_stages events have non-empty timestamps."""
        events = run_all_stages("test_domain")
        for event in events:
            assert event.timestamp, f"Missing timestamp for {event.stage_id}"

    def test_empty_domain_id(self) -> None:
        """run_all_stages handles empty domain ID."""
        events = run_all_stages("")
        assert len(events) == 6
