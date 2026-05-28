#!/usr/bin/env python3
"""
Load Skill Context - Preflight Context Loading Script

Outputs complete skill context for use in command preflight checks:
- Full SKILL.md content
- Complete frontmatter from all reference files
- All markdown headers from all reference files

Usage:
    python3 scripts/load_skill_context.py /path/to/skill-folder
    python3 scripts/load_skill_context.py ~/.claude/skills/creating-commands
"""

import sys
from pathlib import Path
import re
import yaml

def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return {}
    return {}

def extract_all_headers(content: str) -> list:
    """Extract all markdown headers (H1-H6) from content, excluding those inside code blocks."""
    header_pattern = r'^(#{1,6})\s+(.+)$'
    headers = []
    in_code_block = False

    for line in content.split('\n'):
        # Track code fence boundaries
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip headers inside code blocks
        if in_code_block:
            continue

        # Extract headers outside code blocks
        match = re.match(header_pattern, line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append((level, text))

    return headers

def load_skill_context(skill_path: str):
    """Load and display complete skill context."""
    skill_dir = Path(skill_path).resolve()

    if not skill_dir.exists():
        print(f"Error: Skill directory not found: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md not found in {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # Output full SKILL.md content
    print("=" * 80)
    print("SKILL.md")
    print("=" * 80)
    with open(skill_md, 'r', encoding='utf-8') as f:
        skill_content = f.read()
        print(skill_content)

    # Process reference files
    ref_dir = skill_dir / "references"
    if ref_dir.exists() and ref_dir.is_dir():
        ref_files = sorted([f for f in ref_dir.glob("*.md")])

        if ref_files:
            print("\n" + "=" * 80)
            print("REFERENCE FILES")
            print("=" * 80)

            for ref_file in ref_files:
                print(f"\n{'─' * 80}")
                print(f"File: references/{ref_file.name}")
                print('─' * 80)

                with open(ref_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Output complete frontmatter
                frontmatter = extract_frontmatter(content)
                if frontmatter:
                    print("\nFrontmatter:")
                    print("---")
                    print(yaml.dump(frontmatter, default_flow_style=False, sort_keys=False).strip())
                    print("---")
                else:
                    print("\nFrontmatter: None")

                # Output all headers
                headers = extract_all_headers(content)
                if headers:
                    print("\nTOC:")
                    for level, text in headers:
                        indent = "  " * (level - 1)
                        print(f"{indent}{'#' * level} {text}")
                else:
                    print("\nHeaders: None found")

    # List all other directories and their contents
    print("\n" + "=" * 80)
    print("OTHER DIRECTORIES & FILES")
    print("=" * 80)

    # Get all subdirectories except references (already processed)
    subdirs = sorted([d for d in skill_dir.iterdir()
                     if d.is_dir() and d.name not in ['references', '.git', '__pycache__']])

    for subdir in subdirs:
        all_files = sorted([f for f in subdir.rglob("*") if f.is_file()])
        if all_files:
            print(f"\n{subdir.name}/:")
            for file in all_files:
                rel_path = file.relative_to(subdir)
                # Show file type indicator
                if file.suffix == '.md':
                    print(f"  - {rel_path} (markdown)")
                elif file.suffix in ['.py', '.js', '.sh', '.rb']:
                    print(f"  - {rel_path} (script)")
                elif file.suffix in ['.yaml', '.yml', '.json', '.toml']:
                    print(f"  - {rel_path} (config)")
                else:
                    print(f"  - {rel_path}")

    print("\n" + "=" * 80)
    print("END OF SKILL CONTEXT")
    print("=" * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 load_skill_context.py /path/to/skill-folder", file=sys.stderr)
        print("\nExample:")
        print("  python3 scripts/load_skill_context.py ~/.claude/skills/creating-commands", file=sys.stderr)
        sys.exit(1)

    load_skill_context(sys.argv[1])
