# TodoWrite Patterns for Triage

## Overview

The triage skill uses **native TodoWrite** for task tracking. Since TodoWrite doesn't have a built-in `blockedBy` field, we encode dependencies in the task content.

## Dependency Encoding

```
[DEPS:none]           → No dependencies, can start immediately
[DEPS:id1,id2,id3]    → Blocked until all listed IDs are completed
```

## Task ID Format

Use hierarchical IDs with domain prefix:

```
{domain}:{scope}:{identifier}

triage:batch-1:item-1    → Batch 1, item 1
triage:batch-1:item-2    → Batch 1, item 2
triage:batch-1:review    → Batch 1 review phase
triage:batch-2:item-1    → Batch 2, item 1
triage:cleanup           → Final cleanup task
```

## Parsing Dependencies

Before starting any task:

1. Parse the `[DEPS:...]` prefix from task content
2. Extract dependency IDs (split by comma)
3. Check each dependency's status via TodoRead
4. Only proceed if ALL dependencies are `completed`

**Example:**
```
Task: triage:batch-1:review
Content: "[DEPS:triage:batch-1:item-1,triage:batch-1:item-2,triage:batch-1:item-3] Review batch 1"

Check: Are item-1, item-2, item-3 all completed?
- If yes → can start review
- If no → still blocked, wait or process other unblocked tasks
```

## Full Task Graph Example

```typescript
TodoWrite({
  todos: [
    // Batch 1 - parallel (no deps on each other)
    { id: "triage:batch-1:item-1", content: "[DEPS:none] Distill: ✂️ Article 1", status: "pending", priority: "medium" },
    { id: "triage:batch-1:item-2", content: "[DEPS:none] Distill: ✂️ Article 2", status: "pending", priority: "medium" },
    { id: "triage:batch-1:item-3", content: "[DEPS:none] Distill: 🎤 Voice memo", status: "pending", priority: "medium" },

    // Batch 1 review - blocked until all items done
    { id: "triage:batch-1:review", content: "[DEPS:triage:batch-1:item-1,triage:batch-1:item-2,triage:batch-1:item-3] Review batch 1 proposals", status: "pending", priority: "high" },

    // Batch 2 - blocked until batch 1 review done
    { id: "triage:batch-2:item-1", content: "[DEPS:triage:batch-1:review] Distill: ✂️ Article 3", status: "pending", priority: "medium" },
    { id: "triage:batch-2:item-2", content: "[DEPS:triage:batch-1:review] Distill: ✂️ Article 4", status: "pending", priority: "medium" },
    { id: "triage:batch-2:item-3", content: "[DEPS:triage:batch-1:review] Distill: 📎 Invoice PDF", status: "pending", priority: "medium" },

    // Batch 2 review
    { id: "triage:batch-2:review", content: "[DEPS:triage:batch-2:item-1,triage:batch-2:item-2,triage:batch-2:item-3] Review batch 2 proposals", status: "pending", priority: "high" },

    // Final cleanup
    { id: "triage:cleanup", content: "[DEPS:triage:batch-2:review] Cleanup triage session", status: "pending", priority: "low" }
  ]
})
```

## Finding Unblocked Tasks

```typescript
TodoRead() → filter triage:* tasks → find where:
  - status === "pending"
  - [DEPS:...] dependencies are all "completed" (or DEPS:none)
```

## Task State Transitions

```
pending → in_progress → completed
```

1. **Mark in_progress** before starting work
2. **Mark completed** after work finishes
3. Check if any blocked tasks become unblocked

## Resume Capability

On session start:

```typescript
TodoRead()
```

Filter for tasks where `id.startsWith("triage:")`.

If triage tasks exist with `status === "pending"` or `status === "in_progress"`:

```
Found existing triage session:
• 3 completed
• 2 pending
• 1 in progress

Resume from where you left off? (y/n)
```

## Cleanup

When all reviews complete, remove triage tasks:

```typescript
TodoRead() → filter OUT all triage:* tasks → TodoWrite(remaining)
```

## Quick Reference

| Pattern | Meaning |
|---------|---------|
| `[DEPS:none]` | No dependencies |
| `[DEPS:id1,id2]` | Blocked by id1 AND id2 |
| `triage:batch-N:item-N` | Analysis task |
| `triage:batch-N:review` | Review phase |
| `triage:cleanup` | Final cleanup |
