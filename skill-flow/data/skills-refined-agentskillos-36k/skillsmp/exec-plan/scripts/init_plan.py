#!/usr/bin/env python3
"""
Initialize a new ExecPlan file with proper structure and timestamps.

Usage:
    python init_plan.py <output.md> "Short title describing the work"
    python init_plan.py <output.md> "Add user authentication" --purpose "Enable users to log in"

Creates a properly structured ExecPlan ready for authoring.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE = '''# {title}

This ExecPlan is a living document. The sections Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective must be kept up to date as work proceeds.


## Purpose / Big Picture

{purpose}


## Progress

Use a list with checkboxes to summarize granular steps. Every stopping point must be documented here, even if it requires splitting a partially completed task into two ("done" vs. "remaining"). This section must always reflect the actual current state of the work.

- [ ] Research: Understand current state and identify all affected files
- [ ] Design: Define approach, interfaces, and milestones
- [ ] Milestone 1: [describe first deliverable]
- [ ] Validation: Verify all acceptance criteria pass

Use timestamps to measure rates of progress.


## Surprises & Discoveries

Document unexpected behaviors, bugs, optimizations, or insights discovered during implementation. Provide concise evidence.

- Observation: ...
  Evidence: ...


## Decision Log

Record every decision made while working on the plan in the format:

- Decision: ...
  Rationale: ...
  Date/Author: ...


## Outcomes & Retrospective

Summarize outcomes, gaps, and lessons learned at major milestones or at completion. Compare the result against the original purpose.


## Context and Orientation

Describe the current state relevant to this task as if the reader knows nothing. Name the key files and modules by full path. Define any non-obvious term you will use. Do not refer to prior plans.


## Plan of Work

Describe, in prose, the sequence of edits and additions. For each edit, name the file and location (function, module) and what to insert or change. Keep it concrete and minimal.


## Concrete Steps

State the exact commands to run and where to run them (working directory). When a command generates output, show a short expected transcript so the reader can compare. This section must be updated as work proceeds.


## Validation and Acceptance

Describe how to start or exercise the system and what to observe. Phrase acceptance as behavior, with specific inputs and outputs. If tests are involved, say "run <project's test command> and expect <N> passed; the new test <n> fails before the change and passes after."


## Idempotence and Recovery

If steps can be repeated safely, say so. If a step is risky, provide a safe retry or rollback path. Keep the environment clean after completion.


## Artifacts and Notes

Include the most important transcripts, diffs, or snippets as indented examples. Keep them concise and focused on what proves success.


## Interfaces and Dependencies

Be prescriptive. Name the libraries, modules, and services to use and why. Specify the types, traits/interfaces, and function signatures that must exist at the end of the milestone. Prefer stable names and paths.


---

## Plan Revision Notes

- ({timestamp}) Initial plan created
'''


def init_plan(output_path: str, title: str, purpose: str = None) -> bool:
    """
    Create a new ExecPlan file.
    
    Returns True on success, False if file exists.
    """
    path = Path(output_path)
    
    if path.exists():
        print(f"Error: File already exists: {output_path}")
        print("  Delete it first or choose a different name.")
        return False
    
    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    
    if not purpose:
        purpose = "Explain in a few sentences what someone gains after this change and how they can see it working. State the user-visible behavior you will enable."
    
    content = TEMPLATE.format(
        title=title,
        purpose=purpose,
        timestamp=timestamp,
    )
    
    path.write_text(content)
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python init_plan.py <output.md> \"Title\" [--purpose \"Purpose statement\"]")
        print()
        print("Examples:")
        print("  python init_plan.py .plans/auth.md \"Add JWT Authentication\"")
        print("  python init_plan.py feature.md \"Refactor Database Layer\" --purpose \"Improve query performance\"")
        sys.exit(1)
    
    output_path = sys.argv[1]
    title = sys.argv[2]
    
    purpose = None
    if '--purpose' in sys.argv:
        idx = sys.argv.index('--purpose')
        if idx + 1 < len(sys.argv):
            purpose = sys.argv[idx + 1]
    
    if init_plan(output_path, title, purpose):
        print(f"✓ Created: {output_path}")
        print()
        print("Next steps:")
        print("  1. Fill in Purpose / Big Picture with observable user-visible behavior")
        print("  2. Research and fill in Context and Orientation")
        print("  3. Define milestones with specific acceptance criteria")
        print("  4. Run: python validate_plan.py " + output_path)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
