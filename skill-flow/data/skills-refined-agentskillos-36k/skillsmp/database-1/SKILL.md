---
name: database
description: Database skill for the ikigai project
---

# Database

## Description
PostgreSQL-backed event stream architecture with agent registry, session management, message persistence, inter-agent mail, and conversation replay using talloc-based memory management.

## Schema

### schema_metadata
Tracks applied migrations for incremental schema updates.

| Column         | Type    | Constraints    | Description                   |
|----------------|---------|----------------|-------------------------------|
| schema_version | INTEGER | PRIMARY KEY    | Current schema version number |

**Current version:** 5

### sessions
Groups messages by conversation session with persistent state across app launches.

| Column     | Type        | Constraints    | Description                              |
|------------|-------------|----------------|------------------------------------------|
| id         | BIGSERIAL   | PRIMARY KEY    | Session identifier                       |
| started_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Session start timestamp       |
| ended_at   | TIMESTAMPTZ | NULL           | Session end timestamp (NULL = active)    |
| title      | TEXT        | NULL           | Optional user-defined session title      |

**Indexes:**
- `idx_sessions_started`: `started_at DESC` for recent session lookup

### messages
Event stream storage for conversation timeline with support for replay, rollback, and agent attribution.

| Column     | Type        | Constraints                          | Description                        |
|------------|-------------|--------------------------------------|------------------------------------|
| id         | BIGSERIAL   | PRIMARY KEY                          | Message identifier                 |
| session_id | BIGINT      | NOT NULL, FK sessions(id) ON DELETE CASCADE | Parent session           |
| kind       | TEXT        | NOT NULL                             | Event type discriminator           |
| content    | TEXT        | NULL                                 | Message text (NULL for clear)      |
| data       | JSONB       | NULL                                 | Event metadata (LLM params, etc.)  |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW()              | Event timestamp                    |
| agent_uuid | TEXT        | NULL, FK agents(uuid)                | Agent that created this message    |

**Event Kinds:**
- `clear`: Context reset (session start or /clear command)
- `system`: System prompt message
- `user`: User input message
- `assistant`: LLM response message
- `tool_call`: Tool invocation request
- `tool_result`: Tool execution result
- `mark`: Checkpoint created by /mark command
- `rewind`: Rollback operation created by /rewind command
- `agent_killed`: Agent termination event
- `command`: Slash command output for persistence across restarts
- `fork`: Fork event recorded in both parent and child histories
- `usage`: Token usage tracking event

**Indexes:**
- `idx_messages_session`: `(session_id, created_at)` for chronological event stream processing
- `idx_messages_search`: GIN index on `to_tsvector('english', content)` for full-text search
- `idx_messages_agent`: `(agent_uuid, id)` for efficient agent-based range queries

### agents
Agent registry tracking agent lifecycle, parent-child relationships, and status transitions.

| Column          | Type         | Constraints                          | Description                              |
|-----------------|--------------|--------------------------------------|------------------------------------------|
| uuid            | TEXT         | PRIMARY KEY                          | Base64url agent UUID (22 chars)          |
| name            | TEXT         | NULL                                 | Optional human-friendly name             |
| parent_uuid     | TEXT         | NULL, FK agents(uuid) ON DELETE RESTRICT | Parent agent (NULL for root)    |
| fork_message_id | BIGINT       | NULL                                 | Message ID at fork point                 |
| status          | agent_status | NOT NULL, DEFAULT 'running'          | Agent status (running/dead)              |
| created_at      | BIGINT       | NOT NULL                             | Unix epoch timestamp (seconds)           |
| ended_at        | BIGINT       | NULL                                 | Unix epoch timestamp (NULL if running)   |
| provider        | TEXT         | NULL                                 | LLM provider (anthropic, openai, etc.)   |
| model           | TEXT         | NULL                                 | Model identifier (claude-opus-4.5, etc.) |
| thinking_level  | TEXT         | NULL                                 | Thinking budget/level for extended thinking |

**Enum Types:**
- `agent_status`: `'running'`, `'dead'`

**Indexes:**
- `idx_agents_parent`: `parent_uuid` for child queries
- `idx_agents_status`: `status` for running agent queries

**Constraints:**
- Parent deletion is RESTRICTED (must kill children first)
- Agent 0 (root) has `parent_uuid=NULL`

### mail
Inter-agent messaging table for Erlang-style message passing between agents.

