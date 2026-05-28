---
name: cat:token-report
description: Generate a detailed token usage report with threshold analysis and recommendations for context management.
---

# Token Report

## Purpose

Analyze token consumption from session files to understand context utilization, detect concerning patterns, and provide recommendations for context management. Essential for monitoring session resource consumption and ensuring efficient use of context.

## When to Use

- Periodic health checks during long-running orchestration
- After subagent completion to analyze efficiency
- When monitoring detects approaching context limits
- To inform decomposition decisions
- Post-task retrospectives on token efficiency
- Quick health check during any session

## Workflow

### 1. Locate Session File

Session file location (uses auto-substituted session ID):

```bash
# Session file location
SESSION_FILE="/home/node/.config/claude/projects/-workspace/${CLAUDE_SESSION_ID}.jsonl"

# Verify file exists
if [ ! -f "${SESSION_FILE}" ]; then
  echo "ERROR: Session file not found for ${CLAUDE_SESSION_ID}"
  exit 1
fi
```

### 2. Extract Subagent Token Usage

**Primary Metric:** Extract `totalTokens` from Task tool completions.

```bash
# Extract Task tool completions with their descriptions and metrics
SUBAGENT_DATA=$(jq -s '
  # Build map of tool_use_id -> {description, type} from Task invocations
  (
    [.[] | select(.type == "assistant") | .message.content[]? |
     select(.type == "tool_use" and .name == "Task") |
     {key: .id, value: {description: .input.description, type: (.input.subagent_type // "unknown")}}] | from_entries
  ) as $task_map |

  # Extract Task completions with their metrics
  [.[] | select(.type == "user" and .toolUseResult.totalTokens != null) |
   ($task_map[.message.content[0].tool_use_id] // {description: "Unknown", type: "unknown"}) as $task_info |
   {
     tool_use_id: .message.content[0].tool_use_id,
     description: $task_info.description,
     subagent_type: $task_info.type,
     totalTokens: .toolUseResult.totalTokens,
     totalDurationMs: .toolUseResult.totalDurationMs,
     totalToolUseCount: .toolUseResult.totalToolUseCount,
     agentId: .toolUseResult.agentId,
     status: .toolUseResult.status
   }
  ] |

  # Filter out non-Task tool results
  map(select(.totalTokens > 0))
' "${SESSION_FILE}")

# Check if any subagent executions found
SUBAGENT_COUNT=$(echo "$SUBAGENT_DATA" | jq 'length')

if [ "$SUBAGENT_COUNT" -eq 0 ]; then
  echo "No subagent executions found in session."
  exit 0
fi
```

### 3. Format Token Report as Box-Drawing Table

Each subagent runs in its own independent context window. The "Context" column shows what percentage of that subagent's context limit was used.

**IMPORTANT:** Use `/cat:render-box` skill for table rendering. The table contains emojis (✓, ⚠) which require emoji-aware width calculation for proper column alignment.

```bash
# Values from agent-architecture.md § Context Limit Constants
CONTEXT_LIMIT=...
SOFT_TARGET_PCT=...
HARD_LIMIT_PCT=...
SOFT_TARGET=$((CONTEXT_LIMIT * SOFT_TARGET_PCT / 100))
HARD_LIMIT=$((CONTEXT_LIMIT * HARD_LIMIT_PCT / 100))

# Extract data for table rendering (JSON array)
TABLE_DATA=$(echo "$SUBAGENT_DATA" | jq -r --argjson limit "$CONTEXT_LIMIT" --argjson soft "$SOFT_TARGET" --argjson hard "$HARD_LIMIT" '
  [.[] |
    (.totalTokens / 1000 | . * 10 | floor / 10 | tostring + "k") as $tokens_fmt |
    (.totalTokens * 100 / $limit | floor) as $pct |
    (if .totalTokens >= $hard then "⚠ EXCEEDED"
     elif .totalTokens >= $soft then "⚠ HIGH"
     else "✓ OK"
     end) as $health |
    ((.totalDurationMs / 1000 | floor) as $secs |
     if $secs >= 60 then (($secs / 60 | floor | tostring) + "m " + (($secs % 60) | tostring) + "s")
     else ($secs | tostring) + "s" end) as $duration_fmt |
    (if (.description | length) > 28 then (.description[:25] + "...") else .description end) as $desc |
    {
      type: .subagent_type,
      description: $desc,
      tokens: $tokens_fmt,
      context: ($pct | tostring) + "% " + $health,
      duration: $duration_fmt
    }
  ]
')
```

