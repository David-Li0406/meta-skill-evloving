# Handoff Patterns

data flow patterns between skills in compositions.

## core principle

> "explicit handoffs prevent data loss and enable debugging"

every handoff should:
1. have defined schema
2. be serializable (JSON/YAML)
3. include metadata for tracing
4. handle missing/optional fields

## pattern 1: JSON packet

most common pattern for structured data.

### schema

```json
{
  "meta": {
    "source_skill": "skill-name",
    "timestamp": "ISO-8601",
    "chain_id": "uuid",
    "step": 1
  },
  "data": {
    // skill-specific output
  },
  "status": "success | partial | error",
  "errors": []
}
```

### example: skill-improve → consult-deep

```json
{
  "meta": {
    "source_skill": "skill-improve",
    "timestamp": "2025-12-17T10:30:00Z",
    "chain_id": "abc123",
    "step": 1
  },
  "data": {
    "skill_name": "metaprompt-factory",
    "skill_content": "# metaprompt-factory\n...",
    "lines": 362,
    "references_count": 3,
    "changes_made": [
      "added decision tree for prompt structure",
      "added XML patterns from Anthropic docs",
      "created 3 reference files"
    ]
  },
  "status": "success",
  "errors": []
}
```

### receiving skill unpacks:

```bash
# in consult-deep prompt
<skill_content>
{{ data.skill_content }}
</skill_content>

<changes>
{{ data.changes_made | join("\n") }}
</changes>
```

---

## pattern 2: file-based handoff

for large content that would bloat JSON.

### schema

```json
{
  "meta": {
    "source_skill": "loop",
    "chain_id": "abc123",
    "step": 3
  },
  "files": {
    "pr_diff": "/tmp/chain-abc123/pr-diff.txt",
    "test_output": "/tmp/chain-abc123/test-results.json",
    "structure": "/tmp/chain-abc123/outline.yaml"
  },
  "status": "success"
}
```

### example: loop → pr-audit

```bash
# loop writes files
mkdir -p /tmp/chain-$CHAIN_ID
git diff main...HEAD > /tmp/chain-$CHAIN_ID/pr-diff.txt
verify --json > /tmp/chain-$CHAIN_ID/test-results.json
outline --pr=HEAD --format=yaml > /tmp/chain-$CHAIN_ID/structure.yaml

# pr-audit reads files
cat <<EOF | codex exec --model "gpt-5.2-codex xhigh"
PR audit.

<diff>
$(cat /tmp/chain-$CHAIN_ID/pr-diff.txt)
</diff>

<structure>
$(cat /tmp/chain-$CHAIN_ID/structure.yaml)
</structure>

<tests>
$(cat /tmp/chain-$CHAIN_ID/test-results.json | jq '.summary')
</tests>
EOF
```

---

## pattern 3: environment variables

for simple scalar values.

### example: issue context flow

```bash
# issue-context sets
export ISSUE_ID="ARB-123"
export ISSUE_TITLE="Add dark mode toggle"
export ISSUE_PRIORITY="high"
export AFFECTED_FILES="src/components/Settings.tsx,src/hooks/useTheme.ts"

# next skill reads
cat <<EOF | copilot -p --model gemini-3-pro
Pre-flight for $ISSUE_ID: $ISSUE_TITLE

Affected files: $AFFECTED_FILES
Priority: $ISSUE_PRIORITY

Is the scope well-defined?
EOF
```

### when to use

| env vars | JSON packet | file-based |
|----------|-------------|------------|
| < 10 fields | structured data | large content |
| simple scalars | nested objects | binary/multiline |
| quick scripts | debugging needed | reprocessing needed |

---

## pattern 4: streaming handoff

for real-time progress in long chains.

### schema

```bash
# write to shared file with timestamps
echo "$(date +%s) step=1 status=started" >> /tmp/chain-$CHAIN_ID/progress.log
echo "$(date +%s) step=1 status=complete output=/tmp/chain-$CHAIN_ID/step1.json" >> /tmp/chain-$CHAIN_ID/progress.log
```

### example: long-horizon → slack (progress updates)

```bash
# long-horizon writes progress
echo "$(date +%s) phase=plan progress=25 message='Plan complete, starting implementation'" >> $PROGRESS_FILE

# monitoring script sends updates
tail -f $PROGRESS_FILE | while read line; do
  progress=$(echo $line | grep -o 'progress=[0-9]*' | cut -d= -f2)
  message=$(echo $line | grep -o 'message=.*' | cut -d= -f2-)

  if [ $((progress % 25)) -eq 0 ]; then
    echo "Progress: $progress% - $message" | slack dm send --user luke
  fi
done
```

