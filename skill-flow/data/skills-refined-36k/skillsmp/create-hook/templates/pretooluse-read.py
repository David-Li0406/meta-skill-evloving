#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["cchooks"]
# ///
"""PreToolUse hook template for Read tool validation.

Use this to protect sensitive files from being read.

Copy this template and customize for your plugin:
  cp ${CLAUDE_PLUGIN_ROOT}/skills/create-hook/templates/pretooluse-read.py \
     your-plugin/hooks/your-hook.py
"""

import re

from cchooks import PreToolUseContext, create_context


c = create_context()
assert isinstance(c, PreToolUseContext)

# Exit early if not the Read tool
if c.tool_name != "Read":
    c.output.exit_success()

file_path = c.tool_input.get("file_path", "")

# =============================================================================
# PROTECTED PATTERNS - Files that should never be read
# =============================================================================
PROTECTED_PATTERNS: list[tuple[str, str]] = [
    # (pattern, reason_message)
    # Example: Protect .env files
    # (r"\.env($|\.)", "Environment files may contain secrets"),
    # (r"credentials\.json$", "Credentials files should not be read"),
]

# Check protected patterns
for pattern, reason in PROTECTED_PATTERNS:
    if re.search(pattern, file_path):
        c.output.exit_block(
            f"BLOCKED: {reason}\n"
            f"File: {file_path}\n"
            "If you need this file's contents, ask the user to provide them."
        )

# Allow everything else
c.output.exit_success()