Use the extracted `TABLE_DATA` JSON with `/cat:render-box` to produce the final table output.

### 4. Calculate Efficiency Metrics

```bash
# Messages in session
MESSAGE_COUNT=$(jq -s '[.[] | select(.type == "assistant")] | length' "${SESSION_FILE}")

# Tool calls
TOOL_CALLS=$(jq -s '[.[] | select(.type == "tool_use")] | length' "${SESSION_FILE}")

# Average tokens per message
AVG_TOKENS_PER_MSG=$((TOTAL_TOKENS / MESSAGE_COUNT))

# Input/Output ratio
IO_RATIO=$(echo "scale=2; ${INPUT_TOKENS} / ${OUTPUT_TOKENS}" | bc 2>/dev/null || echo "N/A")
```

### 5. Generate Report

```yaml
token_report:
  session_id: abc123
  generated_at: 2026-01-10T15:45:00Z

  token_usage:
    input_tokens: 45000
    output_tokens: 20000
    total_tokens: 65000
    cache_creation_tokens: 5000
    cache_read_tokens: 12000

  context_analysis:
    tokens_used: 65000
    percent_used: 32.5%
    headroom: 15000
    status: HEALTHY

  efficiency:
    messages: 45
    tool_calls: 120
    avg_tokens_per_message: 1444
    input_output_ratio: 2.25

  recommendations: []
```

### 6. Generate Recommendations

Based on analysis, provide actionable guidance:

```yaml
recommendations:
  - type: CONTEXT_WARNING
    condition: "tokens_used > 75% of threshold"
    action: "Consider decomposing remaining work into new subagent"

  - type: COMPACTION_DETECTED
    condition: "compaction_events > 0"
    action: "Context was compacted. Review for lost context. Consider smaller task scope."

  - type: HIGH_INPUT_RATIO
    condition: "input_output_ratio > 5.0"
    action: "High re-reading of context. Consider more targeted file reads."

  - type: LOW_EFFICIENCY
    condition: "messages > 50 && commits == 0"
    action: "Many messages without commits. May indicate confusion or scope issues."
```

## Examples

### Example Output

```
## Subagent Token Report

╭─────────────────┬──────────────────────────────┬────────┬──────────────┬──────────╮
│ Type            │ Description                  │ Tokens │ Context      │ Duration │
├─────────────────┼──────────────────────────────┼────────┼──────────────┼──────────┤
│ Explore         │ Explore session file format  │ 69.2k  │ 34% ✓ OK     │ 1m 7s    │
│ Plan            │ Plan token measurement fix   │ 56.0k  │ 28% ✓ OK     │ 52s      │
│ general-purpose │ Implement token fix          │ 45.0k  │ 22% ✓ OK     │ 43s      │
├─────────────────┼──────────────────────────────┼────────┼──────────────┼──────────┤
│                 │ TOTAL                        │ 170.2k │ -            │ 2m 42s   │
╰─────────────────┴──────────────────────────────┴────────┴──────────────┴──────────╯

Subagents: 3
```

## Anti-Patterns

### Always flag compaction events as concerns

```yaml
# ❌ Treating compaction as normal
compaction_events: 3
status: HEALTHY  # Wrong!

# ✅ Compaction always indicates concern
compaction_events: 3
status: WARNING
recommendation: "Multiple compactions indicate task is too large"
```

### Always provide contextual interpretation for numbers

```yaml
# ❌ Numbers without meaning
tokens: 65000

# ✅ Contextual interpretation
tokens: 65000
percent_of_limit: 32.5%
status: HEALTHY
headroom_remaining: 135000
```

### Warn proactively at 40% threshold

```bash
# ❌ Warning only at limit
if [ "${PERCENT}" -ge 100 ]; then
  echo "WARNING"
fi

# ✅ Proactive warning at 40%
if [ "${PERCENT}" -ge 40 ]; then
  echo "WARNING - approaching context limit"
fi
```

### Analyze individually before aggregating

```yaml
# ❌ Only aggregate view
total_fleet_tokens: 185000
status: OK  # Misses individual issues

# ✅ Individual + aggregate
subagent_a: 65000 (HEALTHY)
subagent_b: 85000 (WARNING)  # This needs attention!
subagent_c: 35000 (HEALTHY)
aggregate: 185000
```

## Related Skills

- `cat:render-box` - Required for table output with emoji alignment
- `cat:monitor-subagents` - Uses token reports for health checks
- `cat:decompose-task` - Triggered by token warnings
- `cat:collect-results` - Includes token metrics in collection
- `cat:learn-from-mistakes` - Uses token data for context-related analysis