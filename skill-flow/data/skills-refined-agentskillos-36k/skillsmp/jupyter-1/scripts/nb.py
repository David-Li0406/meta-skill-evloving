#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "nbformat>=5.9",
#     "nbclient>=0.8",
#     "nbconvert>=7.0",
# ]
# ///
"""
Jupyter Notebook CLI - A unified tool for notebook interaction.

Usage:
    nb.py inspect <notebook>              List cells and metadata
    nb.py show <notebook> [options]       Show cell contents
    nb.py execute <notebook> [options]    Execute notebook
    nb.py validate <notebook>             Validate notebook structure
    nb.py convert <notebook> --to <fmt>   Convert notebook
    nb.py clear <notebook>                Clear all outputs
    nb.py grep <pattern> <notebook>       Search cells for pattern
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from nbformat import NotebookNode


# =============================================================================
# Domain Types
# =============================================================================


@dataclass(frozen=True)
class CellInfo:
    """Immutable cell metadata for display."""

    index: int
    cell_type: str
    lines: int
    has_output: bool
    first_line: str


@dataclass(frozen=True)
class NotebookMeta:
    """Immutable notebook metadata."""

    path: str
    kernel: str
    language: str
    cell_count: int


@dataclass(frozen=True)
class ValidationResult:
    """Immutable validation result."""

    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


@dataclass(frozen=True)
class CellMatch:
    """Immutable cell match result."""

    index: int
    cell_type: str
    matching_lines: tuple[str, ...]
    source: str


# =============================================================================
# Constants
# =============================================================================

IMAGE_FORMATS: dict[str, str] = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/svg+xml": ".svg",
}


# =============================================================================
# Errors
# =============================================================================


class NotebookError(Exception):
    """Base exception for notebook operations."""

    pass


class NotebookLoadError(NotebookError):
    """Failed to load notebook."""

    def __init__(self, path: str, reason: str):
        self.path = path
        self.reason = reason
        super().__init__(f"Failed to load {path}: {reason}")


class CellExecutionError(NotebookError):
    """Cell execution failed."""

    def __init__(self, cell_index: int, error: str):
        self.cell_index = cell_index
        self.error = error
        super().__init__(f"Cell {cell_index} failed: {error}")


# =============================================================================
# Protocols
# =============================================================================


class OutputPrinter(Protocol):
    """Protocol for output printing strategies."""

    def print(self, output: dict, raw: bool = False) -> None: ...


# =============================================================================
# Core Functions
# =============================================================================


def load_notebook(path: str) -> "NotebookNode":
    """Load a notebook from path."""
    import nbformat

    try:
        return nbformat.read(path, as_version=4)
    except Exception as e:
        raise NotebookLoadError(path, str(e)) from e


def save_notebook(nb: "NotebookNode", path: str) -> None:
    """Save notebook to path."""
    import nbformat

    nbformat.write(nb, path)


def get_notebook_meta(nb: "NotebookNode", path: str) -> NotebookMeta:
    """Extract notebook metadata."""
    return NotebookMeta(
        path=path,
        kernel=nb.metadata.get("kernelspec", {}).get("display_name", "unknown"),
        language=nb.metadata.get("language_info", {}).get("name", "unknown"),
        cell_count=len(nb.cells),
    )


def get_cell_info(cell: dict, index: int) -> CellInfo:
    """Extract cell info for display."""
    source = cell.get("source", "")
    return CellInfo(
        index=index,
        cell_type=cell.get("cell_type", "unknown"),
        lines=source.count("\n") + 1 if source else 0,
        has_output=bool(cell.get("outputs", [])),
        first_line=source.split("\n")[0][:40] if source else "(empty)",
    )


def is_python_notebook(nb: "NotebookNode") -> bool:
    """Check if notebook uses Python kernel."""
    lang = nb.metadata.get("language_info", {}).get("name", "").lower()
    if not lang:
        # Fallback to kernelspec
        kernel = nb.metadata.get("kernelspec", {}).get("name", "").lower()
        return "python" in kernel or kernel == ""
    return lang == "python" or lang.startswith("python")


def find_matching_cells(
    nb: "NotebookNode",
    pattern: re.Pattern[str],
) -> tuple[CellMatch, ...]:
    """Find cells matching pattern. Pure function returning immutable results."""
    matches: list[CellMatch] = []
    for i, cell in enumerate(nb.cells):
        source = cell.get("source", "")
        if pattern.search(source):
            matching = tuple(ln for ln in source.split("\n") if pattern.search(ln))
            matches.append(CellMatch(i, cell.cell_type, matching, source))
    return tuple(matches)


def save_image_output(
    data: dict[str, str],
    image_dir: Path,
    cell_idx: int,
    output_idx: int,
) -> Path | None:
    """Save image data to file. Returns path if saved, None if no image."""
    import base64

    for mime_type, ext in IMAGE_FORMATS.items():
        if mime_type in data:
            image_dir.mkdir(parents=True, exist_ok=True)
            path = image_dir / f"cell_{cell_idx}_output_{output_idx}{ext}"
            content = data[mime_type]
            if mime_type == "image/svg+xml":
                path.write_text(content if isinstance(content, str) else "".join(content))
            else:
                path.write_bytes(base64.b64decode(content))
            return path
    return None


def parse_cell_indices(spec: str, total: int) -> list[int]:
    """Parse cell specification like '0,2-4,7' into list of indices."""
    indices: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s) if start_s else 0
            end = int(end_s) if end_s else total - 1
            indices.extend(range(start, end + 1))
        else:
            indices.append(int(part))
    return sorted(set(i for i in indices if 0 <= i < total))


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from text."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def print_output(
    output: dict,
    raw: bool = False,
    image_dir: Path | None = None,
    cell_idx: int = 0,
    output_idx: int = 0,
) -> None:
    """Print a cell output."""
    match output.get("output_type", ""):
        case "stream":
            print(output.get("text", ""), end="")

        case "execute_result" | "display_data":
            data = output.get("data", {})

            # Try to save image first
            if image_dir:
                saved_path = save_image_output(data, image_dir, cell_idx, output_idx)
                if saved_path:
                    print(f"[Image saved: {saved_path}]")
                    return

            if raw:
                print(json.dumps(data, indent=2))
            elif "text/plain" in data:
                text = data["text/plain"]
                if isinstance(text, list):
                    text = "".join(text)
                print(text)
            elif "text/html" in data:
                print("[HTML output - use --raw to see]")
            elif "image/png" in data:
                print("[Image output (PNG)]")
            elif "image/jpeg" in data:
                print("[Image output (JPEG)]")
            elif "image/svg+xml" in data:
                print("[Image output (SVG)]")
            else:
                print(f"[Output type: {list(data.keys())}]")

        case "error":
            print(f"Error: {output.get('ename', 'Unknown')}")
            print(output.get("evalue", ""))
            if not raw:
                for line in output.get("traceback", []):
                    print(strip_ansi(line))


def validate_notebook(nb: "NotebookNode", require_outputs: bool = False) -> ValidationResult:
    """Validate notebook structure and code. Returns immutable result."""
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


# =============================================================================
# Commands
# =============================================================================


def cmd_inspect(args: argparse.Namespace) -> int:
    """Inspect notebook structure."""
    nb = load_notebook(args.notebook)
    meta = get_notebook_meta(nb, args.notebook)

    print(f"Notebook: {meta.path}")
    print(f"Kernel: {meta.kernel}")
    print(f"Language: {meta.language}")
    print(f"Cells: {meta.cell_count}")
    print()
    print("Index | Type     | Lines | Has Output | First Line")
    print("-" * 70)

    for i, cell in enumerate(nb.cells):
        info = get_cell_info(cell, i)
        output_marker = "Yes" if info.has_output else "No"
        print(f"{info.index:5} | {info.cell_type:8} | {info.lines:5} | {output_marker:10} | {info.first_line}")

    return 0


def cmd_show(args: argparse.Namespace) -> int:
    """Show cell contents."""
    nb = load_notebook(args.notebook)
    image_dir = Path(args.save_images) if args.save_images else None

    indices = parse_cell_indices(args.cells, len(nb.cells)) if args.cells else list(range(len(nb.cells)))

    for i in indices:
        if i >= len(nb.cells):
            print(f"Warning: Cell {i} does not exist", file=sys.stderr)
            continue

        cell = nb.cells[i]

        # Filter by type
        if args.type and cell.cell_type != args.type:
            continue

        print("=" * 60)
        print(f"CELL {i} [{cell.cell_type}]")
        print("=" * 60)

        if not args.output_only:
            print(cell.source)

        if args.output or args.output_only:
            outputs = cell.get("outputs", [])
            if outputs:
                print("\n--- OUTPUT ---")
                for out_idx, out in enumerate(outputs):
                    print_output(out, args.raw, image_dir, i, out_idx)
        print()

    return 0


def cmd_execute(args: argparse.Namespace) -> int:
    """Execute notebook cells."""
    from nbclient import NotebookClient
    from nbclient.exceptions import CellExecutionError as NBCellExecutionError

    nb = load_notebook(args.notebook)
    image_dir = Path(args.save_images) if args.save_images else None

    client = NotebookClient(
        nb,
        timeout=args.timeout,
        kernel_name=args.kernel or nb.metadata.get("kernelspec", {}).get("name", "python3"),
    )

    try:
        if args.cells:
            indices = parse_cell_indices(args.cells, len(nb.cells))
            with client.setup_kernel():
                for i in indices:
                    if i >= len(nb.cells):
                        print(f"Warning: Cell {i} does not exist", file=sys.stderr)
                        continue
                    print(f"Executing cell {i}...", file=sys.stderr)
                    client.execute_cell(nb.cells[i], i)
        else:
            print("Executing all cells...", file=sys.stderr)
            client.execute()

        print("Execution complete.", file=sys.stderr)

    except NBCellExecutionError as e:
        print(f"Cell execution failed: {e}", file=sys.stderr)
        if not args.allow_errors:
            return 1

    # Save or show results
    if args.in_place:
        save_notebook(nb, args.notebook)
        print(f"Saved: {args.notebook}", file=sys.stderr)
    else:
        indices = parse_cell_indices(args.cells, len(nb.cells)) if args.cells else list(range(len(nb.cells)))
        for i in indices:
            if i >= len(nb.cells):
                continue
            cell = nb.cells[i]
            if cell.cell_type == "code" and cell.get("outputs"):
                print(f"\n--- CELL {i} OUTPUT ---")
                for out_idx, out in enumerate(cell["outputs"]):
                    print_output(out, image_dir=image_dir, cell_idx=i, output_idx=out_idx)

    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate notebook structure and code."""
    nb = load_notebook(args.notebook)
    result = validate_notebook(nb, args.require_outputs)

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


