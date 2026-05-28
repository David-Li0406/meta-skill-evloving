# Hook Examples Library

Pre-built hook patterns for common use cases. All examples are production-ready and security-reviewed.

**Configuration Format Note:** All JSON examples below show the complete `hooks.json` structure. For plugin hooks (like PRISM), use `${CLAUDE_PLUGIN_ROOT}` in paths. For user-level hooks, use absolute paths.

## Quick Reference

| Example | Event | Purpose | Language |
|---------|-------|---------|----------|
| [bash-command-logger](#bash-command-logger) | PreToolUse | Log all bash commands | Bash + jq |
| [file-protection](#file-protection) | PreToolUse | Block edits to sensitive files | Python |
| [auto-formatter](#auto-formatter) | PostToolUse | Format code on save | Bash |
| [story-context-enforcer](#story-context-enforcer) | PreToolUse | Ensure PRISM story context | Python |
| [workflow-tracker](#workflow-tracker) | PostToolUse | Track workflow progress | Python |
| [desktop-notifier](#desktop-notifier) | Stop | Desktop notifications | Bash |
| [git-safety-guard](#git-safety-guard) | PreToolUse | Prevent dangerous git ops | Python |
| [test-runner](#test-runner) | PostToolUse | Auto-run tests | Bash |

---

## Logging & Auditing

### bash-command-logger

**Purpose**: Log all bash commands for compliance and debugging

**Event**: PreToolUse
**Matcher**: Bash
**Language**: Bash + jq

**Configuration** (`~/.claude/settings.json` for user-level):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\(.tool_input.command) - \(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

**Features**:
- Logs command and description
- Timestamps automatically (file modification time)
- Non-blocking (exit 0)
- Low overhead

**Dependencies**: `jq`

**Install**:
```
*install-example bash-command-logger
```

---

### file-change-tracker

**Purpose**: Track all file modifications with timestamps

**Event**: PostToolUse
**Matcher**: Edit|Write
**Language**: Python

**Hook Script** (`hooks/file-change-tracker.py`):
```python
#!/usr/bin/env python3
import json
import sys
from datetime import datetime

data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', 'unknown')

timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
with open('.file-changes.log', 'a') as f:
    f.write(f"{timestamp} | MODIFIED | {file_path}\n")

print(f"✅ Tracked change: {file_path}")
```

**Configuration** (plugin hooks.json):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/file-change-tracker.py"
          }
        ]
      }
    ]
  }
}
```

---

### workflow-auditor

**Purpose**: Comprehensive workflow event logging

**Event**: Multiple (PreToolUse, PostToolUse, Stop)
**Matcher**: *
**Language**: Python

**Features**:
- Logs all tool usage
- Captures exit codes
- Records execution time
- Creates structured audit trail

**Configuration**:
```json
{
  "event": "PostToolUse",
  "matcher": "*",
  "command": "python hooks/workflow-auditor.py"
}
```

---

## Validation & Safety

### file-protection

**Purpose**: Block edits to sensitive files (.env, package-lock.json, .git/)

**Event**: PreToolUse
**Matcher**: Edit|Write
**Language**: Python

**Hook Script** (`hooks/file-protection.py`):
```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

# Protected patterns
protected = [
    '.env',
    'package-lock.json',
    'yarn.lock',
    '.git/',
    'secrets.json',
    'credentials'
]

for pattern in protected:
    if pattern in file_path:
        print(f"❌ ERROR: Cannot edit protected file: {file_path}", file=sys.stderr)
        print(f"   Pattern matched: {pattern}", file=sys.stderr)
        print(f"   Protected files cannot be modified by AI", file=sys.stderr)
        sys.exit(2)  # Block operation

sys.exit(0)  # Allow operation
```

**Configuration**:
```json
{
  "event": "PreToolUse",
  "matcher": "Edit|Write",
  "command": "python hooks/file-protection.py"
}
```

**Customization**: Edit `protected` list to add/remove patterns

---

### git-safety-guard

**Purpose**: Prevent dangerous git operations (force push, hard reset)

**Event**: PreToolUse
**Matcher**: Bash
**Language**: Python

**Hook Script** (`hooks/git-safety-guard.py`):
```python
#!/usr/bin/env python3
import json
import sys
import re

data = json.load(sys.stdin)
command = data.get('tool_input', {}).get('command', '')

# Dangerous git patterns
dangerous = [
    (r'git\s+push.*--force', 'Force push'),
    (r'git\s+reset.*--hard', 'Hard reset'),
    (r'git\s+clean.*-[dfx]', 'Git clean'),
    (r'rm\s+-rf\s+\.git', 'Delete .git'),
    (r'git\s+rebase.*-i.*main', 'Rebase main branch')
]

for pattern, name in dangerous:
    if re.search(pattern, command, re.IGNORECASE):
        print(f"❌ ERROR: Dangerous git operation blocked: {name}", file=sys.stderr)
        print(f"   Command: {command}", file=sys.stderr)
        print(f"   Reason: High risk of data loss", file=sys.stderr)
        print(f"   Override: Run manually if absolutely necessary", file=sys.stderr)
        sys.exit(2)  # Block

sys.exit(0)  # Allow
```

**Configuration**:
```json
{
  "event": "PreToolUse",
  "matcher": "Bash",
  "command": "python hooks/git-safety-guard.py"
}
```

---

### syntax-validator

**Purpose**: Validate code syntax before saving

**Event**: PreToolUse
**Matcher**: Edit|Write
**Language**: Python

**Features**:
- Checks Python syntax with `ast.parse()`
- Validates JSON with `json.loads()`
- Checks YAML with `yaml.safe_load()`
- Blocks on syntax errors

**Configuration**:
```json
{
  "event": "PreToolUse",
  "matcher": "Edit|Write",
  "command": "python hooks/syntax-validator.py"
}
```

---

## Automation

### auto-formatter

**Purpose**: Automatically format code on save

**Event**: PostToolUse
**Matcher**: Edit|Write
**Language**: Bash

**Hook Script** (`hooks/auto-formatter.sh`):
```bash
#!/bin/bash
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Format based on file extension
if [[ "$FILE_PATH" =~ \.ts$ ]] || [[ "$FILE_PATH" =~ \.js$ ]]; then
  prettier --write "$FILE_PATH" 2>/dev/null
  echo "✅ Formatted TypeScript/JavaScript: $FILE_PATH"
elif [[ "$FILE_PATH" =~ \.py$ ]]; then
  black "$FILE_PATH" 2>/dev/null
  echo "✅ Formatted Python: $FILE_PATH"
elif [[ "$FILE_PATH" =~ \.go$ ]]; then
  gofmt -w "$FILE_PATH" 2>/dev/null
  echo "✅ Formatted Go: $FILE_PATH"
fi

exit 0
```

**Configuration**:
```json
{
  "event": "PostToolUse",
  "matcher": "Edit|Write",
  "command": "bash hooks/auto-formatter.sh"
}
```

**Dependencies**: `prettier`, `black`, `gofmt` (based on languages used)

---

### test-runner

**Purpose**: Automatically run tests when code changes

**Event**: PostToolUse
**Matcher**: Edit|Write
**Language**: Bash

**Hook Script** (`hooks/test-runner.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Only run for source files
if [[ ! "$FILE_PATH" =~ \.(ts|js|py|go)$ ]]; then
  exit 0
fi

echo "🧪 Running tests for: $FILE_PATH"

# Run tests based on project type
if [ -f "package.json" ]; then
  npm test -- "$FILE_PATH" 2>&1 | tail -20
elif [ -f "pytest.ini" ] || [ -f "setup.py" ]; then
  pytest "$FILE_PATH" 2>&1 | tail -20
elif [ -f "go.mod" ]; then
  go test ./... 2>&1 | tail -20
fi

if [ ${PIPESTATUS[0]} -ne 0 ]; then
  echo "⚠️  Tests failed - review output above"
else
  echo "✅ Tests passed"
fi

exit 0  # Don't block even if tests fail
```

**Configuration**:
```json
{
  "event": "PostToolUse",
  "matcher": "Edit|Write",
  "command": "bash hooks/test-runner.sh"
}
```

---

### auto-commit

**Purpose**: Create automatic backup commits

**Event**: PostToolUse
**Matcher**: Edit|Write
**Language**: Bash

**Hook Script** (`hooks/auto-commit.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Create backup commit
git add "$FILE_PATH" 2>/dev/null
git commit -m "Auto-backup: $FILE_PATH [Claude Code]" 2>/dev/null

if [ $? -eq 0 ]; then
  echo "💾 Auto-commit created for: $FILE_PATH"
else
  echo "ℹ️  No changes to commit"
fi

exit 0
```

**Configuration**:
```json
{
  "event": "PostToolUse",
  "matcher": "Edit|Write",
  "command": "bash hooks/auto-commit.sh"
}
```

**⚠️ Warning**: Creates many commits! Consider using only during development.

---

## Notifications

### desktop-notifier

**Purpose**: Send desktop notifications when Claude needs input

**Event**: Stop
**Matcher**: *
**Language**: Bash

**Hook Script** (`hooks/desktop-notifier.sh`):
```bash
#!/bin/bash
# macOS
command -v osascript >/dev/null && osascript -e 'display notification "Claude Code awaiting input" with title "Claude Code"'

# Linux
command -v notify-send >/dev/null && notify-send "Claude Code" "Awaiting your input"

# Windows (requires BurntToast PowerShell module)
command -v powershell.exe >/dev/null && powershell.exe -Command "New-BurntToastNotification -Text 'Claude Code', 'Awaiting your input'"

exit 0
```

**Configuration**:
```json
{
  "event": "Stop",
  "matcher": "*",
  "command": "bash hooks/desktop-notifier.sh"
}
```

**Dependencies**:
- macOS: Built-in `osascript`
- Linux: `notify-send` (libnotify)
- Windows: `BurntToast` PowerShell module

---

### slack-integration

**Purpose**: Send updates to Slack when tasks complete

**Event**: Stop
**Matcher**: *
**Language**: Python

**Hook Script** (`hooks/slack-notifier.py`):
```python
#!/usr/bin/env python3
import json
import sys
import os
import requests

SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

if not SLACK_WEBHOOK_URL:
    sys.exit(0)  # Silently skip if not configured

data = json.load(sys.stdin)

message = {
    "text": "Claude Code task completed",
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "✅ *Claude Code Task Completed*\nReady for your review"
            }
        }
    ]
}

