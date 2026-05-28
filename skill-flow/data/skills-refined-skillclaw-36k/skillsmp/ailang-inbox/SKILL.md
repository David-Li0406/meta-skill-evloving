---
name: AILANG Inbox
description: Cross-agent communication system with semantic search and GitHub sync. Check messages, find similar content, deduplicate, and sync with GitHub Issues for AI workflows across sessions.
---

# AILANG Inbox

AILANG's messaging system enables AI agents to communicate asynchronously across sessions and projects. Features semantic search (SimHash + Ollama neural), deduplication, and GitHub sync.

## Session Start Routine

**At the start of EVERY session, check for messages:**

```bash
# Check for unread messages
ailang messages list --unread

# Or check specific inbox
ailang messages list --inbox user --unread
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `ailang messages list --unread` | Check for new messages |
| `ailang messages list --inbox user` | Check user inbox |
| `ailang messages send user "msg" --from agent` | Send to user |
| `ailang messages ack MSG_ID` | Mark as read |
| `ailang messages ack --all` | Mark all as read |
| `ailang messages read MSG_ID` | View full message |
| `ailang messages search "query"` | Semantic search (SimHash) |
| `ailang messages search "query" --neural` | Neural search (Ollama) |
| `ailang messages dedupe` | Find duplicate messages |
| `ailang messages dedupe --apply` | Mark duplicates |

## Checking Messages

### List Messages

```bash
# All messages
ailang messages list

# Only unread
ailang messages list --unread

# Specific inbox
ailang messages list --inbox user

# Filter by sender
ailang messages list --from sprint-executor

# Limit results
ailang messages list --limit 5

# JSON output (for parsing)
ailang messages list --json
```

### Read Full Message

```bash
# View complete message content
ailang messages read MSG_ID
```

### Acknowledge Messages

```bash
# Mark single message as read
ailang messages ack MSG_ID

# Mark all unread as read
ailang messages ack --all

# Mark all in specific inbox
ailang messages ack --all --inbox user

# Mark as unread again (for retry)
ailang messages unack MSG_ID
```

## Sending Messages

### To User

```bash
# Simple text message
ailang messages send user "Task completed successfully" --from my-agent --title "Status Update"

# With JSON payload
ailang messages send user --json '{"status":"done","result":"All tests passing"}' --from my-agent
```

### To Another Agent

```bash
# Send to specific agent inbox
ailang messages send sprint-executor "Ready for handoff" --from planner

# With correlation ID (for tracking workflows)
ailang messages send sprint-executor --json '{"task":"execute"}' --from planner --correlation workflow_123
```

## Workflow Patterns

### 1. Session Start Check

```bash
# 1. Check for messages
ailang messages list --unread

# 2. If messages exist:
#    - Summarize to user
#    - Ask what action to take

# 3. After handling:
ailang messages ack --all
```

### 2. Agent Handoff

```bash
# Agent A completes work and hands off to Agent B
ailang messages send agent-b --json '{
  "type": "handoff",
  "task": "continue_implementation",
  "artifacts": ["path/to/results/"],
  "context": "Previous work completed"
}' --from agent-a --correlation project_xyz
```

### 3. Completion Notification

```bash
# Notify user that autonomous work is done
ailang messages send user --json '{
  "type": "completion",
  "status": "success",
  "summary": "All 5 milestones completed",
  "artifacts": ["results/v1.0/"]
}' --from sprint-executor --title "Sprint Complete"
```

### 4. Error Reporting

```bash
# Report error to user
ailang messages send user --json '{
  "type": "error",
  "error": "Tests failing at milestone 3",
  "details": "logs/error.log",
  "needs_help": true
}' --from executor --title "Error Encountered"
```

## Correlation IDs

Track related messages across agent handoffs:

```json
{
  "message_id": "msg_20251208_103045_abc123",
  "correlation_id": "workflow_project_x",
  "from": "planner",
  "to": "executor",
  "payload": { ... }
}
```

**Benefits:**
- Track entire workflow chains
- Filter messages by workflow
- Debug multi-agent interactions
- Resume work from where you left off

## Message Types

### Completion
```json
{
  "type": "completion",
  "status": "success",
  "result": "All tests passing",
  "artifacts": ["path/to/output/"]
}
```

### Handoff
```json
{
  "type": "handoff",
  "task": "next_phase",
  "context": "Previous work summary",
  "dependencies": ["file1.ail", "file2.ail"]
}
```

### Error
```json
{
  "type": "error",
  "error": "Description of failure",
  "details": "path/to/logs",
  "needs_help": true
}
```

### Request
```json
{
  "type": "request",
  "action": "review_code",
  "files": ["src/module.ail"],
  "priority": "high"
}
```

## Watch for Messages

Monitor for new messages in real-time:

```bash
# Watch all inboxes
ailang messages watch

