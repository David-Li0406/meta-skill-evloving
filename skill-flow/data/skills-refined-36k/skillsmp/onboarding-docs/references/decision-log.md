# Decision Log Patterns

Architecture Decision Records (ADR) for documenting technical decisions.

## ADR Structure

### Standard Template

```markdown
# ADR-[NUMBER]: [TITLE]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Date
YYYY-MM-DD

## Context
[Describe the context and problem statement]
[What forces are at play?]
[What constraints exist?]

## Decision
[Describe the decision that was made]
[Be specific about what will be done]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

### Neutral
- [Side effect that's neither good nor bad]

## Alternatives Considered

### [Alternative 1]
- **Pros:** [advantages]
- **Cons:** [disadvantages]
- **Why rejected:** [reason]

### [Alternative 2]
- **Pros:** [advantages]
- **Cons:** [disadvantages]
- **Why rejected:** [reason]
```

### Example ADR

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Date
2024-01-15

## Context
We need to choose a primary database for our application. Requirements:
- ACID compliance for financial transactions
- Support for complex queries and joins
- Ability to scale to millions of records
- Strong ecosystem and community support
- Team familiarity

Current team has experience with PostgreSQL (3 engineers) and MySQL (2 engineers).

## Decision
We will use PostgreSQL as our primary database.

We will:
- Use PostgreSQL 15 or later
- Deploy on AWS RDS for managed operations
- Use Prisma as our ORM
- Implement read replicas when needed for scaling

## Consequences

### Positive
- ACID compliance ensures data integrity for payments
- Rich feature set (JSONB, full-text search, arrays)
- Excellent performance for complex queries
- Strong team expertise reduces ramp-up time
- Wide hosting options (AWS, GCP, self-hosted)

### Negative
- Vertical scaling has limits vs. horizontal-first databases
- Slightly more complex replication setup than MySQL
- Higher memory requirements for optimal performance

### Neutral
- Will use cloud-managed service (RDS) rather than self-hosted
- Migration path to other SQL databases exists if needed

## Alternatives Considered

### MySQL 8.0
- **Pros:** Familiar to 2 team members, slightly easier replication
- **Cons:** Weaker JSONB support, less advanced features
- **Why rejected:** PostgreSQL's feature set better matches requirements

### MongoDB
- **Pros:** Flexible schema, easy horizontal scaling
- **Cons:** No ACID transactions across documents, team unfamiliar
- **Why rejected:** Financial data requires ACID guarantees

### CockroachDB
- **Pros:** Distributed SQL, PostgreSQL compatible
- **Cons:** Higher operational complexity, cost
- **Why rejected:** Over-engineered for current scale
```

## Decision Log Organization

### Directory Structure

```
docs/
└── decisions/
    ├── README.md           # Index of all decisions
    ├── template.md         # ADR template
    ├── 001-database.md
    ├── 002-api-design.md
    ├── 003-auth-provider.md
    └── ...
```

### Index Document

```markdown
# Architecture Decision Records

## Active Decisions

| ID | Title | Date | Status |
|----|-------|------|--------|
| [ADR-001](./001-database.md) | Use PostgreSQL | 2024-01-15 | Accepted |
| [ADR-002](./002-api-design.md) | REST over GraphQL | 2024-01-20 | Accepted |
| [ADR-003](./003-auth-provider.md) | Auth0 for Authentication | 2024-02-01 | Accepted |

## Superseded Decisions

| ID | Title | Superseded By |
|----|-------|---------------|
| [ADR-004](./004-old-cache.md) | Redis for Caching | ADR-008 |

## Decision Categories

### Infrastructure
- [ADR-001](./001-database.md) - Database selection
- [ADR-005](./005-hosting.md) - Cloud provider

### Architecture
- [ADR-002](./002-api-design.md) - API design approach
- [ADR-006](./006-microservices.md) - Service boundaries

### Security
- [ADR-003](./003-auth-provider.md) - Authentication
- [ADR-007](./007-encryption.md) - Data encryption
```

## Lightweight ADR Format

For smaller decisions:

```markdown
# ADR-015: Use Jest for Testing

**Status:** Accepted | **Date:** 2024-03-01

**Context:** Need a JavaScript testing framework.

**Decision:** Use Jest because:
- Built-in mocking
- Snapshot testing
- Team familiarity
- Good TypeScript support

**Alternatives rejected:**
- Mocha+Chai: More setup required
- Vitest: Newer, less ecosystem support
```

## When to Write an ADR

### Always Document

- Database selection
- Major framework choices
- Authentication approach
- API design patterns
- Significant architecture changes
- Security-related decisions
- External service integrations

### Consider Documenting

- Library choices for critical functionality
- Testing strategy changes
- Build/deploy pipeline changes
- Significant refactoring approaches

### Skip Documentation

- Minor library updates
- Bug fixes
- Style/formatting decisions
- Temporary workarounds

## ADR Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Proposed │────>│ Accepted │────>│Deprecated│
└──────────┘     └────┬─────┘     └──────────┘
                      │
                      │ superseded
                      ▼
                ┌──────────┐
                │Superseded│
                │by ADR-XXX│
                └──────────┘
```

### Updating Decisions

When a decision changes:

```markdown
# ADR-004: Use Redis for Caching

## Status
~~Accepted~~ → Superseded by [ADR-008](./008-memcached.md)

## Superseded
**Date:** 2024-06-15
**Reason:** Migrated to Memcached for cost optimization
**See:** [ADR-008](./008-memcached.md) for current approach
```

## Decision Reviews

Schedule periodic reviews:

```markdown
# Decision Review: Q1 2024

## Reviewed Decisions
| ADR | Current Status | Action |
|-----|----------------|--------|
| ADR-001 | Working well | Keep |
| ADR-003 | Auth0 costs high | Review alternatives |
| ADR-005 | Requirements changed | Propose update |

## Proposed New Decisions
- ADR-020: Migrate to different auth provider
- ADR-021: Add caching layer
```