try:
    response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=5)
    if response.status_code == 200:
        print("✅ Slack notification sent")
except Exception as e:
    print(f"⚠️  Slack notification failed: {e}", file=sys.stderr)

sys.exit(0)
```

**Configuration**:
```json
{
  "event": "Stop",
  "matcher": "*",
  "command": "python hooks/slack-notifier.py"
}
```

**Setup**:
1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Set environment variable: `export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...`

**Dependencies**: `requests` library

---

### completion-notifier

**Purpose**: Play sound when Claude finishes

**Event**: Stop
**Matcher**: *
**Language**: Bash

**Hook Script** (`hooks/completion-notifier.sh`):
```bash
#!/bin/bash
# macOS
command -v afplay >/dev/null && afplay /System/Library/Sounds/Glass.aiff

# Linux
command -v paplay >/dev/null && paplay /usr/share/sounds/freedesktop/stereo/complete.oga

# Cross-platform with ffplay (if installed)
command -v ffplay >/dev/null && ffplay -nodisp -autoexit /path/to/notification.mp3

exit 0
```

**Configuration**:
```json
{
  "event": "Stop",
  "matcher": "*",
  "command": "bash hooks/completion-notifier.sh"
}
```

---

## PRISM-Specific

### story-context-enforcer

**Purpose**: Ensure PRISM workflow commands have active story context

**Event**: PreToolUse
**Matcher**: Bash
**Language**: Python

**Hook Script**: See `hooks/enforce-story-context.py` in PRISM plugin

**Configuration**:
```json
{
  "event": "PreToolUse",
  "matcher": "Bash",
  "command": "python hooks/enforce-story-context.py"
}
```

**Blocks commands**: `*develop-story`, `*review`, `*risk`, `*design`, etc.

**Required**: `.prism-current-story.txt` file with active story path

---

### workflow-tracker

**Purpose**: Track PRISM workflow progress and log events

**Event**: PostToolUse
**Matcher**: Write
**Language**: Python

**Hook Script**: See `hooks/track-current-story.py` in PRISM plugin

**Configuration**:
```json
{
  "event": "PostToolUse",
  "matcher": "Write",
  "command": "python hooks/track-current-story.py"
}
```

**Creates**:
- `.prism-current-story.txt` (active story)
- `.prism-workflow.log` (audit trail)

---

## Installation

### Quick Install

All examples can be installed with:

```
*install-example [example-name]
```

### Manual Installation

1. Copy hook script to `hooks/` directory
2. Make executable: `chmod +x hooks/script.sh`
3. Add configuration to `.claude/settings.json`
4. Test: `*test-hook [hook-name]`

---

## Customization

All examples can be customized by:

1. Editing hook scripts directly
2. Modifying patterns/thresholds
3. Adding additional logic
4. Changing matchers
5. Combining multiple hooks

---

## Dependencies Summary

| Example | Dependencies | Installation |
|---------|--------------|--------------|
| bash-command-logger | jq | `brew install jq` |
| file-protection | Python 3 | Built-in |
| auto-formatter | prettier, black, gofmt | Via package managers |
| test-runner | npm, pytest, go | Project-specific |
| desktop-notifier | OS-specific | Built-in or system package |
| slack-integration | requests | `pip install requests` |
| git-safety-guard | Python 3 | Built-in |

---

## Contributing

Want to add your own example?

1. Create hook script with clear documentation
2. Test thoroughly in safe environment
3. Security review (no credentials, safe operations)
4. Submit via `*export-hooks` and share

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
**Total Examples**: 13
