---
name: process-logs
description: Process error logs from admin panel - fetch new errors, analyze, create tasks, fix, and mark resolved
version: 1.5.0
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

- Take time to understand the full context
- Test the fix mentally: "What else could break?"
- Check for similar patterns elsewhere in codebase
- One good fix > multiple quick patches

### 5. LOG NOTES (MANDATORY)

**Always write notes when updating log status.** Keep it brief, in English.

| Status        | What to write in notes                                                                           |
| ------------- | ------------------------------------------------------------------------------------------------ |
| `resolved`    | Root cause + fix applied. Example: `Missing constraint. Added 'approved' to enum via migration.` |
| `auto_muted`  | **System-assigned.** Don't change. Skip these errors in processing.                              |
| `ignored`     | **Never use.** Fix or ask user.                                                                  |
| `to_verify`   | Why pending + what to check. Example: `External API timeout. Monitor for 24h.`                   |
| `in_progress` | Beads task ID. Example: `Working on mc2-5ch`                                                     |

**Format:** `<root_cause>. <action_taken>.` — Max 100 chars.

**Examples:**

- `ESM import conflict. Renamed generator.ts to generator-node.ts.`
- `Constraint missing 'approved'. Added via migration 20250115_fix_status.`
- `Cloudflare 500. External issue, retry logic already exists. Monitoring.`

### 6. AUTO-MUTED ERRORS

Some errors are **automatically ignored** by the system with status `auto_muted`. These are expected events, NOT bugs.

**Current auto-mute rules** (from `src/shared/logger/auto-classification.ts`):

| Pattern                            | Reason            | Description                           |
| ---------------------------------- | ----------------- | ------------------------------------- |
| `Redis connection (ended\|closed)` | graceful_shutdown | Redis disconnects during app restart  |
| `graceful.*shutdown`               | graceful_shutdown | Server shutdown events during deploys |
| `/health.*404`                     | monitoring_probe  | Health probes from monitoring tools   |
| `Cloudflare.*5xx`                  | external_service  | Cloudflare edge errors                |
| `ECONNRESET.*external`             | external_service  | External API connection resets        |

**When you see `auto_muted` errors:**

- Skip them in processing — they don't need fixes
- If you see a pattern that should be auto-muted, add it to `auto-classification.ts`

**How to add a new auto-mute rule:**

1. Edit `packages/course-gen-platform/src/shared/logger/auto-classification.ts`:

   ```typescript
   {
     pattern: /your-pattern/i,
     reason: 'category',  // graceful_shutdown | monitoring_probe | external_service
     description: 'Why this is expected',
   }
   ```

2. Update this SKILL.md with the new pattern

**When NOT to auto-mute:**

- Errors that SOMETIMES indicate real problems
- New error types (analyze first, then decide)
- Anything affecting user experience

### 7. SEARCH SIMILAR PROBLEMS FIRST

**Before fixing, check if we solved this before:**

```sql
-- Search similar errors by message (use mcp__supabase__execute_sql)
SELECT el.id, el.error_message, el.severity, lis.status, lis.notes, el.created_at
FROM error_logs el
LEFT JOIN log_issue_status lis ON lis.log_id = el.id AND lis.log_type = 'error_log'
WHERE to_tsvector('english', el.error_message) @@ plainto_tsquery('english', '<keyword>')
  AND lis.status = 'resolved'
ORDER BY el.created_at DESC
LIMIT 5;
```

**What to search for:**

- Key error terms: `constraint`, `undefined`, `timeout`, `not found`
- Function/module names from stack trace
- Error codes or specific identifiers

**If found similar resolved issue:**

1. Read the `notes` field — contains root cause and fix
2. Apply same solution pattern if applicable
3. Reference in your notes: `Similar to <date>. Same fix applied.`

## Usage

Invoke via: `/process-logs` or "обработай логи ошибок"

## Workflow

### Step 1: Fetch New Errors

```sql
-- Use mcp__supabase__execute_sql
-- NOTE: This excludes auto_muted errors (they are handled automatically)
SELECT el.id, el.severity, el.error_message, el.metadata, el.stack_trace,
       el.course_id, el.lesson_id, el.request_id, el.trpc_path, el.trpc_input, el.attempted_value
FROM error_logs el
LEFT JOIN log_issue_status lis ON lis.log_id = el.id AND lis.log_type = 'error_log'
WHERE lis.id IS NULL OR (lis.status NOT IN ('resolved', 'ignored', 'auto_muted'))
ORDER BY
  CASE el.severity WHEN 'CRITICAL' THEN 1 WHEN 'ERROR' THEN 2 ELSE 3 END,
  el.created_at DESC
LIMIT 20;
```

