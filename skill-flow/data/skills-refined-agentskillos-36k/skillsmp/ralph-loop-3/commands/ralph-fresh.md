---
description: "Start Ralph Loop with fresh context per iteration"
argument-hint: "PROMPT [--task-id ID] [--max-iterations N] [--completion-promise TEXT]"
allowed-tools: ["Bash(${CLAUDE_PLUGIN_ROOT}/scripts/setup-fresh-loop.sh:*)"]
hide-from-slash-command-tool: "true"
---

# Ralph Fresh Loop

Execute the setup script to initialize a fresh-context Ralph loop:

```!
"${CLAUDE_PLUGIN_ROOT}/scripts/setup-fresh-loop.sh" $ARGUMENTS
```

This starts an autonomous loop where history is cleared between iterations. Each iteration gets a fresh Claude session, preventing context pollution from previous attempts.

## When to use

- **Hallucination prevention**: When the agent starts repeating mistakes due to previous history
- **Large tasks**: When the context window would otherwise get too full
- **Independent steps**: When each iteration is a discrete step that doesn't need full conversation history

CRITICAL RULE: If a completion promise is set, you may ONLY output it when the statement is completely and unequivocally TRUE. Do not output false promises to escape the loop.
