# allowed-tools

Restricts which tools Claude can use without permission prompts when skill is active.

## How It Works

- **Allowlist model**: Only listed tools skip permission
- **Empty/omitted**: Standard permission model applies
- **Scope limitation**: Permissions apply globally, not just during skill execution

## Syntax

```yaml
# Comma-separated
allowed-tools: Read, Grep, Glob

# YAML list
allowed-tools:
  - Read
  - Grep
  - Bash(python:*)

# MCP tools
allowed-tools:
  - mcp__linear__create_issue
  - mcp__github__*
```

## Examples

**Read-only exploration skill:**

```yaml
---
name: code-explorer
description: Explores codebase structure and patterns
allowed-tools:
  - Read
  - Grep
  - Glob
---
```

**Build automation skill:**

```yaml
---
name: build-runner
description: Runs build and test commands
allowed-tools:
  - Bash(npm:*)
  - Bash(yarn:*)
  - Bash(make:*)
  - Read
---
```

## Links

- Docs: https://code.claude.com/docs/en/skills.md
- Issues:
  - [#14956](https://github.com/anthropics/claude-code/issues/14956) - allowed-tools doesn't grant Bash permission
  - [#15006](https://github.com/anthropics/claude-code/issues/15006) - Request for skill-specific auto-approval
  - [#11088](https://github.com/anthropics/claude-code/issues/11088) - Fine-grained permissions request
