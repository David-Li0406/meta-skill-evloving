#!/usr/bin/env python3
"""Semi-automated documentation sync tool for skill updates.

This script helps propagate changes across documentation files when a skill is updated:
1. Prompts for skill name and new version
2. Updates SKILL.md version in frontmatter
3. Identifies affected sections in WORKFLOW.md
4. Prompts for CHANGELOG entry
5. Creates git commit with proper format
6. Optionally archives previous version

Usage:
    python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \\
        <skill-name> <new-version>

Example:
    python .claude/skills/workflow-utilities/scripts/sync_skill_docs.py \\
        bmad-planner 5.2.0

Options:
    --archive: Archive previous SKILL.md version
    --dry-run: Show what would be changed without making changes
    --auto-commit: Skip commit message confirmation

Constants:
- SKILL_DIRS: List of valid skill names
  Rationale: Validate skill name input
- VERSION_PATTERN: Regex for semantic versioning
  Rationale: Enforce MAJOR.MINOR.PATCH format
"""

import argparse
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Constants
SKILL_DIRS = [
    "workflow-orchestrator",
    "tech-stack-adapter",
    "git-workflow-manager",
    "bmad-planner",
    "speckit-author",
    "quality-enforcer",
    "workflow-utilities",
]

VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
YAML_FRONTMATTER_PATTERN = re.compile(r"^(---\n.*?version:\s*)(\d+\.\d+\.\d+)(.*?\n---)", re.DOTALL | re.MULTILINE)


def error_exit(message: str, code: int = 1) -> None:
    """Print error message and exit."""
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def run_command(cmd: list[str], capture=True, check=True) -> str | None:
    """Run command and return output or None on error."""
    try:
        if capture:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check)
            return None
    except subprocess.CalledProcessError as e:
        if check:
            error_exit(f"Command failed: {' '.join(cmd)}\n{e.stderr}")
        return None
    except FileNotFoundError:
        error_exit(f"Command not found: {cmd[0]}")


def parse_version(version_str: str) -> tuple[int, int, int] | None:
    """Parse semantic version string."""
    match = VERSION_PATTERN.match(version_str)
    if not match:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def get_current_version(skill_md: Path) -> str | None:
    """Extract current version from SKILL.md frontmatter."""
    if not skill_md.exists():
        return None

    content = skill_md.read_text()
    match = re.search(r"version:\s*(\d+\.\d+\.\d+)", content)
    if not match:
        return None

    return match.group(1)


def update_skill_md_version(skill_md: Path, old_version: str, new_version: str, dry_run: bool = False) -> bool:
    """Update version in SKILL.md frontmatter.

    Args:
        skill_md: Path to SKILL.md file
        old_version: Current version
        new_version: New version to set
        dry_run: If True, don't write changes

    Returns:
        True if update successful, False otherwise
    """
    content = skill_md.read_text()

    # Update version in frontmatter
    new_content = re.sub(r"(version:\s*)" + re.escape(old_version), r"\g<1>" + new_version, content, count=1)

    if new_content == content:
        print(f"  ⚠ No version found to update in {skill_md}")
        return False

    if dry_run:
        print(f"  [DRY RUN] Would update {skill_md}")
        print(f"    version: {old_version} → {new_version}")
        return True

    skill_md.write_text(new_content)
    print(f"  ✓ Updated {skill_md}")
    print(f"    version: {old_version} → {new_version}")
    return True


def prompt_changelog_entry(skill_name: str, old_version: str, new_version: str) -> str:
    """Prompt user to create CHANGELOG entry.

    Args:
        skill_name: Name of the skill
        old_version: Previous version
        new_version: New version

    Returns:
        CHANGELOG entry content
    """
    print("\n" + "=" * 70)
    print(f"CHANGELOG Entry for {skill_name}")
    print("=" * 70)
    print(f"Version: {old_version} → {new_version}")
    print()
    print("Enter changelog entry (type 'END' on a blank line when done):")
    print()
    print("Categories: Added, Changed, Deprecated, Removed, Fixed, Security")
    print()

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    changelog_content = "\n".join(lines)

    # Generate full CHANGELOG entry
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    entry = f"""## [{new_version}] - {today}

{changelog_content}
"""

    return entry


