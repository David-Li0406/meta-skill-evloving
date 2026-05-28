#!/usr/bin/env python3
"""
Skill Index Updater - Regenerate skill indexes for IDEs without native skill support.

This script scans skill directories and updates indexes in three locations:
- Global skills: Updated in ~/.kiro/steering/global.md (if Kiro installed)
- Global skills: Updated in ~/Documents/Cline/Rules/cline_overview.md (if Cline installed)
- Local skills: Updated in AGENTS.md (only when NOT in home directory)

Architecture Note:
    - Global skills: ~/.claude/skills/ (available across all repos)
    - Local skills: .claude/skills/ in the current repo (project-specific)
    - When working from ~/, only global skills exist (no local skills)

Usage:
    python update_skill_index.py
    python update_skill_index.py --dry-run

Requirements:
    - Python 3.8+
    - PyYAML (pip install pyyaml) - optional, falls back to regex parsing
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Try PyYAML, fall back to regex parsing if unavailable
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def parse_yaml_fallback(text: str) -> Optional[Dict]:
    """Simple regex-based YAML parser for basic key: value frontmatter."""
    result = {}
    for line in text.strip().split("\n"):
        match = re.match(r'^(\w+):\s*(.+)$', line.strip())
        if match:
            result[match.group(1)] = match.group(2).strip()
    return result if result else None


# Paths
HOME_DIR = Path.home()
GLOBAL_SKILLS_DIR = HOME_DIR / ".claude" / "skills"
KIRO_GLOBAL_MD = HOME_DIR / ".kiro" / "steering" / "global.md"
CLINE_OVERVIEW_MD = HOME_DIR / "Documents" / "Cline" / "Rules" / "cline_overview.md"

# Markers for the index sections
GLOBAL_INDEX_START = "## Available Global Skills Index"
LOCAL_INDEX_START = "## Available Local Skills Index"
INDEX_END = "---"


def find_repo_root() -> Optional[Path]:
    """Find the repository root by looking for .git directory."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".git").exists():
            return parent
    return None


def is_home_directory() -> bool:
    """Check if we're working from the home directory."""
    cwd = Path.cwd().resolve()
    home = HOME_DIR.resolve()
    return cwd == home


def parse_frontmatter(skill_path: Path) -> Optional[Dict]:
    """
    Parse YAML frontmatter from a SKILL.md file.

    Args:
        skill_path: Path to SKILL.md file

    Returns:
        Dict with 'name' and 'description', or None if parsing fails
    """
    try:
        content = skill_path.read_text(encoding="utf-8")
    except (IOError, OSError) as e:
        print(f"  Warning: Cannot read {skill_path}: {e}", file=sys.stderr)
        return None

    # Match frontmatter between --- markers
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        print(f"  Warning: No frontmatter found in {skill_path}", file=sys.stderr)
        return None

    # Parse YAML (with fallback if PyYAML unavailable)
    if YAML_AVAILABLE:
        try:
            frontmatter = yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            print(f"  Warning: Invalid YAML in {skill_path}: {e}", file=sys.stderr)
            return None
    else:
        frontmatter = parse_yaml_fallback(match.group(1))
        if not frontmatter:
            print(f"  Warning: Could not parse frontmatter in {skill_path}", file=sys.stderr)
            return None

    if not frontmatter or "name" not in frontmatter or "description" not in frontmatter:
        print(f"  Warning: Missing name/description in {skill_path}", file=sys.stderr)
        return None

    return {
        "name": frontmatter["name"],
        "description": frontmatter["description"],
        "folder": skill_path.parent.name,
    }


def scan_skills_dir(skills_dir: Path, path_prefix: str) -> List[Dict]:
    """
    Scan a skill directory and extract frontmatter.

    Args:
        skills_dir: Path to the skills directory to scan
        path_prefix: Path prefix for display (e.g., ".claude/skills")

    Returns:
        List of skill dicts sorted by name
    """
    skills = []

    if not skills_dir or not skills_dir.exists():
        return skills

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith("."):
            continue

        # A directory is only a skill if it contains SKILL.md
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        skill_data = parse_frontmatter(skill_file)
        if skill_data:
            skill_data["path_prefix"] = path_prefix
            skills.append(skill_data)

    return sorted(skills, key=lambda s: s["name"])


def generate_global_index(skills: List[Dict]) -> str:
    """
    Generate the index section for global.md (Kiro format).

    Args:
        skills: List of skill dicts

    Returns:
        Formatted string matching global.md format
    """
    lines = [
        GLOBAL_INDEX_START,
        "*(Auto-generated - do not edit manually)*",
        "",
    ]

    for skill in skills:
        lines.append(f"  path: {skill['path_prefix']}/{skill['folder']}")
        lines.append(f"  name: {skill['name']}")
        lines.append(f"  description: {skill['description']}")
        lines.append("---")

    return "\n".join(lines)


