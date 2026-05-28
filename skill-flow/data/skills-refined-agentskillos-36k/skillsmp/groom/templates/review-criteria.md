# Self-Review Checklist

Use this checklist to review drafted issues before presenting to the user.

## Issue Quality

- [ ] Description clearly explains what and why
- [ ] Acceptance criteria are specific and testable
- [ ] Out of scope section defines clear boundaries
- [ ] No ambiguous language or undefined terms
- [ ] All user decisions have been incorporated

## Codebase Alignment

- [ ] Approach aligns with existing codebase patterns
- [ ] Referenced files/modules actually exist
- [ ] Complexity estimate is realistic given codebase
- [ ] No conflicts with existing features
- [ ] Technical terminology matches project conventions

## Labels

- [ ] Type label is set (bug, feature, enhancement, etc.)
- [ ] Area label is set if applicable (area:auth, area:storage, etc.)
- [ ] Labels are appropriate for the issue content

## Completeness

- [ ] Ready for implementation without further clarification
- [ ] No open questions remain unaddressed
- [ ] Edge cases have been considered
- [ ] Dependencies (if any) are identified

## Priority

- [ ] Priority label has been suggested or assigned
- [ ] Priority level is appropriate given impact and urgency

## Common Issues to Fix

**Before presenting to user, fix:**

- Vague acceptance criteria ("works correctly" -> specific behavior)
- Missing scope boundaries
- Undefined technical terms
- Unreferenced or non-existent patterns
- Overly complex approaches when simpler ones exist

**Note to raise with user:**

- Potential conflicts with existing features
- Architectural trade-offs not yet discussed
- Scope items that could go either way
- Discovered complexity that affects estimates
