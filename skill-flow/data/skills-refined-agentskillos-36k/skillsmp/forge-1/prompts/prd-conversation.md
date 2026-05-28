# PRD Conversation Guide

Use these questions to build a Product Requirements Document during the Focus phase.

## Intent Questions

1. **What problem are you solving?**
   - Who experiences this problem?
   - How painful is it? (frequency, severity)
   - What happens if we don't solve it?

2. **Who is the target user?**
   - Be specific (not "everyone")
   - What do they care about?
   - What's their technical level?

3. **What does success look like?**
   - How will we know it worked?
   - What metrics matter?
   - What's the minimum viable outcome?

## Scope Questions

4. **What's in scope for this cycle?**
   - Core features only
   - What's the smallest useful increment?

5. **What's explicitly out of scope?**
   - Future enhancements
   - Nice-to-haves
   - Edge cases to defer

6. **What constraints apply?**
   - Technical constraints (languages, frameworks)
   - Time constraints
   - Integration requirements

## Technical Questions

7. **What systems does this interact with?**
   - Existing code to integrate with
   - External services
   - Data sources

8. **What are the key risks?**
   - Technical unknowns
   - Performance concerns
   - Security considerations

## Acceptance Questions

9. **How will we test this?**
   - Key scenarios to verify
   - Edge cases that matter
   - Performance thresholds

10. **What would make us reject the implementation?**
    - Deal-breakers
    - Quality gates
    - Non-negotiables

## PRD Template

```markdown
# [Feature Name]

## Problem Statement
[What problem exists and for whom]

## Target Users
[Specific user description]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## In Scope
- [Feature 1]
- [Feature 2]

## Out of Scope
- [Deferred item 1]
- [Deferred item 2]

## Constraints
- [Technical constraint]
- [Other constraint]

## Key Risks
- [Risk 1]
- [Risk 2]

## System Context
[C4 L1 diagram or description]
```