# Watch specific inbox
ailang messages watch --inbox user
```

## Cleanup

Remove old messages:

```bash
# Remove messages older than 7 days
ailang messages cleanup --older-than 7d

# Remove expired messages
ailang messages cleanup --expired

# Preview without deleting
ailang messages cleanup --dry-run
```

## Semantic Search (v0.5.11+)

Find messages by meaning, not just exact text. AILANG uses SimHash by default for fast, zero-cost semantic search.

### Search Commands

```bash
# Search by semantic content (SimHash - default, fast)
ailang messages search "parser error handling"

# Set similarity threshold (0.0-1.0)
ailang messages search "bugs" --threshold 0.5

# Find messages similar to a specific message
ailang messages list --similar-to MSG_ID

# Hide duplicate messages (collapsed view)
ailang messages list --collapsed

# Show duplicates of a specific message
ailang messages list --duplicates-of MSG_ID
```

### Search Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--threshold` | 0.70 | Minimum similarity (0.0-1.0) |
| `--limit` | 20 | Maximum results |
| `--max-scan` | 1000 | Maximum messages to scan |
| `--inbox` | (all) | Filter by inbox |
| `--neural` | false | Use Ollama embeddings |
| `--simhash` | true | Force SimHash mode |
| `--json` | false | Output as JSON |

### How SimHash Works

SimHash generates a 64-bit fingerprint based on word frequencies:
- **Score 1.0**: Identical or near-identical
- **Score 0.9+**: Very similar (likely duplicates)
- **Score 0.7-0.9**: Related topics
- **Score below 0.7**: Different content

## Deduplication

Find and mark duplicate messages to reduce inbox noise.

```bash
# Report duplicates (dry run - shows what would be marked)
ailang messages dedupe

# Custom similarity threshold
ailang messages dedupe --threshold 0.90

# Actually mark duplicates
ailang messages dedupe --apply

# Filter by inbox
ailang messages dedupe --inbox user --apply
```

### How Deduplication Works

1. **Find groups**: Messages with similarity ≥ threshold are grouped
2. **Select representative**: Oldest message in each group is kept
3. **Mark duplicates**: Newer messages get `dup_of` set to representative's ID
4. **View behavior**: `--collapsed` hides messages with `dup_of` set

## Neural Search (Ollama)

For more sophisticated semantic search, use neural embeddings via local Ollama.

### Prerequisites

1. Install Ollama: https://ollama.ai
2. Start Ollama server: `ollama serve`
3. Pull an embedding model: `ollama pull nomic-embed-text`

### Configuration

Create `~/.ailang/config.yaml`:

```yaml
embeddings:
  provider: ollama
  ollama:
    model: nomic-embed-text
    endpoint: http://localhost:11434
    timeout: 30s
  search:
    default_mode: simhash
    simhash_threshold: 0.70
    neural_threshold: 0.75
```

### Using Neural Search

```bash
# Use neural embeddings (requires Ollama running)
ailang messages search "parser bugs" --neural

# Force SimHash (faster, no Ollama needed)
ailang messages search "parser bugs" --simhash
```

### Model Recommendations

| Model | Speed | Quality | Notes |
|-------|-------|---------|-------|
| `nomic-embed-text` | Fast | Good | Best balance |
| `mxbai-embed-large` | Medium | Better | Higher quality |
| `embeddinggemma` | Fast | Good | Google model |

## GitHub Integration (v0.5.9+)

Sync messages with GitHub Issues for visibility across AILANG instances.

### Sending to GitHub

```bash
# Bug report (creates GitHub issue)
ailang messages send user "Parser crash" --type bug --github

# Feature request
ailang messages send user "Add async support" --type feature --github

# Custom repo
ailang messages send user "Bug report" --github --repo owner/repo
```

### Importing from GitHub

```bash
# Import issues from configured repo
ailang messages import-github

# Filter by labels
ailang messages import-github --labels bug,feature

# Preview without importing
ailang messages import-github --dry-run
```

### GitHub Configuration

Add to `~/.ailang/config.yaml`:

```yaml
github:
  expected_user: YourGitHubUsername   # Must match gh auth status
  default_repo: owner/repo             # Target repo for issues
  create_labels:
    - ailang-message
  watch_labels:
    - ailang-message
  auto_import: true                    # Import on session start
```

## Storage

- **Database**: `~/.ailang/state/collaboration.db` (SQLite)
- **Shared with**: Collaboration Hub dashboard
- **Message statuses**: `unread`, `read`, `archived`, `deleted`

## Integration with Collaboration Hub

Messages are visible in the web dashboard:

```bash
# Start the Collaboration Hub server
ailang serve

# Access at http://localhost:1957
```

The dashboard provides:
- Real-time message view
- Agent activity timeline
- Workflow visualization
- Message filtering and search
