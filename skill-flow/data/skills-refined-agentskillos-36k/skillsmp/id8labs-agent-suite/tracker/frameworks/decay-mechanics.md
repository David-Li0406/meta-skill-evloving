# Decay Mechanics

## Philosophy

Inactivity is information. If a project isn't moving, something's wrong.

Decay mechanics:
- Surface stalled projects before they silently die
- Create healthy pressure to make decisions
- Distinguish "paused intentionally" (ICE) from "abandoned" (decay)

**Ice is not death** - it's intentional pause with option to revive.

---

## Decay Calculation

```
days_since_activity = today - project.last_activity
decay_percent = min(100, (days_since_activity / state_max_duration) * 100)
```

### Max Duration by State

| State | Max Duration | Rationale |
|-------|--------------|-----------|
| CAPTURED | 14 days | Ideas are cheap, validate or drop |
| VALIDATING | 30 days | Research shouldn't drag on |
| VALIDATED | 21 days | Decide: build, pivot, or kill |
| ARCHITECTING | 14 days | Design paralysis is real |
| BUILDING | 90 days | Longer runway, but not infinite |
| LAUNCHING | 21 days | Launch momentum matters |
| GROWING | 180 days | Growth takes time |
| OPERATING | None | Maintenance can be sparse |
| EXITING | 60 days | Deals have momentum or die |

---

## Decay Thresholds

| Level | Range | Indicator | Behavior |
|-------|-------|-----------|----------|
| Healthy | 0-49% | 🟢 | No action |
| Warning | 50-79% | 🟡 | Surfaces in daily pulse |
| Critical | 80-99% | 🔴 | Escalates in weekly review |
| Frozen | 100% | ⛔ | Blocks transitions, auto-ice |

---

## Warning Behavior

At warning threshold (50%):
- Dashboard shows yellow indicator
- Next daily pulse highlights this project
- Nudge content varies by style setting:

| Style | Message |
|-------|---------|
| Gentle | "Haven't touched {project} in {X} days. Still active?" |
| Direct | "{Project} is going stale. What's the blocker?" |
| Aggressive | "{Project} dies in {Y} days. Act now or ice it." |

---

## Critical Behavior

At critical threshold (80%):
- Dashboard shows red indicator
- Weekly review forces attention
- Suggests: "Make progress, ice intentionally, or kill"

---

## Freeze Behavior

At 100% decay:
1. Project state changes to ICE (auto-freeze)
2. Last active state preserved
3. File moved to `.id8labs/projects/ice/`
4. Freeze reason logged: "Inactivity decay - {X} days without activity"
5. Dashboard shows ❄️ indicator

---

## Activity That Resets Decay

Any of these actions reset the decay clock to 0:

| Activity | Source |
|----------|--------|
| Invoke ID8Labs skill for project | Skill completion |
| Log entry via `/tracker log` | Manual |
| State transition | `/tracker update` |
| Pass a gate requirement | `/tracker gate-pass` |
| Complete a review that addresses project | Ritual |

---

## Ice Duration Limits

Projects on ice have their own lifecycle:

| Time on Ice | Action |
|-------------|--------|
| 0-3 months | Standard ice, no action needed |
| 3-6 months | Monthly prompt: "Still want {project} on ice?" |
| 6+ months | Force decision: REVIVE or ARCHIVE |

### 6-Month Ice Cleanup

At 6 months on ice:
```
"{Project} has been on ice for 6 months.

Options:
1. REVIVE - Thaw and return to {previous_state}
2. ARCHIVE - Close permanently and capture learnings

What would you like to do?"
```

---

## Revival Process (Thawing)

When `/tracker thaw <project>` is called:

### Step 1: REFLECT
```
"Why did {project} freeze?"
Freeze reason: {stored_reason}
Time on ice: {duration}

"What caused the stall?" → Prompt for user input
```

### Step 2: REVALIDATE
```
If on ice < 3 months:
  → Skip revalidation, proceed to recommit

If on ice 3-6 months:
  → "Core assumptions may have shifted. Quick gut check:"
  → "Is the problem still relevant?"
  → "Has competition changed?"

If on ice > 6 months:
  → "Recommend re-running id8scout to revalidate"
  → "Market conditions likely changed"
```

### Step 3: RECOMMIT
```
"What stage should {project} resume at?"
Previous state: {previous_state}

Options:
- Resume at {previous_state}
- Step back to earlier state

"What's different now? Why won't it stall again?"
→ Prompt for commitment

"What's your specific next action?"
→ Prompt for action

"When will you do it?"
→ Prompt for date (optional)
```

### Step 4: REACTIVATE
```
1. Move file from ice/ to active/
2. Restore to chosen state
3. Reset decay timer
4. Log revival: "Revived from ice. Commitment: {commitment}"
5. Confirm: "{Project} is back. Go get it."
```

---

## Manual Ice

User can manually ice a project anytime:

```
/tracker ice <project> [reason]
```

**If reason not provided, prompt:**
```
"Why are you icing {project}?"
Options:
- Need to focus on another project
- Waiting for external dependency
- Temporary resource constraint
- Need to think more before proceeding
- Other: [free text]
```

**Record:**
- Freeze date
- Reason
- Previous state
- Manual flag (vs auto-freeze)

**Same revival process applies.**

---

## Kill vs Ice Decision Guide

| Situation | Action | Reason |
|-----------|--------|--------|
| Validation = KILL verdict | Kill | Evidence says don't build |
| Lost interest personally | Kill | No point forcing it |
| Market disappeared | Kill | Opportunity gone |
| Need to focus elsewhere | Ice | Might return |
| Waiting on dependency | Ice | External blocker |
| Overwhelmed, need break | Ice | Capacity issue |
| Not sure anymore | Ice first | Decide with distance |
| On ice 6+ months | Force choice | Either commit or let go |

---

## Decay Exemptions

| State | Decay? | Reason |
|-------|--------|--------|
| OPERATING | No | Maintenance can be sparse |
| EXITED | No | Terminal, waiting archive |
| ARCHIVED | No | Terminal |
| ICE | No | Intentionally paused |
| KILLED | No | Terminal |

---

## Configuration

In `.id8labs/config/settings.yaml`:

```yaml
decay:
  warn_threshold: 50      # Percent at which warning triggers
  critical_threshold: 80  # Percent at which critical triggers
  freeze_threshold: 100   # Percent at which auto-ice triggers

  # Custom per-state windows (optional)
  custom_windows:
    # BUILDING: 120  # Override default 90 days
```
