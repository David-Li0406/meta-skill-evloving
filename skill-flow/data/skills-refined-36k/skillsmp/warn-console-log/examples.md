# Hook Examples

Complete Python hook examples for common use cases.

## Python PreToolUse Validator

Block dangerous commands before execution:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
import json
import re
import sys

BLOCKED_PATTERNS = [
    (r"\brm\s+-rf\b", "Blocked: rm -rf is dangerous"),
    (r"--force\b", "Blocked: --force operations disabled"),
]

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

command = data.get("tool_input", {}).get("command", "")

for pattern, message in BLOCKED_PATTERNS:
    if re.search(pattern, command, re.I):
        print(message, file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

## Python UserPromptSubmit with Context

Add context to every user prompt:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
import json
import sys
import datetime

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

# Add context to conversation
context = f"Current time: {datetime.datetime.now()}"
print(context)

sys.exit(0)
```

## Auto-Approve Documentation Files

Automatically approve read access to documentation:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
import json
import sys

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

tool_name = data.get("tool_name", "")
file_path = data.get("tool_input", {}).get("file_path", "")

if tool_name == "Read" and file_path.endswith((".md", ".txt", ".json")):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Documentation auto-approved"
        },
        "suppressOutput": True
    }
    print(json.dumps(output))

sys.exit(0)
```

## Schema Change Notification

Notify when database schema files are modified:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
import json
import sys

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

file_path = data.get("tool_input", {}).get("file_path", "")

if "schema" in file_path and file_path.endswith(".ts"):
    print("Schema modified. Remember to run: pnpm db:generate")

sys.exit(0)
```

## Protected File Blocker

Block modifications to sensitive files:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
import json
import sys
from pathlib import Path

PROTECTED_PATTERNS = [
    ".env",
    ".env.local",
    "credentials",
    "secrets",
    ".git/",
]

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

file_path = data.get("tool_input", {}).get("file_path", "")

for pattern in PROTECTED_PATTERNS:
    if pattern in file_path:
        print(f"Blocked: Cannot modify protected file ({pattern})", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
```

## Post-Write Formatter

Format files after writing:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
import json
import subprocess
import sys
from pathlib import Path

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

file_path = data.get("tool_input", {}).get("file_path", "")

if not file_path or not Path(file_path).exists():
    sys.exit(0)

# Format based on file type
if file_path.endswith((".ts", ".tsx", ".js", ".jsx")):
    subprocess.run(["npx", "prettier", "--write", file_path], capture_output=True)
elif file_path.endswith(".py"):
    subprocess.run(["ruff", "format", file_path], capture_output=True)
elif file_path.endswith(".md"):
    subprocess.run(["npx", "markdownlint", "--fix", file_path], capture_output=True)

sys.exit(0)
```