| Column     | Type      | Constraints                          | Description                        |
|------------|-----------|--------------------------------------|------------------------------------|
| id         | BIGSERIAL | PRIMARY KEY                          | Mail message identifier            |
| session_id | BIGINT    | NOT NULL, FK sessions(id) ON DELETE CASCADE | Parent session           |
| from_uuid  | TEXT      | NOT NULL                             | Sender agent UUID                  |
| to_uuid    | TEXT      | NOT NULL                             | Recipient agent UUID               |
| body       | TEXT      | NOT NULL                             | Message body                       |
| timestamp  | BIGINT    | NOT NULL                             | Unix epoch timestamp (seconds)     |
| read       | INTEGER   | NOT NULL, DEFAULT 0                  | Read status (0=unread, 1=read)     |

**Indexes:**
- `idx_mail_recipient`: `(session_id, to_uuid, read)` for inbox queries

**Design notes:**
- Mail is scoped to session (deleted when session is deleted)
- No foreign key on from_uuid/to_uuid (allows messaging dead agents)
- Read status is INTEGER for PostgreSQL compatibility

## Key Types

### ik_db_ctx_t
Database context managing PostgreSQL connection lifecycle.
```c
typedef struct {
    PGconn *conn;  // PostgreSQL connection handle
} ik_db_ctx_t;
```
- Memory: Allocated as child of caller's talloc context
- Destructor: Automatically calls `PQfinish()` on conn
- Cleanup: Single `talloc_free()` on parent releases everything

### ik_msg_t
Canonical message structure representing a single event.
```c
typedef struct {
    int64_t id;       // DB row ID (0 if not from DB)
    char *kind;       // Message kind discriminator
    char *content;    // Message text content or human-readable summary
    char *data_json;  // Structured data for tool messages (NULL for text messages)
} ik_msg_t;
```

**Conversation kinds** (included in LLM context):
- `system`, `user`, `assistant`, `tool_call`, `tool_result`, `tool`

**Metadata kinds** (not included in LLM context):
- `clear`, `mark`, `rewind`, `agent_killed`, `command`, `fork`, `usage`

### ik_replay_mark_t
Checkpoint information for conversation rollback.
```c
typedef struct {
    int64_t message_id;  // ID of the mark event
    char *label;         // User label or NULL
    size_t context_idx;  // Position in context array when mark was created
} ik_replay_mark_t;
```

### ik_replay_mark_stack_t
Dynamic array of checkpoint marks.
```c
typedef struct {
    ik_replay_mark_t *marks;  // Dynamic array of marks
    size_t count;             // Number of marks
    size_t capacity;          // Allocated capacity
} ik_replay_mark_stack_t;
```

### ik_replay_context_t
Dynamic array of messages representing conversation state with mark stack for rollback.
```c
typedef struct {
    ik_msg_t **messages;              // Dynamic array of message pointers (unified type)
    size_t count;                     // Number of messages in context
    size_t capacity;                  // Allocated capacity
    ik_replay_mark_stack_t mark_stack; // Stack of checkpoint marks
} ik_replay_context_t;
```
- Initial capacity: 16 messages
- Growth: Geometric (capacity *= 2)
- Memory: All structures allocated under parent talloc context

### ik_replay_range_t
Defines a subset of messages to query for agent-based replay.
```c
typedef struct {
    char *agent_uuid;   // Which agent's messages to query
    int64_t start_id;   // Start AFTER this message ID (0 = from beginning)
    int64_t end_id;     // End AT this message ID (0 = no limit, i.e., leaf)
} ik_replay_range_t;
```

**Semantics:**
- `start_id` is exclusive (query messages AFTER this ID)
- `end_id` is inclusive (query messages up to and including this ID)
- `end_id = 0` means "no upper limit" (used for leaf agent)

### ik_db_agent_row_t
Agent row structure for query results.
```c
typedef struct {
    char *uuid;
    char *name;
    char *parent_uuid;
    char *fork_message_id;
    char *status;
    int64_t created_at;
    int64_t ended_at;        // 0 if still running
    char *provider;          // LLM provider (nullable)
    char *model;             // Model identifier (nullable)
    char *thinking_level;    // Thinking budget/level (nullable)
} ik_db_agent_row_t;
```

### ik_mail_msg_t
Mail message structure for inter-agent messaging.
```c
typedef struct ik_mail_msg {
    int64_t id;
    char *from_uuid;
    char *to_uuid;
    char *body;
    int64_t timestamp;
    bool read;
} ik_mail_msg_t;
```

### ik_pg_result_wrapper_t
Wrapper for PGresult with automatic cleanup via talloc destructor.
```c
typedef struct {
    PGresult *pg_result;
} ik_pg_result_wrapper_t;
```
- Destructor automatically calls `PQclear()` when talloc context is freed

