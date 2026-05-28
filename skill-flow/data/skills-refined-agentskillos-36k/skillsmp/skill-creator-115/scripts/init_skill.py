#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path> [--resources <dirs>] [--examples]

Examples:
    init_skill.py my-skill --path skills/              # Only SKILL.md
    init_skill.py my-skill --path skills/ --resources scripts,references
    init_skill.py my-skill --path skills/ --resources scripts --examples
"""

import sys
import argparse
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: "TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it."
---

# {skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" → "Reading" → "Creating" → "Editing"
- Structure: ## Overview → ## Workflow Decision Tree → ## Step 1 → ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" → "Merge PDFs" → "Split PDFs" → "Extract Text"
- Structure: ## Overview → ## Quick Start → ## Task Category 1 → ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" → "Colors" → "Typography" → "Features"
- Structure: ## Overview → ## Guidelines → ## Specifications → ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" → numbered capability list
- Structure: ## Overview → ## Core Capabilities → ### 1. Feature → ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.

Example real scripts from other skills:
- pdf/scripts/fill_fillable_fields.py - Fills PDF form fields
- pdf/scripts/convert_pdf_to_images.py - Converts PDF pages to images
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

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within
the output the agent produces.

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg, .gif
- Fonts: .ttf, .otf, .woff, .woff2
- Boilerplate code: Project directories, starter files
- Data files: .csv, .json, .xml, .yaml

Note: This is a text placeholder. Actual assets can be any file type.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path, resources=None, examples=False):
    """
    Initialize a new skill directory with template SKILL.md.

    Args:
        skill_name: Name of the skill
        path: Path where the skill directory should be created
        resources: List of resource directories to create (scripts, references, assets)
        examples: Whether to create example files in resource directories

    Returns:
        Path to created skill directory, or None if error
    """
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Create SKILL.md from template
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ Created SKILL.md")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    # Create resource directories only if requested
    if resources:
        try:
            if 'scripts' in resources:
                scripts_dir = skill_dir / 'scripts'
                scripts_dir.mkdir(exist_ok=True)
                print("✅ Created scripts/")
                if examples:
                    example_script = scripts_dir / 'example.py'
                    example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
                    example_script.chmod(0o755)
                    print("   └── Added example.py")

            if 'references' in resources:
                references_dir = skill_dir / 'references'
                references_dir.mkdir(exist_ok=True)
                print("✅ Created references/")
                if examples:
                    example_reference = references_dir / 'api_reference.md'
                    example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
                    print("   └── Added api_reference.md")

            if 'assets' in resources:
                assets_dir = skill_dir / 'assets'
                assets_dir.mkdir(exist_ok=True)
                print("✅ Created assets/")
                if examples:
                    example_asset = assets_dir / 'example_asset.txt'
                    example_asset.write_text(EXAMPLE_ASSET)
                    print("   └── Added example_asset.txt")
        except Exception as e:
            print(f"❌ Error creating resource directories: {e}")
            return None

    print(f"\n✅ Skill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items")
    if resources:
        print("2. Customize or delete the example files as needed")
    print("3. Run quick_validate.py when ready to check the skill structure")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a new skill from template',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-skill --path skills/              # Only SKILL.md
  %(prog)s my-skill --path skills/ --resources scripts,references
  %(prog)s my-skill --path skills/ --resources scripts --examples

Skill name requirements:
  - Hyphen-case identifier (e.g., 'data-analyzer')
  - Lowercase letters, digits, and hyphens only
  - Max 64 characters
  - Must match directory name exactly
"""
    )
    parser.add_argument('skill_name', help='Name of the skill to create')
    parser.add_argument('--path', required=True, help='Directory where the skill will be created')
    parser.add_argument('--resources', help='Comma-separated list of directories to create: scripts,references,assets')
    parser.add_argument('--examples', action='store_true', help='Add example files in resource directories (requires --resources)')

    args = parser.parse_args()

    # Parse resources
    resources = None
    if args.resources:
        resources = [r.strip() for r in args.resources.split(',')]
        valid_resources = {'scripts', 'references', 'assets'}
        invalid = set(resources) - valid_resources
        if invalid:
            print(f"❌ Error: Invalid resource types: {', '.join(invalid)}")
            print(f"   Valid options: {', '.join(valid_resources)}")
            sys.exit(1)

    # Warn if --examples without --resources
    if args.examples and not args.resources:
        print("⚠️  Warning: --examples has no effect without --resources")

    print(f"🚀 Initializing skill: {args.skill_name}")
    print(f"   Location: {args.path}")
    if resources:
        print(f"   Resources: {', '.join(resources)}")
    if args.examples:
        print(f"   Examples: enabled")
    print()

    result = init_skill(args.skill_name, args.path, resources, args.examples)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
