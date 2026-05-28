---
title: {{TITLE}}
category: architecture
status: proposed
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
author: Claude
tags: []
adr_number: {{OPTIONAL_ADR_NUMBER}}
---

# {{TITLE}}

## Context

{{What is the context for this architectural decision? What forces are at play?}}

## Decision

{{What is the architectural decision? Be specific and concrete.}}

## Rationale

{{Why was this decision made? What trade-offs were considered?}}

## Consequences

### Positive

- {{Benefit 1}}
- {{Benefit 2}}

### Negative

- {{Drawback 1}}
- {{Drawback 2}}

### Neutral

- {{Side effect that is neither good nor bad}}

## Implementation Notes

{{Technical details for implementing this architecture.}}

### Components Affected

| Component | Change Type | Description |
|-----------|-------------|-------------|
| {{Component name}} | Add/Modify/Remove | {{What changes}} |

### Diagram

```
{{ASCII diagram showing the architecture, or link to visual diagram}}

┌─────────────┐     ┌─────────────┐
│  Component  │────▶│  Component  │
└─────────────┘     └─────────────┘
```

## Alternatives Considered

### {{Alternative 1}}

{{Description and why it was not chosen}}

### {{Alternative 2}}

{{Description and why it was not chosen}}

## Related

### Codebase

- [{{primary_file.rb}}](../../{{path/to/primary_file.rb}}) - {{Primary file affected by this decision}}
- [{{config_file}}](../../{{path/to/config}}) - {{Configuration related to this decision}}

### Related Documentation

- [{{Related Plan}}](../plans/{{YYYY-MM-DD}}-{{filename}}.md) - {{Plan that implements this decision}}
- [{{Related ADR}}](../architecture/{{YYYY-MM-DD}}-{{filename}}.md) - {{Related architectural decision}}
