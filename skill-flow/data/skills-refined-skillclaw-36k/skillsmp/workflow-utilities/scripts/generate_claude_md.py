#!/usr/bin/env python3
"""Generate missing CLAUDE.md files for directory hierarchy.

This script scans the repository for directories missing CLAUDE.md files
and generates them with proper parent/child/sibling references.

Usage:
    python generate_claude_md.py [--dry-run] [--verbose]

Created: 2025-11-23
Purpose: Ensure complete AI navigation hierarchy
"""

import argparse
from pathlib import Path

# Repository root (detect from script location)
REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent

# Directories to skip
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules", ".tmp", ".uv", "dist", "build", ".coverage", "htmlcov", ".idea", ".vscode"}

# Directories that should have CLAUDE.md
TARGET_DIRS = [
    # Core structure
    ".claude",
    ".claude/commands",
    ".claude/commands/workflow",
    ".claude/skills",
    ".agents",
    # Documentation
    "docs",
    "docs/archived",
    "docs/reference",
    # Tests
    "tests",
    "tests/unit",
    "tests/contract",
    "tests/integration",
]

# Directory purposes (for generated content)
DIR_PURPOSES = {
    ".claude": "Claude Code configuration root containing commands, skills, and settings.",
    ".claude/commands": "Slash command definitions organized by category.",
    ".claude/commands/workflow": "7-phase workflow commands (/1_specify through /7_backmerge plus orchestrator).",
    ".claude/skills": "Modular skill implementations (9 skills) for workflow automation.",
    ".agents": "Auto-synced mirror of .claude/skills/ for cross-tool AI compatibility. Do not edit directly.",
    "docs": "Documentation root for guides, references, and archives.",
    "docs/archived": "Compressed and deprecated documentation.",
    "docs/reference": "Workflow reference documentation and quick-reference guides.",
    "tests": "Test suite root with unit, contract, and integration tests.",
    "tests/unit": "Unit tests for individual components and functions.",
    "tests/contract": "Contract tests verifying API boundaries and interfaces.",
    "tests/integration": "Integration tests for end-to-end workflow verification.",
    "specs": "Feature specifications with design artifacts.",
    "contracts": "API contracts and interface definitions for this feature.",
    "scripts": "Executable Python scripts for this skill.",
    "templates": "Markdown and code templates for this skill.",
    "schemas": "Data schemas and validation definitions.",
}

TEMPLATE = """---
type: claude-context
directory: {directory}
purpose: {purpose}
parent: {parent}
sibling_readme: {sibling_readme}
children:
{children}
---

# Claude Code Context: {name}

## Purpose

{purpose}

## Contents

{contents}

## Related

{related}
"""


def get_purpose(dir_path: Path, dir_name: str) -> str:
    """Get purpose description for a directory."""
    rel_path = str(dir_path.relative_to(REPO_ROOT))

    # Check exact match first
    if rel_path in DIR_PURPOSES:
        return DIR_PURPOSES[rel_path]

    # Check by directory name
    if dir_name in DIR_PURPOSES:
        return DIR_PURPOSES[dir_name]

    # Check if it's a spec directory
    if rel_path.startswith("specs/") and "/" in rel_path[6:]:
        # It's a subdirectory of a spec
        subdir = rel_path.split("/")[-1]
        if subdir in DIR_PURPOSES:
            return DIR_PURPOSES[subdir]

    if rel_path.startswith("specs/"):
        spec_name = dir_name.replace("-", " ").title()
        return f"Feature specification for {spec_name}."

    # Default purpose
    return f"{dir_name.replace('-', ' ').replace('_', ' ').title()} directory."


def find_children(dir_path: Path) -> list[str]:
    """Find child directories that have or should have CLAUDE.md."""
    children = []

    if not dir_path.exists():
        return children

    for item in sorted(dir_path.iterdir()):
        if item.is_dir() and item.name not in SKIP_DIRS:
            # Check if child has CLAUDE.md or is a target directory
            if (item / "CLAUDE.md").exists():
                children.append(f"{item.name}/CLAUDE.md")
            elif any(item.name == d.split("/")[-1] for d in TARGET_DIRS):
                children.append(f"{item.name}/CLAUDE.md")
            elif item.name in ("scripts", "templates", "contracts", "schemas", "ARCHIVED"):
                children.append(f"{item.name}/CLAUDE.md")

    return children


def find_contents(dir_path: Path) -> str:
    """Generate contents description for a directory."""
    if not dir_path.exists():
        return "*(Directory will be created)*"

    items = []
    files = []
    dirs = []

    for item in sorted(dir_path.iterdir()):
        if item.name.startswith(".") and item.name not in (".claude", ".agents"):
            continue
        if item.name in SKIP_DIRS:
            continue

        if item.is_dir():
            dirs.append(f"- `{item.name}/` - Subdirectory")
        elif item.suffix == ".md" and item.name != "CLAUDE.md":
            dirs.append(f"- `{item.name}` - Documentation")
        elif item.suffix == ".py":
            files.append(f"- `{item.name}` - Python script")
        elif item.suffix in (".json", ".yaml", ".yml"):
            files.append(f"- `{item.name}` - Configuration")

    items = dirs[:5] + files[:5]  # Limit to 10 items

    if not items:
        return "*(Empty or contains only hidden files)*"

    if len(dirs) + len(files) > 10:
        items.append(f"- *...and {len(dirs) + len(files) - 10} more items*")

    return "\n".join(items)


