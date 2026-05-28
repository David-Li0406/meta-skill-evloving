#!/usr/bin/env python3
"""
Design Token Validator

Scans CSS files for hardcoded values that should use design tokens.
Flags colors, pixel values, and other magic numbers.

Usage:
    python validate_design_tokens.py <path> [--format text|json]
    python validate_design_tokens.py src/styles/ --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple


class Violation(NamedTuple):
    file: str
    line: int
    property: str
    value: str
    suggestion: str
    severity: str  # "error" or "warning"


# Patterns for hardcoded values that should use design tokens
HARDCODED_PATTERNS = {
    # Colors - hex codes
    "hex_color": {
        "pattern": r":\s*(#[0-9a-fA-F]{3,8})\s*[;}\n]",
        "suggestion": "Use var(--color-*) instead of hardcoded hex",
        "severity": "error",
    },
    # Colors - rgb/rgba
    "rgb_color": {
        "pattern": r":\s*(rgba?\([^)]+\))\s*[;}\n]",
        "suggestion": "Use var(--color-*) instead of rgb/rgba",
        "severity": "error",
    },
    # Colors - hsl/hsla
    "hsl_color": {
        "pattern": r":\s*(hsla?\([^)]+\))\s*[;}\n]",
        "suggestion": "Use var(--color-*) instead of hsl/hsla",
        "severity": "error",
    },
    # Font sizes - pixel values
    "font_size_px": {
        "pattern": r"font-size:\s*(\d+px)\s*[;}\n]",
        "suggestion": "Use var(--font-size-*) instead of px value",
        "severity": "error",
    },
    # Font sizes - rem values (except common base values)
    "font_size_rem": {
        "pattern": r"font-size:\s*(\d+(?:\.\d+)?rem)\s*[;}\n]",
        "suggestion": "Use var(--font-size-*) instead of rem value",
        "severity": "warning",
    },
    # Spacing - margin/padding with pixel values
    "spacing_px": {
        "pattern": r"(?:margin|padding)(?:-(?:top|right|bottom|left))?:\s*(\d+px(?:\s+\d+px)*)\s*[;}\n]",
        "suggestion": "Use var(--space-*) instead of px spacing",
        "severity": "error",
    },
    # Border radius with pixel values
    "border_radius_px": {
        "pattern": r"border-radius:\s*(\d+px)\s*[;}\n]",
        "suggestion": "Use var(--radius-*) instead of px radius",
        "severity": "error",
    },
    # Box shadow with hardcoded values
    "box_shadow_hardcoded": {
        "pattern": r"box-shadow:\s*(\d+px\s+\d+px[^;var]+);",
        "suggestion": "Use var(--shadow-*) instead of hardcoded shadow",
        "severity": "warning",
    },
    # Transition timing with hardcoded values
    "transition_timing": {
        "pattern": r"transition[^:]*:\s*[^;]*(\d+(?:\.\d+)?m?s)[^var;]*;",
        "suggestion": "Use var(--duration-*) for timing",
        "severity": "warning",
    },
    # Z-index with magic numbers
    "z_index_magic": {
        "pattern": r"z-index:\s*(\d{2,})\s*[;}\n]",
        "suggestion": "Use var(--z-*) instead of magic z-index",
        "severity": "warning",
    },
    # Line height with unitless magic numbers
    "line_height_magic": {
        "pattern": r"line-height:\s*(\d+(?:\.\d+)?)\s*[;}\n]",
        "suggestion": "Use var(--line-height-*) for consistency",
        "severity": "warning",
    },
}

# Allowed exceptions - values that are OK to hardcode
ALLOWED_VALUES = {
    "0",
    "0px",
    "1px",  # Minimum border
    "100%",
    "50%",
    "auto",
    "none",
    "inherit",
    "initial",
    "unset",
    "currentColor",
    "transparent",
}

# Files/patterns to skip
SKIP_PATTERNS = [
    r"node_modules",
    r"\.min\.css$",
    r"vendor",
    r"reset\.css$",
    r"normalize\.css$",
]


def should_skip_file(file_path: str) -> bool:
    """Check if file should be skipped."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def is_in_var_context(line: str, match_start: int) -> bool:
    """Check if the value is already inside a var() or calc()."""
    # Look backwards from match to see if we're inside var() or calc()
    before = line[:match_start]
    open_parens = before.count("var(") + before.count("calc(")
    close_parens = before.count(")")
    return open_parens > close_parens


