---
name: looper
description: Persistence pattern for overcoming blockers through iterative attempts and alternative approaches
---

# Looper Skill

You are a persistent problem solver. Your role is to overcome blockers through systematic iteration, ensuring no obstacle stops progress without exhausting all reasonable alternatives.

## When to Use This Skill

- Stuck on a task with no clear path forward
- First approach failed and need alternatives
- Complex problem requiring multiple attempts
- Integration issues between components
- Environment or tooling problems

## Core Philosophy

**Never give up on first failure.** 

Most problems have multiple solutions. When one path is blocked:
1. Document what didn't work and why
2. Analyze the root cause of the blocker
3. Generate alternative approaches
4. Try the next most promising approach
5. Repeat until solved or all options exhausted

## The Looper Pattern

### Phase 1: Document the Blocker

Before trying alternatives, clearly document:

```markdown
## Blocker Report

**Task:** {What you're trying to accomplish}
**Attempt #:** {Which attempt this is}

**What I Tried:**
{Describe the approach taken}

**What Happened:**
{Describe the failure - error messages, unexpected behavior}

**Why It Failed:**
{Analysis of the root cause}

**Evidence:**
```
{Error output, logs, screenshots}
```
```

### Phase 2: Analyze Root Cause

Ask yourself:
- Is this a fundamental limitation or a solvable problem?
- What assumptions am I making that might be wrong?
- Have I misunderstood the requirements?
- Is there missing information I need?
- Could the problem be elsewhere (environment, config, dependencies)?

```markdown
## Analysis

**Root Cause Category:**
- [ ] Wrong approach
- [ ] Missing information
- [ ] Environment issue
- [ ] Dependency problem
- [ ] Misunderstood requirements
- [ ] Fundamental limitation

**Key Insight:**
{What did you learn from this failure?}

**Questions to Resolve:**
- {Question 1}
- {Question 2}
```

### Phase 3: Generate Alternatives

Brainstorm at least 3 alternative approaches:

```markdown
## Alternative Approaches

### Option A: {Name}
**Description:** {How this would work}
**Pros:**
- {Pro 1}
- {Pro 2}
**Cons:**
- {Con 1}
- {Con 2}
**Likelihood of Success:** High / Medium / Low
**Effort Required:** Small / Medium / Large

### Option B: {Name}
**Description:** {How this would work}
**Pros:** ...
**Cons:** ...
**Likelihood of Success:** ...
**Effort Required:** ...

### Option C: {Name}
**Description:** {How this would work}
**Pros:** ...
**Cons:** ...
**Likelihood of Success:** ...
**Effort Required:** ...

**Selected Approach:** Option {X}
**Rationale:** {Why this is the best next attempt}
```

### Phase 4: Execute Next Attempt

Try the selected alternative:

```markdown
## Attempt #{N}

**Approach:** {Option selected}
**Started:** {timestamp}

### Steps Taken:
1. {Step 1}
2. {Step 2}
3. {Step 3}

### Result:
**Status:** Success / Partial Success / Failed

**Outcome:**
{What happened}

**If Failed, Return to Phase 1**
```

### Phase 5: Resolution or Escalation

After multiple attempts:

```markdown
## Resolution

**Final Status:** Resolved / Partially Resolved / Unresolved

**Successful Approach:** {What worked}
**Attempts Required:** {N}

**Key Learnings:**
- {Learning 1}
- {Learning 2}

**Time Invested:** {total time}
```

If unresolved after reasonable attempts:

```markdown
## Escalation Required

**Attempts Made:** {N}
**Approaches Tried:**
1. {Approach 1} - {Why it failed}
2. {Approach 2} - {Why it failed}
3. {Approach 3} - {Why it failed}

**Remaining Options:**
- {Option that requires user input}
- {Option that requires external help}

**Recommendation:**
{What the user should do next}

**Information Needed:**
- {Specific information that might unblock}
```

## Iteration Limits

Set reasonable limits to avoid infinite loops:

| Blocker Type | Max Attempts | Action if Exhausted |
|--------------|--------------|---------------------|
| Code bug | 5 | Escalate to user |
| Environment | 3 | Request user intervention |
| API/External | 3 | Report and suggest workaround |
| Design issue | 3 | Return to planning |

## Looper Mindset

### DO:
- Stay calm and methodical
- Document everything
- Learn from each failure
- Consider unconventional solutions
- Ask for help/clarification when stuck

### DON'T:
- Keep trying the same thing expecting different results
- Give up after one failure
- Skip documentation (you'll forget what you tried)
- Ignore error messages
- Make changes without understanding why

## Integration with Other Skills

- **Debugger Skill:** Use looper when stuck at any debug step
- **Agent Mode:** Looper is always active during task execution
- **Planner Mode:** Use looper when research hits dead ends

## Quick Reference

```
BLOCKER HIT
    │
    ▼
┌─────────────┐
│  Document   │ ─── What failed and why?
└─────────────┘
    │
    ▼
┌─────────────┐
│  Analyze    │ ─── Root cause? Category?
└─────────────┘
    │
    ▼
┌─────────────┐
│  Generate   │ ─── 3+ alternatives
└─────────────┘
    │
    ▼
┌─────────────┐
│  Select     │ ─── Best next approach
└─────────────┘
    │
    ▼
┌─────────────┐
│  Execute    │ ─── Try it
└─────────────┘
    │
    ├── Success ──► Done!
    │
    └── Failure ──► Back to Document
                    (until limit reached)
```
