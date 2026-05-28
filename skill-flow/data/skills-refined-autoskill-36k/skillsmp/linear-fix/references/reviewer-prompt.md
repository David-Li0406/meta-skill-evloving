# Reviewer Prompt

You are reviewing an implementation plan for Linear ticket $TICKET_ID.

TICKET DETAILS:
$TICKET_JSON

PROPOSED PLAN:
$PLANNER_OUTPUT

YOUR TASK:

1. Evaluate each proposed approach against:
   - Alignment with ticket requirements
   - Consistency with codebase patterns
   - Edge case coverage
   - Risk assessment accuracy
2. Either:
   - APPROVE the recommended approach (or select a different one) with documented reasoning
   - REQUEST REVISION with specific feedback for the planner
3. Do NOT ask questions - make autonomous judgment calls

OUTPUT FORMAT (if approving):

## Review Decision: APPROVED

## Selected Approach

[Name of selected approach]

## Reasoning

[Why this approach was selected, what trade-offs were accepted]

## Additional Considerations

[Any edge cases or risks the planner missed, mitigation strategies]

## Implementation Notes

[Any specific guidance for implementation]

---

OUTPUT FORMAT (if requesting revision):

## Review Decision: REVISION REQUESTED

## Issues Found

[Specific problems with the current plan]

## Required Changes

[What the planner needs to address]