def generate_local_index(skills: List[Dict]) -> str:
    """
    Generate the index section for AGENTS.md (markdown format).

    Args:
        skills: List of local skill dicts

    Returns:
        Formatted markdown string
    """
    lines = [
        LOCAL_INDEX_START,
        "_This index is for IDEs that don't natively support skills (e.g., Gemini CLI, Kiro). Skip if your IDE reads SKILL.md directly._",
        "",
    ]

    for skill in skills:
        lines.append(f"- **Name:** `{skill['name']}`")
        lines.append(f"  - **Trigger:** {skill['description']}")
        lines.append(f"  - **Path:** `{skill['path_prefix']}/{skill['folder']}/SKILL.md`")
        lines.append("")

    return "\n".join(lines)


def update_file_index(file_path: Path, new_index: str, index_start: str, dry_run: bool = False) -> bool:
    """
    Update the index section in a file.

    Args:
        file_path: Path to the file to update
        new_index: New index content to insert
        index_start: The marker string that starts the index section
        dry_run: If True, print changes without writing

    Returns:
        True if successful, False otherwise
    """
    if not file_path.exists():
        print(f"Error: {file_path} not found", file=sys.stderr)
        return False

    content = file_path.read_text(encoding="utf-8")

    # Find the index section
    start_match = re.search(rf"^{re.escape(index_start)}.*$", content, re.MULTILINE)
    if not start_match:
        print(f"Error: '{index_start}' header not found in {file_path}", file=sys.stderr)
        print(f"  Tip: Add this line to your file: {index_start}", file=sys.stderr)
        return False

    # Find where the index section ends
    # The index contains skill entries. For global.md each ends with ---.
    # The section ends when we hit content that's not part of a skill entry.
    
    remaining_content = content[start_match.start():]
    lines = remaining_content.split('\n')
    
    end_char_pos = len(content)  # Default: replace to end of file
    current_pos = start_match.start()
    found_first_skill = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        line_start_pos = current_pos
        current_pos += len(line) + 1  # +1 for newline
        stripped = line.strip()
        
        # Skip header and auto-generated comment
        if i == 0 or stripped.startswith('*(Auto-generated') or stripped.startswith('_This index'):
            i += 1
            continue
        
        # Empty lines are ok within the index
        if stripped == '':
            i += 1
            continue
            
        # Skill entry indicators
        is_skill_content = (
            stripped.startswith('path:') or
            stripped.startswith('name:') or
            stripped.startswith('description:') or
            stripped.startswith('- **Name:**') or
            stripped.startswith('- **Trigger:**') or
            stripped.startswith('- **Path:**')
        )
        
        if is_skill_content:
            found_first_skill = True
            i += 1
            continue
        
        # --- separator within the index (between skills)
        if stripped == '---':
            # Check what comes after this separator
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            
            if j >= len(lines):
                # EOF after ---, this is the end
                end_char_pos = line_start_pos
                break
            
            next_content = lines[j].strip()
            is_next_skill = (
                next_content.startswith('path:') or
                next_content.startswith('name:') or
                next_content.startswith('- **Name:**')
            )
            
            if is_next_skill:
                # More skills follow, continue
                i += 1
                continue
            else:
                # Non-skill content after ---, index ends here
                end_char_pos = line_start_pos
                break
        
        # Any other content means end of index
        if found_first_skill:
            end_char_pos = line_start_pos
            break
        
        i += 1
    
    # Build new content
    remaining = content[end_char_pos:].lstrip('\n').lstrip('-').lstrip('\n')
    if remaining:
        new_content = content[:start_match.start()] + new_index + "\n\n" + remaining
    else:
        new_content = content[:start_match.start()] + new_index + "\n"

    if dry_run:
        print(f"\n=== DRY RUN: Would write to {file_path} ===")
        print(new_index)
        print("=== END ===\n")
        return True

    file_path.write_text(new_content, encoding="utf-8")
    return True


AGENTS_MD_TEMPLATE = """# Agents and Skills

This file documents the agents and skills available in this repository.

## Available Local Skills Index

---
"""