def update_changelog(changelog_md: Path, entry: str, dry_run: bool = False) -> bool:
    """Update CHANGELOG.md with new entry.

    Args:
        changelog_md: Path to CHANGELOG.md
        entry: CHANGELOG entry to add
        dry_run: If True, don't write changes

    Returns:
        True if update successful, False otherwise
    """
    if not changelog_md.exists():
        print(f"  ⚠ CHANGELOG.md not found: {changelog_md}")
        print("  Creating new CHANGELOG.md...")

        header = """# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

"""
        content = header + entry
    else:
        content = changelog_md.read_text()

        # Insert after [Unreleased] section
        # Find the line with ## [Unreleased]
        unreleased_match = re.search(r"(## \[Unreleased\].*?\n\n)", content, re.DOTALL)

        if unreleased_match:
            # Insert after [Unreleased] section
            insert_pos = unreleased_match.end()
            content = content[:insert_pos] + entry + "\n" + content[insert_pos:]
        else:
            # No [Unreleased] section, insert at top after header
            header_end = content.find("\n## ")
            if header_end != -1:
                content = content[:header_end] + "\n" + entry + content[header_end:]
            else:
                content = content + "\n" + entry

    if dry_run:
        print(f"  [DRY RUN] Would update {changelog_md}")
        print(f"\n{entry}")
        return True

    changelog_md.write_text(content)
    print(f"  ✓ Updated {changelog_md}")
    return True


def find_workflow_md_sections(workflow_md: Path, skill_name: str) -> list[str]:
    """Find sections in WORKFLOW.md that reference the skill.

    Args:
        workflow_md: Path to WORKFLOW.md
        skill_name: Name of the skill

    Returns:
        List of section headings that reference the skill
    """
    if not workflow_md.exists():
        return []

    content = workflow_md.read_text()
    sections = []

    # Find all section headings (### or ##) followed by content mentioning skill
    section_pattern = re.compile(r"^(#{2,3}) (.+?)$", re.MULTILINE)

    current_section = None
    current_section_content = []

    for line in content.split("\n"):
        section_match = section_pattern.match(line)
        if section_match:
            # Check previous section for skill reference
            if current_section and skill_name in "\n".join(current_section_content):
                sections.append(current_section)

            # Start new section
            current_section = section_match.group(2)
            current_section_content = []
        else:
            current_section_content.append(line)

    # Check last section
    if current_section and skill_name in "\n".join(current_section_content):
        sections.append(current_section)

    return sections


def create_commit_message(skill_name: str, old_version: str, new_version: str, changelog_entry: str) -> str:
    """Generate git commit message.

    Args:
        skill_name: Name of the skill
        old_version: Previous version
        new_version: New version
        changelog_entry: CHANGELOG entry content

    Returns:
        Formatted commit message
    """
    # Determine commit type from version change
    old_v = parse_version(old_version)
    new_v = parse_version(new_version)

    if old_v[0] != new_v[0]:
        commit_type = "feat!"  # MAJOR breaking change
    elif old_v[1] != new_v[1]:
        commit_type = "feat"  # MINOR new feature
    else:
        commit_type = "fix"  # PATCH bug fix

    # Extract first line from changelog for summary
    first_line = changelog_entry.split("\n")[2] if len(changelog_entry.split("\n")) > 2 else "update"
    first_line = first_line.lstrip("- ").strip()

    commit_msg = f"""{commit_type}({skill_name}): {first_line}

Updated {skill_name} from v{old_version} to v{new_version}:

{changelog_entry.strip()}

Updated documentation:
- .claude/skills/{skill_name}/SKILL.md (version {new_version})
- .claude/skills/{skill_name}/CHANGELOG.md (new entry)

Refs: .claude/skills/{skill_name}/CHANGELOG.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"""

    return commit_msg


def archive_previous_version(skill_md: Path, old_version: str, dry_run: bool = False) -> bool:
    """Archive previous SKILL.md version.

    Args:
        skill_md: Path to SKILL.md
        old_version: Version to archive
        dry_run: If True, don't create archive

    Returns:
        True if archive successful, False otherwise
    """
    archived_dir = skill_md.parent / "ARCHIVED"
    archived_dir.mkdir(exist_ok=True)

    archive_file = archived_dir / f"SKILL_v{old_version.replace('.', '_')}.md"

    if dry_run:
        print(f"  [DRY RUN] Would archive to {archive_file}")
        return True

    # Copy current SKILL.md to archive
    import shutil

    shutil.copy2(skill_md, archive_file)

    print(f"  ✓ Archived previous version to {archive_file}")
    return True


