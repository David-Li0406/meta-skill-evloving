# Eisenhower Matrix

## Overview

The Eisenhower Matrix (also called the Urgent-Important Matrix) helps you decide what to work on by categorizing tasks into four quadrants based on urgency and importance.

Named after President Dwight D. Eisenhower, who said: "What is important is seldom urgent and what is urgent is seldom important."

---

## The Four Quadrants

```
                    URGENT              NOT URGENT
              ┌─────────────────┬─────────────────┐
              │                 │                 │
   IMPORTANT  │   Q1: DO NOW   │  Q2: SCHEDULE   │
              │   (Crises)     │  (Goals)        │
              │                 │                 │
              ├─────────────────┼─────────────────┤
              │                 │                 │
NOT IMPORTANT │  Q3: DELEGATE  │   Q4: DELETE    │
              │  (Interrupts)  │   (Waste)       │
              │                 │                 │
              └─────────────────┴─────────────────┘
```

### Q1: Urgent + Important → DO NOW
- Crises, deadlines, emergencies
- Problems that must be solved today
- Last-minute preparations

### Q2: Important + Not Urgent → SCHEDULE
- Strategic planning
- Relationship building
- Personal development
- Prevention and preparation

### Q3: Urgent + Not Important → DELEGATE
- Interruptions
- Some meetings
- Some emails
- Other people's priorities

### Q4: Not Urgent + Not Important → DELETE
- Time wasters
- Pleasant activities mistaken for work
- Escape activities

---

## When to Use

**Good for:**
- Medium to heavy task volume
- Mixed priority tasks
- When everything feels equally important
- Weekly planning

**Not ideal for:**
- Very light task days (overkill)
- When you already know your one priority
- Execution mode (use after planning)

---

## How to Apply

### Step 1: List All Tasks (2 minutes)
Write down everything on your plate for today/this week.

### Step 2: Categorize Each Task (3 minutes)
For each task, ask:
1. "Is this urgent?" (Deadline today/soon, someone waiting, time-sensitive)
2. "Is this important?" (Moves goals forward, significant consequences)

Place in appropriate quadrant.

### Step 3: Process by Quadrant (ongoing)

**Q1 (Do Now):**
- These are your non-negotiable tasks today
- Time block them first
- Max 3 items ideally

**Q2 (Schedule):**
- These are your most valuable tasks
- Schedule specific times for them
- Protect this time fiercely
- Aim to spend most time here

**Q3 (Delegate):**
- Can someone else do this?
- If not, batch and minimize time
- Set boundaries on interruptions

**Q4 (Delete):**
- Remove from list
- Be honest about what's actually Q4
- If it stays on your list, reclassify

---

## Process Template

```markdown
## Eisenhower Matrix: {date}

### Q1: Do Now (Urgent + Important)
- [ ] {task}
- [ ] {task}
- [ ] {task}

### Q2: Schedule (Important + Not Urgent)
| Task | Scheduled For |
|------|---------------|
| {task} | {day/time} |
| {task} | {day/time} |

### Q3: Delegate/Minimize (Urgent + Not Important)
| Task | Delegate To | Or Minimize How |
|------|-------------|-----------------|
| {task} | {person} | {batch time} |

### Q4: Delete (Neither)
- {deleted task} - reason: {why it's not needed}
```

---

## Defining Urgent vs Important

### Urgent Signals
- Deadline is today or soon
- Someone is actively waiting
- Consequences of delay are immediate
- Time-sensitive opportunity

### Important Signals
- Aligns with core goals
- Significant impact if done/not done
- Moves long-term projects forward
- Affects multiple areas

### Common Misclassifications

| Task | Often Put In | Actually Belongs |
|------|--------------|------------------|
| Email | Q1 | Q3 (usually not important) |
| Social media | Q4 | Q4 (correct) |
| Exercise | Q4 | Q2 (important, not urgent) |
| Planning | Q3 | Q2 (important, not urgent) |
| Meetings | Q1 | Often Q3 (urgent but not important) |

---

## Variations

### Daily Eisenhower
Apply only to today's tasks. Simpler, faster.

### Weekly Eisenhower
Apply to the whole week. Better for planning.

### Project Eisenhower
Apply to a single project's tasks. Good for project planning.

---

## Pitfalls

### 1. Everything in Q1
If everything is urgent and important, your system is broken.
**Fix:** Use tiebreaker questions. Force items to Q2.

### 2. Ignoring Q2
Q2 is where real progress happens, but it's easy to neglect.
**Fix:** Schedule Q2 time first, before Q1 fills your day.

### 3. Q3 Disguised as Q1
Other people's urgency isn't your importance.
**Fix:** Ask "Important to whom?" and "What happens if I don't?"

### 4. Guilt About Q4
Deleting feels wrong, but keeping creates false obligation.
**Fix:** Delete decisively. If it matters, it'll come back.

---

## Integration with ID8TODAY

After applying Eisenhower:
- Q1 items → P1 (Must Do)
- Q2 items → Schedule in time blocks
- Q3 items → Batch to specific times or delegate
- Q4 items → Remove from today.md

```
/today apply eisenhower
```

Reorganizes today's tasks into quadrants and creates prioritized list.

---

## Output Format

```markdown
## Eisenhower Analysis: {date}

### Quadrant Summary
| Q | Count | Action |
|---|-------|--------|
| Q1 | {n} | Do now |
| Q2 | {n} | Schedule |
| Q3 | {n} | Delegate/batch |
| Q4 | {n} | Delete |

### Q1: Do Now
1. {task} - {why urgent + important}
2. {task}
3. {task}

### Q2: Scheduled
| Task | Time Block |
|------|------------|
| {task} | {time} |

### Q3: Batched
Time: {X:XX pm}
- {task}
- {task}

### Q4: Deleted
- {task} ❌

### Today's Order
1. {first Q1 task}
2. {second Q1 task}
3. {Q2 block if scheduled}
4. {Q3 batch time}
```
