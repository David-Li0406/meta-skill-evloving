---
name: Bloat Manager
description: Prevent unbounded growth of system artifacts. Use when checking system health, consolidating files, or managing archives.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Bloat Manager Skill

## Purpose

Prevent unbounded growth of system artifacts by implementing soft limits, suggesting consolidation, and managing archives. This skill maintains system health without blocking productive work.

## Auto-Activation Triggers

This skill activates when:
- It's Monday (weekly maintenance check)
- User says "check for bloat", "cleanup review", or "consolidate"
- Any soft limit threshold is approached or exceeded
- Files exceed size or count limits

## CRITICAL: Soft Limits Philosophy

**Never block operations. Always warn and suggest.**

Soft limits educate rather than frustrate. They allow justified exceptions while building awareness over time.

### Threshold Architecture

```
HEALTHY    → APPROACHING (80%)  → EXCEEDED (100%)  → CRITICAL (120%)
[No action]   [Suggest review]     [Recommend action]   [Escalate priority]
```

## Soft Limits Reference

### File Size Limits

| Artifact | Soft Limit | Review Trigger | Critical |
|----------|------------|----------------|----------|
| CLAUDE.md | 400 lines | 450 lines | 500 lines |
| quick-reference.md | 100 lines | 120 lines | 150 lines |
| procedural-memory.md | 500 lines | 600 lines | 750 lines |
| episodic-memory.md | 200 lines | 250 lines | 300 lines |
| Individual SKILL.md | 300 lines | 350 lines | 400 lines |

### Count Limits

| Category | Soft Limit | Review Trigger | Critical |
|----------|------------|----------------|----------|
| Active skills | 30 | 40 | 50 |
| Active pain points | 50 | 65 | 80 |
| Error history entries | 100 | 150 | 200 |
| Patterns in quick-ref | 20 | 25 | 30 |

### Retention Policies

| Content Type | Active Period | Archive Trigger | Delete Trigger |
|--------------|---------------|-----------------|----------------|
| Patterns | Rolling 6 months | Unused 6 months | Never |
| Session summaries | 30 days | After 30 days | After 1 year |
| Error history | 30 days | After 90 days | After 1 year |
| Resolved pain points | 30 days | After 30 days | After 6 months |

## Core Workflow

### Step 1: Gather Metrics

Collect current state of all monitored artifacts:

```bash
# Count lines in key files
wc -l .claude/CLAUDE.md
wc -l .claude/memory/active/quick-reference.md
wc -l .claude/memory/active/procedural-memory.md
wc -l .claude/memory/active/episodic-memory.md

# Count skills
find .claude/skills -name "SKILL.md" | wc -l

# Count active pain points
grep -c "^### " .claude/pain-points/active-pain-points.md

# Count error history entries
python3 -c "import json; print(len(json.load(open('.claude/pain-points/ai-error-history.json')).get('errors', {})))"
```

### Step 2: Assess Health Status

For each metric, determine status:
- **Healthy**: Below 80% of soft limit
- **Approaching**: 80-99% of soft limit
- **Exceeded**: 100-119% of soft limit
- **Critical**: 120%+ of soft limit

### Step 3: Generate Health Report

Present findings in clear format:

```markdown
## System Health Report - YYYY-MM-DD

### Summary
- Overall Status: [Healthy/Needs Attention/Action Required]
- Items Approaching Limits: N
- Items Exceeding Limits: N

### Detailed Metrics

| Artifact | Current | Limit | Status |
|----------|---------|-------|--------|
| CLAUDE.md | 385 lines | 400 | Approaching (96%) |
| Skills | 28 | 30 | Approaching (93%) |
| Pain Points | 42 | 50 | Healthy (84%) |

### Recommended Actions
1. [Specific action for exceeded items]
2. [Specific action for approaching items]
```

### Step 4: Propose Consolidation (if needed)

For items needing attention:

**For CLAUDE.md bloat:**
- Identify sections that can move to `.claude/specs/`
- Find redundant or outdated rules
- Suggest merging related specifications

