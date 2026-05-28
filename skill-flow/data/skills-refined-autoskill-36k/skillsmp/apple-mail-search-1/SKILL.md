---
name: apple-mail-search
description: Fast & safe Apple Mail search with body content support.
homepage: https://clawdhub.com/mneves75/apple-mail-search
repository: https://github.com/gumadeiras/apple-mail-search-cli
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["mail-search"]}}}
---

# Apple Mail (Fast & Safe)

Fast SQLite search for Apple Mail.app emails with body content support.

**✨ Highlights:**
- **Safe DB access:** Copies database to temp file before querying — won't corrupt if Mail.app is running
- **Body content support:** Read full email bodies via AppleScript (slow for thousands, but instant for a few)
- **~50ms queries:** SQLite vs 8+ minutes with pure AppleScript
- **Note:** This tool searches/reads Apple Mail.app only. Use `himalaya` skill to send emails.

## Installation (optional)

**symlink script (recommended)**
```bash
# Symlink the script to make it available globally
sudo ln -sf ./scripts/mail-search /usr/local/bin/mail-search
# Pull updates with: clawdhub update
```

## Usage

```bash
mail-search subject "invoice"          # Search subjects
mail-search sender "@amazon.com"       # Search by sender email
mail-search from-name "John"           # Search by sender name
mail-search to "recipient@example.com" # Search sent mail
mail-search unread                     # List unread emails
mail-search attachments                # List emails with attachments
mail-search attachment-type pdf        # Find PDFs
mail-search recent 7                   # Last 7 days
mail-search date-range 2025-01-01 2025-01-31
mail-search open 12345                 # Open email in Mail.app
mail-search body 12345                 # Read full email body (AppleScript)
mail-search stats                      # Database statistics
```

## Options

```
-n, --limit N     Max results (default: 20)
-j, --json        Output as JSON
-c, --csv         Output as CSV
-q, --quiet       No headers
--db PATH         Override database path
```

## Examples

```bash
# Find bank statements from last month
mail-search subject "statement" -n 50

# Get unread emails as JSON for processing
mail-search unread --json | jq '.[] | .subject'

# Find all PDFs from a specific sender
mail-search sender "@bankofamerica.com" -n 100 | grep -i statement

# Export recent emails to CSV
mail-search recent 30 --csv > recent_emails.csv
```

## Why This Exists

| Method | Time for 130k emails |
|--------|---------------------|
| AppleScript iteration | 8+ minutes |
| Spotlight/mdfind | **Broken since Big Sur** |
| SQLite (this tool) | ~50ms |

Apple removed the emlx Spotlight importer in macOS Big Sur. This tool queries the `Envelope Index` SQLite database directly.

## Technical Details

**Database:** `~/Library/Mail/V{9,10,11}/MailData/Envelope Index`

**Key tables:**
- `messages` - Email metadata (dates, flags, FKs)
- `subjects` - Subject lines
- `addresses` - Email addresses and display names
- `recipients` - TO/CC mappings
- `attachments` - Attachment filenames

**Limitations:**
- **Apple Mail.app only** — this tool queries Mail.app's local database
- **Read-only for Mail.app** — can search/read but cannot compose/send
- **To send emails:** Use the separate `himalaya` skill (IMAP/SMTP)
- SQLite queries: metadata only (subjects, senders, dates)
- Body content: AppleScript (fast for a few emails, slow for thousands)

## Reading Email Bodies

For full email body content, use the `body` command:

```bash
mail-search body 94695                 # Read single email by ID
```

This uses AppleScript to fetch the full content from Mail.app. It's:
- **Fast** for 1-10 emails (~100ms each)
- **Slow** for hundreds/thousands (use sparingly)

The SQLite database only stores metadata; actual body content lives in Mail.app's internal cache.

## Advanced: Raw SQL

For custom queries, use sqlite3 directly:

```bash
sqlite3 -header -column ~/Library/Mail/V10/MailData/Envelope\ Index "
SELECT m.ROWID, s.subject, a.address 
FROM messages m 
JOIN subjects s ON m.subject = s.ROWID 
LEFT JOIN addresses a ON m.sender = a.ROWID 
WHERE s.subject LIKE '%your query%' 
ORDER BY m.date_sent DESC 
LIMIT 20;
"
```

## License

MIT
