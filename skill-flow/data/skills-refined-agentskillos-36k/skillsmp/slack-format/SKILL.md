---
name: slack-format
description: "Format messages for Slack using mrkdwn syntax. Use when: (1) Writing or drafting a Slack message, (2) Converting markdown to Slack format, (3) User asks to 'format for Slack' or 'Slack message', (4) Copying text to clipboard for Slack."
---

# Slack mrkdwn Format

Slack uses "mrkdwn" - NOT standard markdown. Only differences listed below.

## Key Differences

| Element | Slack mrkdwn | NOT this |
|---------|--------------|----------|
| Bold | `*text*` | `**text**` |
| Italic | `_text_` | `*text*` |
| Strike | `~text~` | `~~text~~` |
| Link | `<url\|text>` | `[text](url)` |

## Not Supported

- Headers (`#`, `##`, etc.) - use *bold* instead
- Nested lists
- Tables
- Images (use file uploads)

## Mentions

```
<@U012AB3CD>        User (by ID)
<#C123ABC456>       Channel (by ID)
<!here>             @here
<!channel>          @channel
```

## Escaping

Escape `&`, `<`, `>` in user content as `&amp;` `&lt;` `&gt;`

## Output

Write to clipboard: `cat /tmp/slack-msg.md | pbcopy`
