# Hook Script Examples

Complete examples from Claude cookbooks demonstrating hook script implementation patterns.

## Example 1: Pre-Write Safety Hook (Bash)

**Purpose**: Warn before overwriting protected files

**Source**: Claude Skills Cookbook

**Hook Configuration**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/pre-write.sh"
          }
        ]
      }
    ]
  }
}
```

**Script** (`.claude/hooks/pre-write.sh`):
```bash
#!/bin/bash
# PreToolUse Hook - Write Safety Check
# Prevents accidental overwrites of key files

set -e

# Read JSON input from stdin
INPUT=$(cat)

# Parse tool_name and file_path from JSON
# Using basic string manipulation (jq is better if available)
TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)

# Only run for Write tool
if [[ "$TOOL_NAME" != "Write" ]]; then
  exit 0
fi

# Protected files - should never be overwritten without explicit user request
PROTECTED_FILES=(
  ".env"
  "requirements.txt"
  "package.json"
)

# Check if writing to protected file
for protected in "${PROTECTED_FILES[@]}"; do
  if [[ "$FILE_PATH" == *"$protected"* ]]; then
    # Print warning to stderr (visible to user)
    echo "⚠️ WARNING: Attempting to write to protected file: $FILE_PATH" >&2
    echo "This file should rarely be modified. Proceeding with caution..." >&2
    # Allow but warn - don't block (exit 0, not exit 2)
  fi
done

# Warn if writing to notebooks/ without .ipynb extension
if [[ "$FILE_PATH" == *"notebooks/"* ]] && [[ "$FILE_PATH" != *".ipynb" ]]; then
  echo "⚠️ Writing non-notebook file to notebooks/ directory: $FILE_PATH" >&2
fi

# Warn if writing to sample_data/
if [[ "$FILE_PATH" == *"sample_data/"* ]]; then
  echo "ℹ️ Modifying sample data: $FILE_PATH" >&2
fi

# Always allow operation (exit 0)
exit 0
```

**Make Executable**:
```bash
chmod +x .claude/hooks/pre-write.sh
```

**Key Patterns**:
- Read from stdin with `cat`
- Parse JSON with grep/cut (or use jq)
- Check conditions with array iteration
- Output warnings to stderr
- Exit 0 to allow operation
- Use `set -e` for error handling

## Example 2: Pre-Bash Safety Hook (Bash)

**Purpose**: Prevent dangerous commands and provide helpful reminders

**Source**: Claude Skills Cookbook

**Script** (`.claude/hooks/pre-bash.sh`):
```bash
#!/bin/bash
# PreToolUse Hook - Bash Safety Check
# Prevents dangerous commands and provides helpful reminders

set -e

# Read input
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
COMMAND=$(echo "$INPUT" | grep -o '"command":"[^"]*"' | sed 's/"command":"//;s/"$//')

# Only run for Bash tool
if [[ "$TOOL_NAME" != "Bash" ]]; then
  exit 0
fi

# Check for potentially dangerous commands
if [[ "$COMMAND" == *"rm -rf"* ]]; then
  echo "⚠️ WARNING: Attempting to delete directory recursively!" >&2
  echo "Command: $COMMAND" >&2
  echo "Please verify this is intentional." >&2
  # Could use exit 2 to block, but we'll warn only
fi

# Warn about pip install without using requirements.txt
if [[ "$COMMAND" == *"pip install"* ]] && [[ "$COMMAND" != *"requirements.txt"* ]]; then
  echo "ℹ️ Installing package directly. Consider updating requirements.txt" >&2
fi

# Remind about kernel restart after SDK reinstall
if [[ "$COMMAND" == *"pip install"* ]] && [[ "$COMMAND" == *"anthropic"* ]]; then
  echo "ℹ️ Remember: Restart Jupyter kernel after SDK installation!" >&2
fi

# Warn if trying to start jupyter/servers
if [[ "$COMMAND" == *"jupyter notebook"* ]] || [[ "$COMMAND" == *"jupyter lab"* ]]; then
  echo "ℹ️ Starting Jupyter. Make sure to select the venv kernel in notebooks." >&2
fi

exit 0
```

**Key Patterns**:
- Pattern matching with `[[ "$VAR" == *"pattern"* ]]`
- Multiple condition checks
- Context-aware reminders
- Non-blocking warnings

## Example 3: Post-Tool Audit Logger (Python)

**Purpose**: Track all file writes and edits for compliance

**Source**: Chief of Staff Agent Cookbook

**Hook Configuration**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/report-tracker.py"
          }
        ]
      }
    ]
  }
}
```

