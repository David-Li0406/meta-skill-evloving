---
title: Hook Examples
description: Eight complete working examples of different hook types for validation, automation, and context injection
keywords: hooks, examples, PreToolUse, PostToolUse, UserPromptSubmit, Stop, SessionStart, validation, automation
skill: creating-hooks
---

# Claude Code Hook Examples

This document provides complete, working examples of different hook types.

## Example 1: PreToolUse - Bash Command Validation

Validates bash commands before execution, providing helpful suggestions.

**Hook configuration** (add to `~/.claude/settings.json` or `.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate_bash.py"
          }
        ]
      }
    ]
  }
}
```

**Hook script** (`.claude/hooks/validate_bash.py`):

```python
#!/usr/bin/env python3
import json
import re
import sys

# Validation rules: (pattern, message)
VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance"
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "Use 'rg --files | rg pattern' instead of 'find -name' for better performance"
    ),
    (
        r"rm\s+-rf\s+/",
        "DANGER: Attempting to delete from root directory"
    ),
]

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(0)

# Validate the command
issues = []
for pattern, message in VALIDATION_RULES:
    if re.search(pattern, command):
        issues.append(message)

if issues:
    for message in issues:
        print(f"• {message}", file=sys.stderr)
    # Exit code 2 blocks tool call and shows stderr to Claude
    sys.exit(2)

# Exit 0 allows the command to proceed
sys.exit(0)
```

Make script executable: `chmod +x .claude/hooks/validate_bash.py`

## Example 2: PostToolUse - Auto-format After File Edit

Automatically formats code files after Write or Edit operations.

**Hook configuration**:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto_format.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Hook script** (`.claude/hooks/auto_format.py`):

```python
#!/usr/bin/env python3
import json
import subprocess
import sys
import os

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(1)

tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if not file_path or not os.path.exists(file_path):
    sys.exit(0)

# Determine formatter based on file extension
formatters = {
    ".py": ["black", "--quiet"],
    ".js": ["prettier", "--write"],
    ".ts": ["prettier", "--write"],
    ".go": ["gofmt", "-w"],
}

ext = os.path.splitext(file_path)[1]
if ext not in formatters:
    sys.exit(0)

formatter = formatters[ext]
try:
    subprocess.run(
        formatter + [file_path],
        capture_output=True,
        timeout=30,
        check=True
    )
    print(f"Formatted {file_path} with {formatter[0]}")
except subprocess.TimeoutExpired:
    print(f"Formatter timed out for {file_path}", file=sys.stderr)
    sys.exit(1)
except subprocess.CalledProcessError as e:
    print(f"Formatter failed: {e.stderr.decode()}", file=sys.stderr)
    sys.exit(2)  # Exit 2 shows error to Claude
except FileNotFoundError:
    # Formatter not installed, skip silently
    sys.exit(0)

sys.exit(0)
```

Make script executable: `chmod +x .claude/hooks/auto_format.py`

## Example 3: UserPromptSubmit - Inject Git Context

Adds current git status to every prompt automatically.

**Hook configuration**:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/inject_git_context.py"
          }
        ]
      }
    ]
  }
}
```

**Hook script** (`~/.claude/hooks/inject_git_context.py`):

```python
#!/usr/bin/env python3
import json
import subprocess
import sys
import os

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

# Check if we're in a git repository
cwd = input_data.get("cwd", os.getcwd())
try:
    subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=cwd,
        capture_output=True,
        check=True,
        timeout=5
    )
except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
    # Not a git repo or git not available
    sys.exit(0)

# Get git status
try:
    result = subprocess.run(
        ["git", "status", "--short", "--branch"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=5,
        check=True
    )
    git_status = result.stdout.strip()
except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
    sys.exit(0)

# Get current branch
try:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=5,
        check=True
    )
    branch = result.stdout.strip()
except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
    branch = "unknown"

# Output context (stdout with exit 0 is added to context for UserPromptSubmit)
if git_status:
    print(f"\n## Git Context\nCurrent branch: {branch}\n```\n{git_status}\n```\n")

sys.exit(0)
```

Make script executable: `chmod +x ~/.claude/hooks/inject_git_context.py`

## Example 4: PreToolUse - Auto-approve Documentation Reads

Automatically approves Read operations for documentation files.

**Hook configuration**:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/auto_approve_docs.py"
          }
        ]
      }
    ]
  }
}
```

**Hook script** (`~/.claude/hooks/auto_approve_docs.py`):

```python
#!/usr/bin/env python3
import json
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

# Auto-approve documentation file extensions
safe_extensions = (".md", ".mdx", ".txt", ".json", ".yaml", ".yml", ".toml")

if file_path.endswith(safe_extensions):
    # Use JSON output to auto-approve
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Documentation file auto-approved"
        },
        "suppressOutput": True
    }
    print(json.dumps(output))

sys.exit(0)
```

Make script executable: `chmod +x ~/.claude/hooks/auto_approve_docs.py`

## Example 5: SessionStart - Load Recent Changes

Injects recent git commits and changes at session start.

**Hook configuration**:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/load_recent_changes.py"
          }
        ]
      }
    ]
  }
}
```

**Hook script** (`.claude/hooks/load_recent_changes.py`):

```python
#!/usr/bin/env python3
import json
import subprocess
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

# Check if in git repo
try:
    subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        capture_output=True,
        check=True,
        timeout=5
    )
except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
    sys.exit(0)

# Get recent commits
try:
    result = subprocess.run(
        ["git", "log", "--oneline", "-10"],
        capture_output=True,
        text=True,
        timeout=5,
        check=True
    )
    recent_commits = result.stdout.strip()
