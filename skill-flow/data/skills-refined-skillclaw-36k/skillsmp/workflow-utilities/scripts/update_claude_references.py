#!/usr/bin/env python3
"""Update all CLAUDE.md files with cross-references to parent, children, and README."""

import sys
from pathlib import Path


def get_all_claude_files(root_dir: Path) -> list[Path]:
    """Find all CLAUDE.md files in the repository."""
    return sorted(root_dir.rglob("CLAUDE.md"))


def get_relative_path(from_file: Path, to_file: Path) -> str:
    """Get relative path from one file to another."""
    try:
        return str(to_file.relative_to(from_file.parent))
    except ValueError:
        # Files are in different trees, use .. to go up
        from_parts = from_file.parent.parts
        to_parts = to_file.parts

        # Find common ancestor
        common = 0
        for i, (a, b) in enumerate(zip(from_parts, to_parts)):
            if a == b:
                common = i + 1
            else:
                break

        # Go up from 'from' to common ancestor
        ups = len(from_parts) - common
        up_path = "../" * ups

        # Go down from common ancestor to 'to'
        down_path = "/".join(to_parts[common:])

        return up_path + down_path


def generate_cross_references(claude_file: Path, root_dir: Path) -> str:
    """Generate cross-reference section for a CLAUDE.md file."""

    dir_path = claude_file.parent
    refs = []

    # Reference to README.md in same directory
    readme = dir_path / "README.md"
    if readme.exists():
        refs.append("- **[README.md](README.md)** - Human-readable documentation for this directory")

    # Reference to parent CLAUDE.md (if not root)
    if dir_path != root_dir:
        parent_claude = dir_path.parent / "CLAUDE.md"
        if parent_claude.exists():
            rel_path = get_relative_path(claude_file, parent_claude)
            parent_name = dir_path.parent.name if dir_path.parent != root_dir else "Root"
            refs.append(f"- **[../{parent_claude.name}]({rel_path})** - Parent directory: {parent_name}")

    # References to child directories' CLAUDE.md files
    child_dirs = sorted([d for d in dir_path.iterdir() if d.is_dir() and not d.name.startswith(".")])
    child_claudes = []

    for child_dir in child_dirs:
        child_claude = child_dir / "CLAUDE.md"
        if child_claude.exists():
            rel_path = get_relative_path(claude_file, child_claude)
            child_claudes.append(f"- **[{child_dir.name}/CLAUDE.md]({rel_path})** - {child_dir.name.replace('-', ' ').replace('_', ' ').title()}")

    if child_claudes:
        refs.append("")
        refs.append("**Child Directories:**")
        refs.extend(child_claudes)

    if refs:
        section = "\n## Related Documentation\n\n"
        section += "\n".join(refs)
        section += "\n"
        return section

    return ""


def update_claude_file(claude_file: Path, root_dir: Path, dry_run: bool = False):
    """Update a CLAUDE.md file with cross-references."""

    content = claude_file.read_text(encoding="utf-8")

    # Remove existing "Related Documentation" section if present
    lines = content.split("\n")
    new_lines = []
    skip_section = False

    for line in lines:
        if line.startswith("## Related Documentation"):
            skip_section = True
            continue
        elif skip_section and line.startswith("## "):
            skip_section = False

        if not skip_section:
            new_lines.append(line)

    # Remove trailing empty lines
    while new_lines and not new_lines[-1].strip():
        new_lines.pop()

    # Generate new cross-references
    cross_refs = generate_cross_references(claude_file, root_dir)

    # Add cross-references before any existing "Related Skills" section or at the end
    final_content = "\n".join(new_lines)
    if "## Related Skills" in final_content:
        # Insert before Related Skills
        final_content = final_content.replace("## Related Skills", f"{cross_refs}\n## Related Skills")
    else:
        # Append at end
        final_content += f"\n{cross_refs}"

    if dry_run:
        print(f"\n{'=' * 60}")
        print(f"Would update: {claude_file.relative_to(root_dir)}")
        print(f"{'=' * 60}")
        print(cross_refs)
    else:
        claude_file.write_text(final_content, encoding="utf-8")
        print(f"✓ Updated {claude_file.relative_to(root_dir)}")


def main():
    """Update all CLAUDE.md files with cross-references."""

    dry_run = "--dry-run" in sys.argv

    root_dir = Path.cwd()

    # Find all CLAUDE.md files
    claude_files = get_all_claude_files(root_dir)

    print(f"Found {len(claude_files)} CLAUDE.md files")
    print()

    if dry_run:
        print("DRY RUN MODE - No files will be modified")
        print()

    # Update each file
    for claude_file in claude_files:
        update_claude_file(claude_file, root_dir, dry_run)

    print()
    print(f"✅ {'Would update' if dry_run else 'Updated'} {len(claude_files)} CLAUDE.md files")

    if dry_run:
        print()
        print("Run without --dry-run to apply changes")


if __name__ == "__main__":
    main()
