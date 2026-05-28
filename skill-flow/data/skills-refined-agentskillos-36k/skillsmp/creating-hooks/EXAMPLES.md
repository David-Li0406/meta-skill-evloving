# Hook Examples

Copy-paste examples for common Claude Code hook use cases.

Each example includes:
- Use case description
- Complete JSON config (ready to paste into settings.json)
- Script file (if needed)
- Expected behavior
- Testing instructions

---

## Example 1: Auto-Lint After File Writes

**Use Case:** Automatically run Prettier and ESLint after Claude writes or edits files.

**Hook Event:** `PostToolUse`

### JSON Configuration

Add to `~/.claude/settings.json` or `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/auto-lint.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Script File

Create `.claude/hooks/auto-lint.sh`:

```bash
#!/bin/bash

# Read hook input from stdin
INPUT=$(cat)

# Extract the file path from the tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.filePath // empty')

# Exit if no file path found
if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Only lint supported file types
case "$FILE_PATH" in
  *.js|*.jsx|*.ts|*.tsx|*.json|*.md|*.css|*.scss)
    ;;
  *)
    exit 0
    ;;
esac

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Run Prettier (if available)
if command -v prettier &> /dev/null || [ -f "$CLAUDE_PROJECT_DIR/node_modules/.bin/prettier" ]; then
  npx prettier --write "$FILE_PATH" 2>/dev/null
fi

# Run ESLint with auto-fix (if available and applicable)
case "$FILE_PATH" in
  *.js|*.jsx|*.ts|*.tsx)
    if command -v eslint &> /dev/null || [ -f "$CLAUDE_PROJECT_DIR/node_modules/.bin/eslint" ]; then
      npx eslint --fix "$FILE_PATH" 2>/dev/null
    fi
    ;;
esac

exit 0
```

Make executable:

```bash
chmod +x .claude/hooks/auto-lint.sh
```

### Expected Behavior

- After every `Write` or `Edit` tool call, the script runs
- Prettier formats the file (if applicable)
- ESLint fixes auto-fixable issues (for JS/TS files)
- Exit code 0 allows Claude to continue normally

### Testing Instructions

1. Start Claude Code: `claude`
2. Ask Claude to create a file: "Create a file test.js with a simple function"
3. Check that the file is formatted
4. Verify in verbose mode (Ctrl+O) that the hook ran

---

## Example 2: Validate Bash Commands

**Use Case:** Block dangerous bash commands before execution.

**Hook Event:** `PreToolUse`

### JSON Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-bash.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Script File

Create `.claude/hooks/validate-bash.py`:

```python
#!/usr/bin/env python3
"""
Validate bash commands before execution.
Exit code 2 blocks the command and shows stderr to Claude.
"""
import json
import sys
import re

# Dangerous command patterns
BLOCKED_PATTERNS = [
    # Destructive commands
    (r"\brm\s+(-rf?|--recursive)\s+[/~]", "Blocking recursive delete on root or home"),
    (r"\brm\s+-rf?\s+\*", "Blocking recursive delete with wildcard"),
    (r">\s*/dev/sd[a-z]", "Blocking direct disk writes"),
    (r"\bmkfs\b", "Blocking filesystem formatting"),
    (r"\bdd\s+.*of=/dev", "Blocking dd to disk devices"),

    # System-level dangers
    (r"chmod\s+(-R\s+)?777\s+/", "Blocking chmod 777 on system paths"),
    (r"\b:(){ :|:& };:", "Blocking fork bombs"),
    (r">\s*/etc/passwd", "Blocking writes to /etc/passwd"),
    (r">\s*/etc/shadow", "Blocking writes to /etc/shadow"),

    # Network dangers (optional - uncomment if needed)
    # (r"\bcurl\b.*\|\s*bash", "Blocking curl pipe to bash"),
    # (r"\bwget\b.*\|\s*bash", "Blocking wget pipe to bash"),

    # Git dangers
    (r"git\s+push\s+.*--force\s+.*\b(main|master)\b", "Blocking force push to main/master"),
    (r"git\s+push\s+-f\s+.*\b(main|master)\b", "Blocking force push to main/master"),
]

