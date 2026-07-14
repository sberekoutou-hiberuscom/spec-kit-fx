"""Unit tests for the ValidationResult dataclass."""

from __future__ import annotations

from core._validation_result import ValidationResult


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_minimal_creation(self) -> None:
        """Creating a ValidationResult with only required fields works."""
        result = ValidationResult(object_id="test.object", message="Something went wrong")
        assert result.object_id == "test.object"
        assert result.severity == "error"
        assert result.message == "Something went wrong"
        assert result.fix_hint is None

    def test_with_all_fields(self) -> None:
        """Creating a ValidationResult with all fields works."""
        result = ValidationResult(
            object_id="test.object",
            severity="warning",
            message="Check this value",
            fix_hint="Set the value to a positive integer",
        )
        assert result.object_id == "test.object"
        assert result.severity == "warning"
        assert result.message == "Check this value"
        assert result.fix_hint == "Set the value to a positive integer"

    def test_info_severity(self) -> None:
        """Severity can be set to 'info'."""
        result = ValidationResult(
            object_id="test.object",
            severity="info",
            message="Informational message",
        )
        assert result.severity == "info"

    def test_error_severity_default(self) -> None:
        """Default severity is 'error'."""
        result = ValidationResult(object_id="test.object", message="Error message")
        assert result.severity == "error"

    def test_fix_hint_optional(self) -> None:
        """fix_hint can be None or a string."""
        no_hint = ValidationResult(object_id="test.object", message="No hint")
        assert no_hint.fix_hint is None

        with_hint = ValidationResult(
            object_id="test.object",
            message="With hint",
            fix_hint="Try this fix",
        )
        assert with_hint.fix_hint == "Try this fix"

    def test_dataclass_equality(self) -> None:
        """Two ValidationResults with same fields are equal."""
        a = ValidationResult(object_id="obj", severity="error", message="msg")
        b = ValidationResult(object_id="obj", severity="error", message="msg")
        assert a == b

    def test_dataclass_inequality(self) -> None:
        """Two ValidationResults with different fields are not equal."""
        a = ValidationResult(object_id="obj", severity="error", message="msg")
        b = ValidationResult(object_id="obj", severity="warning", message="msg")
        assert a != b

    def test_repr(self) -> None:
        """ValidationResult has a useful repr."""
        result = ValidationResult(object_id="obj", severity="error", message="msg")
        r = repr(result)
        assert "ValidationResult" in r
        assert "object_id=" in r
        assert "severity=" in r