## Connection API

### ik_db_init
Initialize database connection with default migrations directory.
```c
res_t ik_db_init(TALLOC_CTX *ctx, const char *conn_str, ik_db_ctx_t **out_ctx);
```
- **Parameters:**
  - `ctx`: Talloc context for allocations (must not be NULL)
  - `conn_str`: PostgreSQL connection string (e.g., `postgresql://user:pass@host:port/dbname`)
  - `out_ctx`: Output parameter for database context (must not be NULL)
- **Returns:** `OK` with db_ctx on success, `ERR` on failure
- **Error Codes:** `ERR_INVALID_ARG`, `ERR_DB_CONNECT`, `ERR_DB_MIGRATE`
- **Behavior:** Establishes connection and runs migrations from `./share/ikigai/migrations/`

### ik_db_init_with_migrations
Initialize database connection with custom migrations directory.
```c
res_t ik_db_init_with_migrations(TALLOC_CTX *ctx, const char *conn_str,
                                  const char *migrations_dir, ik_db_ctx_t **out_ctx);
```
- **Parameters:**
  - `ctx`: Talloc context for allocations (must not be NULL)
  - `conn_str`: PostgreSQL connection string (must not be NULL or empty)
  - `migrations_dir`: Path to migrations directory (must not be NULL)
  - `out_ctx`: Output parameter for database context (must not be NULL)
- **Returns:** `OK` with db_ctx on success, `ERR` on failure
- **Error Codes:** `ERR_INVALID_ARG`, `ERR_DB_CONNECT`, `ERR_DB_MIGRATE`, `ERR_IO`

### ik_db_begin
Begin transaction.
```c
res_t ik_db_begin(ik_db_ctx_t *db_ctx);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Executes "BEGIN" to start a new transaction

### ik_db_commit
Commit transaction.
```c
res_t ik_db_commit(ik_db_ctx_t *db_ctx);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Executes "COMMIT" to commit the current transaction

### ik_db_rollback
Rollback transaction.
```c
res_t ik_db_rollback(ik_db_ctx_t *db_ctx);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Executes "ROLLBACK" to abort the current transaction

## Session API

### ik_db_session_create
Create a new session with started_at=NOW() and ended_at=NULL.
```c
res_t ik_db_session_create(ik_db_ctx_t *db_ctx, int64_t *session_id_out);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `session_id_out`: Output parameter for new session ID (must not be NULL)
- **Returns:** `OK` with session_id on success, `ERR` on failure

### ik_db_session_get_active
Get the most recent active session (ended_at IS NULL).
```c
res_t ik_db_session_get_active(ik_db_ctx_t *db_ctx, int64_t *session_id_out);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `session_id_out`: Output parameter for session ID (must not be NULL)
- **Returns:** `OK` with session_id (0 if none found), `ERR` on database failure
- **Behavior:** Returns 0 (not an error) if no active session exists

### ik_db_session_end
End a session by setting ended_at=NOW().
```c
res_t ik_db_session_end(ik_db_ctx_t *db_ctx, int64_t session_id);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `session_id`: Session ID to end (must be > 0)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Session will no longer be returned by `get_active`

## Message API

### ik_db_message_insert
Insert a message event into the database.
```c
res_t ik_db_message_insert(ik_db_ctx_t *db,
                            int64_t session_id,
                            const char *agent_uuid,
                            const char *kind,
                            const char *content,
                            const char *data_json);
```
- **Parameters:**
  - `db`: Database connection context (must not be NULL)
  - `session_id`: Session ID (must be positive, references sessions.id)
  - `agent_uuid`: Agent UUID (may be NULL for backward compatibility)
  - `kind`: Event kind string (must be valid kind)
  - `content`: Message content (may be NULL for clear events, empty string allowed)
  - `data_json`: JSONB data as JSON string (may be NULL)
- **Returns:** `OK` on success, `ERR` on failure (invalid params or database error)

### ik_db_message_is_valid_kind
Validate that a kind string is one of the allowed event kinds.
```c
bool ik_db_message_is_valid_kind(const char *kind);
```
- **Parameters:**
  - `kind`: The kind string to validate (may be NULL)
- **Returns:** true if kind is valid, false otherwise
- **Valid Kinds:** clear, system, user, assistant, tool_call, tool_result, mark, rewind, agent_killed, command, fork, usage

