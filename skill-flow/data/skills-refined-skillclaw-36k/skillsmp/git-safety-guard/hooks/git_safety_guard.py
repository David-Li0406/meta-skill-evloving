#!/usr/bin/env python3
import json
import re
import sys

# Destructive patterns (best-effort; keep conservative to avoid false positives).
DESTRUCTIVE_PATTERNS = [
    (r"git\s+checkout\s+--\s+", "git checkout -- discards changes."),
    (r"git\s+restore\b", "git restore can discard changes."),
    (r"git\s+reset\s+--hard", "git reset --hard destroys changes."),
    (r"git\s+reset\s+--merge", "git reset --merge can lose changes."),
    (r"git\s+clean\s+-[a-z]*f", "git clean -f deletes files."),
    (r"git\s+push\b.*\s(--force|-f|--force-with-lease)\b", "git push --force rewrites remote history."),
    (r"git\s+branch\b.*\s-D\b", "git branch -D force-deletes a branch."),
    (r"git\s+stash\s+(drop|clear)\b", "git stash drop/clear permanently deletes stashes."),
    (r"rm\s+-[a-z]*r[a-z]*f", "rm -rf is destructive."),
]


def main() -> int:
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    command = input_data.get("tool_input", {}).get("command", "")
    if input_data.get("tool_name") != "Bash" or not command:
        return 0

    for pattern, reason in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": f"BLOCKED: {reason}\nCommand: {command}",
                        }
                    }
                )
            )
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
