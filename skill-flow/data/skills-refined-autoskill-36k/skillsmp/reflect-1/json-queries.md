# JSON Query Patterns

Working with the `message` JSON field in base views. See SKILL.md for JSON syntax basics and gotchas.

## Message JSON Structure

### Assistant Messages

```json
{
  "id": "msg_01GC7S5QXPz4Cj5QJVwk7nkW",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-4-5-20251101",
  "content": [...],
  "stop_reason": "end_turn|tool_use|max_tokens",
  "usage": {
    "input_tokens": 2,
    "output_tokens": 155,
    "cache_read_input_tokens": 0
  }
}
```

### Content Block Types

**Text block:**
```json
{"type": "text", "text": "The response..."}
```

**Tool use block:**
```json
{"type": "tool_use", "id": "toolu_019...", "name": "Read", "input": {"file_path": "/path/to/file"}}
```

**Thinking block:**
```json
{"type": "thinking", "thinking": "Reasoning...", "signature": "base64..."}
```

### User Messages (tool results)

```json
{
  "role": "user",
  "content": [
    {"type": "tool_result", "tool_use_id": "toolu_014...", "content": "output...", "is_error": false}
  ]
}
```

## Working with Content Arrays

### Extract first content block

```sql
SELECT message->'content'->0 as first_block FROM assistant_messages LIMIT 1;
```

### Expand all content blocks with UNNEST

```sql
SELECT timestamp, block->>'type' as block_type, block->>'name' as tool_name
FROM assistant_messages,
LATERAL UNNEST(CAST(message->'content' AS JSON[])) as t(block)
WHERE block->>'type' = 'tool_use'
LIMIT 20;
```

### Find thinking blocks

```sql
SELECT timestamp, left(block->>'thinking', 200) as thinking_preview
FROM assistant_messages,
LATERAL UNNEST(CAST(message->'content' AS JSON[])) as t(block)
WHERE block->>'type' = 'thinking'
LIMIT 5;
```

### Tool results with UNNEST (requires CTE)

```sql
WITH array_msgs AS (
  SELECT * FROM user_messages WHERE json_type(message->'content') = 'ARRAY'
)
SELECT timestamp, block->>'tool_use_id' as tool_id,
       CAST(block->>'is_error' AS BOOLEAN) as is_error,
       left(block->>'content', 100) as result_preview
FROM array_msgs,
LATERAL UNNEST(CAST(message->'content' AS JSON[])) as t(block)
WHERE block->>'type' = 'tool_result'
LIMIT 10;
```

## Common Patterns

### Get model usage breakdown

```sql
SELECT message->>'model' as model, count(*) as messages,
       sum(CAST(message->'usage'->>'output_tokens' AS BIGINT)) as total_output
FROM assistant_messages GROUP BY model ORDER BY messages DESC;
```

### Count by stop reason

```sql
SELECT message->>'stop_reason' as reason, count(*) as cnt
FROM assistant_messages GROUP BY reason ORDER BY cnt DESC;
```

### Get tool input parameters

```sql
SELECT timestamp, message->'content'->0->>'name' as tool,
       message->'content'->0->'input' as input
FROM assistant_messages
WHERE message->>'stop_reason' = 'tool_use'
ORDER BY timestamp DESC LIMIT 5;
```

### Link tool results to tool calls

```sql
SELECT u.timestamp as result_time, a.timestamp as call_time,
       a.message->'content'->0->>'name' as tool_name,
       CAST(u.toolUseResult->>'durationMs' AS INTEGER) as duration_ms
FROM user_messages u
JOIN assistant_messages a ON u.sourceToolAssistantUUID = a.uuid
WHERE u.toolUseResult IS NOT NULL
ORDER BY u.timestamp DESC LIMIT 10;
```