def main():
    """Main entry point for sync tool."""
    parser = argparse.ArgumentParser(description="Semi-automated documentation sync tool for skill updates")
    parser.add_argument("skill_name", help="Name of the skill (e.g., bmad-planner)")
    parser.add_argument("new_version", help="New version number (e.g., 5.2.0)")
    parser.add_argument("--archive", action="store_true", help="Archive previous SKILL.md version")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without making them")
    parser.add_argument("--auto-commit", action="store_true", help="Skip commit message confirmation")

    args = parser.parse_args()

    # Validate skill name
    if args.skill_name not in SKILL_DIRS:
        error_exit(f"Invalid skill name: {args.skill_name}\nValid skills: {', '.join(SKILL_DIRS)}")

    # Validate new version format
    if not parse_version(args.new_version):
        error_exit(f"Invalid version format: {args.new_version} (expected MAJOR.MINOR.PATCH)")

    # Get repository root
    try:
        repo_root = Path(run_command(["git", "rev-parse", "--show-toplevel"]))
    except (subprocess.CalledProcessError, FileNotFoundError, TypeError):
        error_exit("Not in a git repository")

    # Paths
    skill_dir = repo_root / ".claude" / "skills" / args.skill_name
    skill_md = skill_dir / "SKILL.md"
    changelog_md = skill_dir / "CHANGELOG.md"
    workflow_md = repo_root / "WORKFLOW.md"

    # Verify skill directory exists
    if not skill_dir.exists():
        error_exit(f"Skill directory not found: {skill_dir}")

    if not skill_md.exists():
        error_exit(f"SKILL.md not found: {skill_md}")

    # Get current version
    old_version = get_current_version(skill_md)
    if not old_version:
        error_exit(f"Could not extract current version from {skill_md}")

    print("=" * 70)
    print("Skill Documentation Sync Tool")
    print("=" * 70)
    print(f"Skill: {args.skill_name}")
    print(f"Version: {old_version} → {args.new_version}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Step 1: Update SKILL.md version
    print("Step 1: Update SKILL.md version")
    print("-" * 70)
    if not update_skill_md_version(skill_md, old_version, args.new_version, args.dry_run):
        error_exit("Failed to update SKILL.md")

    # Step 2: Archive previous version (if requested)
    if args.archive:
        print("\nStep 2: Archive previous version")
        print("-" * 70)
        archive_previous_version(skill_md, old_version, args.dry_run)

    # Step 3: Prompt for CHANGELOG entry
    print("\nStep 3: Create CHANGELOG entry")
    print("-" * 70)
    changelog_entry = prompt_changelog_entry(args.skill_name, old_version, args.new_version)

    # Step 4: Update CHANGELOG.md
    print("\nStep 4: Update CHANGELOG.md")
    print("-" * 70)
    update_changelog(changelog_md, changelog_entry, args.dry_run)

    # Step 5: Find affected WORKFLOW.md sections
    print("\nStep 5: Identify affected WORKFLOW.md sections")
    print("-" * 70)
    workflow_sections = find_workflow_md_sections(workflow_md, args.skill_name)
    if workflow_sections:
        print(f"  Found {len(workflow_sections)} section(s) in WORKFLOW.md:")
        for section in workflow_sections:
            print(f"    - {section}")
        print("\n  ⚠ Please manually review and update these sections in WORKFLOW.md")
    else:
        print(f"  No sections found referencing {args.skill_name} (this might be OK)")

    # Step 6: Create git commit
    if not args.dry_run:
        print("\nStep 6: Create git commit")
        print("-" * 70)

        commit_msg = create_commit_message(args.skill_name, old_version, args.new_version, changelog_entry)

        print("Commit message:")
        print("-" * 70)
        print(commit_msg)
        print("-" * 70)

        if not args.auto_commit:
            confirm = input("\nCreate this commit? (Y/n) > ").strip().lower()
            if confirm and confirm not in ["y", "yes"]:
                print("Aborted.")
                sys.exit(0)

        # Stage files
        run_command(["git", "add", str(skill_md)], capture=False)
        run_command(["git", "add", str(changelog_md)], capture=False)

        # Commit
        run_command(["git", "commit", "-m", commit_msg], capture=False)

        print("\n✓ Commit created successfully!")

    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)

    if args.dry_run:
        print("DRY RUN - No changes were made")
    else:
        print(f"✓ Updated {args.skill_name} from v{old_version} to v{args.new_version}")

    print("\nNext steps:")
    print("  1. Review SKILL.md for any additional documentation updates")
    print("  2. Review WORKFLOW.md sections identified above")
    print("  3. Update root CLAUDE.md if command examples changed")
    print("  4. Run: python .claude/skills/workflow-utilities/scripts/validate_versions.py")
    print("  5. Review complete UPDATE_CHECKLIST: cat .claude/skills/UPDATE_CHECKLIST.md")

    print()


if __name__ == "__main__":
    main()
