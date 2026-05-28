---
name: creating-hooks
description: Use this skill when creating event-driven automation in Claude Code, such as validation, context injection, or auto-linting. It provides comprehensive guidance on hook events, configuration, and usage.
---

# Creating Hooks for Claude Code

Build event-driven automation for Claude Code using hooks—scripts that execute at specific workflow points.

## Quick Reference of Hook Events

| Hook Event            | When It Fires                     | Uses Matcher | Common Use Cases                          |
|-----------------------|-----------------------------------|--------------|-------------------------------------------|
| `PreToolUse`         | Before tool executes              | Yes          | Validation, auto-approval, input modification |
| `PostToolUse`        | After tool succeeds               | Yes          | Auto-formatting, linting, logging         |
| `PostToolUseFailure` | After tool fails                  | Yes          | Error handling, fallback logic             |
| `PermissionRequest`   | User shown permission dialog      | Yes          | Auto-allow/deny, policy enforcement       |
| `Notification`       | Claude sends notification         | Yes          | Custom alerts, logging                     |
| `UserPromptSubmit`   | User submits prompt               | No           | Prompt validation, context injection       |
| `SessionStart`       | Session begins/resumes            | Yes          | Context loading, environment setup        |
| `SessionEnd`         | Session ends                      | Yes          | Cleanup, logging                          |

## Hook Configuration Locations

Hooks are configured in settings files (in order of precedence):

| Location                             | Scope               | Committed |
|--------------------------------------|---------------------|-----------|
| `~/.claude/settings.json`            | User (all projects) | No        |
| `.claude/settings.json`              | Project             | Yes       |
| `.claude/settings.local.json`        | Local project       | No        |

## Basic Hook Structure

To create a hook, use the following JSON structure:

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Matcher Syntax

| Pattern | Matches                | Example                |
|---------|-----------------------|------------------------|
| `*`     | All tools             | `*`                    |
| `Bash`  | Bash tool only        | `Bash`                 |
| `Write` | Write tools           | `Write|Edit`          |
| `Read.*`| Read and any Read variants | `Read.*`          |

## Example Hook Configuration

Here’s an example of a hook that logs a message after a tool successfully executes:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'File written!'"
          }
        ]
      }
    ]
  }
}
```

## Key Considerations

- **Exit Codes**: Understand how exit codes affect hook behavior. For example, an exit code of `0` indicates success, while `2` can block execution in `PreToolUse`.
- **Testing**: Always test hooks in a safe environment to ensure they behave as expected before deploying them in production.

Use this skill to effectively create and manage hooks in Claude Code, enhancing your automation and validation processes.