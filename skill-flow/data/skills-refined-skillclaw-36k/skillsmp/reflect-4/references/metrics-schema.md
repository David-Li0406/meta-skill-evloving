# Reflect Metrics Schema Reference

This document describes the complete schema for reflect metrics stored in `~/.claude/reflect-metrics.jsonl`.

## Overview

Metrics are stored in **JSONL (JSON Lines)** format - each line is a complete, self-contained JSON object representing a single event.

**Location**: `~/.claude/reflect-metrics.jsonl`

**Format**: One JSON object per line (newline-delimited JSON)

**Purpose**: Track proposal effectiveness, user satisfaction, and continuous improvement

---

## Event Types

The metrics database contains three types of events:

1. **proposal** - When a reflect proposal is made and user responds
2. **outcome** - When effectiveness of a proposal is measured
3. **external_feedback** - When objective signals (test/lint errors) are captured

---

## Proposal Event Schema

Logged when a user approves, rejects, modifies, or defers a reflect proposal.

### Fields

```json
{
  "type": "proposal",
  "timestamp": "2026-01-17T15:30:00Z",
  "session_id": "abc123ef",
  "skill": "frontend-design",
  "user_action": "approved",
  "corrections": 2,
  "successes": 3,
  "edge_cases": 1,
  "preferences": 0,
  "external_feedback_count": 5,
  "critic_score": 85,
  "critic_recommendation": "APPROVE with suggestions",
  "critic_concerns": ["MED item lacks context about when Grid is preferred vs Flexbox"],
  "changes": [
    {
      "confidence": "high",
      "action": "Add constraint",
      "description": "All interactive elements must have aria-labels"
    }
  ],
  "commit_message": "frontend-design: add accessibility constraints",
  "modifications": ""
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✓ | Always "proposal" |
| `timestamp` | string (ISO-8601) | ✓ | When proposal was made |
| `session_id` | string | ✓ | Unique session identifier |
| `skill` | string | ✓ | Skill being reflected on |
| `user_action` | string | ✓ | User response: "approved", "rejected", "modified", "deferred" |
| `corrections` | number | ✓ | Count of HIGH-confidence correction signals |
| `successes` | number | ✓ | Count of MED-confidence success signals |
| `edge_cases` | number | ✓ | Count of MED-confidence edge case signals |
| `preferences` | number | ✓ | Count of LOW-confidence preference signals |
| `external_feedback_count` | number |  | Count of objective signals (tests/lint) ⭐ Phase 2 |
| `critic_score` | number (0-100) |  | Critic agent validation score ⭐ Phase 4 |
| `critic_recommendation` | string |  | Critic recommendation: "APPROVE", "APPROVE with suggestions", "REVISE", "REJECT" ⭐ Phase 4 |
| `critic_concerns` | array[string] |  | List of concerns raised by critic agent ⭐ Phase 4 |
| `changes` | array |  | Proposed changes with confidence/action/description |
| `commit_message` | string |  | Proposed git commit message |
| `modifications` | string |  | User modifications to proposal (if action=modified) |

### User Action Values

- **approved**: User accepted proposal as-is
- **rejected**: User declined proposal
- **modified**: User requested changes to proposal
- **deferred**: User postponed decision

---

## Outcome Event Schema

Logged when the effectiveness of an approved proposal is measured (manual or automatic).

### Fields

```json
{
  "type": "outcome",
  "timestamp": "2026-01-18T10:15:00Z",
  "session_id": "abc123ef",
  "skill": "frontend-design",
  "next_session_metrics": {
    "corrections_before": 2,
    "corrections_after": 0,
    "user_satisfaction": "positive",
    "similar_issues": false
  },
  "improvement_helpful": true,
  "confidence": 0.8,
  "auto_tracked": true
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✓ | Always "outcome" |
| `timestamp` | string (ISO-8601) | ✓ | When outcome was tracked |
| `session_id` | string | ✓ | Session ID from original proposal |
| `skill` | string | ✓ | Skill being evaluated |
| `next_session_metrics` | object | ✓ | Comparison metrics |
| `next_session_metrics.corrections_before` | number | ✓ | Errors at time of proposal |
| `next_session_metrics.corrections_after` | number | ✓ | Errors in current session |
| `next_session_metrics.user_satisfaction` | string | ✓ | "positive", "neutral", "negative" |
| `next_session_metrics.similar_issues` | boolean | ✓ | Whether same issues recurred |
| `improvement_helpful` | boolean/string | ✓ | true, false, or "neutral" |
| `confidence` | number | ✓ | Confidence in assessment (0.0-1.0) |
| `auto_tracked` | boolean |  | true if automatically tracked ⭐ NEW |

### Helpful Values

- **true**: Improvement reduced errors or improved satisfaction
- **false**: Improvement didn't help or made things worse
- **"neutral"**: No significant change

---

## External Feedback Event Schema

Logged when objective signals (test failures, lint errors, build errors) are captured.

### Fields

```json
{
  "type": "external_feedback",
  "timestamp": "2026-01-17T14:45:00Z",
  "skill": "frontend-design",
  "source": "pytest",
  "severity": "error",
  "file": "tests/test_component.py",
  "line": "42",
  "message": "AssertionError: missing aria-label on input element",
  "context": "Accessibility test suite"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | ✓ | Always "external_feedback" |
| `timestamp` | string (ISO-8601) | ✓ | When feedback was captured |
| `skill` | string | ✓ | Skill that generated the code |
| `source` | string | ✓ | Source of feedback: "pytest", "ruff", "mypy", "eslint", "tsc", "build", "custom" |
| `severity` | string | ✓ | "error", "warning", "info" |
| `file` | string |  | File where error occurred |
| `line` | string |  | Line number (stored as string for flexibility) |
| `message` | string | ✓ | Error/warning message |
| `context` | string |  | Additional context |

### Source Values

- **pytest**: Python test failures
- **ruff**: Python linter errors
- **mypy**: Python type checker errors
- **eslint**: JavaScript/TypeScript linter errors
- **tsc**: TypeScript compiler errors
- **build**: Build system errors
- **custom**: User-defined feedback sources

---

## Storage Location

### Primary Metrics File

**Path**: `~/.claude/reflect-metrics.jsonl`

**Purpose**: Central metrics database for all skills

**Format**: JSONL (one JSON object per line)

**Rotation**: Manual (no automatic rotation - user responsible)

**Backup Strategy**: Create backup before any risky operations

```bash
# Backup metrics
cp ~/.claude/reflect-metrics.jsonl ~/.claude/reflect-metrics.jsonl.backup.$(date +%s)
```

### External Feedback Storage

**Path**: `~/.claude/reflect-external-feedback/`

**Purpose**: Storage for external feedback signals (test failures, lint errors, etc.)

**Lifecycle**:
1. Captured during skill execution or analysis
2. Read by reflect during proposal generation
3. Cleaned periodically via `/reflect cleanup`

---

## Querying Metrics

### Count Proposals by Skill

```bash
grep '"type":"proposal"' ~/.claude/reflect-metrics.jsonl | \
  grep '"skill":"frontend-design"' | \
  wc -l
```

### Count Approved Proposals

```bash
grep '"user_action":"approved"' ~/.claude/reflect-metrics.jsonl | wc -l
```

### List Recent Outcomes

```bash
grep '"type":"outcome"' ~/.claude/reflect-metrics.jsonl | tail -10
```

### Count External Feedback by Source

```bash
grep '"type":"external_feedback"' ~/.claude/reflect-external-feedback/latest-feedback.jsonl | \
  grep '"source":"pytest"' | \
  wc -l
```

### Get Acceptance Rate for Skill

```bash
skill="frontend-design"
total=$(grep "\"skill\":\"$skill\"" ~/.claude/reflect-metrics.jsonl | grep '"type":"proposal"' | wc -l)
approved=$(grep "\"skill\":\"$skill\"" ~/.claude/reflect-metrics.jsonl | grep '"user_action":"approved"' | wc -l)

if [ "$total" -gt 0 ]; then
    echo "scale=2; ($approved / $total) * 100" | bc
    echo "%"
fi
```

---

## Analysis Tools

### Built-in Commands

```bash
# View statistics
/reflect stats [skill-name]

# Analyze effectiveness
/reflect analyze-effectiveness

# Track outcome manually
/reflect validate [skill-name]
```

### External Tools

**jq** - JSON processor for advanced queries:
```bash
# Get all proposals with external feedback
cat ~/.claude/reflect-metrics.jsonl | \
  jq -c 'select(.type=="proposal" and .external_feedback_count > 0)'

# Calculate average corrections per proposal
cat ~/.claude/reflect-metrics.jsonl | \
  jq -s 'map(select(.type=="proposal")) | map(.corrections) | add / length'
```

---

## Schema Evolution

### Version History

**v1.0** (Original):
- Basic proposal and outcome tracking
- Conversation signal counts

**v2.0** (Phase 2) ⭐ CURRENT:
- Added `external_feedback_count` to proposals
- Added `external_feedback` event type
- Added `auto_tracked` flag to outcomes
- Support for objective signals (tests, lint, build)

### Backwards Compatibility

All Phase 2 additions are **optional fields** - existing metrics remain valid:

- Old proposals without `external_feedback_count` → defaults to 0
- Old outcomes without `auto_tracked` → defaults to false
- Mixed event types coexist in same file

No migration required for existing metrics files.

---

## Best Practices

### 1. Regular Backups

```bash
# Weekly backup
cp ~/.claude/reflect-metrics.jsonl ~/.claude/reflect-metrics.jsonl.weekly.backup
```

### 2. Periodic Cleanup

Archive metrics older than 90 days to separate file:

```bash
# TODO: Automated archival (Phase 5, L2)
# For now, manual rotation when file becomes large (>10MB)
```

### 3. Include External Feedback

When running tests/linters, note failures as HIGH confidence signals during analysis:
- Test failures indicate skill generated incorrect code
- Linter errors indicate style/quality issues
- Build failures indicate missing dependencies or syntax errors

### 4. Monitor Disk Usage

```bash
# Check metrics file size
ls -lh ~/.claude/reflect-metrics.jsonl

# If >10MB, consider archiving old entries
```

---

## Integration Points

### Scripts that READ metrics

- `reflect-stats.sh` - Generates statistics
- `reflect-analyze-effectiveness.sh` - Analyzes patterns
- `reflect-track-outcome.sh` - Finds session IDs

### Scripts that WRITE metrics

- `reflect-track-proposal.sh` - Writes proposal events
- `reflect-track-outcome.sh` - Writes outcome events

---

## Troubleshooting

### Corrupted Metrics File

```bash
# Backup current file
cp ~/.claude/reflect-metrics.jsonl ~/.claude/reflect-metrics.jsonl.corrupted

# Find and remove malformed lines
cat ~/.claude/reflect-metrics.jsonl | jq -c . > ~/.claude/reflect-metrics.jsonl.clean

# Replace
mv ~/.claude/reflect-metrics.jsonl.clean ~/.claude/reflect-metrics.jsonl
```

### Missing External Feedback

Check if feedback was cleared:
```bash
ls -la ~/.claude/reflect-external-feedback/feedback-backup-*.jsonl
```

Restore if needed:
```bash
cp ~/.claude/reflect-external-feedback/feedback-backup-[timestamp].jsonl \
   ~/.claude/reflect-external-feedback/latest-feedback.jsonl
```

---

*This schema documentation is part of the reflect plugin. Last updated: 2026-01-17 (Phase 2)*
