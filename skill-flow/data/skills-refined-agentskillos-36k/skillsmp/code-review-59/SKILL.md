---
name: code-review
description: Use for requesting and receiving code reviews - dispatch reviewer agent for self-review, verify feedback before implementing, no performative agreement
---

# Code Review

## Overview

Code review requires technical evaluation, not emotional performance. Request reviews early, receive feedback with rigor.

**Core principles:**
- **Requesting:** Review early, review often. Catch issues before they cascade.
- **Receiving:** Verify before implementing. Technical correctness over social comfort.

**Announce at start:** "I'm using gambit:code-review to [request/receive] review."

## Rigidity Level

MEDIUM FREEDOM - Follow the self-review checklist strictly before requesting. Verify all feedback before implementing. Adapt review scope to context. No performative agreement.

## Quick Reference

### Requesting Review

| Step | Action | STOP If |
|------|--------|---------|
| 1 | Run self-review checklist | Critical issues found |
| 2 | Dispatch code-reviewer agent | - |
| 3 | Act on feedback by severity | Critical unfixed |

### Receiving Review

| Step | Action | STOP If |
|------|--------|---------|
| 1 | Read complete feedback | - |
| 2 | Restate requirement in own words | Any item unclear |
| 3 | Verify against codebase | Feedback breaks things |
| 4 | Implement one item at a time | Tests fail |

**Forbidden responses:** "You're absolutely right!", "Great point!", "Thanks for catching that!"

---

## Part 1: Requesting Review

### When to Request

**Mandatory:**
- After completing Task from epic
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

### Step 1: Self-Review Checklist

**BEFORE dispatching reviewer, verify:**

```bash
# Run all automated checks
Task
  subagent_type: "hyperpowers:test-runner"
  prompt: "Run: go test ./... && golangci-lint run"
```

**Automated checks:**
- [ ] All tests pass
- [ ] No linter warnings
- [ ] No TODOs without issue numbers: `grep -r "TODO" src/ | grep -v "#"`
- [ ] No stub implementations: `grep -r "unimplemented\|todo!\|panic" src/`
- [ ] No unsafe patterns in production: `grep -r "\.unwrap()\|\.expect(" src/`

**Code quality self-check:**
- [ ] Error handling proper (Result/Option, not panic)
- [ ] Edge cases handled (empty, nil, boundaries)
- [ ] Names clear (would junior understand in 6 months?)
- [ ] No "while I'm here" changes mixed in
- [ ] Tests meaningful (not tautological)

**If any critical issues found:** Fix before requesting review.

### Step 2: Dispatch Code-Reviewer Agent

**First, get git SHAs:**

```bash
BASE_SHA=$(git rev-parse HEAD~N)  # or origin/main for full branch diff
HEAD_SHA=$(git rev-parse HEAD)
```

**Then dispatch with this template:**

```
Task
  subagent_type: "feature-dev:code-reviewer"
  description: "Review [brief description]"
  prompt: |
    Review the changes in this commit range:

    ## What Was Implemented
    {WHAT_WAS_IMPLEMENTED}
    [Brief description of what you built]

    ## Requirements
    {PLAN_OR_REQUIREMENTS}
    [What it should do - from Task or epic]

    ## Commit Range
    Base: {BASE_SHA}
    Head: {HEAD_SHA}

    ## Specific Concerns
    {CONCERNS}
    [Areas you're uncertain about]

    ## Review Focus
    - Does implementation match requirements?
    - Are there bugs, edge cases missed?
    - Is error handling sufficient?
    - Are tests meaningful (not tautological)?
    - Is code clear and maintainable?

    Return findings as:
    - Critical: [Must fix before merge]
    - Important: [Should fix before proceeding]
    - Minor: [Note for future]
    - Strengths: [What's done well]
```

**Template placeholders:**
| Placeholder | Description |
|-------------|-------------|
| `{WHAT_WAS_IMPLEMENTED}` | What you just built |
| `{PLAN_OR_REQUIREMENTS}` | What it should do (from Task) |
| `{BASE_SHA}` | Starting commit |
| `{HEAD_SHA}` | Ending commit |
| `{CONCERNS}` | Areas you're uncertain about |

### Step 3: Act on Feedback

**By severity:**

| Severity | Action |
|----------|--------|
| **Critical** | Fix immediately. Do not proceed until fixed. |
| **Important** | Fix before proceeding to next Task. |
| **Minor** | Note for later. OK to defer. |

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

---

## Part 2: Receiving Review

### The Response Pattern

```
WHEN receiving feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

### Forbidden Responses

**NEVER:**
- "You're absolutely right!" (performative)
- "Great point!" / "Excellent feedback!" (performative)
- "Thanks for catching that!" (performative)
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

### Handling Unclear Feedback

**IF any item is unclear:**

```
STOP - do not implement anything yet
ASK for clarification on unclear items
```

**Why:** Items may be related. Partial understanding = wrong implementation.

**Example:**
```
Reviewer: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

### Verifying Feedback Before Implementing

**BEFORE implementing external feedback:**

1. **Check:** Technically correct for THIS codebase?
2. **Check:** Breaks existing functionality?
3. **Check:** Reason for current implementation?
4. **Check:** Works on all platforms/versions?
5. **Check:** Does reviewer understand full context?

**IF suggestion seems wrong:**
- Push back with technical reasoning
- Show code/tests that prove current approach works

**IF can't easily verify:**
- Say so: "I can't verify this without [X]. Should I investigate?"

