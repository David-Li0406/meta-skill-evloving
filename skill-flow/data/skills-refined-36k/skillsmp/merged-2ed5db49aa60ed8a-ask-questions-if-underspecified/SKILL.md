---
name: ask-questions-if-underspecified
description: Use this skill to clarify requirements before implementing changes when a request is underspecified or ambiguous. It helps ensure you gather the minimum must-have questions to avoid misinterpretation and wrong work.
---

# Ask Questions If Underspecified

## Goal

Ask the minimum set of clarifying questions needed to avoid wrong work. Do not start implementing until the must-have questions are answered or the user explicitly approves proceeding with stated assumptions.

## Workflow

### 1) Decide whether the request is underspecified

Treat a request as underspecified if one or more of the following are unclear:
- Objective (what should change vs. stay the same)
- “Done” (acceptance criteria, examples, edge cases)
- Scope (which files/components/users are in/out)
- Constraints (compatibility, performance, style, dependencies, time)
- Environment (runtime versions, OS, build/test runner)
- Safety/reversibility (migration/rollback risk)

If there are multiple plausible interpretations, assume it is underspecified.

### 2) Ask must-have questions first

Ask 1–5 questions in the first pass, focusing on those that eliminate whole branches of work. Make them easy to answer:
- Use numbered questions with short options (yes/no or a/b/c)
- Recommend defaults when reasonable
- Provide a fast-path response (e.g., “reply `defaults`”)
- Separate “Need to know” from “Nice to know” when helpful

### 3) Pause before acting

Until must-have answers arrive:
- Do not run commands, edit files, or produce a detailed plan that depends on unknowns.
- Allow low-risk discovery reads (repo structure/configs) if they do not commit to a direction.

### 4) Confirm interpretation, then proceed

Once answered, restate requirements in 1–3 sentences (including key constraints and what success looks like), then start work.

## Response format

Use a compact, scannable structure. Example:

```text
Need to know
1) Scope?
   a) **Minimal change**
   b) Refactor while touching the area
   c) Not sure - use default
2) Compatibility target?
   a) **Current project defaults**
   b) Also support older versions: <specify>
   c) Not sure - use default
Reply with: defaults (or 1a 2a)
```

## If asked to proceed without answers

- State assumptions as a short numbered list.
- Ask for confirmation.
- Proceed only after confirmation or corrections.

## Anti-patterns

- Don’t ask questions you can answer via quick, low-risk discovery (configs/docs/grep).
- Don’t ask open-ended questions when a tight multiple-choice would resolve ambiguity faster.