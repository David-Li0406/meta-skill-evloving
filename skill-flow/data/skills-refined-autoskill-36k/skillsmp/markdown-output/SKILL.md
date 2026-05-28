---
name: markdown-output
description: Formatting and delivering GitHub-flavored markdown content. Use when producing markdown that will be posted to GitHub (issues, PRs, comments, discussions), when the user asks for content to copy/paste elsewhere, or when creating markdown files. Covers proper formatting for collapsible sections, code blocks, tables, alerts, and delivering content via clipboard when manual pasting is needed.
---

# Markdown Output

## Delivery Method

Determine how content reaches its destination before formatting:

1. **Agent posts directly**: Use `gh` CLI for GitHub (issues, PRs, comments) or write to local files. This is preferred when available.
2. **User pastes manually**: Copy to clipboard when the user needs to paste content elsewhere.

For clipboard delivery, use platform-specific commands with a quoted heredoc delimiter to preserve all formatting:

```bash
# macOS
cat << 'EOF' | pbcopy
content here
EOF

# Linux
cat << 'EOF' | xclip -selection clipboard
content here
EOF
```

The single quotes around `'EOF'` prevent shell expansion of special characters.

## Collapsible Sections

GitHub requires blank lines after `<details>` and `<summary>` tags for proper rendering.

Correct:

```markdown
<details>

<summary>Click to expand</summary>

Content inside the collapsible section.

</details>
```

Incorrect (will not render properly):

```markdown
<details>
<summary>Click to expand</summary>
Content inside the collapsible section.
</details>
```

## Code Blocks

Always specify a language hint for syntax highlighting: `sql`, `json`, `ruby`, `kusto`, `bash`, `python`, etc.

JSON code blocks must contain valid JSON with quoted keys and string values:

Correct:

```json
{"my_policy": "enabled", "count": 42}
```

Incorrect:

```json
{my_policy: enabled, count: 42}
```

## Tables

Tables require blank lines before and after them for proper rendering:

```markdown
Some text above.

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |

Some text below.
```

## Alerts

GitHub supports special alert callouts using blockquote syntax:

```markdown
> [!NOTE]
> Useful information that users should know.

> [!TIP]
> Helpful advice for doing things better.

> [!IMPORTANT]
> Key information users need to know.

> [!WARNING]
> Urgent info that needs immediate attention.

> [!CAUTION]
> Advises about risks or negative outcomes.
```
