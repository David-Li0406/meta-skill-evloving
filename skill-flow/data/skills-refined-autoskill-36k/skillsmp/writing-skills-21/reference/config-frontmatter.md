# Frontmatter Fields

The YAML block at the top of SKILL.md that configures skill behavior.

## How It Works

Claude Code parses frontmatter at startup. Only `name` and `description` load initially (~100 tokens). Full content loads on-demand when skill triggers.

## Schema

```yaml
---
name: string # Required. Max 64 chars, lowercase/numbers/hyphens
description: string # Required. Max 1024 chars, third person
allowed-tools: string[] # Optional. Tools Claude can use without permission
context: "fork" # Optional. Run in isolated subagent
agent: string # Optional. Agent type when context: fork
model: string # Optional. Override model for this skill
user-invocable: boolean # Optional. Show in slash menu (default: true)
disable-model-invocation: boolean # Optional. Prevent Claude auto-invoking (default: false)
hooks: object # Optional. PreToolUse/PostToolUse/Stop handlers
---
```

## Invocation Control (v2.1.3+)

Since v2.1.3, skills and slash commands are merged. Both can be user-invoked (`/skill-name`) and model-invoked (Claude uses them contextually).

| Field | Effect |
|-------|--------|
| `user-invocable: false` | Model-only; users cannot invoke via `/command` |
| `disable-model-invocation: true` | User-only; Claude cannot invoke autonomously |

**Model-only skill** (internal primitive):

```yaml
---
name: email-summarize
description: Summarize an email thread. Use when user asks for email digest.
user-invocable: false
---
```

Users see: "This slash command can only be invoked by Claude, not directly by users."

**User-only skill** (explicit command):

```yaml
---
name: dangerous-operation
description: Performs destructive cleanup
disable-model-invocation: true
---
```

Claude will not invoke this autonomously; user must explicitly type `/dangerous-operation`.

### Two-Layer Architecture Pattern

| Layer | Frontmatter | Purpose |
|-------|-------------|---------|
| Core Primitives | `user-invocable: false` | Internal capabilities Claude orchestrates; not in `/help` |
| Driver Skills | (default) | User-facing entry points that compose primitives |

## Examples

**Simple skill:**

```yaml
---
name: commit-helper
description: Generates commit messages from staged changes. Use when user asks for help writing commits or reviewing diffs.
---
```

**Full-featured skill:**

```yaml
---
name: secure-deployment
description: Deploys to production with security checks. Use when deploying, releasing, or pushing to prod.
allowed-tools:
  - Read
  - Bash(git:*)
  - Bash(npm:*)
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

## Links

- Docs: https://code.claude.com/docs/en/skills.md
- Best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Issues:
  - [#9817](https://github.com/anthropics/claude-code/issues/9817) - Multiline description breaks discovery
  - [#13005](https://github.com/anthropics/claude-code/issues/13005) - Custom frontmatter fields stripped
  - [#10589](https://github.com/anthropics/claude-code/issues/10589) - Block scalar style misinterpreted
  - [#13115](https://github.com/anthropics/claude-code/issues/13115) - Skills/commands merge (v2.1.3)
  - [#15842](https://github.com/anthropics/claude-code/issues/15842) - user-invocable naming collision
  - [#16900](https://github.com/anthropics/claude-code/issues/16900) - Documentation gap on skill/command relationship
