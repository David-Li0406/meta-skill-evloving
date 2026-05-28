---
name: consultant:clarify
description: "Clarify ambiguous requirements using Jobs-to-be-Done framework. Marie asks probing questions to transform vague ideas into concrete specifications."
invocation: user
---

# Clarify Requirements

Transform vague user requirements into concrete, actionable specifications.

## When to Use

- User has unclear or incomplete requirements
- Need to dig deeper into business value
- Requirements are too technical, missing the "why"
- Multiple interpretations are possible

## Process

### 1. Understand Current State
- Read requirement as stated
- Identify what's missing or ambiguous

### 2. Apply 5W1H Framework
| Question | Purpose |
|----------|---------|
| WHO | Who are the users? What roles? |
| WHAT | What exactly needs to happen? |
| WHEN | What triggers this? Timing? |
| WHERE | Context/environment? |
| WHY | Business value? |
| HOW | Expected flow? |

### 3. Ask Clarifying Questions
- One focused question at a time
- Provide concrete examples
- Offer options when possible

### 4. Validate Understanding
"Si je comprends bien, quand [trigger], alors [action] pour [outcome]. C'est correct?"

### 5. Document
Add to project-context.md:
- Requirements Registry
- Assumptions
- Remaining ambiguities

## Output

```markdown
## Requirement: {name}

### Context
{business_context}

### Specification
- User: {who}
- Trigger: {when}
- Action: {what}
- Outcome: {result}

### Acceptance Criteria
- [ ] AC-1: {criterion}
- [ ] AC-2: {criterion}

### Open Questions
- {remaining_ambiguity}
```

## Agent

This skill uses the `consultant-discovery` subagent.