**For skill bloat:**
- Identify similar skills that can merge
- Find unused skills (no invocations in 30 days)
- Suggest deprecating obsolete skills

**For memory bloat:**
- Identify patterns to archive (unused 6+ months)
- Find duplicate or near-duplicate entries
- Suggest consolidating related patterns

**For pain point bloat:**
- Identify resolved pain points to archive
- Find stale pain points (no updates in 60 days)
- Suggest closing or escalating old items

### Step 5: Execute Approved Actions

Only after user approval:
- Move content to archives
- Consolidate files
- Update references
- Document changes in episodic memory

## Edge Cases

### Monday Falls on Holiday
**Condition**: Weekly check lands on a holiday
**Handling**: Run check on next working day, note delay in report

### Multiple Items Critical
**Condition**: Several artifacts exceed critical thresholds
**Handling**: Prioritize by impact - CLAUDE.md > skills > memory > pain points

### New Project (Few Artifacts)
**Condition**: Project is new, most metrics near zero
**Handling**: Skip check, note "healthy - early stage project"

### Archive Directory Missing
**Condition**: Archive target doesn't exist
**Handling**: Create archive structure before moving files

## Integration Points

### With Pain Point Manager
- Archive resolved pain points
- Track bloat-related friction as pain points

### With Memory System
- Log consolidation actions in episodic memory
- Update procedural memory with new patterns discovered

### With Skill Metrics
- Use invocation data to identify unused skills
- Track bloat manager effectiveness

## Output Examples

### Example 1: Healthy System

**Trigger**: Weekly Monday check
**Response**:
```markdown
## System Health Report - 2026-01-13

### Summary
Overall Status: **Healthy**

All artifacts are within healthy limits. No action required.

| Artifact | Current | Limit | Status |
|----------|---------|-------|--------|
| CLAUDE.md | 285 lines | 400 | Healthy (71%) |
| Skills | 12 | 30 | Healthy (40%) |
| Pain Points | 8 | 50 | Healthy (16%) |
| Error History | 23 | 100 | Healthy (23%) |

Next scheduled check: 2026-01-20
```

### Example 2: Action Required

**Trigger**: User says "check for bloat"
**Response**:
```markdown
## System Health Report - 2026-01-16

### Summary
Overall Status: **Action Required**

2 items exceeding limits, 1 approaching.

| Artifact | Current | Limit | Status |
|----------|---------|-------|--------|
| CLAUDE.md | 456 lines | 400 | **Exceeded (114%)** |
| Skills | 35 | 30 | **Exceeded (117%)** |
| Pain Points | 45 | 50 | Approaching (90%) |

### Recommended Actions

**1. CLAUDE.md Consolidation (Priority: High)**
- Move deployment specifications (lines 180-250) to `.claude/specs/deployment.md`
- Archive deprecated rules from 2025 (lines 312-340)
- Expected reduction: ~100 lines

**2. Skill Consolidation (Priority: High)**
- Merge `data-validator` and `input-checker` (similar purpose)
- Archive `legacy-formatter` (0 invocations in 60 days)
- Expected reduction: 5 skills

**3. Pain Point Review (Priority: Medium)**
- Review 12 pain points older than 30 days
- 5 appear resolved but not archived

Shall I proceed with any of these actions?
```

## Error Handling

### If File Read Fails
1. Log the error
2. Mark that artifact as "Unable to assess"
3. Continue with other artifacts
4. Note incomplete assessment in report

### If Archive Write Fails
1. Do not delete original
2. Report failure to user
3. Suggest manual intervention
4. Log in error history

### If Metrics File Corrupted
1. Back up corrupted file
2. Initialize fresh metrics file
3. Note data loss in report
4. Continue with available data

## Skill Metadata

**Version:** 1.0.0
**Created:** 2026-01-16
**Category:** System Maintenance
**Integration:** Memory System, Pain Points, Skill Metrics
**Maintenance:** Self-monitoring (runs weekly)
