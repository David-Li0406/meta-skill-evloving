# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Preflight Validator - Verify ADR and Design Spec artifacts exist.

ADR: implement-plan-preflight skill

Usage:
    uv run preflight_validator.py <adr-id>

Example:
    uv run preflight_validator.py 2025-12-01-clickhouse-aws-ohlcv-ingestion
"""

import os
import re
import sys
from pathlib import Path

# ADR: 2025-12-08-mise-env-centralized-config
# Configuration via environment variables with defaults for backward compatibility
ADR_DIR = os.environ.get("ADR_DIR", "docs/adr")
DESIGN_DIR = os.environ.get("DESIGN_DIR", "docs/design")
DESIGN_SPEC_FILENAME = os.environ.get("DESIGN_SPEC_FILENAME", "spec.md")

# Emoji regex pattern for validation in graph labels
# Covers common emoji ranges: emoticons, symbols, dingbats, pictographs
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F9FF"  # Misc Symbols, Emoticons
    r"\U00002600-\U000026FF"  # Misc symbols (sun, cloud, etc.)
    r"\U00002700-\U000027BF"  # Dingbats
    r"\U0001FA00-\U0001FAFF]"  # Extended symbols
)


def validate_adr_frontmatter(adr_path: Path) -> list[str]:
    """Validate ADR has required YAML frontmatter fields."""
    errors = []
    required_fields = [
        "status",
        "date",
        "decision-maker",
        "consulted",
        "research-method",
        "clarification-iterations",
        "perspectives",
    ]

    content = adr_path.read_text()

    # Check for frontmatter
    if not content.startswith("---"):
        errors.append("ADR missing YAML frontmatter (must start with ---)")
        return errors

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("ADR frontmatter not properly closed (missing closing ---)")
        return errors

    frontmatter = parts[1]

    for field in required_fields:
        if f"{field}:" not in frontmatter:
            errors.append(f"ADR missing required frontmatter field: {field}")

    return errors


def validate_adr_sections(adr_path: Path) -> list[str]:
    """Validate ADR has required sections."""
    errors = []
    required_sections = [
        "Context and Problem Statement",
        "Research Summary",
        "Decision Log",
        "Considered Options",
        "Decision Outcome",
        "Synthesis",
        "Consequences",
        "Architecture",
    ]

    content = adr_path.read_text()

    for section in required_sections:
        if f"## {section}" not in content:
            errors.append(f"ADR missing required section: ## {section}")

    # Check for Design Spec link
    if "**Design Spec**:" not in content:
        errors.append("ADR missing Design Spec link in header")

    return errors


def validate_graph_labels(file_path: Path) -> list[str]:
    """Validate all graph-easy diagrams have emoji + title in label.

    Extracts graph-easy source from <details> blocks and validates each
    has a `graph { label: "emoji Title"; }` pattern.
    """
    errors = []
    content = file_path.read_text()

    # Pattern to extract graph-easy source from <details> blocks
    # Matches: <details>...<summary>graph-easy source</summary>...```...graph content...```...</details>
    details_pattern = re.compile(
        r"<details>\s*<summary>graph-easy source</summary>\s*```\s*(.*?)```\s*</details>",
        re.DOTALL | re.IGNORECASE,
    )

    # Find all graph-easy source blocks
    matches = details_pattern.findall(content)

    if not matches:
        # No diagrams found - not an error (some files may not have diagrams)
        return errors

    for i, graph_source in enumerate(matches, 1):
        # Check for graph { label: pattern
        label_match = re.search(r'graph\s*\{[^}]*label:\s*"([^"]*)"', graph_source)

        if not label_match:
            errors.append(
                f"Diagram #{i}: Missing `graph {{ label: \"emoji Title\"; }}` - "
                "every diagram MUST have emoji + title"
            )
            continue

        label_text = label_match.group(1)

        # Check for emoji in label
        if not EMOJI_PATTERN.search(label_text):
            errors.append(
                f'Diagram #{i}: Label "{label_text}" missing semantic emoji - '
                "add emoji matching diagram purpose (see Emoji Selection Guide)"
            )

    return errors


def validate_spec_backlink(spec_path: Path, adr_id: str) -> list[str]:
    """Validate design spec has ADR backlink."""
    errors = []
    content = spec_path.read_text()

    if "**ADR**:" not in content:
        errors.append("Design spec missing ADR backlink in header")

    if adr_id not in content:
        errors.append(f"Design spec ADR link doesn't reference {adr_id}")

    return errors


def validate_spec_frontmatter(spec_path: Path) -> list[str]:
    """Validate design spec has required YAML frontmatter fields."""
    errors = []
    required_fields = [
        "adr",
        "source",
        "implementation-status",
        "phase",
        "last-updated",
    ]

    content = spec_path.read_text()

    # Check for frontmatter
    if not content.startswith("---"):
        errors.append("Spec missing YAML frontmatter (must start with ---)")
        return errors

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Spec frontmatter not properly closed (missing closing ---)")
        return errors

    frontmatter = parts[1]

    for field in required_fields:
        if f"{field}:" not in frontmatter:
            errors.append(f"Spec missing required frontmatter field: {field}")

    # Validate implementation-status value
    valid_statuses = ["in_progress", "blocked", "completed", "abandoned"]
    if "implementation-status:" in frontmatter:
        status_match = re.search(r"implementation-status:\s*(\S+)", frontmatter)
        if status_match:
            status = status_match.group(1)
            if status not in valid_statuses:
                errors.append(
                    f"Spec has invalid implementation-status: {status} "
                    f"(expected: {', '.join(valid_statuses)})"
                )

    # Validate phase value
    valid_phases = ["preflight", "phase-1", "phase-2", "phase-3"]
    if "phase:" in frontmatter:
        phase_match = re.search(r"phase:\s*(\S+)", frontmatter)
        if phase_match:
            phase = phase_match.group(1)
            if phase not in valid_phases:
                errors.append(
                    f"Spec has invalid phase: {phase} "
                    f"(expected: {', '.join(valid_phases)})"
                )

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: uv run preflight_validator.py <adr-id>")
        print("Example: uv run preflight_validator.py 2025-12-01-my-feature")
        sys.exit(1)

    adr_id = sys.argv[1]

    # Validate ADR ID format
    if not re.match(r"^\d{4}-\d{2}-\d{2}-[\w-]+$", adr_id):
        print(f"Invalid ADR ID format: {adr_id}")
        print("Expected format: YYYY-MM-DD-slug")
        sys.exit(1)

    adr_path = Path(f"{ADR_DIR}/{adr_id}.md")
    spec_path = Path(f"{DESIGN_DIR}/{adr_id}/{DESIGN_SPEC_FILENAME}")

    all_errors = []

    # Check file existence
    print(f"Validating preflight artifacts for: {adr_id}")
    print("-" * 50)

    if not adr_path.exists():
        all_errors.append(f"ADR file not found: {adr_path}")
    else:
        print(f"[OK] ADR file exists: {adr_path}")
        all_errors.extend(validate_adr_frontmatter(adr_path))
        all_errors.extend(validate_adr_sections(adr_path))
        all_errors.extend(validate_graph_labels(adr_path))

    if not spec_path.exists():
        all_errors.append(f"Design spec not found: {spec_path}")
    else:
        print(f"[OK] Design spec exists: {spec_path}")
        all_errors.extend(validate_spec_frontmatter(spec_path))
        all_errors.extend(validate_spec_backlink(spec_path, adr_id))
        all_errors.extend(validate_graph_labels(spec_path))

    # Report results
    print("-" * 50)

    if all_errors:
        print(f"\n[FAIL] Preflight validation failed with {len(all_errors)} error(s):\n")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n[PASS] Preflight validation successful!")
        print("All artifacts exist and are properly formatted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
