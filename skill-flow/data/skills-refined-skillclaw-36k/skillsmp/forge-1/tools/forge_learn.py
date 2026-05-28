#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Manage FORGE learnings and retrospectives."""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

LEARNING_CATEGORIES = ["pattern", "anti-pattern", "decision", "tool"]

RETRO_TEMPLATE = """## Retrospective: {date}

### Cycle: {cycle_id}

### What Went Well
-

### What Could Be Improved
-

### Action Items
- [ ]

### Key Learnings
-

---

"""


def get_forge_dir() -> Path:
    """Get the .forge directory path."""
    return Path.cwd() / ".forge"


def get_learnings_path() -> Path:
    """Get the learnings.md file path."""
    return get_forge_dir() / "learnings.md"


def add_learning(category: str, title: str, description: str, context: str = "") -> bool:
    """Add a new learning to the knowledge base."""
    forge_dir = get_forge_dir()

    if not forge_dir.exists():
        print("Error: FORGE not initialized.")
        return False

    learnings_path = get_learnings_path()

    if not learnings_path.exists():
        print("Error: learnings.md not found.")
        return False

    # Map category to section
    section_map = {
        "pattern": "## Patterns",
        "anti-pattern": "## Anti-Patterns",
        "decision": "## Decisions",
        "tool": "## Tools",
    }

    section_header = section_map.get(category)
    if not section_header:
        print(f"Error: Unknown category '{category}'")
        print(f"Valid categories: {', '.join(LEARNING_CATEGORIES)}")
        return False

    content = learnings_path.read_text()

    # Format the learning entry
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = f"\n### {title}\n"
    entry += f"*Added: {timestamp}*\n\n"
    entry += f"{description}\n"
    if context:
        entry += f"\n**Context**: {context}\n"

    # Find section and append
    section_pos = content.find(section_header)

    if section_pos == -1:
        # Section doesn't exist, add it
        content += f"\n{section_header}\n{entry}"
    else:
        # Find end of section (next ## or end of file)
        next_section = content.find("\n## ", section_pos + len(section_header))
        if next_section == -1:
            # Append to end
            content += entry
        else:
            # Insert before next section
            content = content[:next_section] + entry + content[next_section:]

    learnings_path.write_text(content)

    print(f"Added learning: {title}")
    print(f"  Category: {category}")
    print(f"  File: {learnings_path}")

    return True


def list_learnings() -> None:
    """List all learnings by category."""
    learnings_path = get_learnings_path()

    if not learnings_path.exists():
        print("Error: learnings.md not found.")
        return

    content = learnings_path.read_text()

    print("FORGE Learnings")
    print("=" * 50)

    # Count entries per section
    import re

    for category, section_name in [
        ("Patterns", "## Patterns"),
        ("Anti-Patterns", "## Anti-Patterns"),
        ("Decisions", "## Decisions"),
        ("Tools", "## Tools"),
    ]:
        section_pos = content.find(section_name)
        if section_pos == -1:
            count = 0
        else:
            # Count ### headers in section
            next_section = content.find("\n## ", section_pos + len(section_name))
            if next_section == -1:
                section_content = content[section_pos:]
            else:
                section_content = content[section_pos:next_section]

            count = len(re.findall(r"^### ", section_content, re.MULTILINE))

        print(f"  {category}: {count} entries")

    print()
    print(f"View: {learnings_path}")


def run_retrospective(cycle_id: str | None = None) -> bool:
    """Start or continue a retrospective."""
    forge_dir = get_forge_dir()

    if not forge_dir.exists():
        print("Error: FORGE not initialized.")
        return False

    # Find cycle if not specified
    if not cycle_id:
        active_dir = forge_dir / "cycles" / "active"
        completed_dir = forge_dir / "cycles" / "completed"

        # Check active first
        cycles = list(active_dir.glob("*.md")) + list(completed_dir.glob("*.md"))
        cycles = sorted(cycles, reverse=True)

        if not cycles:
            print("Error: No cycles found.")
            return False

        cycle_id = cycles[0].stem
        print(f"Using most recent cycle: {cycle_id}")

    # Add retrospective to learnings
    learnings_path = get_learnings_path()
    content = learnings_path.read_text()

    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    retro_content = RETRO_TEMPLATE.format(date=date, cycle_id=cycle_id)

    # Check if retrospectives section exists
    retro_section = "## Retrospectives"
    if retro_section not in content:
        content += f"\n{retro_section}\n"

    # Add retrospective after section header
    section_pos = content.find(retro_section)
    insert_pos = section_pos + len(retro_section) + 1
    content = content[:insert_pos] + retro_content + content[insert_pos:]

    learnings_path.write_text(content)

    print(f"Started retrospective for: {cycle_id}")
    print(f"Edit: {learnings_path}")
    print()
    print("Retrospective prompts:")
    print("  1. What went well?")
    print("  2. What could be improved?")
    print("  3. What action items should we capture?")
    print("  4. What key learnings should we remember?")

    return True


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Manage FORGE learnings")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a new learning")
    add_parser.add_argument(
        "category",
        choices=LEARNING_CATEGORIES,
        help="Learning category",
    )
    add_parser.add_argument("title", help="Learning title")
    add_parser.add_argument("description", help="Learning description")
    add_parser.add_argument(
        "--context",
        "-c",
        default="",
        help="Additional context",
    )

    # list command
    subparsers.add_parser("list", help="List all learnings")

    # retro command
    retro_parser = subparsers.add_parser("retro", help="Run a retrospective")
    retro_parser.add_argument(
        "cycle_id",
        nargs="?",
        default=None,
        help="Cycle ID (default: most recent)",
    )

    args = parser.parse_args()

    if args.command == "add":
        success = add_learning(
            args.category, args.title, args.description, args.context
        )
        return 0 if success else 1
    elif args.command == "list":
        list_learnings()
        return 0
    elif args.command == "retro":
        success = run_retrospective(args.cycle_id)
        return 0 if success else 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
