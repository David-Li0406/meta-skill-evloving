---
name: claude-hook-creation
description: Use this skill when creating or modifying hooks for Claude Code in settings.json, particularly for automating tool execution workflows.
---

# Creating and Configuring Claude Code Hooks

This skill allows you to create and configure hooks in `.claude/settings.json` for various events in Claude Code.

## Hook Structure

Define hooks in the following JSON format:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/my-hook.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Hook Events

| Event | When | Common Use |
|-------|------|------------|
| `PreToolUse` | Before tool runs | Validate, block |
| `PostToolUse` | After tool succeeds | Format, lint |
| `UserPromptSubmit` | User sends prompt | Add context |
| `SessionStart` | Session begins | Load context |
| `Stop` | Agent finishes | Cleanup |

## Matcher Syntax

**Matchers match TOOL NAMES only, not file paths.**

```json
// ✅ CORRECT - tool name regex
"matcher": "Write|Edit"

// ❌ WRONG - glob patterns don't work
"matcher": "Edit(**/*.md)"
"matcher": "Write(docs/*.ts)"
```

## Handling Absolute Paths

Tools pass **absolute paths** in `tool_input.file_path`. Your script must handle this:

```bash
# Strip project dir to get relative path
rel_path="${file_path#$CLAUDE_PROJECT_DIR/}"

# Now match against relative path
if [[ "$rel_path" =~ ^docs/.*\.md$ ]]; then
  # ...
fi
```

## Hook Input (stdin JSON)

The input to your hook script will be in the following format:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/dir",
  "hook_event_name": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/absolute/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

## Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| 0 | Success | Continue, stdout shown in transcript (Ctrl-R) |
| 2 | Block | Stop tool, stderr shown to Claude |
| Other | Error | Continue, stderr shown to user |

## Script Template

Here’s a basic template for your hook script:

```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# Convert absolute to relative
rel_path="${file_path#$CLAUDE_PROJECT_DIR/}"

# Filter by extension/path
if [[ -z "$rel_path" || ! "$rel_path" =~ \.(ts|tsx|md)$ ]]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"
# Your logic here

exit 0
```

## Notes

- **Changes require restart** — Hook edits don't take effect until CC restarts.
- **Parallel execution** — Multiple matching hooks run in parallel.
- **60s default timeout** — Override with `"timeout": <seconds>`.
- **Debug mode** — `claude --debug` shows hook execution details.

Use this skill when you need to create or modify hooks for Claude Code, especially when automating workflows or validating hook configurations.