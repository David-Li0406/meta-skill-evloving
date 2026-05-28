#!/usr/bin/env python3
"""
Memory Bank TODO Extractor

Extracts action items and next steps from Memory Bank files.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict
import re
import json
from datetime import datetime


TODO_PATTERNS = [
    r"^- \[ \] (.+)$",  # Markdown checkbox unchecked
    r"^- \[x\] (.+)$",  # Markdown checkbox checked
    r"^- TODO: (.+)$",  # TODO prefix
    r"^- (.+)$",  # Simple bullet point
]

PRIORITY_KEYWORDS = ["urgent", "critical", "important", "asap", "blocker", "blocked"]
STATUS_KEYWORDS = ["in progress", "started", "working on", "doing"]


def find_memory_bank(project_path: Path) -> Path:
    """Find the memory-bank directory in the project."""
    memory_bank_path = project_path / "memory-bank"

    if not memory_bank_path.exists():
        print(f"❌ Memory Bank not found at {memory_bank_path}")
        sys.exit(1)

    return memory_bank_path


def extract_section_content(content: str, section_name: str) -> str:
    """Extract content under a specific markdown section."""
    # Find the section header
    pattern = rf"^##?\s+{re.escape(section_name)}\s*$"
    lines = content.split("\n")

    in_section = False
    section_lines = []

    for line in lines:
        if re.match(pattern, line, re.IGNORECASE):
            in_section = True
            continue

        # Stop at next same-level or higher header
        if in_section:
            if re.match(r"^##?\s+", line):
                break
            section_lines.append(line)

    return "\n".join(section_lines)


def parse_todos(text: str, source: str) -> List[Dict]:
    """Parse TODO items from text."""
    todos = []
    lines = text.split("\n")

    for i, line in enumerate(lines, 1):
        line = line.strip()

        if not line:
            continue

        # Check if line matches any TODO pattern
        matched = False
        is_completed = False
        todo_text = ""

        # Check for checkbox patterns
        checkbox_match = re.match(r"^- \[([ x])\] (.+)$", line, re.IGNORECASE)
        if checkbox_match:
            is_completed = checkbox_match.group(1).lower() == "x"
            todo_text = checkbox_match.group(2).strip()
            matched = True

        # Check for TODO: prefix
        elif line.startswith("- TODO:"):
            todo_text = line[7:].strip()
            matched = True

        # Check for simple bullet points under relevant sections
        elif line.startswith("- ") or line.startswith("* "):
            todo_text = line[2:].strip()
            matched = True

        if matched and todo_text:
            # Determine priority
            priority = "normal"
            lower_text = todo_text.lower()

            if any(keyword in lower_text for keyword in PRIORITY_KEYWORDS):
                priority = "high"

            # Determine status
            status = "completed" if is_completed else "pending"
            if any(keyword in lower_text for keyword in STATUS_KEYWORDS):
                status = "in_progress"

            todos.append({
                "text": todo_text,
                "source": source,
                "line": i,
                "status": status,
                "priority": priority,
                "completed": is_completed
            })

    return todos


def extract_todos_from_file(file_path: Path, sections: List[str] = None) -> List[Dict]:
    """Extract TODOs from a specific file."""
    if not file_path.exists():
        return []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"⚠️  Cannot read {file_path}: {e}", file=sys.stderr)
        return []

    all_todos = []

    # If specific sections specified, extract from those sections only
    if sections:
        for section in sections:
            section_content = extract_section_content(content, section)
            if section_content.strip():
                todos = parse_todos(section_content, f"{file_path.name}::{section}")
                all_todos.extend(todos)
    else:
        # Extract from entire file
        todos = parse_todos(content, file_path.name)
        all_todos.extend(todos)

    return all_todos


def extract_all_todos(memory_bank: Path) -> Dict:
    """Extract all TODOs from Memory Bank."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "todos": [],
        "summary": {
            "total": 0,
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "high_priority": 0
        }
    }

    # File-specific sections to check
    file_sections = {
        "activeContext.md": ["Next Steps", "Blockers"],
        "progress.md": ["What's Left to Build", "Known Issues"],
        "projectbrief.md": None,
        "productContext.md": None,
        "techContext.md": None,
        "systemPatterns.md": None,
    }

    for filename, sections in file_sections.items():
        file_path = memory_bank / filename
        todos = extract_todos_from_file(file_path, sections)
        results["todos"].extend(todos)

    # Update summary
    results["summary"]["total"] = len(results["todos"])
    results["summary"]["pending"] = len([t for t in results["todos"] if t["status"] == "pending"])
    results["summary"]["in_progress"] = len([t for t in results["todos"] if t["status"] == "in_progress"])
    results["summary"]["completed"] = len([t for t in results["todos"] if t["status"] == "completed"])
    results["summary"]["high_priority"] = len([t for t in results["todos"] if t["priority"] == "high"])

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Extract TODO items from Memory Bank",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s .
  %(prog)s /path/to/project
  %(prog)s . --json
  %(prog)s . --pending-only
  %(prog)s . --high-priority
        """
    )

    parser.add_argument(
        "project_path",
        type=Path,
        help="Path to project root containing memory-bank directory"
    )

    parser.add_argument(
        "--pending-only",
        action="store_true",
        help="Show only pending TODOs (exclude completed)"
    )

    parser.add_argument(
        "--high-priority",
        action="store_true",
        help="Show only high-priority TODOs"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Validate project path
    if not args.project_path.exists():
        print(f"❌ Project path does not exist: {args.project_path}")
        sys.exit(1)

    # Find memory bank
    memory_bank = find_memory_bank(args.project_path)

    # Extract TODOs
    results = extract_all_todos(memory_bank)

    # Filter results based on flags
    todos = results["todos"]

    if args.pending_only:
        todos = [t for t in todos if t["status"] != "completed"]

    if args.high_priority:
        todos = [t for t in todos if t["priority"] == "high"]

    # Output results
    if args.json:
        output = dict(results)
        output["todos"] = todos
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Memory Bank TODOs: {memory_bank}")
        print(f"{'='*60}\n")

        # Show summary
        print(f"Summary:")
        print(f"  Total: {results['summary']['total']}")
        print(f"  Pending: {results['summary']['pending']}")
        print(f"  In Progress: {results['summary']['in_progress']}")
        print(f"  Completed: {results['summary']['completed']}")
        print(f"  High Priority: {results['summary']['high_priority']}")

        if todos:
            print(f"\nTODO Items:\n")

            # Group by status
            for status in ["in_progress", "pending", "completed"]:
                status_todos = [t for t in todos if t["status"] == status]

                if status_todos:
                    status_label = {
                        "pending": "📋 Pending",
                        "in_progress": "🔄 In Progress",
                        "completed": "✅ Completed"
                    }.get(status, status)

                    print(f"{status_label}:")

                    for todo in status_todos:
                        priority_icon = "🔴" if todo["priority"] == "high" else "  "
                        print(f"  {priority_icon} {todo['text']}")
                        print(f"     ({todo['source']})")

                    print()
        else:
            print("\n✅ No TODO items found\n")

        print(f"{'='*60}\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