### ik_msg_create_tool_result
Create a canonical tool result message with kind="tool_result".
```c
ik_msg_t *ik_msg_create_tool_result(void *parent,
                                     const char *tool_call_id,
                                     const char *name,
                                     const char *output,
                                     bool success,
                                     const char *content);
```
- **Parameters:**
  - `parent`: Talloc context for allocation (can be NULL for root)
  - `tool_call_id`: Unique tool call ID (e.g., "call_abc123")
  - `name`: Tool name (e.g., "glob", "file_read")
  - `output`: Tool output string (can be empty string)
  - `success`: Whether the tool executed successfully (true/false)
  - `content`: Human-readable summary for the message (e.g., "3 files found")
- **Returns:** Allocated `ik_msg_t` struct (owned by parent), or NULL on OOM
- **Memory:** All fields are children of the message; single `talloc_free()` releases all

### ik_msg_is_conversation_kind
Check if a message kind should be included in LLM conversation context.
```c
bool ik_msg_is_conversation_kind(const char *kind);
```
- **Parameters:**
  - `kind`: Message kind string (e.g., "user", "assistant", "clear")
- **Returns:** true if kind should be sent to LLM, false otherwise
- **Conversation kinds:** system, user, assistant, tool_call, tool_result, tool
- **Metadata kinds:** clear, mark, rewind, agent_killed, command, fork

## Agent API

