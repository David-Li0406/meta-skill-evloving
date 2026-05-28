---
name: rapid-triage-reasoning
description: Fast decision-making methodology for time-critical situations. Use when you have minutes (not hours) to decide, during incidents, emergencies, or hard deadlines. Optimizes for "good enough now" over "perfect later". Unlike other patterns that maximize quality, RTR maximizes decision speed while maintaining acceptable quality floors.
license: MIT
---

# Rapid Triage Reasoning (RTR)

**Purpose**: Make defensible decisions under extreme time pressure. RTR accepts that perfect is the enemy of good when time is the critical constraint.

## When to Use Rapid Triage Reasoning

**Use RTR when:**
- Decision needed in minutes, not hours
- Production incident requiring immediate action
- Hard deadline with no extension possible
- Stakes of delay exceed stakes of suboptimal choice
- "No decision" is worse than "imperfect decision"

**Don't use RTR when:**
- You actually have time (even if it feels urgent)
- Decision is irreversible AND high-stakes (take the time)
- Problem requires deep analysis (flag for later, make temporary decision)
- You can buy time by acknowledging the problem

**RTR vs Other Patterns:**
- ToT: When you need THE BEST (RTR: when you need SOMETHING GOOD NOW)
- HE: When you need THE CAUSE (RTR: when you need TO ACT before knowing cause)
- BoT: When you need ALL OPTIONS (RTR: when you need ONE OPTION FAST)

---

## Core Methodology: RAPID Framework

### R - Recognize Constraints

**Goal**: Explicitly acknowledge time pressure and scope limits

**Process** (30 seconds):
1. State the hard deadline: "Decision needed by [TIME]"
2. State consequences of delay: "If we don't decide by then, [CONSEQUENCE]"
3. State quality floor: "Minimum acceptable outcome is [THRESHOLD]"
4. Acknowledge what you're sacrificing: "We may miss [OPTIMIZATION]"

**Template:**
```markdown
## Time Constraint Recognition

**Deadline**: [Specific time or duration]
**Cost of Delay**: [What happens if we miss deadline]
**Quality Floor**: [Minimum acceptable outcome]
**Acceptable Sacrifice**: [What we're giving up for speed]
```

**Example:**
```markdown
## Time Constraint Recognition

**Deadline**: 5 minutes (users experiencing errors NOW)
**Cost of Delay**: Every minute = ~100 failed transactions
**Quality Floor**: Stop the bleeding, even if not root cause fix
**Acceptable Sacrifice**: May need to revisit with proper fix later
```

---

### A - Assess Available Options

**Goal**: Generate options you can actually execute in time

**Process** (1-2 minutes):
1. List ONLY options executable within deadline
2. Don't waste time on options that require unavailable resources
3. Include "do nothing / wait" as explicit option
4. Include "reversible quick fix" options
5. Maximum 4 options (cognitive limit under pressure)

**Feasibility Filter:**
```markdown
| Option | Executable in Time? | Reversible? | Keep? |
|--------|---------------------|-------------|-------|
| [Option 1] | Yes/No | Yes/No | Yes/No |
| [Option 2] | Yes/No | Yes/No | Yes/No |
```

**Discard any option where "Executable in Time" = No**

**Template:**
```markdown
## Viable Options (Max 4)

### Option 1: [Name]
- **Action**: [Specific steps]
- **Time to Execute**: [Minutes]
- **Reversible**: [Yes/No/Partially]

### Option 2: [Name]
...

### Option N: Do Nothing / Wait
- **Action**: Accept current state
- **Rationale**: [When this is actually correct]
```

---

### P - Prioritize by Reversibility

**Goal**: Prefer reversible actions when uncertain

**Reversibility Hierarchy:**
1. **Fully Reversible** (Prefer): Can undo with no lasting effects
2. **Partially Reversible**: Can mitigate but not fully undo
3. **Irreversible** (Caution): Cannot undo, permanent consequences

**Decision Rule:**
- If uncertain AND options have similar outcomes → Choose most reversible
- If one option clearly better AND irreversible → Still okay if confidence >70%
- If uncertain AND must choose irreversible → Get second opinion if ANY time remains

**Quick Assessment Matrix:**
```markdown
| Option | Expected Outcome | Confidence | Reversibility | Score |
|--------|------------------|------------|---------------|-------|
| A | [Outcome] | [%] | [1-3] | [Calc] |
| B | [Outcome] | [%] | [1-3] | [Calc] |

Score = Confidence × (Reversibility + 1) / 4
Prefer highest score
```

---

### I - Implement with Checkpoints

**Goal**: Start acting while maintaining ability to course-correct

**Process:**
1. Begin executing chosen option IMMEDIATELY
2. Set checkpoint at 25% and 50% of remaining time
3. At each checkpoint: Is it working? Continue or pivot?
4. Document what you're doing (brief notes, not essays)

**Checkpoint Template:**
```markdown
## Execution Log

**Started**: [Time]
**Action**: [What we're doing]

### Checkpoint 1 (25%): [Time]
- Working? [Yes/Partially/No]
- Continue? [Yes/Pivot to Option X]

### Checkpoint 2 (50%): [Time]
- Working? [Yes/Partially/No]
- Continue? [Yes/Pivot to Option X]
```

**Pivot Rules:**
- Pivot if current action is clearly not working
- Don't pivot just because you thought of something better
- Pivot to next option in priority list, don't re-analyze

---

### D - Document for Follow-up

**Goal**: Enable proper analysis after the crisis

**Process** (do WHILE acting, not after):
1. Note what you tried and results
2. Flag items for post-incident review
3. Capture hypotheses you didn't have time to test
4. Note any technical debt created

