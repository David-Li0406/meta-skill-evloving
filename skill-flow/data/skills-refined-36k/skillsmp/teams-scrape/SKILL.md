---
name: teams-scrape
description: Use when extracting Microsoft Teams chat messages - navigates Teams, captures clipboard, parses to JSON, and persists with deterministic new message detection
version: 2.0.0
---

# Teams Chat Scraper

Extract chat messages from Microsoft Teams desktop app using `macos-automator` MCP tools and persist with deterministic new message detection.

## When to Use

Invoke this skill when you need to:
- Extract chat history from a Teams DM or channel
- Capture meeting chat content
- Get structured JSON from Teams messages
- Parse reactions, replies, and attachments
- **Track new messages** since last scrape (deterministic by message ID)

## Prerequisites

1. **Microsoft Teams desktop app** must be running
2. **Accessibility permissions** granted to the terminal/Claude Code
3. **macos-automator MCP** available (provides `execute_script` tool)

## Architecture

This skill uses a **two-phase approach**:

1. **AppleScript navigation** (via macos-automator MCP) - navigates Teams and captures clipboard
2. **TypeScript CLI** - parses clipboard, deduplicates by ID, persists atomically

The CLI handles parsing/storage/diffing, while AppleScript handles UI automation.

## Persistence & New Message Detection

Scrape results are saved to `~/.config/teams-scrape/` for tracking changes between runs.

### Storage Location

```
~/.config/teams-scrape/
├── ben-laughlin.json      # Kebab-case filename from target name
├── jay-pancholi.json
└── engineering-standup.json
```

### File Schema

```typescript
interface StoredChat {
  target: string;           // Original target name
  targetSlug: string;       // Kebab-case filename
  lastScrapedAt: string;    // ISO 8601 timestamp of last scrape
  messageCount: number;     // Total messages stored
  messages: TeamsMessage[]; // All captured messages (sorted by timestamp)
}

interface TeamsMessage {
  id: string;               // Stable hash ID for deduplication
  author: string;
  timestamp: string;        // ISO 8601
  content: string;
  replyTo?: { author: string; preview: string };
  reactions?: { emoji: string; count: number; name: string }[];
  attachments?: { type: "gif" | "image" | "file" | "url" | "loop"; name?: string; url?: string }[];
  mentions?: string[];
  edited?: boolean;
}
```

### Deterministic New Message Detection

The CLI uses **stable message IDs** (hash of author + timestamp + content prefix) to detect truly new messages:

1. Parse clipboard into `TeamsMessage[]` with stable IDs
2. Load existing stored chat (if any)
3. Compare by message ID to find truly new messages
4. Merge (append new only, preserve existing)
5. Save atomically with file locking

This ensures running the same scrape twice reports "0 new messages" - the detection is **deterministic**.

## CLI Usage

The `teams-scrape` CLI provides three commands:

```bash
# Process clipboard (main command)
pbpaste | bun run plugins/teams-scrape/src/cli.ts process "Ben Laughlin"

# Load existing history (read-only)
bun run plugins/teams-scrape/src/cli.ts load "Ben Laughlin"

# List all stored chats
bun run plugins/teams-scrape/src/cli.ts list
```

### CLI Output (process command)

```json
{
  "target": "Ben Laughlin",
  "capturedAt": "2026-01-20T10:00:00.000Z",
  "isNewScrape": false,
  "totalMessages": 31,
  "newMessages": [
    {
      "id": "abc123def456",
      "author": "Ben Laughlin",
      "timestamp": "2026-01-20T09:15:00.000Z",
      "content": "Hey, did you see the PR?"
    }
  ],
  "storagePath": "/Users/nathan/.config/teams-scrape/ben-laughlin.json"
}
```

## Workflow

### Step 1: Navigate to Target Chat

Use `macos-automator` to activate Teams and navigate:

```applescript
-- Navigate to a specific person or channel
tell application "Microsoft Teams" to activate
delay 0.5
tell application "System Events"
    tell process "Microsoft Teams"
        keystroke "g" using command down  -- Open "Go to" search
        delay 0.8
        keystroke "TARGET_NAME"           -- Type target name
        delay 1.5
        key code 36                        -- Enter (select first result)
        delay 1.5
    end tell
end tell
```

**MCP call:**
```json
{
  "tool": "mcp__macos-automator__execute_script",
  "arguments": {
    "script_content": "tell application \"Microsoft Teams\" to activate\ndelay 0.5\ntell application \"System Events\"\n    tell process \"Microsoft Teams\"\n        keystroke \"g\" using command down\n        delay 0.8\n        keystroke \"Jay Pancholi\"\n        delay 1.5\n        key code 36\n        delay 1.5\n    end tell\nend tell",
    "timeout_seconds": 10
  }
}
```

### Step 2: Capture Chat Content

**Critical:** Press Escape before Cmd+A to ensure the chat area has focus.

```applescript
tell application "System Events"
    tell process "Microsoft Teams"
        key code 53                        -- Escape (clear focus)
        delay 0.3
        keystroke "a" using command down   -- Select all
        delay 0.5
        keystroke "c" using command down   -- Copy
        delay 0.8
    end tell
end tell
do shell script "pbpaste"                  -- Return clipboard content
```

**MCP call:**
```json
{
  "tool": "mcp__macos-automator__execute_script",
  "arguments": {
    "script_content": "tell application \"System Events\"\n    tell process \"Microsoft Teams\"\n        key code 53\n        delay 0.3\n        keystroke \"a\" using command down\n        delay 0.5\n        keystroke \"c\" using command down\n        delay 0.8\n    end tell\nend tell\ndo shell script \"pbpaste\"",
    "timeout_seconds": 5
  }
}
```

