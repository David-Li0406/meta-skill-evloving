---
name: slack-message-formatter
description: Use this skill when you need to format text for Slack messages, converting standard Markdown to Slack's mrkdwn syntax.
---

# Slack Message Formatter

Format content for Slack using their `mrkdwn` syntax (NOT standard Markdown).

## Quick Reference

### Slack mrkdwn Syntax

| Format          | Slack Syntax         | Example                     |
|-----------------|----------------------|-----------------------------|
| Bold            | `*text*`             | `*important*`              |
| Italic          | `_text_`             | `_emphasis_`               |
| Strikethrough   | `~text~`             | `~deleted~`                |
| Inline code     | `` `text` ``         | `` `code` ``               |
| Code block      | ` ``` ` (triple backticks) | See below               |
| Link            | `<URL|text>`         | `<https://example.com|Click here>` |
| Bullet list     | `• item` or `* item` | `• First item`             |
| Numbered list   | `1. item`            | `1. First item`            |
| Quote           | `> text`             | `> quoted text`            |
| User mention    | `<@USERID>`          | `<@U123ABC>`               |
| Channel         | `<#CHANNELID>`       | `<#C123ABC>`               |
| Emoji           | `:emoji_name:`       | `:rocket:`                 |

### What Slack Does NOT Support

- `**bold**` (use `*bold*` instead)
- `## Headers` (use `*Bold Text*` instead)
- Tables with `| |` syntax (not supported at all)
- Horizontal rules `---` (not rendered)
- Complex ASCII art (gets mangled)
- Syntax highlighting in code blocks
- Nested formatting
- Images via markdown

## Conversion Rules

When converting content for Slack:

1. **Headers**: Replace `## Header` with `*Header*` (bold)
2. **Bold**: Replace `**text**` with `*text*`
3. **Tables**: Convert to bullet lists or simple text
4. **Diagrams**: Simplify to basic ASCII in code blocks, or describe in text
5. **Links**: Convert `[text](url)` to `<url|text>`
6. **Lists**: Use `•` for bullets, `1.` for numbered

## Code Block Example

```
This is a code block in Slack.
No syntax highlighting available.
Keep it simple and readable.
```

## Workflow

When user asks to format for Slack:

1. **Convert** the content using rules above
2. **Simplify** any tables or complex diagrams
3. **Copy to clipboard** using `pbcopy` (macOS) or `xclip` (Linux)
4. **Confirm** with user that it's ready to paste

### Copy to Clipboard Command

```bash
# macOS
cat << 'EOF' | pbcopy
Your formatted content here
EOF

# Linux
cat << 'EOF' | xclip -selection clipboard
Your formatted content here
EOF
```

## Example Conversion

### Input (Standard Markdown)

```markdown
## Important Update

**Key changes:**
- Feature A added
- Bug B fixed

| Status | Count |
|--------|-------|
| Done   | 5    
```