**Template:**
```markdown
## RTR Decision Record

**Situation**: [1-sentence summary]
**Time Pressure**: [Why urgent]
**Decision Made**: [What we chose]
**Rationale**: [Why, in 1-2 sentences]
**Outcome**: [What happened]

### Follow-up Required
- [ ] [Investigation or fix needed]
- [ ] [Technical debt to address]
- [ ] [Root cause analysis with HE]
```

---

## Time Budgets by Scenario

| Scenario | Total Time | R | A | P | I | D |
|----------|------------|---|---|---|---|---|
| **5-minute incident** | 5 min | 30s | 1m | 30s | 2.5m | 30s |
| **15-minute deadline** | 15 min | 1m | 3m | 2m | 8m | 1m |
| **30-minute decision** | 30 min | 2m | 5m | 3m | 18m | 2m |
| **1-hour critical** | 60 min | 3m | 10m | 7m | 35m | 5m |

**If you have >1 hour, consider if RTR is actually needed**

---

## Pre-Built Triage Patterns

### Pattern 1: Production Incident Triage

```markdown
## Incident Triage (5 minutes)

### Immediate Questions (1 min)
1. What's the user impact? [Severity 1-4]
2. Is it getting worse? [Yes/No/Stable]
3. When did it start? [Time]
4. Any recent changes? [Yes/No]

### Triage Decision Tree (1 min)
- Recent deploy? → Rollback first, investigate second
- External dependency down? → Failover or graceful degradation
- Resource exhaustion? → Scale up or restart
- Unknown? → Enable verbose logging, restart if safe

### Action (3 min)
[Execute chosen action, monitor]

### Document (ongoing)
[Brief notes for postmortem]
```

### Pattern 2: Meeting Decision Triage

```markdown
## Meeting Decision (2 minutes before deadline)

### Frame (15s)
"We need to decide [X] in the next 2 minutes"

### Options (30s)
"Our options are: A, B, or defer to [person/time]"

### Quick Poll (30s)
"Any strong objections to [recommended option]?"

### Decide (15s)
"Going with [option]. We can revisit in [timeframe] if needed"

### Document (30s)
[Note decision, rationale, revisit date]
```

### Pattern 3: Technical Triage

```markdown
## Technical Decision Under Pressure

### Constraint Check (30s)
- Time available: [X minutes]
- Reversibility requirement: [High/Medium/Low]
- Blast radius if wrong: [Small/Medium/Large]

### Option Generation (1 min)
- Conservative option: [Safest choice]
- Aggressive option: [Fastest/best if works]
- Middle ground: [Balance]

### Selection (30s)
IF blast radius = Large → Conservative
ELSE IF time < 10min → Aggressive (if reversible)
ELSE → Middle ground

### Execute
[Go with selected option]
```

---

## Common Mistakes

1. **Fake Urgency**: Treating everything as urgent
   - Fix: Ask "What happens if I take 30 more minutes?"
   - If answer is "nothing much" → Not RTR territory

2. **Analysis Paralysis Under Pressure**: Freezing when time is short
   - Fix: Force yourself to pick within time budget
   - Any decision > No decision (usually)

3. **Skipping Documentation**: "I'll remember later"
   - Fix: Document WHILE acting, even if brief
   - Future you will thank present you

4. **Cowboy Decisions**: Using time pressure to avoid review
   - Fix: RTR still requires stating rationale
   - "No time to explain" is a red flag

5. **Not Following Up**: Making RTR decisions permanent
   - Fix: Always flag for follow-up
   - RTR is triage, not treatment

---

## RTR Quality Metrics

Unlike other methodologies that optimize for decision QUALITY, RTR optimizes for:

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Decision Time** | Within deadline | Did we decide in time? |
| **Quality Floor** | Met minimum threshold | Did outcome meet minimum? |
| **Reversibility Preference** | Chose reversible when uncertain | Could we undo if wrong? |
| **Follow-up Rate** | 100% get follow-up | Did we revisit the decision? |
| **Regret Rate** | <20% | Would we decide differently with more time? |

**Acceptable RTR Outcome**: Decision made in time, met quality floor, documented for follow-up.

**RTR is NOT about making perfect decisions. It's about making good-enough decisions fast enough to matter.**

---

## Integration with Other Patterns

**RTR as Starting Point:**
- RTR (triage) → HE (root cause after stabilization)
- RTR (quick fix) → ToT (proper solution design)
- RTR (incident) → AR (post-incident security review)

**RTR Escalation:**
If during RTR you realize:
- This is actually not urgent → Exit RTR, use appropriate pattern
- This requires expertise you lack → Escalate, don't guess
- The options all look terrible → Document and escalate

---

## Output Template

```markdown
# RTR Decision Record: [Situation]

## Constraints
- **Deadline**: [When]
- **Cost of Delay**: [What]
- **Quality Floor**: [Minimum acceptable]

## Options Considered
1. [Option A] - [Time: Xm, Reversible: Y/N]
2. [Option B] - [Time: Xm, Reversible: Y/N]
3. [Option C] - [Time: Xm, Reversible: Y/N]

## Decision
**Chosen**: [Option]
**Rationale**: [1-2 sentences]
**Confidence**: [%] (lower is expected in RTR)

## Execution
- Started: [Time]
- Checkpoints: [What happened]
- Outcome: [Result]

## Follow-up Required
- [ ] [Item 1]
- [ ] [Item 2]

## Post-Incident Review
[To be completed after crisis passes]
```

---

## Version History

**V1.0** (Current):
- Initial release
- RAPID framework (Recognize, Assess, Prioritize, Implement, Document)
- Pre-built patterns for incidents, meetings, technical decisions
- Time budgets for different scenarios
- Integration points with HE, ToT, AR for follow-up
