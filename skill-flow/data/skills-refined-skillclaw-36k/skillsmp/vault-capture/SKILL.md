---
name: vault-capture
description: >
  Use when user intends to quickly save thoughts, ideas, or information.
  Triggered when someone wants to preserve something for later review or processing.
  Creates a fleeting note in 00_Inbox.
---

# Vault Capture

## Behavior

1. Create new note in `00_Inbox/`
2. Filename: `YYYY-MM-DD-{slug}.md` (slug from content, max 5 words, kebab-case)
3. Apply template structure from `${CLAUDE_PLUGIN_ROOT}/templates/tpl-fleeting.md`
4. Fill in content from user input

## Frontmatter

```yaml
---
type: fleeting
created: {today's date YYYY-MM-DD}
source: capture
tags: []
---
```

## Template Reference

Use the fleeting template structure:
- Title from first meaningful phrase
- Content as provided by user
- Footer with capture timestamp

## After Capture

- Confirm creation with filename
- Show brief preview of captured content
- Optionally ask if they want to add tags or process immediately

## Examples

User: "Remember this: AI agents work best with clear goals"
→ Creates `00_Inbox/2024-01-15-ai-agents-clear-goals.md`

User: "Quick thought about the marketing campaign"
→ Creates `00_Inbox/2024-01-15-marketing-campaign-thought.md`
