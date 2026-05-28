# Phase 5: Architecture & Design

## Objective

Define system structure, component relationships, and technical design decisions.

## Step 1: Architecture Style Selection

Present architecture options based on requirements:

```markdown
### Decision: Architecture Style

| Style | Description | Pros | Cons | Best For |
|-------|-------------|------|------|----------|
| **Monolith (Recommended for MVP)** | Single deployable unit | Simple, fast to build, easy to debug | Scaling limits, tight coupling | Small teams, early stage |
| **Microservices** | Distributed services | Independent scaling, team autonomy | Complexity, network overhead | Large teams, high scale |
| **Serverless** | Function-based | No infra management, pay-per-use | Cold starts, vendor lock-in | Event-driven, variable load |
| **Modular Monolith** | Monolith with clear boundaries | Best of both, migration path | Discipline required | Growing systems |

**Recommendation**: [Style] because [reasoning based on requirements]
```

## Step 2: High-Level Architecture Diagram

```markdown
### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Clients                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │   Web    │  │  Mobile  │  │   CLI    │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
└───────┼─────────────┼─────────────┼─────────────────────────┘
        │             │             │
        └─────────────┼─────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway                              │
│  • Authentication  • Rate Limiting  • Routing               │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Service A   │  │  Service B   │  │  Service C   │
│  [Purpose]   │  │  [Purpose]   │  │  [Purpose]   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Database │  │  Cache   │  │  Queue   │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```
```

## Step 3: Component Design

For each major component:

```markdown
### Component: [Name]

**Responsibility**: [Single responsibility description]
**Dependencies**: [What it needs]
**Dependents**: [What needs it]

**Interface**:
```
Input:  [Data it receives]
Output: [Data it produces]
Events: [Events it emits/consumes]
```

**Internal Structure**:
```
┌─────────────────────────────┐
│        [Component]          │
├─────────────────────────────┤
│ ┌─────────┐  ┌─────────┐   │
│ │ Module  │  │ Module  │   │
│ │   A     │──│   B     │   │
│ └─────────┘  └─────────┘   │
└─────────────────────────────┘
```

**Key Design Decisions**:
| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| [Decision 1] | [A, B, C] | [B] | [Why] |
```

## Step 4: Data Model Design

```markdown
### Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐
│    User      │       │   Account    │
├──────────────┤       ├──────────────┤
│ id (PK)      │───┐   │ id (PK)      │
│ email        │   │   │ user_id (FK) │◄──┘
│ name         │   │   │ status       │
│ created_at   │   │   │ balance      │
└──────────────┘   │   └──────────────┘
                   │
                   │   ┌──────────────┐
                   │   │ Transaction  │
                   │   ├──────────────┤
                   └──►│ id (PK)      │
                       │ account_id   │
                       │ amount       │
                       │ timestamp    │
                       └──────────────┘
```

### Entity Definitions

| Entity | Purpose | Key Attributes | Relationships |
|--------|---------|----------------|---------------|
| User | [Purpose] | id, email, name | Has many Accounts |
| Account | [Purpose] | id, status | Belongs to User |
```

## Step 5: Sequence Diagrams

For key interactions:

```markdown
### Sequence Diagram: [Use Case Name]

```
┌──────┐     ┌──────┐     ┌──────┐     ┌──────┐
│Client│     │  API │     │Service│    │  DB  │
└──┬───┘     └──┬───┘     └──┬───┘     └──┬───┘
   │            │            │            │
   │  Request   │            │            │
   │───────────►│            │            │
   │            │  Validate  │            │
   │            │───────────►│            │
   │            │            │   Query    │
   │            │            │───────────►│
   │            │            │   Result   │
   │            │            │◄───────────│
   │            │  Response  │            │
   │            │◄───────────│            │
   │  Response  │            │            │
   │◄───────────│            │            │
   │            │            │            │
```

**Timing Constraints**:
| Step | Max Duration | Fallback |
|------|--------------|----------|
| API → Service | 100ms | Timeout error |
| Service → DB | 50ms | Circuit breaker |
```

## Step 6: Technology Stack Decisions

```markdown
### Decision: Technology Stack

#### Runtime/Language

| Option | Pros | Cons | Team Experience |
|--------|------|------|-----------------|
| **[Option A] (Recommended)** | [Pros] | [Cons] | [High/Med/Low] |
| [Option B] | [Pros] | [Cons] | [High/Med/Low] |

#### Database

| Option | Type | Pros | Cons | Best For |
|--------|------|------|------|----------|
| **[Option A] (Recommended)** | [SQL/NoSQL] | [Pros] | [Cons] | [Use case] |
| [Option B] | [SQL/NoSQL] | [Pros] | [Cons] | [Use case] |

#### Infrastructure

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Hosting | [Choice] | [Why] |
| Container | [Choice] | [Why] |
| CI/CD | [Choice] | [Why] |
```

## Step 7: Critical Reflection

### Architecture Quality Attributes

| Attribute | How Addressed | Trade-offs |
|-----------|---------------|------------|
| **Scalability** | [Approach] | [What we sacrifice] |
| **Reliability** | [Approach] | [What we sacrifice] |
| **Maintainability** | [Approach] | [What we sacrifice] |
| **Security** | [Approach] | [What we sacrifice] |
| **Performance** | [Approach] | [What we sacrifice] |

### Validation Questions
- Does this architecture support all use cases?
- Can we meet NFRs with this design?
- Where are the single points of failure?
- How do we handle component failures?
- Is this overengineered for our needs?

## Phase 5 Approval Gate

```markdown
## Phase 5 Summary: Architecture & Design

### Architecture Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Style | [Choice] | [Why] |
| Language | [Choice] | [Why] |
| Database | [Choice] | [Why] |
| Hosting | [Choice] | [Why] |

### Components Designed
| Component | Responsibility | Dependencies |
|-----------|---------------|--------------|
| [Component A] | [Purpose] | [Deps] |
| [Component B] | [Purpose] | [Deps] |

### Data Entities
[List key entities and relationships]

### Key Sequence Flows
[List documented sequences]

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Plan] |

---

**Do you approve Phase 5? Any architecture changes before proceeding to Interface Contracts?**
```
