#!/usr/bin/env python3
"""
Quick validation script for skills - no external dependencies

Usage:
    python3 quick_validate.py <skill_directory>

This script validates:
- SKILL.md exists
- YAML frontmatter is present and valid
- Required fields (name, description) exist
- Naming conventions are followed
"""

import sys
import re
from pathlib import Path


# Allowed properties in frontmatter
ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'}


def parse_simple_yaml(yaml_text):
    """
    Simple YAML parser for skill frontmatter.
    Handles basic key: value pairs without external dependencies.
    """
    result = {}
    current_key = None
    multiline_value = []

    for line in yaml_text.split('\n'):
        # Skip empty lines
        if not line.strip():
            if current_key and multiline_value:
                multiline_value.append('')
            continue

        # Check if this is a new key
        match = re.match(r'^([a-z][a-z0-9_-]*)\s*:\s*(.*)$', line, re.IGNORECASE)
        if match:
            # Save previous multiline value
            if current_key and multiline_value:
                result[current_key] = '\n'.join(multiline_value).strip()
                multiline_value = []

            key = match.group(1).lower()
            value = match.group(2).strip()

            # Handle inline value
            if value:
                result[key] = value
                current_key = None
            else:
                current_key = key
        elif current_key:
            # Continue multiline value
            multiline_value.append(line.strip())

    # Save final multiline value
    if current_key and multiline_value:
        result[current_key] = '\n'.join(multiline_value).strip()

    return result


def validate_skill(skill_path):
    """
    Validate a skill directory.

    Returns:
        tuple: (is_valid: bool, message: str)
    """
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read content
    content = skill_md.read_text()

    # Check frontmatter exists
    if not content.startswith('---'):
        return False, "No YAML frontmatter found (must start with ---)"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format (missing closing ---)"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = parse_simple_yaml(frontmatter_text)
    except Exception as e:
        return False, f"Error parsing frontmatter: {e}"

    # Check for unexpected properties
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Validate name
    name = frontmatter.get('name', '').strip()
    if not name:
        return False, "Name cannot be empty"

    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"

    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"

    if len(name) > 64:
        return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Validate description
    description = frontmatter.get('description', '').strip()
    if not description:
        return False, "Description cannot be empty"

    if '<' in description or '>' in description:
        return False, "Description cannot contain angle brackets (< or >)"

    if len(description) > 1024:
        return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Check for TODO placeholders
    if '[TODO' in description:
        return False, "Description still contains [TODO] placeholder - please complete it"

    return True, "Skill is valid!"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 quick_validate.py <skill_directory>")
        print("\nExample:")
        print("  python3 quick_validate.py ~/dotfiles/.claude/skills/my-skill")
        sys.exit(1)

    skill_path = sys.argv[1]

    print(f"Validating skill: {skill_path}")
    print()

    valid, message = validate_skill(skill_path)

    if valid:
        print(f"Success: {message}")
    else:
        print(f"Error: {message}")

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
