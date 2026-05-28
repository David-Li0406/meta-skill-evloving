#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "# Planning Inbox Entry — Synthesis",
    "## Metadata",
    "## Purpose of this entry",
    "## Key insights or conclusions",
    "## Proposed requirements or constraints",
    "## Non-committal or exploratory ideas",
    "## Open questions and uncertainties",
    "## Suggested impact on plan or backlog",
    "## Explicit exclusions",
]

REQUIRED_METADATA_FIELDS = [
    "- Date:",
    "- Source",
    "- Author:",
    "- Related context or links:",
]

TEMPLATE_PLACEHOLDERS = [
    "(Why this input exists. What problem, decision, or opportunity it addresses.)",
    "(Crisp statements of what was learned or decided.)",
    "(Only include items you believe may warrant execution.",
    "Use clear, testable language where possible.)",
    "(Optional. Ideas that should **not** be treated as requirements.)",
    "(What still needs clarification before execution.)",
    "(If applicable, describe how this might change priorities, sequencing,",
    "or scope. This is advisory, not binding.)",
    "(Anything that was discussed but should **not** be carried forward.)",
]

FILENAME_PATTERNS = [
    re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}_.+_.+\.md$"),
    re.compile(r"^\d{4}-\d{2}-\d{2}-.+-.+\.md$"),
]


def find_repo_root(start: Path) -> Path | None:
    for candidate in [start, *start.parents]:
        if (candidate / "planning" / "inbox").is_dir():
            return candidate
    return None


def load_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []


def find_heading_indices(lines: list[str]) -> dict[str, int]:
    indices = {}
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped in REQUIRED_HEADINGS and stripped not in indices:
            indices[stripped] = idx
    return indices


def section_content(lines: list[str], start_idx: int, end_idx: int) -> list[str]:
    content = []
    for line in lines[start_idx + 1 : end_idx]:
        if line.strip():
            content.append(line)
    return content


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    errors = []
    warnings = []
    lines = load_lines(path)
    if not lines:
        errors.append("File is empty or unreadable.")
        return errors, warnings

    indices = find_heading_indices(lines)
    for heading in REQUIRED_HEADINGS:
        if heading not in indices:
            errors.append(f"Missing heading: {heading}")

    if errors:
        return errors, warnings

    ordered_indices = [indices[h] for h in REQUIRED_HEADINGS]
    if ordered_indices != sorted(ordered_indices):
        errors.append("Headings are out of order.")
        return errors, warnings

    for i, heading in enumerate(REQUIRED_HEADINGS):
        start_idx = indices[heading]
        end_idx = indices[REQUIRED_HEADINGS[i + 1]] if i + 1 < len(REQUIRED_HEADINGS) else len(lines)
        content = section_content(lines, start_idx, end_idx)
        if not content:
            errors.append(f"Section '{heading}' is empty.")

    metadata_start = indices["## Metadata"]
    metadata_end = indices["## Purpose of this entry"]
    metadata_content = [line.strip() for line in lines[metadata_start + 1 : metadata_end] if line.strip()]
    for field in REQUIRED_METADATA_FIELDS:
        if not any(line.startswith(field) for line in metadata_content):
            errors.append(f"Metadata field missing: {field}")

    if not any(pattern.match(path.name) for pattern in FILENAME_PATTERNS):
        warnings.append("Filename does not match the recommended naming convention.")

    for placeholder in TEMPLATE_PLACEHOLDERS:
        if placeholder in lines:
            warnings.append("Template placeholder text still present.")
            break

    return errors, warnings


def collect_inbox_files(repo_root: Path) -> list[Path]:
    inbox_dir = repo_root / "planning" / "inbox"
    files = [path for path in inbox_dir.glob("*.md") if path.name != ".gitkeep"]
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate planning inbox entries.")
    parser.add_argument("paths", nargs="*", help="Optional inbox entry file paths to validate.")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    if not repo_root:
        print("Error: could not locate repo root with planning/inbox.", file=sys.stderr)
        return 2

    if args.paths:
        files = [Path(p).expanduser().resolve() for p in args.paths]
    else:
        files = collect_inbox_files(repo_root)

    if not files:
        print("No inbox entries found to validate.")
        return 0

    had_errors = False
    for path in files:
        errors, warnings = validate_file(path)
        if errors:
            had_errors = True
        status = "OK" if not errors else "ERROR"
        print(f"{status}: {path}")
        for error in errors:
            print(f"  - {error}")
        for warning in warnings:
            print(f"  - Warning: {warning}")

    return 1 if had_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
