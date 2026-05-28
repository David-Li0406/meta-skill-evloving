# Monthly Strategy Ritual

**Duration:** 30 minutes
**Trigger:** End of month, `/tracker strategy`, or 30+ days since last
**Purpose:** Portfolio-level thinking, pattern recognition, strategic course correction

---

## When to Run

- Last day of each month
- First day of new month
- Anytime you need to zoom out and think strategically
- When feeling overwhelmed or directionless

---

## Strategy Flow

### Phase 1: Load Everything (2 minutes)
```
Load all active projects
Load all ice projects
Load recent archive (last 90 days)
Load monthly snapshots (last 3 months from Memory MCP)
```

### Phase 2: Portfolio Health (5 minutes)
```
Capacity assessment:
  - Count active projects
  - Compare to recommended (3-5 for solo builder)
  - Assess: over/under/right-sized

Stage distribution:
  - Count projects at each stage
  - Identify bottlenecks (too many at one stage)
  - Identify gaps (zero at important stages)
```

### Phase 3: Month in Review (5 minutes)
```
List all significant events:
  - State transitions
  - Projects iced
  - Projects killed
  - New projects captured
  - Major milestones
```

### Phase 4: Ice Box Audit (5 minutes)
```
For each iced project:
  - Calculate duration on ice
  - Force decision if 6+ months
  - Prompt for thaw/archive decision
```

### Phase 5: Pattern Recognition (8 minutes)
```
Analyze:
  - What's working (successful patterns)
  - What's not working (stall patterns)
  - Recurring blockers
  - Velocity trends

Extract learnings:
  - Technical
  - Market
  - Process
```

### Phase 6: Set Intentions (5 minutes)
```
Based on analysis:
  - Primary focus (1-2 projects)
  - Projects to ice (for focus)
  - New captures to consider
  - Process experiments
```

---

## Output Format

```markdown
# Monthly Strategy - {MONTH YEAR}

## Portfolio Health

### Capacity Assessment

| Metric | Value | Assessment |
|--------|-------|------------|
| Active projects | {n} | {Over capacity/Right-sized/Room for more} |
| Recommended max | 4-5 | - |
| Ice projects | {n} | - |
| Total pipeline | {n} | - |

{If over capacity:}
⚠️ **Over capacity.** Consider icing {n} projects to focus.

{If under capacity:}
✅ **Room for more.** Pipeline could use new captures.

### Stage Distribution

```
CAPTURED     {bar} {n} {bottleneck/gap flag}
VALIDATING   {bar} {n}
VALIDATED    {bar} {n}
ARCHITECTING {bar} {n}
BUILDING     {bar} {n}
LAUNCHING    {bar} {n}
GROWING      {bar} {n}
OPERATING    {bar} {n}
```

**Observations:**
- {e.g., "Heavy concentration in BUILDING (5) - shipping bottleneck"}
- {e.g., "No projects in VALIDATING - validation pipeline dry"}
- {e.g., "3 in OPERATING - good stable revenue base"}

---

## Month in Review

### State Transitions
| Date | Project | From → To | Notes |
|------|---------|-----------|-------|
| {date} | {project} | {from} → {to} | {notes} |

**Summary:** {n} projects advanced, {n} stalled, {n} reversed

### Projects Iced
| Project | Date | Reason |
|---------|------|--------|
| {name} | {date} | {reason} |

### Projects Killed
| Project | Date | Lessons |
|---------|------|---------|
| {name} | {date} | {key lesson} |

### New Captures
| Project | Date | One-liner |
|---------|------|-----------|
| {name} | {date} | {one-liner} |

---

## Ice Box Audit

| Project | Iced | Duration | Decision |
|---------|------|----------|----------|
| {name} | {date} | {N months} | {REVIVE / ARCHIVE / Keep} |

{For each 6+ months:}
### ⚠️ {Project} - On Ice {N} Months

**Original freeze reason:** {reason}
**Current relevance:** {still valid / outdated}

**Decision required:**
- [ ] REVIVE - Thaw and return to {previous state}
- [ ] ARCHIVE - Close permanently, capture learnings

---

## Pattern Recognition

### What's Working ✅

{Patterns that led to progress:}
1. **{Pattern}** - {Evidence}
   - {e.g., "Daily 1-hour focused blocks led to consistent BUILDING progress"}

2. **{Pattern}** - {Evidence}
   - {e.g., "Running Scout before committing prevented 2 bad builds"}

### What's Not Working ⚠️

{Patterns that led to stalls:}
1. **{Pattern}** - {Evidence}
   - {e.g., "ARCHITECTING → BUILDING taking 3x expected time"}
   - **Hypothesis:** Over-engineering before MVP

2. **{Pattern}** - {Evidence}
   - {e.g., "3 projects iced this month"}
   - **Hypothesis:** Saying yes too fast at CAPTURED

### Recurring Blockers

| Blocker Type | Frequency | Projects Affected |
|--------------|-----------|-------------------|
| {type} | {n} times | {projects} |

**Most common:** {blocker}
**Mitigation:** {suggestion}

---

## Learnings Harvest

### Technical Learnings
{What you learned about building:}
- {e.g., "Supabase RLS policies need more upfront design"}
- {e.g., "Playwright E2E tests catch more than unit tests for UI"}

### Market Learnings
{What you learned about users/markets:}
- {e.g., "Solo creators prefer simple over powerful"}
- {e.g., "Free tier conversions higher than expected"}

### Process Learnings
{What you learned about how you work:}
- {e.g., "Weekly reviews prevent surprise freezes"}
- {e.g., "Morning is best for BUILDING, afternoon for VALIDATING"}

---

## Next Month Intentions

### Primary Focus
{Which 1-2 projects get most attention:}

**1. {Project}**
- Current state: {state}
- Monthly goal: {specific outcome}
- Why prioritized: {rationale}

**2. {Project}**
- Current state: {state}
- Monthly goal: {outcome}
- Why: {rationale}

### Projects to Ice
{To create focus:}
- {Project} - {reason to pause}

### New Captures to Consider
{Ideas worth adding:}
- {Idea} - {why worth capturing}

### Process Experiments
{Things to try differently:}
- {Experiment} - {expected outcome}

---

## Monthly Metrics

| Metric | This Month | Last Month | 3-Month Avg | Trend |
|--------|------------|------------|-------------|-------|
| Projects advanced | {n} | {n} | {n} | {↑/↓/→} |
| Projects iced | {n} | {n} | {n} | {↑/↓/→} |
| Projects killed | {n} | {n} | {n} | {↑/↓/→} |
| Avg decay | {n}% | {n}% | {n}% | {↑/↓/→} |
| Avg days in stage | {n} | {n} | {n} | {↑/↓/→} |
| Gate completions | {n} | {n} | {n} | {↑/↓/→} |

---

## Strategy Complete

**Time spent:** ~30 minutes
**Next monthly strategy:** {first of next month}

### Key Insight

{Single most important takeaway from this review:}

> "{insight}"

*Store this insight. Revisit next month.*

---

*Strategy captured in Memory MCP for trend tracking.*
```