**Script** (`.claude/hooks/report-tracker.py`):
```python
#!/usr/bin/env python3
"""
PostToolUse hook: Tracks ALL file writes and edits
Maintains history of all document changes for compliance
"""

import json
import os
import sys
from datetime import datetime


def track_report(tool_name, tool_input, tool_response):
    """Log ALL file creation/modification for audit trail"""

    # Debug: Log that hook was called
    print(f"🔍 Hook called for tool: {tool_name}", file=sys.stderr)

    # Get file path from tool input
    file_path = tool_input.get("file_path", "")

    if not file_path:
        print("⚠️ No file_path in tool_input", file=sys.stderr)
        return

    print(f"📝 Tracking file: {file_path}", file=sys.stderr)

    # Prepare history file path
    history_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../audit/report_history.json"
    )

    try:
        # Load existing history or create new
        if os.path.exists(history_file):
            with open(history_file) as f:
                history = json.load(f)
        else:
            history = {"reports": []}

        # Determine action type
        action = "created" if tool_name == "Write" else "modified"

        # Calculate word count if content available
        content = tool_input.get("content", "") or tool_input.get("new_string", "")
        word_count = len(content.split()) if content else 0

        # Create history entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "file": os.path.basename(file_path),
            "path": file_path,
            "action": action,
            "word_count": word_count,
            "tool": tool_name,
        }

        # Add to history
        history["reports"].append(entry)

        # Keep only last 50 entries
        history["reports"] = history["reports"][-50:]

        # Save updated history
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        with open(history_file, "w") as f:
            json.dump(history, f, indent=2)

        print(f"📊 File tracked: {os.path.basename(file_path)} ({action})")

    except Exception as e:
        print(f"Report tracking error: {e}", file=sys.stderr)


# Main execution
if __name__ == "__main__":
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        tool_response = input_data.get("tool_response", {})

        # Track the report
        track_report(tool_name, tool_input, tool_response)

        # Always exit successfully
        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on errors
```

**Make Executable**:
```bash
chmod +x .claude/hooks/report-tracker.py
```