def generate_claude_md(dir_path: Path, dry_run: bool = False, verbose: bool = False) -> bool:
    """Generate CLAUDE.md for a directory."""
    rel_path = dir_path.relative_to(REPO_ROOT)
    dir_name = dir_path.name

    # Determine parent
    parent_claude = dir_path.parent / "CLAUDE.md"
    if parent_claude.exists() or dir_path.parent != REPO_ROOT:
        parent = "../CLAUDE.md"
    else:
        parent = "null"

    # Check for sibling README
    readme_path = dir_path / "README.md"
    sibling_readme = "README.md" if readme_path.exists() else "null"

    # Find children
    children = find_children(dir_path)
    children_yaml = "\n".join(f"  - {c}" for c in children) if children else "  []"

    # Get purpose
    purpose = get_purpose(dir_path, dir_name)

    # Get contents
    contents = find_contents(dir_path)

    # Build related section
    related_items = []
    if parent != "null":
        related_items.append(f"- **Parent**: [{dir_path.parent.name}]({parent})")
    if sibling_readme != "null":
        related_items.append(f"- **README**: [{sibling_readme}]({sibling_readme})")
    for child in children[:3]:
        child_name = child.replace("/CLAUDE.md", "")
        related_items.append(f"- **{child_name}**: [{child}]({child})")

    related = "\n".join(related_items) if related_items else "*No related files*"

    # Generate content
    content = TEMPLATE.format(
        directory=str(rel_path), purpose=purpose, parent=parent, sibling_readme=sibling_readme, children=children_yaml, name=dir_name, contents=contents, related=related
    )

    claude_md_path = dir_path / "CLAUDE.md"

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"Path: {claude_md_path}")
        print(f"{'=' * 60}")
        print(content[:500] + "..." if len(content) > 500 else content)

    if dry_run:
        print(f"[DRY-RUN] Would create: {claude_md_path}")
        return True

    # Create directory if needed
    dir_path.mkdir(parents=True, exist_ok=True)

    # Write file
    claude_md_path.write_text(content)
    print(f"Created: {claude_md_path}")
    return True


def find_missing_claude_md(repo_root: Path) -> list[Path]:
    """Find all directories that should have CLAUDE.md but don't."""
    missing = []

    # Check target directories
    for target in TARGET_DIRS:
        target_path = repo_root / target
        if target_path.exists() and not (target_path / "CLAUDE.md").exists():
            missing.append(target_path)

    # Check specs directories
    specs_dir = repo_root / "specs"
    if specs_dir.exists():
        for spec in specs_dir.iterdir():
            if spec.is_dir() and spec.name not in SKIP_DIRS:
                if not (spec / "CLAUDE.md").exists():
                    missing.append(spec)
                # Check contracts subdirectory
                contracts = spec / "contracts"
                if contracts.exists() and not (contracts / "CLAUDE.md").exists():
                    missing.append(contracts)

    # Check skill subdirectories
    skills_dir = repo_root / ".claude" / "skills"
    if skills_dir.exists():
        for skill in skills_dir.iterdir():
            if skill.is_dir() and skill.name not in SKIP_DIRS:
                for subdir in ("scripts", "templates", "schemas"):
                    subdir_path = skill / subdir
                    if subdir_path.exists() and not (subdir_path / "CLAUDE.md").exists():
                        missing.append(subdir_path)

    return sorted(missing)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate missing CLAUDE.md files for directory hierarchy")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without creating files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show generated content")

    args = parser.parse_args()

    print(f"Repository root: {REPO_ROOT}")
    print("Scanning for missing CLAUDE.md files...\n")

    missing = find_missing_claude_md(REPO_ROOT)

    if not missing:
        print("All directories have CLAUDE.md files!")
        return

    print(f"Found {len(missing)} directories missing CLAUDE.md:\n")
    for path in missing:
        print(f"  - {path.relative_to(REPO_ROOT)}")

    print(f"\n{'=' * 60}")
    print("Generating CLAUDE.md files...")
    print("=" * 60 + "\n")

    created = 0
    for path in missing:
        if generate_claude_md(path, dry_run=args.dry_run, verbose=args.verbose):
            created += 1

    print(f"\n{'=' * 60}")
    if args.dry_run:
        print(f"[DRY-RUN] Would create {created} CLAUDE.md files")
    else:
        print(f"Created {created} CLAUDE.md files")
    print("=" * 60)


if __name__ == "__main__":
    main()
