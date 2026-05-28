---
name: process-logs
description: Use this skill when you need to process error logs from the admin panel, including fetching new errors, analyzing them, creating tasks, fixing issues, and marking them as resolved.
---

# Process Error Logs

Automated workflow for processing error logs from `/admin/logs`.

## CRITICAL REQUIREMENTS

> **YOU MUST FOLLOW THESE RULES. NO EXCEPTIONS.**

### 1. BEADS IS MANDATORY

**EVERY error MUST have a Beads task.** No direct fixes without tracking.

```bash
# ALWAYS run this FIRST for each error:
bd create --type=bug --priority=<1-3> --title="Fix: <error_message>" --files "<relevant_files>"
bd update <task_id> --status=in_progress
```

### 2. TASK COMPLEXITY ROUTING

**Route tasks by complexity:**

| Complexity  | Examples                              | Action                   |
| ----------- | ------------------------------------- | ------------------------ |
| **Simple**  | Typo fix, single import, config value | Execute directly         |
| **Medium**  | Multi-file fix, migration, API change | **Delegate to subagent** |
| **Complex** | Architecture change, new feature      | Ask user first           |

**Subagent selection for MEDIUM tasks:**

- DB/migration → `database-architect`
- API/tRPC → `fullstack-nextjs-specialist`
- Types → `typescript-types-specialist`
- UI → `nextjs-ui-designer`

**Execute directly for SIMPLE tasks:**

- Single-line fix (typo, wrong value)
- Import path correction
- Config constant change
- Comment fix

### 3. CONTEXT7 IS MANDATORY

**ALWAYS query documentation before implementing:**

```
mcp__context7__resolve-library-id → mcp__context7__query-docs
```

### 4. BUG FIXING PRINCIPLES

> **This is PRODUCTION. Every bug matters.**

**Fix fundamentally, not superficially:**

- Find and fix the ROOT CAUSE, not just symptoms
- If error happens in function X but cause is in function Y → fix Y
- Don't add workarounds/hacks that mask the problem
- Ask: "Why did this happen?" until you reach the actual cause

**Never ignore errors:**

- Every error indicates a real problem
- "Works most of the time" is NOT acceptable
- External service errors → add retry logic or graceful degradation
- Config warnings → fix config or make truly optional

**Propose improvements:**

- If you see code that could be better → create separate Beads task
- If fix reveals related issues → document them
- If pattern repeats → suggest refactoring to prevent future bugs
- Format: `bd create --type=chore --title="Improve: <description>"`

**Quality over speed:**

- Take time to understand the problem thoroughly before implementing a fix.