---

## Memory Integration

### Store Monthly Snapshot
```
mcp__memory__create_entities({
  name: "monthly-strategy-{YYYY-MM}",
  entityType: "monthly-strategy",
  observations: [
    "active: {n}",
    "ice: {n}",
    "advanced: {n}",
    "iced: {n}",
    "killed: {n}",
    "avg_decay: {n}%",
    "key_insight: {insight}",
    "working_patterns: [{patterns}]",
    "broken_patterns: [{patterns}]",
    "primary_focus: {project}"
  ]
})
```

### Track Learnings
```
mcp__memory__add_observations({
  entityName: "id8labs-learnings",
  contents: [
    "Technical: {learning}",
    "Market: {learning}",
    "Process: {learning}"
  ]
})
```

### Retrieve Historical Data
```
# Get last 3 monthly snapshots
mcp__memory__search_nodes({
  query: "monthly-strategy"
})
```

---

## Capacity Guidelines

| Active Projects | Assessment | Recommendation |
|-----------------|------------|----------------|
| 1-2 | Under capacity | Room for more captures |
| 3-4 | Optimal | Healthy portfolio |
| 5-6 | At capacity | Be selective about new |
| 7+ | Over capacity | Ice or kill to focus |

**Factors that affect capacity:**
- Project complexity (simple vs complex)
- Stage distribution (BUILDING takes more than OPERATING)
- External commitments (job, family, etc.)
- Current energy levels

---

## Bottleneck Detection

| Pattern | Indicates | Action |
|---------|-----------|--------|
| 3+ projects in BUILDING | Shipping bottleneck | Focus on launching |
| 0 projects in VALIDATING | Dry pipeline | Capture new ideas |
| Many in CAPTURED | Validation bottleneck | Run Scout on backlog |
| 3+ iced in month | Capacity issue | Reduce intake |
| Avg decay rising | Attention spread thin | Consolidate focus |
