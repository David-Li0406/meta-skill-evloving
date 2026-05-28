# Plan: Uplift Triage Skill to Native TodoWrite with blockedBy

## Current State

The triage skill uses a **custom JSON state file** (`~/.claude/para-triage-state.json`) for:
- Session tracking (`session_id`, `started_at`, `status`)
- Progress tracking (`processed[]`, `pending[]`, `current_batch`)
- Resume capability (skip already-processed items)

## Target State

Replace custom state management with **native Claude Code TodoWrite tool** which provides:
- Built-in persistence (`~/.claude/tasks/` via `CLAUDE_CODE_TASK_LIST_ID`)
- Native UI (`Ctrl+T` to view)
- `blockedBy` dependencies for execution ordering
- Cross-session resume via environment variable

## Scope

**Single-session workflow.** This plan is for triage running in one Claude Code session at a time.

Multi-session orchestration (e.g., Jira ticket decomposition across git worktrees) is a **separate pattern** requiring external state coordination - out of scope for this uplift.

---

## Critical Design Decisions

### Decision 1: Extend TodoWrite Schema for blockedBy

**Problem:** Native TodoWrite doesn't support `blockedBy` - we need task dependencies.

**Solution:** Create a **wrapper skill pattern** that:
1. Uses native TodoWrite for persistence/UI
2. Encodes dependency information in structured task content
3. Provides helper instructions for interpreting dependencies

**Extended Schema (encoded in content):**

```typescript
// Native TodoWrite call
TodoWrite({
  todos: [
    {
      id: "triage:batch-1:item-1",
      content: "[DEPS:none] Distill: ✂️ Article Title",
      status: "pending",
      priority: "medium"
    },
    {
      id: "triage:batch-1:review",
      content: "[DEPS:triage:batch-1:item-1,triage:batch-1:item-2,triage:batch-1:item-3] Review batch 1",
      status: "pending",
      priority: "high"
    }
  ]
})
```

**Dependency encoding format:**
```
[DEPS:none]           → No dependencies, can start immediately
[DEPS:id1,id2,id3]    → Blocked until all listed IDs are completed
```

**Skill instructions parse this and enforce:**
- Don't start a task with `[DEPS:...]` until all deps are `completed`
- When marking a task complete, check if it unblocks others

### Decision 2: Namespace Tasks by Workflow Domain

**Problem:** Multiple workflows (triage, distill, review-pr, etc.) could pollute the same task list.

**Solution:** Use **hierarchical task IDs** with domain prefix:

```
{domain}:{workflow}:{identifier}
```

**Examples:**
```
triage:batch-1:item-1      → Triage workflow, batch 1, item 1
triage:batch-1:review      → Triage workflow, batch 1, review phase
distill:single:article-xyz → Distill workflow, single mode, specific article
git:pr-123:review          → Git workflow, PR review task
```

**Benefits:**
1. **Isolation** - TodoRead can filter by prefix: `triage:*`
2. **Cleanup** - Clear all tasks for a workflow: remove all `triage:*`
3. **Multiple workflows** - Run triage AND pr-review simultaneously
4. **Hierarchy** - Batch grouping is visible in task structure

### Decision 3: Task State Machine

**Problem:** Need to enforce dependency order without native blockedBy.

**Solution:** Skill instructions define state transitions:

```
┌──────────────────────────────────────────────────────────────────┐
│                     TASK STATE MACHINE                           │
│                                                                  │
│  [DEPS:none] + pending     → CAN start (mark in_progress)       │
│  [DEPS:x,y]  + pending     → CHECK if x,y are completed         │
│                              ├─ All completed → CAN start       │
│                              └─ Not all → BLOCKED (stay pending)│
│  in_progress               → Working on it                      │
│  completed                 → Done, may unblock others           │
└──────────────────────────────────────────────────────────────────┘
```

