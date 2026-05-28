# Session Management

Unified management of conversation threads and deep research sessions.

## Contents

- Session Types
- Ownership
- Unified Listing
- Thread Management (lifecycle, operations)
- Research Session Management (lifecycle, operations)
- Deletion Confirmation Gate
- Resuming Sessions
- Storage Interface
- Data Handling Policy
- Auto-Cleanup Behavior
- Filtering Sessions

## Session Types

| Type | ID Format | Description |
|------|-----------|-------------|
| Thread | `thread-[a-zA-Z0-9]{8,16}` | Interactive conversations (chat, thinkdeep, ideate) |
| Research | `research-[a-zA-Z0-9]{8,16}` | Background deep research sessions |

## Ownership

**foundry-mcp is the single source of truth** for all session data. The skill never caches or stores session state locally.

## Unified Listing

The `foundry-research sessions` command shows both types:

```bash
mcp__plugin_foundry_foundry-mcp__research action="thread-list" limit=10
mcp__plugin_foundry_foundry-mcp__research action="deep-research-list" limit=10
```

### Combined Display

```
AskUserQuestion:
"Select a session to resume:"
Options:
- "thread-abc123: 'API design discussion' (chat, 3 messages, 2h ago)"
- "thread-def456: 'Performance analysis' (thinkdeep, 7 messages, 1d ago)"
- "research-xyz789: 'ML frameworks survey' (completed, 42 sources)"
- "research-ghi012: 'Auth patterns' (in_progress, 60%)"
- "Start new session"
- "Cancel"
```

## Thread Management

### Thread Lifecycle

```
created → active → archived → deleted
   │         │         │
   │         │         └→ Soft delete (recoverable for 30 days)
   │         └→ No activity for 7 days
   └→ First message sent
```

| State | Description | Can Resume | Can Delete |
|-------|-------------|------------|------------|
| `created` | Thread initialized, no messages | Yes | Yes |
| `active` | Has messages, recently used | Yes | Yes |
| `archived` | Inactive >7 days, auto-archived | Yes | Yes |
| `deleted` | Soft deleted, pending purge | No | N/A |

### Thread Operations

```bash
# List threads
mcp__plugin_foundry_foundry-mcp__research action="thread-list" limit=10 status="active"

# Get thread details
mcp__plugin_foundry_foundry-mcp__research action="thread-get" thread_id="thread-abc123"

# Delete thread
mcp__plugin_foundry_foundry-mcp__research action="thread-delete" thread_id="thread-abc123"
```

## Research Session Management

### Session Lifecycle

```
started → in_progress → completed
              │              │
              └→ failed      └→ (report available)
```

| State | Description | Can Resume | Has Report |
|-------|-------------|------------|------------|
| `started` | Initialized, beginning decomposition | Yes | No |
| `in_progress` | Actively researching | Yes | Partial |
| `completed` | All iterations done | No | Yes |
| `failed` | Error during research | Yes | Partial |

### Research Operations

```bash
# List research sessions
mcp__plugin_foundry_foundry-mcp__research action="deep-research-list" limit=10 completed_only=false

# Get session status
mcp__plugin_foundry_foundry-mcp__research action="deep-research-status" research_id="research-abc123"

# Get final report
mcp__plugin_foundry_foundry-mcp__research action="deep-research-report" research_id="research-abc123"

# Delete session
mcp__plugin_foundry_foundry-mcp__research action="deep-research-delete" research_id="research-abc123"
```

## Deletion Confirmation Gate

Before deleting any session, always confirm:

### Thread Deletion
```
AskUserQuestion:
"Delete thread {thread_id}? This removes {n} messages."
Options:
- "Yes, delete permanently"
- "No, keep thread"
- "Archive instead"
```

### Research Session Deletion
```
AskUserQuestion:
"Delete research session {research_id}? This removes the report and all gathered sources."
Options:
- "Yes, delete permanently"
- "No, keep session"
```

## Resuming Sessions

### Resume Thread
```
foundry-research thread-abc123 continue the discussion
```
Invokes:
```bash
mcp__plugin_foundry_foundry-mcp__research action="chat" thread_id="thread-abc123" prompt="continue the discussion"
```

### Resume Research (check status)
```
foundry-research research-abc123
```
Invokes:
```bash
mcp__plugin_foundry_foundry-mcp__research action="deep-research-status" research_id="research-abc123"
```
Then fetches report if completed.

## Storage Interface

### Read Operations
- **Always** read from MCP on resume (no local cache)
- Thread/session context loaded fresh each interaction

### Write Operations
- Messages persisted to MCP after each exchange
- Research progress updated automatically during execution
- Metadata updated (timestamps, turn count, progress)

### Cache Rules
- No persistent client-side cache
- In-memory context valid only for current conversation
- Refresh on each resume

## Data Handling Policy

| Aspect | Threads | Research Sessions |
|--------|---------|-------------------|
| Retention (active) | Indefinite | Indefinite |
| Retention (archived) | 90 days | 90 days |
| Retention (deleted) | 30 days soft | 30 days soft |
| Hard delete | After 30-day soft delete | After 30-day soft delete |
| Redaction | User can request | User can request |

## Auto-Cleanup Behavior

| Trigger | Threads | Research Sessions |
|---------|---------|-------------------|
| No activity 7 days | Auto-archive | No action |
| Archived 90 days | Auto-delete (soft) | Auto-delete (soft) |
| Soft deleted 30 days | Hard delete | Hard delete |
| Completed 90 days | N/A | Auto-archive |

Auto-cleanup runs daily. Users notified before archive/delete via system message.

## Filtering Sessions

```bash
# Only threads
foundry-research sessions list type=threads

# Only research
foundry-research sessions list type=research

# All (default)
foundry-research sessions list

# Only completed research
foundry-research sessions list type=research completed=true
```
