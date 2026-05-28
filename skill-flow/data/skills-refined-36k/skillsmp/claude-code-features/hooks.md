# Hooks

**Trigger**: Event-driven (PreToolUse, PostToolUse, SessionStart, etc.)

## Characteristics

- Implemented as shell commands
- **Deterministic** behavior (no LLM judgment dependency)
- Can block with exit code 2

## Best For

- Auto-format/lint after file edits
- Blocking dangerous commands
- Pre-commit validation
- Sending notifications
- Logging

## Not Suitable For

- Context-dependent decisions (→ Skills/Agents)
- Complex workflows (→ Commands)
