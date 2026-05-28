#!/usr/bin/env python3
"""
post_tool_use.py - Captures tool usage for pattern learning.
Runs after every tool execution via Claude Code hooks.

Hook type: PostToolUse
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
import hashlib

# Determine skills directory based on environment
SKILLS_DIR = Path(os.environ.get('SKILL_SYSTEM_DIR', Path.home() / ".claude" / "skills"))
PATTERNS_DIR = SKILLS_DIR / ".skill-system" / "patterns"
SEQUENCES_FILE = PATTERNS_DIR / "tool-sequences.jsonl"


def get_session_id():
    """Get or generate a session ID."""
    # Try to get from environment or generate from timestamp
    session_id = os.environ.get('CLAUDE_SESSION_ID')
    if not session_id:
        # Use date-hour as a rough session grouping
        session_id = datetime.utcnow().strftime("%Y%m%d-%H")
    return session_id


def summarize_input(tool_input, tool_name):
    """Create a compact summary of tool input for pattern matching."""
    if not tool_input:
        return {}

    summary = {}

    # For file operations, track file extension and path depth
    if "file_path" in tool_input:
        path = Path(tool_input["file_path"])
        summary["file_ext"] = path.suffix.lower() if path.suffix else "none"
        summary["path_depth"] = len(path.parts)

    # For Bash commands, extract the primary command
    if "command" in tool_input and tool_name == "Bash":
        cmd = tool_input["command"].strip()
        if cmd:
            # Get first word (the command itself)
            parts = cmd.split()
            primary_cmd = parts[0] if parts else ""
            # Remove path prefix if present
            if "/" in primary_cmd:
                primary_cmd = primary_cmd.split("/")[-1]
            summary["command"] = primary_cmd

            # Detect common tool patterns
            if primary_cmd in ["docker", "docker-compose"]:
                summary["domain_hint"] = "devops"
            elif primary_cmd in ["kubectl", "helm", "k9s"]:
                summary["domain_hint"] = "devops"
            elif primary_cmd in ["git", "gh"]:
                summary["domain_hint"] = "git"
            elif primary_cmd in ["npm", "yarn", "pnpm", "node"]:
                summary["domain_hint"] = "frontend"
            elif primary_cmd in ["python", "pip", "pytest"]:
                summary["domain_hint"] = "backend"

    # For Grep/Glob, track search intent
    if "pattern" in tool_input:
        pattern = tool_input["pattern"]
        summary["has_pattern"] = True
        # Hash the pattern for privacy but uniqueness
        summary["pattern_hash"] = hashlib.md5(pattern.encode()).hexdigest()[:8]

    if "glob" in tool_input or "path" in tool_input:
        summary["is_search"] = True

    return summary


def main():
    # Debug: log that hook was triggered
    debug_file = PATTERNS_DIR / "hook-debug.log"
    try:
        with open(debug_file, "a") as f:
            f.write(f"{datetime.utcnow().isoformat()} - Hook triggered\n")
    except:
        pass

    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
        # Debug: log input
        with open(debug_file, "a") as f:
            f.write(f"  Input: {json.dumps(input_data)[:200]}\n")
    except json.JSONDecodeError as e:
        with open(debug_file, "a") as f:
            f.write(f"  JSON Error: {e}\n")
        sys.exit(0)
    except Exception as e:
        with open(debug_file, "a") as f:
            f.write(f"  Error: {e}\n")
        sys.exit(0)

    # Extract tool information
    tool_name = input_data.get("tool_name", "unknown")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})

    # Skip internal/system tools (AskUserQuestion now has dedicated hook in hooks.json)
    skip_tools = ["TodoWrite", "ExitPlanMode", "EnterPlanMode"]
    if tool_name in skip_tools:
        sys.exit(0)

    # Build observation record
    record = {
        "session_id": get_session_id(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "tool": tool_name,
        "input_summary": summarize_input(tool_input, tool_name),
        "success": not tool_response.get("error", False),
    }

    # Ensure patterns directory exists
    try:
        PATTERNS_DIR.mkdir(parents=True, exist_ok=True)

        # Append to JSONL file (atomic append)
        with open(SEQUENCES_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        # Silent fail - observation should never break the main workflow
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
