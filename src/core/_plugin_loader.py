"""Plugin loader — dynamic module loading for validators and exporters.

Uses ``importlib.import_module()`` (stdlib) to load user-provided Python
modules at runtime. No third-party dependencies.
"""

from __future__ import annotations

import importlib
import types
from pathlib import Path


def load_plugin(module_path: str) -> types.ModuleType:
    """Load a Python module by dotted path.

    Args:
        module_path: Dotted module path (e.g. ``"my_domain.validators.size_check"``).

    Returns:
        The loaded module.

    Raises:
        ModuleNotFoundError: If the module cannot be found.
        ImportError: If the module fails to import.
    """
    return importlib.import_module(module_path)


def _run_validators(
    manifest_validators: list[str],
    objects: dict[str, object],
) -> list[dict[str, object]]:
    """Run all registered validators for a domain.

    Iterates ``manifest.validators``, loads each plugin, calls
    ``module.run(objects)``, and collects results.

    Args:
        manifest_validators: List of dotted module paths from the manifest.
        objects: Domain objects to validate.

    Returns:
        List of validation result dicts with keys ``object_id``, ``severity``,
        ``message``, and ``fix_hint``.
    """
    results: list[dict[str, object]] = []
    for vpath in manifest_validators:
        try:
            mod = load_plugin(vpath)
            if not hasattr(mod, "run"):
                results.append(
                    {
                        "object_id": vpath,
                        "severity": "error",
                        "message": f"Validator module '{vpath}' has no 'run' function",
                        "fix_hint": "Add a 'run(objects)' function to the module",
                    }
                )
                continue
            output = mod.run(objects)
            if isinstance(output, list):
                results.extend(output)
        except (ModuleNotFoundError, ImportError) as exc:
            results.append(
                {
                    "object_id": vpath,
                    "severity": "error",
                    "message": f"Failed to load validator '{vpath}': {exc}",
                    "fix_hint": "Verify the module path is correct and installed",
                }
            )
    return results


def _run_exporters(
    manifest_exports: list[str],
    objects: dict[str, object],
    output_dir: Path,
) -> list[Path]:
    """Run all registered exporters for a domain.

    Iterates ``manifest.exports``, loads each plugin, calls
    ``module.run(objects, output_dir)``, and collects output file paths.

    Args:
        manifest_exports: List of dotted module paths from the manifest.
        objects: Domain objects to export.
        output_dir: Directory to write exported files into.

    Returns:
        List of output file paths that were created.
    """
    outputs: list[Path] = []
    for epath in manifest_exports:
        try:
            mod = load_plugin(epath)
            if not hasattr(mod, "run"):
                continue
            result = mod.run(objects, output_dir)
            if isinstance(result, list):
                outputs.extend(Path(p) for p in result)
            elif isinstance(result, (str, Path)):
                outputs.append(Path(result))
        except (ModuleNotFoundError, ImportError):
            continue
    return outputs
