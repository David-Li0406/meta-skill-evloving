# context: fork

Runs skill in isolated subagent with separate conversation history.

## How It Works

- Separate context window (doesn't pollute main conversation)
- Can specify agent type via `agent` field
- Results returned to main conversation when complete

## Agent Options

| Agent             | Speed        | Use Case                   |
| ----------------- | ------------ | -------------------------- |
| `Explore`         | Fast (Haiku) | Read-only code exploration |
| `Plan`            | Medium       | Research and planning      |
| `general-purpose` | Full         | Multi-step complex work    |

## Examples

**Code analysis in isolation:**

```yaml
---
name: code-review
description: Reviews code quality and suggests improvements
context: fork
agent: general-purpose
---

# Code Review

Analyze the code for:
1. Security vulnerabilities
2. Performance issues
3. Code style violations

Output a structured report.
```

**Quick exploration:**

```yaml
---
name: find-patterns
description: Finds code patterns across the codebase
context: fork
agent: Explore
---
Search for the requested pattern and summarize findings.
```

## Links

- Docs: https://code.claude.com/docs/en/sub-agents.md
- Issues:
  - [#14016](https://github.com/anthropics/claude-code/issues/14016) - Skills don't auto-activate in spawned agents
  - [#12633](https://github.com/anthropics/claude-code/issues/12633) - Request for subagent-exclusive skills
