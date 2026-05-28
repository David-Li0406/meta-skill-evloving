# Architecture Decision Record Template

## ADR-[NUMBER]: [Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX

---

## Context

What is the issue that we're seeing that motivates this decision or change?

Describe:
- The problem we're trying to solve
- The constraints we're working within
- Any relevant background information
- The forces at play (technical, business, team)

---

## Decision

What is the change that we're proposing and/or doing?

State the decision clearly and concisely. Use active voice:
- "We will..."
- "The system will..."
- "Teams will..."

---

## Alternatives Considered

### Option 1: [Name]

**Description:** Brief explanation

**Pros:**
- Benefit 1
- Benefit 2

**Cons:**
- Drawback 1
- Drawback 2

**Why not chosen:** Reason

### Option 2: [Name]

**Description:** Brief explanation

**Pros:**
- Benefit 1
- Benefit 2

**Cons:**
- Drawback 1
- Drawback 2

**Why not chosen:** Reason

---

## Consequences

What becomes easier or more difficult to do because of this change?

### Positive

- Benefit 1
- Benefit 2
- Benefit 3

### Negative

- Trade-off 1
- Trade-off 2

### Neutral

- Change that's neither good nor bad

---

## Implementation Notes

Any specific guidance for implementing this decision:

- Technical details
- Migration steps
- Timeline considerations
- Team responsibilities

---

## References

- Related ADRs: ADR-XXX
- External resources: [Link]
- Relevant documentation: [Link]

---

# Example: Completed ADR

## ADR-001: Use PostgreSQL for Primary Database

**Date:** 2024-01-15
**Status:** Accepted

---

## Context

We need to choose a database for our new e-commerce platform. The system will handle:
- ~100k daily active users
- Complex queries across orders, products, and inventory
- Strong consistency requirements for financial data
- Need for full-text search on product catalog

Our team has experience with both PostgreSQL and MongoDB.

---

## Decision

We will use PostgreSQL as our primary database.

We will use PostgreSQL's built-in full-text search capabilities rather than adding Elasticsearch initially. We can add Elasticsearch later if search requirements grow beyond PostgreSQL's capabilities.

---

## Alternatives Considered

### Option 1: MongoDB

**Pros:**
- Flexible schema for product attributes
- Native JSON support
- Horizontal scaling built-in

**Cons:**
- Weaker consistency guarantees
- Complex transactions harder to implement
- Would require separate search solution

**Why not chosen:** Financial data requires strong consistency; relational model fits our domain better.

### Option 2: PostgreSQL + Elasticsearch

**Pros:**
- Best-in-class search capabilities
- Scales search independently

**Cons:**
- Additional operational complexity
- Data synchronization challenges
- Higher infrastructure cost

**Why not chosen:** Premature optimization; PostgreSQL full-text search sufficient for MVP.

---

## Consequences

### Positive

- Strong ACID guarantees for financial transactions
- Team familiarity reduces ramp-up time
- Single database simplifies operations
- Rich ecosystem of tools and extensions

### Negative

- Less flexibility for unstructured product attributes
- May need to add search solution later
- Vertical scaling has limits

### Neutral

- Will use JSONB columns for flexible product attributes
- Schema migrations required for model changes

---

## Implementation Notes

- Use JSONB for product attributes that vary by category
- Set up pg_trgm extension for fuzzy search
- Plan for read replicas as traffic grows
- Use connection pooling (PgBouncer) from the start
