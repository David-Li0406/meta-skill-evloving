# Task Capture Framework

## Purpose

A frictionless system for getting tasks out of your head and into a trusted system. The goal: never lose a task, never hold one in memory.

---

## Capture Philosophy

### The Rule
**Capture everything. Process later. Never organize in the moment.**

When a task appears:
1. Grab it immediately
2. Use minimal format
3. Move on
4. Process during designated times

### Why This Matters
- Cognitive load kills productivity
- The brain is for thinking, not remembering
- Capture failure creates anxiety
- Speed beats perfection in capture

---

## Capture Formats

### Quick Capture (Mobile/Voice)

Absolute minimum info:
```
[domain] task description
```

Examples:
```
[id8] add error handling to auth
[tv] call producer about ep 4
[life] schedule haircut
```

### Standard Capture

Add metadata when you have 30 seconds:
```
[domain] task ~duration @deadline !resistance
```

Examples:
```
[id8] write API documentation ~90 @fri !2
[tv] review rough cut ~60 @today !1
[life] renew car registration ~30 @dec15 !4
```

### Full Capture

For complex tasks worth describing:
```markdown
## Task
{Clear description of what "done" looks like}

**Domain:** {id8 / tv / life}
**Project:** {if id8, project-slug}
**Energy Required:** {low / medium / high}
**Duration:** {minutes estimate}
**Deadline:** {date or none}
**Resistance:** {0-5 scale}
**Dependencies:** {what must happen first}
**Context:** {where/when this can be done}
```

---

## Domain Classification

### ID8 (Product Work)
Tasks related to building, launching, growing ID8Labs products.

**Signals:**
- Code, design, writing
- Product decisions
- User research
- Marketing/growth
- Operations

**Routing:**
- Links to project in ID8Tracker
- Syncs completion back to tracker
- Counts toward project progress

### TV (Production Work)
Reality TV production tasks.

**Signals:**
- Beat sheets, outlines
- Interviews, field work
- Edit reviews, notes
- Delivery, distribution
- Crew coordination

**Routing:**
- Tracked separately from ID8
- Calendar-driven (shoot dates)
- Deadline-heavy

### Life (Personal Admin)
Everything else that keeps life running.

**Signals:**
- Appointments
- Errands
- Health/fitness
- Family/social
- Finance/admin

**Routing:**
- Supporting tasks, not primary
- Batch to specific times
- Don't let them interrupt deep work

---

## Capture Entry Points

### During Work
- Thought interrupts → jot in parking lot
- Don't stop current task to process
- Format: quick capture only

### Inbox Processing
- Designated times (morning, after lunch)
- Move from parking lot to today/tomorrow
- Add metadata during processing

### Evening Planning
- Review all captured items
- Assign to days
- Set priorities

### Weekly Review
- Empty all inboxes
- Assign week's tasks
- Clear parking lot

---

## Task Anatomy

### Required Fields
- **What**: Clear action verb + object
- **Domain**: Where it belongs (id8/tv/life)

### Helpful Fields
- **Duration**: Time estimate in minutes
- **Deadline**: Hard date if exists
- **Resistance**: 0-5 how much you're avoiding it

### Optional Fields
- **Project**: ID8Tracker project-slug
- **Energy**: Energy level required
- **Context**: Where/when it can be done
- **Dependencies**: What must happen first

---

## Task Quality

### Good Tasks

**Clear action verb:**
```
Write → Write user documentation for auth flow
Review → Review episode 3 rough cut
Call → Call producer about schedule change
```

**Defined done state:**
```
"Ship landing page" → "Deploy landing page to production"
"Work on auth" → "Implement email verification"
"Handle support" → "Respond to 5 oldest tickets"
```

**Right size:**
- 15-120 minutes per task
- Bigger? Break it down
- Smaller? Batch it

### Bad Tasks

**Too vague:**
```
"Work on product" → Break into specific actions
"Stuff" → Be specific
"Important thing" → Name it
```

