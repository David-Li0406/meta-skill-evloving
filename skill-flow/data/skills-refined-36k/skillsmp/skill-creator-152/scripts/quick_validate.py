#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import sys
import os
import re
from pathlib import Path

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists (must be uppercase)
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        # Check if lowercase version exists
        if (skill_path / 'skill.md').exists():
            return False, "Found 'skill.md' but must be uppercase 'SKILL.md'"
        if (skill_path / 'README.md').exists():
            return False, "Found 'README.md' but must be 'SKILL.md'"
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter = match.group(1)

    # Check required fields
    if 'name:' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description:' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Check for invalid custom fields (only name, description, license allowed)
    allowed_fields = ['name', 'description', 'license']
    frontmatter_lines = frontmatter.strip().split('\n')
    for line in frontmatter_lines:
        if ':' in line:
            field = line.split(':')[0].strip()
            if field and field not in allowed_fields:
                return False, f"Invalid frontmatter field '{field}' - only 'name', 'description', and 'license' are allowed"

    # Extract name for validation
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name matches directory name
        if name != skill_path.name:
            return False, f"Name '{name}' does not match directory name '{skill_path.name}'"

    # Extract and validate description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Warn if description is too vague (no trigger context)
        trigger_keywords = ['when', 'use this', 'for', 'should be used', 'applies']
        has_trigger = any(keyword in description.lower() for keyword in trigger_keywords)
        if not has_trigger and len(description) < 50:
            return False, f"Description is too vague - should explain WHEN to use the skill (include 'when', 'use this', 'for', etc.)"

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)