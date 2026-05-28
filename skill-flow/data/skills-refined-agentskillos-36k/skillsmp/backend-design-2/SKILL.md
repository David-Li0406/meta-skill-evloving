---
name: backend-design
description: Design robust backend systems and APIs. Use when users ask to plan or implement services, data models, or integrations.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Backend Design Skill

This skill guides the design of reliable backend systems, APIs, and data models with clear trade-offs, strong correctness guarantees, and operational readiness.

## Design Thinking

- **Scope**: Identify core use cases, data flows, and integration points.
- **Constraints**: Latency, throughput, availability, compliance, and deployment limits.
- **Data**: Define entities, relationships, invariants, and lifecycle.
- **Reliability**: Error handling, retries, idempotency, and consistency model.

## Architecture Guidelines

- **API Design**: Explicit contracts, versioning, validation, and error shape.
- **Storage**: Choose stores based on access patterns and durability needs.
- **Performance**: Indexing, caching, batching, and async processing.
- **Security**: AuthN/AuthZ, least privilege, secrets handling, auditability.
- **Observability**: Logging, metrics, tracing, and alerting signals.
- **Scalability**: Stateless services where possible, clear scaling boundaries.

## Output Requirements

Provide a clear backend plan or implementation that includes:

- Data model and key invariants
- API endpoints or service interfaces
- Failure modes and recovery strategy
- Performance and scaling considerations
- Security and observability notes

## Response Checklist

```markdown
Backend Design Checklist

- [ ] Confirm requirements and constraints
- [ ] Define data model and invariants
- [ ] Specify API contracts and error shape
- [ ] Address failure modes and consistency
- [ ] Cover performance, scaling, and caching
- [ ] Include security and observability plans
```
