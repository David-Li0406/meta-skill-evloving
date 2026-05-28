#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> [--path <path>]

Examples:
    init_skill.py my-new-skill
    init_skill.py my-new-skill --path skills/public
"""

import sys
import argparse
from pathlib import Path

SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it.]
---

# {skill_title}

## Overview
[TODO: 1-2 sentences explaining what this skill enables]

## Implementation
[TODO: Add content here. See examples in existing skills]
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

Appropriate for: In-depth documentation, API references, or detailed information the Agent should reference.
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within the output the Agent produces.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created

    Returns:
        Path to created skill directory, or None if error
    """
    # Determine skill directory path
    # If path is just a directory, append skill_name
    # If path ends with skill_name, use it as is? 
    # The original script does: skill_dir = Path(path).resolve() / skill_name
    # We will stick to that convention: path is the PARENT directory.
    
    skill_dir = Path(path).resolve() / skill_name

    # Check if directory already exists
    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    # Create skill directory
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
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
        print("✅ Created SKILL.md")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    # Create resource directories with example files
    try:
        # Create scripts/ directory with example script
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ Created scripts/example.py")

        # Create references/ directory with example reference doc
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ Created references/api_reference.md")

        # Create assets/ directory with example asset placeholder
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ Created assets/example_asset.txt")
    except Exception as e:
        print(f"❌ Error creating resource directories: {e}")
        return None

    # Print next steps
    print(f"\\n✅ Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    print("2. Customize or delete the example files in scripts/, references/, and assets/")
    print(f"3. Run the validator: python .agent/skills/skill-creator/scripts/quick_validate.py {skill_dir}")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(description="Initialize a new skill.")
    parser.add_argument("skill_name", help="Name of the skill (hyphen-case, e.g. my-skill)")
    parser.add_argument("--path", default=".agent/skills", help="Parent directory for the skill (default: .agent/skills)")
    
    args = parser.parse_args()

    print(f"🚀 Initializing skill: {args.skill_name}")
    print(f"   Location: {args.path}")
    print()

    result = init_skill(args.skill_name, args.path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
