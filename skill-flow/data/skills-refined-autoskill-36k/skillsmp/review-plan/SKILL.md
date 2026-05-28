---
name: review-plan
description: Review and critique the current plan created in plan mode. Use after creating a plan to identify gaps, risks, and get clarifying questions. Triggers on "review plan", "critique plan", "check my plan", or when user wants feedback on their implementation plan.
---

# Review Current Plan

Conduct a thorough review of the plan created in the current session. Act as a meticulous technical reviewer and strategic advisor.

## Prerequisites

This skill requires an active plan from plan mode. If no plan exists in context, inform the user they need to create a plan first using plan mode.

## Review Dimensions

Systematically analyze the plan across:

1. **Completeness**: Missing components, edge cases, error handling, dependencies not addressed
2. **Technical feasibility**: Technical challenges, performance bottlenecks, architectural concerns
3. **Implementation clarity**: Does each step have sufficient detail? Any ambiguity?
4. **Dependencies & prerequisites**: External deps, tools, libraries, infrastructure requirements documented?
5. **Testing strategy**: Testing approaches, validation criteria, quality checks defined?
6. **Deployment & rollout**: Deployment steps, rollback procedures, monitoring covered?
7. **Documentation**: Documentation requirements and knowledge transfer needs addressed?
8. **Timeline realism**: Does timeline account for complexity and blockers?
9. **Resource allocation**: Compute, storage, third-party services, budget identified?
10. **Security & compliance**: Security considerations, compliance requirements noted?

## Output Format

1. **Brief summary**: Overall quality assessment and critical gaps (2-3 sentences max)

2. **Iterative questions**: Ask clarifying questions **one at a time** using AskUserQuestion tool:
   - **Context**: What aspect you're questioning and why it matters
   - **Current state**: What the plan says (or doesn't say) about this
   - **Impact**: Why this decision matters for success
   - Provide multiple-choice options where applicable

3. After each answer, either:
   - Ask the next critical question, or
   - Confirm the plan is comprehensive

## Guidelines

- Be direct and concise in feedback
- Prioritize critical gaps over minor improvements
- Focus on risks that could derail the project
- Don't ask about things already clearly addressed in the plan
- Stop questioning when all critical decisions are resolved

## Reference Files

- `references/question-examples.md` - Sample clarifying questions with context
