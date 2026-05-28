#!/usr/bin/env python3
"""
Scaffolds a new Agent Skill directory structure.

Usage:
    python scaffold.py <skill-name> "<description>"
    python scaffold.py api-client "Makes HTTP requests to backend APIs with retry logic"

Options:
    --output-dir    Base directory for skills (default: .claude/skills)
    --with-scripts  Include scripts/ directory
    --with-refs     Include references/ directory
    --full          Include all optional directories
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime


SKILL_TEMPLATE = '''---
name: {name}
description: {description}
license: MIT
metadata:
  version: "1.0"
  author: {author}
  created: "{created}"
---

# {title}

{description}

## When to Use

- [Describe trigger condition 1]
- [Describe trigger condition 2]

## Process

1. [Step one]
2. [Step two]
3. [Step three]

## Examples

### Example 1: [Scenario]

```
[Input/command example]
```

Expected output:
```
[Output example]
```

## Guidelines

- [Guideline 1]
- [Guideline 2]
- [Guideline 3]

## Related Skills

- [List related skills if any]
'''


def validate_name(name: str) -> tuple[bool, str]:
    """Validate skill name against Agent Skills spec."""
    if not name:
        return False, "Name cannot be empty"
    
    if len(name) > 64:
        return False, f"Name too long ({len(name)} chars): maximum 64"
    
    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', name):
        return False, "Name must be lowercase letters, numbers, hyphens; cannot start/end with hyphen"
    
    return True, ""


def scaffold_skill(
    name: str,
    description: str,
    output_dir: Path,
    with_scripts: bool = False,
    with_refs: bool = False,
    author: str = "your-name"
) -> Path:
    """
    Create a new skill directory structure.
    
    Returns the path to the created skill directory.
    """
    # Validate name
    valid, error = validate_name(name)
    if not valid:
        raise ValueError(f"Invalid skill name: {error}")
    
    # Validate description
    if not description:
        raise ValueError("Description cannot be empty")
    if len(description) > 1024:
        raise ValueError(f"Description too long ({len(description)} chars): maximum 1024")
    
    # Create skill directory
    skill_dir = output_dir / name
    if skill_dir.exists():
        raise FileExistsError(f"Skill directory already exists: {skill_dir}")
    
    skill_dir.mkdir(parents=True)
    
    # Generate title from name
    title = name.replace('-', ' ').title()
    
    # Create SKILL.md
    skill_content = SKILL_TEMPLATE.format(
        name=name,
        description=description,
        title=title,
        author=author,
        created=datetime.now().strftime("%Y-%m-%d")
    )
    
    (skill_dir / "SKILL.md").write_text(skill_content)
    
    # Create optional directories
    if with_scripts:
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()
        
        # Create placeholder script
        placeholder = scripts_dir / "helper.py"
        placeholder.write_text('''#!/usr/bin/env python3
"""
Helper script for {name} skill.

Usage:
    python helper.py [args]
"""

import sys

def main():
    print("Hello from {name} helper script!")
    print(f"Arguments: {{sys.argv[1:]}}")

if __name__ == "__main__":
    main()
'''.format(name=name))
    
    if with_refs:
        refs_dir = skill_dir / "references"
        refs_dir.mkdir()
        
        # Create placeholder reference
        placeholder = refs_dir / "DETAILS.md"
        placeholder.write_text(f'''# {title} - Detailed Reference

This file contains detailed documentation that the agent loads on-demand.

## Section 1

[Add detailed content here]

## Section 2

[Add more content here]
''')
    
    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description='Scaffold a new Agent Skill directory structure'
    )
    parser.add_argument(
        'name',
        help='Skill name (lowercase, hyphens, e.g., "api-client")'
    )
    parser.add_argument(
        'description',
        help='Skill description (what it does and when to use it)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('.claude/skills'),
        help='Base directory for skills (default: .claude/skills)'
    )
    parser.add_argument(
        '--with-scripts',
        action='store_true',
        help='Include scripts/ directory with placeholder'
    )
    parser.add_argument(
        '--with-refs',
        action='store_true',
        help='Include references/ directory with placeholder'
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Include all optional directories'
    )
    parser.add_argument(
        '--author',
        default='your-name',
        help='Author name for metadata'
    )
    
    args = parser.parse_args()
    
    # --full enables all optional dirs
    with_scripts = args.with_scripts or args.full
    with_refs = args.with_refs or args.full
    
    try:
        skill_dir = scaffold_skill(
            name=args.name,
            description=args.description,
            output_dir=args.output_dir,
            with_scripts=with_scripts,
            with_refs=with_refs,
            author=args.author
        )
        
        print(f"✅ Created skill: {skill_dir}")
        print(f"\nFiles created:")
        for f in sorted(skill_dir.rglob('*')):
            if f.is_file():
                print(f"   {f.relative_to(skill_dir.parent.parent.parent)}")
        
        print(f"\nNext steps:")
        print(f"  1. Edit {skill_dir}/SKILL.md with your instructions")
        print(f"  2. Validate: python .claude/skills/skill-foundry/scripts/validate.py {skill_dir}/SKILL.md")
        print(f"  3. Mirror to .github/skills: bash scripts/install.sh")
        
    except (ValueError, FileExistsError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