**Key Patterns**:
- Use `json.load(sys.stdin)` for input parsing
- Graceful error handling with try/except
- Create directories with `os.makedirs(..., exist_ok=True)`
- Maintain rolling history (last N entries)
- Always exit 0 in PostToolUse (can't block completed operations)
- Use stderr for status messages

## Example 4: Script Usage Logger (Python)

**Purpose**: Log when Python scripts are executed via Bash tool

**Source**: Chief of Staff Agent Cookbook

**Script** (`.claude/hooks/script-usage-logger.py`):
```python
#!/usr/bin/env python3
"""
PostToolUse hook: Logs execution of Python scripts through Bash tool
Distinguishes between Claude SDK tools and actual script executions
"""

import json
import os
import re
import sys
from datetime import datetime


def log_script_usage(tool_name, tool_input, tool_response):
    """Log script executions (not SDK tool calls)"""

    # Only process Bash tool calls
    if tool_name != "Bash":
        return

    # Get the command that was executed
    command = tool_input.get("command", "")
    description = tool_input.get("description", "")

    # Check if command executes a Python script
    # Pattern: python scripts/something.py or ./scripts/something.py
    script_pattern = r"(?:python\s+)?(?:\./)?scripts/(\w+\.py)"
    match = re.search(script_pattern, command)

    if not match:
        return  # Not a script execution

    script_name = match.group(1)

    # Check if execution was successful
    success = tool_response.get("success", False)

    # Prepare log file
    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../audit/script_usage_log.json"
    )

    try:
        # Load existing log
        if os.path.exists(log_file):
            with open(log_file) as f:
                log_data = json.load(f)
        else:
            log_data = {"executions": []}

        # Create log entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "script": script_name,
            "command": command,
            "description": description,
            "tool_used": tool_name,
            "success": success,
        }

        # Add to log
        log_data["executions"].append(entry)

        # Keep last 100 entries
        log_data["executions"] = log_data["executions"][-100:]

        # Save log
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=2)

        status = "✅" if success else "❌"
        print(f"{status} Script executed: {script_name}", file=sys.stderr)

    except Exception as e:
        print(f"Logging error: {e}", file=sys.stderr)


if __name__ == "__main__":
    try:
        # Read input
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        tool_response = input_data.get("tool_response", {})

        log_script_usage(tool_name, tool_input, tool_response)

        sys.exit(0)

    except Exception as e:
        print(f"Hook error: {e}", file=sys.stderr)
        sys.exit(0)
```

**Key Patterns**:
- Regex pattern matching for command analysis
- Filter by tool name before processing
- Check success status from tool_response
- Conditional execution based on command content

## Example 5: Session Start Environment Check (Bash)

**Purpose**: Verify environment setup at session start

**Source**: Claude Skills Cookbook

**Script** (`.claude/hooks/session-start.sh`):
```bash
#!/bin/bash
# SessionStart Hook - Environment Validation
# Verifies dependencies, API keys, and project setup

set -e

echo "🔍 Project Environment Check" >&2
echo "======================================" >&2

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️ WARNING: No virtual environment detected!" >&2
    echo "  Run: source venv/bin/activate" >&2
    echo "" >&2
fi

# Check if Anthropic SDK is installed and get version
if python -c "import anthropic" 2>/dev/null; then
    SDK_VERSION=$(python -c "import anthropic; print(anthropic.__version__)" 2>/dev/null || echo "unknown")
    echo "✅ Anthropic SDK: $SDK_VERSION" >&2

    # Check for minimum version
    if [[ "$SDK_VERSION" < "0.71.0" ]]; then
        echo "⚠️ SDK version $SDK_VERSION may be too old (minimum 0.71.0 recommended)" >&2
        echo "  Run: pip install anthropic>=0.71.0" >&2
        echo "" >&2
    fi
else
    echo "❌ Anthropic SDK not installed" >&2
    echo "  Run: pip install -r requirements.txt" >&2
    echo "" >&2
fi

# Check for API key
if [[ -f ".env" ]]; then
    if grep -q "^ANTHROPIC_API_KEY=sk-" .env 2>/dev/null; then
        echo "✅ API key configured in .env" >&2
    else
        echo "⚠️ .env exists but API key may not be set" >&2
        echo "  Check ANTHROPIC_API_KEY in .env" >&2
        echo "" >&2
    fi
else
    echo "⚠️ .env file not found" >&2
    echo "  Run: cp .env.example .env" >&2
    echo "  Then add your ANTHROPIC_API_KEY" >&2
    echo "" >&2
fi

# Check outputs directory
if [[ -d "outputs" ]]; then
    FILE_COUNT=$(find outputs -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "✅ outputs/ directory exists ($FILE_COUNT files)" >&2
else
    echo "ℹ️ Creating outputs/ directory..." >&2
    mkdir -p outputs
fi

echo "" >&2
echo "======================================" >&2
echo "Ready to work! 🚀" >&2
echo "" >&2

exit 0
```

**Key Patterns**:
- Environment variable checks
- Version validation with comparison
- Directory creation if missing
- File pattern checks with grep
- User-friendly output formatting

## Example 6: Blocking Pre-Write Hook (Bash)

**Purpose**: Block writes to specific files completely

**Script**:
```bash
#!/bin/bash
set -e

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)

if [[ "$TOOL_NAME" != "Write" ]]; then
  exit 0
fi

# Absolutely protected files
BLOCKED_FILES=(
  "production.env"
  ".env.production"
  "secrets.json"
)

for blocked in "${BLOCKED_FILES[@]}"; do
  if [[ "$FILE_PATH" == *"$blocked"* ]]; then
    echo "🚫 BLOCKED: Cannot write to $blocked" >&2
    echo "This file is protected and cannot be modified by Claude." >&2
    # Exit 2 to block the operation
    exit 2
  fi
done

exit 0
```

**Key Pattern**: Use `exit 2` to block PreToolUse operations

## Example 7: JSON Output for Modified Input (Python)

**Purpose**: Modify tool input before execution

**Script**:
```python
#!/usr/bin/env python3
import json
import sys

# Read input
input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name")
tool_input = input_data.get("tool_input", {})

if tool_name == "Write":
    file_path = tool_input.get("file_path", "")

    # Add automatic header to all Python files
    if file_path.endswith(".py"):
        content = tool_input.get("content", "")

        # Add header if not present
        if not content.startswith("#!/usr/bin/env python3"):
            header = "#!/usr/bin/env python3\n# Auto-generated by Claude Code\n\n"
            modified_content = header + content

            # Output JSON with modified input
            output = {
                "decision": "allow",
                "updatedInput": {
                    "file_path": file_path,
                    "content": modified_content
                },
                "additionalContext": f"Added standard header to {file_path}"
            }

            print(json.dumps(output))
            sys.exit(0)

# No modification needed
sys.exit(0)
```

**Key Pattern**: Output JSON to stdout to modify tool input

## Common Script Patterns

### Input Parsing (Bash)
```bash
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)
COMMAND=$(echo "$INPUT" | grep -o '"command":"[^"]*"' | sed 's/"command":"//;s/"$//')
```

### Input Parsing (Python)
```python
import json
import sys

input_data = json.load(sys.stdin)
tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
tool_response = input_data.get("tool_response", {})
```

### Error Handling (Python)
```python
try:
    # Hook logic here
    pass
except Exception as e:
    print(f"Hook error: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on errors
```

### File Operations (Python)
```python
# Ensure directory exists
os.makedirs(directory_path, exist_ok=True)

# Atomic file write
with open(file_path, "w") as f:
    json.dump(data, f, indent=2)

# Safe file read
if os.path.exists(file_path):
    with open(file_path) as f:
        data = json.load(f)
```

### Output Messages
```bash
# Bash: stderr for user-visible messages
echo "Message to user" >&2

# Python: stderr for user-visible messages
print("Message to user", file=sys.stderr)
```

## Testing Hook Scripts

**Test with sample input**:
```bash
# Create test input
echo '{"tool_name":"Write","tool_input":{"file_path":"/test/file.txt"}}' | python3 hook-script.py
```

**Test with jq for complex JSON**:
```bash
jq -n '{tool_name: "Write", tool_input: {file_path: "/test.txt", content: "test"}}' | ./hook-script.sh
```

**Check exit codes**:
```bash
./hook-script.sh < test-input.json
echo "Exit code: $?"
```