### ik_db_agent_insert
Insert agent into registry.
```c
res_t ik_db_agent_insert(ik_db_ctx_t *db_ctx, const ik_agent_ctx_t *agent);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `agent`: Agent context with uuid, parent_uuid, created_at set (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Inserts agent with status='running', created_at=NOW()

### ik_db_agent_mark_dead
Mark agent as dead.
```c
res_t ik_db_agent_mark_dead(ik_db_ctx_t *db_ctx, const char *uuid);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `uuid`: Agent UUID to update (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Updates status to 'dead', sets ended_at. Idempotent (marking dead agent is no-op).

### ik_db_agent_get
Lookup agent by UUID.
```c
res_t ik_db_agent_get(ik_db_ctx_t *db_ctx, TALLOC_CTX *ctx,
                      const char *uuid, ik_db_agent_row_t **out);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `uuid`: Agent UUID to lookup (must not be NULL)
  - `out`: Output parameter for agent row (must not be NULL)
- **Returns:** `OK` with agent row on success, `ERR` if not found or on failure

### ik_db_agent_list_running
List all running agents.
```c
res_t ik_db_agent_list_running(ik_db_ctx_t *db_ctx, TALLOC_CTX *ctx,
                               ik_db_agent_row_t ***out, size_t *count);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `out`: Output parameter for array of agent row pointers (must not be NULL)
  - `count`: Output parameter for array size (must not be NULL)
- **Returns:** `OK` with agent rows on success, `ERR` on failure
- **Behavior:** Returns all agents with status='running' ordered by created_at

### ik_db_agent_get_children
Get children of an agent.
```c
res_t ik_db_agent_get_children(ik_db_ctx_t *db_ctx, TALLOC_CTX *ctx,
                               const char *parent_uuid,
                               ik_db_agent_row_t ***out, size_t *count);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `parent_uuid`: Parent agent UUID (must not be NULL)
  - `out`: Output parameter for array of agent row pointers (must not be NULL)
  - `count`: Output parameter for array size (must not be NULL)
- **Returns:** `OK` with agent rows on success, `ERR` on failure
- **Behavior:** Returns all agents whose parent_uuid matches, ordered by created_at

### ik_db_agent_get_parent
Get parent agent.
```c
res_t ik_db_agent_get_parent(ik_db_ctx_t *db_ctx, TALLOC_CTX *ctx,
                              const char *uuid, ik_db_agent_row_t **out);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `uuid`: Child agent UUID (must not be NULL)
  - `out`: Output parameter for parent agent row (must not be NULL)
- **Returns:** `OK` with parent row (or NULL for root) on success, `ERR` on failure
- **Behavior:** Retrieves parent record for ancestry chain walking. Sets *out to NULL if agent has no parent.

### ik_db_ensure_agent_zero
Ensure Agent 0 exists in registry.
```c
res_t ik_db_ensure_agent_zero(ik_db_ctx_t *db, char **out_uuid);
```
- **Parameters:**
  - `db`: Database context (must not be NULL)
  - `out_uuid`: Output parameter for Agent 0's UUID (must not be NULL)
- **Returns:** `OK` with UUID on success, `ERR` on failure
- **Behavior:** Called once during ik_repl_init(). Creates Agent 0 if missing, retrieves UUID if present. On upgrade: if messages exist but no agents, creates Agent 0 and adopts orphan messages.

### ik_db_agent_get_last_message_id
Get the last message ID for an agent.
```c
res_t ik_db_agent_get_last_message_id(ik_db_ctx_t *db_ctx, const char *agent_uuid,
                                       int64_t *out_message_id);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `agent_uuid`: Agent UUID (must not be NULL)
  - `out_message_id`: Output parameter for last message ID (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Returns maximum message ID for agent. Used during fork to record fork point. Returns 0 if agent has no messages.

### ik_db_agent_update_provider
Update agent provider configuration.
```c
res_t ik_db_agent_update_provider(ik_db_ctx_t *db_ctx, const char *uuid,
                                   const char *provider, const char *model,
                                   const char *thinking_level);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `uuid`: Agent UUID to update (must not be NULL)
  - `provider`: Provider name (may be NULL)
  - `model`: Model identifier (may be NULL)
  - `thinking_level`: Thinking budget/level (may be NULL)
- **Returns:** `OK` on success, `ERR_DB_CONNECT` on database error
- **Behavior:** Updates provider, model, and thinking_level atomically. NULL values clear the configuration. Returns OK if agent not found (UPDATE affects 0 rows).

## Mail API

### ik_db_mail_insert
Insert mail message (sets msg->id on success).
```c
res_t ik_db_mail_insert(ik_db_ctx_t *db, int64_t session_id,
                        ik_mail_msg_t *msg);
```
- **Parameters:**
  - `db`: Database context (must not be NULL)
  - `session_id`: Session ID (must be positive)
  - `msg`: Mail message (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Inserts mail message, sets msg->id to the new row ID

### ik_db_mail_inbox
Get inbox for agent (unread first, then by timestamp desc).
```c
res_t ik_db_mail_inbox(ik_db_ctx_t *db, TALLOC_CTX *ctx,
                       int64_t session_id, const char *to_uuid,
                       ik_mail_msg_t ***out, size_t *count);
```
- **Parameters:**
  - `db`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `session_id`: Session ID (must be positive)
  - `to_uuid`: Recipient agent UUID (must not be NULL)
  - `out`: Output parameter for array of mail message pointers (must not be NULL)
  - `count`: Output parameter for array size (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Returns all mail for recipient, ordered by read status (unread first), then timestamp desc

### ik_db_mail_inbox_filtered
Get filtered inbox by sender (unread first, then by timestamp desc).
```c
res_t ik_db_mail_inbox_filtered(ik_db_ctx_t *db, TALLOC_CTX *ctx,
                                int64_t session_id, const char *to_uuid,
                                const char *from_uuid,
                                ik_mail_msg_t ***out, size_t *count);
```
- **Parameters:**
  - `db`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `session_id`: Session ID (must be positive)
  - `to_uuid`: Recipient agent UUID (must not be NULL)
  - `from_uuid`: Sender agent UUID filter (must not be NULL)
  - `out`: Output parameter for array of mail message pointers (must not be NULL)
  - `count`: Output parameter for array size (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Returns mail from specific sender, ordered by read status, then timestamp desc

### ik_db_mail_mark_read
Mark message as read.
```c
res_t ik_db_mail_mark_read(ik_db_ctx_t *db, int64_t mail_id);
```
- **Parameters:**
  - `db`: Database context (must not be NULL)
  - `mail_id`: Mail message ID (must be positive)
- **Returns:** `OK` on success, `ERR` on failure

### ik_db_mail_delete
Delete message (validates recipient owns the message).
```c
res_t ik_db_mail_delete(ik_db_ctx_t *db, int64_t mail_id,
                        const char *recipient_uuid);
```
- **Parameters:**
  - `db`: Database context (must not be NULL)
  - `mail_id`: Mail message ID (must be positive)
  - `recipient_uuid`: Recipient agent UUID (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** Validates that recipient_uuid matches to_uuid before deleting

### ik_mail_msg_create
Create a mail message structure.
```c
ik_mail_msg_t *ik_mail_msg_create(TALLOC_CTX *ctx,
                                   const char *from_uuid,
                                   const char *to_uuid,
                                   const char *body);
```
- **Parameters:**
  - `ctx`: Talloc context for allocation
  - `from_uuid`: Sender agent UUID
  - `to_uuid`: Recipient agent UUID
  - `body`: Message body
- **Returns:** Allocated mail message structure

## Replay API

### ik_db_messages_load
Load messages from database and replay to build conversation context (TEST-ONLY).
```c
res_t ik_db_messages_load(TALLOC_CTX *ctx, ik_db_ctx_t *db_ctx, int64_t session_id, ik_logger_t *logger);
```
- **Parameters:**
  - `ctx`: Talloc context for allocations (must not be NULL)
  - `db_ctx`: Database connection context (must not be NULL)
  - `session_id`: Session ID to load messages for (must be positive)
  - `logger`: Logger instance (may be NULL)
- **Returns:** `OK` with `ik_replay_context_t*` on success, `ERR` on failure
- **Behavior:**
  - TEST-ONLY: Queries by session_id only, does not support agent-based replay
  - Production code should use `ik_agent_replay_history()` instead
  - Queries messages table ordered by `created_at`
  - Processes events to build conversation context:
    - `clear`: Empty context (set count = 0)
    - `system`/`user`/`assistant`/`tool_call`/`tool_result`: Append to context array
    - `mark`: Append to context and push mark onto mark stack
    - `rewind`: Truncate context to target mark's position, append rewind event
  - Uses geometric growth (capacity *= 2) for dynamic arrays
  - Initial capacity: 16 messages

## Agent Replay API

### ik_agent_find_clear
Find most recent clear event for an agent.
```c
res_t ik_agent_find_clear(ik_db_ctx_t *db_ctx, TALLOC_CTX *ctx,
                          const char *agent_uuid, int64_t max_id,
                          int64_t *clear_id_out);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `ctx`: Talloc context for error allocation (must not be NULL)
  - `agent_uuid`: Agent UUID to search (must not be NULL)
  - `max_id`: Maximum message ID to consider (0 = no limit)
  - `clear_id_out`: Output for clear message ID (0 if not found)
- **Returns:** `OK` on success, `ERR` on database failure

### ik_agent_build_replay_ranges
Build replay ranges by walking ancestor chain.
```c
res_t ik_agent_build_replay_ranges(ik_db_ctx_t *db_ctx, TALLOC_CTX *ctx,
                                    const char *agent_uuid,
                                    ik_replay_range_t **ranges_out,
                                    size_t *count_out);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `agent_uuid`: Leaf agent UUID to start from (must not be NULL)
  - `ranges_out`: Output for array of replay ranges (must not be NULL)
  - `count_out`: Output for number of ranges (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Algorithm:** "Walk backwards, play forwards"
  1. Start at leaf agent, end_id=0
  2. For each agent, find most recent clear (within range)
  3. If clear found: add range starting after clear, terminate walk
  4. If no clear: add range from beginning, continue to parent
  5. Reverse array for chronological order (root first)

### ik_agent_query_range
Query messages for a single replay range.
```c
res_t ik_agent_query_range(ik_db_ctx_t *db_ctx, TALLOC_CTX *ctx,
                            const ik_replay_range_t *range,
                            ik_msg_t ***messages_out,
                            size_t *count_out);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `range`: Replay range specification (must not be NULL)
  - `messages_out`: Output for array of message pointers (must not be NULL)
  - `count_out`: Output for number of messages (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Query:** `WHERE agent_uuid=$1 AND id>$2 AND ($3=0 OR id<=$3)`

### ik_agent_replay_history
Replay history for an agent using range-based algorithm.
```c
res_t ik_agent_replay_history(ik_db_ctx_t *db_ctx, TALLOC_CTX *ctx,
                               const char *agent_uuid,
                               ik_replay_context_t **ctx_out);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `ctx`: Talloc context for result allocation (must not be NULL)
  - `agent_uuid`: Agent UUID to replay (must not be NULL)
  - `ctx_out`: Output for replay context (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Behavior:** High-level function that combines `build_replay_ranges` and `query_range` to reconstruct agent's full conversation context on startup

## Migration System

### ik_db_migrate
Apply all pending database migrations from specified directory.
```c
res_t ik_db_migrate(ik_db_ctx_t *db_ctx, const char *migrations_dir);
```
- **Parameters:**
  - `db_ctx`: Database context (must not be NULL)
  - `migrations_dir`: Path to migrations directory (must not be NULL)
- **Returns:** `OK` on success, `ERR` on failure
- **Error Codes:** `ERR_INVALID_ARG`, `ERR_IO`, `ERR_DB_MIGRATE`

### Migration Algorithm
1. Query current schema version from `schema_metadata` table (0 if table doesn't exist)
2. Scan migrations directory for `.sql` files
3. Parse migration numbers from filenames (e.g., `001-initial-schema.sql` → 1)
4. Sort migrations by number
5. Filter to pending migrations (number > current_version)
6. For each pending migration:
   - Read SQL file contents
   - Execute SQL via `PQexec()` within transaction
   - Check for errors (rollback on failure)
   - Continue to next migration on success

### Migration File Format
- **Naming:** `NNN-description.sql` (e.g., `001-initial-schema.sql`, `002-agents-table.sql`)
- **Content:** Valid SQL with `BEGIN`/`COMMIT` for atomicity
- **Version Update:** Each migration must update `schema_metadata.schema_version`
- **Idempotency:** Safe to run multiple times; already-applied migrations are skipped

### Current Migrations
- **001-initial-schema.sql**: Creates `schema_metadata`, `sessions`, and `messages` tables with indexes
- **002-agents-table.sql**: Creates `agents` table with agent_status enum, parent_uuid FK, and indexes
- **003-messages-agent-uuid.sql**: Adds `agent_uuid` column to messages table with FK and index
- **004-mail-table.sql**: Creates `mail` table for inter-agent messaging with indexes
- **005-multi-provider.sql**: Adds `provider`, `model`, and `thinking_level` columns to agents table for multi-provider support; truncates all tables for clean slate

## PGresult Memory Management

**CRITICAL:** NEVER call `PQclear()` manually. Always wrap with `ik_db_wrap_pg_result()`.

### ik_db_wrap_pg_result
Wrap PGresult with automatic cleanup via talloc destructor.
```c
ik_pg_result_wrapper_t *ik_db_wrap_pg_result(TALLOC_CTX *ctx, PGresult *pg_res);
```
- **Parameters:**
  - `ctx`: Parent talloc context
  - `pg_res`: PGresult to wrap (may be NULL)
- **Returns:** Wrapper object (never NULL - panics on allocation failure)
- **Usage:** Wrap all `PQexec()` and `PQexecParams()` results to prevent leaks
- **Cleanup:** Destructor automatically calls `PQclear()` when parent talloc context is freed

**Usage pattern:**
```c
// Wrap immediately after PQexec/PQexecParams
ik_pg_result_wrapper_t *wrapper = ik_db_wrap_pg_result(tmp_ctx, PQexec(conn, query));
PGresult *res = wrapper->pg_result;

// Use normally - no manual cleanup needed
if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    talloc_free(tmp_ctx);  // Destructor calls PQclear() automatically
    return ERR(...);
}
```

This integrates PGresult (malloc-based) with talloc's hierarchical memory model.

## Testing Patterns

### Test Isolation Pattern A (Transaction-based)
Most tests use transaction isolation for speed:
```c
static const char *DB_NAME;
static ik_db_ctx_t *db;
static TALLOC_CTX *test_ctx;

// Suite setup (once per file)
DB_NAME = ik_test_db_name(NULL, __FILE__);
ik_test_db_create(DB_NAME);
ik_test_db_migrate(NULL, DB_NAME);

// Per-test setup
test_ctx = talloc_new(NULL);
ik_test_db_connect(test_ctx, DB_NAME, &db);
ik_test_db_begin(db);

// Per-test teardown
ik_test_db_rollback(db);
talloc_free(test_ctx);

// Suite teardown (once per file)
ik_test_db_destroy(DB_NAME);
```

**Rolemodel:** `tests/unit/repl/repl_actions_db_basic_test.c`

**Key benefits:**
- Parallel execution across test files (separate DBs)
- Fast isolation within a file (transaction rollback)
- Idempotent - works regardless of previous state

### Test Isolation Pattern B (Empty database)
Migration tests use empty database without migrations:
```c
DB_NAME = ik_test_db_name(NULL, __FILE__);
ik_test_db_create(DB_NAME);  // No migrate call
// ... test migration logic ...
ik_test_db_destroy(DB_NAME);
```

### Key Test Functions

#### ik_test_db_name
Derive database name from source file path.
```c
const char *ik_test_db_name(TALLOC_CTX *ctx, const char *file_path);
```
- Example: `tests/unit/db/session_test.c` → `ikigai_test_session_test`

#### ik_test_db_create
Create test database (drops if exists).
```c
res_t ik_test_db_create(const char *db_name);
```
- Idempotent: Safe to call regardless of previous state
- Uses admin database connection to drop/create

#### ik_test_db_migrate
Run migrations on test database from `./share/ikigai/migrations/` directory.
```c
res_t ik_test_db_migrate(TALLOC_CTX *ctx, const char *db_name);
```

#### ik_test_db_connect
Open connection to test database (no migrations).
```c
res_t ik_test_db_connect(TALLOC_CTX *ctx, const char *db_name, ik_db_ctx_t **out);
```

#### ik_test_db_begin
Begin transaction for test isolation.
```c
res_t ik_test_db_begin(ik_db_ctx_t *db);
```

#### ik_test_db_rollback
Rollback transaction to discard test changes.
```c
res_t ik_test_db_rollback(ik_db_ctx_t *db);
```

#### ik_test_db_truncate_all
Truncate all application tables (for non-transactional tests).
```c
res_t ik_test_db_truncate_all(ik_db_ctx_t *db);
```
- Executes: `TRUNCATE TABLE messages, sessions, agents, mail RESTART IDENTITY CASCADE`

#### ik_test_db_destroy
Drop test database completely.
```c
res_t ik_test_db_destroy(const char *db_name);
```

## Test Database Configuration

**Fixed configuration** - hardcoded in `tests/test_utils.c`:
- **User**: `ikigai`
- **Password**: `ikigai`
- **Host**: `localhost` (override with `PGHOST` environment variable)
- **Admin DB**: `postgres` (for CREATE/DROP DATABASE operations)
- **Test DBs**: Per-file databases named `ikigai_test_<basename>`

**Connection strings:**
```c
ADMIN_DB_URL = "postgresql://ikigai:ikigai@localhost/postgres"
TEST_DB_URL_PREFIX = "postgresql://ikigai:ikigai@localhost/"
```

**Database setup requirements:**
1. PostgreSQL server running on localhost
2. User `ikigai` with password `ikigai` created
3. User must have CREATEDB privilege (for creating test databases)
4. No need to pre-create test databases (created/destroyed per test file)

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Production connection string |
| `PGHOST` | Override PostgreSQL host (default: localhost) |
| `SKIP_LIVE_DB_TESTS` | Set to `1` to skip DB tests |

## Key Files

| File | Purpose |
|------|---------|
| `share/ikigai/migrations/001-initial-schema.sql` | Initial database schema with sessions and messages tables |
| `share/ikigai/migrations/002-agents-table.sql` | Agent registry table with parent-child relationships |
| `share/ikigai/migrations/003-messages-agent-uuid.sql` | Add agent_uuid column to messages table |
| `share/ikigai/migrations/004-mail-table.sql` | Inter-agent mail table for message passing |
| `share/ikigai/migrations/005-multi-provider.sql` | Add provider, model, thinking_level to agents table |
| `src/db/connection.h` | Database connection API (init, destructor, transactions) |
| `src/db/connection.c` | Connection implementation with validation and migration runner |
| `src/db/session.h` | Session CRUD API (create, get_active, end) |
| `src/db/session.c` | Session implementation with parameterized queries |
| `src/db/message.h` | Message insertion API and tool result helpers |
| `src/db/message.c` | Message implementation with kind validation and yyjson |
| `src/db/agent.h` | Agent registry API (insert, mark_dead, queries, update_provider) |
| `src/db/agent.c` | Agent implementation with parent-child queries |
| `src/db/agent_row.h` | Agent row parsing helper API |
| `src/db/agent_row.c` | Agent row parsing from PGresult |
| `src/db/agent_zero.h` | Agent 0 (root agent) creation API |
| `src/db/agent_zero.c` | Agent 0 creation and orphan message adoption |
| `src/db/mail.h` | Mail API (insert, inbox, mark_read, delete) |
| `src/db/mail.c` | Mail implementation with inbox filtering |
| `src/db/replay.h` | Replay context structures and message loading API |
| `src/db/replay.c` | Event stream replay algorithm with mark/rewind support |
| `src/db/agent_replay.h` | Agent-based replay API (find_clear, build_ranges, query_range) |
| `src/db/agent_replay.c` | Agent replay implementation with ancestry chain walking |
| `src/db/migration.h` | Migration system API |
| `src/db/migration.c` | Migration scanner, parser, and executor |
| `src/db/pg_result.h` | PGresult wrapper API |
| `src/db/pg_result.c` | PGresult wrapper implementation with talloc destructor |
| `src/msg.h` | Canonical message structure and kind validation |
| `src/mail/msg.h` | Mail message structure |
| `tests/test_utils.h` | Database test utilities header |
| `tests/test_utils.c` | Database test utilities implementation |
| `tests/unit/test_utils/db_test.c` | DB test utilities tests |

## Related Skills

- `memory` - talloc-based memory management and ownership rules
- `errors` - Result types with OK()/ERR() patterns
- `source-code` - Map of all src/*.c files by functional area