def cmd_convert(args: argparse.Namespace) -> int:
    """Convert notebook to other formats."""
    from nbconvert import exporters

    nb = load_notebook(args.notebook)

    exporter_map: dict[str, type] = {
        "py": exporters.PythonExporter,
        "python": exporters.PythonExporter,
        "html": exporters.HTMLExporter,
        "md": exporters.MarkdownExporter,
        "markdown": exporters.MarkdownExporter,
        "rst": exporters.RSTExporter,
        "script": exporters.ScriptExporter,
    }

    fmt = args.to.lower()
    if fmt not in exporter_map:
        print(f"Unknown format: {fmt}. Available: {list(exporter_map.keys())}", file=sys.stderr)
        return 1

    exporter = exporter_map[fmt]()
    body, _ = exporter.from_notebook_node(nb)

    if args.output:
        Path(args.output).write_text(body)
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(body)

    return 0


def cmd_clear(args: argparse.Namespace) -> int:
    """Clear all outputs from notebook."""
    nb = load_notebook(args.notebook)

    cleared = sum(1 for cell in nb.cells if cell.cell_type == "code" and cell.get("outputs"))

    for cell in nb.cells:
        if cell.cell_type == "code":
            cell["outputs"] = []
            cell["execution_count"] = None

    save_notebook(nb, args.notebook)
    print(f"Cleared outputs from {cleared} cells.", file=sys.stderr)
    return 0


