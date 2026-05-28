---
name: review-architecture
description: Use when reviewing code for architectural consistency, designing backend systems, or evaluating structural changes
---

# Architecture Review

Guidelines for reviewing and designing software architecture.

## When to Use

- After structural changes or new service introductions
- When designing APIs, data schemas, or system boundaries
- Before major refactoring efforts
- When evaluating architectural decisions

## Review Process

1. **Contextualize**: Understand the change's purpose within the broader system
2. **Identify Boundaries**: Determine affected components, services, and layers
3. **Pattern Check**: Compare against existing conventions
4. **Assess Impact**: Evaluate modularity and coupling effects
5. **Formulate Feedback**: Provide specific, actionable recommendations

## Architecture Checklist

### Pattern Compliance
- [ ] Adheres to established patterns (microservices, event-driven, layered)
- [ ] SOLID principles followed
- [ ] Dependencies flow correctly (no circular references)
- [ ] Appropriate abstraction levels
- [ ] Clear separation of concerns

### Service Design
- [ ] Single, well-defined responsibility per service
- [ ] Efficient, well-defined inter-service communication
- [ ] Clear service boundaries
- [ ] Proper API contracts with versioning

### Data Architecture
- [ ] Appropriate database selection for use case
- [ ] Proper schema design with indexing strategy
- [ ] Data flow is clear and traceable
- [ ] Caching strategy defined where needed

### Quality Attributes
- [ ] Scalability: Can handle 10x load without major redesign
- [ ] Security: Proper boundaries and validation points
- [ ] Observability: Logging, metrics, tracing planned
- [ ] Testability: Components testable in isolation

## Decision Priority

When multiple solutions exist:
1. **Testability** - Can it be tested in isolation?
2. **Readability** - Will other developers understand it?
3. **Consistency** - Matches existing patterns?
4. **Simplicity** - Least complex solution?
5. **Reversibility** - Easy to change later?

## Output Format

### Impact Assessment
- **Level**: High/Medium/Low
- **Summary**: Brief architectural significance

### Issues Found
For each issue:
- **Location**: File/component affected
- **Violation**: Principle or pattern violated
- **Impact**: Current and future implications
- **Recommendation**: Specific fix with code example if helpful

### Example Recommendation

> **Issue**: `OrderService` directly queries `Customer` database table, violating service autonomy.
>
> **Recommendation**: Publish `OrderCreated` event; let `CustomerService` subscribe and update its own data. This decouples services and improves resilience.

## Design Guidance

### API Contract Template
```
METHOD /api/v1/resource
Request: { fields }
Response (2xx): { fields }
Error (4xx/5xx): { error, message }
Auth: Required/Optional
```

### Schema Template
```sql
CREATE TABLE resource (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- fields with types and constraints
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_resource_field ON resource(field);
```

## Guiding Principles

- **Pragmatism over dogma** - Patterns are guides, not rules
- **Enable, don't obstruct** - Facilitate rapid, quality development
- **Clarity with justification** - Explain *why* something is problematic
- **Design for failure** - Assume components will fail
- **Start simple** - Create clear paths for evolution
