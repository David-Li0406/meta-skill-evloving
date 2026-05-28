# Weekly Review Ritual

**Duration:** 15 minutes
**Trigger:** End of week, `/tracker review`, or 7+ days since last review
**Purpose:** Full pipeline check, assess progress, set next week's priorities

---

## When to Run

- Every Friday/Sunday (whichever ends your work week)
- Anytime 7+ days have passed since last review
- When feeling lost about overall direction

---

## Review Flow

### Phase 1: Load Portfolio (1 minute)
```
Load all active projects
Load all ice projects
Load last week's snapshot (from Memory MCP)
Calculate all metrics
```

### Phase 2: Portfolio Snapshot (2 minutes)
```
For each status category:
  - Count this week
  - Compare to last week
  - Calculate change (+/-)

Output comparison table
Highlight significant changes
```

### Phase 3: Project-by-Project (8 minutes)
```
For each active project:
  1. State and health
  2. Activity summary (last 7 days)
  3. Gate progress
  4. Blockers
  5. Suggested next action

Flag projects with:
  - No activity this week
  - New blockers
  - Ready to transition
```

### Phase 4: Decisions & Priorities (4 minutes)
```
Identify decisions needed:
  - Projects stalled: continue, ice, or kill?
  - Projects at gate: advance?
  - Ice projects: thaw or archive?

Set next week priorities:
  - Top 3 by priority score
  - Specific weekly goals for each
```

---

## Output Format

```markdown
# Weekly Review - Week of {DATE}

## Portfolio Snapshot

| Status | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| 🟢 Healthy | {n} | {n} | {+N/-N/→} |
| 🟡 Warning | {n} | {n} | {+N/-N/→} |
| 🔴 Critical | {n} | {n} | {+N/-N/→} |
| ❄️ Ice | {n} | {n} | {+N/-N/→} |

**Week Summary:**
- {n} projects advanced
- {n} projects entered warning
- {n} new blockers logged
- {n} blockers resolved

---

## Project Reviews

### {Project 1} - {STATE}

| Metric | Value |
|--------|-------|
| Health | {emoji} |
| Decay | {X}% |
| Days in stage | {N} |

**This Week's Activity:**
{Summary of activity log entries}
{If none: "⚠️ No activity logged this week"}

**Gate Progress:**
{N}/{M} MUST-HAVEs complete for {next state}
- [x] Completed requirement
- [ ] Remaining requirement

**Blockers:**
{List or "None"}

**Next Action:**
→ {Specific suggested action}

---

{Repeat for each active project}

---

## Decay Watch

### Entered Warning This Week
{Projects that crossed 50%}

### Approaching Critical
{Projects at 70-79%}

### At Risk of Freeze
{Projects at 90%+}

---

## Gate Status

### Ready to Advance
{Projects with all MUST-HAVEs complete}

| Project | Current | Next | Action |
|---------|---------|------|--------|
| {name} | {state} | {next} | `/tracker update {slug} {next}` |

### Almost Ready (1-2 remaining)
| Project | Current | Remaining |
|---------|---------|-----------|
| {name} | {state} | {requirement} |

---

## Decisions Needed

{List projects requiring explicit decisions:}

### {Project} - {Current State}
**Situation:** {Brief context}
**Options:**
1. Continue - {what this means}
2. Ice - {what this means}
3. Kill - {what this means}

**Recommendation:** {option} because {reason}

---

## Ice Box Check

| Project | On Ice | Duration | Recommendation |
|---------|--------|----------|----------------|
| {name} | {date} | {N days/months} | {Keep/Thaw/Archive} |

---

## Next Week Priorities

### 1. {Project} - {Goal}
**Why first:** {rationale}
**Success looks like:** {specific outcome}

### 2. {Project} - {Goal}
**Why:** {rationale}
**Success looks like:** {outcome}

### 3. {Project} - {Goal}
**Why:** {rationale}
**Success looks like:** {outcome}

---

## Review Complete

**Time:** ~15 minutes
**Next review:** {date + 7 days}

{If insights worth noting:}
**Note to self:** {insight to remember for monthly strategy}
```

---

## Comparison Logic

Week-over-week changes:
```
For each metric:
  change = this_week - last_week
  if change > 0: "+{change}"
  if change < 0: "{change}"
  if change == 0: "→"
```

Activity summary:
```
For each project:
  activities = filter(activity_log, last 7 days)
  if activities.length == 0:
    "⚠️ No activity logged"
  else:
    summarize(activities) # Group by type
```

---

## Memory Integration

### Store This Week's Snapshot
```
mcp__memory__create_entities({
  name: "weekly-snapshot-{date}",
  entityType: "portfolio-snapshot",
  observations: [
    "healthy: {n}",
    "warning: {n}",
    "critical: {n}",
    "ice: {n}",
    "projects: [{slug, state, decay}, ...]"
  ]
})
```

### Retrieve Last Week's Snapshot
```
mcp__memory__search_nodes({
  query: "weekly-snapshot"
})
# Get most recent before current date
```

---

## Special Handling

### First Review (No Previous Data)
```markdown
## Portfolio Snapshot

| Status | This Week |
|--------|-----------|
| 🟢 Healthy | {n} |
| 🟡 Warning | {n} |
| 🔴 Critical | {n} |
| ❄️ Ice | {n} |

*First weekly review - baseline established. Compare next week.*
```

### No Active Projects
```markdown
# Weekly Review - Week of {DATE}

No active projects to review.

**Options:**
- Capture a new idea: `/tracker new <slug> <name>`
- Thaw from ice: {list iced projects}
- Review archived for revival candidates
```

### Many Critical Projects
```markdown
## ⚠️ Portfolio Health Alert

{n} projects in critical/warning zone. This is above normal.

**Consider:**
1. Ice low-priority projects to focus
2. Kill projects that aren't working
3. Block dedicated time to address backlog

**Triage Order:**
{List by priority}
```
