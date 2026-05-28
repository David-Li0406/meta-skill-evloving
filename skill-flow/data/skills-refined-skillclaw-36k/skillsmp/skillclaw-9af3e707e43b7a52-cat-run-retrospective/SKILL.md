---
name: cat:run-retrospective
description: Use this skill to run scheduled retrospective analyses, derive action items, and track their effectiveness.
---

# Skill body

## Purpose

Execute scheduled retrospective analysis on accumulated mistakes. This skill identifies patterns, evaluates action item effectiveness, derives new action items, and creates escalations for ineffective fixes. It implements the full workflow defined in `retrospectives.json`.

## When to Use

- Automatically triggered by `learn-from-mistakes` when thresholds are met.
- Manually invoked with `/cat:run-retrospective`.
- After significant project milestones.
- When pattern recurrence is suspected.

## Trigger Conditions

The retrospective is triggered when EITHER condition is met:

```yaml
triggers:
  time_based: days_since_last_retrospective >= trigger_interval_days  # default: 14
  count_based: mistake_count_since_last >= mistake_count_threshold    # default: 10
```

## Workflow

### 1. Check Trigger Conditions

```bash
RETRO_FILE=".claude/cat/retrospectives/index.json"

# Get config and state
INTERVAL=$(jq -r '.config.trigger_interval_days' "$RETRO_FILE")
THRESHOLD=$(jq -r '.config.mistake_count_threshold' "$RETRO_FILE")
LAST_RETRO=$(jq -r '.last_retrospective // empty' "$RETRO_FILE")
MISTAKES_SINCE=$(jq -r '.mistake_count_since_last' "$RETRO_FILE")

# Calculate days since last retrospective
if [[ -n "$LAST_RETRO" && "$LAST_RETRO" != "null" ]]; then
  LAST_EPOCH=$(date -d "$LAST_RETRO" +%s 2>/dev/null || echo 0)
else
  LAST_EPOCH=0
fi
NOW_EPOCH=$(date +%s)
DAYS_SINCE=$(( (NOW_EPOCH - LAST_EPOCH) / 86400 ))

# Check triggers
if [[ $DAYS_SINCE -ge $INTERVAL ]] || [[ $MISTAKES_SINCE -ge $THRESHOLD ]]; then
  echo "RETROSPECTIVE TRIGGERED"
  echo "  Days since last: $DAYS_SINCE (threshold: $INTERVAL)"
  echo "  Mistakes since last: $MISTAKES_SINCE (threshold: $THRESHOLD)"
else
  echo "No retrospective needed"
  echo "  Days since last: $DAYS_SINCE / $INTERVAL"
  echo "  Mistakes since last: $MISTAKES_SINCE / $THRESHOLD"
  exit 0
fi
```

### 2. Gather Mistakes for Analysis

```bash
# Aggregate ALL mistakes since last retrospective across all split files
if [[ -n "$LAST_RETRO" && "$LAST_RETRO" != "null" ]]; then
  MISTAKES_TO_ANALYZE=$(cat ".claude/cat/retrospectives/mistakes-*.json" 2>/dev/null | \
    jq -s --arg last "$LAST_RETRO" \
    '[.[].mistakes[] | select(.timestamp > $last)]')
else
  # No previous retrospective - analyze all mistakes
  MISTAKES_TO_ANALYZE=$(cat ".claude/cat/retrospectives/mistakes-*.json" 2>/dev/null)
fi

MISTAKE_COUNT=$(echo "$MISTAKES_TO_ANALYZE" | jq 'length')
echo "Analyzing $MISTAKE_COUNT mistakes since $LAST_RETRO"
```

### 3. Analyze by Category

```yaml
category_analysis:
  query: |
    jq --arg last "$LAST_RETRO" '
      [.[] | select(.timestamp > $last)]
      | group_by(.category)
      | map({category: .[0].category, count: length})
    '
```