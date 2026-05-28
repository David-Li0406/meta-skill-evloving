---
name: memory-maintenance
description: Prune and consolidate state files, surface important items from journal to core state
---

# Memory Maintenance

Run this when state files are getting bloated or context feels cluttered. Can be triggered manually or as an ambient task.

## Size Limits

These are the target limits for state files:

| File             | Target    | Hard limit |
| ---------------- | --------- | ---------- |
| today.md         | ~30 lines | 50 lines   |
| inbox.md         | ~20 lines | 30 lines   |
| commitments.md   | ~40 lines | 60 lines   |
| ambient-tasks.md | ~30 lines | 40 lines   |

## Workflow

### 1. Check file sizes

Read each state file and count lines. Flag any over the target limit.

### 2. Prune today.md

- Remove completed items older than today
- Consolidate verbose notes into concise summaries
- Move reference information to project files

### 3. Process inbox.md

- Archive or action items older than 3 days
- Consolidate related items
- Delete anything that's no longer relevant

### 4. Clean commitments.md

- Archive completed commitments (move to a `state/archive/` file if needed)
- Merge related commitments
- Remove commitments that have been inactive for 2+ weeks without explicit decision to keep

### 5. Tidy ambient-tasks.md

- Move completed tasks to bottom "Completed" section
- Delete completed tasks older than 1 week
- Remove tasks that are no longer relevant

### 6. Check for duplication

Look for information duplicated across files:

- Same commitment in both today.md and commitments.md
- Project details scattered across multiple files
- Establish single source of truth

### 7. Verify project/people files

For files in `state/projects/` and `state/people/`:

- Remove any that are stale (not referenced in 2+ weeks)
- Consolidate if multiple files cover the same topic
- Ensure each has a clear purpose

### 8. Review topic files

For files in `state/topics/`:

- Check each is under ~20 lines (distilled, not exhaustive)
- Remove any that are stale or no longer relevant
- Look for topics that should be merged (overlapping concepts)
- Verify accuracy - flag anything that might be outdated

### 9. Review recent journal entries

Use `get_recent_journal` to fetch recent entries (last 40). Look for:

- **Conventions/preferences**: Things Matt said to remember (e.g., "repos go in ~/Repos", "always check lockfile")
- **Decisions**: Important choices that should be documented in project files
- **Commitments**: Promises made that should go in commitments.md
- **People context**: Info about people that should go in people files
- **Action items**: Tasks that got mentioned but not tracked

For each item found:

- If it's a convention: Add to AGENTS.md or a conventions file
- If it's a commitment: Add to commitments.md
- If it's project context: Add to the relevant project file
- If it's people context: Create or update a people file
- If it's a one-off task: Add to today.md or ambient-tasks.md
- If it's durable knowledge: Create or update a topic file

### 10. Commit

Stage and commit with message: "Memory maintenance: [date]"

## Output

Report:

**Files processed:**

- today.md: X lines -> Y lines
- inbox.md: X lines -> Y lines
- [etc.]

**Items archived/removed:**

- [List of significant removals]

**Issues found:**

- [Any duplication or staleness concerns]

**Surfaced from journal:**

- [Items moved from journal to state files]
