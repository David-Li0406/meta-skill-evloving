---
name: ask-questions-if-underspecified
description: Use this skill to clarify requirements before implementing a task, ensuring all necessary information is gathered to avoid miscommunication and incorrect work.
---

# Ask Questions If Underspecified

## Goal

Ask the minimum set of clarifying questions needed to avoid wrong work; do not start implementing until the must-have questions are answered (or the user explicitly approves proceeding with stated assumptions).

## Workflow

### 1) Decide whether the request is underspecified

Treat a request as underspecified if after exploring how to perform the work, some or all of the following are not clear:
- Define the objective (what should change vs stay the same)
- Define "done" (acceptance criteria, examples, edge cases)
- Define scope (which files/components/users are in/out)
- Define constraints (compatibility, performance, style, dependencies, time)
- Identify environment (language/runtime versions, OS, build/test runner)
- Clarify safety/reversibility (data migration, rollout/rollback, risk)

If multiple plausible interpretations exist, assume it is underspecified.

### 2) Ask must-have questions first (keep it small)

Ask 1-5 questions in the first pass. Prefer questions that eliminate whole branches of work.

Make questions easy to answer:
- Optimize for scannability (short, numbered questions; avoid paragraphs)
- Offer multiple-choice options when possible
- Suggest reasonable defaults when appropriate (mark them clearly as the default/recommended choice; bold the recommended choice in the list)
- Include a fast-path response (e.g., reply `defaults` to accept all recommended/default choices)
- Include a low-friction "not sure" option when helpful (e.g., "Not sure - use default")
- Separate "Need to know" from "Nice to know" if that reduces friction
- Structure options so the user can respond with compact decisions (e.g., `1b 2a 3c`); restate the chosen options in plain language to confirm

### 3) Pause before acting

Until must-have answers arrive:
- Do not run commands, edit files, or produce a detailed plan that depends on unknowns
- Perform a clearly labeled, low-risk discovery step only if it does not commit you to a direction (e.g., inspect repo structure, read relevant config files)

If the user explicitly asks you to proceed without answers:
- State your assumptions as a short numbered list
- Ask for confirmation