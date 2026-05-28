#!/usr/bin/env python3
"""Migrate existing CLAUDE.md and README.md files to include YAML frontmatter."""

import re
import sys
from pathlib import Path


def has_yaml_frontmatter(content: str) -> bool:
    """
    Check if content has YAML frontmatter.

    Args:
        content: File content

    Returns:
        True if content starts with YAML frontmatter
    """
    return content.strip().startswith("---")


def extract_frontmatter(content: str) -> tuple[str | None, str]:
    """
    Extract YAML frontmatter and body from content.

    Args:
        content: File content

    Returns:
        Tuple of (frontmatter, body) or (None, content) if no frontmatter
    """
    if not has_yaml_frontmatter(content):
        return None, content

    # Match frontmatter pattern: ---\n...content...\n---\n
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)

    return None, content


def get_child_directories(dir_path: Path) -> list[str]:
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


def format_yaml_list(items: list[str], indent: int = 2) -> str:
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


def infer_purpose_from_content(content: str, dir_name: str, is_archived: bool) -> str:
    """
    Infer purpose from existing content.

    Args:
        content: File content
        dir_name: Directory name
        is_archived: True if this is an ARCHIVED directory

    Returns:
        Purpose string
    """
    if is_archived:
        return f"Archive of deprecated files from {dir_name}"

    # Try to extract from existing "## Purpose" section
    purpose_match = re.search(r"## Purpose\n\n(.+?)(?:\n\n##|\Z)", content, re.DOTALL)
    if purpose_match:
        purpose = purpose_match.group(1).strip()
        # Clean up template text
        if not purpose.startswith("["):
            return purpose

    return f"Context-specific guidance for {dir_name}"


def infer_related_skills(content: str, is_archived: bool) -> list[str]:
    """
    Infer related skills from existing content.

    Args:
        content: File content
        is_archived: True if this is an ARCHIVED directory

    Returns:
        List of related skills
    """
    if is_archived:
        return ["workflow-utilities"]

    # Try to extract from existing "## Related Skills" section
    skills_match = re.search(r"## Related Skills\n\n(.+?)(?:\n\n##|\Z)", content, re.DOTALL)
    if skills_match:
        skills_text = skills_match.group(1).strip()
        # Extract skill names (lines starting with -)
        skills = []
        for line in skills_text.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                skill = line.lstrip("- ").strip()
                if skill:
                    skills.append(skill)
        if skills:
            return skills

    return ["workflow-orchestrator", "workflow-utilities"]


def migrate_claude_md(file_path: Path, dry_run: bool = False) -> bool:
    """
    Migrate CLAUDE.md file to include YAML frontmatter.

    Args:
        file_path: Path to CLAUDE.md file
        dry_run: If True, only print what would be done

    Returns:
        True if file was migrated
    """
    if not file_path.exists():
        return False

    content = file_path.read_text()

    # Check if already has frontmatter
    if has_yaml_frontmatter(content):
        print(f"  ⊘ {file_path} (already has frontmatter)")
        return False

    dir_path = file_path.parent

    # Calculate relative directory path from repository root
    try:
        repo_root = dir_path
        while repo_root.parent != repo_root:
            if (repo_root / ".git").exists():
                break
            repo_root = repo_root.parent
        relative_dir = dir_path.relative_to(repo_root)
    except ValueError:
        relative_dir = dir_path

    # Determine if this is an ARCHIVED directory
    is_archived = dir_path.name == "ARCHIVED"

    # Determine parent
    parent_claude = "../CLAUDE.md" if dir_path.parent != dir_path and (dir_path.parent / "CLAUDE.md").exists() else None

    # Get children
    child_dirs = get_child_directories(dir_path)
    children_yaml = format_yaml_list(child_dirs) if child_dirs else " []"

    # Infer purpose and related skills from content
    purpose = infer_purpose_from_content(content, dir_path.parent.name if is_archived else dir_path.name, is_archived)
    related_skills = infer_related_skills(content, is_archived)
    skills_yaml = format_yaml_list(related_skills)

    # Build frontmatter
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

    # Update "Related Documentation" section if it doesn't exist
    if "## Related Documentation" not in content:
        # Insert before "## Related Skills" if it exists, otherwise at the end
        if "## Related Skills" in content:
            content = content.replace(
                "## Related Skills",
                """## Related Documentation

- **[README.md](README.md)** - Human-readable documentation for this directory
"""
                + (f"- **[{parent_claude}]({parent_claude})** - Parent directory\n\n" if parent_claude else "\n")
                + ("**Child Directories:**\n" + "\n".join(f"- **[{child}]({child})**" for child in child_dirs) + "\n\n" if child_dirs else "")
                + "## Related Skills",
            )
        else:
            # Add at the end
            related_doc = "\n## Related Documentation\n\n- **[README.md](README.md)** - Human-readable documentation for this directory\n"
            if parent_claude:
                related_doc += f"- **[{parent_claude}]({parent_claude})** - Parent directory\n"
            if child_dirs:
                related_doc += "\n**Child Directories:**\n" + "\n".join(f"- **[{child}]({child})**" for child in child_dirs) + "\n"
            content += related_doc

    new_content = frontmatter + content

    if dry_run:
        print(f"  ✓ {file_path} (would add frontmatter)")
    else:
        file_path.write_text(new_content)
        print(f"  ✓ {file_path}")

    return True


