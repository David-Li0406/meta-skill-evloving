---
name: use-case
description: Use Case document creation following the working backwards methodology
---

# Amazon Use Case Writing Skill

Use this skill when creating customer-centric use case documents that follow Amazon's working backwards methodology and customer-obsessed approach.

**Template:** See `docs/templates/use-case-template.md` for the authoritative template structure.

## When to Use This Skill

- When designing new product features and need customer-centric documentation
- When converting technical requirements into customer-focused scenarios
- When preparing product requirement documents (PRDs) following Amazon best practices
- When documenting user workflows with structured format

## Document Structure Summary

Create a 500-800 word document (~1-2 pages) with these sections:

1. **Metadata** (YAML header) - ID, title, actor, type, version
2. **Use Case Statement** - As a [actor], I want [action], so that [benefit]
3. **Overview** - Customer problem narrative
4. **Actors** - Primary, secondary, external dependencies
5. **Preconditions** - Required states before use case begins
6. **Trigger** - Event that initiates the use case
7. **Main Flow** - Happy path (4-8 steps from customer perspective)
8. **Alternate/Edge Flows** - Common variations
9. **Exception Flows** - Error conditions and recovery
10. **Postconditions/Outcomes** - Success state, business benefits, data changes
11. **Success Metrics** - Measurable criteria with targets
12. **Assumptions & Open Questions** - Marked assumptions, research needs

## Writing Style

| Aspect | Guideline |
|--------|-----------|
| **Perspective** | Customer's perspective, never system's |
| **Language** | Plain English, short sentences |
| **Jargon** | Avoid technical shorthand |
| **Tense** | Present tense for steps |
| **Voice** | Active voice throughout |
| **Specificity** | Specific enough to test |

## EARS Syntax for Criteria

When writing testable criteria, use EARS format:

| Pattern | Template |
|---------|----------|
| **Ubiquitous** | THE System SHALL [requirement] |
| **Event-Driven** | WHEN [trigger], THE System SHALL [response] |
| **State-Driven** | WHILE [state], THE System SHALL [behavior] |
| **Optional** | WHERE [feature] is enabled, THE System SHALL [behavior] |
| **Unwanted** | IF [condition], THE System SHALL [response] |

## Quality Checklist

- [ ] Use case statement follows As/I want/So that format
- [ ] Overview explains customer problem (not solution)
- [ ] Preconditions are verifiable states
- [ ] Trigger is a specific, observable event
- [ ] Main flow steps are from customer perspective
- [ ] Alternate flows cover common variations
- [ ] Exception flows cover error conditions
- [ ] Success metrics are measurable
- [ ] Assumptions marked with **(Assumption)**
- [ ] Word count: 500-800 words

## Output Location

```
docs/usecases/[use-case-name].md
```