def cmd_grep(args: argparse.Namespace) -> int:
    """Search cells for pattern."""
    nb = load_notebook(args.notebook)
    flags = re.IGNORECASE if args.ignore_case else 0
    pattern = re.compile(args.pattern, flags)

    matches = find_matching_cells(nb, pattern)

    if not matches:
        print(f"No matches for '{args.pattern}'", file=sys.stderr)
        return 1

    if args.cells_only:
        print(",".join(str(m.index) for m in matches))
        return 0

    for m in matches:
        print(f"=== CELL {m.index} [{m.cell_type}] ===")
        if args.context:
            print(m.source)
        else:
            for line in m.matching_lines:
                print(line)
        print()

    return 0


# =============================================================================
# CLI
# =============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Jupyter Notebook CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="List cells and metadata")
    p_inspect.add_argument("notebook", help="Path to notebook")
    p_inspect.set_defaults(func=cmd_inspect)

    # show
    p_show = subparsers.add_parser("show", help="Show cell contents")
    p_show.add_argument("notebook", help="Path to notebook")
    p_show.add_argument("-c", "--cells", help="Cell indices (e.g., 0,2-4,7)")
    p_show.add_argument("-t", "--type", choices=["code", "markdown"], help="Filter by type")
    p_show.add_argument("-o", "--output", action="store_true", help="Include outputs")
    p_show.add_argument("--output-only", action="store_true", help="Show only outputs")
    p_show.add_argument("--raw", action="store_true", help="Show raw output data")
    p_show.add_argument("--save-images", metavar="DIR", help="Save images to directory")
    p_show.set_defaults(func=cmd_show)

    # execute
    p_exec = subparsers.add_parser("execute", help="Execute notebook")
    p_exec.add_argument("notebook", help="Path to notebook")
    p_exec.add_argument("-c", "--cells", help="Cell indices to execute")
    p_exec.add_argument("-i", "--in-place", action="store_true", help="Save outputs back to file")
    p_exec.add_argument("-k", "--kernel", help="Kernel name to use")
    p_exec.add_argument("-t", "--timeout", type=int, default=600, help="Cell timeout (seconds)")
    p_exec.add_argument("--allow-errors", action="store_true", help="Continue on cell errors")
    p_exec.add_argument("--save-images", metavar="DIR", help="Save images to directory")
    p_exec.set_defaults(func=cmd_execute)

    # validate
    p_val = subparsers.add_parser("validate", help="Validate notebook")
    p_val.add_argument("notebook", help="Path to notebook")
    p_val.add_argument("--require-outputs", action="store_true", help="Warn if cells have no outputs")
    p_val.set_defaults(func=cmd_validate)

    # convert
    p_conv = subparsers.add_parser("convert", help="Convert notebook")
    p_conv.add_argument("notebook", help="Path to notebook")
    p_conv.add_argument("--to", required=True, help="Output format (py, html, md, rst)")
    p_conv.add_argument("-o", "--output", help="Output file (default: stdout)")
    p_conv.set_defaults(func=cmd_convert)

    # clear
    p_clear = subparsers.add_parser("clear", help="Clear outputs")
    p_clear.add_argument("notebook", help="Path to notebook")
    p_clear.set_defaults(func=cmd_clear)

    # grep
    p_grep = subparsers.add_parser("grep", help="Search cells for pattern")
    p_grep.add_argument("pattern", help="Regex pattern to search for")
    p_grep.add_argument("notebook", help="Path to notebook")
    p_grep.add_argument("-i", "--ignore-case", action="store_true", help="Case-insensitive search")
    p_grep.add_argument("-C", "--context", action="store_true", help="Show full cell context")
    p_grep.add_argument("--cells-only", action="store_true", help="Print only matching cell indices")
    p_grep.set_defaults(func=cmd_grep)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
