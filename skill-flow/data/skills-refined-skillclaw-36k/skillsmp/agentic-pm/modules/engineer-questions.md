# Module: Answering Engineer Questions (Guardrails + Escalation)

## Objective

Resolve ambiguity without creating scope creep.

## Procedure

1) **Restate** the question and the relevant acceptance criteria.

2) **Identify** whether it affects:
   - Contract (API/schema/types)
   - Merge order / integration plan
   - Scope boundaries
   - Other tasks

3) **Respond** with:
   - A definitive decision if possible
   - OR a question back to the user if escalation needed

4) **Update**:
   - Decision log (always)
   - Affected task files (if the decision changes requirements)
   - Dependency graph (if merge order changes)

## Hard rule

**Do not let engineers invent product behavior.** If unclear, escalate to user.

## Response format

```markdown
## Question Response

**Original question**: <restate>

**Relevant criteria**: <quote from task file>

**Decision**: <your answer>

**Rationale**: <why>

**Impact**:
- Task file updates: <none / list>
- Decision log: <entry added>
- Other tasks affected: <none / list>
```

## Escalation triggers

Escalate to user (do not answer yourself) if:
- Question implies missing product requirements
- Answer would change user-facing behavior
- Answer affects security or data handling
- Multiple valid interpretations exist
- Answer would change scope significantly

## Decision log entry format

```markdown
### Decision: <title>

- **Date**: <date>
- **Task**: TASK-<ID>
- **Question**: <summary>
- **Decision**: <answer>
- **Rationale**: <why>
- **Impact**: <what changed>
```

## Common question patterns

| Pattern | Action |
|---------|--------|
| "Should I also..." | Check non-goals; usually NO |
| "What if X happens?" | Check acceptance criteria; add if missing |
| "Which pattern should I use?" | Provide code example; update task file |
| "Is this in scope?" | Check goal + non-goals; clarify boundaries |
| "How should this behave?" | Escalate to user (product decision) |