def init_agents_md(file_path: Path, dry_run: bool = False) -> bool:
    """Create AGENTS.md with default template."""
    if dry_run:
        print(f"\n=== DRY RUN: Would create {file_path} ===")
        print(AGENTS_MD_TEMPLATE)
        print("=== END ===\n")
        return True
    
    file_path.write_text(AGENTS_MD_TEMPLATE, encoding="utf-8")
    print(f"Created: {file_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Update skill indexes (global.md and AGENTS.md)"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be written without making changes"
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create AGENTS.md if it doesn't exist"
    )
    parser.add_argument(
        "--force-local",
        action="store_true",
        help="Force local skills update even if not in a git repository"
    )
    args = parser.parse_args()

    in_home = is_home_directory()
    repo_root = find_repo_root()
    cwd = Path.cwd()
    agents_md_exists = (cwd / "AGENTS.md").exists()
    
    # Determine what to update
    update_global = True  # Always update global skills
    # Update local if: not in home AND (in git repo OR AGENTS.md exists OR user forces it)
    update_local = not in_home and (repo_root is not None or agents_md_exists or args.force_local)
    
    print(f"Working directory: {Path.cwd()}")
    print(f"Home directory: {HOME_DIR}")
    print(f"In home directory: {in_home}")
    if repo_root:
        print(f"Repository root: {repo_root}")
    else:
        print(f"Repository root: Not detected")
    print(f"AGENTS.md exists: {agents_md_exists}")
    print()

    # === Update global skills in global.md ===
    print("=" * 60)
    print("GLOBAL SKILLS")
    print("=" * 60)
    
    print(f"Scanning global skills in: {GLOBAL_SKILLS_DIR}")
    global_skills = scan_skills_dir(GLOBAL_SKILLS_DIR, "~/.claude/skills")
    print(f"  Found {len(global_skills)} global skills")
    
    if global_skills:
        print("\n  Skills found:")
        for s in global_skills:
            print(f"    - {s['name']} ({s['folder']})")
        
        global_index = generate_global_index(global_skills)
        
        # Update Kiro global.md if it exists
        if KIRO_GLOBAL_MD.exists():
            if update_file_index(KIRO_GLOBAL_MD, global_index, GLOBAL_INDEX_START, dry_run=args.dry_run):
                if not args.dry_run:
                    print(f"\nUpdated: {KIRO_GLOBAL_MD}")
            else:
                print(f"\nFailed to update: {KIRO_GLOBAL_MD}", file=sys.stderr)
        else:
            print(f"\nSkipping Kiro: {KIRO_GLOBAL_MD.parent} not found (Kiro not installed)")
        
        # Update Cline overview.md if it exists
        if CLINE_OVERVIEW_MD.exists():
            if update_file_index(CLINE_OVERVIEW_MD, global_index, GLOBAL_INDEX_START, dry_run=args.dry_run):
                if not args.dry_run:
                    print(f"Updated: {CLINE_OVERVIEW_MD}")
            else:
                print(f"\nFailed to update: {CLINE_OVERVIEW_MD}", file=sys.stderr)
        else:
            print(f"Skipping Cline: {CLINE_OVERVIEW_MD.parent} not found (Cline not installed)")
    else:
        print("\nNo global skills found.")

    # === Update local skills in AGENTS.md (only if not in home directory) ===
    if update_local:
        print()
        print("=" * 60)
        print("LOCAL SKILLS")
        print("=" * 60)
        
        # Use repo_root if available, otherwise use current directory
        base_dir = repo_root if repo_root else cwd
        local_skills_dir = base_dir / ".claude" / "skills"
        agents_md = base_dir / "AGENTS.md"
        
        print(f"Scanning local skills in: {local_skills_dir}")
        local_skills = scan_skills_dir(local_skills_dir, ".claude/skills")
        print(f"  Found {len(local_skills)} local skills")
        
        if local_skills:
            print("\n  Skills found:")
            for s in local_skills:
                print(f"    - {s['name']} ({s['folder']})")
            
            local_index = generate_local_index(local_skills)
            
            # Check if AGENTS.md exists, offer to create if not
            if not agents_md.exists():
                if args.init:
                    if not init_agents_md(agents_md, args.dry_run):
                        sys.exit(1)
                else:
                    print(f"\nAGENTS.md not found at: {agents_md}")
                    response = input("Create it now? [Y/n]: ").strip().lower()
                    if response in ("", "y", "yes"):
                        if not init_agents_md(agents_md, args.dry_run):
                            sys.exit(1)
                    else:
                        print("Skipping local skills index update.")
                        return
            
            if agents_md.exists():
                if update_file_index(agents_md, local_index, LOCAL_INDEX_START, dry_run=args.dry_run):
                    if not args.dry_run:
                        print(f"\nUpdated: {agents_md}")
                else:
                    print(f"\nFailed to update: {agents_md}", file=sys.stderr)
        else:
            print("\nNo local skills found.")
    else:
        if in_home:
            print("\nSkipping local skills (working from home directory - no local skills exist)")
        elif not repo_root and not agents_md_exists and not args.force_local:
            print("\nSkipping local skills (not in a git repository and no AGENTS.md found)")
            print("  Tip: Use --force-local to update anyway, or create AGENTS.md first")

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if args.dry_run:
        print("Dry run complete. No changes made.")
    else:
        print("Index update complete.")


if __name__ == "__main__":
    main()
