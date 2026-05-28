---
name: managing-permissions
description: Use this skill when configuring Claude Code permissions in settings.json to control tool access, protect sensitive files, and implement security best practices.
---

# Managing Permissions

Configure Claude Code permissions to control tool access and protect sensitive files.

## Overview

Permissions are configured in `settings.json` using three groups: **allow**, **ask**, and **deny**. The rule precedence is Deny > Ask > Allow.

### Configuration Hierarchy

1. Managed settings (enterprise policies)
2. Command-line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User global settings (`~/.claude/settings.json`)

## Permission Groups

### Allow

Grants explicit permission for tool use without confirmation. Use for safe, routine operations that don't risk data loss or security exposure.

**Examples:** Reading source code, running tests, read-only git commands.

### Ask

Prompts for user confirmation before allowing tool use. Use for operations requiring review, such as publishing changes or modifying dependencies.

**Examples:** Git push/commit, package installation, editing critical config files.

### Deny

Explicitly blocks tool use and takes precedence over allow and ask rules. Use for resource management, workflow guardrails, and focus management.

**⚠️ Important:** Deny rules are workflow controls, not security mechanisms. For protecting secrets and credentials, use hooks instead.

## Basic Syntax

All permission rules follow this format:

```
ToolName(pattern)
```

**Available Tools:** Bash, Read, Edit, Write, Glob, Grep, WebFetch, etc.

**Pattern Types:**

- **Bash:** Prefix matching (e.g., `Bash(git status)`)
- **File tools:** Glob matching (e.g., `Read(src/**)`)

## Configuration Workflow

When setting up permissions:

1. **For security:** Use hooks to protect secrets.
2. **Add deny rules:** Block large files and prevent workflow mistakes.
3. **Add allow rules:** Enable routine safe operations.
4. **Add ask rules:** Require confirmation for important operations.
5. **Test configuration:** Verify typical workflows work correctly.
6. **Iterate:** Add rules as needed based on actual usage.

## Sample Workflow Configuration

```json
{
  "permissions": {
    "deny": [
      "Read(node_modules/**)",
      "Bash(git push origin main:*)"
    ],
    "allow": [
      "Bash(git status)",
      "Read(src/**)"
    ],
    "ask": [
      "Bash(git push:*)"
    ]
  }
}
```

## Reference Files

Concise guides with practical examples:

- **allow-permissions.md** - What to allow (non-destructive operations), practical examples.
- **ask-permissions.md** - What to ask for (external changes, critical configs).
- **deny-permissions.md** - Key limitations and proper use cases.
- **official-reference.md** - Complete technical reference, glob syntax, known limitations.

For comprehensive patterns and security guidance, see additional references as needed.