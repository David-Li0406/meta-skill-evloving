---
name: yaml-frontmatter-reference
description: Use this skill when creating or validating YAML frontmatter for Claude Code skills, agents, or commands.
---

# YAML Frontmatter Reference for Claude Code

This document provides a complete reference for the YAML frontmatter properties used in Claude Code for skills, agents (subagents), and commands.

## Skills (SKILL.md)

```yaml
---
name: skill-name                    # Required: identifier (lowercase-with-hyphens)
description: Use when...            # Required: when to use (third person)
allowed-tools: Read, Grep, Glob     # Optional: allowed tools (comma-separated)
model: inherit                      # Optional: inherit / specific model name
version: "1.0.0"                    # Optional: for versioning
disable-model-invocation: false     # Optional: true to prevent automatic invocation
mode: false                         # Optional: true to display Mode Commands section
---
```

| Property | Required | Values |
|----------|----------|--------|
| `name` | Yes | lowercase-with-hyphens |
| `description` | Yes | "Use when..." format recommended |
| `allowed-tools` | No | Read, Grep, Glob, Bash, Write, Edit, Task... |
| `model` | No | `inherit` / specific model name |
| `version` | No | Semantic version |
| `disable-model-invocation` | No | `true` / `false` |
| `mode` | No | `true` / `false` |

## Agents (Subagents)

```yaml
---
name: agent-name                    # Required: identifier
description: |                      # Required: description (multi-line recommended)
  Use when reviewing code...
  <example>
  user: "レビューして"
  assistant: "agent-nameで確認します"
  </example>
tools: Read, Grep, Glob, Bash       # Optional: allowed tools (inherits by default)
model: sonnet                       # Optional: sonnet/opus/haiku/inherit
color: blue                         # Optional: visual identifier color
permissionMode: default             # Optional: permission mode
skills: skill1, skill2              # Optional: skills to auto-load
---
```

| Property | Required | Values |
|----------|----------|--------|
| `name` | Yes | identifier |
| `description` | Yes | description (multi-line with examples recommended) |
| `tools` | No | comma-separated (inherits all tools by default) |
| `model` | No | `sonnet` / `opus` / `haiku` / `inherit` |
| `color` | No | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan` |
| `skills` | No | comma-separated skill names |

## Commands (Slash Commands)

```yaml
---
description: Command description    # Recommended: necessary for SlashCommand tool
argument-hint: [arg1] [arg2]        # Optional: argument hints
allowed-tools: Bash(git:*), Read    # Optional: allowed tools
model: claude-3-5-haiku-20241022    # Optional: specific model name
disable-model-invocation: true      # Optional: prevent SlashCommand tool invocation
---
```

| Property | Required | Values |
|----------|----------|--------|
| `description` | Recommended | description text |
| `argument-hint` | No | `[message]`, `[file] [options]`, etc. |
| `allowed-tools` | No | tool restrictions (wildcards allowed) |
| `model` | No | specific model name |
| `disable-model-invocation` | No | `true` / `false` |

### Validation Checklist

#### Skills
- [ ] Opening `---` present
- [ ] `name` is lowercase-with-hyphens
- [ ] `description` includes usage context
- [ ] `allowed-tools` is comma-separated
- [ ] Closing `---` present
- [ ] No YAML syntax errors

#### Agents
- [ ] Opening `---` present
- [ ] `name` is valid
- [ ] `description` includes examples
- [ ] `tools` is comma-separated
- [ ] Closing `---` present
- [ ] No YAML syntax errors

#### Commands
- [ ] Opening `---` present
- [ ] `description` explains command purpose
- [ ] `allowed-tools` is valid
- [ ] Closing `---` present
- [ ] No YAML syntax errors

## Common Errors

### Invalid YAML Syntax
```yaml
# WRONG - missing colon
name agent-name

# CORRECT
name: agent-name
```

### Incorrect Tool Format
```yaml
# WRONG - no spaces after commas
tools: TodoWrite,Read,Write

# CORRECT
tools: TodoWrite, Read, Write
```

### Missing Examples
```yaml
# WRONG - too generic
description: Use this agent for development tasks.

# CORRECT
description: |
  Use this agent when implementing TypeScript features. Examples:
  (1) "Create a user service" - implements service with full CRUD
  (2) "Add validation" - adds Zod schemas to endpoints
  (3) "Fix type errors" - resolves TypeScript compilation issues
```

## Sources

- [Subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [Agent Skills - Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Slash Commands - Claude Code Docs](https://code.claude.com/docs/en/slash-commands)
- [GitHub Issue #8501 - Frontmatter documentation](https://github.com/anthropics/claude-code/issues/8501)
- [Claude Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)