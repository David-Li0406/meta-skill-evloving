---
name: review-captured
description: Review recently captured commands from Claude sessions
allowed-tools: Read, Bash, Glob
---

# Review Captured Commands

Review the commands that have been captured during Claude sessions.

## Instructions

1. Read the captured commands log at `.claude/captured/commands.jsonl`
2. Parse the JSONL and display the commands in a readable format
3. Group by base_command if there are many entries
4. Show the most recent 20 commands by default
5. Highlight any patterns that might be good candidates for the baseline

## Output Format

Display commands like:

```
Recent Captured Commands
========================

[timestamp] command
  └─ description

...
```

## Candidate Identification

Look for:
- Commands used frequently
- Commands with clear, safe patterns
- Commands that represent common workflows

Suggest which commands might be good to promote to the baseline using `/add-rule`.