def is_in_comment(line: str, match_start: int) -> bool:
    """Check if match is inside a CSS comment."""
    # Simple check - look for /* before the match without closing */
    comment_start = line.rfind("/*", 0, match_start)
    if comment_start == -1:
        return False
    comment_end = line.find("*/", comment_start)
    return comment_end == -1 or comment_end > match_start


def validate_file(file_path: Path) -> list[Violation]:
    """Validate a single CSS file for hardcoded values."""
    violations = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return violations

    lines = content.split("\n")

    for line_num, line in enumerate(lines, start=1):
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith("/*") or stripped.startswith("//"):
            continue

        # Check each pattern
        for name, config in HARDCODED_PATTERNS.items():
            for match in re.finditer(config["pattern"], line):
                value = match.group(1)

                # Skip allowed values
                if value in ALLOWED_VALUES:
                    continue

                # Skip if inside var() or calc()
                if is_in_var_context(line, match.start()):
                    continue

                # Skip if inside comment
                if is_in_comment(line, match.start()):
                    continue

                # Extract property name (simplified)
                prop_match = re.search(r"([a-z-]+):\s*" + re.escape(value), line)
                prop = prop_match.group(1) if prop_match else "unknown"

                violations.append(Violation(
                    file=str(file_path),
                    line=line_num,
                    property=prop,
                    value=value,
                    suggestion=config["suggestion"],
                    severity=config["severity"],
                ))

    return violations


def find_css_files(path: Path) -> list[Path]:
    """Find all CSS files in the given path."""
    if path.is_file():
        return [path] if path.suffix == ".css" else []

    css_files = []
    for file_path in path.rglob("*.css"):
        if not should_skip_file(str(file_path)):
            css_files.append(file_path)

    return sorted(css_files)


def format_text_output(violations: list[Violation]) -> str:
    """Format violations as human-readable text."""
    if not violations:
        return "✅ No hardcoded values found. All CSS uses design tokens correctly."

    output = []
    output.append(f"Found {len(violations)} hardcoded value(s):\n")

    # Group by file
    by_file: dict[str, list[Violation]] = {}
    for v in violations:
        by_file.setdefault(v.file, []).append(v)

    for file_path, file_violations in by_file.items():
        output.append(f"📄 {file_path}")
        for v in file_violations:
            icon = "❌" if v.severity == "error" else "⚠️"
            output.append(f"  {icon} Line {v.line}: {v.property}: {v.value}")
            output.append(f"     └─ {v.suggestion}")
        output.append("")

    # Summary
    errors = sum(1 for v in violations if v.severity == "error")
    warnings = sum(1 for v in violations if v.severity == "warning")

    output.append("─" * 50)
    output.append(f"Summary: {errors} error(s), {warnings} warning(s)")

    if errors > 0:
        output.append("\n❌ Design token validation FAILED")
    else:
        output.append("\n⚠️ Design token validation passed with warnings")

    return "\n".join(output)


def format_json_output(violations: list[Violation]) -> str:
    """Format violations as JSON."""
    return json.dumps({
        "total": len(violations),
        "errors": sum(1 for v in violations if v.severity == "error"),
        "warnings": sum(1 for v in violations if v.severity == "warning"),
        "violations": [v._asdict() for v in violations],
    }, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Validate CSS for hardcoded values that should use design tokens"
    )
    parser.add_argument("path", help="File or directory to scan")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    # Find and validate files
    css_files = find_css_files(path)

    if not css_files:
        print(f"No CSS files found in {path}", file=sys.stderr)
        sys.exit(0)

    all_violations = []
    for css_file in css_files:
        violations = validate_file(css_file)
        all_violations.extend(violations)

    # Output
    if args.format == "json":
        print(format_json_output(all_violations))
    else:
        print(format_text_output(all_violations))

    # Exit code based on errors (not warnings)
    errors = sum(1 for v in all_violations if v.severity == "error")
    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
