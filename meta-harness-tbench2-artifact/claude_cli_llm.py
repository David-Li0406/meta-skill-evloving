"""Claude Code CLI backend for the meta-harness LLM call.

When META_HARNESS_USE_CLAUDE_CLI=1 is set, the agent routes its tool-calling LLM
request through the local `claude` CLI (subscription auth) instead of litellm
hitting the Anthropic API. This shells out once per agent step:

    claude -p --output-format json --json-schema <schema> --model <alias>
           --tools "" --append-system-prompt <sys> < prompt

The CLI's `--json-schema` flag enforces a structured response matching the
agent's tool union (execute_commands / task_complete / image_read). The
`structured_output` field in the CLI's JSON result is then synthesised back
into the same `tool_calls` shape that the rest of agent.py expects.
"""

from __future__ import annotations

import asyncio
import json
import os
import uuid
from dataclasses import dataclass
from typing import Any

from harbor.models.metric import UsageInfo


CLAUDE_CLI_PATH = os.environ.get(
    "CLAUDE_CLI_PATH",
    os.environ.get("CLAUDE_CODE_EXECPATH", "claude"),
)

# Structured-output schema. Mirrors the litellm `tools` schema flattened into a
# single object whose `tool` discriminator picks which fields are meaningful.
RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "tool": {
            "type": "string",
            "enum": ["execute_commands", "task_complete", "image_read"],
            "description": "Which tool to invoke this turn.",
        },
        "analysis": {
            "type": "string",
            "description": "For execute_commands: situation analysis.",
        },
        "plan": {
            "type": "string",
            "description": "For execute_commands: plan for next commands.",
        },
        "commands": {
            "type": "array",
            "description": "For execute_commands: list of keystrokes to send.",
            "items": {
                "type": "object",
                "properties": {
                    "keystrokes": {"type": "string"},
                    "duration": {"type": "number"},
                },
                "required": ["keystrokes"],
            },
        },
        "file_path": {
            "type": "string",
            "description": "For image_read: absolute path to image.",
        },
        "image_read_instruction": {
            "type": "string",
            "description": "For image_read: what to extract from the image.",
        },
    },
    "required": ["tool"],
}


_MODEL_ALIASES = {
    "claude-opus-4-7": "opus",
    "claude-opus-4-6": "claude-opus-4-6",
    "claude-opus-4-5": "claude-opus-4-5",
    "claude-sonnet-4-6": "sonnet",
    "claude-sonnet-4-5": "claude-sonnet-4-5",
    "claude-haiku-4-5": "haiku",
}


def _normalise_model(model_name: str) -> str:
    """Convert litellm-style model names (anthropic/claude-opus-4-6) into the
    short alias the `claude` CLI accepts (`opus`/`sonnet`/`haiku`/full name)."""
    name = model_name.split("/", 1)[-1].strip()
    # strip trailing [1m] context-size tag if present
    bracket = name.find("[")
    if bracket > 0:
        name = name[:bracket]
    return _MODEL_ALIASES.get(name, name)


def _flatten_content(content: Any) -> str:
    """Reduce a message content field (string OR list of content-blocks) to plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text" and "text" in block:
                    parts.append(block["text"])
                elif block.get("type") == "image_url":
                    parts.append("[image attached]")
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content) if content is not None else ""


def _format_conversation(messages: list[dict[str, Any]]) -> tuple[str, str]:
    """Split messages into (system_prompt, conversation_text).

    The CLI is one-shot: we serialise the full transcript into a single prompt
    so the model sees prior turns. Tool/assistant messages are tagged so the
    model can follow the trajectory.
    """
    system_parts: list[str] = []
    convo_parts: list[str] = []

    for msg in messages:
        role = msg.get("role", "")
        text = _flatten_content(msg.get("content"))

        if role == "system":
            if text:
                system_parts.append(text)
        elif role == "user":
            if text:
                convo_parts.append(f"<user>\n{text}\n</user>")
        elif role == "assistant":
            tool_calls = msg.get("tool_calls") or []
            tc_summary = ""
            if tool_calls:
                rendered = []
                for tc in tool_calls:
                    fn = tc.get("function", {})
                    rendered.append(
                        f"  - {fn.get('name', '?')}({fn.get('arguments', '')})"
                    )
                tc_summary = "\n[prior tool calls]\n" + "\n".join(rendered)
            block = (text or "") + tc_summary
            if block.strip():
                convo_parts.append(f"<assistant>\n{block}\n</assistant>")
        elif role == "tool":
            # acknowledgement of a prior tool call; usually short ("executed")
            if text and text.strip() and text.strip().lower() != "executed":
                convo_parts.append(f"<tool_result>\n{text}\n</tool_result>")

    system_prompt = "\n\n".join(p for p in system_parts if p)
    conversation = "\n\n".join(convo_parts)
    return system_prompt, conversation


_PROMPT_INSTRUCTION = """You are the LLM driver for a Terminal-Bench agent. Each turn, pick exactly ONE tool to invoke and emit it as structured JSON matching the provided schema.

Tools:
- execute_commands: run terminal commands. Required: analysis (string), plan (string), commands (array of {keystrokes: string, duration?: number}). The commands array may be empty to wait.
- task_complete: signal you believe the task is done (will require a follow-up confirmation turn).
- image_read: read an image file. Required: file_path (absolute path), image_read_instruction (what to extract). Use ONLY for image files.

