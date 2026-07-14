"""``specify domain`` command group — scaffold, validate, and run domains.

This module is the CLI/UX layer only (thin commands over services).
Each command resolves a domain, delegates to core services, and renders
Rich output.
"""
from __future__ import annotations

import typer

domain_app = typer.Typer(
    name="domain",
    help="Scaffold, validate, and run domains",
    add_completion=False,
)


def register(parent: typer.Typer) -> None:
    """Register the domain sub-app on a parent Typer app."""
    parent.add_typer(domain_app, name="domain")
