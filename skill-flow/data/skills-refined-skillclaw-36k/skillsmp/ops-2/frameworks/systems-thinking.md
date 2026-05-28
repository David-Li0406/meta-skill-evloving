# Systems Thinking Framework

## Purpose

Build systems, not task lists. A system runs without you. A task list requires you.

---

## Systems vs Tasks

| Aspect | Task Approach | Systems Approach |
|--------|---------------|------------------|
| Trigger | "I need to do X" | "When Y happens, X occurs" |
| Dependency | You | The system |
| Scalability | Linear with time | Multiplicative |
| Reliability | Variable | Consistent |
| Knowledge | In your head | Documented |

---

## System Components

### Every System Has:

```
TRIGGER
What initiates the system?
├── Time-based (daily, weekly)
├── Event-based (new user, payment)
├── Threshold-based (metric hits X)
└── Request-based (support ticket)

INPUT
What information does the system need?
├── Data sources
├── Context required
└── Permissions needed

PROCESS
What steps transform input to output?
├── Step 1
├── Step 2
├── Decision points
└── Exception handling

OUTPUT
What does the system produce?
├── Actions taken
├── Artifacts created
├── Notifications sent
└── Records updated

FEEDBACK
How do we know it worked?
├── Success criteria
├── Quality checks
├── Metrics tracked
└── Error signals
```

---

## System Design Process

### Step 1: Identify the Job

**Questions:**
- What outcome are we trying to achieve?
- How often does this need to happen?
- What triggers the need?
- Who cares about the outcome?

### Step 2: Map Current State

**Document how it happens now:**
1. List every step you take
2. Note decision points
3. Identify information sources
4. Record time for each step
5. Mark what requires judgment

### Step 3: Design Target State

**Design the ideal system:**
1. What can be eliminated?
2. What can be automated?
3. What can be standardized?
4. What must stay manual?

### Step 4: Build Components

**Create system components:**
1. Write the SOP (even if automated)
2. Build automation where viable
3. Set up triggers
4. Create quality checks
5. Establish feedback loops

### Step 5: Test and Iterate

**Validate the system:**
1. Run it manually first
2. Check outputs match expectations
3. Handle edge cases
4. Automate confidence
5. Monitor and adjust

---

## System Categories

### Operational Systems

| System | Purpose | Typical Trigger |
|--------|---------|-----------------|
| Onboarding | New user setup | User signs up |
| Support | Handle issues | Ticket created |
| Billing | Manage payments | Payment due |
| Maintenance | Keep things running | Scheduled |
| Backup | Protect data | Scheduled |

### Marketing Systems

| System | Purpose | Typical Trigger |
|--------|---------|-----------------|
| Content | Publish regularly | Calendar |
| Email | Nurture leads | Behavior |
| Social | Build presence | Calendar |
| Analytics | Track performance | Weekly |

### Product Systems

| System | Purpose | Typical Trigger |
|--------|---------|-----------------|
| Release | Ship updates | Code ready |
| Monitoring | Catch issues | Always on |
| Feedback | Collect input | Usage events |
| Testing | Verify quality | Code change |

---

## Automation Decision Framework

### When to Automate

```
      HIGH VOLUME
           │
    ┌──────┼──────┐
    │ AUTOMATE    │ CONSIDER
SIMPLE─────┼──────┼─────COMPLEX
    │ SCRIPT      │ HYBRID
    └──────┼──────┘
           │
      LOW VOLUME
```

| Quadrant | Strategy |
|----------|----------|
| High volume + Simple | Full automation |
| High volume + Complex | Partial automation with human review |
| Low volume + Simple | Script or manual |
| Low volume + Complex | Manual (not worth automating) |

### Automation ROI Calculator

```
Hours saved per week × 50 weeks × Hourly value
────────────────────────────────────────────────
Hours to build + (Hours to maintain × 50)

If result > 2, automate.
```

---

## Feedback Loops

### Types of Feedback

| Type | Speed | Use Case |
|------|-------|----------|
| Real-time alerts | Instant | Errors, outages |
| Daily digest | 24 hours | Metrics, activity |
| Weekly review | 7 days | Trends, optimization |
| Monthly analysis | 30 days | Strategic decisions |

### Designing Good Feedback

**Effective feedback is:**
- Timely (arrives when useful)
- Actionable (tells you what to do)
- Proportional (severity matches urgency)
- Specific (points to the issue)

**Bad feedback:**
- Alert fatigue (too many notifications)
- Vague warnings ("something's wrong")
- Delayed signals (too late to act)
- Missing context (what happened?)

---

## System Documentation Template

```markdown
# System: {Name}

## Purpose
{One sentence: what this system achieves}

## Trigger
{What initiates this system}

## Inputs
- {Input 1}: {where it comes from}
- {Input 2}: {where it comes from}

## Process
1. {Step 1}
2. {Step 2}
3. {Step 3}
   - If {condition}: {action}
   - Else: {alternative}

## Outputs
- {Output 1}: {where it goes}
- {Output 2}: {where it goes}

## Feedback
- Success indicator: {how we know it worked}
- Error signal: {how we know it failed}
- Metrics tracked: {what we measure}

## Owner
{Who maintains this system}

## Review Schedule
{How often we evaluate and improve}
```

---

## System Health Indicators

### Signs of Healthy Systems

| Indicator | Healthy | Unhealthy |
|-----------|---------|-----------|
| Exceptions | Rare, documented | Frequent, ad-hoc |
| Manual intervention | Minimal | Constant |
| Output quality | Consistent | Variable |
| Documentation | Current | Outdated |
| Owner clarity | Clear | Ambiguous |

### System Audit Questions

1. When did this system last fail?
2. How long to recover?
3. Who knows how it works?
4. When was it last improved?
5. Is documentation current?

---

## Common System Failures

| Failure Mode | Symptom | Prevention |
|--------------|---------|------------|
| Single point of failure | Everything stops when X breaks | Redundancy, documentation |
| Undocumented exceptions | Chaos when edge case hits | Document all paths |
| Stale automation | Wrong outputs | Regular review |
| Missing feedback | Silent failures | Monitoring, alerts |
| Over-automation | Rigid, can't adapt | Keep humans in loop |

---

## Output Format

```markdown
## System Design: {Name}

### Job to Be Done
{What outcome this achieves}

### Current State
| Step | Time | Automated | Notes |
|------|------|-----------|-------|
| {step} | {X min} | {Y/N} | {notes} |

### Target State
| Component | Implementation |
|-----------|----------------|
| Trigger | {how initiated} |
| Process | {steps} |
| Automation | {tools/scripts} |
| Feedback | {how monitored} |

### Implementation Plan
1. {First action}
2. {Second action}
3. {Third action}

### Success Criteria
- {Metric 1}: {target}
- {Metric 2}: {target}
```
