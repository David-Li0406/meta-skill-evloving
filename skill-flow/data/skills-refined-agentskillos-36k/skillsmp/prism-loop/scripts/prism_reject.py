#!/usr/bin/env python3
"""
PRISM Reject - loop back from current gate to earlier phase.

Outputs the instruction for the step it loops back to.
"""

import re
import sys
from pathlib import Path

STATE_FILE = Path(".claude/prism-loop.local.md")

# Steps with their loop_back_to index (None = no reject allowed)
WORKFLOW_STEPS = [
    ("review_previous_notes", "sm", "planning-review", None),
    ("draft_story", "sm", "draft", None),
    ("write_failing_tests", "qa", "write-failing-tests", None),
    ("red_gate", None, None, 0),  # Reject loops back to step 0
    ("implement_tasks", "dev", "develop-story", None),
    ("verify_green_state", "qa", "verify-green-state", None),
    ("green_gate", None, None, None),  # Final gate - no reject
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
    """Update state file to loop back."""
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


def build_agent_instruction(step_id: str, agent: str, action: str, story_file: str, prompt: str = "") -> str:
    """Build instruction for the agent step."""

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
        return

    if not state["paused_for_manual"]:
        print("Workflow is not at a gate.")
        print(f"Current step: {state['current_step']}")
        return

    current_index = state["current_step_index"]
    current_step = state["current_step"]

    # Find loop_back_to for current step
    loop_back_to = None
    for i, (step_id, agent, action, back_to) in enumerate(WORKFLOW_STEPS):
        if i == current_index:
            loop_back_to = back_to
            break

    if loop_back_to is None:
        print(f"Cannot reject from {current_step} - no loop back defined.")
        print("Use /prism-approve to continue or /cancel-prism to stop.")
        return

    # Get the step we're looping back to
    back_step_id, back_agent, back_action, _ = WORKFLOW_STEPS[loop_back_to]
    update_state(back_step_id, loop_back_to)

    print("=" * 60)
    print(f"REJECTED! Looping back to: {back_step_id}")
    print(f"[Step {loop_back_to + 1}/{len(WORKFLOW_STEPS)}]")
    print("=" * 60)
    print("")

    # Output the instruction for the step we're looping back to
    instruction = build_agent_instruction(
        back_step_id,
        back_agent,
        back_action,
        state["story_file"],
        state["prompt"]
    )
    print(instruction)


if __name__ == "__main__":
    main()
