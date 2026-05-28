#!/usr/bin/env bash
# Complete session summary query
# Usage: ./session-summary.sh <session_id>
#   or:  CLAUDE_SESSION_ID=xxx ./session-summary.sh

SESSION_ID="${1:-$CLAUDE_SESSION_ID}"

if [[ -z "$SESSION_ID" ]]; then
  echo "Error: Session ID required (pass as argument or set CLAUDE_SESSION_ID)" >&2
  exit 1
fi

cat << 'EOF' | ${CLAUDE_PLUGIN_ROOT}/bin/cc-query -s "$SESSION_ID"
-- 1. Session Stats (key/value)
WITH overview AS (
  SELECT
    count(*) as total_messages,
    count(DISTINCT agentId) FILTER (WHERE agentId IS NOT NULL) as agent_count,
    min(timestamp) as started,
    max(timestamp) as ended,
    date_diff('minute', min(timestamp), max(timestamp)) as duration_minutes,
    max(cwd) as working_directory,
    max(project) as project_name
  FROM messages
),
tokens AS (
  SELECT
    sum(input_tokens) as input_tokens,
    sum(output_tokens) as output_tokens,
    sum(cache_read_tokens) as cache_read_tokens
  FROM token_usage
),
agents AS (
  SELECT string_agg(agentId || ' (' || cnt || ' msgs)', ', ') as agent_summary
  FROM (
    SELECT agentId, count(*) as cnt
    FROM messages
    WHERE isAgent = true AND agentId IS NOT NULL
    GROUP BY agentId
    ORDER BY min(timestamp) ASC
  )
),
final_todos AS (
  SELECT replace(replace(todos::VARCHAR, chr(10), '\\n'), chr(13), '') as todos_json
  FROM user_messages
  WHERE todos IS NOT NULL
  ORDER BY timestamp DESC LIMIT 1
)
SELECT key, value FROM (
  SELECT 1 as ord, 'total_messages' as key, total_messages::VARCHAR as value FROM overview
  UNION ALL SELECT 2, 'duration_minutes', duration_minutes::VARCHAR FROM overview
  UNION ALL SELECT 3, 'started', started::VARCHAR FROM overview
  UNION ALL SELECT 4, 'ended', ended::VARCHAR FROM overview
  UNION ALL SELECT 5, 'working_directory', working_directory FROM overview
  UNION ALL SELECT 6, 'project', project_name FROM overview
  UNION ALL SELECT 7, 'input_tokens', input_tokens::VARCHAR FROM tokens
  UNION ALL SELECT 8, 'output_tokens', output_tokens::VARCHAR FROM tokens
  UNION ALL SELECT 9, 'cache_read_tokens', cache_read_tokens::VARCHAR FROM tokens
  UNION ALL SELECT 10, 'agent_count', agent_count::VARCHAR FROM overview
  UNION ALL SELECT 11, 'agents', agent_summary FROM agents
  UNION ALL SELECT 12, 'final_todos', todos_json FROM final_todos
)
ORDER BY ord;

-- 2. Files Touched
SELECT
  file_path,
  concat(
    CASE WHEN count(*) FILTER (WHERE tool_name = 'Read') > 0 THEN 'r' ELSE '' END,
    CASE WHEN count(*) FILTER (WHERE tool_name = 'Write') > 0 THEN 'w' ELSE '' END,
    CASE WHEN count(*) FILTER (WHERE tool_name = 'Edit') > 0 THEN 'e' ELSE '' END
  ) as ops,
  count(*) as total
FROM file_operations
WHERE file_path IS NOT NULL
GROUP BY file_path
ORDER BY total DESC;

-- 3. Timeline (messages and tools unified)
WITH assistant_array_msgs AS (
  SELECT * FROM assistant_messages
  WHERE json_type(message->'content') = 'ARRAY'
)
SELECT strftime(timestamp, '%m-%d %H:%M:%S') as timestamp, id, type, len,
       replace(replace(detail, chr(10), '\\n'), chr(13), '') as detail
