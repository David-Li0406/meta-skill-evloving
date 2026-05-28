---
name: slacker
description: Interact with Slack (reminders, DMs, activity, saved messages)
---

# Slack CLI (slacker) Skill

Quick reference for using `slacker` CLI tool to interact with Slack programmatically.

**Repository:** https://github.com/shanemcd/slacker

## Quick Start

The easiest way to use `slacker` is with `uvx` - no installation or repository cloning required:

```bash
# List reminders and saved messages
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminders

# Create a reminder
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminder "me to call mom tomorrow at 9am"

# List today's DMs
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms

# View activity feed (mentions, threads, reactions)
uvx --from "git+https://github.com/shanemcd/slacker" slacker activity

# Check authentication
uvx --from "git+https://github.com/shanemcd/slacker" slacker whoami
```

**Tip**: Add an alias to your shell for convenience:
```bash
alias slacker='uvx --from "git+https://github.com/shanemcd/slacker" slacker'

# Then use it simply:
slacker reminders
slacker reminder "me to review PR in 30 minutes"
```

## Overview

`slacker` extracts Slack authentication credentials from your browser session, enabling programmatic access to Slack APIs without creating a bot or app.

## When to Use This Skill

Use this skill when:
- User asks to create a Slack reminder
- User wants to check their reminders or saved messages
- User asks about recent DMs or Slack activity
- User mentions Slack mentions, threads, or reactions
- User wants to search Slack messages
- User asks about their Slack notes or saved items

## Authentication

### First-Time Setup

```bash
# Extract credentials from your browser session
uvx --from "git+https://github.com/shanemcd/slacker" slacker login https://redhat.enterprise.slack.com

# Test authentication
uvx --from "git+https://github.com/shanemcd/slacker" slacker whoami
```

Credentials are stored at `~/.config/slacker/credentials` with `0600` permissions (read-only by owner).

## Common Commands

### Create Reminders

Create reminders using natural language - works exactly like typing `/remind` in Slack:

```bash
# Standard format: "me to [task] [when]"
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminder "me to call mom tomorrow at 9am"
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminder "me to review PR in 30 minutes"
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminder "me to check status next Monday"

# Can omit "me to" - Slack will figure it out
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminder "call mom tomorrow"
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminder "team sync prep Monday at 2pm"

# Recurring reminders
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminder "me to do weekly planning every Monday at 9am"
```

**Natural language parsing by Slack:**
Slack automatically parses the text to extract the task and timing. Supported formats:
- Relative: "in 30 minutes", "in 2 hours", "in 3 days"
- Absolute: "tomorrow", "next Monday", "Friday at 3pm"
- Combined: "tomorrow at 9am", "next week on Tuesday"
- Recurring: "every weekday", "every Monday at 9am"

### List Reminders and Saved Items

```bash
# List all saved items (reminders + saved messages)
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminders

# List only reminders (exclude saved messages)
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminders --reminders-only

# Limit results
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminders --limit 10

# JSON output for programmatic processing
uvx --from "git+https://github.com/shanemcd/slacker" slacker --output json reminders
```

**Text output includes:**
- Reminder text and due date
- Saved message preview (100 chars) with full message text
- Channel names and message links
- Status (in_progress, completed)
- Summary counts (total, uncompleted, overdue, completed)

**JSON output includes:**
- Full message text (not truncated!)
- All metadata (timestamps, channel IDs, states)
- Structured data for easy parsing with `jq`

### List DMs

View direct messages and group DMs with Slack usernames:

```bash
# List today's DM activity (default)
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms

# List DMs since a specific time (natural language)
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms --since "yesterday"
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms --since "2 days ago"
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms --since "last Monday"
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms --since "3 hours ago"

# JSON output for programmatic processing
uvx --from "git+https://github.com/shanemcd/slacker" slacker --output json dms --since "yesterday"
```

**Text output shows:**
- Individual DMs with direction (incoming/outgoing)
- Group DMs with participant activity
- Slack usernames (handles) for each person
- Message timestamps (HH:MM format)
- Message preview (80 chars)
- File attachment indicators
- Summary counts

### View Activity Feed

Show mentions, threads, and reactions from your Slack activity with enriched details:

