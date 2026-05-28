---
name: Skill Improver
description: Monitors skill effectiveness and improves failures. Use when skills fail or have low success rates.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Skill Improver Skill

## Purpose

Monitor skill effectiveness and improve skills that fail. This skill is the third stage of the self-improvement loop, ensuring skills remain effective over time and adapt to changing requirements.

## Auto-Activation Triggers

This skill activates when:
- Skill monitor reports a failure
- Skill success rate drops below 80%
- Same failure pattern occurs twice
- User reports "skill not working" or "skill failed"
- Weekly skill health review

## CRITICAL: Improvement Protocol

**Fix root causes, not symptoms. Every improvement must be verified.**

### Improvement Decision Matrix

```
┌─────────────────┬────────────────────┬─────────────────────┐
│ Condition       │ Action             │ Priority            │
├─────────────────┼────────────────────┼─────────────────────┤
│ 1 failure       │ Log and analyze    │ Monitor             │
│ 2 same pattern  │ Apply improvement  │ High                │
│ 3+ failures     │ Escalate/redesign  │ Critical            │
│ <80% success    │ Health report      │ Medium              │
│ 0 invokes/7d    │ Check relevance    │ Low                 │
└─────────────────┴────────────────────┴─────────────────────┘
```

## Failure Categories

### Category Reference

| Type | Description | Fix Approach |
|------|-------------|--------------|
| **Coverage Gap** | Doesn't trigger for valid scenario | Add new trigger pattern |
| **Logic Error** | Wrong action taken | Fix workflow steps |
| **Missing Context** | Lacks needed information | Add context gathering step |
| **Edge Case** | Unusual input not handled | Add edge case section |
| **Outdated** | Stale file paths or references | Update paths and refs |
| **Integration** | Doesn't work with other skills | Fix integration points |

## Core Workflow

### Step 1: Load Skill Metrics

Review current skill health:

```bash
cat .claude/skills/skill-metrics.json | python3 -m json.tool
```

Identify skills needing attention:
- Success rate < 80%
- Recent failures
- Zero invocations in 7 days

### Step 2: Analyze Failure Pattern

For failing skill, examine:

1. **Recent failure contexts**
   ```bash
   grep -A 5 "skill-name" .claude/skills/skill-metrics.json
   ```

2. **Skill definition**
   ```bash
   cat .claude/skills/[skill-name]/SKILL.md
   ```

3. **Related error history**
   ```bash
   grep "skill-name" .claude/pain-points/ai-error-history.json
   ```

### Step 3: Categorize Failure

Determine failure type:

**Coverage Gap Indicators:**
- "Skill didn't activate when expected"
- "Should have used [skill] but didn't"
- Trigger conditions not matching

**Logic Error Indicators:**
- "Skill ran but did wrong thing"
- Wrong output or action
- Steps executed in wrong order

**Missing Context Indicators:**
- "Didn't have enough information"
- Required data not gathered
- Assumptions failed

**Edge Case Indicators:**
- "Works normally, but not for [specific case]"
- Unusual input not handled
- Special conditions not considered

**Outdated Indicators:**
- File paths don't exist
- Commands fail
- References broken

### Step 4: Design Improvement

Based on failure category:

**For Coverage Gap:**
```markdown
## Triggers Section Update

Add new trigger:
- [New specific trigger condition]

Update pattern in skill_suggester.py if needed.
```

**For Logic Error:**
```markdown
## Workflow Section Update

### Step N (modified):
[Corrected instructions]

### Step N+1 (new):
[Additional step if needed]
```

**For Missing Context:**
```markdown
## Workflow Section Update

### Step 0 (new): Gather Context
1. Check [required information]
2. Read [needed file]
3. Verify [assumption]
```

**For Edge Case:**
```markdown
## Edge Cases Section Update

### [New Edge Case Name]
**Condition**: [When this occurs]
**Handling**: [What to do]
```

**For Outdated:**
```markdown
## Updates Required
- Line XX: Change `/old/path` to `/new/path`
- Line YY: Update command from `old-cmd` to `new-cmd`
```

### Step 5: Apply Improvement

Edit the skill file:

```bash
# Read current skill
cat .claude/skills/[skill-name]/SKILL.md

# Apply targeted edit
# (Use Edit tool for specific changes)
```

### Step 6: Update Metadata

Update skill metadata section:

```markdown
## Skill Metadata

**Version:** 1.0.1  (increment patch for fix)
**Last Improved:** YYYY-MM-DD
**Improvement:** [Brief description of change]
```

Update skill metrics:

```json
{
  "skills": {
    "skill-name": {
      "improvements": [
        {
          "date": "YYYY-MM-DD",
          "type": "coverage_gap",
          "description": "Added trigger for X scenario"
        }
      ]
    }
  }
}
```

### Step 7: Verify Improvement

Confirm fix is valid:

1. **YAML frontmatter valid**
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('.claude/skills/[skill-name]/SKILL.md').read().split('---')[1])"
   ```

2. **No syntax errors in workflow**
   - Commands are valid
   - File paths exist
   - References are correct

3. **Edge cases covered**
   - New case is documented
   - Handling is complete

### Step 8: Log Improvement

Record in episodic memory:

```markdown
### Skill Improvement
- Skill: [skill-name]
- Version: 1.0.0 → 1.0.1
- Failure Type: [category]
- Fix Applied: [brief description]
- Verified: Yes
```

## Skill Health Report

When generating health reports:

```markdown
## Skill Health Report - YYYY-MM-DD

### Summary
- Total Skills: N
- Healthy (>80%): N
- Needs Attention: N
- Critical: N

### Skills Needing Attention

#### [skill-name] - 65% success rate
**Recent Failures**: 3
**Pattern**: Logic error in step 2
**Recommendation**: Review workflow logic

#### [skill-name] - 0 invocations
**Last Invoked**: 14 days ago
**Recommendation**: Verify triggers still relevant

### Recommended Actions
1. [Priority 1 action]
2. [Priority 2 action]
```

## Edge Cases

### Skill Is Fundamentally Broken
**Condition**: Success rate near 0%, multiple failure types
**Handling**: Flag for complete redesign, don't patch

### No Clear Failure Pattern
**Condition**: Failures are random, no common cause
**Handling**: Add more logging to skill, monitor for patterns

### Improvement Would Be Breaking Change
**Condition**: Fix would change skill behavior significantly
**Handling**: Increment minor version, document migration if needed

### Skill Has No Metrics
**Condition**: New skill, no data yet
**Handling**: Skip for now, ensure metrics are being collected

## Integration Points

### With Skill Monitor Hook
- Receives failure notifications
- Updates metrics after improvements
- Tracks improvement effectiveness

### With Skill Builder
- May recommend rebuilding vs. improving
- Shares quality standards
- Uses same template structure

### With Memory System
- Logs improvements in episodic memory
- May update patterns in procedural memory
- References quick-reference for context

## Output Examples

### Example 1: Coverage Gap Fix

**Trigger**: Skill "permission-fixer" didn't activate for .sh files
**Response**:
```markdown
## Skill Improvement: permission-fixer

### Failure Analysis
**Type**: Coverage Gap
**Pattern**: Skill only triggers for `/scripts/` but user created .sh in `/tools/`

### Improvement Applied

**Triggers Section Update:**
```markdown
## Auto-Activation Triggers
This skill activates when:
- When creating files in `/scripts/` directory
- When creating any `.sh` file (added)
- When bash command fails with "Permission denied"
```

### Verification
- YAML valid: Yes
- Triggers updated: Yes
- Version: 1.0.0 → 1.0.1

### Metrics Updated
- Logged improvement in skill-metrics.json
- Reset failure counter for this pattern
```

### Example 2: Health Report

**Trigger**: Weekly skill health review
**Response**:
```markdown
## Skill Health Report - 2026-01-16

### Summary
- Total Skills: 8
- Healthy: 6 (75%)
- Needs Attention: 2 (25%)
- Critical: 0

### Detailed Status

| Skill | Invocations | Success Rate | Status |
|-------|-------------|--------------|--------|
| pain-point-manager | 24 | 95.8% | Healthy |
| bloat-manager | 4 | 100% | Healthy |
| permission-fixer | 12 | 75% | Needs Attention |
| api-validator | 0 | N/A | Dormant |

### Recommended Actions

1. **permission-fixer** (Priority: High)
   - 3 recent failures with pattern "directory not found"
   - Investigate: May need path validation step

2. **api-validator** (Priority: Low)
   - No invocations in 14 days
   - Review: Are triggers still relevant?
```

## Error Handling

### If Skill File Missing
1. Check if skill was archived
2. Report skill not found
3. Suggest recreating via skill-builder

### If Metrics Corrupted
1. Back up corrupted file
2. Rebuild from available data
3. Note data loss in report

### If Improvement Breaks Skill
1. Revert to previous version
2. Log failed improvement attempt
3. Escalate for manual review

## Skill Metadata

**Version:** 1.0.0
**Created:** 2026-01-16
**Category:** Self-Improvement
**Integration:** Skill Monitor, Skill Builder, Memory System
**Maintenance:** Continuous (triggered by skill monitor) + Weekly health review