Most turns should be execute_commands. Keep keystrokes terse and end shell commands with a newline character so they execute. Use small durations (0.1-1.0s) for fast commands, larger for long-running ones, never above 60s."""


@dataclass
class _CLIResult:
    content: str
    tool_calls: list[dict[str, Any]]
    usage: UsageInfo | None


async def call_claude_cli(
    messages: list[dict[str, Any]],
    model_name: str,
    timeout_sec: float = 900.0,
    max_budget_usd: float | None = None,
) -> _CLIResult:
    """Single non-interactive `claude -p` invocation that returns a structured
    response synthesised into the tool-call shape agent.py expects."""

    system_from_msgs, conversation = _format_conversation(messages)

    full_prompt = (
        f"{_PROMPT_INSTRUCTION}\n\n"
        f"=== Conversation so far ===\n{conversation}\n\n"
        f"=== Your turn ===\nEmit ONE JSON object per the schema. Do not add commentary."
    )

    cli_model = _normalise_model(model_name)

    cmd = [
        CLAUDE_CLI_PATH,
        "-p",
        "--input-format", "text",
        "--output-format", "json",
        "--json-schema", json.dumps(RESPONSE_SCHEMA),
        "--model", cli_model,
        "--tools", "",
        "--permission-mode", "bypassPermissions",
        "--no-session-persistence",
        "--exclude-dynamic-system-prompt-sections",
    ]
    if system_from_msgs:
        cmd.extend(["--append-system-prompt", system_from_msgs])
    if max_budget_usd is not None:
        cmd.extend(["--max-budget-usd", str(max_budget_usd)])

    # Run in a clean cwd so claude's CLAUDE.md auto-discovery doesn't pull
    # in anything from the meta-harness repo or the user's home dir.
    workdir = os.environ.get("META_HARNESS_CLI_WORKDIR") or "/tmp"

    # Drop env vars that would steer the child CLI session away from the
    # user's subscription auth or into reusing the current claude session.
    # ANTHROPIC_API_KEY / ANTHROPIC_AUTH_TOKEN must be dropped so the CLI
    # falls back to the keychain-stored OAuth credentials (subscription).
    child_env = {
        k: v for k, v in os.environ.items()
        if k not in {
            "ANTHROPIC_API_KEY",
            "ANTHROPIC_AUTH_TOKEN",
            "ANTHROPIC_BASE_URL",
            "CLAUDE_CODE_SIMPLE",
            "CLAUDE_CODE_SESSION_ID",
            "CLAUDE_CODE_ENTRYPOINT",
            "CLAUDECODE",
            "AI_AGENT",
        }
    }

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=workdir,
        env=child_env,
    )

    try:
        stdout_bytes, stderr_bytes = await asyncio.wait_for(
            proc.communicate(input=full_prompt.encode("utf-8")),
            timeout=timeout_sec,
        )
    except asyncio.TimeoutError:
        proc.kill()
        raise RuntimeError(f"claude CLI timed out after {timeout_sec}s")

    if proc.returncode != 0:
        err = stderr_bytes.decode("utf-8", errors="replace")[:2000]
        out = stdout_bytes.decode("utf-8", errors="replace")[:2000]
        raise RuntimeError(
            f"claude CLI exited {proc.returncode}. "
            f"stderr={err or '<empty>'} stdout={out or '<empty>'}"
        )

    raw = stdout_bytes.decode("utf-8", errors="replace").strip()
    # `claude -p --output-format json` emits a single JSON object on stdout.
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"claude CLI returned non-JSON output: {raw[:500]}") from e

    if payload.get("is_error") or payload.get("subtype") != "success":
        raise RuntimeError(
            f"claude CLI reported error: {payload.get('result') or payload.get('api_error_status')}"
        )

    structured = payload.get("structured_output")
    if not isinstance(structured, dict):
        # Fallback: try to parse `result` as JSON.
        result_text = payload.get("result", "")
        try:
            structured = json.loads(result_text)
        except Exception:
            raise RuntimeError(
                f"claude CLI did not produce structured_output. result={result_text[:500]}"
            )

    tool_calls = _structured_to_tool_calls(structured)
    content_text = payload.get("result", "") or ""
    usage = _extract_usage(payload)

    return _CLIResult(content=content_text, tool_calls=tool_calls, usage=usage)


def _structured_to_tool_calls(structured: dict[str, Any]) -> list[dict[str, Any]]:
    """Map our flat structured response onto the OpenAI/litellm tool_calls shape."""
    tool = structured.get("tool")
    if tool == "execute_commands":
        args = {
            "analysis": structured.get("analysis", ""),
            "plan": structured.get("plan", ""),
            "commands": structured.get("commands", []) or [],
        }
        return [_make_tool_call("execute_commands", args)]
    if tool == "task_complete":
        return [_make_tool_call("task_complete", {})]
    if tool == "image_read":
        args = {
            "file_path": structured.get("file_path", ""),
            "image_read_instruction": structured.get("image_read_instruction", ""),
        }
        return [_make_tool_call("image_read", args)]
    return []


def _make_tool_call(name: str, args: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"call_{uuid.uuid4().hex[:12]}",
        "type": "function",
        "function": {
            "name": name,
            "arguments": json.dumps(args),
        },
    }


def _extract_usage(payload: dict[str, Any]) -> UsageInfo | None:
    usage = payload.get("usage") or {}
    if not usage:
        return None
    try:
        return UsageInfo(
            prompt_tokens=int(usage.get("input_tokens") or 0),
            completion_tokens=int(usage.get("output_tokens") or 0),
            cache_tokens=int(usage.get("cache_read_input_tokens") or 0),
            cost_usd=float(payload.get("total_cost_usd") or 0.0),
        )
    except (TypeError, ValueError):
        return None
