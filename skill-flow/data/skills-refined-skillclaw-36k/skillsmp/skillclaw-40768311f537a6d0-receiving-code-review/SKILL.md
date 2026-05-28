---
name: receiving-code-review
description: Use this skill when processing code review feedback to ensure technical correctness before implementing any changes.
---

# Skill body

## Core Principle

**Verify before implementing. Ask before assuming. Technical correctness over social comfort.**

## Overview

Code review feedback requires technical evaluation, not performative agreement. This skill teaches how to receive, evaluate, and implement feedback professionally.

## The Iron Laws

### Law 1: Technical Evaluation Required

**Never blindly accept feedback.** Verify it's technically correct first.

### Law 2: No Performative Agreement

**Forbidden phrases:**
- ❌ "You're absolutely right!"
- ❌ "Great point!"
- ❌ "Good catch!"
- ❌ "Thanks for the feedback!"
- ❌ "I should have thought of that!"

**Why forbidden:** These are social lubricants, not technical responses. They signal submission rather than evaluation.

### Law 3: Verify Against Codebase

**Check actual code before responding.** The reviewer may be wrong or looking at an outdated version.

## Response Pattern (The Six Steps)

### Step 1: READ

Read feedback completely without reacting.

```
Reviewer feedback received:
"This function does too much. Split into smaller functions."

[Read completely, don't respond yet]
```

### Step 2: UNDERSTAND

Restate the requirement to confirm understanding.

```
Understanding check:
Reviewer suggests: Break down AuthController->login() into smaller methods

My understanding:
- Current login() method is ~80 lines
- Reviewer wants it split into multiple single-purpose methods
- Likely: validateCredentials(), generateToken(), logAuthEvent()

Is my understanding correct?
```

### Step 3: VERIFY

Check against actual codebase reality.

```
Verification:

Checking AuthController->login():
- Line count: 82 lines ✅ (confirms "too long")
- Complexity: 3 nested conditions
- Responsibilities: Validation, auth, token generation, logging, response

Verification: Reviewer's observation is accurate.
```

### Step 4: EVALUATE

Is the feedback technically sound?

```
Technical evaluation:

Pros of splitting:
- Single Responsibility Principle
- Easier to test individual parts
- More readable

Cons of splitting:
- More indirection
- Might be premature abstraction

Decision: Feedback is technically sound. Benefits outweigh costs.
```

### Step 5: RESPOND

Technical acknowledgment or reasoned pushback.

**If agreeing:**
```
Technical acknowledgment:
"I see the value in splitting the function for clarity and maintainability."
```

**If pushing back:**
```
Reasoned pushback:
"I believe the current implementation is sufficient because it meets the requirements without unnecessary complexity."
```

### Step 6: IMPLEMENT

Implement changes one item at a time, testing each.

---

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
Feedback: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.

WRONG: Implement 1,2,3,6 now, ask about 4,5 later
RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5."
```

---

## When to Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with prior architectural decisions

**How to push back:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests/code
- Escalate if architectural