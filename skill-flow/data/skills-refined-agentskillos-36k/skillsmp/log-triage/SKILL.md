---
name: log-triage
description: Process daily note log entries into structured inbox notes. Handles voice memos (🎤), URLs (YouTube, Twitter/X, GitHub, articles), and text entries. Use when triaging daily logs, converting voice memos, or processing saved URLs.
allowed-tools: Read, Edit, mcp__plugin_para-obsidian_para-obsidian__para_read, mcp__plugin_para-obsidian_para-obsidian__para_list, mcp__plugin_para-obsidian_para-obsidian__para_create, mcp__plugin_para-obsidian_para-obsidian__para_insert, mcp__plugin_para-obsidian_para-obsidian__para_frontmatter_set, mcp__plugin_para-obsidian_para-obsidian__para_config, mcp__plugin_para-obsidian_para-obsidian__para_template_fields, mcp__firecrawl__firecrawl_scrape, mcp__youtube-transcript__get_video_info, mcp__youtube-transcript__get_transcript, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__evaluate_script, WebFetch
---

# Log Triage

Process daily note log entries into structured inbox notes.

## Critical Rules

1. **Always confirm** before creating notes
2. **Preserve raw transcriptions** in voice memos (never truncate)
3. **Mark processed entries** with `✅ <time> - Processed → [[Note Title]]`
4. Create notes in `00 Inbox/`

## Entry Detection & Handler Routing

When you encounter a log entry, detect type and load the appropriate handler:

| Pattern | Type | Handler |
|---------|------|---------|
| `- [time] - 🎤 [long text]` | Voice memo (>200 words) | [meeting-memo.md](handlers/meeting-memo.md) |
| `- [time] - 🎤 [short text]` | Short voice memo | [text-entry.md](handlers/text-entry.md) |
| `youtube.com` or `youtu.be` | YouTube video | [youtube.md](handlers/youtube.md) |
| `x.com` or `twitter.com` | Twitter/X post | [twitter.md](handlers/twitter.md) |
| Other URLs | Generic URL | [url-generic.md](handlers/url-generic.md) |
| Plain text | Text entry | [text-entry.md](handlers/text-entry.md) |

**Load the handler ONLY when you encounter that entry type.** This keeps context minimal.

## Session Flow

```
1. Read daily note → Find ## Log section
2. Parse entries → Detect types
3. Show triage plan → Get user confirmation
4. For each entry:
   → Load appropriate handler
   → Extract/fetch content
   → Create note
   → Mark entry as processed
5. Summary → What was created
```

## Step 1: Find Daily Note

```
para_read({ file: "000 Timestamps/Daily Notes/YYYY-MM-DD.md" })
```

If no date specified, find most recent note with log entries.

## Step 2: Parse Log Section

Find `## Log` heading. Parse entries matching:
```
- [time] - [content]
```

Skip entries already marked with ✅.

## Step 3: Show Triage Plan

Before processing, show what each entry will become:

```
Found 3 log entries:

1. 🎤 9:26am (~2000 words) → Meeting note
2. 🎤 12:04pm (45 words) → Capture note
3. URL 1:33pm (x.com) → Tweet clipping

Proceed? [y/n]
```

## Step 4: Process Each Entry

Load the appropriate handler and follow its instructions for:
- Content extraction
- Note creation
- Frontmatter population

## Step 5: Mark as Processed

After creating the note, replace the log entry:

```
Before: - 6:21 pm - https://youtube.com/watch?v=abc123
After:  - 6:21 pm - ✅ Processed → [[✂️🎬 Channel - Video Title]]
```

Use the Edit tool on the daily note directly.

## Templates Reference

Use `para_config` to get vault and templates path.
Use `para_template_fields` to inspect required fields.

**Primary:** `meeting`, `capture`
**Clippings:** In `Templates/Clippings/` - matched by URL domain