**IF conflicts with prior architectural decisions:**
- Stop and discuss before implementing

### YAGNI Check for "Professional" Features

**IF reviewer suggests "implementing properly":**

```bash
# Check if feature is actually used
grep -r "functionName" src/
```

- If unused: "This function isn't called. Remove it (YAGNI)?"
- If used: Then implement properly

### Implementation Order

**FOR multi-item feedback:**

1. Clarify anything unclear FIRST
2. Then implement in this order:
   - Blocking issues (breaks, security)
   - Simple fixes (typos, imports)
   - Complex fixes (refactoring, logic)
3. Test each fix individually
4. Verify no regressions

### When to Push Back

**Push back when:**
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Escalate if architectural

### Acknowledging Correct Feedback

**When feedback IS correct:**

```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
```

**Why no performative agreement:** Actions speak. Just fix it. The code itself shows you heard.

### Correcting Your Pushback

**If you pushed back and were wrong:**

```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified and you're correct. My understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

State the correction factually and move on.

---

## Critical Rules

### Rules That Have No Exceptions

1. **Run self-review checklist before requesting** → Don't waste reviewer time on obvious issues
2. **No performative agreement** → Technical acknowledgment or pushback only
3. **Verify feedback before implementing** → Check if it breaks things
4. **Clarify unclear items FIRST** → Don't implement partial understanding
5. **Test each fix individually** → One at a time, verify no regressions
6. **Push back with technical reasoning** → Not defensiveness, not blind acceptance

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Skip self-review | Always run checklist before requesting |

---

## Examples

### Bad: Performative Agreement

```
Reviewer: "Remove legacy code"

❌ "You're absolutely right! Let me remove that..."
[Removes code without checking if it's actually unused]
[Build breaks because legacy code was still called]
```

### Good: Technical Verification

```
Reviewer: "Remove legacy code"

✅ "Checking..."
$ grep -r "legacyFunction" src/
src/handler.go:45: result := legacyFunction(data)

"legacyFunction is still called at handler.go:45. Should I:
A) Update handler to use new function, then remove legacy?
B) Keep legacy for now until handler is migrated?
C) Something else?"
```

### Bad: Blind Implementation

```
Reviewer: "Use async/await pattern here"

[Implements async/await without checking]
[Breaks because caller doesn't handle promises]
[Introduces race condition in tests]
```

### Good: Verify Then Implement

```
Reviewer: "Use async/await pattern here"

✅ "Checking callers..."
$ grep -r "functionName" src/
3 callers found, all synchronous

"Converting to async would require updating 3 callers:
- handler.go:45
- service.go:78
- batch.go:112

Want me to update all callers, or keep synchronous for now?"
```

### YAGNI Example

```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"

✅ "Checking usage..."
$ grep -r "metricsEndpoint" src/
[no results]

"Nothing calls metricsEndpoint. Remove it (YAGNI)?
Or is there usage I'm missing?"
```

### Unclear Feedback Example

```
Reviewer: "Fix items 1-6"

Items 1,2,3,6: Clear
Items 4,5: Unclear what specifically to change

❌ WRONG:
"Fixing 1,2,3,6 now..."
[Implements partial, asks about 4,5 after]

✅ RIGHT:
"I understand items 1,2,3,6. Need clarification on 4 and 5:
- Item 4 mentions 'proper error handling' - which function?
- Item 5 says 'update tests' - add new tests or modify existing?

Will implement all 6 once clarified."
```

---

## Verification Checklist

### Before Requesting Review
- [ ] All tests pass (verified with test-runner)
- [ ] No linter warnings
- [ ] No TODOs without issue numbers
- [ ] No stub implementations
- [ ] Error handling proper
- [ ] Edge cases handled
- [ ] Names clear
- [ ] Tests meaningful (not tautological)

### After Receiving Review
- [ ] Read complete feedback without reacting
- [ ] Restated unclear items (or asked for clarification)
- [ ] Verified feedback against codebase
- [ ] Evaluated if technically sound
- [ ] Pushed back on incorrect suggestions (with reasoning)
- [ ] Implemented one item at a time
- [ ] Tested after each fix
- [ ] Verified no regressions

**Can't check all boxes?** Return to process.

---

## Integration

**This skill calls:**
- `gambit:verify` (for self-review verification)
- feature-dev:code-reviewer agent (for requesting review)
- test-runner agent (for running tests)

**This skill is called by:**
- `gambit:execute-plan` (after each Task)
- Before merging to main
- When stuck and need fresh perspective

**Workflow:**
```
Complete Task
    ↓
gambit:code-review (requesting)
    ↓
Self-review checklist
    ↓
Dispatch code-reviewer agent
    ↓
Receive feedback
    ↓
gambit:code-review (receiving)
    ↓
Verify → Implement → Test
    ↓
Ready for next Task
```

---

## Resources

**Self-review patterns:**
- Run automated checks FIRST
- Check edge cases: empty, nil, max, unicode
- Ask "would junior understand this in 6 months?"
- Check test meaningfulness (not tautological)

**When to push back:**
- Breaks existing functionality → Show failing test
- YAGNI → Show grep proving unused
- Wrong for this stack → Explain constraint
- Lacks context → Provide missing context

**When stuck:**
- Feedback unclear → Ask before implementing
- Feedback seems wrong → Verify, then push back with evidence
- Feedback breaks things → Report what breaks, ask how to proceed
- Multiple items → Clarify all, then implement in order
