---
name: systems-decompose
description: Decompose a feature into system components before implementation
---

# Systems Decomposition

Before implementing, let's properly decompose this feature:

## Context

1. **What are we building?** Describe the feature.
2. **Who triggers it?** User action, system event, scheduled?
3. **What should happen?** The happy path outcome.

## Data Flow Mapping

Map the complete flow:

```
[Trigger] → [Input] → [Validation] → [Business Logic] → [Side Effects] → [Output]
```

For each step:

- What data comes in?
- What transformation happens?
- What data goes out?
- What can go wrong?

## Interface Contracts

Define explicit interfaces:

### Input Schema

- What fields are required?
- What are the types and constraints?
- Validation rules?

### Output Schema

- Success response format?
- Error response format?
- All possible error types?

### Error Enumeration

List ALL possible errors:

- Validation errors
- Not found errors
- Authorization errors
- External service errors
- System errors

## Boundaries

Clarify ownership:

- What does this component OWN?
- What does it NOT own?
- What are the integration points?

## Dependencies

For each external dependency:

- What is it?
- Sync or async?
- What if it fails?
- How do we recover?

This decomposition will guide implementation.
