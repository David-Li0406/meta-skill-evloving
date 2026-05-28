---
name: create-coding-plan
description: Create a concise, actionable coding plan. Triggers when user asks to "plan", "outline", "scope", or "break down" a coding task, or requests a checklist before implementation.
metadata:
  short-description: Create a plan
---

# Create Plan

## Goal

Turn a user prompt into a single, actionable plan delivered in your final response.

## Minimal workflow

Throughout the entire workflow, operate in read-only mode. Do not write or update files.

1. **Scan context quickly**
   - Read `README.md` and any obvious docs (`docs/`, `CONTRIBUTING.md`, `ARCHITECTURE.md`).
   - Skim relevant files (the ones most likely to be touched).
   - Identify constraints (language, frameworks, CI/test commands, deployment shape).

2. **Ask follow-ups only if blocking**
   - Ask at most 1–2 questions.
   - Only ask if you cannot responsibly plan without the answer, prefer multiple-choice.
   - If unsure but not blocked, make a reasonable assumption and proceed.

3. **Create a plan using the template below**
   - Start with 1 short paragraph describing intent and approach.
   - Call out what is in scope and out of scope.
   - Provide a small ordered checklist (default 6–10 items):
      - discovery → changes → tests → rollout
      - verb-first (“Add…”, “Refactor…”, “Verify…”)
   - Include at least one item for tests/validation and one for edge cases/risk when applicable.
   - If there are unknowns, include a tiny Open questions section (max 3).

4. **Output only the plan**

## Plan template (follow exactly)

```markdown
# Plan

<1–3 sentences: what we’re doing, why, and the high-level approach.>

## Scope
- In:
- Out:

## Action items
[ ] <Step 1>
[ ] <Step 2>
[ ] <Step 3>
[ ] <Step 4>
[ ] <Step 5>
[ ] <Step 6>

## Open questions
- <Question 1>
- <Question 2>
- <Question 3>
```

## Checklist item guidance

Good checklist items:
- Point to likely files/modules (e.g., `src/...`, `app/...`, `services/...`).
- Name concrete validation (e.g., “Run `npm test`”, “Add unit tests for X”).
- Include safe rollout when relevant (feature flag, migration plan, rollback note).

Avoid:
- Vague steps (“handle backend”, “do auth”).
- Too many micro-steps.
- Writing code snippets (keep the plan implementation-agnostic).
