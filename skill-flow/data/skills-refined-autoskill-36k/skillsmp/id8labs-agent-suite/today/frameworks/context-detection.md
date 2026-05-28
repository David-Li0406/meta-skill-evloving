# Context Detection Framework

## Purpose

Automatically assess the current work context to recommend the best productivity method. Context-aware suggestions beat one-size-fits-all approaches.

---

## Context Dimensions

### 1. Task Volume
How many things need to be done today?

| Volume | Task Count | State |
|--------|------------|-------|
| Light | 1-4 | Focused day, depth over breadth |
| Medium | 5-10 | Balanced day, prioritization needed |
| Heavy | 11+ | Overloaded, triage required |

**Detection signals:**
- Count tasks in today.md
- Count items in parking lot
- Check calendar density

### 2. Energy Level
What's your current capacity?

| Level | Description | Signs |
|-------|-------------|-------|
| High | Full capacity, motivated | Slept well, early morning, caffeine hit |
| Medium | Normal working capacity | Mid-day, typical state |
| Low | Depleted, struggling | Late day, poor sleep, stressed |

**Detection signals:**
- Time of day (morning = higher)
- Yesterday's close (productive = momentum)
- User self-report
- Calendar load (back-to-back = draining)

### 3. Resistance Level
How much task avoidance is happening?

| Level | Description | Signs |
|-------|-------------|-------|
| Low | Tasks feel approachable | Starting easily, no dread |
| Medium | Some avoidance | Delaying certain tasks |
| High | Significant avoidance | Everything feels hard, finding excuses |

**Detection signals:**
- Tasks with resistance score 4-5
- Tasks carried forward multiple days
- Time spent on low-priority busy work
- Explicit user mention of avoidance

### 4. Time Available
How much focused time exists?

| Availability | Hours | State |
|--------------|-------|-------|
| Full day | 6+ hours | Deep work possible |
| Half day | 3-5 hours | Choose carefully |
| Fragments | <3 hours | Quick wins only |

**Detection signals:**
- Calendar free time
- Known commitments
- Time of day remaining

### 5. Task Type Mix
What kinds of tasks dominate?

| Type | Description | Methods |
|------|-------------|---------|
| Deep work | Creative, complex, requires focus | Time Blocking, Eat the Frog |
| Admin | Routine, many small items | Batching, 2-Minute Rule |
| Mixed | Variety of types | 1-3-5, Eisenhower |
| Collaborative | Meetings, calls, async | Time Blocking (protect non-meeting) |

**Detection signals:**
- Task duration estimates
- Context tags (@f for focus, etc.)
- Calendar meeting density

---

## Context Assessment Flow

```
1. GATHER
   - Read today.md for task count
   - Check parking-lot.md for overflow
   - Review calendar for commitments
   - Note time of day

2. ASSESS
   - Volume: Light / Medium / Heavy
   - Energy: Low / Medium / High
   - Resistance: Low / Medium / High
   - Time: Full / Half / Fragments
   - Type: Deep / Admin / Mixed / Collaborative

3. MATCH
   - Cross-reference context matrix
   - Identify top 2-3 method candidates
   - Consider user history/preferences

4. RECOMMEND
   - Primary method with rationale
   - Alternative if primary doesn't fit
   - Quick start guide for chosen method
```

---

## Context → Method Matrix

### Primary Recommendations

| Volume | Energy | Best Methods |
|--------|--------|--------------|
| Light | High | Eat the Frog, Deep Work |
| Light | Medium | Ivy Lee, Time Blocking |
| Light | Low | Energy Mapping, Pomodoro |
| Medium | High | Eisenhower, 1-3-5 |
| Medium | Medium | GTD, Time Blocking |
| Medium | Low | Must-Should-Could, Batching |
| Heavy | High | GTD Full Capture, Eisenhower |
| Heavy | Medium | 1-3-5, Must-Should-Could |
| Heavy | Low | Two-Minute Rule, Triage |

### Resistance Modifiers

When resistance is HIGH, add:
- **Pomodoro** - Makes tasks feel smaller
- **Eat the Frog** - Face it first
- **Two-Minute Rule** - Build momentum with quick wins

### Time Modifiers

| Time Available | Add/Modify |
|----------------|------------|
| Full day | Can use any method |
| Half day | Skip elaborate planning, use 1-3-5 |
| Fragments | Two-Minute Rule, Batching only |

---

## Context Scenarios

### Scenario 1: Fresh Monday Morning
**Context:**
- Volume: Medium (7 tasks)
- Energy: High (rested)
- Resistance: Low (motivated)
- Time: Full day

**Recommendation:** Eisenhower Matrix or Eat the Frog
**Rationale:** High energy should tackle high-impact work. Start with the hardest/most important task.