def migrate_readme_md(file_path: Path, dry_run: bool = False) -> bool:
    """
    Migrate README.md file to include YAML frontmatter.

    Args:
        file_path: Path to README.md file
        dry_run: If True, only print what would be done

    Returns:
        True if file was migrated
    """
    if not file_path.exists():
        return False

    content = file_path.read_text()

    # Check if already has frontmatter
    if has_yaml_frontmatter(content):
        print(f"  ⊘ {file_path} (already has frontmatter)")
        return False

    dir_path = file_path.parent

    # Calculate relative directory path from repository root
    try:
        repo_root = dir_path
        while repo_root.parent != repo_root:
            if (repo_root / ".git").exists():
                break
            repo_root = repo_root.parent
        relative_dir = dir_path.relative_to(repo_root)
    except ValueError:
        relative_dir = dir_path

    # Determine if this is an ARCHIVED directory
    is_archived = dir_path.name == "ARCHIVED"

    # Extract title from first # heading
    title_match = re.match(r"^# (.+)$", content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = "Archived Files" if is_archived else dir_path.name.replace("-", " ").replace("_", " ").title()

    # Determine parent
    parent_readme = "../README.md" if dir_path.parent != dir_path and (dir_path.parent / "README.md").exists() else None

    # Get children
    child_dirs = get_child_directories(dir_path)
    readme_children = [child.replace("CLAUDE.md", "README.md") for child in child_dirs]
    children_readme_yaml = format_yaml_list(readme_children) if readme_children else " []"

    # Build frontmatter
    frontmatter = f"""---
type: directory-documentation
directory: {relative_dir}
title: {title}
sibling_claude: CLAUDE.md
parent: {parent_readme or "null"}
children:{children_readme_yaml}
---

"""

    # Update "Related Documentation" section if it doesn't exist
    if "## Related Documentation" not in content:
        related_doc = "\n## Related Documentation\n\n- **[CLAUDE.md](CLAUDE.md)** - Context for Claude Code\n"
        if parent_readme:
            related_doc += f"- **[{parent_readme}]({parent_readme})** - Parent directory documentation\n"
        content += related_doc

    new_content = frontmatter + content

    if dry_run:
        print(f"  ✓ {file_path} (would add frontmatter)")
    else:
        file_path.write_text(new_content)
        print(f"  ✓ {file_path}")

    return True


def migrate_directory(directory: Path, dry_run: bool = False) -> tuple[int, int]:
    """
    Migrate all CLAUDE.md and README.md files in directory tree.

    Args:
        directory: Root directory to migrate
        dry_run: If True, only print what would be done

    Returns:
        Tuple of (migrated_count, skipped_count)
    """
    migrated = 0
    skipped = 0

    # Find all CLAUDE.md files
    print("\nMigrating CLAUDE.md files:")
    for claude_md in sorted(directory.rglob("CLAUDE.md")):
        if migrate_claude_md(claude_md, dry_run):
            migrated += 1
        else:
            skipped += 1

    # Find all README.md files
    print("\nMigrating README.md files:")
    for readme_md in sorted(directory.rglob("README.md")):
        # Skip root README.md (it's different)
        if readme_md.parent == directory:
            continue
        if migrate_readme_md(readme_md, dry_run):
            migrated += 1
        else:
            skipped += 1

    return migrated, skipped


if __name__ == "__main__":
    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    directory = Path.cwd()

    if dry_run:
        print("DRY RUN MODE - No files will be modified\n")

    print(f"Migrating directory: {directory}")

    migrated, skipped = migrate_directory(directory, dry_run)

    print(f"\n{'Would migrate' if dry_run else 'Migrated'}: {migrated} files")
    print(f"Skipped: {skipped} files")

    if dry_run:
        print("\nRun without --dry-run to apply changes")
