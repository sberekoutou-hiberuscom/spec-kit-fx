"""Unit tests for core._errors module.

Tests the error class hierarchy, string representations, and chaining.
"""

from __future__ import annotations

import pytest

from core._errors import (
    AdapterSyncError,
    ConfigurationError,
    CoreError,
    DependencyError,
    SchemaError,
    ValidationError,
)


class TestCoreError:
    """Tests for CoreError base class."""

    def test_is_exception_subclass(self) -> None:
        """CoreError inherits from Exception."""
        assert issubclass(CoreError, Exception)

    def test_default_message(self) -> None:
        """CoreError has a default message."""
        err = CoreError()
        assert str(err) == ""

    def test_custom_message(self) -> None:
        """CoreError accepts a custom message."""
        err = CoreError("Something went wrong")
        assert str(err) == "Something went wrong"

    def test_repr(self) -> None:
        """CoreError repr includes class name and message."""
        err = CoreError("test error")
        assert "CoreError" in repr(err)
        assert "test error" in repr(err)


class TestErrorHierarchy:
    """Tests for error subclass hierarchy."""

    def test_configuration_error_is_core_error(self) -> None:
        """ConfigurationError is a CoreError."""
        assert issubclass(ConfigurationError, CoreError)

    def test_schema_error_is_core_error(self) -> None:
        """SchemaError is a CoreError."""
        assert issubclass(SchemaError, CoreError)

    def test_dependency_error_is_core_error(self) -> None:
        """DependencyError is a CoreError."""
        assert issubclass(DependencyError, CoreError)

    def test_validation_error_is_core_error(self) -> None:
        """ValidationError is a CoreError."""
        assert issubclass(ValidationError, CoreError)

    def test_adapter_sync_error_is_core_error(self) -> None:
        """AdapterSyncError is a CoreError."""
        assert issubclass(AdapterSyncError, CoreError)

    def test_all_subclasses_distinct(self) -> None:
        """All error subclasses are distinct types."""
        errors = [
            ConfigurationError,
            SchemaError,
            DependencyError,
            ValidationError,
            AdapterSyncError,
        ]
        assert len({e.__name__ for e in errors}) == 5


class TestErrorChaining:
    """Tests for error chaining."""

    def test_chaining_with_cause(self) -> None:
        """CoreError supports __cause__ chaining."""
        try:
            raise ValueError("original cause")
        except ValueError as cause:
            err = ConfigurationError("wrapped error")
            err.__cause__ = cause

        assert isinstance(err.__cause__, ValueError)
        assert str(err.__cause__) == "original cause"

    def test_raise_and_catch_as_core_error(self) -> None:
        """Specific errors can be caught as CoreError."""
        with pytest.raises(CoreError) as exc_info:
            raise ConfigurationError("test config error")
        assert isinstance(exc_info.value, ConfigurationError)
        assert str(exc_info.value) == "test config error"

    def test_error_message_in_all_types(self) -> None:
        """All error types accept and display messages."""
        for error_class in [
            ConfigurationError,
            SchemaError,
            DependencyError,
            ValidationError,
            AdapterSyncError,
        ]:
            msg = f"{error_class.__name__} message"
            err = error_class(msg)
            assert str(err) == msg
