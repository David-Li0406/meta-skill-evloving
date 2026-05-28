---
name: go-loop
description: |
  This skill should be used when the user asks to "implement stories", "work on PRD",
  "autonomous coding", "overnight run", "implement features while I sleep", "AFK mode",
  "hands-off development", "run unattended", "how does /go work", "batch development",
  "iterate on stories", or discusses HITL vs AFK approaches. Covers the go loop
  execution modes (HITL vs AFK), when to use each, and progression from cautious
  to confident autonomous development.
version: 1.0.0
---

# Go Loop - Iterative Task Execution

**Current branch:** !`git branch --show-current 2>/dev/null || echo "not in git repo"`

The go loop executes PRD stories or generic tasks iteratively, with two distinct modes
for different levels of autonomy and oversight.

## When to Use Go Loop

- Implementing stories from a PRD (`/go plans/feature/prd.json`)
- Generic iterative tasks (`/go "Build CSV parser" --completion-promise "DONE"`)
- Autonomous overnight development (AFK mode)
- Learning/debugging new workflows (HITL mode with `--once`)

## State Management

**Single Source of Truth**: prd.json IS the state. The hook derives the current story as the
first story with `passes: false` (sorted by priority). Progress log is embedded in prd.json's
`log` array - no separate progress.txt file.

**What Claude Updates:**
- `passes: true` when story completes
- `completed_at` and `commit` fields (optional - hook can set)

**What Hook Updates:**
- Appends to prd.json's `log` array automatically

## Execution Modes

### HITL (Human-In-The-Loop)

Default mode. Hook-based continuation within a single Claude session.

**Characteristics:**
- Single Claude session throughout
- Stop hook blocks exit, injects next prompt
- Context accumulates (can cause "context rot" in long sessions)
- Best for: Learning, debugging, risky tasks, complex decisions

**Usage:**
```bash
/go plans/auth/prd.json              # Full HITL loop
/go plans/auth/prd.json --once       # Single iteration, then stop
```

### AFK (Away From Keyboard)

External bash loop. Each iteration is a fresh Claude session.

**Characteristics:**
- External bash for-loop controls iteration
- Fresh context per iteration (prevents context rot)
- State persists in prd.json only (single source of truth)
- Best for: Bulk work, overnight runs, well-defined tasks

**Usage:**
```bash
/go plans/auth/prd.json --afk                # External loop, 50 iterations
/go plans/auth/prd.json --afk --max 30       # Limit to 30 iterations
/go plans/auth/prd.json --afk --stream       # Real-time output visibility
```

## Mode Decision Tree

```
Is this a learning/debugging session?
├─ YES → Use HITL (--once for single iterations)
└─ NO → Do you trust the PRD and want hands-off execution?
        ├─ YES → Use AFK (--afk)
        └─ NO → Use HITL until confident
```

## Progression Path

Recommended approach when starting with a new PRD:

1. **Start with `--once`** - Run single iterations, review each output
2. **Graduate to HITL** - Let the hook continue automatically when comfortable
3. **Go AFK** - Use `--afk` for overnight runs once workflow is proven

## Quality Expectations

Both modes enforce the same quality standards:

- **Production code only** - No shortcuts, no "good enough for now"
- **Pre-commit reviews required** - code-simplifier + kieran reviewer in parallel
- **Atomic commits** - Each story = one commit with story reference

## Completion Signals

### PRD Mode
- All stories have `passes: true` in prd.json
- `<promise>ALL STORIES COMPLETE</promise>` marker

### Generic Mode
- `<promise>COMPLETION_TEXT</promise>` with exact promise text

## Command Reference

Run `/go --help` for full options or use these common patterns:

```bash
# PRD mode
/go plans/feature/prd.json

# PRD mode with iteration limit
/go plans/feature/prd.json --max-iterations 20

# Generic mode
/go "Build X" --completion-promise "X COMPLETE"

# AFK mode (external loop)
/go plans/feature/prd.json --afk --stream
```

## Task Integration (Optional)

For visibility via Ctrl+T and cross-session resume, sync PRD stories to Claude's Task system.

### On Loop Start (after reading prd.json)

1. Call `TaskList()` to check for existing tasks
2. If no tasks with `metadata.prd_path` matching this PRD:
   ```
   For each story where passes == false:
     TaskCreate({
       subject: "Story {id}: {title}",
       description: "Steps:\n- {step1}\n- {step2}...",
       activeForm: "Implementing story {id}",
       metadata: { loop: "go", prd_path: "{path}", story_id: {id} }
     })
   ```
3. Set `blockedBy` based on priority (story 2 blocked by story 1, etc.)
4. **Update state file** with task mappings:
   ```bash
   # Edit .claude/go-loop-{session}.local.md frontmatter:
   story_tasks: '{"1": "task-id-1", "2": "task-id-2"}'
   ```
5. Output `<tasks_synced/>` to signal completion

### During Work

- On story start: `TaskUpdate(task_id, status: "in_progress")`
- On story complete: `TaskUpdate(task_id, status: "completed")`

The hook will include the task_id in prompts once `story_tasks` is populated.

### Cross-Session Resume

After `/clear`, say "check tasks" or "what tasks are pending":
1. `TaskList()` returns pending tasks with metadata
2. Read `metadata.prd_path` to find the PRD file
3. Resume work on first pending story

## Additional Resources

### Reference Files

For detailed mode documentation:
- **`references/hitl-mode.md`** - Hook-based HITL details
- **`references/afk-mode.md`** - Ralph-style AFK loop details
