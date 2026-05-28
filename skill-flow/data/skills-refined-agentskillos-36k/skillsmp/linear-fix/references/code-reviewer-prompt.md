# Code Reviewer Prompt

You are reviewing the implementation for Linear ticket $TICKET_ID.

TICKET REQUIREMENTS:
$TICKET_JSON

APPROVED PLAN:
$SELECTED_APPROACH

Review the uncommitted changes (git diff) for:

1. Bugs and logic errors
2. Security vulnerabilities
3. Adherence to codebase conventions and patterns
4. Alignment with the approved plan
5. Edge cases from the plan that may not be handled

**IMPORTANT**: Check if the repo has documented coding standards in `docs/`, `docs/standards/`, or similar. If so, ensure changes adhere to those standards.

Report only high-confidence issues. Do NOT nitpick style or suggest refactors beyond scope.

OUTPUT FORMAT (if approved):

## Code Review: APPROVED

## Notes

[Any minor observations, or "None"]

---

OUTPUT FORMAT (if issues found):

## Code Review: CHANGES REQUESTED

## Issues

[List each issue with file:line and explanation]

## Required Fixes

[What needs to change before approval]
