---
name: System Design
description: This skill should be used when the user asks to "design a system", "architect an application", "plan infrastructure", "create system architecture", "design for scale", "microservices architecture", "monolith vs microservices", "design patterns", "scalability planning", "high availability design", or needs guidance on system design decisions, trade-offs, and best practices.
version: 1.0.0
---

# System Design

Comprehensive guidance for designing scalable, resilient, and maintainable software systems.

## Core Principles

### Scalability Dimensions

1. **Vertical Scaling** - Add resources to existing nodes (CPU, RAM, storage)
2. **Horizontal Scaling** - Add more nodes to distribute load
3. **Database Scaling** - Sharding, read replicas, connection pooling

### Design Trade-offs

| Trade-off | Option A | Option B | Consider |
|-----------|----------|----------|----------|
| CAP Theorem | Consistency | Availability | Network partitions are inevitable |
| Latency vs Throughput | Low latency | High throughput | User expectations |
| Complexity vs Flexibility | Simple monolith | Flexible microservices | Team size, deployment frequency |

## Architecture Patterns

### Monolith Architecture

When to use:
- Small team (< 10 developers)
- New product with unclear boundaries
- Simple deployment requirements
- Rapid prototyping needed

Structure:
```
monolith/
├── api/           # HTTP handlers
├── services/      # Business logic
├── repositories/  # Data access
├── models/        # Domain models
└── config/        # Configuration
```

### Microservices Architecture

When to use:
- Large teams needing independent deployment
- Different scaling requirements per component
- Polyglot technology requirements
- Strong domain boundaries exist

Key concerns:
- Service discovery
- Inter-service communication (sync vs async)
- Distributed transactions
- Observability across services

### Event-Driven Architecture

Components:
- **Event Producers** - Generate events on state changes
- **Event Broker** - Kafka, RabbitMQ, AWS EventBridge
- **Event Consumers** - React to events asynchronously

Patterns:
- Event Sourcing - Store events as source of truth
- CQRS - Separate read/write models
- Saga Pattern - Distributed transaction management

## Designing for Scale

### Load Estimation

Calculate expected load:
```
Daily Active Users (DAU): X
Actions per user per day: Y
Peak multiplier: Z (typically 2-3x average)

Requests per second (RPS) = (DAU × Y × Z) / 86400
```

### Capacity Planning

For each component, determine:
1. **CPU requirements** - Compute-intensive operations
2. **Memory requirements** - In-memory data, caching
3. **Storage requirements** - Data growth rate
4. **Network requirements** - Bandwidth, latency constraints

### Database Selection

| Use Case | Recommended | Rationale |
|----------|-------------|-----------|
| Transactions | PostgreSQL, MySQL | ACID compliance |
| Documents | MongoDB, CouchDB | Schema flexibility |
| Key-Value | Redis, DynamoDB | Low latency access |
| Time Series | InfluxDB, TimescaleDB | Time-based queries |
| Graph | Neo4j, Neptune | Relationship traversal |
| Search | Elasticsearch, Algolia | Full-text search |

## High Availability Patterns

### Redundancy Levels

1. **Active-Passive** - Standby takes over on failure
2. **Active-Active** - Multiple active instances sharing load
3. **N+1 Redundancy** - One spare for every N active

### Failure Domains

Distribute across:
- Multiple availability zones (AZ)
- Multiple regions (for global apps)
- Multiple cloud providers (for critical systems)

### Circuit Breaker Pattern

Prevent cascade failures:
```
States:
1. CLOSED - Normal operation, requests pass through
2. OPEN - Failures exceeded threshold, requests fail fast
3. HALF-OPEN - Test if service recovered
```

## API Design

### REST Principles

- Use nouns for resources (`/users`, `/orders`)
- HTTP verbs for actions (GET, POST, PUT, DELETE)
- Consistent response format
- Proper status codes
- Version in URL or header

### GraphQL Considerations

When to prefer GraphQL:
- Complex, nested data requirements
- Multiple clients with different needs
- Bandwidth optimization needed
- Rapid frontend iteration

### API Versioning Strategies

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL Path | `/v1/users` | Clear, cacheable | URL pollution |
| Query Param | `/users?v=1` | Flexible | Cache complexity |
| Header | `Accept-Version: 1` | Clean URLs | Hidden version |

## Security by Design

### Authentication Patterns

- **Session-based** - Server-side session storage
- **Token-based (JWT)** - Stateless, client-side storage
- **OAuth 2.0** - Third-party authentication
- **API Keys** - Service-to-service authentication

### Authorization Models

- **RBAC** - Role-Based Access Control
- **ABAC** - Attribute-Based Access Control
- **ReBAC** - Relationship-Based Access Control

### Security Checklist

- [ ] Input validation on all endpoints
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries to prevent SQL injection
- [ ] Rate limiting to prevent abuse
- [ ] Encryption in transit (TLS)
- [ ] Encryption at rest for sensitive data
- [ ] Secrets management (not in code)

## Performance Optimization

### Caching Strategies

| Level | Tool | Use Case |
|-------|------|----------|
| CDN | CloudFront, Cloudflare | Static assets |
| Application | Redis, Memcached | Session, computed data |
| Database | Query cache | Repeated queries |
| Client | Browser cache | Assets, API responses |

### Asynchronous Processing

Move off critical path:
- Email/notification sending
- Report generation
- Image/video processing
- Third-party API calls
- Analytics/logging

## Design Documentation

### System Design Document Template

1. **Overview** - Problem statement, goals
2. **Requirements** - Functional and non-functional
3. **Architecture** - High-level diagram
4. **Components** - Detailed component design
5. **Data Model** - Schema design
6. **APIs** - Interface definitions
7. **Security** - Authentication, authorization
8. **Scalability** - How system scales
9. **Monitoring** - Observability plan
10. **Trade-offs** - Decisions and alternatives

## Additional Resources

### Reference Files

For detailed patterns and examples:
- **`references/patterns.md`** - Comprehensive design patterns catalog
- **`references/case-studies.md`** - Real-world system design examples
- **`references/estimation.md`** - Capacity planning formulas

### Example Files

Working templates in `examples/`:
- **`system-design-template.md`** - Design document template
- **`architecture-diagram.md`** - Mermaid diagram examples
