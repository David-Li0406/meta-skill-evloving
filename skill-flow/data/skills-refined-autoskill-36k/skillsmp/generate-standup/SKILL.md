---
name: generate-standup
description: Generate daily standup notes from memory. Use when user says "standup", "daily report", "what did I work on", "summarize my day", or needs work summary.
allowed-tools: mcp__aiii__recall_memories, mcp__aiii__list_spaces
---

# Generate Standup

Generate formatted daily standup notes from aiii memories.

## When to Use

- User asks for standup notes
- User wants a daily/weekly summary
- User needs to report what they worked on
- Morning routine to review previous day

## Instructions

1. **Determine the time period**:
   - "standup" → yesterday + today so far
   - "what did I do today" → today only
   - "weekly summary" → last 7 days
   - Specific date → that date

2. **Query Work space memories**:
   - Filter by Work space
   - Filter by time range
   - Include all relevant entries

3. **Also check cross-space activity** if relevant:
   - Learning space for skills acquired
   - Any space with today's entries

4. **Categorize into standup format**:

   **Done/Yesterday:**
   - Completed tasks
   - Merged PRs
   - Resolved issues

   **Today/Working On:**
   - In-progress items mentioned
   - Planned continuations
   - New tasks started

   **Blockers:**
   - Issues mentioned as blocking
   - Dependencies waiting on
   - Questions needing answers

5. **Format the output**:

```markdown
## Standup - January 8, 2026

### Done

- Fixed authentication bug in PR #234
- Reviewed rate limiting implementation
- Updated API documentation

### Working On

- Continuing API refactoring
- Writing tests for new endpoints

### Blockers

- None currently
```

6. **Offer customization**:
   - Different formats (bullet points, prose, etc.)
   - More/less detail
   - Different time ranges

## Example Interaction

**User:** "Generate my standup"

**Claude:**

1. Determines: yesterday + today
2. Queries Work space memories for those dates
3. Finds 4 memories from yesterday, 1 from today
4. Categorizes: 3 completed, 2 in-progress, 0 blockers
5. Formats and presents standup
6. Offers: "Want me to adjust the format or include more detail?"

## No Work Memories

If no Work memories found for the period:

1. State clearly that no work was recorded
2. Suggest the user may need to:
   - Enable session auto-capture
   - Manually save important work
3. Offer to search a different time range
