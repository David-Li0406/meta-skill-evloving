# Process Incoming Workflow

**Trigger:** "check incoming", "process captures", "what's in my inbox", "review captures"

## Purpose
Review and process content captured via Telegram and items in the Obsidian inbox.

## Workflow Steps

### 1. Check Capture Pipeline Status

```bash
# See pending Telegram messages
~/.claude/bin/ingest/ingest-wrapper status

# See recent messages with details
~/.claude/bin/ingest/ingest-wrapper status --recent

# Check for failures
~/.claude/bin/ingest/ingest-wrapper status --failed
```

### 2. Check Obsidian Inbox

```bash
# View unprocessed inbox items
~/.claude/bin/obs/obs-wrapper incoming
```

### 3. Present Summary

```markdown
## Incoming Items

### Telegram Captures
| Status | Count |
|--------|-------|
| Pending | 3 |
| Processing | 0 |
| Completed | 15 |
| Failed | 1 |

**Pending by type:**
- text: 1
- url: 1
- photo: 1

**Recent captures:**
1. [text] "Meeting notes from standup #meeting @alice"
2. [url] https://example.com/article #read-later
3. [photo] Screenshot (awaiting analysis)

### Obsidian Inbox
- 5 notes tagged #incoming
- Oldest: 3 days ago
- Newest: Today

**Items needing attention:**
1. "Quick thought about caching" - needs tagging
2. "Article: Kubernetes patterns" - needs summary
```

### 4. Process Options

Offer actions based on what's pending:

**For Telegram captures:**
```bash
# Process all pending
ingest process --verbose

# Process specific type
ingest process --type url
ingest process --type photo

# Retry failed
ingest retry && ingest process
```

**For Inbox notes:**
- Read and re-tag with appropriate project
- Summarize and archive
- Link to related notes

### 5. Execute Processing

If user wants to process:

```bash
# Process Telegram captures
~/.claude/bin/ingest/ingest-wrapper process --verbose
```

Report results:
- Notes created
- Any failures and why
- Suggestions for failed items

### 6. Post-Processing

After processing:
- Update embeddings if many new notes: `obs embed`
- Suggest reviewing new notes
- Offer to help organize/tag items

## Failure Handling

If captures failed:

```bash
# See failed messages
ingest status --failed

# Common issues:
# - API key missing → Check ~/.claude/.env
# - Network error → Retry later
# - Unsupported format → Manual processing needed
```

For each failure, suggest:
- Retry if transient error
- Manual intervention if format issue
- Skip if content is invalid