---

## pattern 5: validation handoff

standardized format for validation results.

### schema

```json
{
  "validator": "consult-deep | consult-light | pr-audit",
  "target": "what was validated",
  "result": {
    "pass": true,
    "score": 9,
    "confidence": 8
  },
  "details": {
    "criteria_scores": {},
    "issues": [],
    "suggestions": []
  },
  "meta": {
    "model": "gpt-5.2-codex xhigh | gemini-3-pro",
    "timestamp": "ISO-8601",
    "duration_ms": 12500
  }
}
```

### example: consult-deep validation

```json
{
  "validator": "consult-deep",
  "target": "skill-improve on metaprompt-factory",
  "result": {
    "pass": true,
    "score": 10,
    "confidence": 10
  },
  "details": {
    "criteria_scores": {
      "decision_trees": 10,
      "concrete_values": 10,
      "tool_integration": 10,
      "anti_patterns": 10,
      "references": 10
    },
    "issues": [],
    "suggestions": []
  },
  "meta": {
    "model": "gpt-5.2-codex xhigh",
    "timestamp": "2025-12-17T10:45:00Z",
    "duration_ms": 45000
  }
}
```

### downstream consumption

```bash
# check if should continue chain
PASS=$(echo $VALIDATION | jq -r '.result.pass')
SCORE=$(echo $VALIDATION | jq -r '.result.score')

if [ "$PASS" = "true" ] && [ $SCORE -ge 8 ]; then
  echo "Validation passed, continuing chain"
else
  echo "Validation failed (score: $SCORE), stopping"
  exit 1
fi
```

---

## pattern 6: aggregation handoff

combining results from parallel fan-out.

### schema

```json
{
  "aggregation": {
    "source_count": 3,
    "success_count": 3,
    "failed_count": 0
  },
  "results": [
    {"source": "skill-A", "key_output": "..."},
    {"source": "skill-B", "key_output": "..."},
    {"source": "skill-C", "key_output": "..."}
  ],
  "synthesis": {
    // combined analysis
  }
}
```

### example: parallel pre-flight checks

```bash
# run 3 checks in parallel
check_security &
check_performance &
check_tests &
wait

# aggregate results
cat <<EOF > /tmp/chain-$CHAIN_ID/preflight.json
{
  "aggregation": {
    "source_count": 3,
    "success_count": $(cat /tmp/results/*.json | jq -s '[.[] | select(.pass)] | length'),
    "failed_count": $(cat /tmp/results/*.json | jq -s '[.[] | select(.pass | not)] | length')
  },
  "results": $(cat /tmp/results/*.json | jq -s '.'),
  "synthesis": {
    "all_pass": $(cat /tmp/results/*.json | jq -s 'all(.pass)'),
    "blocking_issues": $(cat /tmp/results/*.json | jq -s '[.[] | .issues[] | select(.severity == "high")]')
  }
}
EOF
```

---

## debugging handoffs

### logging

```bash
# add to each handoff
log_handoff() {
  local step=$1
  local data=$2
  echo "[$(date +%Y-%m-%dT%H:%M:%S)] step=$step" >> /tmp/chain-$CHAIN_ID/handoffs.log
  echo "$data" | jq -c '.' >> /tmp/chain-$CHAIN_ID/handoffs.log
}
```

### validation

```bash
# validate handoff schema
validate_handoff() {
  local data=$1
  local required_fields=$2

  for field in $required_fields; do
    if [ "$(echo $data | jq -r ".$field")" = "null" ]; then
      echo "ERROR: missing required field: $field"
      return 1
    fi
  done
}
```

### replay

```bash
# replay from checkpoint
replay_from_step() {
  local step=$1
  local chain_id=$2

  # read handoff from that step
  handoff=$(cat /tmp/chain-$chain_id/step-$step.json)

  # continue chain from there
  # ...
}
```

---

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| implicit data | "the next skill knows" | explicit schema |
| raw stdout | can't parse | JSON/structured output |
| hardcoded paths | breaks on different runs | use $CHAIN_ID |
| no metadata | can't debug | include source, timestamp |
| no error field | silent failures | always include status/errors |
| oversized JSON | memory issues | file-based for large data |
