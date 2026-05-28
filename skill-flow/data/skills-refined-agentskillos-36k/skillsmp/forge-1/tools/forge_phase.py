#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Manage FORGE phase transitions and tasks."""

import argparse
import re
import sys
from pathlib import Path

PHASES = ["Focus", "Orchestrate", "Refine", "Generate", "Evaluate"]


def get_forge_dir() -> Path:
    """Get the .forge directory path."""
    return Path.cwd() / ".forge"


def get_active_cycle() -> Path | None:
    """Get the most recent active cycle."""
    forge_dir = get_forge_dir()
    active_dir = forge_dir / "cycles" / "active"

    if not active_dir.exists():
        return None

    cycles = sorted(active_dir.glob("*.md"), reverse=True)
    return cycles[0] if cycles else None


def get_active_phase(content: str) -> str | None:
    """Extract the active phase from cycle content."""
    pattern = r"<!-- FORGE_PHASE:(\w+):Active -->"
    match = re.search(pattern, content)
    return match.group(1) if match else None


def get_phase_items(content: str, phase_name: str) -> list[tuple[bool, str]]:
    """Extract checkbox items from a phase section."""
    # Find phase section
    section_pattern = rf"## Phase \d+: {phase_name}.*?(?=## Phase \d+:|---\s*$|\Z)"
    section_match = re.search(section_pattern, content, re.DOTALL)

    if not section_match:
        return []

    section = section_match.group(0)

    # Find checkboxes
    items = []
    checkbox_pattern = r"- \[([ xX])\] (.+?)(?:\n|$)"
    for match in re.finditer(checkbox_pattern, section):
        completed = match.group(1).lower() == "x"
        text = match.group(2).strip()
        items.append((completed, text))

    return items


def update_phase_state(content: str, phase_name: str, new_state: str) -> str:
    """Update phase state marker in content."""
    pattern = rf"(<!-- FORGE_PHASE:{phase_name}:)\w+(-->)"
    return re.sub(pattern, rf"\g<1>{new_state}\2", content)


def advance_phase(force: bool = False) -> bool:
    """Advance to the next phase."""
    cycle_path = get_active_cycle()

    if not cycle_path:
        print("Error: No active cycle found.")
        return False

    content = cycle_path.read_text()
    current_phase = get_active_phase(content)

    if not current_phase:
        print("Error: Could not determine current phase.")
        return False

    # Check if at final phase
    if current_phase == "Evaluate":
        print("Already at final phase (Evaluate).")
        print(f"Complete the cycle with: uv run forge_cycle.py complete {cycle_path.stem}")
        return False

    # Validate current phase requirements
    items = get_phase_items(content, current_phase)
    incomplete = [text for completed, text in items if not completed]

    if incomplete and not force:
        print(f"Cannot advance: {len(incomplete)} incomplete items in {current_phase}:")
        for item in incomplete:
            print(f"  - {item}")
        print()
        print("Complete these items or use --force to skip validation.")
        return False

    if incomplete and force:
        print(f"Warning: Forcing advance with {len(incomplete)} incomplete items.")

    # Get next phase
    current_idx = PHASES.index(current_phase)
    next_phase = PHASES[current_idx + 1]

    # Update content
    content = update_phase_state(content, current_phase, "Complete")
    content = update_phase_state(content, next_phase, "Active")

    # Write back
    cycle_path.write_text(content)

    print(f"Advanced: {current_phase} -> {next_phase}")
    print()

    # Print phase guidance
    guidance = {
        "Orchestrate": [
            "Design Container architecture (C4 L2)",
            "Design Component architecture (C4 L3)",
            "Create dependency map",
            "Break into session-sized tasks",
        ],
        "Refine": [
            "Write Given-When-Then acceptance criteria",
            "Document interface specifications",
            "Enumerate edge cases by category",
            "Remember: NO CODE in this phase",
        ],
        "Generate": [
            "Follow TDD: RED -> GREEN -> REFACTOR",
            "One task per session",
            "Write failing tests first",
            "Minimum 80% coverage",
        ],
        "Evaluate": [
            "Verify against acceptance criteria",
            "Test edge cases",
            "Complete security review",
            "Make disposition decision",
        ],
    }

    if next_phase in guidance:
        print(f"Next steps for {next_phase}:")
        for step in guidance[next_phase]:
            print(f"  - {step}")

    return True