### Scenario 2: Overwhelmed Wednesday
**Context:**
- Volume: Heavy (15+ tasks)
- Energy: Medium
- Resistance: High (everything feels hard)
- Time: Half day (meetings)

**Recommendation:** Two-Minute Rule + Must-Should-Could
**Rationale:** Clear small items fast to reduce overwhelm. Strict triage on what actually happens today.

### Scenario 3: Low-Energy Friday
**Context:**
- Volume: Light (4 tasks)
- Energy: Low (end of week)
- Resistance: Medium
- Time: Half day

**Recommendation:** Energy Mapping + Batching
**Rationale:** Match low-energy tasks to low energy. Group admin together.

### Scenario 4: Shoot Week (TV)
**Context:**
- Volume: Variable
- Energy: Depleted
- Domain: TV dominant (70%)
- Time: Fragments

**Recommendation:** Time Blocking (protect rest)
**Rationale:** Shoot days are non-negotiable. Protect non-shoot time fiercely. Minimize ID8 work.

### Scenario 5: Launch Week (ID8)
**Context:**
- Volume: Heavy
- Energy: High (adrenaline)
- Domain: ID8 dominant (80%)
- Time: Full days

**Recommendation:** Time Blocking + Eisenhower
**Rationale:** Protect deep work blocks. Ruthless prioritization. Ship beats perfect.

---

## Detection Prompts

### Quick Assessment (30 seconds)

Ask user three questions:

1. **Volume:** "How many things need your attention today?"
   - 1-4 → Light
   - 5-10 → Medium
   - 11+ → Heavy

2. **Energy:** "How are you feeling right now?"
   - "Ready to tackle hard things" → High
   - "Normal working day" → Medium
   - "Tired/stressed/struggling" → Low

3. **Resistance:** "Are you avoiding anything today?"
   - "No, ready to go" → Low
   - "A few things I'm putting off" → Medium
   - "Everything feels hard" → High

### Automatic Detection (from data)

```
Volume = count(today.md tasks) + count(parking-lot.md)
Energy = f(time_of_day, yesterday_completion_rate, calendar_density)
Resistance = max(task_resistance_scores) or average if >3 items at 4+
Time = calendar_free_hours remaining
```

---

## Method Quick-Start Cards

When recommending a method, provide a quick-start:

### Example: Eisenhower Matrix Quick-Start

```markdown
## Today's Method: Eisenhower Matrix

**Why this method:** Medium volume, high energy—time to prioritize smartly.

**Quick setup (2 minutes):**
1. List all tasks
2. Ask for each: "Urgent?" and "Important?"
3. Place in quadrant:
   - Urgent + Important → DO NOW
   - Important + Not Urgent → SCHEDULE
   - Urgent + Not Important → DELEGATE (or batch)
   - Neither → DELETE

**Start with:** Your top item from "DO NOW" quadrant
```

### Example: Two-Minute Rule Quick-Start

```markdown
## Today's Method: Two-Minute Rule

**Why this method:** Heavy volume, low energy—clear quick wins to build momentum.

**Quick setup (1 minute):**
1. Scan your task list
2. Anything <2 minutes? Do it NOW
3. Don't add it to the list—just do it
4. Continue until all 2-minute items done

**Then:** Apply Must-Should-Could to remaining items
**Start with:** First quick task you see
```

---

## User Preferences

Track in preferences.md:

```markdown
# Method Preferences

## Defaults
- Morning method: {Eat the Frog}
- Afternoon method: {Batching}
- Heavy day method: {1-3-5}
- Low energy method: {Energy Mapping}

## Never Suggest
- {Method user doesn't like}

## Domain Defaults
- ID8 deep work: Time Blocking
- TV production: Calendar-driven
- Life admin: Batching

## Time Block Defaults
- Deep work: 9am-12pm
- Admin: 2pm-4pm
- Planning: 5pm-6pm
```

---

## Output Format

### Context Assessment

```markdown
## Context Assessment

| Dimension | Reading | Signal |
|-----------|---------|--------|
| Volume | {Light/Medium/Heavy} | {X tasks} |
| Energy | {Low/Medium/High} | {indicators} |
| Resistance | {Low/Medium/High} | {indicators} |
| Time | {Full/Half/Fragments} | {X hours available} |
| Type | {Deep/Admin/Mixed} | {dominant task type} |

## Recommendation

**Primary Method:** {method name}
**Rationale:** {why this fits context}

**Alternative:** {backup method}
**When to switch:** {trigger condition}

## Quick Start
{3-5 lines to begin immediately}
```

### Method Suggestion

```markdown
## Suggested Method: {name}

**Context match:**
- Volume: {match} ✓
- Energy: {match} ✓
- Resistance: {match} ✓

**How to use today:**
1. {step 1}
2. {step 2}
3. {step 3}

**Start now with:** {first action}
```
