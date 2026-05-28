---
name: vault-weekly
description: >
  Use when user wants to review or reflect on their week.
  Triggered when intention involves weekly planning, retrospective, or summary.
  Creates weekly review note and references daily notes.
---

# Vault Weekly

## Behavior

1. Determine current ISO week number (YYYY-Www)
2. Calculate week date range (Monday to Sunday)
3. Create note: `06_Daily/weekly/YYYY-Www-review.md`
4. Scan past 7 days of daily notes in `06_Daily/daily/`
5. Pre-populate review with highlights extracted from dailies

## Frontmatter

```yaml
---
type: weekly
week: {YYYY-Www}
date_start: {Monday YYYY-MM-DD}
date_end: {Sunday YYYY-MM-DD}
tags: []
---
```

## Template Structure

```markdown
# Week {week} Review ({start} ~ {end})

## Highlights
What went well this week?

## Challenges
What was difficult?

## Learnings
What did I learn?

## Projects Progress
| Project | Status | Notes |
|---------|--------|-------|
| | | |

## Next Week
What are the priorities?

## Gratitude
What am I thankful for?
```

## Data Extraction from Dailies

Scan daily notes for:
- **Wins** sections → populate Highlights
- **Learnings** sections → populate Learnings
- **Log** entries → summarize activity
- **mood/energy** averages → note trends

## Review Prompts

- "What were the wins this week?"
- "What was challenging?"
- "What did you learn?"
- "Priorities for next week?"
