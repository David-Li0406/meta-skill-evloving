---
name: code-review-skill
description: Provide structured software code reviews that confirm scope, focus on root causes, evaluate tests, and enforce project conventions.
---

# Code Review Skill

Use this when the user requests a review of code, pull requests, or diffs. Load the smallest relevant context first (changed files, linked tickets, reproduction steps) before drilling into implementation details.

## Review flow

1. **Establish scope**
   - Summarize the change intent, affected components, and linked issues.
   - Ask for missing diffs, runtime configuration, or reproduction instructions.
2. **Trace the cause**
   - Important: try to fix things at the cause, not the symptom. Follow data flow upstream to ensure the change touches the real source of the problem.
   - Flag quick fixes that mask deeper defects or debt.
3. **Manage context**
   - Pin key files and collapse unrelated noise.
   - Record assumptions and request clarification when signals conflict.
4. **Validate correctness**
   - Inspect logic paths, edge cases, and concurrency or performance concerns.
   - Map existing tests to behaviors; specify new tests or instrumentation when coverage is thin.
5. **Check conventions**
   - Compare against architecture and style guides. Surface deviations with concrete alternatives or references.
6. **Communicate outcomes**
   - Grade findings by severity (blocker, follow-up, nit).
   - Offer actionable edits, test commands, or documentation updates.

## Response template

```
### Findings
- [severity] file:line — issue + why it matters

### Questions
- Clarifications needed to proceed

### Recommended actions
- Ordered list of fixes, tests, or follow-ups
```

## Safeguards

- If critical context is missing, pause and ask for it instead of guessing.
- Never suggest destructive git commands unless the user has already used them in the conversation.
- When advising on tests, prefer deterministic automated coverage; call out manual validation only when unavoidable.
