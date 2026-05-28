---
name: creating-claude-hooks
description: Use this skill when creating or publishing Claude Code hooks, covering executable format, event types, JSON I/O, exit codes, security requirements, and PRPM package structure.
---

# Creating Claude Code Hooks

Use this skill when creating, improving, or publishing Claude Code hooks. It provides essential guidance on hook format, event handling, I/O conventions, and package structure.

## When to Use This Skill

Activate this skill when:
- A user asks to create a new Claude Code hook.
- A user wants to publish a hook as a PRPM package.
- A user needs to understand hook format or events.
- A user is troubleshooting hook execution.
- A user asks about the differences between hooks, skills, and commands.

## Quick Reference

### Hook File Format

| Aspect | Requirement |
|--------|-------------|
| **Location** | `.claude/hooks/<event-name>` |
| **Format** | Executable file (shell, TypeScript, Python, etc.) |
| **Permissions** | Must be executable (`chmod +x`) |
| **Shebang** | Required (`#!/bin/bash` or `#!/usr/bin/env node`) |
| **Input** | JSON via stdin |
| **Output** | Text via stdout (shown to user) |
| **Exit Codes** | `0` = success, `2` = block, other = error |

### Available Events

| Event | When It Fires | Common Use Cases |
|-------|---------------|------------------|
| `session-start` | New session begins | Environment setup, logging, checks |
| `user-prompt-submit` | Before user input processes | Validation, enhancement, filtering |
| `tool-call` | Before tool execution | Permission checks, logging, modification |
| `assistant-response` | After assistant responds | Formatting, logging, cleanup |

## Hook Format Requirements

### File Location

**Project hooks:**
```
.claude/hooks/session-start
.claude/hooks/user-prompt-submit
```

**User-global hooks:**
```
~/.claude/hooks/session-start
~/.claude/hooks/tool-call
```

### Executable Requirements

Every hook MUST:

1. **Have a shebang line:**
```bash
#!/bin/bash
# or
#!/usr/bin/env node
# or
#!/usr/bin/env python3
```

2. **Be executable:**
```bash
chmod +x .claude/hooks/session-start
```

3. **Handle JSON input from stdin:**
```bash
#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.input.file_path // empty')
```

4. **Exit with appropriate code:**
```bash
exit 0  # Success
exit 2  # Block operation
exit 1  # Error (logs but continues)
```

## Input/Output Format

### JSON Input Structure

Hooks receive JSON via stdin with event-specific data.