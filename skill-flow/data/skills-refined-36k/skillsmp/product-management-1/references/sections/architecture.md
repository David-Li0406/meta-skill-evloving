# Architecture Decisions

Document technical choices and rationale.

## Decision Record Format

```
## Architecture Decisions

### ADR-1: Authentication Method
**Decision:** JWT with refresh tokens
**Context:** Need stateless auth for scalability
**Alternatives considered:**
- Session-based (rejected: requires sticky sessions)
- OAuth only (rejected: need internal auth too)
**Consequences:**
- Token management required on client
- Need refresh token rotation

### ADR-2: Database Choice
**Decision:** PostgreSQL
**Context:** Need relational data with JSON support
**Alternatives considered:**
- MongoDB (rejected: need strong consistency)
- MySQL (rejected: JSON support weaker)
**Consequences:**
- Operational complexity higher than SQLite
- Need connection pooling

### ADR-3: API Style
**Decision:** REST with OpenAPI spec
**Context:** Multiple clients, need documentation
**Alternatives considered:**
- GraphQL (rejected: team unfamiliar)
- gRPC (rejected: browser support complex)
**Consequences:**
- Multiple endpoints to maintain
- OpenAPI spec maintenance required
```

## Technology Stack

```
## Tech Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| Frontend | React | Team expertise |
| Backend | Node.js | Full-stack JS |
| Database | PostgreSQL | Reliability |
| Cache | Redis | Session storage |
| Queue | BullMQ | Background jobs |
```

## Constraints

```
## Technical Constraints

- Must run on Node 18+
- Must support PostgreSQL 14+
- Must work behind corporate proxy
- Must not require Docker for local dev
```

## Non-Functional Requirements

```
## NFRs

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Response time | < 200ms | p95 latency |
| Uptime | 99.9% | Monthly SLA |
| Concurrent users | 1000 | Load test |
| Data retention | 7 years | Compliance |
```
