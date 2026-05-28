#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["cchooks"]
# ///
"""PostToolUse hook template for running actions after file edits.

Common uses:
- Auto-format code after edits
- Run linters
- Update related files

Copy this template and customize for your plugin:
  cp ${CLAUDE_PLUGIN_ROOT}/skills/create-hook/templates/posttooluse-edit.py \
     your-plugin/hooks/your-hook.py
"""

import subprocess
from pathlib import Path

from cchooks import PostToolUseContext, create_context


c = create_context()
assert isinstance(c, PostToolUseContext)

# Exit early if not the Edit tool
if c.tool_name != "Edit":
    c.output.exit_success()

file_path = c.tool_input.get("file_path", "")
if not file_path:
    c.output.exit_success()

path = Path(file_path)

# =============================================================================
# FILE TYPE HANDLERS
# =============================================================================

# Example: Format Python files with ruff
if path.suffix == ".py":
    try:
        subprocess.run(
            ["ruff", "format", file_path],
            check=False,  # Ignore non-zero exit codes
            capture_output=True,
            timeout=30,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass  # Don't fail if ruff isn't available

# Example: Format JavaScript/TypeScript with prettier
# if path.suffix in (".js", ".ts", ".jsx", ".tsx"):
#     try:
#         subprocess.run(
#             ["npx", "prettier", "--write", file_path],
#             capture_output=True,
#             timeout=30,
#         )
#     except (subprocess.TimeoutExpired, FileNotFoundError):
#         pass

c.output.exit_success()
