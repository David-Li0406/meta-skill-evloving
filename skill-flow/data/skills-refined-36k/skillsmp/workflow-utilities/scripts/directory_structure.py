#!/usr/bin/env python3
"""Create standard directory structure with CLAUDE.md, README.md, ARCHIVED/."""

import sys
from pathlib import Path


def get_child_directories(dir_path):
    """
    Get list of child directories that have CLAUDE.md files.

    Args:
        dir_path: Path to directory

    Returns:
        List of relative paths to child CLAUDE.md files
    """
    children = []
    if not dir_path.exists():
        return children

    for child in sorted(dir_path.iterdir()):
        if child.is_dir() and (child / "CLAUDE.md").exists():
            children.append(f"{child.name}/CLAUDE.md")

    return children


def format_yaml_list(items, indent=2):
    """
    Format list items for YAML frontmatter.

    Args:
        items: List of items to format
        indent: Number of spaces for indentation

    Returns:
        Formatted YAML list string
    """
    if not items:
        return " []"

    spaces = " " * indent
    return "\n" + "\n".join(f"{spaces}- {item}" for item in items)


def create_directory_structure(directory, is_archived=False):
    """
    Create standard directory structure with YAML frontmatter.

    Args:
        directory: Path to directory
        is_archived: True if this IS an ARCHIVED directory

    Creates:
        - CLAUDE.md (with YAML frontmatter and cross-references)
        - README.md (with YAML frontmatter and cross-references)
        - ARCHIVED/ (unless is_archived=True)
    """
    dir_path = Path(directory).resolve()
    dir_path.mkdir(parents=True, exist_ok=True)

    dir_name = dir_path.name

    # Calculate relative directory path from repository root
    try:
        # Find repository root (has .git directory)
        repo_root = dir_path
        while repo_root.parent != repo_root:
            if (repo_root / ".git").exists():
                break
            repo_root = repo_root.parent

        relative_dir = dir_path.relative_to(repo_root)
    except ValueError:
        # Fallback if we can't find repo root
        relative_dir = dir_path

    # Determine parent paths
    parent_claude = "../CLAUDE.md" if dir_path.parent != dir_path else None
    parent_readme = "../README.md" if dir_path.parent != dir_path else None

    # Get children (will be populated after ARCHIVED is created)
    child_dirs = []
    if not is_archived:
        child_dirs.append("ARCHIVED/CLAUDE.md")

    # Scan for existing child directories
    for child in sorted(dir_path.iterdir()):
        if child.is_dir() and child.name != "ARCHIVED" and (child / "CLAUDE.md").exists():
            child_dirs.append(f"{child.name}/CLAUDE.md")

    # Create CLAUDE.md
    claude_md = dir_path / "CLAUDE.md"
    if not claude_md.exists():
        if is_archived:
            context_type = "Archived Content"
            purpose = f"Archive of deprecated files from {dir_path.parent.name}"
            related_skills = ["workflow-utilities"]
        else:
            context_type = dir_name
            purpose = f"Context-specific guidance for {dir_name}"
            related_skills = ["workflow-orchestrator", "workflow-utilities"]

        # Build children section
        children_yaml = format_yaml_list(child_dirs) if child_dirs else "[]"

        # Build related skills section
        skills_yaml = format_yaml_list(related_skills)

        frontmatter = f"""---
type: claude-context
directory: {relative_dir}
purpose: {purpose}
parent: {parent_claude or "null"}
sibling_readme: README.md
children:{children_yaml}
related_skills:{skills_yaml}
---

"""

        body = f"""# Claude Code Context: {context_type}

## Purpose

{purpose}

## Directory Structure

[Describe the organization of files in this directory]

## Files in This Directory

[List key files and their purposes]

## Usage

[How to work with code/content in this directory]

## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
"""

        if parent_claude:
            # Determine parent directory name
            parent_dir_name = dir_path.parent.name.replace("-", " ").replace("_", " ").title()
            body += f"- **[{parent_claude}]({parent_claude})** - Parent directory: {parent_dir_name}\n"

        if child_dirs:
            body += "\n**Child Directories:**\n"
            for child_path in child_dirs:
                child_name = child_path.split("/")[0].replace("-", " ").replace("_", " ").title()
                body += f"- **[{child_path}]({child_path})** - {child_name}\n"

        body += """
## Related Skills

"""
        for skill in related_skills:
            body += f"- {skill}\n"

        claude_md.write_text(frontmatter + body)
        print(f"✓ Created {claude_md}")

    # Create README.md
    readme_md = dir_path / "README.md"
    if not readme_md.exists():
        if is_archived:
            title = "Archived Files"
            overview = "Archive of deprecated files that are no longer in active use."
        else:
            title = dir_name.replace("-", " ").replace("_", " ").title()
            overview = f"Documentation for {dir_name}"

        # Build children section for README
        readme_children = [child.replace("CLAUDE.md", "README.md") for child in child_dirs]
        children_readme_yaml = format_yaml_list(readme_children) if readme_children else "[]"

        frontmatter = f"""---
type: directory-documentation
directory: {relative_dir}
title: {title}
sibling_claude: CLAUDE.md
parent: {parent_readme or "null"}
children:{children_readme_yaml}
---

"""

        body = f"""# {title}

## Overview

{overview}

## Contents

[Describe the contents of this directory]

## Structure

[Explain the organization and key files]

## Usage

[How to use the resources in this directory]

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Context for Claude Code
"""

        if parent_readme:
            body += f"- **[{parent_readme}]({parent_readme})** - Parent directory documentation\n"

        readme_md.write_text(frontmatter + body)
        print(f"✓ Created {readme_md}")

    # Create ARCHIVED/ subdirectory (unless this IS archived)
    if not is_archived:
        archived_dir = dir_path / "ARCHIVED"
        archived_dir.mkdir(exist_ok=True)

        # Recursively create structure for ARCHIVED
        create_directory_structure(archived_dir, is_archived=True)

    print(f"✓ Directory structure complete: {dir_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: directory_structure.py <directory>")
        print("Example: directory_structure.py planning/my-feature")
        sys.exit(1)

    create_directory_structure(sys.argv[1])
