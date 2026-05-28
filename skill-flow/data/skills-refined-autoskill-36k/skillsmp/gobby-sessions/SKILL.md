---
name: gobby-sessions
description: This skill should be used when the user asks to "/gobby-sessions", "list sessions", "session handoff", "pickup session". Manage agent sessions - list, show details, handoff context, search messages, and resume previous work.
---

# /gobby-sessions - Session Management Skill

This skill manages agent sessions via the gobby-sessions MCP server. Parse the user's input to determine which subcommand to execute.

## Session Context

**IMPORTANT**: Use the `session_id` from your SessionStart hook context for most calls. Look for it in your system context:
```
session_id: fd59c8fc-...
```

This is the **internal Gobby session ID** - use it for task creation, parent_session_id, etc.

## Subcommands

### `/gobby-sessions get-current` - Look up your session ID
Call `gobby-sessions.get_current` with:
- `external_id`: (required) Your CLI's session ID
- `source`: (required) CLI source - "claude", "antigravity", "gemini", or "codex"

Returns your internal Gobby session_id from the external CLI session ID.

**How to find your external_id by CLI:**

| CLI | How to find external_id |
|-----|------------------------|
| **Claude Code** | Extract from your JSONL transcript path: `/path/to/<external_id>.jsonl` |
| **Antigravity** | Same as Claude Code - extract from JSONL path |
| **Gemini** | Extract from your transcript path filename |
| **Codex** | Extract from your session transcript path |

**When to use this tool:**
- When you only have the CLI's external session ID (from transcript path, env var, etc.)
- When `session_id` wasn't injected in your context
- For cross-CLI session correlation

**Note:** If you already have `session_id` in your context (from SessionStart hook), you don't need this tool.

Example: `/gobby-sessions get-current ea13ad4f-ca32-48e6-9000-e5e6af35a397 claude`
→ `get_current(external_id="ea13ad4f-ca32-48e6-9000-e5e6af35a397", source="claude")`

### `/gobby-sessions list` - List all sessions
Call `gobby-sessions.list_sessions` with:
- `limit`: Max results (default 20)
- `status`: Filter by status (active, ended)
- `source`: Filter by source (claude, gemini, codex)
- `project_id`: Optional project scope

Returns recent sessions with ID, source, start time, and status.

Example: `/gobby-sessions list` → `list_sessions(limit="20")`
Example: `/gobby-sessions list active` → `list_sessions(status="active")`
Example: `/gobby-sessions list claude` → `list_sessions(source="claude")`

### `/gobby-sessions show <session-id>` - Show session details
Call `gobby-sessions.get_session` with:
- `session_id`: (required) The session ID to retrieve

Returns full session details including:
- Session metadata (source, times, duration)
- Tool calls made
- Tasks worked on
- Summary if available

Example: `/gobby-sessions show` → `get_session(session_id="<current session_id>")`
Example: `/gobby-sessions show sess-abc123` → `get_session(session_id="sess-abc123")`

### `/gobby-sessions messages <session-id>` - Get session messages
Call `gobby-sessions.get_session_messages` with:
- `session_id`: (required) Session ID
- `limit`: Max messages to return
- `offset`: Skip first N messages
- `full_content`: Include full message content (default truncated)

Returns conversation messages from a session.

Example: `/gobby-sessions messages` → `get_session_messages(session_id="<current session_id>")`

### `/gobby-sessions search <query>` - Search messages
Call `gobby-sessions.search_messages` with:
- `query`: (required) Search query (uses FTS)
- `session_id`: Optional - scope to specific session
- `limit`: Max results
- `full_content`: Include full message content

Searches message content using Full Text Search.

Example: `/gobby-sessions search authentication bug` → `search_messages(query="authentication bug")`
Example: `/gobby-sessions search error --session=sess-abc123` → `search_messages(query="error", session_id="sess-abc123")`

