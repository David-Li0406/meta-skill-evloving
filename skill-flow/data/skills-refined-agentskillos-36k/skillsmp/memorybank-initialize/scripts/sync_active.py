#!/usr/bin/env python3
"""
Memory Bank Active Context Sync Tool

Fast update tool for activeContext.md and progress.md. Allows quick updates
to current work status without full Memory Bank review.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Optional
import json
from datetime import datetime
import re


def find_memory_bank(project_path: Path) -> Path:
    """Find the memory-bank directory in the project."""
    memory_bank_path = project_path / "memory-bank"

    if not memory_bank_path.exists():
        print(f"❌ Memory Bank not found at {memory_bank_path}")
        sys.exit(1)

    return memory_bank_path


def read_file_sections(file_path: Path) -> Dict[str, str]:
    """Parse a markdown file into sections."""
    if not file_path.exists():
        return {}

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ Cannot read {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    sections = {}
    current_section = None
    current_content = []
    lines = content.split("\n")

    for line in lines:
        # Check for section header (## Section Name)
        header_match = re.match(r"^##\s+(.+)$", line)

        if header_match:
            # Save previous section
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()

            # Start new section
            current_section = header_match.group(1).strip()
            current_content = []
        elif current_section:
            current_content.append(line)

    # Save last section
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def write_file_sections(file_path: Path, sections: Dict[str, str], title: str = None):
    """Write sections back to a markdown file."""
    lines = []

    # Add title if provided
    if title:
        lines.append(f"# {title}\n")

    # Add each section
    for section_name, content in sections.items():
        lines.append(f"## {section_name}\n")
        if content.strip():
            lines.append(content.strip())
            lines.append("")  # Empty line after section

    output = "\n".join(lines)

    try:
        file_path.write_text(output, encoding="utf-8")
    except Exception as e:
        print(f"❌ Cannot write {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def update_section(file_path: Path, section_name: str, new_content: str, append: bool = False):
    """Update a specific section in a markdown file."""
    sections = read_file_sections(file_path)

    if section_name not in sections:
        print(f"⚠️  Section '{section_name}' not found in {file_path.name}, creating it", file=sys.stderr)
        sections[section_name] = ""

    if append and sections[section_name].strip():
        # Append to existing content
        sections[section_name] = sections[section_name].strip() + "\n" + new_content.strip()
    else:
        # Replace content
        sections[section_name] = new_content.strip()

    # Determine title from filename
    title = "Active Context" if file_path.name == "activeContext.md" else "Progress"

    write_file_sections(file_path, sections, title=title)


def sync_active_context(
    memory_bank: Path,
    updates: Dict[str, str],
    append: bool = False
) -> Dict:
    """Sync activeContext.md with provided updates."""
    active_context_path = memory_bank / "activeContext.md"

    results = {
        "timestamp": datetime.now().isoformat(),
        "file": str(active_context_path),
        "updated_sections": [],
        "success": True
    }

    valid_sections = ["Current Focus", "Recent Changes", "Next Steps", "Blockers", "Learnings"]

    for section, content in updates.items():
        if section not in valid_sections:
            print(f"⚠️  Warning: '{section}' is not a standard activeContext.md section", file=sys.stderr)

        try:
            update_section(active_context_path, section, content, append=append)
            results["updated_sections"].append(section)
        except Exception as e:
            print(f"❌ Failed to update section '{section}': {e}", file=sys.stderr)
            results["success"] = False

    return results


def sync_progress(
    memory_bank: Path,
    updates: Dict[str, str],
    append: bool = False
) -> Dict:
    """Sync progress.md with provided updates."""
    progress_path = memory_bank / "progress.md"

    results = {
        "timestamp": datetime.now().isoformat(),
        "file": str(progress_path),
        "updated_sections": [],
        "success": True
    }

    valid_sections = ["What's Working", "What's Left to Build", "Current Status", "Known Issues"]

    for section, content in updates.items():
        if section not in valid_sections:
            print(f"⚠️  Warning: '{section}' is not a standard progress.md section", file=sys.stderr)

        try:
            update_section(progress_path, section, content, append=append)
            results["updated_sections"].append(section)
        except Exception as e:
            print(f"❌ Failed to update section '{section}': {e}", file=sys.stderr)
            results["success"] = False

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Fast sync tool for Memory Bank active files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update Current Focus in activeContext.md
  %(prog)s . --active '{"Current Focus": "Working on authentication"}'

  # Append to Next Steps
  %(prog)s . --active '{"Next Steps": "- Add tests"}' --append

  # Update progress.md
  %(prog)s . --progress '{"Current Status": "Sprint 2 in progress"}'

  # Update both files
  %(prog)s . --active '{"Current Focus": "Bug fixes"}' --progress '{"Known Issues": "- Login timeout"}'

  # Read from file
  %(prog)s . --active @updates.json
        """
    )

    parser.add_argument(
        "project_path",
        type=Path,
        help="Path to project root containing memory-bank directory"
    )

    parser.add_argument(
        "--active",
        type=str,
        help="JSON object with activeContext.md updates, or @filename to read from file"
    )

    parser.add_argument(
        "--progress",
        type=str,
        help="JSON object with progress.md updates, or @filename to read from file"
    )

    parser.add_argument(
        "--append",
        action="store_true",
        help="Append to existing section content instead of replacing"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Validate inputs
    if not args.active and not args.progress:
        parser.error("At least one of --active or --progress must be provided")

    if not args.project_path.exists():
        print(f"❌ Project path does not exist: {args.project_path}")
        sys.exit(1)

    # Find memory bank
    memory_bank = find_memory_bank(args.project_path)

    # Parse updates
    def parse_updates(update_str: str) -> Optional[Dict]:
        if not update_str:
            return None

        # Check if it's a file reference
        if update_str.startswith("@"):
            file_path = Path(update_str[1:])
            if not file_path.exists():
                print(f"❌ File not found: {file_path}")
                sys.exit(1)
            try:
                return json.loads(file_path.read_text())
            except Exception as e:
                print(f"❌ Cannot parse {file_path}: {e}")
                sys.exit(1)

        # Parse as JSON string
        try:
            return json.loads(update_str)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            sys.exit(1)

    active_updates = parse_updates(args.active)
    progress_updates = parse_updates(args.progress)

    # Perform updates
    results = {
        "timestamp": datetime.now().isoformat(),
        "activeContext": None,
        "progress": None,
        "success": True
    }

    if active_updates:
        results["activeContext"] = sync_active_context(memory_bank, active_updates, append=args.append)
        if not results["activeContext"]["success"]:
            results["success"] = False

    if progress_updates:
        results["progress"] = sync_progress(memory_bank, progress_updates, append=args.append)
        if not results["progress"]["success"]:
            results["success"] = False

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Memory Bank Sync: {memory_bank}")
        print(f"{'='*60}\n")

        if results["activeContext"]:
            print(f"activeContext.md updated:")
            for section in results["activeContext"]["updated_sections"]:
                print(f"  ✅ {section}")

        if results["progress"]:
            print(f"\nprogress.md updated:")
            for section in results["progress"]["updated_sections"]:
                print(f"  ✅ {section}")

        print(f"\n{'='*60}")
        if results["success"]:
            print("✅ Sync completed successfully")
        else:
            print("⚠️  Sync completed with errors")
        print(f"{'='*60}\n")

    sys.exit(0 if results["success"] else 1)


if __name__ == "__main__":
    main()
