# Analyzing a Specific Session

Use this workflow when asked to analyze a particular session by ID. This is a basic template. Customize your queries for your task.

## Single-Call Template

Run this batched query (replace `SESSION_ID`):

```bash
cat << 'EOF' | node "${CLAUDE_PLUGIN_ROOT}/bin/cc-query.js"
-- 1. Overview
SELECT count(*) as msgs, min(timestamp) as started, max(timestamp) as ended,
       count(DISTINCT agentId) as agents FROM messages WHERE sessionId = 'SESSION_ID';
-- 2. What was discussed
SELECT timestamp, left(content, 300) FROM human_messages WHERE sessionId = 'SESSION_ID' ORDER BY timestamp;
-- 3. Tools used
SELECT tool_name, count(*) as calls FROM tool_uses WHERE sessionId = 'SESSION_ID' GROUP BY tool_name ORDER BY calls DESC;
-- 4. Errors encountered
SELECT tool_use_id, left(result_content, 200) FROM tool_results WHERE sessionId = 'SESSION_ID' AND is_error ORDER BY timestamp;
-- 5. Token usage
SELECT sum(input_tokens) as input, sum(output_tokens) as output, sum(cache_read_tokens) as cached FROM token_usage WHERE sessionId = 'SESSION_ID';
EOF
```

This single call provides everything needed. Only run follow-up queries for specific details.

## Output Format

Present results as a summary table:

```markdown
## Session Stats for `SESSION_ID`

### Overview
| Metric | Value |
|--------|-------|
| **Total Messages** | X |
| **Duration** | ~N minutes (START to END) |
| **Agents** | N distinct agents |

### Message Breakdown
| Type | Count |
|------|-------|
| Assistant | X |
| User | X |
| System | X |

### Tool Usage
| Tool | Calls |
|------|-------|
| Bash | X |
| Read | X |
| ... | ... |

### Token Consumption
| Metric | Tokens |
|--------|--------|
| Input | X |
| Output | X |
| Cached | X |

### Errors
- N tool errors occurred (or "None")

### Topic
Brief description of what the session was about based on human_messages.
```

## Agent Analysis (if agents > 1)

Add this query to understand agent breakdown:

```sql
SELECT agentId, count(*) as msgs, min(timestamp) as started
FROM messages WHERE sessionId = 'SESSION_ID' AND isAgent = true
GROUP BY agentId ORDER BY started;
```

## Finding Sessions

If user provides partial info, find the session first:

```bash
cat << 'EOF' | node "${CLAUDE_PLUGIN_ROOT}/bin/cc-query.js"
-- By date
SELECT sessionId, project, min(timestamp) as started, count(*) as msgs
FROM messages WHERE DATE(timestamp) = '2026-01-15'
GROUP BY sessionId, project ORDER BY started;

-- By topic keyword
SELECT DISTINCT sessionId, min(timestamp) as started
FROM human_messages WHERE lower(content) LIKE '%keyword%'
GROUP BY sessionId ORDER BY started DESC LIMIT 5;
EOF
```
