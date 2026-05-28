# Frontmatter Hooks

Define hooks directly in Skills, Agents, and Slash Commands using YAML frontmatter. These hooks are lifecycle-scoped and automatically cleaned up when the component finishes.

## Overview

| Aspect | Description |
|--------|-------------|
| **Supported Components** | Skills, Agents, Slash Commands |
| **Supported Events** | `PreToolUse`, `PostToolUse`, `Stop` |
| **Lifecycle** | Active only during component execution |
| **Cleanup** | Automatic when component finishes |

## Supported Components

| Component | File Location | Use Case |
|-----------|---------------|----------|
| Skills | `.claude/skills/*/SKILL.md` | Validation during skill execution |
| Agents | `.claude/agents/*.md` | Agent-specific tool control |
| Slash Commands | `.claude/commands/*.md` | Command-specific automation |

## Syntax

The `hooks` field in frontmatter uses the same structure as settings-based hooks:

```yaml
---
name: component-name
description: Component description
hooks:
  EventName:
    - matcher: "ToolPattern"
      hooks:
        - type: command
          command: "your-command"
          timeout: 30
          once: true
---
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `matcher` | string | For PreToolUse/PostToolUse | Regex pattern for tool names |
| `hooks` | array | Yes | Array of hook definitions |
| `type` | string | Yes | `command` or `prompt` |
| `command` | string | For command type | Bash command to execute |
| `prompt` | string | For prompt type | Prompt for LLM evaluation |
| `timeout` | number | No | Timeout in seconds (default: 60) |
| `once` | boolean | No | Run only once per session |

## The `once` Option

The `once: true` option runs the hook only once during the component's lifecycle, even if the trigger occurs multiple times.

### Use Cases

- One-time validation at component start
- Initial setup that shouldn't repeat
- Environment checks before first tool use

### Example

```yaml
---
name: deploy-skill
description: Deployment workflow with one-time validation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./check-deploy-ready.sh"
          once: true  # Only runs before first Bash call
---
```

## Examples by Component

### Skill with Hooks

```yaml
---
name: code-review
description: Code review skill with auto-linting
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "npx eslint --fix \"$TOOL_INPUT_file_path\""
  Stop:
    - hooks:
        - type: command
          command: "./summarize-review.sh"
---

# Code Review Skill

This skill reviews code and auto-lints on file changes.
```

### Agent with Hooks

```yaml
---
name: secure-agent
description: Agent with security validation
tools: ["Read", "Grep", "Glob"]
hooks:
  PreToolUse:
    - matcher: ".*"
      hooks:
        - type: command
          command: "./security-check.sh"
          once: true
  Stop:
    - hooks:
        - type: command
          command: "./audit-log.sh"
---

# Secure Agent

A read-only agent with security logging.
```

### Slash Command with Hooks

```yaml
---
description: Deploy with pre-flight checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./preflight-check.sh"
          once: true
---

Deploy the current branch to staging environment.

Check all tests pass before deploying.
```

## Lifecycle Behavior

### When Hooks Are Active

```
Component Invoked
       │
       ▼
┌─────────────────┐
│ Hooks Registered │ ◄── Frontmatter hooks become active
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Component Runs   │ ◄── Hooks fire on matching events
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Component Ends   │ ◄── Frontmatter hooks removed
└─────────────────┘
```

### Hook Priority

When multiple hooks match the same event:

1. Settings-based hooks run first (project, then user)
2. Frontmatter hooks run after settings hooks
3. Within frontmatter, hooks run in definition order

## Comparison: Settings vs Frontmatter Hooks

| Feature | Settings Hooks | Frontmatter Hooks |
|---------|----------------|-------------------|
| **Location** | `settings.json` | Component YAML frontmatter |
| **Scope** | Global/project-wide | Component lifecycle only |
| **Events** | All 10 events | PreToolUse, PostToolUse, Stop |
| **Active** | Always (when enabled) | Only during component execution |
| **Cleanup** | Manual management | Automatic |
| **`once` option** | Not supported | Supported |
| **Distribution** | Separate config | Bundled with component |
| **Use case** | Project automation | Component-specific behavior |

## When to Use Frontmatter Hooks

### Use Frontmatter Hooks When:

- Hook logic is specific to one skill/agent/command
- You want hooks bundled for distribution
- Hooks should only run during component execution
- You need the `once: true` option

### Use Settings Hooks When:

- Hooks apply project-wide
- You need events not supported in frontmatter
- Hooks should persist across all components
- Enterprise policy enforcement

## Environment Variables

Frontmatter hooks have access to the same environment variables as settings hooks:

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Absolute path to project root |
| `TOOL_INPUT_*` | Tool input fields (PreToolUse/PostToolUse) |
| `TOOL_OUTPUT_*` | Tool output fields (PostToolUse only) |

## Debugging

### Check Hook Registration

Use `/hooks` in Claude Code to see all registered hooks, including frontmatter hooks during component execution.

### Debug Mode

```bash
claude --debug
```

Shows hook registration and execution logs.

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Hook not firing | Wrong event name | Use PreToolUse, PostToolUse, or Stop only |
| Hook runs multiple times | Missing `once: true` | Add `once: true` for one-time hooks |
| Hook not registered | YAML syntax error | Validate YAML frontmatter |
| Command not found | Relative path | Use absolute path or `$CLAUDE_PROJECT_DIR` |

## Security Considerations

- Frontmatter hooks in distributed skills run with user permissions
- Validate inputs before executing commands
- Use absolute paths for script references
- Consider sandboxing for untrusted skills

## Related Documentation

- [SKILL.md](./SKILL.md) - Main hooks documentation
- [EVENTS.md](./EVENTS.md) - All hook events reference
- [EXAMPLES.md](./EXAMPLES.md) - More hook examples
