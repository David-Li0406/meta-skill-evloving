#!/usr/bin/env python3
"""
Validate AGD (Agent-centric Governance Decision) files.

Managed by: agent-centric skill (auto-updated, do not edit manually)
To disable auto-update, add this filename to disableAutoUpdateScripts in config.json.

Usage:
    validate-agds.py                    # Auto-detect from CLAUDE_PROJECT_DIR
    validate-agds.py <project_dir>      # Manual override

Called by PostToolUse hook after Write/Edit operations.
Reads hook input from stdin to determine if validation is needed.

Exit codes:
- 0: Valid, all AGD files pass validation
- 2: Invalid, validation errors found (blocking - Claude will process)
"""

import json
import re
import sys
from pathlib import Path

from utils import (
    AGD_PATTERN,
    REF_FIELDS,
    find_agd_file,
    get_agents_dir,
    get_decisions_dir,
    get_project_dir,
    load_config,
    parse_frontmatter,
)


def validate_tags(tags_str: str, allowed_tags: list[str], filename: str) -> list[str]:
    """Validate that all tags are in the allowed list."""
    if not tags_str:
        return []

    errors = []
    tags = [t.strip() for t in tags_str.split(',') if t.strip()]
    for tag in tags:
        if tag not in allowed_tags:
            errors.append(f"{filename}: invalid tag '{tag}' (not in config.tags)")
    return errors


def validate_references(frontmatter: dict, decisions_dir: Path, filename: str) -> list[str]:
    """Validate that all AGD references point to existing files."""
    errors = []

    for field in REF_FIELDS:
        if field not in frontmatter or not frontmatter[field]:
            continue

        refs = [r.strip() for r in frontmatter[field].split(',') if r.strip()]
        for ref in refs:
            ref_match = re.match(r'(AGD-\d+)', ref)
            if not ref_match:
                errors.append(f"{filename}: invalid reference format '{ref}' in {field}")
                continue

            if not find_agd_file(decisions_dir, ref):
                errors.append(f"{filename}: {field} references non-existent {ref_match.group(1)}")

    return errors


def validate_all_decisions(project_dir: Path) -> list[str]:
    """Validate all AGD files in the decisions directory."""
    errors = []
    decisions_dir = get_decisions_dir(project_dir)
    config_path = get_agents_dir(project_dir) / 'config.json'

    if not decisions_dir.exists():
        return errors

    config = load_config(config_path)
    allowed_tags = config.get('tags', []) if config else []

    for agd_file in decisions_dir.glob(AGD_PATTERN):
        try:
            content = agd_file.read_text()
        except IOError as e:
            errors.append(f"{agd_file.name}: cannot read file - {e}")
            continue

        frontmatter = parse_frontmatter(content)

        if 'tags' in frontmatter:
            errors.extend(validate_tags(frontmatter['tags'], allowed_tags, agd_file.name))

        errors.extend(validate_references(frontmatter, decisions_dir, agd_file.name))

    return errors


def main():
    project_dir = get_project_dir()

    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    tool_input = hook_input.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    # Only validate if the operation was on an AGD file
    if file_path:
        decisions_path = str(get_decisions_dir(project_dir))
        if decisions_path not in file_path:
            sys.exit(0)

    errors = validate_all_decisions(project_dir)

    if errors:
        print("\n⚠️  AGD VALIDATION ERRORS", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        print("\n📋 To fix tag errors:", file=sys.stderr)
        print("   1. Add missing tags to .agents/config.json", file=sys.stderr)
        print("   2. Or update the AGD file to use existing tags", file=sys.stderr)
        print("\n📋 To fix reference errors:", file=sys.stderr)
        print("   Check that referenced AGD files exist", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == '__main__':
    main()
