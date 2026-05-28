---
name: managing-claude-code-permissions
description: Use this skill when configuring Claude Code permissions in settings.json to ensure security and compliance while managing tool access and file permissions.
---

# Managing Claude Code Permissions

Configure Claude Code permissions to control tool access and protect sensitive files effectively.

## Overview

Permissions are configured in `settings.json` using three groups: **allow**, **ask**, and **deny**. The rule precedence is as follows:

1. **Deny** - Explicitly blocks tool use (highest priority).
2. **Ask** - Requires user confirmation before allowing tool use.
3. **Allow** - Grants explicit permission for tool use without confirmation.

### Configuration Hierarchy

Permissions are evaluated in this order (highest to lowest):

1. Managed settings (enterprise policies)
2. Command-line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User global settings (`~/.claude/settings.json`)

## Permission Groups

### Allow

Grants explicit permission for tool use without confirmation.

**When to use:** Safe, routine operations that don't risk data loss or security exposure.

**Examples:**
- Reading source code
- Running tests
- Read-only git commands

### Ask

Prompts for user confirmation before allowing tool use.

**When to use:** Operations requiring review, such as publishing changes or modifying dependencies.

**Examples:**
- Git push/commit
- Package installation
- Editing critical config files

### Deny

Explicitly blocks tool use. Takes precedence over allow and ask rules.

**⚠️ Important:** Deny rules are workflow controls, NOT security mechanisms. They have significant limitations (tool-specific, easily bypassed, prefix-only matching for Bash).

**When to use:**
- Resource management (blocking node_modules, build artifacts to save tokens)
- Workflow guardrails (preventing accidental git push to main)
- Focus management (avoiding deprecated/legacy code)

## Common Permission Patterns

### Basic Configuration Example

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Read"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "defaultMode": "default"
}
```

### Git Operations Example

```json
{
  "permissions": {
    "allow": [
      "Bash(git status)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(git commit:*)"
    ]
  }
}
```

### Package Managers Example

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npm test:*)",
      "Bash(bun *)",
      "Bash(yarn *)"
    ]
  }
}
```