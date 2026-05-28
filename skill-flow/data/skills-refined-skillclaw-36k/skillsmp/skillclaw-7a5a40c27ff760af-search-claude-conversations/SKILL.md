---
name: search-claude-conversations
description: Use this skill to search through Claude Code conversation history for specific topics, keywords, or timeframes when you need to find past discussions or continue previous work.
---

# Search Claude Conversations

**Purpose:** Efficiently search through Claude Code conversation history stored in the local database to retrieve relevant past interactions.

## Database Location

To find the database location, run:

```bash
vibe-check status
```

The default location is: `~/.vibe-check/vibe_check.db`

**Note:** If the status shows no PID, vibe-check is not running and the database may be stale. Start it with `vibe-check start`.

## Important: Use Read-Only Mode

To avoid database locks when the monitor is running, always use read-only mode:

```bash
sqlite3 "file:/path/to/vibe_check.db?mode=ro" "SELECT ..."
```

## Search Queries

### Search Messages by Content

```sql
SELECT
    event_session_id,
    event_type,
    SUBSTR(event_message, 1, 150) as message_preview,
    inserted_at,
    git_remote_url,
    file_name
FROM conversation_events
WHERE event_message LIKE '%{search_term}%'
    AND event_message IS NOT NULL
ORDER BY inserted_at DESC
LIMIT 20;
```

### Search by Repository

```sql
SELECT
    event_session_id,
    event_type,
    SUBSTR(event_message, 1, 150) as message_preview,
    inserted_at,
    file_name
FROM conversation_events
WHERE git_remote_url LIKE '%{repo_name}%'
ORDER BY inserted_at DESC
LIMIT 20;
```

### Search by Date Range

```sql
SELECT
    event_session_id,
    event_type,
    SUBSTR(event_message, 1, 150) as message_preview,
    inserted_at,
    git_remote_url
FROM conversation_events
WHERE DATE(inserted_at) BETWEEN '{start_date}' AND '{end_date}'
    AND event_message IS NOT NULL
ORDER BY inserted_at DESC
LIMIT 50;
```

### Search by Session ID

```sql
SELECT
    event_type,
    event_message,
    inserted_at,
    line_number
FROM conversation_events
WHERE event_session_id = '{session_id}'
ORDER BY line_number ASC;
```

### Find Sessions About a Topic

```sql
SELECT
    event_session_id,
    COUNT(*) as mentions,
    MIN(inserted_at) as first_mention,
    MAX(inserted_at) as last_mention,
    MAX(git_remote_url) as repository
FROM conversation_events
WHERE event_message LIKE '%{topic}%'
GROUP BY event_session_id
ORDER BY mentions DESC
LIMIT 10;
```

## Usage Flow

When a user requests a search:

1. **Extract search criteria** from the user's question:
   - Search term/keyword
   - Date range (if specified)
   - Repository name (if specified)

2. **Execute the appropriate SQL query** based on the extracted criteria.

3. **Return the results** in a user-friendly format, summarizing the findings and providing context where necessary.

## CLI Options

For command-line usage, you can utilize the following options:

- `--interactive`: Enter interactive mode with autocomplete.
- `--file <pattern>`: Filter by file path pattern.
- `--tool <name>`: Filter by tool used (e.g., Edit, Write).
- `--since <date>`: Specify a starting date for the search.
- `--until <date>`: Specify an ending date for the search.
- `--limit <n>`: Limit the number of results returned (default: 20).
- `--context <n>`: Show N messages before/after the match.

## Output Formats

Results can be formatted in various ways, including markdown summaries or raw JSON for programmatic use.