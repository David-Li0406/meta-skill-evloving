# [Title]

## Status

Approved

## Context

Describe the background, challenges, and current issues here. Follow the flow: facts → challenges → what you want to solve.
Use bullet points when listing facts or issues:

- [Fact 1]
- [Fact 2]
- [Fact 3]

Issues:
- [Challenge 1]
- [Challenge 2]

Close this section by explaining what you want to solve and the general approach.

## Decision

Start with a brief summary of the overall decision. This summary should give readers a high-level understanding of what was decided and why (1-2 paragraphs).

[Summary of the decision goes here. Explain the general approach and key principles.]

Include diagrams if helpful for explaining the overall design.

### Decision 1

If there are multiple decisions, create a section for each. Describe the details of each decision here.
However, avoid creating too many sections unnecessarily.

Use pseudocode to illustrate concepts (not implementation-specific code):

```js
// Pseudocode example
async function handleRequest(request) {
  const cached = await cache.get(request)
  if (cached) {
    return cached
  }

  const response = await fetch(origin)
  await cache.put(request, response)
  return response
}
```

## Consequences

### Positive

- [Positive outcomes]
- [Positive outcomes]

### Negative

- [Negative outcomes]
- [Negative outcomes]

### Neutral

- [Neutral impacts]
- [Neutral impacts]

## Notes

### Alternatives Considered

- **Alternatives**: [Alternative approaches that were considered]
- **Alternatives**: [Alternative approaches that were considered]
- **Alternatives**: [Alternative approaches that were considered]

### References

- [Related documents and external resources]