**Enforcement in SKILL.md:**
```markdown
### Before Starting Any Task

1. Parse the `[DEPS:...]` prefix from task content
2. If deps exist, check each dep's status via TodoRead
3. Only proceed if ALL dependencies are `completed`
4. If blocked, move to next unblocked task or wait
```

---

## Architecture Change

### Before (Custom JSON)
```
┌─────────────────────────────────────────┐
│   ~/.claude/para-triage-state.json      │
│  {                                      │
│    processed: [...],                    │
│    pending: [...],                      │
│    current_batch: 2                     │
│  }                                      │
└─────────────────────────────────────────┘
```

### After (Native TodoWrite + Encoded Dependencies)
```
┌────────────────────────────────────────────────────────────────────────────────┐
│                              TodoWrite                                          │
│                                                                                │
│  triage:batch-1:item-1  [completed]   "[DEPS:none] Distill: ✂️ Article 1"      │
│  triage:batch-1:item-2  [completed]   "[DEPS:none] Distill: ✂️ Article 2"      │
│  triage:batch-1:item-3  [completed]   "[DEPS:none] Distill: 🎤 Voice memo"     │
│                                                                                │
│  triage:batch-1:review  [completed]   "[DEPS:triage:batch-1:item-1,...]        │
│                                        Review batch 1 proposals"               │
│                                                                                │
│  triage:batch-2:item-1  [in_progress] "[DEPS:triage:batch-1:review]            │
│                                        Distill: ✂️ Article 3"                  │
│  triage:batch-2:item-2  [pending]     "[DEPS:triage:batch-1:review]            │
│                                        Distill: ✂️ Article 4"                  │
│  triage:batch-2:item-3  [pending]     "[DEPS:triage:batch-1:review]            │
│                                        Distill: 🎤 Voice memo 2"               │
│                                                                                │
│  triage:batch-2:review  [pending]     "[DEPS:triage:batch-2:item-1,...]        │
│                                        Review batch 2 proposals"               │
│                                                                                │
│  triage:cleanup         [pending]     "[DEPS:triage:batch-2:review]            │
│                                        Cleanup triage tasks"                   │
└────────────────────────────────────────────────────────────────────────────────┘

Key Design Patterns:
1. Namespace prefix: "triage:" isolates from other workflows
2. Dependency encoding: [DEPS:id1,id2] in content (parsed by skill)
3. Hierarchical IDs: domain:scope:identifier
4. Cleanup task: removes all triage:* on completion
```

---

## Implementation Plan

### Phase 1: Understand TodoWrite API

**Current TodoWrite schema (from system prompt extraction):**
```typescript
{
  todos: {
    content: string;           // Task description
    status: "pending" | "in_progress" | "completed";
    priority: "high" | "medium" | "low";
    id: string;
  }[];
}
```

**blockedBy feature (from CJ Hess article):**
- Tasks can reference other task IDs they depend on
- Blocked tasks don't execute until dependencies complete
- Externalizes execution order outside context (survives compaction)

**CRITICAL GAP:** The extracted system prompt shows `id` but not `blockedBy`. Need to verify:
1. Is `blockedBy` in the actual API?
2. Is it `addBlockedBy` parameter on Task tool?
3. Or is it TodoWrite with extended schema?

**Action:** Test in a Claude Code session to discover exact API.

### Phase 2: Design Task Structure

**Task naming convention:**
```
BATCH-{batch_num}-{item_num}: "Distill: {icon} {title}"
REVIEW-{batch_num}: "Review batch {batch_num} proposals"
```

**Dependency graph for 9 items (3 batches):**
```
Batch 1 (parallel):
  - BATCH-1-1 (no deps)
  - BATCH-1-2 (no deps)
  - BATCH-1-3 (no deps)

Review 1 (sequential):
  - REVIEW-1 blockedBy [BATCH-1-1, BATCH-1-2, BATCH-1-3]

Batch 2 (parallel, after review):
  - BATCH-2-1 blockedBy [REVIEW-1]
  - BATCH-2-2 blockedBy [REVIEW-1]
  - BATCH-2-3 blockedBy [REVIEW-1]

Review 2 (sequential):
  - REVIEW-2 blockedBy [BATCH-2-1, BATCH-2-2, BATCH-2-3]

... and so on
```

