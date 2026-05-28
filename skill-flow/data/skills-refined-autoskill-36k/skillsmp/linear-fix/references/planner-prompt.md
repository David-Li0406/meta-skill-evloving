# Planner Prompt

You are planning the implementation for Linear ticket $TICKET_ID.

TICKET DETAILS:
$TICKET_JSON

COMMENTS:
$TICKET_COMMENTS

REQUIREMENTS:

1. Explore the codebase thoroughly - understand existing patterns before proposing changes
2. Propose 2-3 distinct implementation approaches
3. For each approach, document:
   - Description and rationale
   - Files to create/modify
   - Trade-offs (pros/cons)
   - Risk assessment (low/medium/high)
   - Edge cases to handle
4. Recommend the best approach with clear justification
5. Do NOT ask questions - make judgment calls and document your reasoning

OUTPUT FORMAT:

## Codebase Analysis

[Relevant patterns, conventions, and architecture insights]

## Approach 1: [Name]

- Description: ...
- Files: ...
- Trade-offs: ...
- Risk: [low/medium/high]
- Edge cases: ...

## Approach 2: [Name]

...

## Approach 3 (optional): [Name]

...

## Recommendation

[Selected approach with detailed justification]