### Step 3: Parse the Clipboard Content

Parse the raw text into structured JSON. See format documentation below.

---

## Teams Clipboard Format

Teams uses a specific text format when copying chat content. For detailed parsing patterns, see [FORMAT.md](FORMAT.md).

**Key patterns:**
- Messages: `AuthorName\nDD/MM/YYYY H:MM am/pm\nContent`
- Replies: `Begin Reference...End Reference` blocks
- Reactions: `emoji\nN emoji-name reactions.`
- Attachments: `(GIF Image)`, `(Image)`, `has an attachment:`, `Url Preview for`, `Loop Component`
- Mentions: Inline names or `Everyone`
- Edited: `Edited.` suffix

---

## Output Schema

Return parsed messages as JSON:

```typescript
interface TeamsMessage {
  author: string;
  timestamp: string;          // ISO 8601 format
  content: string;
  replyTo?: {
    author: string;
    preview: string;
  };
  reactions?: {
    emoji: string;
    count: number;
    name: string;
  }[];
  attachments?: {
    type: "gif" | "image" | "file" | "url" | "loop";
    name?: string;
    url?: string;
  }[];
  mentions?: string[];
  edited?: boolean;
}

interface TeamsChat {
  target: string;             // Channel or person name
  capturedAt: string;         // ISO 8601 timestamp
  messageCount: number;
  messages: TeamsMessage[];
}
```

**Example output:**

```json
{
  "target": "Jay Pancholi",
  "capturedAt": "2025-01-20T14:30:00.000Z",
  "messageCount": 2,
  "messages": [
    {
      "author": "Jay Pancholi",
      "timestamp": "2025-01-15T14:34:00.000Z",
      "content": "Hey Nathan, just checking in on the project status.\nLet me know when you have a moment.",
      "reactions": [
        { "emoji": "👍", "count": 1, "name": "like" }
      ]
    },
    {
      "author": "Nathan Vale",
      "timestamp": "2025-01-15T14:45:00.000Z",
      "content": "All good! I'll have the update ready by EOD.",
      "replyTo": {
        "author": "Jay Pancholi",
        "preview": "Hey Nathan, just checking in on the project status."
      }
    }
  ]
}
```

---

## Error Handling

### Teams Not Running

If Teams is not running, the AppleScript will fail. Check first:

```applescript
tell application "System Events"
    set isRunning to (name of processes) contains "Microsoft Teams"
end tell
return isRunning
```

### Target Not Found

If Cmd+G search doesn't find the target:
- The script will timeout waiting for navigation
- Suggest verifying the exact name/channel exists
- Consider partial matches or typos

### Accessibility Permissions

If keystrokes don't work:
- Check System Preferences → Security & Privacy → Privacy → Accessibility
- Ensure terminal app has permission granted

### Empty Clipboard

If clipboard is empty after capture:
- Teams window may not have focus
- Chat area may not be selected
- Try the Escape → Cmd+A → Cmd+C sequence again

---

## Complete Example

**User request:** "Scrape my chat with Jay Pancholi from Teams"

**Workflow:**

1. Navigate to Jay Pancholi's chat using Cmd+G (AppleScript via macos-automator)
2. Capture content with Escape → Cmd+A → Cmd+C (AppleScript)
3. Pipe clipboard to CLI for parsing and persistence
4. Return structured JSON with new message detection

**Step 1: Navigate and capture (AppleScript)**

```applescript
-- Navigate and capture in one script
tell application "Microsoft Teams" to activate
delay 0.5

tell application "System Events"
    tell process "Microsoft Teams"
        -- Navigate
        keystroke "g" using command down
        delay 0.8
        keystroke "Jay Pancholi"
        delay 1.5
        key code 36
        delay 2.0

        -- Capture
        key code 53
        delay 0.3
        keystroke "a" using command down
        delay 0.5
        keystroke "c" using command down
        delay 0.8
    end tell
end tell

do shell script "pbpaste"
```

**Step 2: Process with CLI**

After capturing clipboard content, pipe it to the CLI:

```bash
pbpaste | bun run plugins/teams-scrape/src/cli.ts process "Jay Pancholi"
```

**Expected output:**

```json
{
  "target": "Jay Pancholi",
  "capturedAt": "2026-01-20T14:30:00.000Z",
  "isNewScrape": false,
  "totalMessages": 45,
  "newMessages": [
    {
      "id": "a1b2c3d4e5f6",
      "author": "Jay Pancholi",
      "timestamp": "2026-01-20T14:25:00.000Z",
      "content": "The PR is ready for review"
    }
  ],
  "storagePath": "/Users/nathan/.config/teams-scrape/jay-pancholi.json"
}
```

---

## Tips

- **Increase delays** if Teams is slow to respond (especially on first navigation)
- **Verify target name** matches exactly what appears in Teams search
- **AU date format**: The parser handles DD/MM/YYYY H:MM am/pm automatically
- **Deterministic detection**: Same scrape twice = 0 new messages (deduplication by ID)
- **Atomic writes**: CLI uses file locking for concurrent safety
- **Filename convention**: Target names are auto-converted to kebab-case
- **Logs**: Check `~/.claude/logs/teams-scrape.jsonl` for debugging

## Observability

- **Logs**: JSONL format at `~/.claude/logs/teams-scrape.jsonl`
- **Correlation IDs**: Each CLI invocation gets a unique correlation ID for tracing
- **Timing**: All operations are logged with duration in milliseconds
- **Error categorization**: Errors are classified as transient/permanent/configuration
