# Failure Modes and Recovery

Common issues in fanout execution and how to handle them.

## Session-Level Failures

### 1. Session Spawn Failure

**Symptom:** `agents session start` returns error or no session_id

**Causes:**
- Agent CLI not installed or not in PATH
- Invalid project path
- Resource contention (too many concurrent sessions)

**Detection:**
```bash
SESSION=$(cat prompt.md | agents session start -a copilot -p $PROJECT -g "analysis" --json -q)
if [ -z "$SESSION" ] || [ "$SESSION" = "null" ]; then
  echo "Spawn failed"
fi
```

**Recovery:**
```bash
# Retry with backoff
for i in {1..3}; do
  SESSION=$(cat prompt.md | agents session start -a copilot -p $PROJECT -g "analysis" --json -q)
  if [ -n "$SESSION" ] && [ "$SESSION" != "null" ]; then
    break
  fi
  sleep $((i * 5))  # 5, 10, 15 second backoff
done
```

### 2. Session Timeout

**Symptom:** Output file never appears within timeout window

**Causes:**
- Agent stuck in reasoning loop
- Complex analysis taking too long
- Agent waiting for user input (shouldn't happen with -p flag)

**Detection:**
```bash
TIMEOUT=120
ELAPSED=0
while [ ! -f "$OUTPUT_PATH" ] && [ $ELAPSED -lt $TIMEOUT ]; do
  sleep 10
  ELAPSED=$((ELAPSED + 10))
done

if [ ! -f "$OUTPUT_PATH" ]; then
  echo "Timeout after ${TIMEOUT}s"
fi
```

**Recovery:**
```bash
# Kill stalled session
agents session stop $SESSION_ID --force

# Re-spawn with simpler prompt
SIMPLE_PROMPT=$(echo "$PROMPT" | head -30)  # Truncate
SESSION=$(echo "$SIMPLE_PROMPT" | agents session start -a copilot ...)
```

### 3. Empty or Invalid Output

**Symptom:** Output file exists but contains invalid JSON or empty content

**Causes:**
- Agent returned prose instead of JSON
- Agent returned partial response
- Output contract not followed

**Detection:**
```bash
if [ -f "$OUTPUT_PATH" ]; then
  # Check if valid JSON
  if ! jq -e . "$OUTPUT_PATH" >/dev/null 2>&1; then
    echo "Invalid JSON output"
  fi

  # Check required fields
  STATUS=$(jq -r '.status // "missing"' "$OUTPUT_PATH")
  if [ "$STATUS" = "missing" ]; then
    echo "Missing required fields"
  fi
fi
```

**Recovery:**
```bash
# Wrap in JSON extraction prompt
cat << EOF | copilot -p --model gemini-3-pro --output-format json
The following agent output needs to be converted to valid JSON.
Extract the key information and format as:
{
  "mode": "fanout",
  "analysis_type": "$ANALYSIS_TYPE",
  "status": "partial",
  "summary": "extracted summary",
  "confidence": estimated 1-10,
  "artifacts": [{"type": "analysis", "content": "extracted content"}],
  "sources": {"files_read": [], "tools_used": []},
  "next_steps": [],
  "blockers": []
}

Original output:
$(cat $OUTPUT_PATH)
EOF
```

### 4. Agent Modified Files

**Symptom:** Git shows unexpected changes after analysis

**Causes:**
- Constraints block missing or ignored
- Agent interpreted analysis as action
- Agent created temp files

**Detection:**
```bash
# Check git status after session
CHANGES=$(git status --porcelain)
if [ -n "$CHANGES" ]; then
  echo "Unexpected file changes detected"
  git status --short
fi
```

**Recovery:**
```bash
# Revert changes
git checkout -- .
git clean -fd

# Re-run with stronger constraints
REINFORCED_PROMPT=$(cat << 'EOF'
CRITICAL: This is READ-ONLY analysis.
- Do NOT create, modify, or delete any files
- Do NOT run any commands that modify state
- Do NOT create git commits
- ONLY read files and report findings
- If you feel compelled to modify something, report it in next_steps instead

$ORIGINAL_PROMPT
EOF
)
```

## Aggregation-Level Failures

### 5. Too Few Successful Sessions

**Symptom:** Less than 50% of sessions succeeded

**Threshold:** 3/6 minimum for reliable aggregation

**Detection:**
```bash
TOTAL=${#SESSION_IDS[@]}
SUCCESSFUL=0
for sid in "${SESSION_IDS[@]}"; do
  if [ -f "$HOME/.agents/prompts/${sid}-response.json" ]; then
    STATUS=$(jq -r '.status' "$HOME/.agents/prompts/${sid}-response.json")
    if [ "$STATUS" = "success" ] || [ "$STATUS" = "partial" ]; then
      SUCCESSFUL=$((SUCCESSFUL + 1))
    fi
  fi
done

if [ $SUCCESSFUL -lt $((TOTAL / 2)) ]; then
  echo "Insufficient results: $SUCCESSFUL/$TOTAL"
fi
```

**Recovery:**
```bash
# Identify which analysis types failed
FAILED_TYPES=()
for type in gap pattern friction synergy platform meta; do
  # Check if this type succeeded
  # Re-spawn only failed types
done

# Proceed with partial aggregation + gaps noted
```

### 6. All Low Confidence

**Symptom:** Average confidence < 5 across all sessions

**Causes:**
- Insufficient context provided
- Project type mismatch
- Analysis scope too broad

**Detection:**
```bash
AVG_CONF=$(jq -s '[.[].confidence] | add / length' combined.json)
if [ $(echo "$AVG_CONF < 5" | bc) -eq 1 ]; then
  echo "Low confidence across all analyses: $AVG_CONF"
fi
```

**Recovery:**
```bash
# Gather more context before re-running
layer . --format=json > /tmp/architecture.json
outline --stats src/ > /tmp/code-stats.txt

# Re-run with enriched context
ENRICHED_CONTEXT="
Additional context:
Architecture: $(cat /tmp/architecture.json)
Code stats: $(cat /tmp/code-stats.txt)

$ORIGINAL_PROMPT
"
```

### 7. Contradictory Critical Findings

**Symptom:** High-confidence analyses directly contradict each other on critical issues

**Detection:**
```bash
# Extract high-confidence findings
HIGH_CONF=$(jq -s '[.[] | select(.confidence >= 8)]' combined.json)

# Check for opposing recommendations on same topic
# (requires semantic analysis - use copilot)
```

**Recovery:**
```bash
# Surface as explicit decision point
# Do NOT try to resolve automatically
# Present both positions with evidence to human

cat << EOF
## Decision Required

Two high-confidence analyses disagree:

### Position A (gap-analysis, confidence: 9)
$(jq -r '.artifacts[0].content' gap-result.json)

### Position B (pattern-extraction, confidence: 8)
$(jq -r '.artifacts[0].content' pattern-result.json)

Please review and decide which direction to take.
EOF
```

## Resource Failures

### 8. API Rate Limiting

**Symptom:** Multiple sessions fail with rate limit errors

**Detection:**
```bash
# Check for rate limit patterns in output
grep -l "rate limit" ~/.agents/prompts/*-response.json
```

**Recovery:**
```bash
# Reduce parallelism
MAX_PARALLEL=2  # Down from 6

# Add delay between spawns
for type in "${ANALYSIS_TYPES[@]}"; do
  spawn_session "$type"
  sleep 5  # Rate limit buffer
done
```

### 9. Context Window Exceeded

**Symptom:** Agent returns truncated or incomplete analysis

**Causes:**
- Prompt too long
- Target codebase too large
- Too many files in scope

**Detection:**
```bash
# Check if summary mentions truncation
SUMMARY=$(jq -r '.summary' "$OUTPUT_PATH")
if echo "$SUMMARY" | grep -qi "truncat\|incomplete\|partial"; then
  echo "Possible context overflow"
fi
```

**Recovery:**
```bash
# Scope down the analysis
# Instead of: design extract .
# Use: design extract src/auth/

# Or use file budget
outline --budget=2000 src/ > /tmp/scoped-outline.txt
```

## Recovery Decision Tree

```
Session failed?
├── Spawn failed
│   └── Retry 3x with backoff
│       ├── Still failing → skip this analysis type, note gap
│       └── Succeeded → continue
├── Timeout
│   └── Force stop, retry with simpler prompt
│       ├── Still timing out → skip, note as "too complex"
│       └── Succeeded → continue
├── Invalid output
│   └── Attempt JSON extraction
│       ├── Extraction failed → mark as failed, note gap
│       └── Extracted → use with confidence penalty (-2)
└── Files modified
    └── Revert changes, retry with reinforced constraints
        ├── Still modifying → STOP, human intervention needed
        └── Clean run → continue

Aggregation failed?
├── < 50% success rate
│   └── Identify failed types, re-run just those
│       ├── Still failing → proceed with partial + explicit gaps
│       └── Recovered → full aggregation
├── Low confidence
│   └── Gather more context, re-run all
│       ├── Still low → report as "preliminary, needs followup"
│       └── Improved → normal aggregation
└── Critical contradictions
    └── Do NOT resolve automatically
        └── Surface as decision point for human
```

## Reporting Failures

Always include failure information in final output:

```json
{
  "mode": "fanout-aggregation",
  "execution": {
    "total_sessions": 6,
    "successful": 4,
    "partial": 1,
    "failed": 1,
    "failures": [
      {
        "type": "synergy",
        "reason": "timeout",
        "attempted_recovery": true,
        "recovery_succeeded": false
      }
    ]
  },
  "coverage_gaps": [
    "synergy analysis not completed - connection opportunities may be missing"
  ],
  "confidence_warnings": [
    "friction analysis had low confidence (4/10) - may need deeper investigation"
  ]
}
```