### Phase 3: Update SKILL.md

**Changes to triage/SKILL.md:**

1. **Remove Phase 5 (State Persistence)** - Native TodoWrite handles this

2. **Add allowed-tools:** `TodoWrite, TodoRead`

3. **Update Phase 0.1 (Load State):**
   ```markdown
   ### 0.1 Check for Resume (if continuing)

   Use TodoRead to check for existing triage tasks:

   ```
   TodoRead()
   ```

   If tasks exist with pattern `BATCH-*` or `REVIEW-*`:
   - Show user the pending tasks
   - Offer to resume or start fresh
   ```

4. **Update Phase 1.1 (Spawn Subagents):**
   ```markdown
   ### 1.1 Create Batch Tasks

   For each batch of 3 items, create tasks with dependencies:

   ```
   TodoWrite({
     todos: [
       // Batch N items (parallel - no deps on each other)
       { id: "BATCH-N-1", content: "Distill: ✂️ [title1]", status: "pending", priority: "medium" },
       { id: "BATCH-N-2", content: "Distill: 🎤 [title2]", status: "pending", priority: "medium" },
       { id: "BATCH-N-3", content: "Distill: ✂️ [title3]", status: "pending", priority: "medium" },
       // Review task (blocked until batch completes)
       { id: "REVIEW-N", content: "Review batch N proposals", status: "pending", priority: "high", blockedBy: ["BATCH-N-1", "BATCH-N-2", "BATCH-N-3"] }
     ]
   })
   ```

   Then spawn 3 Task subagents in parallel (single message).
   ```

5. **Update Phase 2 (Sequential Review):**
   ```markdown
   ### 2.0 Mark Review In Progress

   When starting review:
   ```
   TodoWrite({ todos: [
     { id: "REVIEW-N", content: "Review batch N proposals", status: "in_progress", priority: "high" }
   ]})
   ```

   After each proposal is handled (A/E/S/D):
   ```
   TodoWrite({ todos: [
     { id: "BATCH-N-X", content: "...", status: "completed", priority: "medium" }
   ]})
   ```
   ```

6. **Add Quit Behavior:**
   ```markdown
   ### Q (Quit) Action

   When user quits:
   1. Current task statuses are already persisted in TodoWrite
   2. No need to save JSON file
   3. Next session: TodoRead() shows pending tasks
   4. User can resume with "continue triage" or start fresh
   ```

### Phase 4: Add Session Persistence

**Environment variable for cross-session persistence:**

Update command documentation (`commands/triage.md`):
```markdown
## Cross-Session Persistence

For long triage sessions that span terminal restarts:

```bash
CLAUDE_CODE_TASK_LIST_ID=inbox-triage claude
```

This stores tasks in `~/.claude/tasks/inbox-triage/` and survives terminal closes.
```

### Phase 5: Remove Custom State File

1. Delete references to `~/.claude/para-triage-state.json`
2. Remove Phase 5 (State Persistence) entirely
3. Update Resume Capability section to use TodoRead

---

## Benefits of Native TodoWrite

| Aspect | Custom JSON | Native TodoWrite |
|--------|------------|------------------|
| **Visibility** | Hidden file | Ctrl+T shows tasks |
| **Persistence** | Manual JSON writes | Automatic |
| **Dependencies** | Manual tracking | blockedBy enforces order |
| **Parallelism** | We manage | System optimizes |
| **Resume** | Parse JSON | TodoRead() |
| **Cross-session** | Manual path | CLAUDE_CODE_TASK_LIST_ID |

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| blockedBy API different than expected | Test in session first, adapt design |
| No blockedBy support | Fall back to sequential TodoWrite updates |
| Task list UI gets cluttered | Use clear naming, mark completed tasks |
| Lost context on what was already reviewed | Include proposal summary in task content |

