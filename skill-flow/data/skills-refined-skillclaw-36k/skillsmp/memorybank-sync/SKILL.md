---
name: memorybank-sync
description: Fast synchronization of activeContext.md and progress.md only. Lightweight alternative to full update for quick post-task documentation. NEW skill unique to memory-bank.
---

# Memory Bank: Sync

Fast sync of activeContext.md and progress.md after task completion.

**Helper Scripts Available:**
- `scripts/sync_active.py` - Fast update tool
- `scripts/extract_todos.py` - Get next steps

## What It Does

Lightweight update that ONLY touches:
- **activeContext.md** - Update focus, blockers, learnings
- **progress.md** - Move completed items

**Does NOT touch:** projectbrief, productContext, techContext, systemPatterns

## When to Use

- ✅ After completing individual tasks
- ✅ Quick documentation before ending session
- ✅ Minor progress updates
- ❌ NOT for architecture changes (use `/memorybank update`)

## Workflow

### 1. Gather Information

What changed:
- Completed tasks?
- New focus area?
- Learnings/insights?
- Blockers encountered?

### 2. Run Sync Tool

```bash
# Prepare JSON input
python scripts/sync_active.py /path/to/project '{
  "completed": ["Task that was finished"],
  "new_focus": "What working on now",
  "learnings": ["New pattern discovered"],
  "blockers": ["Issue encountered"]
}'
```

Or extract from conversation:
```bash
python scripts/extract_todos.py /path/to/project
# Use output to populate sync input
```

### 3. Verify Updates

Tool returns what changed:
```json
{
  "updated": {
    "activeContext.md": true,
    "progress.md": true
  },
  "changes": {
    "activeContext": {
      "updated_focus": true,
      "added_blockers": 1,
      "added_learnings": 1
    },
    "progress": {
      "moved_to_completed": 1
    }
  }
}
```

## Performance

- **Speed:** ~2 seconds (vs 5+ for full update)
- **Scope:** 2 files only
- **Use Case:** Frequent updates after tasks

## Example Usage

```bash
# After completing authentication feature
/memorybank sync

# Claude runs:
python scripts/sync_active.py /path/to/project '{
  "completed": ["Implemented user authentication API"],
  "new_focus": "Adding password reset flow",
  "learnings": ["JWT tokens work well with our session management"]
}'

# Result:
# ✓ activeContext.md updated with new focus
# ✓ progress.md updated with completed task
```

## Comparison

| Operation | Files Updated | Time | When to Use |
|-----------|---------------|------|-------------|
| **sync** | 2 (active + progress) | ~2s | After each task |
| **update** | All 6 files | ~5s | Major changes |

See `scripts/README.md` for complete documentation.