```bash
# View all activity (mentions, threads, reactions)
uvx --from "git+https://github.com/shanemcd/slacker" slacker activity

# Filter by activity type
uvx --from "git+https://github.com/shanemcd/slacker" slacker activity --tab mentions
uvx --from "git+https://github.com/shanemcd/slacker" slacker activity --tab threads
uvx --from "git+https://github.com/shanemcd/slacker" slacker activity --tab reactions

# JSON output for programmatic processing
uvx --from "git+https://github.com/shanemcd/slacker" slacker --output json activity --tab mentions
```

**Activity types:**
- `all` - All activity (mentions, threads, reactions, invitations, etc.)
- `mentions` - Only @mentions, @channel, @everyone, and keywords
- `threads` - Only thread replies
- `reactions` - Only emoji reactions to your messages

**Text output features:**
- Activity type (mention, thread reply, reaction, etc.)
- Timestamp (YYYY-MM-DD HH:MM format)
- Channel name (resolved from channel IDs)
- **Actual usernames** (e.g., @jwong, @marturne)
- **Actual team names** (e.g., @aap-mcp-squad)
- **Rendered emojis** for standard emojis
- **Message preview** (80 characters of actual message text)
- **Clean formatting** (Slack markup removed)
- Unread indicator (bullet for unread items)

### Search Messages

```bash
# Search your own messages (notes to self)
uvx --from "git+https://github.com/shanemcd/slacker" slacker api search.messages --data '{"query": "from:@shanemcd to:@shanemcd", "count": 20, "sort": "timestamp", "sort_dir": "desc"}'

# Search in specific channel
uvx --from "git+https://github.com/shanemcd/slacker" slacker api search.messages --data '{"query": "in:#engineering important"}'
```

### Make Generic API Calls

**IMPORTANT:** Use `--params` for GET requests and `--data` for POST requests:
- `--params` sends query parameters (for GET endpoints like `conversations.replies`, `conversations.history`, `users.info`)
- `--data` sends JSON body (for POST endpoints like `chat.postMessage`, `search.messages`)

```bash
# GET request with parameters (conversations.replies, conversations.history, users.info, etc.)
uvx --from "git+https://github.com/shanemcd/slacker" slacker api users.list --params '{"limit": 10}'
uvx --from "git+https://github.com/shanemcd/slacker" slacker api conversations.replies --params '{"channel":"C05S34J4EE9","ts":"1765902174.251099","limit":"100"}'
uvx --from "git+https://github.com/shanemcd/slacker" slacker api conversations.history --params '{"channel":"C12345678","limit":"20"}'

# POST request with data (chat.postMessage, search.messages, etc.)
uvx --from "git+https://github.com/shanemcd/slacker" slacker api chat.postMessage --data '{"channel":"general","text":"Hello!"}'

# Post to your notes channel
uvx --from "git+https://github.com/shanemcd/slacker" slacker api chat.postMessage --data '{"channel":"D19Q000SE","text":"Remember to update slides for tomorrow"}'
```

**Note:** User IDs in the output are automatically resolved to usernames.

### Discover Available API Methods

```bash
# List all API categories
uvx --from "git+https://github.com/shanemcd/slacker" slacker discover

# Filter by category
uvx --from "git+https://github.com/shanemcd/slacker" slacker discover --category chat

# Show all methods
uvx --from "git+https://github.com/shanemcd/slacker" slacker discover --verbose
```

## JSON Output & Processing

All major commands support JSON output via the `--output json` flag for programmatic processing.

```bash
# Get reminders as structured data
uvx --from "git+https://github.com/shanemcd/slacker" slacker --output json reminders

# Get only overdue reminders with jq
uvx --from "git+https://github.com/shanemcd/slacker" slacker --output json reminders --reminders-only | \
  jq --arg now "$(date +%s)" '.items[] | select(.due_timestamp < ($now|tonumber)) | {text, due_date}'

# List all saved messages with full text
uvx --from "git+https://github.com/shanemcd/slacker" slacker --output json reminders | \
  jq '.items[] | select(.type == "message") | .message'

# Get summary counts
uvx --from "git+https://github.com/shanemcd/slacker" slacker --output json reminders | jq '.counts'
```

## Common Workflow Examples

### Morning Routine - Check Reminders

```bash
# List today's reminders
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminders --reminders-only
```

### Check Recent DM Activity

