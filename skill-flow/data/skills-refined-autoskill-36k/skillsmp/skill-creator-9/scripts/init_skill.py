#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> [--path <path>]

Examples:
    init_skill.py my-new-skill
    init_skill.py my-api-helper --path ~/dotfiles/.claude/skills
    init_skill.py custom-skill --path /custom/location

Default path: ~/dotfiles/.claude/skills/
"""

import sys
import os
from pathlib import Path


# Default skills directory
DEFAULT_SKILLS_PATH = Path.home() / "dotfiles" / ".claude" / "skills"


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## When to Use This Skill

**Proactively use this skill when:**
- [TODO: List specific triggers/scenarios]

**DO NOT use when:**
- [TODO: List scenarios where this skill should NOT be used]

## Instructions

### 1. [TODO: First Step]

[TODO: Add detailed instructions]

### 2. [TODO: Second Step]

[TODO: Add detailed instructions]

## Error Handling

- [TODO: Common error scenarios and how to handle them]

## Notes

- Use Nushell syntax (`;` not `&&`)
- [TODO: Add any additional notes]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.
"""

def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def validate_skill_name(skill_name):
    """Validate skill name follows conventions."""
    import re
    if not re.match(r'^[a-z0-9-]+$', skill_name):
        return False, "Name should be hyphen-case (lowercase letters, digits, and hyphens only)"
    if skill_name.startswith('-') or skill_name.endswith('-') or '--' in skill_name:
        return False, "Name cannot start/end with hyphen or contain consecutive hyphens"
    if len(skill_name) > 64:
        return False, f"Name is too long ({len(skill_name)} characters). Maximum is 64 characters."
    return True, None


def init_skill(skill_name, path):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    # Validate skill name
    valid, error = validate_skill_name(skill_name)
    if not valid:
        print(f"Error: {error}")
        return None

    # Determine skill directory path
    skill_dir = Path(path).expanduser().resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("Created SKILL.md")
    except Exception as e:
        print(f"Error creating SKILL.md: {e}")
        return None

    # Create resource directories with example files
    try:
        # Create scripts/ directory with example script
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("Created scripts/example.py")

        # Create references/ directory with example reference doc
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("Created references/reference.md")

    except Exception as e:
        print(f"Error creating resource directories: {e}")
        return None

    # Print next steps
    print(f"\nSkill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    print("2. Customize or delete the example files in scripts/ and references/")
    print("3. Run quick_validate.py to check the skill structure")

    return skill_dir


def main():
    if len(sys.argv) < 2:
        print("Usage: init_skill.py <skill-name> [--path <path>]")
        print("\nSkill name requirements:")
        print("  - Hyphen-case identifier (e.g., 'data-analyzer')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 64 characters")
        print(f"\nDefault path: {DEFAULT_SKILLS_PATH}")
        print("\nExamples:")
        print("  init_skill.py my-new-skill")
        print("  init_skill.py my-api-helper --path ~/dotfiles/.claude/skills")
        sys.exit(1)

    skill_name = sys.argv[1]

    # Parse --path argument
    path = DEFAULT_SKILLS_PATH
    if '--path' in sys.argv:
        path_index = sys.argv.index('--path')
        if path_index + 1 < len(sys.argv):
            path = sys.argv[path_index + 1]
        else:
            print("Error: --path requires a value")
            sys.exit(1)

    print(f"Initializing skill: {skill_name}")
    print(f"Location: {path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
