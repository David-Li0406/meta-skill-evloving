---
name: systematic-debugging
description: Use this skill when encountering bugs, test failures, or unexpected behavior, employing a hypothesis-driven debugging approach.
---

# Systematic Debugging Workflow

You are executing the **SYSTEMATIC DEBUGGING** workflow - a structured process for identifying and resolving issues through hypothesis-driven investigation.

## Contents

- [Problem Context](#problem-context)
- [Workflow Overview](#workflow-overview)
- [Phase Details](#phase-details)
- [Ask For Help Mechanism](#ask-for-help-mechanism)
- [Error Handling](#error-handling)

---

## Problem Context

$ARGUMENTS

If no specific problem was provided, you will help the user define the problem clearly.

---

## Workflow Overview

This command orchestrates a 6-phase workflow:

| Phase | Name                | Purpose                                           |
|-------|---------------------|---------------------------------------------------|
| 1     | Reproduce           | Trigger the issue consistently                    |
| 2     | Investigate         | Gather evidence and trace data flow               |
| 3     | Hypothesize         | Form a specific theory about the root cause      |
| 4     | Test                | Verify the hypothesis with minimal changes        |
| 5     | Fix                 | Address the root cause based on findings          |
| 6     | Verify              | Confirm the fix works and the problem is resolved |

---

## Phase Details

### Phase 1: Reproduce

- Document exact steps to reproduce the issue, including expected vs actual behavior and full error messages.
- If the issue cannot be reproduced, gather more data instead of guessing.

### Phase 2: Investigate

1. Read error messages completely, including line numbers and stack traces.
2. Check recent changes in the codebase.
3. Trace data flow by adding logging at component boundaries.

### Phase 3: Hypothesize

- Form one specific theory about the root cause, avoiding vague statements.

### Phase 4: Test

- Implement the smallest possible change to verify the hypothesis.
- If confirmed, proceed to fix; if not, return to hypothesis formation.

### Phase 5: Fix

- Address the root cause rather than applying superficial fixes.
- Document what was changed.

### Phase 6: Verify

- Write tests that fail before the fix and pass afterward to confirm the resolution.

---

## Ask For Help Mechanism

To prevent spinning wheels, this workflow includes an "ask for help" mechanism.

### When to Trigger

Ask for help when:

1. No progress on hypothesis after multiple attempts.
2. Conflicting evidence arises.
3. Access limitations prevent gathering necessary data.
4. Domain knowledge is required for resolution.
5. Significant time has been spent without progress.

### How to Ask

```
## Seeking Additional Input

I've investigated [N] hypotheses but haven't identified the root cause.

### What I've Tried
1. [Hypothesis 1] - Ruled out because [evidence]
2. [Hypothesis 2] - Ruled out because [evidence]
3. [Hypothesis 3] - Inconclusive, need more data

### What Would Help
- [ ] Access to [specific logs/system]
- [ ] Information about [specific question]
- [ ] Someone with [domain] expertise
- [ ] Permission to [specific action]

### Questions for You

1. Have you seen this issue before?
2. Any recent changes that might be related?
3. Can you provide [specific information]?
4. Should we escalate to [team/person]?
```

---

## Error Handling

| Error                  | Resolution                                      |
|------------------------|-------------------------------------------------|
| Problem too vague      | Ask clarifying questions in Phase 1            |
| No hypotheses match    | Generate new hypotheses, ask for help          |
| Can't reproduce        | Gather more specific reproduction steps         |
| Fix doesn't work       | Return to Phase 3, form new hypotheses         |
| Multiple root causes   | Address each systematically                     |

---

## Philosophy: "Debug with Evidence, Not Intuition"

This workflow ensures:
- Problems are clearly defined before debugging.
- Investigation is systematic, not random.
- Hypotheses are tested with evidence.
- Fixes are verified, not assumed.
- Knowledge is preserved for future issues.

**Let's identify the problem and fix it systematically!**