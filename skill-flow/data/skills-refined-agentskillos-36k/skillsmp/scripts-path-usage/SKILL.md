---
name: scripts-path-usage
description: |
  This skill provides guidance for ultrawork agents on using SCRIPTS_PATH and accessing session data via scripts.
  Required knowledge for all ultrawork agents (explorer, planner, worker, verifier, reviewer, scope-analyzer).
---

# Scripts Path Usage

## What is SCRIPTS_PATH?

`SCRIPTS_PATH` is the expanded absolute path of `${CLAUDE_PLUGIN_ROOT}/src/scripts`.

Your prompt includes it like this:
```
SCRIPTS_PATH: /Users/name/.claude/plugins/cache/ultrawork/0.25.0/src/scripts
```

Use this path to call Bun scripts.

## ⚠️ WARNING: Placeholder vs Bash Variable Syntax

**CRITICAL: `{SCRIPTS_PATH}` and `${CLAUDE_SESSION_ID}` are TEXT PLACEHOLDERS, not bash environment variables!**

These placeholders appear in this documentation to show WHERE to substitute values. You MUST replace them with actual values from your prompt before running commands.

### Correct Usage

Your prompt provides actual values:
```
SCRIPTS_PATH: /Users/mnthe/.claude/plugins/cache/hardworker-marketplace/ultrawork/0.26.1/src/scripts
CLAUDE_SESSION_ID: 76dfec2a-4187-48eb-8073-9435f4386466
```

**Use the literal values in bash commands:**

✅ **CORRECT:**
```bash
bun "/Users/mnthe/.claude/plugins/cache/hardworker-marketplace/ultrawork/0.26.1/src/scripts/session-get.js" --session 76dfec2a-4187-48eb-8073-9435f4386466
```

### Incorrect Usage

❌ **WRONG - Don't use placeholder syntax in actual commands:**
```bash
# This will NOT work - {SCRIPTS_PATH} is not a bash variable!
bun "{SCRIPTS_PATH}/session-get.js" --session ${CLAUDE_SESSION_ID}
```

❌ **WRONG - These are not shell environment variables:**
```bash
# These variables don't exist in the shell environment
echo $SCRIPTS_PATH           # Empty or undefined
echo $CLAUDE_SESSION_ID      # Empty or undefined
```

### Why This Matters

- **Placeholder notation** (`{SCRIPTS_PATH}`) = documentation convention showing "substitute here"
- **Bash variable** (`$SCRIPTS_PATH`) = shell environment variable (NOT available to agents)
- **Agent reality**: You receive literal path values in your prompt, use them directly

### Quick Rule

**When you see `{SCRIPTS_PATH}` in this documentation → Replace with the actual path from your prompt**

## Core Rules

1. **JSON via scripts, Markdown via Read** - Use `session-get.js`, `task-get.js` for JSON access
2. **Use `--field` for efficiency** - `session-get.js --field phase` returns only what you need

## Quick Reference

| Data | Access Method |
|------|---------------|
| session.json | `bun "{SCRIPTS_PATH}/session-get.js" --session $${CLAUDE_SESSION_ID}` |
| tasks/*.json | `bun "{SCRIPTS_PATH}/task-get.js" --session $${CLAUDE_SESSION_ID} --id 1` |
| exploration/*.md | `Read("~/.claude/ultrawork/sessions/$${CLAUDE_SESSION_ID}/exploration/overview.md")` |
