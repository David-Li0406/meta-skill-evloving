---
name: managing-permissions
description: Use this skill when configuring Claude Code permissions in settings.json to control tool access, protect sensitive files, and implement security best practices.
---

# Managing Permissions

Configure Claude Code permissions to control tool access and protect sensitive files.

## Overview

Permissions are configured in `settings.json` using three groups: **allow**, **ask**, and **deny**.

**Rule precedence**: Deny > Ask > Allow

**Configuration hierarchy** (highest to lowest):

1. Managed settings (enterprise policies)
2. Command-line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User global settings (`~/.claude/settings.json`)

## Permission Groups

### Allow

Grants explicit permission for tool use without confirmation.

**When to use:** Safe, routine operations that don't risk data loss or security exposure.

**Examples:** Reading source code, running tests, read-only git commands.

### Ask

Prompts for user confirmation before allowing tool use.

**When to use:** Operations requiring review, such as publishing changes or modifying dependencies.

**Examples:** Git push/commit, package installation, editing critical config files.

### Deny

Explicitly blocks tool use. Takes precedence over allow and ask rules.

**⚠️ Important:** Deny rules are workflow controls, NOT security mechanisms. They have significant limitations (tool-specific, easily bypassed, prefix-only matching for Bash).

**When to use:**

- Resource management (blocking node_modules, build artifacts to save tokens)
- Workflow guardrails (preventing accidental git push to main)
- Focus management (avoiding deprecated/legacy code)

## Basic Syntax

All permission rules follow this format:

```
ToolName(pattern)
```

**Available Tools:** Bash, Read, Edit, Write, Glob, Grep, WebFetch, WebSearch, NotebookEdit, Task, Skill, SlashCommand, TodoWrite, AskUserQuestion, BashOutput, KillShell, ExitPlanMode

**Pattern types:**

- **Bash**: Prefix matching - `Bash(git status)` matches "git status", "git status file.txt"
- **File tools**: Glob matching - `Read(src/**)` matches all files in src/ recursively

## Configuration Workflow

When setting up permissions:

1. **For security: Use hooks** - Protect secrets with PreToolUse hooks (deny rules aren't sufficient for security)
2. **Add deny rules** - Block large files (node_modules, build artifacts) to save tokens, prevent workflow mistakes
3. **Add allow rules** - Enable routine safe operations
4. **Add ask rules** - Require confirmation for important operations
5. **Test configuration** - Verify typical workflows work correctly
6. **Iterate** - Add rules as needed based on actual usage

## Sample Configuration

```json
{
  "permissions": {
    "deny": [
      "Read(node_modules/**)",
      "Read(build/**)",
      "Bash(git push origin main:*)"
    ],
    "allow": [
      "Bash(git status)",
      "Read(src/**)",
      "Read(tests/**)"
    ],
    "ask": [
      "Bash(git push:*)"
    ]
  }
}
```

## Security Essentials

### Principle of Least Privilege

Start restrictive, add permissions as needed to ensure security and compliance.

## Reference Files

Concise guides with practical examples:

- **allow-permissions.md** - What to allow (non-destructive, reversible operations), practical examples, key principles
- **ask-permissions.md** - What to ask for (external changes, dependencies, critical configs), avoiding permission fatigue
- **deny-permissions.md** - Key limitations (tool-specific), proper use cases (resource management, workflow guardrails), why hooks are needed for security
- **official-reference.md** - Complete technical reference, glob syntax, known limitations