FROM (
  -- Human messages
  SELECT timestamp, left(uuid::VARCHAR, 8) as id, 'human' as type,
         length(content) as len,
         CASE WHEN length(content) > 300 THEN left(content, 300) || '...[TRUNCATED]'
              ELSE content END as detail
  FROM human_messages

  UNION ALL

  -- Assistant thinking
  SELECT m.timestamp, left(m.uuid::VARCHAR, 8) as id, 'thinking' as type,
         length(block->>'thinking') as len,
         CASE WHEN length(block->>'thinking') > 300 THEN left(block->>'thinking', 300) || '...[TRUNCATED]'
              ELSE block->>'thinking' END as detail
  FROM assistant_array_msgs m,
  LATERAL UNNEST(CAST(m.message->'content' AS JSON[])) as t(block)
  WHERE block->>'type' = 'thinking'

  UNION ALL

  -- Assistant text responses
  SELECT m.timestamp, left(m.uuid::VARCHAR, 8) as id, 'assistant' as type,
         length(block->>'text') as len,
         CASE WHEN length(block->>'text') > 300 THEN left(block->>'text', 300) || '...[TRUNCATED]'
              ELSE block->>'text' END as detail
  FROM assistant_array_msgs m,
  LATERAL UNNEST(CAST(m.message->'content' AS JSON[])) as t(block)
  WHERE block->>'type' = 'text'
    AND length(block->>'text') > 50

  UNION ALL

  -- All tool calls with tiered detail
  SELECT tu.timestamp, tu.tool_id as id, lower(tu.tool_name) as type,
         CASE
           WHEN tu.tool_name = 'Bash' THEN COALESCE(length(tu.tool_input->>'command'), 0) + COALESCE(length(tr.result_content), 0)
           WHEN tu.tool_name = 'Write' THEN length(tu.tool_input->>'content')
           WHEN tu.tool_name = 'Edit' THEN COALESCE(length(tu.tool_input->>'old_string'), 0) + COALESCE(length(tu.tool_input->>'new_string'), 0)
           WHEN tu.tool_name = 'Read' THEN length(tr.result_content)
           WHEN tu.tool_name = 'Task' THEN length(tu.tool_input->>'prompt')
           ELSE NULL
         END as len,
         CASE
           -- Rich: Bash
           WHEN tu.tool_name = 'Bash' THEN
             CASE WHEN tr.is_error THEN '[ERR] ' ELSE '' END ||
             CASE WHEN length(tu.tool_input->>'command') > 100 THEN left(tu.tool_input->>'command', 100) || '...[TRUNCATED]' ELSE tu.tool_input->>'command' END ||
             ' → ' ||
             CASE WHEN tr.result_content IS NULL THEN '(no output)'
                  WHEN length(tr.result_content) > 150 THEN left(tr.result_content, 150) || '...[TRUNCATED]'
                  ELSE tr.result_content END
           -- Rich: Write
           WHEN tu.tool_name = 'Write' THEN
             tu.tool_input->>'file_path' || ' | ' ||
             CASE WHEN tr.is_error THEN '[ERR] ' || left(tr.result_content, 200) || '...[TRUNCATED]'
                  WHEN length(tu.tool_input->>'content') > 200 THEN left(tu.tool_input->>'content', 200) || '...[TRUNCATED]'
                  ELSE tu.tool_input->>'content' END
           -- Rich: Edit
           WHEN tu.tool_name = 'Edit' THEN
             tu.tool_input->>'file_path' ||
             CASE WHEN tr.is_error THEN ' | [ERR] ' || left(tr.result_content, 200) || '...[TRUNCATED]'
                  ELSE ' | old:' || COALESCE(
                    CASE WHEN length(tu.tool_input->>'old_string') > 100 THEN left(tu.tool_input->>'old_string', 100) || '...[TRUNCATED]'
                         ELSE tu.tool_input->>'old_string' END, '') ||
                       ' | new:' || COALESCE(
                    CASE WHEN length(tu.tool_input->>'new_string') > 100 THEN left(tu.tool_input->>'new_string', 100) || '...[TRUNCATED]'
                         ELSE tu.tool_input->>'new_string' END, '') END
           -- Medium: Read
           WHEN tu.tool_name = 'Read' THEN tu.tool_input->>'file_path'
           -- Medium: Glob
           WHEN tu.tool_name = 'Glob' THEN
             concat(COALESCE(tu.tool_input->>'path', ''), '/', tu.tool_input->>'pattern')
           -- Medium: Grep
           WHEN tu.tool_name = 'Grep' THEN
             concat(tu.tool_input->>'pattern', COALESCE(concat(' in ', tu.tool_input->>'path'), ''))
           -- Medium: Task
           WHEN tu.tool_name = 'Task' THEN
             concat(tu.tool_input->>'subagent_type', ' - ', tu.tool_input->>'description')
           -- Medium: WebFetch
           WHEN tu.tool_name = 'WebFetch' THEN tu.tool_input->>'url'
           -- Medium: WebSearch
           WHEN tu.tool_name = 'WebSearch' THEN tu.tool_input->>'query'
           -- Medium: TodoWrite
           WHEN tu.tool_name = 'TodoWrite' THEN
             CASE WHEN length(tu.tool_input->>'todos') > 200 THEN left(tu.tool_input->>'todos', 200) || '...[TRUNCATED]'
                  ELSE tu.tool_input->>'todos' END
           -- Minimal: everything else
           ELSE CASE WHEN tr.is_error THEN '[ERR]' ELSE NULL END
         END as detail
  FROM tool_uses tu
  LEFT JOIN tool_results tr ON tu.tool_id = tr.tool_use_id
)
ORDER BY timestamp ASC;
EOF
