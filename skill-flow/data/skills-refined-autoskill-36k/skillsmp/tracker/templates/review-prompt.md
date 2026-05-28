# Review Prompt Templates

Templates for the three review rituals: daily pulse, weekly review, monthly strategy.

---

## Daily Pulse (2 minutes)

### Trigger
- Start of work session
- `/tracker pulse` command
- If not run today and user starts a session

### Template

```markdown
# Daily Pulse - {DATE}

## Quick Scan

### 🔴 Critical Projects
{List projects with 80%+ decay or critical blockers}
{If none: "None - all clear"}

### 🟡 Warning Zone
{List projects with 50-79% decay}
{If none: "None - looking good"}

---

## Today's Focus

**Primary:** {highest priority project}
→ {specific suggested action}

**Quick Wins Available:**
- [ ] {quick win 1 - something achievable in <30 min}
- [ ] {quick win 2}

---

## Pulse Complete

{If all healthy: "Portfolio healthy. Keep momentum."}
{If warnings: "Address the warnings before they go critical."}
{If critical: "Handle critical items first. Block time now."}

*Pulse took ~2 minutes. Good to go.*
```

### Generation Logic
```
1. Load all active projects
2. Calculate decay for each
3. Identify critical (80%+) and warning (50-79%)
4. Determine highest priority (highest decay + blockers)
5. Suggest specific next action based on:
   - If at gate: "Pass gate requirement: {next requirement}"
   - If blocked: "Resolve blocker: {blocker}"
   - If building: "Ship next feature"
   - Default: "Log progress to reset decay"
6. Identify quick wins:
   - Gate requirements close to done
   - Low-decay projects that could use a touch
```

---

## Weekly Review (15 minutes)

### Trigger
- End of week
- `/tracker review` command
- If 7+ days since last weekly review

### Template

```markdown
# Weekly Review - Week of {DATE}

## Portfolio Snapshot

| Status | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| 🟢 Healthy | {n} | {n} | {+/-} |
| 🟡 Warning | {n} | {n} | {+/-} |
| 🔴 Critical | {n} | {n} | {+/-} |
| ❄️ Ice | {n} | {n} | {+/-} |

---

## Project-by-Project Review

{For each active project:}

### {Project Name} - {State}
**Health:** {emoji} | **Decay:** {X}% | **Days in stage:** {N}

**This week:**
{Summary of activity log entries from last 7 days}
{If no activity: "⚠️ No activity logged"}

**Gate status:**
{N}/{M} requirements complete for {next state}

**Blockers:**
{List blockers or "None"}

**Next action:**
{Suggested next step}

---

## Decay Warnings

{List any projects that:}
- Entered warning zone this week
- Are approaching critical
- Auto-froze this week

---

## Gate Readiness

**Ready to transition:**
{Projects where all MUST-HAVEs are complete}

**Close to ready:**
{Projects with 1-2 requirements remaining}

---

## Decisions Needed

{List projects requiring explicit decisions:}
- {Project}: Continue, ice, or kill?
- {Project}: Ready to advance to {next state}?

---

## Next Week Priorities

Based on decay, blockers, and momentum:

1. **{Project}** - {goal for next week}
2. **{Project}** - {goal}
3. **{Project}** - {goal}

---

## Review Complete

Time spent: ~15 minutes
Next weekly review: {date + 7 days}

*Log any insights or pattern observations for monthly strategy.*
```

### Generation Logic
```
1. Load all projects + last week's snapshot (from Memory MCP)
2. Calculate week-over-week changes
3. For each project:
   - Summarize activity log (last 7 days)
   - Check gate progress
   - Identify blockers
   - Suggest next action
4. Highlight decay changes
5. Identify transition-ready projects
6. Flag decision points
7. Prioritize next week
8. Store this week's snapshot in Memory MCP
```

---

## Monthly Strategy (30 minutes)

### Trigger
- End of month
- `/tracker strategy` command
- If 30+ days since last monthly strategy

### Template

