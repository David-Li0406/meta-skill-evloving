# Atlas Guardrails - Agent Instructions

This repository uses **Atlas Guardrails** to manage context and prevent technical debt.

## Core Rules

1. **Pack Before Editing**: Before modifying code, get context first.
   ```
   atlas_pack(task="description of your task")
   ```

2. **Search Before Creating**: Before creating new utilities, check for duplicates.
   ```
   atlas_find_duplicates(intent="what you want to build")
   ```

3. **Respect Guardrails**: If `atlas check` fails, fix the API drift before continuing.

## MCP Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `atlas_index()` | Rebuild symbol index | Start of session, after major changes |
| `atlas_pack(task, budget)` | Get relevant context | Before any coding task |
| `atlas_find_duplicates(intent)` | Find existing code | Before creating new functions/classes |

## Workflow

```
1. atlas_index()              # Ensure fresh index
2. atlas_pack(task="...")     # Get context for your task
3. [Read the pack.json]       # Understand the codebase
4. atlas_find_duplicates(...) # Check before creating new code
5. [Make your changes]        # Edit with full context
6. atlas check                # Verify no API drift
```

## Important

- **DO NOT** read random files. Use `atlas_pack` to get relevant context.
- **DO NOT** create new utilities without checking `atlas_find_duplicates` first.
- **DO NOT** ignore `atlas check` failures.

The pack output is deterministic and token-optimized. Trust it over manual exploration.