---

## Next Steps

1. **Verify blockedBy API** - Test in live Claude Code session
2. **Prototype** - Try manual TodoWrite with dependencies
3. **Update SKILL.md** - Implement changes per Phase 3
4. **Test end-to-end** - Full triage session with native tasks
5. **Document** - Update command docs with persistence info

---

## Open Questions

1. **Is `blockedBy` part of TodoWrite schema or Task tool?**
   - CJ Hess mentions it but extracted prompt doesn't show it
   - **RESOLVED:** We encode deps in content with `[DEPS:...]` pattern

2. **Can we update existing tasks or only replace all?**
   - TodoWrite takes full `todos[]` array
   - **RESOLVED:** Read with TodoRead, merge changes, write full array

3. **What happens to completed tasks?**
   - Do they persist forever?
   - **RESOLVED:** Clean up domain tasks on workflow completion

4. **Task ID format constraints?**
   - Can we use our BATCH-N-M format?
   - **RESOLVED:** Use `domain:workflow:identifier` hierarchy

---

## Detailed Implementation: Dependency Encoding

### The [DEPS:...] Pattern

Since native TodoWrite doesn't have `blockedBy`, we encode dependencies in a parseable prefix:

```
Task Content Format:
[DEPS:{dep-list}] {human-readable description}

Where dep-list is:
- "none"           → No dependencies
- "id1"            → Single dependency
- "id1,id2,id3"    → Multiple dependencies (all must complete)
```

### Parsing Dependencies

```typescript
// Pseudocode for skill instructions
function parseDeps(content: string): string[] {
  const match = content.match(/^\[DEPS:([^\]]+)\]/);
  if (!match) return [];
  if (match[1] === "none") return [];
  return match[1].split(",");
}

function isUnblocked(task: Todo, allTasks: Todo[]): boolean {
  const deps = parseDeps(task.content);
  if (deps.length === 0) return true;

  return deps.every(depId => {
    const depTask = allTasks.find(t => t.id === depId);
    return depTask?.status === "completed";
  });
}
```

### Skill Instructions for Dependency Enforcement

Add to SKILL.md:

```markdown
## Dependency Management

### Reading Task Dependencies

Before working on any task, check its dependencies:

1. **TodoRead()** to get all tasks
2. Find your target task by ID
3. Parse `[DEPS:...]` from content
4. Check if all dependency IDs have `status: completed`

### Example Check

```
TodoRead() returns:
- triage:batch-1:item-1 [completed] "[DEPS:none] Distill: Article 1"
- triage:batch-1:item-2 [completed] "[DEPS:none] Distill: Article 2"
- triage:batch-1:item-3 [in_progress] "[DEPS:none] Distill: Article 3"
- triage:batch-1:review [pending] "[DEPS:triage:batch-1:item-1,triage:batch-1:item-2,triage:batch-1:item-3] Review batch 1"

Q: Can we start triage:batch-1:review?
A: NO - triage:batch-1:item-3 is not completed yet

After item-3 completes:
A: YES - all deps (item-1, item-2, item-3) are completed
```

### Updating Task Status

When completing a task:
1. TodoRead() to get current state
2. Update target task's status to "completed"
3. TodoWrite() with full updated array
4. Check if any blocked tasks are now unblocked
```

---

## Namespace Design: Domain Prefixes

### Standard Prefixes

| Domain | Prefix | Example IDs |
|--------|--------|-------------|
| Triage | `triage:` | `triage:batch-1:item-1`, `triage:batch-1:review` |
| Distill | `distill:` | `distill:single:article-xyz` |
| Git | `git:` | `git:pr-123:review`, `git:commit:validation` |
| Build | `build:` | `build:typecheck`, `build:test`, `build:lint` |

### Hierarchy Levels

```
{domain}:{scope}:{identifier}

domain     = workflow type (triage, distill, git, build)
scope      = grouping within domain (batch-1, single, pr-123)
identifier = specific task (item-1, review, typecheck)
```

