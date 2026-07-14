"""Validation result dataclass for domain validation.

Provides a structured representation of a single validation check,
including severity, message, and optional fix hint.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Severity = Literal["error", "warning", "info"]


@dataclass
class ValidationResult:
    """Result of a single validation check on a domain object.

    Attributes:
        object_id: Identifier of the object that was validated.
        severity: Severity level — ``"error"``, ``"warning"``, or ``"info"``.
        message: Human-readable description of the validation outcome.
        fix_hint: Optional suggestion for how to fix the issue.
    """

    object_id: str
    severity: Severity = "error"
    message: str = ""
    fix_hint: str | None = None
