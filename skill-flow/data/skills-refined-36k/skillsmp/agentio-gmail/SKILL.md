---
name: agentio-gmail
description: Use when interacting with Gmail - list, read, search, send (with attachments/inline images), reply, archive, mark, download attachments, or export to PDF. Requires agentio CLI with a configured Gmail profile.
---

# Gmail Operations with agentio

Use `agentio gmail` commands to interact with Gmail. Multiple profiles can be configured - the default profile is used unless you specify `--profile <name>`.

## List Messages

```bash
agentio gmail list [--limit N] [--query QUERY] [--label LABEL]
```

Options:
- `--limit <n>`: Number of messages (default: 10)
- `--query <query>`: Gmail search query
- `--label <label>`: Filter by label (repeatable)

## Get a Message

```bash
agentio gmail get <message-id> [--format text|html|raw] [--body-only]
```

Options:
- `--format`: Body format - `text` (default), `html`, or `raw`
- `--body-only`: Output only the message body

## Search Messages

```bash
agentio gmail search --query <query> [--limit N]
```

Query syntax:
- `from:john@example.com` - From specific sender
- `to:me` - Sent to you
- `after:2024/01/01` / `before:2024/12/31` - Date filters
- `newer_than:7d` / `older_than:1m` - Relative dates (d/m/y)
- `label:inbox` - In specific label
- `is:unread` / `is:starred` - Status filters
- `has:attachment` - With attachments
- `subject:invoice` - Search subject

Combine: `from:boss@work.com is:unread newer_than:7d`

## Send an Email

```bash
agentio gmail send --to <email> --subject <subject> [--body <body>] [options]
```

Options:
- `--to <email>`: Recipient (repeatable)
- `--cc <email>`: CC recipient (repeatable)
- `--bcc <email>`: BCC recipient (repeatable)
- `--subject <subject>`: Email subject
- `--body <body>`: Email body (or pipe via stdin)
- `--html`: Treat body as HTML
- `--attachment <path>`: File to attach (repeatable)
- `--inline <cid:path>`: Inline image (repeatable). Supports PNG, JPG, GIF only (not SVG)

### Inline Images

To embed images directly in HTML emails, use `--inline` with a content ID and file path:

```bash
agentio gmail send \
  --to user@example.com \
  --subject "Report" \
  --html \
  --body '<p>See chart:</p><img src="cid:chart1">' \
  --inline chart1:./chart.png
```

Reference inline images in HTML using `src="cid:<contentId>"`.

## Reply to a Thread

```bash
agentio gmail reply --thread-id <id> [--body <body>] [--html]
```

## Archive a Message

```bash
agentio gmail archive <message-id>
```

## Mark as Read/Unread

```bash
agentio gmail mark <message-id> --read
agentio gmail mark <message-id> --unread
```

## Download Attachments

```bash
agentio gmail attachment <message-id> [--name <filename>] [--output <dir>]
```

Options:
- `--name <filename>`: Download specific attachment by filename (downloads all if not specified)
- `--output <dir>`: Output directory (default: current directory)

## Export Message as PDF

```bash
agentio gmail export <message-id> [--output <path>]
```

Options:
- `--output <path>`: Output file path (default: `message.pdf`)

Requires Chrome, Chromium, or Edge browser installed.
