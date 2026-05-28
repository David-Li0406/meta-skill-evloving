# Interview Skill

Conducts in-depth interviews about features, specs, or ideas to surface non-obvious concerns, edge cases, and tradeoffs.

## Usage

```
/interview                                    # Ask what to discuss
/interview "user authentication flow"         # Interview about a topic
/interview docs/03-build-notes/milestones/m1/01-auth.md  # Interview about existing spec
```

## What It Does

1. Systematically probes key areas:
   - Technical implementation
   - UI/UX considerations
   - Operational concerns
   - Security and privacy
   - Performance and scalability
   - Maintainability

2. Asks thoughtful questions to surface:
   - Edge cases and failure modes
   - Tradeoffs and alternatives
   - Dependencies and integration points
   - Risks and open questions

3. Synthesizes findings into actionable output

## When to Use

- Before creating a new issue spec
- When requirements are unclear
- To think through implementation details
- To refine existing specs

## Files

- `SKILL.md` - Full skill specification
- `README.md` - This file

## See Also

- [Development Cadence](../../../docs/guides/dev-cadence.md)
- [Implementation Workflow](../../../docs/guides/implementation-workflow.md)