# Warning patterns (don't block, just warn)
WARNING_PATTERNS = [
    (r"\brm\s+-r", "Warning: recursive delete detected"),
    (r"\bsudo\b", "Warning: sudo command detected"),
]


def validate_command(command: str) -> tuple[bool, str]:
    """
    Validate a bash command.
    Returns (is_blocked, message).
    """
    for pattern, message in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, message
    return False, ""


def check_warnings(command: str) -> list[str]:
    """Check for warning patterns."""
    warnings = []
    for pattern, message in WARNING_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            warnings.append(message)
    return warnings


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    # Only validate Bash commands
    if tool_name != "Bash" or not command:
        sys.exit(0)

    # Check for blocked commands
    is_blocked, message = validate_command(command)
    if is_blocked:
        print(f"BLOCKED: {message}", file=sys.stderr)
        print(f"Command: {command[:100]}...", file=sys.stderr)
        # Exit code 2 blocks the tool call
        sys.exit(2)

    # Check for warnings (non-blocking)
    warnings = check_warnings(command)
    if warnings:
        for warning in warnings:
            print(warning, file=sys.stdout)

    sys.exit(0)


if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x .claude/hooks/validate-bash.py
```

### Expected Behavior

- Dangerous commands (rm -rf /, force push to main) are blocked
- Claude receives the error message and can adjust its approach
- Warning patterns allow execution but log a message
- Safe commands proceed normally

### Testing Instructions

1. Start Claude Code: `claude`
2. Ask: "Delete everything in the root folder"
3. Claude should be blocked from running `rm -rf /`
4. The hook error message guides Claude to use a safer approach

---

## Example 3: Inject Context at Session Start

**Use Case:** Load recent git commits and environment info when starting a session.

**Hook Event:** `SessionStart`

### JSON Configuration

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/session-context.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Script File

Create `.claude/hooks/session-context.sh`:

```bash
#!/bin/bash

# Session context injection script
# Outputs context that Claude will see at session start

echo "=== Session Context ==="
echo ""

# Current date and time
echo "**Date:** $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""

# Git branch info
if git rev-parse --git-dir > /dev/null 2>&1; then
  BRANCH=$(git branch --show-current 2>/dev/null)
  echo "**Git Branch:** $BRANCH"

  # Recent commits
  echo ""
  echo "**Recent Commits (last 5):**"
  echo '```'
  git log --oneline -5 2>/dev/null
  echo '```'

  # Uncommitted changes summary
  CHANGES=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  if [ "$CHANGES" -gt 0 ]; then
    echo ""
    echo "**Uncommitted Changes:** $CHANGES files"
    echo '```'
    git status --short 2>/dev/null | head -10
    if [ "$CHANGES" -gt 10 ]; then
      echo "... and $((CHANGES - 10)) more"
    fi
    echo '```'
  fi
fi

# Node.js version (if applicable)
if command -v node &> /dev/null; then
  echo ""
  echo "**Node.js:** $(node --version)"
fi

# Bun version (if applicable)
if command -v bun &> /dev/null; then
  echo "**Bun:** $(bun --version)"
fi