```bash
# Morning routine: check DMs since yesterday
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms --since "yesterday"

# After a meeting: check what you missed in the last hour
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms --since "1 hour ago"

# Monday morning: catch up on weekend messages
uvx --from "git+https://github.com/shanemcd/slacker" slacker dms --since "last Friday"
```

### Check Your Activity

```bash
# Morning routine: check all mentions and threads
uvx --from "git+https://github.com/shanemcd/slacker" slacker activity

# See who's reacting to your messages
uvx --from "git+https://github.com/shanemcd/slacker" slacker activity --tab reactions

# Check only @mentions to catch up quickly
uvx --from "git+https://github.com/shanemcd/slacker" slacker activity --tab mentions
```

### Quick Note Taking

```bash
# Post to your notes channel
uvx --from "git+https://github.com/shanemcd/slacker" slacker api chat.postMessage --data '{"channel":"D19Q000SE","text":"Remember to update slides for tomorrow"}'

# Create reminder from note
uvx --from "git+https://github.com/shanemcd/slacker" slacker reminder "me to update slides tomorrow at 8am"
```

### Review Past Notes

```bash
# Search your notes from last week (POST endpoint - uses --data)
uvx --from "git+https://github.com/shanemcd/slacker" slacker api search.messages --data '{"query":"from:@shanemcd to:@shanemcd after:7d"}'

# Get recent messages from notes channel (GET endpoint - uses --params)
uvx --from "git+https://github.com/shanemcd/slacker" slacker api conversations.history --params '{"channel":"D19Q000SE","limit":"20"}'
```

## Key API Endpoints

### Reminders & Later Items

**`saved.list`** - List saved items from Slack "Later"
```bash
uvx --from "git+https://github.com/shanemcd/slacker" slacker api saved.list --data '{"filter":"saved","limit":50,"include_tombstones":true}'
```

### Messages

**`search.messages`** - Search messages
- Supports JQL-like query syntax
- Filters: `from:`, `to:`, `in:`, date ranges
- Sorts by timestamp, relevance

**`conversations.history`** - Get message history
- Requires `channel` ID
- Returns messages with full metadata
- Supports pagination with `limit` and `cursor`

## Channel IDs

**Personal notes channel (notes to self):** `D19Q000SE`

To find other channel IDs:
1. Right-click channel in Slack -> "View channel details"
2. Copy channel ID from the details dialog
3. Or use search: `search.messages` queries reveal channel IDs in results

## Enterprise Restrictions

Red Hat Enterprise Slack workspace has restrictions on certain API endpoints:

**Restricted endpoints:**
- `reminders.list` - Blocked (use `saved.list` instead)
- `conversations.list` - Blocked
- `users.conversations` - Blocked

**Working alternatives:**
- Use `saved.list` for reminders
- Use `search.messages` to find conversations
- Use channel IDs directly when known

## Troubleshooting

### Authentication Expired

If `whoami` fails, re-extract credentials:
```bash
uvx --from "git+https://github.com/shanemcd/slacker" slacker login https://redhat.enterprise.slack.com
```

Credentials expire when you log out of Slack in your browser.

### Enterprise Restrictions

If an API endpoint returns `"error": "enterprise_is_restricted"`, the endpoint is blocked by workspace admin policies. Look for alternative endpoints (e.g., `saved.list` instead of `reminders.list`).

### Channel Not Found

Ensure you're using the correct channel ID format:
- DM/notes: `D` prefix (e.g., `D19Q000SE`)
- Public channel: `C` prefix (e.g., `C1234567890`)
- Private channel: `G` prefix (e.g., `G1234567890`)

## Security Notes

- Credentials stored locally at `~/.config/slacker/credentials`
- File permissions: `0600` (owner read/write only)
- Credentials tied to your browser session
- Expire when you log out of Slack
- Never commit credentials to git

## Tips

1. **Add a shell alias** for convenience:
   ```bash
   alias slacker='uvx --from "git+https://github.com/shanemcd/slacker" slacker'
   ```

2. **Use JSON output** for programmatic processing with `jq`

3. **Natural language reminders** - Slack handles the parsing, just write naturally

4. **Check activity regularly** - The activity command shows mentions you may have missed

5. **Use `--since` for DMs** - Natural language date parsing makes it easy to filter

## Links

- **Repository**: https://github.com/shanemcd/slacker
- **Issues**: https://github.com/shanemcd/slacker/issues

---

*Last updated: 2026-01-15*
