#!/usr/bin/env python3
"""
Update project onboarding documentation
"""
import argparse
import os
import re
import sys
from pathlib import Path


def update_onboarding(project_root: str, section: str, content: str):
    """Update a section in onboarding"""
    
    onboarding_file = Path(project_root) / ".tmp" / ".serena-skills" / "onboarding.md"
    
    if not onboarding_file.exists():
        raise FileNotFoundError("Onboarding not found. Create it first with create_onboarding.py")
    
    current_content = onboarding_file.read_text(encoding='utf-8')
    
    # Find section heading
    section_pattern = re.compile(f'^## {re.escape(section)}$', re.MULTILINE)
    match = section_pattern.search(current_content)
    
    if not match:
        # Section doesn't exist, append it
        new_content = current_content.rstrip() + f"\n\n## {section}\n\n{content}\n"
    else:
        # Find next section or end of file
        next_section = re.search(r'^## ', current_content[match.end():], re.MULTILINE)
        
        if next_section:
            # Replace content until next section
            end_pos = match.end() + next_section.start()
            new_content = (
                current_content[:match.end()] +
                f"\n\n{content}\n\n" +
                current_content[end_pos:]
            )
        else:
            # Replace content until end of file
            new_content = current_content[:match.end()] + f"\n\n{content}\n"
    
    onboarding_file.write_text(new_content, encoding='utf-8')
    
    return f"Updated section '{section}' in onboarding"


def main():
    parser = argparse.ArgumentParser(description="Update project onboarding")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    parser.add_argument("--section", required=True, help="Section name")
    parser.add_argument("--content", required=True, help="New content for section")
    
    args = parser.parse_args()
    
    try:
        result = update_onboarding(args.project_root, args.section, args.content)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
