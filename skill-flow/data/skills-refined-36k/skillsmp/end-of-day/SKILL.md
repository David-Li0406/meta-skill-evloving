---
name: end-of-day
description: Daily review workflow - process completed work, roll over unfinished items, prepare for tomorrow
---

# End of Day Review

Run this at the end of each work day to close out the session cleanly and prepare for tomorrow.

## Workflow

### 1. Process today.md

Read `state/today.md` and for each item:

- **Completed items**: Move to a "Completed" section or remove if trivial
- **Partially done**: Add context about current state, move to tomorrow's priorities
- **Not started**: Evaluate if still relevant. Move to `commitments.md` if important, delete if stale

### 2. Check inbox.md

Read `state/inbox.md` and process each item:

- If actionable and quick: do it now
- If actionable and not quick: add to `commitments.md` with context
- If reference material: move to relevant project file or delete
- If stale: delete

Goal: inbox should be empty or near-empty at end of day.

### 3. Update commitments.md

Review active commitments:

- Add any new commitments that emerged today
- Update progress notes on existing items
- Flag anything that's been stuck for more than a week

### 4. Prepare tomorrow's today.md

Reset `state/today.md` with:

```markdown
# Today – [Day, Date]

## Priorities

- [ ] [Most important thing from commitments]
- [ ] [Second priority]
- [ ] [Third priority]

## Open threads

- [Anything in progress that needs continuation]
```

### 5. Update topics (working knowledge)

Review today's journal entries and conversations for new learnings:

- **New terms**: Internal Cloudflare terminology, project names, concepts encountered
- **Updated understanding**: Corrections to existing knowledge
- **Technical insights**: Patterns, gotchas, how things work

For each:

- If new concept: create `state/topics/[name].md` (~20 lines max)
- If existing topic needs update: revise the topic file (replace outdated info, don't append)
- Use wiki to fill gaps on internal terminology

Keep topics small and current - distilled understanding, not exhaustive notes.

### 6. Write summary

Log a journal entry summarizing:

- What got done
- What's carrying over
- Any blockers or concerns
- Topics created or updated

### 7. Commit

Stage and commit all state file changes with message: "End of day: [date]"

## Output

After completing the workflow, provide a brief summary:

- Tasks completed today
- Items rolled to tomorrow
- Topics created/updated
- Any concerns flagged
