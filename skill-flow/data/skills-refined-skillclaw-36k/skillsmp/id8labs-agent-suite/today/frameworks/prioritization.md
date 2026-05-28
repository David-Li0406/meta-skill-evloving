# Prioritization Framework

## Purpose

Transform a list of tasks into an ordered sequence of action. Not everything is equally important—prioritization is deciding what to do first, what to do later, and what to not do at all.

---

## Core Principle

**Priority = Impact × Urgency ÷ Effort**

With adjustments for:
- Energy requirements vs. available energy
- Resistance (avoiding high-resistance without reason is failure)
- Dependencies (what unlocks other tasks)

---

## Prioritization Dimensions

### 1. Impact
What happens when this is done?

| Level | Description | Signal |
|-------|-------------|--------|
| Critical | Failure if not done | Deadline, commitment, dependency |
| High | Significant progress | Moves a project forward substantially |
| Medium | Useful progress | Contributes to goals |
| Low | Nice to have | Can wait without consequence |
| Zero | Why is this on the list? | Delete it |

### 2. Urgency
When must this be done?

| Level | Timeframe | Action |
|-------|-----------|--------|
| Now | Today | Do first |
| Soon | This week | Schedule |
| Later | This month | Plan |
| Someday | No deadline | Park or delete |

### 3. Effort
How much does this take?

| Level | Duration | Energy |
|-------|----------|--------|
| Quick | <15 min | Low |
| Short | 15-30 min | Low-Medium |
| Medium | 30-60 min | Medium |
| Long | 1-2 hours | Medium-High |
| Deep | 2+ hours | High |

### 4. Energy Match
Does available energy match required energy?

| Task Needs | Your Energy | Match |
|------------|-------------|-------|
| High | High | Go |
| High | Low | Defer |
| Low | High | Waste |
| Low | Low | Do it |

---

## Priority Score Calculation

### Simple Method

Assign 1-5 for each dimension, calculate:

```
Priority Score = (Impact × 2) + Urgency - (Effort / 2) + Resistance Bonus
```

**Resistance Bonus:**
- 0-2 resistance: +0
- 3-4 resistance: +1 (needs attention)
- 5 resistance: +2 (do it or delete it)

### Quick Method

Ask three questions:
1. "If I don't do this today, what happens?" (Urgency)
2. "When done, how much does it move things forward?" (Impact)
3. "How long will it actually take?" (Effort)

Rank by gut feeling after answering.

---

## Priority Categories

### Must Do (P1)
Non-negotiable today.

**Criteria (any one):**
- Hard deadline is today
- Blocks others from working
- Committed to someone
- Significant consequence if not done

**Max count:** 3 items

### Should Do (P2)
High value, do after P1.

**Criteria:**
- High impact
- Moves important project forward
- Deadline this week
- Builds momentum

**Max count:** 5 items

### Could Do (P3)
If time permits.

**Criteria:**
- Useful but not urgent
- Nice to have
- Low effort wins
- Admin/maintenance

**Max count:** No limit (but be realistic)

### Won't Do (P4)
Explicitly not today.

**Criteria:**
- Deferred intentionally
- Lower priority than P1-P3
- Needs different context
- Delegated or deleted

---

## Domain Prioritization

### Cross-Domain Balance

Default priority weight by domain:

| Domain | Weight | Rationale |
|--------|--------|-----------|
| ID8 Projects | 40% | Core mission, wealth building |
| TV Production | 40% | Income, commitments |
| Life Admin | 20% | Supporting tasks |

Adjust based on context:
- Shoot week? TV = 70%
- Launch week? ID8 = 70%
- Life crisis? Life = 50%+

### Within-Domain Prioritization

**ID8 Projects:**
1. Decay warnings (projects about to freeze)
2. Gate checkpoints (milestones approaching)
3. Revenue-generating tasks
4. User-facing improvements
5. Technical debt

**TV Production:**
1. Shoot day prep (non-negotiable)
2. Delivery deadlines
3. Creative development
4. Admin/coordination
5. Optional improvements

**Life Admin:**
1. Health/safety
2. Financial (bills, deadlines)
3. Appointments (committed)
4. Errands (batch-able)
5. Optional/nice-to-have

---

## Priority Conflicts

When two tasks seem equally important:

### Tiebreaker Questions

1. **Which has a harder deadline?**
   - Harder deadline wins

2. **Which unlocks other tasks?**
   - Unblocking wins

3. **Which has higher consequence if dropped?**
   - Higher consequence wins

4. **Which matches current energy better?**
   - Better match wins

5. **Which am I avoiding more?**
   - If avoiding, face it now (Eat the Frog)

### When Everything Feels Urgent

If more than 3 things feel P1:
1. Stop and breathe
2. Ask: "If I could only do ONE thing today..."
3. That's your true P1
4. Demote the rest to P2
5. Communicate if needed (renegotiate deadlines)

---

## Time-Based Priority Shifts

### Morning (High Energy)
- Prioritize high-impact, high-effort tasks
- Face resistance (Eat the Frog candidates)
- Deep work, creative work, hard problems

### Midday (Moderate Energy)
- Medium tasks, meetings
- Collaborative work
- Decision-making

### Afternoon (Lower Energy)
- Admin tasks, batching
- Low-effort wins
- Communication, email

### Evening (Planning Energy)
- Tomorrow's priorities
- Weekly review
- Capture processing

---

## Priority Adjustments

### Promote Tasks When:
- Deadline changed (sooner)
- Discovered dependency
- Request from stakeholder
- Blocking others

### Demote Tasks When:
- Deadline changed (later)
- Context not available
- Energy mismatch
- Bigger priority emerged

### Delete Tasks When:
- Sat on list >30 days untouched
- Can't articulate why it matters
- Someone else did it
- Situation changed

---

## Method-Specific Prioritization

Different methods prioritize differently:

| Method | Priority Logic |
|--------|---------------|
| Eisenhower | Urgent × Important matrix |
| GTD | Context + Energy + Time available |
| Ivy Lee | Top 6, ranked by importance |
| 1-3-5 | Size-based (1 big, 3 medium, 5 small) |
| Eat the Frog | Resistance-first |
| Must-Should-Could | Simple 3-tier |
| Energy Mapping | Energy match first |

---

## Priority Review

### Daily (Morning)
- Set P1 (max 3)
- Order P2 and P3
- Confirm time blocks align

### Daily (Evening)
- What actually got done?
- Were priorities right?
- Adjust tomorrow based on today

### Weekly
- Are you doing P1 tasks?
- What's been P3 too long?
- Domain balance check

---

## Output Format

### Priority Summary

```markdown
## Today's Priorities

### P1 - Must Do
1. {task} | {domain} | {duration} | {deadline}
2. {task} | {domain} | {duration} | {deadline}
3. {task} | {domain} | {duration} | {deadline}

### P2 - Should Do
1. {task} | {domain} | {duration}
2. {task} | {domain} | {duration}
3. {task} | {domain} | {duration}

### P3 - Could Do
- {task} | {duration}
- {task} | {duration}

### Not Today
- {task} → {why deferred}
```

### Priority Decision

When assisting with prioritization:

```markdown
## Priority Analysis: {task}

**Impact:** {1-5} - {rationale}
**Urgency:** {1-5} - {rationale}
**Effort:** {1-5} - {rationale}
**Energy Match:** {good/poor}
**Resistance:** {0-5}

**Priority Score:** {calculated}
**Recommended Priority:** P{1/2/3}
**Reasoning:** {why this priority}
```