**Too big:**
```
"Build authentication system" → Break into steps
"Launch product" → What's the next action?
```

**Not actionable:**
```
"Think about..." → What decision? What action?
"Maybe..." → Decide: in or out?
"Someday..." → Move to parking lot or delete
```

---

## Processing Flow

### From Capture to Execution

```
CAPTURE
   ↓ (raw task, minimal format)
INBOX
   ↓ (processing time)
CLASSIFY
   ↓ (domain, project)
ESTIMATE
   ↓ (duration, energy)
SCHEDULE
   ↓ (today, tomorrow, later)
PRIORITIZE
   ↓ (apply method)
EXECUTE
```

### Two-Minute Rule

During processing, if a task takes <2 minutes:
1. Do it immediately
2. Don't add to list
3. Just done

This prevents list bloat from trivial tasks.

---

## Capture Locations

### Primary: Parking Lot
`.id8labs/today/parking-lot.md`

Raw captures go here:
```markdown
# Parking Lot

## Inbox
- [id8] thing captured at 9am
- [tv] thing captured at 2pm
- [life] thing captured at 5pm

## Processing Queue
{Items being reviewed}

## Archive
{Processed items for reference}
```

### Processed: Today/Tomorrow
`.id8labs/today/today.md`
`.id8labs/today/tomorrow.md`

After processing, tasks move here with full format.

### Deferred: Weekly
Tasks assigned to later days stay in weekly view.

---

## Resistance Scoring

Rate each task 0-5 for resistance:

| Score | Meaning | Indicator |
|-------|---------|-----------|
| 0 | Want to do it | Looking forward to this |
| 1 | Neutral | No strong feeling |
| 2 | Mild avoidance | Putting it off a bit |
| 3 | Moderate avoidance | Finding excuses |
| 4 | Strong avoidance | Dread thinking about it |
| 5 | Maximum resistance | Would rather do anything else |

**Why track resistance?**
- High-resistance tasks need special handling
- Methods like Eat the Frog specifically target these
- Patterns reveal what you're avoiding

---

## Context Tags

For tasks that require specific conditions:

| Context | Symbol | Meaning |
|---------|--------|---------|
| @computer | @c | Needs computer |
| @phone | @p | Can do by phone |
| @errands | @e | Out of house |
| @home | @h | At home only |
| @focus | @f | Needs deep focus |
| @energy | @+ | Needs high energy |
| @low | @- | Can do tired |

Use in capture:
```
[life] schedule dentist @p @- ~10
[id8] refactor auth flow @c @f @+ ~120
```

---

## Common Capture Mistakes

### 1. Over-engineering in the moment
**Problem:** Spending 5 minutes formatting a 5-minute task
**Fix:** Quick capture now, process later

### 2. Keeping tasks in your head
**Problem:** "I'll remember this"
**Fix:** You won't. Capture everything.

### 3. Vague tasks
**Problem:** "Work on project"
**Fix:** Clear next action with done state

### 4. Infinite lists
**Problem:** 50 tasks staring at you
**Fix:** Process to today/tomorrow, archive rest

### 5. No processing time
**Problem:** Capture but never organize
**Fix:** Schedule inbox processing (morning, after lunch)

---

## Output Format

### Capture Confirmation

When task is captured:
```markdown
## Captured

**Task:** {description}
**Domain:** {id8/tv/life}
**Added to:** Parking lot
**Process:** During next inbox review

Quick view: `[{domain}] {task} ~{duration} @{deadline} !{resistance}`
```

### Processing Summary

After inbox processing:
```markdown
## Processed

| Task | Domain | Assigned | Priority |
|------|--------|----------|----------|
| {task} | {domain} | Today | High |
| {task} | {domain} | Tomorrow | Medium |
| {task} | {domain} | Later | Low |

**2-Minute Tasks Done:** {count}
**Moved to Today:** {count}
**Moved to Tomorrow:** {count}
**Deferred:** {count}
**Deleted:** {count}
```
