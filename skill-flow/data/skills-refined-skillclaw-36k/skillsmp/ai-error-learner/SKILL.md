---
name: AI Error Learner
description: Catalogs recurring errors as pain points needing skills. Use when same error occurs multiple times.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# AI Error Learner Skill

## Purpose

Catalog recurring errors as AI pain points that need skills to resolve. This skill is the first stage of the self-improvement loop, detecting patterns in errors that warrant automated solutions.

## Auto-Activation Triggers

This skill activates when:
- Error detector hook flags a recurring error (2+ occurrences)
- User mentions "same error again", "keeps failing", or "recurring issue"
- AI pain point file contains unprocessed entries
- Manual invocation for error pattern review

## CRITICAL: Threshold System

**Do not catalog every error. Only recurring patterns warrant action.**

### Error Escalation Thresholds

```
1st Occurrence  →  Silent logging (no action)
2nd Occurrence  →  Create AI Pain Point, propose skill
3rd+ Occurrence →  Escalate priority, trigger skill-builder
```

### Why Thresholds Matter

- One-off errors are noise, not patterns
- Recurring errors indicate systemic issues
- Escalation ensures important patterns get attention
- Prevents bloating pain point tracking

## Error Fingerprinting

### Fingerprint Format

```
[TOOL_NAME]-[ERROR_TYPE]-[MESSAGE_PATTERN]
```

### Examples

| Fingerprint | Meaning |
|-------------|---------|
| `BASH-PERMISSION_DENIED-chmod` | Script permission issues |
| `PYTHON-MODULE_NOT_FOUND-gymnasium` | Missing Python module |
| `API-TIMEOUT-connection_refused` | External service unavailable |
| `EDIT-FILE_NOT_FOUND-config` | Missing configuration file |
| `BASH-COMMAND_NOT_FOUND-docker` | Missing CLI tool |

### Fingerprinting Rules

1. **Tool name**: Use uppercase, exact tool name
2. **Error type**: Categorize by error class, not specific message
3. **Message pattern**: First recognizable keyword or path segment
4. **Consistency**: Same error must produce same fingerprint

## Core Workflow

### Step 1: Review Error History

Read current error tracking:

```bash
cat .claude/pain-points/ai-error-history.json
```

Identify entries with `count >= 2` that don't have a pain point ID.

### Step 2: Analyze Pattern

For each recurring error:

1. **Understand context**: What was being attempted?
2. **Identify root cause**: Why does this error occur?
3. **Assess frequency**: How often might this recur?
4. **Determine solution type**: Is this a skill, config, or documentation issue?

### Step 3: Create AI Pain Point

Add to `.claude/pain-points/ai-pain-points.md`:

```markdown
### AI-PAIN-NNNN: [Error Summary]

**Fingerprint**: `[TOOL]-[TYPE]-[PATTERN]`
**Occurrences**: N
**First Seen**: YYYY-MM-DD
**Last Seen**: YYYY-MM-DD

**Error Pattern**:
```
[Representative error message]
```

**Root Cause**:
[Analysis of why this occurs]

**Proposed Solution**:
[Type: Skill/Config/Documentation]
[Brief description of solution]

**Priority**: [Low/Medium/High/Critical]
**Status**: Open
```

### Step 4: Update Error History

Add pain point reference to error history entry:

```json
{
  "errors": {
    "[fingerprint]": {
      "pain_point_id": "AI-PAIN-NNNN",
      ...
    }
  }
}
```

### Step 5: Recommend Next Action

Based on priority and occurrence count:

| Condition | Recommendation |
|-----------|----------------|
| High priority, 3+ occurrences | Invoke skill-builder immediately |
| Medium priority, 2-3 occurrences | Queue for next session |
| Low priority | Document and monitor |

## Edge Cases

### Error Too Generic
**Condition**: Fingerprint would match too many different errors
**Handling**: Add more specific context to fingerprint, or split into sub-patterns

### Error Already Has Skill
**Condition**: Skill exists but error still occurs
**Handling**: Create improvement ticket for skill-improver instead

### Error Is Configuration Issue
**Condition**: Error would be fixed by config change, not skill
**Handling**: Document fix in quick-reference, don't create skill

### Error Is External
**Condition**: Error is caused by external service/API
**Handling**: Create monitoring pattern, not fix skill

## Integration Points

### With Error Detector Hook
- Receives fingerprinted errors
- Uses threshold data from hook
- Updates shared error history file

### With Skill Builder
- Passes high-priority pain points
- Provides context for skill creation
- Links pain point to resulting skill

### With Pain Point Manager
- AI pain points are a subset of all pain points
- Uses similar tracking format
- Shared archive workflow

## Output Examples

### Example 1: New Recurring Error

**Trigger**: Error detector reports 2nd occurrence of permission error
**Response**:
```markdown
## Recurring Error Detected

**Fingerprint**: `BASH-PERMISSION_DENIED-scripts/deploy.sh`
**Occurrences**: 2

### Analysis
This error occurs when running deployment scripts without execute permissions.
Scripts are created with 644 permissions by default.

### AI Pain Point Created

**ID**: AI-PAIN-0012
**Priority**: Medium
**Proposed Solution**: Create pre-execution hook that checks and sets script permissions

### Recommendation
This pattern may benefit from a skill. Shall I invoke skill-builder to create one?
```

### Example 2: Escalation to Skill Builder

**Trigger**: Error reaches 3rd occurrence
**Response**:
```markdown
## Error Escalation - AI-PAIN-0008

**Fingerprint**: `PYTHON-IMPORT_ERROR-missing_deps`
**Occurrences**: 3 (escalation threshold reached)

### Pattern Summary
Python imports fail due to missing dependencies not in requirements.txt.

### Escalation Action
Invoking skill-builder with:
- Pain point: AI-PAIN-0008
- Priority: High
- Context: Auto-escalated after 3 occurrences

This will create a dependency verification skill.
```

## Error Handling

### If Error History File Missing
1. Create fresh file with empty structure
2. Log that history was reset
3. Continue processing

### If Pain Point ID Collision
1. Find next available ID
2. Log the collision
3. Continue with new ID

### If Cannot Determine Root Cause
1. Create pain point with "Needs Investigation" status
2. Set priority to Low
3. Flag for manual review

## Skill Metadata

**Version:** 1.0.0
**Created:** 2026-01-16
**Category:** Self-Improvement
**Integration:** Error Detector, Skill Builder, Pain Point Manager
**Maintenance:** Continuous (triggered by error detector)
