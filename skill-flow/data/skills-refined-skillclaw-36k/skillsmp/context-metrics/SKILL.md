---
name: context-metrics
description: View session and context metrics for dogfooding optimization. Use when analyzing whether knowledge injection is helping, understanding context usage patterns, or optimizing the knowledge system.
allowed-tools: Bash
---

# Context Metrics Skill

Track and analyze session metrics to understand context usage, knowledge injection effectiveness, and optimize the claude-knowledge system.

## When to Use

- Analyzing knowledge injection effectiveness
- Understanding context usage patterns
- Measuring session performance
- Dogfooding the knowledge system
- Optimizing knowledge injection strategies
- Debugging why context feels noisy or insufficient
- Tracking compaction patterns

## CLI Reference

All commands use the checkpoint CLI:

```bash
bun run checkpoint metrics <command> [args...]
```

## Commands

### List Session Metrics

View detailed metrics for recorded sessions:

```bash
bun run checkpoint metrics list [issue-number]
```

Without issue number: shows all sessions
With issue number: filters to sessions for that issue

Example:

```bash
bun run checkpoint metrics list
bun run checkpoint metrics list 485
```

### Metrics Summary

View aggregate metrics across all sessions:

```bash
bun run checkpoint metrics summary
```

Shows totals and averages for:

- Total sessions
- Compaction rate
- Files read per session
- Learnings injected per session
- Learnings captured per session
- Review findings per session

## What Metrics Mean

### Files Read

**What**: Number of files Claude read during the session
**Why it matters**: High counts may indicate inefficient context gathering or lack of targeted knowledge

**Interpretation**:

- 10-30 files: Typical focused session
- 30-60 files: Broader exploration or complex issue
- 60+ files: Possible inefficiency, knowledge injection could help

### Learnings Injected

**What**: Number of knowledge entries provided at session start
**Why it matters**: Measures how much prior knowledge was relevant

**Interpretation**:

- 0 learnings: No relevant context (new area or knowledge gap)
- 1-5 learnings: Targeted, relevant context
- 5-10 learnings: Rich context, may need filtering
- 10+ learnings: Possible noise, too broad

### Learnings Captured

**What**: Number of new learnings extracted at session end
**Why it matters**: Measures knowledge accumulation rate

**Interpretation**:

- 0 learnings: Routine work, nothing new learned
- 1-3 learnings: Typical session with some insights
- 3+ learnings: High-value session, lots of new patterns

### Review Findings

**What**: Number of issues caught by review agents
**Why it matters**: Indicates code quality and knowledge application

**Interpretation**:

- 0 findings: Clean implementation or thorough pre-review
- 1-3 findings: Normal, good catch by review
- 3-8 findings: Higher-risk changes or knowledge gaps
- 8+ findings: Possible pattern: repeated mistakes, needs learning

### Compaction Status

**What**: Whether context was compacted during session
**Why it matters**: Indicates hitting context limits

**Interpretation**:

- Not compacted: Context stayed within limits
- Compacted: Hit limits, info may be lost
- Frequently compacted: Too much context, optimize injection

### Session Duration

**What**: Time from session start to session end
**Why it matters**: Longer sessions may indicate complexity or inefficiency

**Interpretation**:

- < 30 min: Quick fix or small feature
- 30-90 min: Standard implementation session
- 90-180 min: Complex feature or debugging
- 180+ min: Extended session, consider breaking into smaller chunks

## Output Format

### List Command

Returns JSON array of session metrics:

```json
[
  {
    "sessionId": "session-485-123",
    "workflowId": "workflow-485-xyz",
    "issueNumber": 485,
    "startTime": "2025-01-15T10:00:00Z",
    "endTime": "2025-01-15T11:30:00Z",
    "durationMinutes": 90,
    "filesRead": 24,
    "learningsInjected": 5,
    "learningsCaptured": 2,
    "reviewFindings": 3,
    "compacted": false,
    "interrupted": false
  }
]
```

### Summary Command

Returns aggregate statistics:

```json
{
  "totalSessions": 42,
  "compactionRate": 0.14,
  "averageFilesRead": 28.5,
  "averageLearningsInjected": 4.2,
  "averageLearningsCaptured": 1.8,
  "averageReviewFindings": 2.1,
  "totalReviewFindings": 88,
  "averageDurationMinutes": 67
}
```

## Example: Dogfooding Analysis

```bash
# 1. Check overall metrics
bun run checkpoint metrics summary

# 2. Identify patterns
# - Is compaction rate high? (>20% = too much context)
# - Are learnings actually being injected? (avg > 0)
# - Are learnings being captured? (avg > 1 = good)
# - High files read with low learnings injected? (knowledge gap)

# 3. Drill into specific issue
bun run checkpoint metrics list 485

# 4. Compare sessions before/after knowledge improvements
bun run checkpoint metrics list 380  # Old issue
bun run checkpoint metrics list 485  # New issue with better knowledge
```

## Example: Optimization Workflow

```bash
# Step 1: Get baseline metrics
bun run checkpoint metrics summary

# Step 2: Implement knowledge improvement
#   - Add more learnings to knowledge graph
#   - Improve semantic search relevance
#   - Better code-area tagging

# Step 3: Work on a few issues with new knowledge

# Step 4: Compare metrics
bun run checkpoint metrics summary
#   - Did files read decrease?
#   - Did learnings injected increase?
#   - Did review findings decrease?
```

## Interpreting Metric Patterns

### Pattern: High Files Read, Low Learnings

**Symptoms**:

- filesRead: 60+
- learningsInjected: 0-2

**Diagnosis**: Knowledge gap - relevant learnings not stored or not being found

**Action**:

- Review past sessions for this code area
- Store missing learnings manually
- Improve semantic search or code-area tagging

### Pattern: High Learnings Injected, High Review Findings

**Symptoms**:

- learningsInjected: 10+
- reviewFindings: 8+

**Diagnosis**: Learnings not being applied or wrong learnings injected

**Action**:

- Check learning quality and relevance
- Filter learnings more strictly
- Review whether learnings are actionable

### Pattern: Frequent Compaction

**Symptoms**:

- compactionRate: >20%
- avgFilesRead: high

**Diagnosis**: Hitting context limits, losing information

**Action**:

- Inject more targeted knowledge at session start
- Reduce breadth of initial file reads
- Improve learning filtering to reduce noise

### Pattern: Low Learning Capture

**Symptoms**:

- learningsCaptured: 0 consistently

**Diagnosis**: Not extracting learnings from sessions

**Action**:

- Review commit messages (learnings come from commits)
- Use conventional commit format
- Add manual learnings for insights

## Integration with Session Hooks

Metrics are recorded automatically by session hooks:

- `onSessionStart`: Records session metadata, prepares for tracking
- `onSessionEnd`: Captures final metrics, calculates duration, stores to database

**Note**: Automatic recording happens when session hooks are wired to Claude Code (currently requires manual invocation via `checkpoint session-end`).
