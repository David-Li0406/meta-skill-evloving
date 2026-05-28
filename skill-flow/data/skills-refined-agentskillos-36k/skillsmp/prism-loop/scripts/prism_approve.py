#!/usr/bin/env python3
"""
PRISM Approve - advance workflow from current gate to next phase.

Outputs the instruction for the next agent step so workflow continues.
"""

import re
import sys
from pathlib import Path

STATE_FILE = Path(".claude/prism-loop.local.md")

WORKFLOW_STEPS = [
    # (step_id, agent, action, step_type, loop_back_to, validation)
    ("review_previous_notes", "sm", "planning-review", "agent", None, None),
    ("draft_story", "sm", "draft", "agent", None, None),
    ("write_failing_tests", "qa", "write-failing-tests", "agent", None, "red"),
    ("red_gate", None, None, "gate", 0, None),
    ("implement_tasks", "dev", "develop-story", "agent", None, "green"),
    ("verify_green_state", "qa", "verify-green-state", "agent", None, "green_full"),
    ("green_gate", None, None, "gate", None, None),
]


def parse_state() -> dict:
    """Parse state file."""
    result = {
        "active": False,
        "current_step": "",
        "current_step_index": 0,
        "story_file": "",
        "paused_for_manual": False,
        "prompt": "",
    }

    if not STATE_FILE.exists():
        return result

    content = STATE_FILE.read_text(encoding='utf-8')

    for key in ["active", "paused_for_manual"]:
        match = re.search(rf"^{key}:\s*(\S+)", content, re.MULTILINE)
        if match:
            result[key] = match.group(1).lower() == "true"

    match = re.search(r"^current_step_index:\s*(\d+)", content, re.MULTILINE)
    if match:
        result["current_step_index"] = int(match.group(1))

    match = re.search(r'^current_step:\s*["\']?([^"\'\n]*)["\']?', content, re.MULTILINE)
    if match:
        result["current_step"] = match.group(1).strip()

    match = re.search(r'^story_file:\s*["\']?([^"\'\n]*)["\']?', content, re.MULTILINE)
    if match:
        result["story_file"] = match.group(1).strip()

    match = re.search(r'^prompt:\s*["\']?([^"\'\n]*)["\']?', content, re.MULTILINE)
    if match:
        result["prompt"] = match.group(1).strip()

    return result


def update_state(current_step: str, current_index: int):
    """Update state file to advance to next step."""
    content = STATE_FILE.read_text(encoding='utf-8')

    content = re.sub(
        r"^current_step:\s*.*$",
        f"current_step: {current_step}",
        content,
        flags=re.MULTILINE
    )

    content = re.sub(
        r"^current_step_index:\s*\d+",
        f"current_step_index: {current_index}",
        content,
        flags=re.MULTILINE
    )

    content = re.sub(
        r"^paused_for_manual:\s*\S+",
        "paused_for_manual: false",
        content,
        flags=re.MULTILINE
    )

    STATE_FILE.write_text(content, encoding='utf-8')


def cleanup():
    """Remove state file."""
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def build_agent_instruction(step_id: str, agent: str, action: str, story_file: str, prompt: str = "") -> str:
    """Build instruction for the next agent step."""

    review_instruction = "Execute SM agent: *planning-review\nReview previous story dev/QA notes for context before drafting new story."
    if prompt:
        review_instruction += f"\n\nWorkflow Context: {prompt}"

    draft_instruction = "Execute SM agent: *draft\nDraft the next story from the sharded epic and architecture documents."
    if prompt:
        draft_instruction += f"\n\nWorkflow Context: {prompt}"

    instructions = {
        "review_previous_notes": review_instruction,
        "draft_story": draft_instruction,
        "write_failing_tests": f"""Execute QA agent: *write-failing-tests {story_file}

TDD RED PHASE: Write failing tests BEFORE implementation.

Process:
1. IDENTIFY existing tests covering affected code areas
2. EXTEND existing test files if found, CREATE new if not
3. WRITE failing tests for each acceptance criterion
4. RUN tests to confirm they FAIL (assertion failures only)
5. UPDATE story with test file paths and mappings

CRITICAL: Tests must FAIL cleanly (assertion failures, not errors).
The stop hook will validate RED state before advancing.""",
        "implement_tasks": f"""Execute DEV agent: *develop-story

TDD GREEN PHASE: Make the failing tests pass.

Story file: {story_file}

Tests exist and are FAILING. Your job:
1. Write MINIMAL code to make each test pass
2. Run tests after each change
3. Continue until ALL tests pass
4. Refactor while keeping tests green

CRITICAL: The stop hook validates that ALL tests pass.
Do NOT stop until tests are GREEN.""",
        "verify_green_state": f"""Execute QA agent: *verify-green-state {story_file}

TDD GREEN STATE VERIFICATION: Confirm implementation is complete.

Process:
1. RUN all tests (unit, integration, e2e)
2. VERIFY all tests PASS
3. RUN linting checks
4. RUN type checks (if applicable)
5. VERIFY build succeeds

The stop hook validates tests + lint before advancing to completion gate.""",
    }

    return instructions.get(step_id, f"Execute {agent} agent: *{action}")


def main():
    state = parse_state()

    if not state["active"]:
        print("No active PRISM workflow.")
        print("Start one with /prism-loop")
        return

    if not state["paused_for_manual"]:
        print("Workflow is not at a gate.")
        print(f"Current step: {state['current_step']}")
        return

    current_index = state["current_step_index"]
    current_step = state["current_step"]

    # Check if this is the final gate (green_gate)
    if current_step == "green_gate":
        print("=" * 60)
        print("PRISM Workflow APPROVED and COMPLETE!")
        print("=" * 60)
        print(f"\nStory file: {state['story_file']}")
        print("")
        print("TDD Cycle Complete:")
        print("  - RED: Failing tests written ✓")
        print("  - GREEN: All tests passing ✓")
        print("  - QA: Verified ✓")
        print("")
        print("Final steps:")
        print("  1. Commit your changes")
        print("  2. Mark the story as Done")
        cleanup()
        return

    # Advance to next step
    next_index = current_index + 1
    if next_index >= len(WORKFLOW_STEPS):
        print("Workflow complete!")
        cleanup()
        return

    next_step = WORKFLOW_STEPS[next_index]
    next_step_id, next_agent, next_action, next_step_type, _, _ = next_step

    update_state(next_step_id, next_index)

    print("=" * 60)
    print(f"APPROVED! Advancing to: {next_step_id}")
    print(f"[Step {next_index + 1}/{len(WORKFLOW_STEPS)}]")
    print("=" * 60)
    print("")

    # Output the instruction for the next agent step
    instruction = build_agent_instruction(
        next_step_id,
        next_agent,
        next_action,
        state["story_file"],
        state["prompt"]
    )
    print(instruction)


if __name__ == "__main__":
    main()
