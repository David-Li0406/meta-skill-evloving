---
name: stuff-watcher
description: Watch classifieds for deals matching your wishlist
---

# Stuff Watcher

Monitor local classifieds (email + messaging apps) for items matching your family's wishlist. Send email alerts on matches.

## Data Sources

### 1. Classifieds Email (Primary)

- **Account**: [YOUR_EMAIL]
- **Tool**: `mcp__gmail__search_emails` and `mcp__gmail__read_email`
- **Sender**: [YOUR_CLASSIFIEDS_DIGEST_SENDER]
- **Subject filter**: "Classifieds" (or appropriate filter)

### 2. Group Chat (When Available)

- **Tool**: Configure based on your messaging platform
- **Group**: TBD (configure when available)
- **Status**: Requires setup - see Setup section

## Execution Flow

### Step 1: Load State

```
Read ~/.claude/skills/stuff-watcher/.last-processed-id (email)
Read ~/.claude/skills/stuff-watcher/.last-chat-id (group chat, if configured)
```

### Step 2: Fetch New Content

**Email:**

```
mcp__gmail__search_emails with query:
"from:[CLASSIFIEDS_SENDER] subject:Classifieds"
maxResults: 20
```

**Group Chat (when linked):**

```bash
# Configure based on your messaging platform
```

### Step 3: Filter to Unprocessed

- Only process emails/messages newer than last-processed IDs
- If no new content, skip to Step 7

### Step 4: Load Wishlist

Read `~/.claude/skills/stuff-watcher/references/wishlist.md`

### Step 5: Match & Score

For each listing:

- Extract item details (name, price, condition, location)
- Match against wishlist items
- Score: Strong / Possible / Weak

### Step 6: Send Alerts (If Matches Found)

**Only send email if there are Strong or Possible matches.**

Use `mcp__gmail__send_email`:

- **To**: [YOUR_FAMILY_EMAILS]
- **Subject**: `Classifieds Alert: [X matches found]`
- **Body**: See Email Format below

### Step 7: Update State

```bash
echo "<newest-email-id>" > ~/.claude/skills/stuff-watcher/.last-processed-id
echo "<newest-chat-id>" > ~/.claude/skills/stuff-watcher/.last-chat-id
```

### Step 8: Terminal Output

Brief summary:

- If matches: "Found X matches in Y listings - alert sent"
- If no matches: "Processed X listings, no matches"

## Match Scoring

### Strong Match (ALERT)

- Exact item from wishlist
- FREE or significantly below market price
- Good/excellent/new condition
- Location in preferred areas

### Possible Match (ALERT with caveat)

- Related item (e.g., "winter coat" when looking for "puffer jacket")
- Right category but details unclear
- Amazing deal not on wishlist
- Slightly outside preferred area

### Weak Match (LOG ONLY - no alert)

- Tangentially related
- Overpriced
- Poor condition
- Far location

## Email Alert Format

**Subject**: `Classifieds Alert: [N] matches found`

**Body**:

```
Found matches on local classifieds!

## Strong Matches

### [Item Name] - [FREE / $XX]
- Condition: [if mentioned]
- Location: [if mentioned]
- Details: [description excerpt]
- Source: [Email / Group Chat]
- Matched: "[wishlist item]"

[Repeat for each strong match]

## Possible Matches

### [Item Name] - [FREE / $XX]
- Details: [description]
- Why flagged: [reason]
- Source: [source]

---
Processed: X email listings, Y chat messages
Run time: [timestamp]
```

## No-Match Behavior

- Do NOT send email
- Terminal only: "Processed X listings, no matches"
- This is the expected common case

## State Files

| File                     | Purpose               |
| ------------------------ | --------------------- |
| `.last-processed-id`     | Last email message ID |
| `.last-chat-id`          | Last chat message ID  |
| `references/wishlist.md` | Items to watch for    |

## Cron Schedule

This skill is designed to run multiple times daily. Recommended schedule:

- 8:00 AM - Morning check
- 12:00 PM - Midday check
- 5:00 PM - Evening check
- 9:00 PM - Night check

## Tool Reference

**Read emails**:

```
mcp__gmail__search_emails
mcp__gmail__read_email
```

**Send alerts**:

```
mcp__gmail__send_email
```
