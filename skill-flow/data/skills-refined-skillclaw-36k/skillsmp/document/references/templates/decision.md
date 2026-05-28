# Decision Template

Use this template for documenting important architectural decisions, technology choices, or technical trade-offs.

## When to Use

- Recording major architectural decisions (ADR style)
- Documenting technology or library choices
- Capturing trade-off analysis for technical decisions
- Explaining why one approach was chosen over alternatives

## Template Structure

```markdown
# {decision_title}

## Metadata

- **Timestamp**: {YYYY-MM-DD HH:MM:SS}
- **Project**: {project_name}
- **Category**: Decision
- **Tags**: {comma_separated_tags}
- **Related Commit**: {commit_hash if available}
- **Status**: {Proposed/Accepted/Deprecated/Superseded}

## Context

Situation that required the decision:

- What did we need to achieve?
- What constraints existed?
- Who were the stakeholders involved?

## Decision

Decision made, clearly and concisely stated.

## Options Considered

### Option 1: {name}

**Pros:**

- Pro 1
- Pro 2

**Cons:**

- Con 1
- Con 2

**Complexity:** {Low/Medium/High}

### Option 2: {name}

**Pros:**

- Pro 1
- Pro 2

**Cons:**

- Con 1
- Con 2

**Complexity:** {Low/Medium/High}

### Option 3: {name}

(Repeat structure)

## Rationale

Detailed explanation of why this option was chosen:

- Factors considered
- Priorities established
- Trade-off analysis

## Consequences

### Positive

- Positive consequence 1
- Positive consequence 2

### Negative

- Negative consequence 1
- Negative consequence 2

### Neutral

- Neutral consequence 1
- Neutral consequence 2

## Implementation Notes

Notes on implementing this decision:

- Required changes
- Implementation order
- Risks to mitigate

## Review Criteria

Criteria for reviewing this decision in the future:

- What would indicate this decision is no longer valid?
- When should we review it?

## References

- Relevant documentation
- Previous discussions
- External resources
```

## Field Descriptions

### Metadata
- **Timestamp**: Auto-generated current date/time
- **Project**: Auto-detected from directory or git repo
- **Category**: Always "Decision"
- **Tags**: Relevant tags (area, technology, type)
- **Related Commit**: Commit implementing this decision
- **Status**: Decision lifecycle stage

#### Status Values
- **Proposed**: Under consideration
- **Accepted**: Approved and being implemented
- **Deprecated**: No longer recommended
- **Superseded**: Replaced by another decision

### Context
Background information needed to understand the decision:
- Business or technical requirements
- Constraints (time, budget, technical)
- Stakeholders and their concerns

### Decision
One-sentence summary of what was decided. Be clear and definitive.

### Options Considered
Document 2-4 alternatives that were evaluated. For each:
- **Pros**: Benefits and advantages
- **Cons**: Drawbacks and limitations
- **Complexity**: Implementation difficulty

### Rationale
Detailed reasoning for the chosen option:
- Decision criteria and priorities
- How each option scored against criteria
- Why cons of chosen option are acceptable

### Consequences
Honest assessment of outcomes:
- **Positive**: Benefits we expect
- **Negative**: Costs or limitations we accept
- **Neutral**: Changes that are neither good nor bad

### Implementation Notes
Practical guidance for implementation:
- Required changes to system
- Recommended implementation order
- Potential risks and mitigation strategies

### Review Criteria
Conditions for revisiting this decision:
- Metrics to monitor
- Thresholds for reconsideration
- Scheduled review date

### References
Supporting materials:
- Architecture diagrams
- Prior RFCs or proposals
- External articles or documentation
- Internal discussion threads