def complete_task(description: str) -> bool:
    """Mark a task as complete by checking its checkbox."""
    cycle_path = get_active_cycle()

    if not cycle_path:
        print("Error: No active cycle found.")
        return False

    content = cycle_path.read_text()
    current_phase = get_active_phase(content)

    if not current_phase:
        print("Error: Could not determine current phase.")
        return False

    # Find and update matching checkbox
    # Match unchecked checkbox with similar text
    pattern = r"- \[ \] ([^\n]*" + re.escape(description[:20]) + r"[^\n]*)"
    match = re.search(pattern, content, re.IGNORECASE)

    if match:
        old_text = match.group(0)
        new_text = old_text.replace("- [ ]", "- [x]", 1)
        content = content.replace(old_text, new_text, 1)
        cycle_path.write_text(content)
        print(f"Completed: {match.group(1)}")
        return True

    # Try exact match
    exact_pattern = r"- \[ \] " + re.escape(description)
    if re.search(exact_pattern, content):
        content = re.sub(exact_pattern, f"- [x] {description}", content, count=1)
        cycle_path.write_text(content)
        print(f"Completed: {description}")
        return True

    print(f"Task not found: {description}")
    print()
    print("Available tasks in current phase:")
    items = get_phase_items(content, current_phase)
    for completed, text in items:
        if not completed:
            print(f"  - {text}")

    return False


def add_task(description: str) -> bool:
    """Add a new task to the current phase."""
    cycle_path = get_active_cycle()

    if not cycle_path:
        print("Error: No active cycle found.")
        return False

    content = cycle_path.read_text()
    current_phase = get_active_phase(content)

    if not current_phase:
        print("Error: Could not determine current phase.")
        return False

    # Find the phase section and add task
    section_pattern = rf"(## Phase \d+: {current_phase}.*?)((?=## Phase \d+:)|(?=---\s*$)|\Z)"
    match = re.search(section_pattern, content, re.DOTALL)

    if not match:
        print(f"Error: Could not find {current_phase} section.")
        return False

    section = match.group(1)

    # Add task before the section ends
    new_task = f"- [ ] {description}\n"

    # Find a good insertion point (after last checkbox or after "###" section)
    last_checkbox = None
    for m in re.finditer(r"- \[[ xX]\] .+\n", section):
        last_checkbox = m

    if last_checkbox:
        insert_pos = match.start(1) + last_checkbox.end()
        content = content[:insert_pos] + new_task + content[insert_pos:]
    else:
        # Add after "### " section header if exists
        notes_match = re.search(r"(### \w+\n\n)", section)
        if notes_match:
            insert_pos = match.start(1) + notes_match.end()
            content = content[:insert_pos] + new_task + content[insert_pos:]
        else:
            print("Error: Could not find insertion point.")
            return False

    cycle_path.write_text(content)
    print(f"Added task: {description}")
    return True


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Manage FORGE phases and tasks")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # advance command
    advance_parser = subparsers.add_parser("advance", help="Advance to next phase")
    advance_parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force advance even with incomplete items",
    )

    # complete-task command
    complete_parser = subparsers.add_parser(
        "complete-task", help="Mark a task as complete"
    )
    complete_parser.add_argument("description", help="Task description (partial match)")

    # add-task command
    add_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    args = parser.parse_args()

    if args.command == "advance":
        success = advance_phase(force=args.force)
        return 0 if success else 1
    elif args.command == "complete-task":
        success = complete_task(args.description)
        return 0 if success else 1
    elif args.command == "add-task":
        success = add_task(args.description)
        return 0 if success else 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
