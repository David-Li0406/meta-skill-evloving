#!/usr/bin/env python3
"""
SEMO Skill Validator - Quick validation for skill structure

Usage:
    quick_validate.py <skill-directory>

Examples:
    quick_validate.py semo-next/skills/health-check
    quick_validate.py semo-po/skills/epic-master
"""

import sys
import re
import yaml
from pathlib import Path


def validate_skill(skill_path):
    """Validate a SEMO skill structure."""
    skill_path = Path(skill_path)
    errors = []
    warnings = []

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, ["SKILL.md not found"], []

    content = skill_md.read_text()

    # Check frontmatter exists
    if not content.startswith('---'):
        return False, ["No YAML frontmatter found"], []

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, ["Invalid frontmatter format"], []

    frontmatter_text = match.group(1)

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, ["Frontmatter must be a YAML dictionary"], []
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML: {e}"], []

    # Check required fields
    if 'name' not in frontmatter:
        errors.append("Missing 'name' in frontmatter")
    if 'description' not in frontmatter:
        errors.append("Missing 'description' in frontmatter")

    # Validate name format
    name = frontmatter.get('name', '')
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"Name '{name}' should be hyphen-case")
        if name.startswith('-') or name.endswith('-') or '--' in name:
            errors.append(f"Name '{name}' has invalid hyphen placement")
        if len(name) > 64:
            errors.append(f"Name too long ({len(name)} chars, max 64)")

    # Validate description
    description = frontmatter.get('description', '')
    if description:
        if '<' in description or '>' in description:
            errors.append("Description cannot contain angle brackets")
        if len(description) > 1024:
            errors.append(f"Description too long ({len(description)} chars, max 1024)")
        # SEMO-specific: check for "when to use"
        desc_lower = description.lower()
        if 'when' not in desc_lower and 'use' not in desc_lower:
            warnings.append("Description should include 'when to use' triggers")

    # Check for forbidden files
    forbidden = ['README.md', 'CHANGELOG.md', 'INSTALLATION_GUIDE.md']
    for f in forbidden:
        if (skill_path / f).exists():
            warnings.append(f"Forbidden file found: {f}")

    # Check line count
    body = content.split('---', 2)[2] if content.count('---') >= 2 else content
    line_count = len(body.strip().split('\n'))
    if line_count > 500:
        warnings.append(f"SKILL.md body has {line_count} lines (recommend <500)")

    # Check SEMO Message section
    if '[SEMO] Skill:' not in content:
        warnings.append("Missing SEMO Message section")

    if errors:
        return False, errors, warnings
    return True, [], warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: quick_validate.py <skill-directory>")
        print("\nExamples:")
        print("  quick_validate.py semo-next/skills/health-check")
        print("  quick_validate.py semo-po/skills/epic-master")
        sys.exit(1)

    skill_path = sys.argv[1]
    print(f"🔍 Validating skill: {skill_path}\n")

    valid, errors, warnings = validate_skill(skill_path)

    if errors:
        print("❌ Validation FAILED:")
        for e in errors:
            print(f"   - {e}")

    if warnings:
        print("\n⚠️  Warnings:")
        for w in warnings:
            print(f"   - {w}")

    if valid:
        print("✅ Skill is valid!")

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