# Check for TODO comments in recently modified files
if git rev-parse --git-dir > /dev/null 2>&1; then
  RECENT_FILES=$(git diff --name-only HEAD~5 2>/dev/null | head -20)
  if [ -n "$RECENT_FILES" ]; then
    TODO_COUNT=$(echo "$RECENT_FILES" | xargs grep -l "TODO\|FIXME" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$TODO_COUNT" -gt 0 ]; then
      echo ""
      echo "**Files with TODOs:** $TODO_COUNT recently modified files contain TODO/FIXME comments"
    fi
  fi
fi

echo ""
echo "=== End Context ==="

exit 0
```

Make executable:

```bash
chmod +x .claude/hooks/session-context.sh
```

### Expected Behavior

- Every time Claude Code starts or resumes, context is injected
- Claude sees current git branch, recent commits, and uncommitted changes
- Environment info (Node/Bun versions) is available
- Claude is aware of TODOs in recently modified files

### Testing Instructions

1. Start Claude Code: `claude`
2. The context should appear in the session
3. Ask Claude: "What was the last commit?"
4. Claude should know from the injected context

### Variant: Persist Environment Variables

If you need to set environment variables for the session:

```bash
#!/bin/bash

# Persist environment variables for the session
if [ -n "$CLAUDE_ENV_FILE" ]; then
  # Load .env file if it exists
  if [ -f "$CLAUDE_PROJECT_DIR/.env" ]; then
    while IFS='=' read -r key value; do
      # Skip comments and empty lines
      [[ "$key" =~ ^#.*$ ]] && continue
      [[ -z "$key" ]] && continue
      echo "export $key=\"$value\"" >> "$CLAUDE_ENV_FILE"
    done < "$CLAUDE_PROJECT_DIR/.env"
  fi

  # Set custom environment variables
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

---

## Example 4: Auto-Approve Safe Tools

**Use Case:** Automatically approve safe read-only tools while requiring permission for dangerous ones.

**Hook Event:** `PermissionRequest`

### JSON Configuration

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Read|Glob|Grep",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PermissionRequest\",\"decision\":{\"behavior\":\"allow\"}}}'",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/permission-check.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Script File

Create `.claude/hooks/permission-check.py`:

```python
#!/usr/bin/env python3
"""
Intelligent permission handling for tools.
Auto-approves safe operations, denies dangerous ones, prompts for others.
"""
import json
import sys
import os
import re

# Patterns for auto-approval
SAFE_WRITE_PATTERNS = [
    r"\.test\.(ts|js|tsx|jsx)$",  # Test files
    r"\.spec\.(ts|js|tsx|jsx)$",  # Spec files
    r"__tests__/",                 # Test directories
    r"\.md$",                      # Markdown files
    r"\.json$",                    # JSON files (careful with package.json)
    r"\.claude/",                  # Claude config files
]

# Patterns to always deny
DENY_PATTERNS = [
    r"\.env$",                     # Environment files
    r"\.env\.",                    # .env.local, .env.production, etc.
    r"secrets?\.(json|ya?ml)$",   # Secret files
    r"credentials",               # Credential files
    r"\.pem$",                    # Private keys
    r"\.key$",                    # Key files
]

# Safe bash commands (auto-approve)
SAFE_BASH_PATTERNS = [
    r"^(ls|cat|head|tail|grep|rg|find|echo|pwd|which|type)\s",
    r"^git\s+(status|log|diff|branch|show)",
    r"^(npm|yarn|pnpm|bun)\s+(list|outdated|info)",
    r"^(node|python|bun)\s+--version",
]


def is_safe_write(file_path: str) -> bool:
    """Check if a file write is safe to auto-approve."""
    for pattern in DENY_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return False

    for pattern in SAFE_WRITE_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return True

    return False  # Default to asking


def is_safe_bash(command: str) -> bool:
    """Check if a bash command is safe to auto-approve."""
    for pattern in SAFE_BASH_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


def is_denied_write(file_path: str) -> tuple[bool, str]:
    """Check if a file write should be denied."""
    for pattern in DENY_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return True, f"Writing to sensitive file pattern: {pattern}"
    return False, ""


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    result = {"hookSpecificOutput": {"hookEventName": "PermissionRequest"}}

    if tool_name in ["Write", "Edit"]:
        file_path = tool_input.get("file_path", "")

        # Check if denied
        is_denied, reason = is_denied_write(file_path)
        if is_denied:
            result["hookSpecificOutput"]["decision"] = {
                "behavior": "deny",
                "message": reason
            }
            print(json.dumps(result))
            sys.exit(0)

        # Check if safe to auto-approve
        if is_safe_write(file_path):
            result["hookSpecificOutput"]["decision"] = {"behavior": "allow"}
            print(json.dumps(result))
            sys.exit(0)

        # Default: let user decide (do nothing, permission dialog shows)

    elif tool_name == "Bash":
        command = tool_input.get("command", "")

        if is_safe_bash(command):
            result["hookSpecificOutput"]["decision"] = {"behavior": "allow"}
            print(json.dumps(result))
            sys.exit(0)

        # Default: let user decide

    # No decision = let the normal permission flow proceed
    sys.exit(0)


if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x .claude/hooks/permission-check.py
```

### Expected Behavior

- `Read`, `Glob`, `Grep` are always auto-approved
- Test file writes are auto-approved
- `.env` and secret file writes are always denied
- Bash commands like `ls`, `git status` are auto-approved
- Other operations show the normal permission dialog

### Testing Instructions

1. Start Claude Code: `claude`
2. Ask: "Read the README.md file" - should auto-approve
3. Ask: "Create a test file test.spec.ts" - should auto-approve
4. Ask: "Create .env.local with secrets" - should be denied
5. Ask: "Run rm -rf node_modules" - should show permission dialog

---

## Example 5: Check Work Completion (Stop Hook)

**Use Case:** Verify Claude has actually completed the task before stopping.

**Hook Event:** `Stop`

### JSON Configuration (Command-based)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-completion.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Script File

Create `.claude/hooks/check-completion.py`:

```python
#!/usr/bin/env python3
"""
Check if Claude has completed the task before stopping.
Uses heuristics to detect incomplete work.
"""
import json
import sys


def check_completion(input_data: dict) -> tuple[bool, str]:
    """
    Check if work appears complete.
    Returns (should_block, reason).
    """
    # If this is already a continuation from stop hook, allow stopping
    # to prevent infinite loops
    if input_data.get("stop_hook_active", False):
        return False, ""

    # Read the transcript to check for incomplete work markers
    transcript_path = input_data.get("transcript_path", "")
    if not transcript_path:
        return False, ""

    try:
        # Read the transcript file
        with open(transcript_path, "r") as f:
            content = f.read()

        # Check for incomplete work markers in Claude's recent output
        incomplete_markers = [
            "I'll continue",
            "Let me continue",
            "I'll now",
            "Next, I'll",
            "I should also",
            "I still need to",
            "TODO:",
            "FIXME:",
            "remaining task",
            "haven't yet",
        ]

        # Check last portion of transcript
        recent_content = content[-5000:] if len(content) > 5000 else content

        for marker in incomplete_markers:
            if marker.lower() in recent_content.lower():
                return True, f"Detected incomplete work marker: '{marker}'. Please complete the task."

        # Check for error patterns that weren't addressed
        error_markers = [
            "error:",
            "failed:",
            "exception:",
            "traceback",
        ]

        # Only check very recent content for errors
        very_recent = content[-2000:] if len(content) > 2000 else content
        for marker in error_markers:
            if marker.lower() in very_recent.lower():
                # Check if there's a fix after the error
                error_pos = very_recent.lower().rfind(marker.lower())
                after_error = very_recent[error_pos:]

                fix_markers = ["fixed", "resolved", "corrected", "works now"]
                if not any(fix.lower() in after_error.lower() for fix in fix_markers):
                    return True, f"Detected unresolved error. Please address it before stopping."

    except Exception as e:
        # If we can't read the transcript, allow stopping
        return False, ""

    return False, ""


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    should_block, reason = check_completion(input_data)

    if should_block:
        # Output JSON to block stopping
        result = {
            "decision": "block",
            "reason": reason
        }
        print(json.dumps(result))
        sys.exit(0)

    # Allow stopping
    sys.exit(0)


if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x .claude/hooks/check-completion.py
```

### Alternative: Prompt-Based Stop Hook

For more intelligent evaluation, use a prompt-based hook:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working.\n\nContext: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors occurred that need fixing\n3. Any follow-up work was promised but not done\n4. Tests pass (if applicable)\n\nIf work is incomplete, respond with:\n{\"decision\": \"block\", \"reason\": \"Specific explanation of what's incomplete\"}\n\nIf work is complete, respond with:\n{\"decision\": \"approve\", \"reason\": \"All tasks completed\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Expected Behavior

- Command-based: Uses heuristics to detect incomplete work markers
- Prompt-based: Uses LLM to intelligently evaluate completion
- If incomplete, Claude continues working
- Prevents premature stopping with "I'll continue..." then stopping
- Has loop protection via `stop_hook_active` flag

### Testing Instructions

1. Start Claude Code: `claude`
2. Give a multi-step task: "Create a utility function and write tests for it"
3. If Claude tries to stop early, the hook should force continuation
4. Claude should complete both parts before stopping

---

## Example 6: Log Session Activity

**Use Case:** Write a session summary and track tool usage when the session ends.

**Hook Event:** `SessionEnd`

### JSON Configuration

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/log-session.py",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

### Script File

Create `.claude/hooks/log-session.py`:

```python
#!/usr/bin/env python3
"""
Log session activity when Claude Code ends.
Creates a summary of the session including tool usage statistics.
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import Counter


def parse_transcript(transcript_path: str) -> dict:
    """Parse the transcript to extract session statistics."""
    stats = {
        "tool_usage": Counter(),
        "files_read": set(),
        "files_written": set(),
        "files_edited": set(),
        "bash_commands": [],
        "errors": [],
        "total_messages": 0,
    }

    if not transcript_path or not os.path.exists(transcript_path):
        return stats

    try:
        with open(transcript_path, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                stats["total_messages"] += 1

                # Check for tool use
                if entry.get("type") == "tool_use":
                    tool_name = entry.get("name", "unknown")
                    stats["tool_usage"][tool_name] += 1

                    tool_input = entry.get("input", {})

                    if tool_name == "Read":
                        file_path = tool_input.get("file_path", "")
                        if file_path:
                            stats["files_read"].add(file_path)

                    elif tool_name == "Write":
                        file_path = tool_input.get("file_path", "")
                        if file_path:
                            stats["files_written"].add(file_path)

                    elif tool_name == "Edit":
                        file_path = tool_input.get("file_path", "")
                        if file_path:
                            stats["files_edited"].add(file_path)

                    elif tool_name == "Bash":
                        command = tool_input.get("command", "")
                        if command:
                            stats["bash_commands"].append(command[:100])

                # Check for errors
                if entry.get("type") == "tool_result":
                    is_error = entry.get("is_error", False)
                    if is_error:
                        content = entry.get("content", "")[:200]
                        stats["errors"].append(content)

    except Exception as e:
        stats["parse_error"] = str(e)

    return stats


def write_session_log(input_data: dict, stats: dict):
    """Write session log to file."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    log_dir = Path(project_dir) / ".claude" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    session_id = input_data.get("session_id", "unknown")
    reason = input_data.get("reason", "unknown")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    log_file = log_dir / f"session_{timestamp}_{session_id[:8]}.md"

    content = f"""# Session Log

**Session ID:** {session_id}
**End Time:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**End Reason:** {reason}

## Tool Usage Summary

| Tool | Count |
|------|-------|
"""

    for tool, count in sorted(stats["tool_usage"].items(), key=lambda x: -x[1]):
        content += f"| {tool} | {count} |\n"

    content += f"""
## Files Accessed

### Read ({len(stats['files_read'])} files)
"""
    for f in sorted(stats["files_read"]):
        content += f"- `{f}`\n"

    content += f"""
### Written ({len(stats['files_written'])} files)
"""
    for f in sorted(stats["files_written"]):
        content += f"- `{f}`\n"

    content += f"""
### Edited ({len(stats['files_edited'])} files)
"""
    for f in sorted(stats["files_edited"]):
        content += f"- `{f}`\n"

    if stats["bash_commands"]:
        content += f"""
## Bash Commands ({len(stats['bash_commands'])} total)

```
"""
        for cmd in stats["bash_commands"][:20]:  # Limit to first 20
            content += f"{cmd}\n"
        if len(stats["bash_commands"]) > 20:
            content += f"... and {len(stats['bash_commands']) - 20} more\n"
        content += "```\n"

    if stats["errors"]:
        content += f"""
## Errors Encountered ({len(stats['errors'])})

"""
        for i, error in enumerate(stats["errors"][:10], 1):
            content += f"{i}. `{error}`\n"

    content += f"""
---
*Log generated automatically by session-end hook*
"""

    with open(log_file, "w") as f:
        f.write(content)

    return log_file


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse transcript
    transcript_path = input_data.get("transcript_path", "")
    stats = parse_transcript(transcript_path)

    # Write log
    log_file = write_session_log(input_data, stats)

    # Output summary to stdout (shown in debug mode)
    print(f"Session log written to: {log_file}")
    print(f"Total tools used: {sum(stats['tool_usage'].values())}")
    print(f"Files modified: {len(stats['files_written']) + len(stats['files_edited'])}")

    sys.exit(0)


if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x .claude/hooks/log-session.py
```

### Expected Behavior

- When Claude Code session ends, a markdown log is created
- Log includes tool usage counts, files accessed, bash commands run
- Logs are stored in `.claude/logs/session_<timestamp>_<id>.md`
- Useful for auditing, debugging, and tracking productivity

### Testing Instructions

1. Start Claude Code: `claude`
2. Do some work (read files, make edits, run commands)
3. Exit Claude Code (type "exit" or Ctrl+C)
4. Check `.claude/logs/` for the session log
5. Review the generated markdown summary

---

## Example 7: Custom Notification Handler

**Use Case:** Send desktop notifications or Slack messages when Claude needs attention.

**Hook Event:** `Notification`

### JSON Configuration

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/notify.sh permission"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/notify.sh idle"
          }
        ]
      }
    ]
  }
}
```

### Script File

Create `.claude/hooks/notify.sh`:

```bash
#!/bin/bash

# Notification handler for Claude Code
# Usage: notify.sh <type>
# Types: permission, idle

NOTIFICATION_TYPE="${1:-unknown}"
INPUT=$(cat)
MESSAGE=$(echo "$INPUT" | jq -r '.message // "Claude Code needs attention"')

# Function for macOS notifications
notify_macos() {
  local title="$1"
  local message="$2"
  osascript -e "display notification \"$message\" with title \"$title\" sound name \"Ping\""
}

# Function for Linux notifications (requires notify-send)
notify_linux() {
  local title="$1"
  local message="$2"
  if command -v notify-send &> /dev/null; then
    notify-send "$title" "$message" --urgency=normal
  fi
}

# Function to send Slack notification (optional)
notify_slack() {
  local message="$1"
  local webhook_url="${SLACK_WEBHOOK_URL:-}"

  if [ -n "$webhook_url" ]; then
    curl -s -X POST -H 'Content-type: application/json' \
      --data "{\"text\":\"$message\"}" \
      "$webhook_url" > /dev/null 2>&1
  fi
}

# Determine notification title based on type
case "$NOTIFICATION_TYPE" in
  permission)
    TITLE="Claude Code - Permission Required"
    ;;
  idle)
    TITLE="Claude Code - Waiting for Input"
    ;;
  *)
    TITLE="Claude Code"
    ;;
esac

# Send notification based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
  notify_macos "$TITLE" "$MESSAGE"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  notify_linux "$TITLE" "$MESSAGE"
fi

# Optionally send to Slack
# notify_slack "$TITLE: $MESSAGE"

exit 0
```

Make executable:

```bash
chmod +x .claude/hooks/notify.sh
```

### Expected Behavior

- When Claude needs permission, you get a desktop notification
- When Claude has been idle 60+ seconds waiting for input, you're notified
- Works on macOS (via osascript) and Linux (via notify-send)
- Optional Slack integration via webhook

### Testing Instructions

1. Set up the hook and script
2. Start Claude Code: `claude`
3. Ask Claude to do something requiring permission
4. You should see/hear a desktop notification
5. For Slack: Set `SLACK_WEBHOOK_URL` environment variable

---

## Example 8: Pre-Compact Context Preservation

**Use Case:** Save important context before auto-compact to prevent information loss.

**Hook Event:** `PreCompact`

### JSON Configuration

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/preserve-context.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Script File

Create `.claude/hooks/preserve-context.py`:

```python
#!/usr/bin/env python3
"""
Preserve important context before auto-compact.
Extracts key decisions, TODOs, and state from the transcript.
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path


def extract_important_context(transcript_path: str) -> dict:
    """Extract important context from transcript before compact."""
    context = {
        "decisions": [],
        "todos": [],
        "file_changes": [],
        "key_info": [],
    }

    if not transcript_path or not os.path.exists(transcript_path):
        return context

    try:
        with open(transcript_path, "r") as f:
            content = f.read()

        lines = content.split('\n')

        for line in lines:
            try:
                entry = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            # Look for assistant messages with decisions
            if entry.get("type") == "assistant" and entry.get("content"):
                text = str(entry.get("content", ""))

                # Extract decisions
                if any(marker in text.lower() for marker in ["decided to", "decision:", "we'll use", "choosing"]):
                    # Get a snippet around the decision
                    for sentence in text.split('.'):
                        if any(m in sentence.lower() for m in ["decided", "decision", "we'll use", "choosing"]):
                            context["decisions"].append(sentence.strip()[:200])

                # Extract TODOs mentioned
                if "todo" in text.lower() or "need to" in text.lower():
                    for sentence in text.split('.'):
                        if "todo" in sentence.lower() or "need to" in sentence.lower():
                            context["todos"].append(sentence.strip()[:200])

            # Track file changes
            if entry.get("type") == "tool_use":
                tool_name = entry.get("name", "")
                tool_input = entry.get("input", {})

                if tool_name in ["Write", "Edit"]:
                    file_path = tool_input.get("file_path", "")
                    if file_path:
                        context["file_changes"].append(file_path)

    except Exception as e:
        context["error"] = str(e)

    return context


def save_context(context: dict):
    """Save extracted context to a file."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    context_dir = Path(project_dir) / ".claude" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    context_file = context_dir / f"pre-compact_{timestamp}.json"

    with open(context_file, "w") as f:
        json.dump(context, f, indent=2)

    return context_file


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    transcript_path = input_data.get("transcript_path", "")

    # Extract important context
    context = extract_important_context(transcript_path)

    # Save to file
    context_file = save_context(context)

    # Output summary
    print(f"Context preserved to: {context_file}")
    print(f"Decisions: {len(context.get('decisions', []))}")
    print(f"TODOs: {len(context.get('todos', []))}")
    print(f"Files changed: {len(context.get('file_changes', []))}")

    sys.exit(0)


if __name__ == "__main__":
    main()
```

Make executable:

```bash
chmod +x .claude/hooks/preserve-context.py
```

### Expected Behavior

- Before auto-compact triggers, important context is extracted
- Decisions, TODOs, and file changes are saved to `.claude/context/`
- Context can be reviewed or re-injected in future sessions
- Helps prevent loss of important information during long sessions

### Testing Instructions

1. Start Claude Code: `claude`
2. Have a long conversation that triggers auto-compact
3. Or manually trigger: `/compact`
4. Check `.claude/context/` for the preserved context file

---

## Quick Reference

| Example | Hook Event | Purpose |
|---------|------------|---------|
| Auto-lint | `PostToolUse` | Format files after writes |
| Validate bash | `PreToolUse` | Block dangerous commands |
| Session context | `SessionStart` | Inject git info, env vars |
| Auto-approve | `PermissionRequest` | Auto-allow safe tools |
| Check completion | `Stop` | Verify work is done |
| Log activity | `SessionEnd` | Track session statistics |
| Notifications | `Notification` | Desktop/Slack alerts |
| Preserve context | `PreCompact` | Save info before compact |

## Exit Code Reference

| Exit Code | Behavior |
|-----------|----------|
| 0 | Success - stdout processed (JSON or plain text) |
| 2 | Block/Error - stderr shown to Claude |
| Other | Non-blocking error - stderr logged |

## JSON Output Quick Reference

```python
# PreToolUse - Allow
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}

# PreToolUse - Deny
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "reason"}}

# PermissionRequest - Allow
{"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": {"behavior": "allow"}}}

# PermissionRequest - Deny
{"hookSpecificOutput": {"hookEventName": "PermissionRequest", "decision": {"behavior": "deny", "message": "reason"}}}

# Stop - Block
{"decision": "block", "reason": "Continue because..."}

# Stop - Allow (or just exit 0)
{"decision": "approve"}

# SessionStart - Add context
{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "Your context here"}}
```
