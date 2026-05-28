---
name: create-architecture-decision-record
description: Use this skill when you need to document significant architectural decisions, including their context, alternatives considered, and consequences, to maintain clarity and rationale for future reference.
---

# Skill Body

## Purpose

Create Architecture Decision Records (ADRs) to capture the "why" behind architectural choices, ensuring that future developers understand the reasoning behind decisions made.

## When to Use This Skill

Trigger this skill when:
- Making significant architectural decisions
- Choosing between competing technologies or frameworks
- Designing new system components or APIs
- Refactoring that changes system structure
- After implementing a feature that involved design trade-offs

## Skip ADR Creation If

- Only minor bug fixes or refactoring
- Documentation or test-only changes
- Configuration tweaks without architectural impact
- Trivial changes with obvious implementation

## Workflow

### 1. Gather Context

Review the implementation to understand:
- What technical decisions were made
- Why this approach was chosen
- What alternatives existed
- What trade-offs were accepted

**If reviewing existing code:**
```bash
git diff main...HEAD
git log --oneline main..HEAD
```

### 2. Investigate Further

If the diff doesn't provide enough context:
- Read referenced files/functions
- Check configuration files
- Review related tests
- Look at dependencies added

### 3. Create the ADR

**Location:** `docs/adr/NNNN-descriptive-title.md`

**Naming convention:**
- Sequential number (0001, 0002, etc.)
- Lowercase with hyphens
- Descriptive but concise

**Examples:**
- `0001-use-jwt-for-authentication.md`
- `0002-adopt-event-sourcing-for-orders.md`
- `0003-postgres-over-mysql.md`

### 4. Use the Template

Use the following template to structure the document:

```markdown
# [Short title of solved problem and solution]

## Status

[proposed | accepted | rejected | deprecated | superseded by ADR-XXXX]

## Context

What is the issue we're seeing that is motivating this decision or change?

Include:
- Current situation
- Problem statement
- Relevant constraints (time, cost, skills, technology)
- Stakeholder concerns
- Dependencies and assumptions

## Decision

What is the change that we're actually proposing or have agreed to implement?

Be specific and actionable:
- What we will do
- What technologies/patterns we'll use
- How it fits into existing architecture
- Any implementation guidelines

## Consequences

What becomes easier or more difficult to do and any risks introduced by the change.

### Positive
- Positive outcomes and benefits

### Negative
- Negative outcomes, drawbacks, and trade-offs

### Neutral
- Neutral impacts and side effects

## Alternatives Considered

- **Alternative A**: Reason for not adopting
- **Alternative B**: Reason for not adopting

## References

- Related ADRs and external resources
```

## Quality Guidelines

**Good ADRs have:**
- Specific technical details (not vague descriptions)
- Concrete examples and code snippets where helpful
- Honest assessment of trade-offs
- Links to relevant resources or prior art

**Avoid:**
- Vague justifications ("it's better")
- Missing context or rationale

## Example

```markdown
# ADR-0001: API Gateway Selection - Kong vs HAProxy

## Status
Accepted

## Context
Legacy system used HAProxy as a simple load balancer. Microservices architecture requires:
- API-aware routing based on paths, headers, JWT claims
- Built-in authentication (JWT validation, OAuth2)
- Rate limiting and circuit breakers
- Plugin ecosystem for extensibility

## Decision
Upgrade from HAProxy to Kong API Gateway

## Consequences

### Positive
- Routes to multiple backend services with path-based rules
- JWT validation out-of-the-box, reducing custom auth code
- Production-grade rate limiting without custom implementation
- Extensible via Lua plugins

### Negative
- More complex configuration than HAProxy
- Requires learning Kong admin API and declarative config
- Higher resource footprint (but acceptable for use case)
```