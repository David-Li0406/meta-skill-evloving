---
name: architect
description: "Architecture review and design process. Use when designing new systems or major features, reviewing code structure, making decisions about patterns or frameworks, creating or reviewing Architecture Decision Records (ADRs), or evaluating technical debt. Also use when changes affect multiple components, decisions are hard to reverse (database schema, API contracts), choosing between competing patterns, or when complexity is increasing without clear benefit. Essential for SOLID principles, design patterns, API design, and microservices vs monolith decisions."
---

# Architecture Review Skill

## Overview

Architecture decisions are expensive to change later. This skill guides systematic architectural review and design before committing to implementation.

**Core principle:** Understand trade-offs BEFORE building. The cheapest architecture change is the one made before code is written.

## The Architecture Review Process

### Phase 1: Requirements Understanding

Before proposing ANY architecture:

1. **Clarify Functional Requirements**
   - What must the system DO?
   - What are the critical user flows?
   - What data needs to be stored/processed?

2. **Identify Quality Attributes**
   - Performance: What latency/throughput is acceptable?
   - Scalability: What growth is expected?
   - Availability: What uptime is required?
   - Security: What data sensitivity levels?

3. **Understand Constraints**
   - Team size and expertise
   - Timeline and budget
   - Existing systems to integrate with
   - Regulatory or compliance requirements

### Phase 2: Design Exploration

**NEVER propose a single solution. Always present options.**

1. **Generate 2-3 Approaches**
   - What's the simplest solution that could work?
   - What's the "industry standard" approach?
   - What's the most scalable/flexible option?

2. **Evaluate Trade-offs**
   For each approach, assess:
   - Complexity: How hard to build and maintain?
   - Flexibility: How easy to change later?
   - Risk: What could go wrong?
   - Cost: Development time, infrastructure, operations

3. **Present with Recommendation**
   - Lead with your recommended option
   - Explain WHY you recommend it
   - Be explicit about trade-offs you're accepting

### Phase 3: Validation

Before finalizing:

1. **SOLID Check**
   - Does the design follow SOLID principles?
   - See `references/solid-principles.md` for patterns

2. **Boundary Check**
   - Are responsibilities clearly separated?
   - Are interfaces well-defined?
   - Can components be tested independently?

3. **Future-Proofing Check**
   - What's likely to change?
   - Is the design flexible where it needs to be?
   - Is it simple where change is unlikely?

## Red Flags - STOP and Reconsider

If you encounter ANY of these, pause and investigate:

### Complexity Smells
```
- More than 3 levels of inheritance
- Circular dependencies between modules
- God classes (>500 lines, >10 methods)
- "Manager", "Handler", "Processor" classes doing everything
- Config files longer than the code they configure
```

### Design Smells
```
- Copy-paste code across multiple files
- Switch statements on type fields
- Null checks everywhere
- Deep nesting (>3 levels)
- Methods with >5 parameters
```

### Architecture Smells
```
- Every change requires modifying multiple services
- Can't deploy one component without deploying others
- Can't test without the full system running
- Unclear ownership of functionality
- Data duplicated across services without clear reason
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "We'll refactor later" | Later never comes. Design right now. |
| "It's just a prototype" | Prototypes become production. Build properly. |
| "We need flexibility" | YAGNI. Build for known requirements. |
| "That's how [BigCo] does it" | You're not BigCo. Match complexity to needs. |
| "Microservices are best practice" | For your scale? Monolith is often better. |
| "We might need to scale" | Design for 10x current load, not 1000x. |
| "It's more maintainable" | Simpler is more maintainable. Prove otherwise. |

## Architecture Decision Record Template

For significant decisions, document:

```markdown
# ADR-001: [Decision Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue? What forces are at play?

## Options Considered
1. **Option A**: [Description]
   - Pros: ...
   - Cons: ...

2. **Option B**: [Description]
   - Pros: ...
   - Cons: ...

## Decision
We chose Option [X] because [reasoning].

## Consequences
- Positive: ...
- Negative: ...
- Risks: ...
```

## Quick Architecture Checklist

Before approving any architectural decision:

- [ ] **Requirements**: Do we understand what we're building and why?
- [ ] **Options**: Have we considered at least 2 approaches?
- [ ] **Trade-offs**: Are we explicit about what we're sacrificing?
- [ ] **Simplicity**: Is this the simplest solution that meets requirements?
- [ ] **Boundaries**: Are responsibilities clearly separated?
- [ ] **Testability**: Can components be tested in isolation?
- [ ] **Reversibility**: How hard is this to change if we're wrong?

## Pattern Selection Guide

| Problem | Consider | Avoid When |
|---------|----------|------------|
| Complex object creation | Factory, Builder | Object is simple |
| Need one instance | Singleton (sparingly) | Testing matters |
| Incompatible interfaces | Adapter | Can modify source |
| Add behavior dynamically | Decorator | Inheritance works |
| Simplify complex system | Facade | Need fine control |
| Swappable algorithms | Strategy | Only one algorithm |
| React to state changes | Observer | Simple callbacks work |
| Undo/redo, queuing | Command | Simple function calls work |

## References

Detailed patterns and examples in `references/`:
- `solid-principles.md` - SOLID with anti-patterns and fixes
- `design-patterns.md` - Common patterns and when to use them
- `api-design.md` - REST API design principles
- `architecture-patterns.md` - Monolith, microservices, hexagonal
