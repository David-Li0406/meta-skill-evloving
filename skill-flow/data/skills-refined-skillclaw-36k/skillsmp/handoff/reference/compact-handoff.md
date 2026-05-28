# Handoff for Context Compaction

When running `/compact`, include additional preservation notes.

## Template

```markdown
# Session Handoff — [Date]
## Context Compaction Note

This handoff was created during context compaction.

### Critical State to Preserve
- [Essential state item 1]
- [Essential state item 2]

### Must Remember
- [Critical fact the next session needs]
- [Decision that must persist]

### Safe to Forget
- [Exploration that didn't pan out]
- [Details superseded by later work]

[Then include standard handoff sections...]
```

## What to Preserve

**Always preserve:**
- User's original request and intent
- Key decisions made and rationale
- Current task status and blockers
- Files modified in this session
- Safety-relevant context

**Safe to omit:**
- Exploratory searches that led nowhere
- Intermediate reasoning steps
- Verbose tool outputs already acted upon
- Redundant context from early session

## Integration with /compact

When `/compact` runs, it will:
1. Trigger handoff with compaction note
2. Write to `.context/handoff.md`
3. Clear context
4. Resume from handoff

The compaction handoff is your lifeline — make it complete.
