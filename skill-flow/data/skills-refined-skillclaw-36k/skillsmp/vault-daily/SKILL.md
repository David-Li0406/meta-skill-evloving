---
name: vault-daily
description: >
  Use when user wants to record or review their day.
  Triggered when intention involves daily planning, logging, or reflection.
  Creates or opens today's daily note.
---

# Vault Daily

## Behavior

1. Determine today's date in YYYY-MM-DD format
2. Check if today's note exists: `06_Daily/daily/YYYY-MM-DD.md`
3. If not exists: create using template from `${CLAUDE_PLUGIN_ROOT}/templates/tpl-daily.md`
4. If exists: read and offer to add content or review

## Frontmatter

```yaml
---
type: daily
date: {YYYY-MM-DD}
mood:
energy:
tags: []
---
```

## Template Structure

```markdown
# {date} ({weekday})

## Morning Intention
What's the one thing that matters today?

## Log
-

## Wins
-

## Learnings
-

## Tomorrow
-
```

## Interaction Prompts

When creating new daily note:
- "What's your main focus for today?"
- "How are you feeling? (mood 1-5)"
- "Energy level? (1-5)"

When opening existing note:
- "Want to add to your log?"
- "Any wins to record?"
- "Anything you learned today?"

## Date Handling

- Use local timezone
- Weekday in user's language preference
- Support "yesterday" or "tomorrow" requests
