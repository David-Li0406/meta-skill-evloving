#!/usr/bin/env python3
"""
PRISM Workflow Status - display current workflow state.
"""

import re
from pathlib import Path

STATE_FILE = Path(".claude/prism-loop.local.md")

# TDD Flow: Planning → RED Gate → GREEN (DEV+QA) → Green Gate (Final)
# Step types: agent (auto), gate (/prism-approve)
WORKFLOW_STEPS = [
    # PLANNING PHASE
    ("review_previous_notes", "SM", "agent"),
    ("draft_story", "SM", "agent"),
    # TDD RED PHASE
    ("write_failing_tests", "QA", "agent"),
    ("red_gate", "-", "gate"),
    # TDD GREEN PHASE - DEV implements, QA validates, then gate
    ("implement_tasks", "DEV", "agent"),
    ("verify_green_state", "QA", "agent"),
    ("green_gate", "-", "gate"),  # Final gate
]


def parse_state() -> dict:
    """Parse state file."""
    result = {
        "active": False,
        "current_step": "",
        "current_step_index": 0,
        "story_file": "",
        "paused_for_manual": False,
        "started_at": "",
    }

    if not STATE_FILE.exists():
        return result

    try:
        content = STATE_FILE.read_text(encoding='utf-8')

        for key in result.keys():
            if key in ["active", "paused_for_manual"]:
                match = re.search(rf"^{key}:\s*(\S+)", content, re.MULTILINE)
                if match:
                    result[key] = match.group(1).lower() == "true"
            elif key == "current_step_index":
                match = re.search(rf"^{key}:\s*(\d+)", content, re.MULTILINE)
                if match:
                    result[key] = int(match.group(1))
            else:
                match = re.search(rf'^{key}:\s*["\']?([^"\'\n]*)["\']?', content, re.MULTILINE)
                if match:
                    result[key] = match.group(1).strip()

    except IOError:
        pass

    return result


def main():
    state = parse_state()

    if not state["active"]:
        print("No active PRISM workflow loop.")
        print("Start one with /prism-loop")
        return

    print("PRISM Workflow Status")
    print("=" * 50)
    print(f"Started: {state['started_at']}")
    print(f"Story: {state['story_file'] or '(not yet created)'}")
    print(f"Paused: {'Yes - waiting for manual action' if state['paused_for_manual'] else 'No'}")
    print("")
    print("Progress:")
    print("-" * 50)

    current_idx = state["current_step_index"]

    for i, (step_id, agent, step_type) in enumerate(WORKFLOW_STEPS):
        if i < current_idx:
            marker = "  DONE"
        elif i == current_idx:
            marker = ">>> CURRENT"
        else:
            marker = "  pending"

        agent_str = f"[{agent}]" if agent != "-" else ""
        type_str = f"({step_type})"
        print(f"{marker:12} {i+1:2}. {step_id} {agent_str} {type_str}")

    print("-" * 50)

    if state["paused_for_manual"]:
        print("")
        current_step = state["current_step"]
        if current_step == "red_gate":
            print("Action: /prism-approve to proceed to GREEN, or /prism-reject to loop back")
        else:
            print("Action: /prism-approve to continue")


if __name__ == "__main__":
    main()
