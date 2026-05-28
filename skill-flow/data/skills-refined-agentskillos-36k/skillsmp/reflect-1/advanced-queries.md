# Advanced Query Patterns

You have the full power of DuckDB available. Use it and be creative! Here are some example queries.

## Activity Analysis

### Coding Activity by Hour

```sql
SELECT extract(hour FROM timestamp) as hour, count(*) as messages,
       repeat('█', (count(*) * 30 / max(count(*)) OVER ())::INT) as activity
FROM messages GROUP BY hour ORDER BY hour;
```

### Token Efficiency Over Time

```sql
SELECT CAST(timestamp AS DATE) as day,
       sum(CAST(message->'usage'->>'output_tokens' AS BIGINT)) as output_tokens,
       count(*) FILTER (WHERE type = 'user') as user_msgs,
       round(sum(CAST(message->'usage'->>'output_tokens' AS BIGINT))::FLOAT /
             nullif(count(*) FILTER (WHERE type = 'user'), 0), 0) as tokens_per_user_msg
FROM messages WHERE CAST(timestamp AS DATE) >= current_date - INTERVAL '14 days'
GROUP BY day ORDER BY day;
```

### Session Size Distribution

```sql
SELECT
  CASE
    WHEN cnt <= 10 THEN '1-10 messages'
    WHEN cnt <= 50 THEN '11-50 messages'
    WHEN cnt <= 100 THEN '51-100 messages'
    WHEN cnt <= 200 THEN '101-200 messages'
    ELSE '200+ messages'
  END as session_size,
  count(*) as sessions,
  repeat('█', (count(*) * 20 / max(count(*)) OVER ())::INT) as chart
FROM (SELECT sessionId, count(*) as cnt FROM messages GROUP BY sessionId)
GROUP BY session_size ORDER BY session_size;
```

## Tool Analysis

### Tool Chains: What Follows What?

```sql
WITH tool_sequence AS (
  SELECT timestamp, sessionId, message->'content'->0->>'name' as tool,
         LAG(message->'content'->0->>'name') OVER (PARTITION BY sessionId ORDER BY timestamp) as prev_tool
  FROM assistant_messages WHERE message->>'stop_reason' = 'tool_use'
)
SELECT prev_tool || ' -> ' || tool as chain, count(*) as cnt
FROM tool_sequence
WHERE prev_tool IS NOT NULL AND tool IS NOT NULL AND prev_tool != '' AND tool != ''
GROUP BY chain ORDER BY cnt DESC LIMIT 10;
```

### Most Edited Files

```sql
SELECT message->'content'->0->'input'->>'file_path' as file, count(*) as edits
FROM assistant_messages
WHERE message->>'stop_reason' = 'tool_use' AND message->'content'->0->>'name' = 'Edit'
GROUP BY file ORDER BY edits DESC LIMIT 10;
```

### Agent Types Spawned

```sql
SELECT message->'content'->0->'input'->>'subagent_type' as agent_type, count(*) as spawns
FROM assistant_messages
WHERE message->>'stop_reason' = 'tool_use' AND message->'content'->0->>'name' = 'Task'
GROUP BY agent_type ORDER BY spawns DESC;
```

### Tool Result Duration Analysis

```sql
SELECT message->'content'->0->>'tool_use_id' as tool_id,
       CAST(toolUseResult->>'durationMs' AS INTEGER) as duration_ms,
       toolUseResult->>'truncated' as truncated
FROM user_messages WHERE toolUseResult IS NOT NULL
ORDER BY duration_ms DESC LIMIT 10;
```

## Cache & Performance

### Cache Efficiency

```sql
SELECT CAST(timestamp AS DATE) as day,
       sum(CAST(message->'usage'->>'input_tokens' AS BIGINT)) as input_tokens,
       sum(CAST(message->'usage'->>'cache_read_input_tokens' AS BIGINT)) as cache_hits,
       round(sum(CAST(message->'usage'->>'cache_read_input_tokens' AS BIGINT))::FLOAT * 100.0 /
             nullif(sum(CAST(message->'usage'->>'input_tokens' AS BIGINT)) +
                    sum(CAST(message->'usage'->>'cache_read_input_tokens' AS BIGINT)), 0), 1) as cache_hit_pct
FROM assistant_messages WHERE CAST(timestamp AS DATE) >= current_date - INTERVAL '7 days'
GROUP BY day ORDER BY day;
```

### Thinking Block Analysis

```sql
SELECT message->>'stop_reason' as outcome,
       round(avg(length(block->>'thinking')), 0) as avg_thinking_len, count(*) as cnt
FROM assistant_messages,
LATERAL UNNEST(CAST(message->'content' AS JSON[])) as t(block)
WHERE block->>'type' = 'thinking'
GROUP BY outcome ORDER BY avg_thinking_len DESC;
```

## Cross-Project Analysis

### Cross-Project Comparison

```sql
SELECT project, count(*) as messages,
       count(*) FILTER (WHERE type = 'assistant' AND message->>'stop_reason' = 'tool_use') as tool_uses,
       round(count(*) FILTER (WHERE type = 'assistant' AND message->>'stop_reason' = 'tool_use')::FLOAT * 100.0 /
             nullif(count(*) FILTER (WHERE type = 'assistant'), 0), 1) as tool_use_pct,
       sum(CAST(message->'usage'->>'output_tokens' AS BIGINT)) as total_tokens
FROM messages GROUP BY project ORDER BY messages DESC;
```