### `/gobby-sessions handoff` - Create session handoff
Call `gobby-sessions.create_handoff` with:
- `session_id`: (REQUIRED) Your session ID - from injected context or `get_current()`
- `notes`: Optional notes to include
- `compact`: Generate compact markdown
- `full`: Generate full transcript
- `write_file`: Write to file
- `output_path`: Custom output path

Creates handoff context by extracting structured data from the session transcript.

Example: `/gobby-sessions handoff` → `create_handoff(session_id="<your session_id>")`
Example: `/gobby-sessions handoff --notes="Continue with auth feature"` → `create_handoff(session_id="...", notes="Continue with auth feature")`

### `/gobby-sessions get-handoff <session-id>` - Get existing handoff
Call `gobby-sessions.get_handoff_context` with:
- `session_id`: (required) Session ID

Retrieves the handoff context (compact_markdown) for a session.

Example: `/gobby-sessions get-handoff sess-abc123` → `get_handoff_context(session_id="sess-abc123")`

### `/gobby-sessions pickup [session-id]` - Resume a previous session
Call `gobby-sessions.pickup` with:
- `session_id`: Optional specific session ID (defaults to most recent)
- `source`: Filter by source (claude, gemini, codex)
- `project_id`: Optional project scope
- `link_child_session_id`: Link this session as child

Retrieves and injects handoff context from a previous session.

Example: `/gobby-sessions pickup` → `pickup()` (resumes most recent)
Example: `/gobby-sessions pickup sess-abc123` → `pickup(session_id="sess-abc123")`

### `/gobby-sessions commits <session-id>` - Get session commits
Call `gobby-sessions.get_session_commits` with:
- `session_id`: (required) Session ID
- `max_commits`: Max commits to return

Returns git commits made during the session timeframe.

Example: `/gobby-sessions commits` → `get_session_commits(session_id="<current session_id>")`

### `/gobby-sessions stats` - Get session statistics
Call `gobby-sessions.session_stats` with:
- `project_id`: Optional project scope

Returns session statistics for the project.

Example: `/gobby-sessions stats` → `session_stats()`

### `/gobby-sessions mark-complete` - Mark loop complete
Call `gobby-sessions.mark_loop_complete` with:
- `session_id`: (REQUIRED) Your session ID - from injected context or `get_current()`

Marks the autonomous loop as complete, preventing session chaining.

Example: `/gobby-sessions mark-complete` → `mark_loop_complete(session_id="<your session_id>")`

## Response Format

After executing the appropriate MCP tool, present the results clearly:
- For list: Table with session ID, source, start time, duration, status
- For show: Full session details in readable format
- For messages: Formatted conversation history
- For search: Matching messages with context
- For handoff/create_handoff: Confirm handoff context was prepared, show summary
- For get-handoff: Show stored handoff context
- For pickup: Show injected context, highlight key continuation points
- For commits: List commits with SHA, message, and timestamp
- For stats: Session statistics summary
- For mark-complete: Confirmation

## Session Concepts

- **Session**: A single agent conversation (Claude Code, Gemini CLI, or Codex)
- **Handoff**: Context preservation across sessions via /compact
- **Pickup**: Resuming work from a previous session's context
- **Source**: Which CLI tool created the session

## ⚠️ Common Mistake: Using list_sessions to Find Your Session

**WRONG:**
```python
# ❌ This will NOT work with multiple active sessions!
result = list_sessions(status="active", limit=1)
my_session_id = result["sessions"][0]["id"]  # Could be ANY active session!
```

**CORRECT:**
```python
# ✅ Use get_current with your unique identifiers
result = get_current(external_id="...", source="claude")
my_session_id = result["session_id"]
```

Multiple sessions can be active simultaneously (parallel agents, multiple terminals). The `get_current` tool uses a composite key to reliably find YOUR session.

## Error Handling

If the subcommand is not recognized, show available subcommands:
- get-current, list, show, messages, search, handoff, get-handoff, pickup, commits, stats, mark-complete
