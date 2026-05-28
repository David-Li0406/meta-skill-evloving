---
description: Work on improvements from all knowledge sources
---

# Improve - Work on Pending Items

ดึง actionable items จากทุก sources แล้วทำงาน (Layer 4)

## Instructions

1. **Scan** knowledge files (prioritized)
2. **Extract** actionable items
3. **Present** to user
4. **Execute** selected items
5. **Update** source files

## Scan Priority

| Priority | Source | Look For |
|----------|--------|----------|
| 1 | `docs/knowledge-base/` | "When to Apply", patterns to implement |
| 2 | `docs/retrospective/` | "Future Improvements" (`- [ ]`) |
| 3 | `docs/learnings/` | "Gotchas" to fix (skip "Distilled") |

## Scan Commands

```bash
# Knowledge base
find $PROJECT_ROOT/docs/knowledge-base -name "*.md" -type f

# Retrospectives
find $PROJECT_ROOT/docs/retrospective -name "*.md" -type f

# Learnings (skip distilled)
find $PROJECT_ROOT/docs/learnings -name "*.md" -type f
```

## Present Format

```markdown
## Pending Improvements

### From Knowledge Base - Priority 1

kafka-error-handling.md:
1. [ ] Apply retry pattern to all consumers

### From Retrospectives - Priority 2

retrospective_2025-12-23_143000.md:
2. [ ] Add consumer mocks to Makefile

### From Learnings - Priority 3

14.30_redis-issue.md:
3. [ ] Document Redis patterns
```

## User Selection

Ask: "เลือก item (หมายเลข, 'all', หรือ 'skip')"

## Execute Workflow

For each selected item:
1. วิเคราะห์ task
2. Implement
3. Test
4. Commit (atomic)
5. Update source:
   - `- [ ]` → `- [x]`
   - Add changelog entry

## Output Summary

```markdown
## Completed

- [x] Add consumer mocks (commit: abc1234)
- [ ] Redis patterns (skipped - needs discussion)

Updated:
- docs/retrospective/2025-12/retrospective_*.md
```

## Rules

| Rule | Description |
|------|-------------|
| **PRIORITIZE** | Knowledge base first |
| **ASK** | If needs discussion/approval |
| **UPDATE** | Source file after completion |
| **ATOMIC** | Use atomic commits |
