# Daily Pulse Ritual

**Duration:** 2 minutes
**Trigger:** Start of work session, `/tracker pulse`, or if not run today
**Purpose:** Quick orientation, catch critical issues, set focus

---

## When to Run

- Every work session start (auto-suggest if not run today)
- Anytime you feel scattered and need to orient
- Before diving into deep work

---

## Pulse Flow

### Step 1: Quick Scan (30 seconds)
```
Load all active projects
Calculate decay for each
Identify:
  - Critical (80%+) → 🔴 Immediate action
  - Warning (50-79%) → 🟡 Address soon
  - Healthy (0-49%) → 🟢 On track
```

### Step 2: Surface Issues (30 seconds)
```
If any critical:
  "🔴 CRITICAL: {project} at {X}% decay. {Y} days to freeze."
  "Suggested action: {action}"

If any warnings:
  "🟡 WARNING: {project} at {X}% decay."
```

### Step 3: Set Focus (30 seconds)
```
Determine highest priority by:
  1. Critical projects first
  2. Then highest decay in warning
  3. Then projects at gate (ready to transition)
  4. Then most momentum (recent activity)

Output:
  "TODAY'S FOCUS: {project}"
  "→ {specific action}"
```

### Step 4: Quick Wins (30 seconds)
```
Identify low-effort high-value actions:
  - Gate requirements almost done
  - Projects that just need a log entry
  - Blockers that might be resolvable today

Output:
  "QUICK WINS:"
  "- [ ] {win 1}"
  "- [ ] {win 2}"
```

---

## Output Format

```markdown
# Daily Pulse - {TODAY}

## Quick Scan

{If all healthy:}
✅ All {n} projects healthy. No critical issues.

{If issues:}
🔴 **Critical:** {n} projects need immediate attention
🟡 **Warning:** {n} projects in decay warning zone

### Critical Projects
| Project | Decay | Days to Freeze |
|---------|-------|----------------|
| {name} | {X}% | {Y} days |

### Warning Projects
| Project | Decay | State |
|---------|-------|-------|
| {name} | {X}% | {state} |

---

## Today's Focus

**Primary:** {project name}
→ {specific action with clear next step}

**Why:** {brief rationale - highest decay, at gate, most momentum}

---

## Quick Wins

- [ ] {Quick win 1}
- [ ] {Quick win 2}

---

*Pulse complete. ~2 minutes. Go build.*
```

---

## Suggested Actions by State

| State | Default Suggested Action |
|-------|-------------------------|
| CAPTURED | "Articulate problem statement to pass gate" |
| VALIDATING | "Continue research: {next research task}" |
| VALIDATED | "Commit to BUILD or decide to PIVOT/KILL" |
| ARCHITECTING | "Complete architecture doc" |
| BUILDING | "Ship next feature / fix next bug" |
| LAUNCHING | "Execute next launch task" |
| GROWING | "Run next growth experiment" |
| OPERATING | "Check systems health" |
| EXITING | "Progress deal / complete due diligence" |

---

## Special Cases

### No Projects
```markdown
# Daily Pulse - {TODAY}

No active projects.

Options:
- Capture a new idea: `/tracker new <slug> <name>`
- Thaw a frozen project: `/tracker thaw <project>`
- Review archived projects for revival candidates
```

### All Healthy
```markdown
# Daily Pulse - {TODAY}

✅ Portfolio healthy!

All {n} projects in good standing. Keep momentum.

**Suggested focus:** {highest momentum project}
→ {advance to next gate}
```

### Multiple Critical
```markdown
# Daily Pulse - {TODAY}

⚠️ {n} projects critical. Triage needed.

## Priority Order
1. {project 1} - {reason it's first}
2. {project 2} - {reason}

Consider:
- ICE some projects to focus
- Kill projects that aren't working
- Block time to address all critical items

Which should be primary focus?
```

---

## After Pulse

Log pulse completion:
```yaml
last_reviews:
  pulse: {today}
```

If any projects were addressed, they get logged:
```
/tracker log {project} "Addressed in daily pulse"
```

---

## Nudge Styles

From settings.yaml:

| Style | Healthy Message | Warning Message | Critical Message |
|-------|-----------------|-----------------|------------------|
| Gentle | "Looking good!" | "Might want to check on {project}" | "When you get a chance, {project} needs attention" |
| Direct | "All clear." | "{project} in warning zone. Address it." | "{project} critical. Act today." |
| Aggressive | "Ship." | "{project} dying. Do something." | "🚨 {project} DEAD IN {N} DAYS. MOVE." |
