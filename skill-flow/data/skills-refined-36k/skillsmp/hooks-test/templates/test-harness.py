#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# ///

"""
Claude Code Hook Test Harness

Unit test hooks in isolation by simulating the Claude Code hook environment.

Run with: uv run test-harness.py
Or import: from test_harness import create_payload, run_hook, assert_blocked

Example:
    payload = create_payload("PreToolUse", tool_name="Bash",
                             tool_input={"command": "rm -rf /"})
    result = run_hook("./my-hook.py", payload)
    assert_blocked(result, "dangerous")
"""

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class HookResult:
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False

    @property
    def blocked(self) -> bool:
        return self.exit_code == 2

    @property
    def allowed(self) -> bool:
        return self.exit_code == 0

    def json_output(self) -> dict | None:
        if self.exit_code != 0:
            return None
        try:
            return json.loads(self.stdout)
        except json.JSONDecodeError:
            return None


def create_payload(
    event_name: str,
    *,
    session_id: str = "test-session-123",
    cwd: str = "/test/project",
    permission_mode: str = "default",
    tool_name: str | None = None,
    tool_input: dict | None = None,
    tool_response: dict | None = None,
    prompt: str | None = None,
    message: str | None = None,
    notification_type: str | None = None,
    stop_hook_active: bool = False,
    trigger: str = "manual",
    custom_instructions: str = "",
    source: str = "startup",
    reason: str = "other",
) -> dict:
    """Create a valid hook input payload for testing."""
    payload = {
        "session_id": session_id,
        "transcript_path": f"/tmp/.claude/sessions/{session_id}.jsonl",
        "cwd": cwd,
        "permission_mode": permission_mode,
        "hook_event_name": event_name,
    }

    if event_name in ("PreToolUse", "PostToolUse"):
        payload["tool_name"] = tool_name or "Bash"
        payload["tool_input"] = tool_input or {}
        payload["tool_use_id"] = "toolu_01TestHookHarness"
        if event_name == "PostToolUse":
            payload["tool_response"] = tool_response or {}

    elif event_name == "UserPromptSubmit":
        payload["prompt"] = prompt or ""

    elif event_name == "Notification":
        payload["message"] = message or ""
        payload["notification_type"] = notification_type or "permission_prompt"

    elif event_name in ("Stop", "SubagentStop"):
        payload["stop_hook_active"] = stop_hook_active

    elif event_name == "PreCompact":
        payload["trigger"] = trigger
        payload["custom_instructions"] = custom_instructions

    elif event_name == "SessionStart":
        payload["source"] = source

    elif event_name == "SessionEnd":
        payload["reason"] = reason

    return payload


def run_hook(
    hook_path: str | Path,
    payload: dict,
    timeout: int = 60,
    env: dict | None = None,
) -> HookResult:
    """Execute a hook with the given payload and return the result."""
    hook_env = os.environ.copy()
    hook_env["CLAUDE_PROJECT_DIR"] = payload.get("cwd", "/test/project")
    if env:
        hook_env.update(env)

    try:
        result = subprocess.run(
            [str(hook_path)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=hook_env,
        )
        return HookResult(
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )
    except subprocess.TimeoutExpired:
        return HookResult(
            exit_code=-1,
            stdout="",
            stderr=f"Hook timed out after {timeout}s",
            timed_out=True,
        )


def assert_blocked(result: HookResult, reason_contains: str | None = None) -> None:
    """Assert the hook blocked the action (exit code 2)."""
    assert result.exit_code == 2, (
        f"Expected exit code 2 (block), got {result.exit_code}. Stderr: {result.stderr}"
    )
    if reason_contains:
        assert reason_contains.lower() in result.stderr.lower(), (
            f"Expected stderr to contain '{reason_contains}', got: {result.stderr}"
        )


def assert_allowed(result: HookResult) -> None:
    """Assert the hook allowed the action (exit code 0, no block decision)."""
    assert result.exit_code == 0, (
        f"Expected exit code 0 (allow), got {result.exit_code}. Stderr: {result.stderr}"
    )
    output = result.json_output()
    if output:
        decision = output.get("decision")
        hook_decision = output.get("hookSpecificOutput", {}).get("permissionDecision")
        assert decision != "block", f"Hook returned block decision: {output}"
        assert hook_decision != "deny", f"Hook returned deny decision: {output}"


def assert_modified_input(
    result: HookResult,
    field: str,
    expected: Any,
) -> None:
    """Assert PreToolUse hook modified a specific input field."""
    assert result.exit_code == 0, f"Expected exit code 0, got {result.exit_code}"
    output = result.json_output()
    assert output, f"Expected JSON output, got: {result.stdout}"

    updated = output.get("hookSpecificOutput", {}).get("updatedInput", {})
    assert field in updated, f"Field '{field}' not in updatedInput: {updated}"
    assert updated[field] == expected, (
        f"Expected {field}={expected}, got {updated[field]}"
    )


def assert_context_added(result: HookResult, contains: str) -> None:
    """Assert hook added context (UserPromptSubmit/SessionStart)."""
    assert result.exit_code == 0, f"Expected exit code 0, got {result.exit_code}"

    if contains.lower() in result.stdout.lower():
        return

    output = result.json_output()
    if output:
        context = output.get("hookSpecificOutput", {}).get("additionalContext", "")
        assert contains.lower() in context.lower(), (
            f"Expected context to contain '{contains}', got: {context}"
        )
        return

    raise AssertionError(
        f"Expected output to contain '{contains}', got: {result.stdout}"
    )


if __name__ == "__main__":
    print("Hook Test Harness")
    print("=" * 40)

    payload = create_payload(
        "PreToolUse",
        tool_name="Bash",
        tool_input={"command": "echo hello", "description": "Print greeting"},
    )
    print("\nExample PreToolUse payload:")
    print(json.dumps(payload, indent=2))

    print("\nUsage:")
    print("  result = run_hook('./my-hook.py', payload)")
    print("  assert_blocked(result, 'dangerous')")
    print("  assert_allowed(result)")
