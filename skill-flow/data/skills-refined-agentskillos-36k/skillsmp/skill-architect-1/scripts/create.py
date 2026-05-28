#!/usr/bin/env python3
"""
Skill Creation Script
Creates a new Agent Skill with the standard directory structure and template files
compliant with the Agent Skills specification.
"""

import os
import sys
import argparse
import re
from pathlib import Path

def validate_skill_name(name):
    """
    Validates the skill name according to the spec:
    - 1-64 characters
    - Lowercase alphanumeric and hyphens only
    - No leading/trailing hyphens
    - No consecutive hyphens
    """
    if not (1 <= len(name) <= 64):
        return False, "Length must be between 1 and 64 characters"
    
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Must contain only lowercase alphanumeric characters and hyphens"
        
    if name.startswith('-') or name.endswith('-'):
        return False, "Must not start or end with a hyphen"
        
    if '--' in name:
        return False, "Must not contain consecutive hyphens"
        
    return True, ""

def create_skill(name, description, output_dir, author="agent-starter", version="1.0"):
    """Creates the skill directory structure and files."""
    
    # Define paths
    base_path = Path(output_dir) / name
    
    if base_path.exists():
        print(f"Error: Directory {base_path} already exists")
        sys.exit(1)
        
    # Create directories
    dirs = [
        base_path,
        base_path / "scripts",
        base_path / "references",
        base_path / "assets"
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {d}")
        
    # Locate template file
    # Script is in scripts/, template is in assets/
    script_dir = Path(__file__).parent.resolve()
    template_path = script_dir.parent / "assets" / "SKILL_TEMPLATE.md"
    
    if template_path.exists():
        with open(template_path, "r") as f:
            template_content = f.read()
        print(f"Used template from: {template_path}")
    else:
        # Fallback template if file is missing
        print(f"Warning: Template not found at {template_path}. Using internal fallback.")
        template_content = """---
name: {name}
description: {description}
license: MIT
metadata:
  author: {author}
  version: {version}
allowed-tools: Bash(python:*) Read
---

# {title_name} Skill

{description}

## Purpose

Describe the specific problem this skill solves.

## Usage

Describe how to use this skill.
"""

    # Fill template
    title_name = name.replace('-', ' ').title()
    try:
        skill_md_content = template_content.format(
            name=name,
            description=description,
            title_name=title_name,
            author=author,
            version=version
        )
    except KeyError as e:
        print(f"Warning: Template key missing: {e}. Using raw template.")
        skill_md_content = template_content
    
    # Write SKILL.md
    skill_md_path = base_path / "SKILL.md"
    with open(skill_md_path, "w") as f:
        f.write(skill_md_content)
    print(f"Created template: {skill_md_path}")
    
    # Create a placeholder script
    script_path = base_path / "scripts" / "example.py"
    example_script_content = """#!/usr/bin/env python3
import sys

def main():
    try:
        # Example logic
        if len(sys.argv) > 1:
            print(f"Received argument: {sys.argv[1]}")
        else:
            print("Hello from the new skill!")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
    with open(script_path, "w") as f:
        f.write(example_script_content)
    print(f"Created placeholder script: {script_path}")
    
    # Make script executable
    os.chmod(script_path, 0o755)

def main():
    parser = argparse.ArgumentParser(description="Create a new Agent Skill")
    parser.add_argument("name", help="Name of the skill (kebab-case)")
    parser.add_argument("--description", "-d", default="A new agent skill", help="Description of the skill")
    parser.add_argument("--dir", default=".claude/skills", help="Parent directory for skills")
    
    args = parser.parse_args()
    
    # Validate name
    is_valid, error = validate_skill_name(args.name)
    if not is_valid:
        print(f"Invalid skill name '{args.name}': {error}")
        sys.exit(1)
        
    # Create skill
    # Assuming the script is run from project root, default dir is relative
    # If .claude/skills doesn't exist, we might want to check
    
    # Determine absolute path for output
    if os.path.isabs(args.dir):
        out_dir = Path(args.dir)
    else:
        out_dir = Path(os.getcwd()) / args.dir
        
    if not out_dir.exists():
        print(f"Warning: Target directory {out_dir} does not exist. Creating it.")
        out_dir.mkdir(parents=True, exist_ok=True)
        
    create_skill(args.name, args.description, out_dir)
    print(f"\nSuccess! Skill '{args.name}' created at {out_dir / args.name}")

if __name__ == "__main__":
    main()
