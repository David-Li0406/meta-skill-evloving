#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["cchooks"]
# ///
"""PreToolUse hook template for Bash command validation.

Copy this template and customize for your plugin:
  cp ${CLAUDE_PLUGIN_ROOT}/skills/create-hook/templates/pretooluse-bash.py \
     your-plugin/hooks/your-hook.py

Then update your hooks/hooks.json to reference it.
"""

import re

from cchooks import PreToolUseContext, create_context


c = create_context()
assert isinstance(c, PreToolUseContext)

# Exit early if not the tool we care about
if c.tool_name != "Bash":
    c.output.exit_success()

command = c.tool_input.get("command", "")

# =============================================================================
# SAFE PATTERNS - Allow these to pass through
# =============================================================================
SAFE_PATTERNS: list[str] = [
    # Example: Allow rm -rf only in temp directories
    # r"rm\s+-rf\s+(/tmp/|/var/tmp/)",
]

# =============================================================================
# BLOCKED PATTERNS - Block these with explanatory messages
# =============================================================================
BLOCKED_PATTERNS: list[tuple[str, str]] = [
    # (pattern, reason_message)
    # Example:
    # (r"rm\s+-rf\s+/", "rm -rf on root is dangerous"),
]

# Check safe patterns first (allowlist before blocklist)
for pattern in SAFE_PATTERNS:
    if re.search(pattern, command):
        c.output.exit_success()

# Check blocked patterns
for pattern, reason in BLOCKED_PATTERNS:
    if re.search(pattern, command):
        c.output.exit_block(
            f"BLOCKED: {reason}\n"
            f"Command: {command}\n"
            "If this operation is truly needed, ask the user for explicit permission."
        )

# Allow everything else
c.output.exit_success()