```markdown
# Monthly Strategy - {MONTH YEAR}

## Portfolio Health

### Capacity Check
- **Active projects:** {n}
- **Recommended max:** {3-5 for solo builder}
- **Assessment:** {Over capacity / Right-sized / Room for more}

### Stage Distribution
```
CAPTURED     {bar} {n}
VALIDATING   {bar} {n}
VALIDATED    {bar} {n}
ARCHITECTING {bar} {n}
BUILDING     {bar} {n}
LAUNCHING    {bar} {n}
GROWING      {bar} {n}
OPERATING    {bar} {n}
```

**Observations:**
- {e.g., "Heavy in BUILDING - shipping bottleneck?"}
- {e.g., "No projects in VALIDATING - pipeline drying up?"}
- {e.g., "3 in OPERATING - good stable base"}

---

## Month in Review

### Transitions This Month
| Date | Project | From | To |
|------|---------|------|----|
{List all state transitions}

### Projects Iced
{List with reasons}

### Projects Killed
{List with lessons learned}

### New Projects Captured
{List}

---

## Ice Box Audit

| Project | On Ice Since | Duration | Decision |
|---------|--------------|----------|----------|
{For each iced project:}
| {name} | {date} | {N months} | {REVIVE / ARCHIVE / Keep ice} |

{Force decisions for anything 6+ months}

---

## Pattern Recognition

### What's Working
{Patterns from successful progress:}
- {e.g., "Daily 1-hour focused blocks → consistent progress"}
- {e.g., "Scout research taking 2 weeks avg → appropriate depth"}

### What's Not Working
{Patterns from stalls:}
- {e.g., "ARCHITECTING → BUILDING transition slow → over-engineering?"}
- {e.g., "3 projects iced this month → saying yes too fast?"}

### Recurring Blockers
{Blockers that keep appearing:}
- {e.g., "External API dependencies"}
- {e.g., "Design decisions"}

---

## Learnings Harvest

### Technical Learnings
{What you learned about building}

### Market Learnings
{What you learned about users/markets}

### Process Learnings
{What you learned about how you work}

---

## Next Month Intentions

### Primary Focus
{Which 1-2 projects get most attention?}

### Projects to Ice (if any)
{To create focus, what should pause?}

### New Captures (if any)
{Any ideas worth adding to pipeline?}

### Process Experiments
{Anything to try differently?}

---

## Monthly Metrics

| Metric | This Month | Last Month | Trend |
|--------|------------|------------|-------|
| Projects advanced | {n} | {n} | {↑/↓/→} |
| Projects iced | {n} | {n} | {↑/↓/→} |
| Projects killed | {n} | {n} | {↑/↓/→} |
| Avg decay | {n}% | {n}% | {↑/↓/→} |
| Avg days in stage | {n} | {n} | {↑/↓/→} |

---

## Strategy Complete

Time spent: ~30 minutes
Next monthly strategy: {date + 30 days}

*Key insight to remember: {single most important takeaway}*
```

### Generation Logic
```
1. Load entire portfolio (active + ice + archive)
2. Load last month's snapshot from Memory MCP
3. Calculate capacity assessment (active vs recommended)
4. Analyze stage distribution for bottlenecks/gaps
5. List all transitions, ices, kills, captures
6. For each iced project:
   - Calculate duration
   - If 6+: force decision
7. Identify patterns from:
   - Activity logs
   - State durations
   - Blocker types
8. Prompt for learnings (or infer from context)
9. Set intentions based on health + patterns
10. Calculate trends
11. Store snapshot in Memory MCP
12. Identify key insight
```

---

## Review Scheduling

Track in settings.yaml:

```yaml
last_reviews:
  pulse: 2025-12-21
  weekly: 2025-12-18
  monthly: 2025-12-01

next_reviews:
  pulse: 2025-12-22
  weekly: 2025-12-25
  monthly: 2026-01-01
```

Auto-prompt when due:
- Pulse: If not run today and user starts session
- Weekly: If 7+ days since last
- Monthly: If 30+ days since last
