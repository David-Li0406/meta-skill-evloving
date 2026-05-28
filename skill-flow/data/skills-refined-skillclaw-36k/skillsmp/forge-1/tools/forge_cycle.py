#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Manage FORGE development cycles."""

import argparse
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

CYCLE_TEMPLATE = """# Cycle: {name}

**Created**: {created}
**Priority**: {priority}
**Status**: Active

## Overview

<!-- Describe what this cycle aims to accomplish -->

---

<!-- FORGE_PHASE:Focus:Active -->
## Phase 1: Focus

**Purpose**: Define what you're building and why.

### Required Outputs
- [ ] Problem statement and target users defined
- [ ] Testable success criteria written
- [ ] System Context diagram (C4 L1) created
- [ ] Clear boundaries on what you WON'T build

### Notes

<!-- Document Focus phase work here -->

---

<!-- FORGE_PHASE:Orchestrate:Pending -->
## Phase 2: Orchestrate

**Purpose**: Break the work into session-sized pieces.

### Required Outputs
- [ ] Container architecture (C4 L2) designed
- [ ] Component architecture (C4 L3) designed
- [ ] Dependency map created
- [ ] Tasks sized for single AI sessions

### Tasks

<!-- List tasks here -->

---

<!-- FORGE_PHASE:Refine:Pending -->
## Phase 3: Refine

**Purpose**: Define exactly what "done" looks like.

### Required Outputs
- [ ] Acceptance criteria in Given-When-Then format
- [ ] Interface specifications documented
- [ ] Edge cases enumerated by category
- [ ] Constraints vs criteria documented

**CRITICAL**: No code in this phase - specifications only.

### Specifications

<!-- Document specifications here -->

---

<!-- FORGE_PHASE:Generate:Pending -->
## Phase 4: Generate

**Purpose**: AI writes code following TDD.

### Process
- [ ] RED: Write failing tests
- [ ] GREEN: Minimal code to pass
- [ ] REFACTOR: Improve while green

### Implementation Notes

<!-- Document implementation progress here -->

---

<!-- FORGE_PHASE:Evaluate:Pending -->
## Phase 5: Evaluate

**Purpose**: Verify output matches intent.

### Checklist
- [ ] Criteria verified line-by-line
- [ ] Edge cases tested
- [ ] Security review completed
- [ ] Integration tested

### Disposition

<!-- Accept / Accept with issues / Revise / Reject -->

---

## Learnings

<!-- Capture learnings during and after the cycle -->
"""


def get_forge_dir() -> Path:
    """Get the .forge directory path."""
    return Path.cwd() / ".forge"


def slugify(name: str) -> str:
    """Convert name to slug for filename."""
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug


def new_cycle(name: str, priority: str = "medium") -> bool:
    """Create a new development cycle."""
    forge_dir = get_forge_dir()

    if not forge_dir.exists():
        print("Error: FORGE not initialized. Run forge_init.py first.")
        return False

    # Generate cycle ID and filename
    timestamp = datetime.now(timezone.utc)
    date_prefix = timestamp.strftime("%Y%m%d")
    slug = slugify(name)
    cycle_id = f"{date_prefix}-{slug}"
    filename = f"{cycle_id}.md"

    # Check for existing cycle with same name
    active_dir = forge_dir / "cycles" / "active"
    cycle_path = active_dir / filename

    if cycle_path.exists():
        print(f"Error: Cycle already exists: {cycle_path}")
        return False

    # Create cycle file
    content = CYCLE_TEMPLATE.format(
        name=name,
        created=timestamp.isoformat(),
        priority=priority,
    )

    with open(cycle_path, "w") as f:
        f.write(content)

    print(f"Created cycle: {cycle_id}")
    print(f"  File: {cycle_path}")
    print(f"  Phase: Focus (Active)")
    print()
    print("Next steps:")
    print("  1. Define problem statement and target users")
    print("  2. Write testable success criteria")
    print("  3. Create C4 L1 System Context diagram")
    print("  4. Set clear boundaries")
    print()
    print("Check status: uv run forge_status.py")

    return True


def list_cycles() -> None:
    """List all active and completed cycles."""
    forge_dir = get_forge_dir()

    if not forge_dir.exists():
        print("Error: FORGE not initialized. Run forge_init.py first.")
        return

    active_dir = forge_dir / "cycles" / "active"
    completed_dir = forge_dir / "cycles" / "completed"

    print("FORGE Cycles")
    print("=" * 40)

    # Active cycles
    print("\nActive:")
    active_cycles = sorted(active_dir.glob("*.md"))
    if active_cycles:
        for cycle in active_cycles:
            cycle_id = cycle.stem
            # Read to get current phase
            content = cycle.read_text()
            phase = _get_active_phase(content)
            print(f"  - {cycle_id} [{phase}]")
    else:
        print("  (none)")

    # Completed cycles
    print("\nCompleted:")
    completed_cycles = sorted(completed_dir.glob("*.md"))
    if completed_cycles:
        for cycle in completed_cycles:
            cycle_id = cycle.stem
            print(f"  - {cycle_id}")
    else:
        print("  (none)")


def _get_active_phase(content: str) -> str:
    """Extract the active phase from cycle content."""
    pattern = r"<!-- FORGE_PHASE:(\w+):Active -->"
    match = re.search(pattern, content)
    return match.group(1) if match else "Unknown"


def complete_cycle(cycle_id: str) -> bool:
    """Complete and archive a cycle."""
    forge_dir = get_forge_dir()

    if not forge_dir.exists():
        print("Error: FORGE not initialized.")
        return False

    active_dir = forge_dir / "cycles" / "active"
    completed_dir = forge_dir / "cycles" / "completed"

    # Find the cycle file
    cycle_path = None
    for path in active_dir.glob("*.md"):
        if cycle_id in path.stem:
            cycle_path = path
            break

    if not cycle_path:
        print(f"Error: Cycle not found: {cycle_id}")
        print("Available cycles:")
        for path in active_dir.glob("*.md"):
            print(f"  - {path.stem}")
        return False

    # Check if in Evaluate phase
    content = cycle_path.read_text()
    active_phase = _get_active_phase(content)

    if active_phase != "Evaluate":
        print(f"Error: Cycle is in {active_phase} phase, not Evaluate.")
        print("Complete all phases before finishing the cycle.")
        return False

    # Move to completed
    dest_path = completed_dir / cycle_path.name
    shutil.move(str(cycle_path), str(dest_path))

    print(f"Completed cycle: {cycle_path.stem}")
    print(f"  Archived to: {dest_path}")
    print()
    print("Consider running a retrospective: uv run forge_learn.py retro")

    return True


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Manage FORGE development cycles")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # new command
    new_parser = subparsers.add_parser("new", help="Create a new cycle")
    new_parser.add_argument("name", help="Cycle name/description")
    new_parser.add_argument(
        "--priority",
        choices=["low", "medium", "high", "critical"],
        default="medium",
        help="Cycle priority (default: medium)",
    )

    # list command
    subparsers.add_parser("list", help="List all cycles")

    # complete command
    complete_parser = subparsers.add_parser("complete", help="Complete a cycle")
    complete_parser.add_argument("cycle_id", help="Cycle ID to complete")

    args = parser.parse_args()

    if args.command == "new":
        success = new_cycle(args.name, args.priority)
        return 0 if success else 1
    elif args.command == "list":
        list_cycles()
        return 0
    elif args.command == "complete":
        success = complete_cycle(args.cycle_id)
        return 0 if success else 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
