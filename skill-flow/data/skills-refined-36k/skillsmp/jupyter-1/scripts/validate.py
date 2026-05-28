#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "nbformat>=5.9",
# ]
# ///
"""
Lightweight notebook validator - checks syntax without heavy dependencies.

Usage:
    validate.py notebook.ipynb [--require-outputs]
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass

import nbformat


@dataclass(frozen=True)
class ValidationResult:
    """Immutable validation result."""

    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def is_python_notebook(nb) -> bool:
    """Check if notebook uses Python kernel."""
    lang = nb.metadata.get("language_info", {}).get("name", "").lower()
    if not lang:
        # Fallback to kernelspec
        kernel = nb.metadata.get("kernelspec", {}).get("name", "").lower()
        return "python" in kernel or kernel == ""
    return lang == "python" or lang.startswith("python")


def validate(path: str, require_outputs: bool = False) -> ValidationResult:
    """Validate notebook structure and Python syntax. Returns immutable result."""
    nb = nbformat.read(path, as_version=4)
    errors: list[str] = []
    warnings: list[str] = []

    is_python = is_python_notebook(nb)
    if not is_python:
        lang = nb.metadata.get("language_info", {}).get("name", "unknown")
        warnings.append(f"Non-Python notebook ({lang}) - skipping syntax validation")

    if not nb.cells:
        warnings.append("Notebook has no cells")

    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue

        source = cell.source
        if not source.strip():
            continue

        # Syntax check (Python only)
        if is_python:
            try:
                ast.parse(source)
            except SyntaxError as e:
                errors.append(f"Cell {i}: Syntax error at line {e.lineno}: {e.msg}")

            # Common Python issues
            if "import *" in source:
                warnings.append(f"Cell {i}: Star import detected")

        if require_outputs and not cell.get("outputs"):
            warnings.append(f"Cell {i}: No outputs")

    return ValidationResult(errors=tuple(errors), warnings=tuple(warnings))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate notebook syntax")
    parser.add_argument("notebook", help="Path to notebook")
    parser.add_argument("--require-outputs", action="store_true")
    args = parser.parse_args()

    result = validate(args.notebook, args.require_outputs)

    if result.errors:
        print("ERRORS:")
        for e in result.errors:
            print(f"  - {e}")

    if result.warnings:
        print("WARNINGS:")
        for w in result.warnings:
            print(f"  - {w}")

    if result.is_valid and not result.warnings:
        print("Notebook is valid.")

    return 0 if result.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