except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
    recent_commits = "Unable to fetch commits"

# Get uncommitted changes
try:
    result = subprocess.run(
        ["git", "diff", "--stat"],
        capture_output=True,
        text=True,
        timeout=5,
        check=True
    )
    uncommitted = result.stdout.strip()
except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
    uncommitted = ""

# Output context (stdout with exit 0 is added to context for SessionStart)
context = f"""
## Recent Development Activity

### Last 10 Commits
```
{recent_commits}
```
"""

if uncommitted:
    context += f"""
### Uncommitted Changes
```
{uncommitted}
```
"""

print(context)
sys.exit(0)
```

Make script executable: `chmod +x .claude/hooks/load_recent_changes.py`

## Example 6: Stop - Verify Test Passage

Prevents Claude from stopping if tests are failing.

**Hook configuration**:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify_tests.py"
          }
        ]
      }
    ]
  }
}
```

**Hook script** (`.claude/hooks/verify_tests.py`):

```python
#!/usr/bin/env python3
import json
import subprocess
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

# Check if stop hook is already active to prevent infinite loops
if input_data.get("stop_hook_active", False):
    sys.exit(0)

# Run tests
try:
    result = subprocess.run(
        ["npm", "test"],
        capture_output=True,
        text=True,
        timeout=60
    )

    if result.returncode != 0:
        # Tests failed - block stoppage with JSON output
        output = {
            "decision": "block",
            "reason": f"Tests are failing. Please fix the following failures:\n\n{result.stdout}\n\n{result.stderr}"
        }
        print(json.dumps(output))
        sys.exit(0)

except subprocess.TimeoutExpired:
    print("Tests timed out - allowing stop", file=sys.stderr)
except FileNotFoundError:
    # npm not found, skip test check
    pass

sys.exit(0)
```

Make script executable: `chmod +x .claude/hooks/verify_tests.py`

## Example 7: PostToolUse - Block Sensitive File Writes

Provides feedback when sensitive files are written.

**Hook configuration**:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/check_sensitive_files.py"
          }
        ]
      }
    ]
  }
}
```

**Hook script** (`~/.claude/hooks/check_sensitive_files.py`):

```python
#!/usr/bin/env python3
import json
import sys
import os

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

# List of sensitive file patterns
sensitive_patterns = [
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.yaml",
    "id_rsa",
    "id_ed25519",
]

basename = os.path.basename(file_path)

if any(pattern in basename for pattern in sensitive_patterns):
    # Provide feedback to Claude about sensitive file
    output = {
        "decision": "block",
        "reason": f"Warning: {file_path} appears to be a sensitive file. Ensure no secrets are committed to version control. Consider adding to .gitignore.",
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"Sensitive file detected: {file_path}"
        }
    }
    print(json.dumps(output))

sys.exit(0)
```

Make script executable: `chmod +x ~/.claude/hooks/check_sensitive_files.py`

## Example 8: UserPromptSubmit - Block Prompts with Secrets

Validates prompts for potential secret exposure.

**Hook configuration**:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/validate_prompt_secrets.py"
          }
        ]
      }
    ]
  }
}
```

**Hook script** (`~/.claude/hooks/validate_prompt_secrets.py`):

```python
#!/usr/bin/env python3
import json
import sys
import re

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

prompt = input_data.get("prompt", "")

# Patterns that might indicate secrets
secret_patterns = [
    (r"(?i)\b(password|pwd)\s*[:=]\s*\S+", "Potential password detected"),
    (r"(?i)\b(api[_-]?key|apikey)\s*[:=]\s*\S+", "Potential API key detected"),
    (r"(?i)\b(secret|token)\s*[:=]\s*\S+", "Potential secret/token detected"),
    (r"\b[A-Za-z0-9]{40}\b", "Potential API token (40 chars) detected"),
]

for pattern, message in secret_patterns:
    if re.search(pattern, prompt):
        # Block the prompt with JSON output
        output = {
            "decision": "block",
            "reason": f"Security policy violation: {message}. Please rephrase without sensitive information."
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
```

Make script executable: `chmod +x ~/.claude/hooks/validate_prompt_secrets.py`

## Testing Hooks

### Manual Testing

1. **Test hook script directly:**
```bash
echo '{"session_id":"test","transcript_path":"","hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"grep foo"}}' | python3 .claude/hooks/validate_bash.py
```

2. **Test with debug mode:**
```bash
claude --debug
# Trigger the hook in conversation
# Check debug output for hook execution details
```

3. **Verify hook registration:**
```bash
# In Claude Code session
/hooks
# Check that your hook appears in the list
```

### Common Issues

**Hook not executing:**
- Verify hook is registered: `/hooks` command
- Check script is executable: `chmod +x script.py`
- Verify matcher pattern matches tool name (case-sensitive)
- Check for syntax errors in settings.json

**Hook timing out:**
- Default timeout is 60 seconds
- Increase timeout in hook configuration: `"timeout": 120`
- Optimize hook script performance

**Wrong output behavior:**
- Review exit codes (0=success, 2=blocking error)
- Check if using stdout vs stderr correctly
- Verify JSON output structure matches schemas

## Hook Best Practices

1. **Performance**: Keep hooks fast (<1 second when possible)
2. **Error handling**: Always catch exceptions and handle gracefully
3. **Timeouts**: Set appropriate timeouts for external commands
4. **Logging**: Use stderr for errors, stdout for output/context
5. **Testing**: Test hooks manually before relying on them
6. **Security**: Validate and sanitize all inputs
7. **Idempotency**: Hooks should be safe to run multiple times
8. **Exit codes**: Use exit codes consistently for communication
