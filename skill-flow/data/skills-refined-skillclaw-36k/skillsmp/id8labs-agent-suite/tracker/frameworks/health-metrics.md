# Health Metrics

## Health Status Indicators

Each project has a health status calculated from multiple factors.

| Symbol | Status | Primary Trigger |
|--------|--------|-----------------|
| 🟢 | Healthy | Decay 0-49%, no blockers |
| 🟡 | Warning | Decay 50-79%, OR has blockers |
| 🔴 | Critical | Decay 80-99%, OR stuck at gate 14+ days |
| ⛔ | Frozen | Decay 100% (auto-ice triggered) |
| ❄️ | Ice | Intentionally paused |
| ⚰️ | Killed | Terminated |
| ✅ | Archived | Complete |

---

## Health Calculation

```
function calculateHealth(project):

  # Terminal states have fixed status
  if project.state == "ICE": return "❄️"
  if project.state == "KILLED": return "⚰️"
  if project.state == "ARCHIVED": return "✅"
  if project.state == "OPERATING": return "🟢"  # No decay

  # Calculate decay
  decay = calculateDecay(project)

  # Check for blockers
  has_blockers = project.blockers.length > 0

  # Check gate stuckness
  days_at_gate = today - project.state_entered
  gate_stuck = days_at_gate > 14 AND not ready_to_transition(project)

  # Determine health
  if decay >= 100:
    return "⛔"  # Frozen
  if decay >= 80 OR gate_stuck:
    return "🔴"  # Critical
  if decay >= 50 OR has_blockers:
    return "🟡"  # Warning

  return "🟢"  # Healthy
```

---

## Per-State Health Signals

What "healthy" looks like varies by stage.

### CAPTURED 🟢
**Healthy:** Idea refined, ready to validate
**Warning signs:**
- Vague idea sitting without clarification
- No problem statement after 7 days

### VALIDATING 🟢
**Healthy:** Active research, new findings being logged
**Warning signs:**
- Research started but no new findings in 10+ days
- Stuck on one aspect without moving to others

### VALIDATED 🟢
**Healthy:** Clear verdict, next steps identified
**Warning signs:**
- Verdict unclear, waffling between BUILD/PIVOT
- Decision paralysis after research complete

### ARCHITECTING 🟢
**Healthy:** Design decisions being made, docs growing
**Warning signs:**
- Stuck on stack choice for 7+ days
- Over-engineering before MVP scope locked
- Perfectionism blocking progress

### BUILDING 🟢
**Healthy:** Code shipping, progress visible
**Warning signs:**
- Blocked on technical issue for 14+ days
- Scope creep without adjustment
- No commits in 2+ weeks

### LAUNCHING 🟢
**Healthy:** Launch activities happening, date approaching
**Warning signs:**
- Launch date slipping repeatedly
- Cold feet, finding reasons not to ship
- Perfectionism blocking "good enough"

### GROWING 🟢
**Healthy:** Experiments running, learning happening
**Warning signs:**
- No experiments in 30+ days
- Metrics stagnant without investigation
- Growth on autopilot without attention

### OPERATING 🟢
**Healthy:** Systems stable, occasional improvements
**Warning signs:**
- Everything on fire, no documentation
- Single point of failure (only you can operate)
- Technical debt accumulating untracked

### EXITING 🟢
**Healthy:** Deal progressing, conversations happening
**Warning signs:**
- Deal stalled for 30+ days
- No buyer engagement
- Due diligence items not being addressed

---

## Blocker Tracking

Projects can have logged blockers that affect health.

### Blocker Format
```yaml
blockers:
  - description: "Waiting for API access from partner"
    logged: 2025-12-15
    type: external
  - description: "Stuck on auth architecture decision"
    logged: 2025-12-18
    type: internal
```

### Blocker Types
| Type | Description | Health Impact |
|------|-------------|---------------|
| external | Waiting on third party | Warning only |
| internal | Something you can solve | Warning, prompts action |
| critical | Blocks all progress | Critical status |

### Clearing Blockers
```
/tracker unblock <project> <blocker-index>
```
Or update project card directly.

---

## Days in Stage Tracking

Track how long a project has been in its current state.

```yaml
state: BUILDING
state_entered: 2025-12-01
# Days in stage = today - state_entered
```

### Healthy Duration Guidelines

| State | Healthy | Concerning | Urgent |
|-------|---------|------------|--------|
| CAPTURED | 0-7 days | 7-14 days | 14+ |
| VALIDATING | 0-14 days | 14-21 days | 21+ |
| VALIDATED | 0-10 days | 10-21 days | 21+ |
| ARCHITECTING | 0-7 days | 7-14 days | 14+ |
| BUILDING | 0-45 days | 45-60 days | 60+ |
| LAUNCHING | 0-7 days | 7-14 days | 14+ |
| GROWING | 0-60 days | 60-120 days | 120+ |
| OPERATING | Any | Any | N/A |
| EXITING | 0-30 days | 30-45 days | 45+ |

---

## Portfolio Health Aggregates

For dashboard summaries:

### Health Distribution
```
🟢 Healthy: 3 projects
🟡 Warning: 2 projects
🔴 Critical: 1 project
❄️ Ice: 2 projects
```

### Stage Distribution
```
CAPTURED     ██░░░░░░░░  1
VALIDATING   ░░░░░░░░░░  0
VALIDATED    █░░░░░░░░░  1
ARCHITECTING ░░░░░░░░░░  0
BUILDING     ████░░░░░░  3
LAUNCHING    █░░░░░░░░░  1
GROWING      ██░░░░░░░░  2
OPERATING    █░░░░░░░░░  1
ICE          ██░░░░░░░░  2
```

### Attention Score
Prioritize projects by urgency:
```
Attention Score = (decay_percent * 2) + (days_blocked * 3) + (gate_stuck_days * 2)
```

Higher score = needs more attention.

---

## Health Trends

Track health over time for pattern recognition.

### Weekly Snapshots
Store in Memory MCP:
```
{
  date: "2025-12-21",
  portfolio: {
    healthy: 3,
    warning: 2,
    critical: 1,
    ice: 2
  },
  projects: [
    { slug: "my-project", health: "🟢", decay: 25 },
    ...
  ]
}
```

### Pattern Detection
- "Project X has been in warning for 3 weeks straight"
- "You've iced 4 projects in the last month - capacity issue?"
- "Average time in BUILDING has increased from 30 to 50 days"

---

## Health Alerts

Configure in settings.yaml:

```yaml
alerts:
  on_warning: true       # Notify when project enters warning
  on_critical: true      # Notify when project enters critical
  on_freeze: true        # Notify when project auto-freezes
  on_gate_stuck: true    # Notify when stuck at gate 14+ days

  aggregate:
    portfolio_critical: 3  # Alert if 3+ projects critical
    weekly_ice_count: 2    # Alert if 2+ projects iced in a week
```