### Filtering by Namespace

In skill instructions:
```markdown
### Finding Triage Tasks

```
TodoRead() → filter where id.startsWith("triage:")
```

### Cleanup After Workflow

```
TodoRead() →
  keep tasks where NOT id.startsWith("triage:") →
  TodoWrite(remaining)
```
```

---

## Full Example: Triage 6 Items (2 Batches)

### Initial TodoWrite

```
TodoWrite({
  todos: [
    // Batch 1 - parallel (no deps on each other)
    { id: "triage:batch-1:item-1", content: "[DEPS:none] Distill: ✂️ Claude Code Article", status: "pending", priority: "medium" },
    { id: "triage:batch-1:item-2", content: "[DEPS:none] Distill: ✂️ TypeScript Tips", status: "pending", priority: "medium" },
    { id: "triage:batch-1:item-3", content: "[DEPS:none] Distill: 🎤 Meeting Notes", status: "pending", priority: "medium" },

    // Batch 1 review - blocked until all items done
    { id: "triage:batch-1:review", content: "[DEPS:triage:batch-1:item-1,triage:batch-1:item-2,triage:batch-1:item-3] Review batch 1 proposals", status: "pending", priority: "high" },

    // Batch 2 - blocked until batch 1 review done
    { id: "triage:batch-2:item-1", content: "[DEPS:triage:batch-1:review] Distill: ✂️ React Patterns", status: "pending", priority: "medium" },
    { id: "triage:batch-2:item-2", content: "[DEPS:triage:batch-1:review] Distill: ✂️ Database Design", status: "pending", priority: "medium" },
    { id: "triage:batch-2:item-3", content: "[DEPS:triage:batch-1:review] Distill: 📎 Invoice PDF", status: "pending", priority: "medium" },

    // Batch 2 review
    { id: "triage:batch-2:review", content: "[DEPS:triage:batch-2:item-1,triage:batch-2:item-2,triage:batch-2:item-3] Review batch 2 proposals", status: "pending", priority: "high" },

    // Final cleanup
    { id: "triage:cleanup", content: "[DEPS:triage:batch-2:review] Cleanup triage session", status: "pending", priority: "low" }
  ]
})
```

### Execution Flow

```
1. Start: Find unblocked tasks (DEPS:none)
   → batch-1:item-1, item-2, item-3 are unblocked
   → Spawn 3 subagents in parallel

2. After batch 1 items complete:
   → batch-1:review is now unblocked
   → Present proposals sequentially to user

3. After batch 1 review complete:
   → batch-2:item-1, item-2, item-3 are now unblocked
   → Spawn next 3 subagents

4. After batch 2 items complete:
   → batch-2:review is unblocked
   → Present proposals

5. After batch 2 review:
   → cleanup is unblocked
   → Remove all triage:* tasks
```

---

## Helper Functions (Skill Instructions)

### Find Unblocked Tasks

```markdown
To find tasks ready to execute:

1. TodoRead() to get all tasks
2. Filter to your domain: `id.startsWith("triage:")`
3. Filter to pending: `status === "pending"`
4. For each, check if unblocked:
   - Parse [DEPS:...] from content
   - If "none" → unblocked
   - If list → check all deps are "completed"
5. Return unblocked tasks
```

### Mark Task Complete and Check Unblocks

```markdown
When finishing a task:

1. TodoRead() to get current state
2. Find your task, set status = "completed"
3. Find tasks that depend on your task ID
4. For each dependent:
   - Check if ALL its deps are now completed
   - If yes, it's now ready (log: "Unblocked: {id}")
5. TodoWrite() with updated array
```

### Cleanup Domain Tasks

```markdown
After workflow completes:

1. TodoRead() to get all tasks
2. Filter OUT your domain: keep where NOT id.startsWith("triage:")
3. TodoWrite() with filtered array
4. Log: "Cleaned up {count} triage tasks"
```
