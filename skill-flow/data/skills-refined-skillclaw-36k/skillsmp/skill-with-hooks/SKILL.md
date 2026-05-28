---
name: skill-with-hooks
description: Example skill demonstrating embedded hooks for validation and logging
version: "1.0.0"
license: MIT
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./hooks/validate-bash.sh"
          timeout: 10
    - matcher: ".*"
      hooks:
        - type: command
          command: "./hooks/log-tool-use.sh"
          timeout: 5
  PostToolUse:
    - matcher: ".*"
      hooks:
        - type: command
          command: "./hooks/log-tool-result.sh"
          timeout: 5
---

# Skill With Hooks Example

This is an example skill that demonstrates how to embed Claude Code-compatible hooks
directly in a skill's frontmatter.

## Purpose

When this skill is loaded, its hooks become active for the session:

1. **PreToolUse (Bash)**: Validates bash commands before execution
2. **PreToolUse (all tools)**: Logs all tool invocations
3. **PostToolUse (all tools)**: Logs tool results

## Hook Scripts

The hooks reference scripts in the `./hooks/` directory relative to this skill:

- `validate-bash.sh` - Checks bash commands for dangerous patterns
- `log-tool-use.sh` - Logs tool name and parameters
- `log-tool-result.sh` - Logs tool execution results

## Usage

Load this skill to activate its hooks:

```
load_skill(skill_name="skill-with-hooks")
```

The hooks will remain active until the session ends.

## Testing

This skill is used to validate the skill-scoped hooks integration between
`amplifier-module-tool-skills` and `amplifier-module-hooks-shell`.
