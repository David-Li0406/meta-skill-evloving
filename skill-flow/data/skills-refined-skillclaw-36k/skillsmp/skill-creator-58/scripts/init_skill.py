#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
 init_skill.py <skill-name> --path <path>

Examples:
 init_skill.py my-new-skill --path skills/public
 init_skill.py my-api-helper --path skills/private
 init_skill.py custom-skill --path /custom/location

For opencode (note the singular `skill` dir name - not plural):
 init_skill.py my-skill --path ~/.config/opencode/skill
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: What the skill does AND when to trigger it. Include specific scenarios, file types, or tasks.]
---

# {skill_title}

[TODO: Add skill content. Delete unused sections below.]

## Resources

Optional directories (delete if unused):
- scripts/ - executable code (Python/Bash)
- references/ - documentation loaded into context as needed
- assets/ - files used in output (templates, images), not loaded into context
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""Example script for {skill_name} - replace or delete."""

def main():
    print("Example script for {skill_name}")

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference for {skill_title}

Replace with actual reference content or delete.
"""

EXAMPLE_ASSET = """Placeholder for asset files (templates, images, fonts). Replace or delete.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """Initialize a new skill directory with template SKILL.md."""
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"Error: {skill_dir} already exists")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)

    try:
        (skill_dir / 'SKILL.md').write_text(skill_content)

        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir()
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)

        references_dir = skill_dir / 'references'
        references_dir.mkdir()
        (references_dir / 'reference.md').write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir()
        (assets_dir / 'example.txt').write_text(EXAMPLE_ASSET)

    except Exception as e:
        print(f"Error: {e}")
        return None

    print(f"Created {skill_dir}")
    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path>")
        print("Example: init_skill.py my-skill --path ~/.config/opencode/skill")
        sys.exit(1)

    result = init_skill(sys.argv[1], sys.argv[3])
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
