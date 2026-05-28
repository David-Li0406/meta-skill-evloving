---
name: claude-code-frontmatter
description: Use this skill when creating or validating YAML frontmatter for Claude Code agents, commands, or skills.
---

# Skill body

## YAML Frontmatter Reference

### Skills (SKILL.md)

```yaml
---
name: skill-name                    # Required: identifier (lowercase-with-hyphens)
description: Use when...            # Required: when to use (third person)
allowed-tools: Read, Grep, Glob     # Optional: allowed tools (comma-separated)
model: inherit                      # Optional: inherit / specific model name
version: "1.0.0"                    # Optional: for version management
disable-model-invocation: false     # Optional: true to prevent automatic invocation of Slash tool
mode: false                         # Optional: true to display Mode Commands section
---
```

| Property | Required | Values |
|----------|----------|--------|
| `name` | Yes | lowercase-with-hyphens |
| `description` | Yes | "Use when..." format recommended |
| `allowed-tools` | No | Read, Grep, Glob, Bash, Write, Edit, Task... |
| `model` | No | `inherit` / specific model name |
| `version` | No | semantic versioning |
| `disable-model-invocation` | No | `true` / `false` |
| `mode` | No | `true` / `false` |

### Agents (Subagents)

```yaml
---
name: agent-name                    # Required: identifier
description: |                      # Required: description (multi-line)
  Use when reviewing code...
  <example>
  user: "Please review"
  assistant: "I will check with agent-name"
  </example>
tools: Read, Grep, Glob, Bash       # Optional: allowed tools (inherits all by default)
model: sonnet                       # Optional: sonnet/opus/haiku/inherit
color: blue                         # Optional: visual identification color
permissionMode: default             # Optional: permission mode
skills: skill1, skill2              # Optional: skills to auto-load
---
```

| Property | Required | Values |
|----------|----------|--------|
| `name` | Yes | identifier |
| `description` | Yes | description (recommended with examples) |
| `tools` | No | comma-separated (inherits all by default) |
| `model` | No | `sonnet` / `opus` / `haiku` / `inherit` |
| `color` | No | `red` / `blue` / `green` / `yellow` / `purple` / `orange` / `pink` / `cyan` |
| `permissionMode` | No | `default` / `acceptEdits` / `bypassPermissions` / `plan` |
| `skills` | No | comma-separated skill names |

### Commands (Slash Commands)

```yaml
---
description: Command description    # Recommended: required for SlashCommand tool
argument-hint: [arg1] [arg2]        # Optional: hints for command arguments
allowed-tools: Task, Bash           # Required: comma-separated
skills: skill1, skill2              # Optional: referenced skills
---
```