### Step 2: For EACH Error (Loop)

```
FOR each error:
  1. CREATE BEADS TASK (MANDATORY):
     bd create --type=bug --priority=<1-3> --title="Fix: <message>" --files "<files>"
     bd update <id> --status=in_progress

  2. ANALYZE error type and SELECT subagent:
     - DB constraint → database-architect
     - tRPC/API → fullstack-nextjs-specialist
     - Types → typescript-types-specialist
     - UI → nextjs-ui-designer

  3. QUERY context7 for relevant docs

  4. DELEGATE using Task tool:
     Task(subagent_type="<selected>", prompt="Fix error: <details>...")

  5. VERIFY results (MANDATORY):
     - Read tool: check modified files
     - Bash: pnpm type-check && pnpm build
     - If errors → re-delegate

  6. MARK resolved in DB:
     INSERT INTO log_issue_status (log_type, log_id, status, notes, updated_at)
     VALUES ('error_log', '<id>', 'resolved', 'Fixed: <desc>', NOW())
     ON CONFLICT (log_type, log_id) DO UPDATE SET status = 'resolved', notes = EXCLUDED.notes, updated_at = NOW();

  7. CLOSE Beads task:
     bd close <id> --reason="Fixed"
```

### Step 3: Summary Report

```markdown
## Log Processing Summary

| Severity | Fixed | Pending | To Verify |
| -------- | ----- | ------- | --------- |
| CRITICAL | X     | Y       | Z         |
| ERROR    | X     | Y       | Z         |
| WARNING  | X     | Y       | Z         |

### Beads Tasks Created:

- mc2-xxx: <description> → <status>

### Pending (need user input):

- <log_id>: <reason>
```

## Subagent Delegation Examples

### DB Constraint Error

```
Task(
  subagent_type="database-architect",
  prompt="Fix DB constraint violation in error_logs.
  Error: <full_error_message>
  Context: <stack_trace>
  Course: <course_id>
  Create migration to fix the constraint."
)
```

### tRPC/API Error

```
Task(
  subagent_type="fullstack-nextjs-specialist",
  prompt="Fix tRPC error in <trpc_path>.
  Error: <full_error_message>
  Input: <trpc_input>
  Stack: <stack_trace>
  Fix the API endpoint."
)
```

### Type Error

```
Task(
  subagent_type="typescript-types-specialist",
  prompt="Fix TypeScript type error.
  Error: <full_error_message>
  File: <file_path>
  Fix types and ensure compatibility."
)
```

## Verification Checklist

Before marking ANY error as resolved:

- [ ] Beads task exists for this error
- [ ] Subagent was used (if not trivial fix)
- [ ] Modified files reviewed with Read tool
- [ ] `pnpm type-check` passes
- [ ] `pnpm build` passes
- [ ] No new errors introduced
- [ ] Beads task closed with reason

## Error Categories

| Pattern                | Category      | Subagent                      | Priority |
| ---------------------- | ------------- | ----------------------------- | -------- |
| `violates.*constraint` | DB constraint | `database-architect`          | 1        |
| `tRPC error`           | API bug       | `fullstack-nextjs-specialist` | 2        |
| `Type.*error`          | Type error    | `typescript-types-specialist` | 2        |
| `Error querying`       | Query bug     | `database-architect`          | 2        |
| Config missing         | Config issue  | **ASK USER**                  | 3        |
| External service       | External      | mark `to_verify`              | 3        |
| Redis shutdown         | Expected      | **SKIP** (auto_muted)         | -        |
| Health probe 404       | Expected      | **SKIP** (auto_muted)         | -        |

**Errors with status `auto_muted` are automatically ignored by the system. Skip them.**

## Reference Docs

- Admin Logs Guide: `.claude/docs/admin-logs-guide.md`
- Error Types: `packages/course-gen-platform/src/shared/logger/types.ts`
- Logs Router: `packages/course-gen-platform/src/server/routers/admin/logs.ts`
- CLAUDE.md: Main orchestration rules
