---
name: jikime-domain-architecture
description: Comprehensive software architecture design guide covering pattern selection, directory structures, trade-off analysis, and architectural decision records for projects of all sizes.
version: 1.0.0
tags: ["domain", "architecture", "design-patterns", "system-design", "adr", "clean-architecture"]
triggers:
  keywords: ["architecture", "design pattern", "system design", "structure", "monolith", "microservices", "아키텍처", "설계 패턴", "시스템 설계", "구조"]
  phases: ["plan", "run"]
  agents: ["architect", "manager-strategy"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~7000
user-invocable: false
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# Software Architecture Design Guide

## Quick Reference (30 seconds)

Architecture Design Guide - Systematic approach to selecting, implementing, and documenting software architecture patterns.

Core Philosophy:
- **Start Simple**: Begin with the simplest architecture that meets requirements, evolve when needed.
- **Team-Aligned**: Match architecture complexity to team capabilities.
- **Documented**: Every significant decision should have an ADR (Architecture Decision Record).

Key Capabilities:
- Pattern selection by project/team size
- 7 architecture patterns with visual diagrams
- Directory structure templates
- Decision framework and trade-off analysis
- ADR templates and examples

Quick Commands:
- Architecture review: Use architect agent
- System design: `/jikime:1-plan --ultrathink`
- Trade-off analysis: Use manager-strategy agent

---

## Implementation Guide (5 minutes)

### Architecture Decision Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Step 1: UNDERSTAND     Step 2: ASSESS        Step 3: SELECT            │
│  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐         │
│  │ Requirements  │────▶│ Project Size  │────▶│  Architecture │         │
│  │ & Constraints │     │ & Team Skills │     │    Pattern    │         │
│  └───────────────┘     └───────────────┘     └───────────────┘         │
│         │                                            │                  │
│         │         Step 5: DOCUMENT           Step 4: STRUCTURE         │
│         │         ┌───────────────┐         ┌───────────────┐          │
│         └─────────│     ADR       │◀────────│   Directory   │          │
│                   │   Creation    │         │    Layout     │          │
│                   └───────────────┘         └───────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Understand Requirements

**Requirements Checklist:**

```markdown
## Functional Requirements
- [ ] Core features and user stories defined
- [ ] Integration points identified
- [ ] Data model understood

## Non-Functional Requirements (NFRs)
- [ ] Performance: Expected load, response times
- [ ] Scalability: Growth trajectory, peak loads
- [ ] Security: Compliance, data sensitivity
- [ ] Availability: Uptime requirements, SLA
- [ ] Maintainability: Change frequency, team turnover
```

**Constraint Categories:**

| Category | Questions to Answer |
|----------|---------------------|
| **Technical** | Existing tech stack? Legacy integrations? |
| **Business** | Budget? Timeline? Regulatory requirements? |
| **Team** | Size? Experience level? Distributed? |
| **Operational** | Deployment frequency? Monitoring needs? |

### Step 2: Assess Project & Team

**Project Size Matrix:**

| Size | Lines of Code | Features | Recommended Complexity |
|------|---------------|----------|------------------------|
| **Small** | < 10K | < 10 | Simple (Layered, MVC) |
| **Medium** | 10K - 100K | 10-50 | Moderate (Clean, Hexagonal) |
| **Large** | 100K - 500K | 50-200 | Complex (Modular Monolith) |
| **Enterprise** | > 500K | > 200 | Distributed (Microservices) |

**Team Size Matrix:**

| Team | Coordination | Recommended |
|------|--------------|-------------|
| **1-3 devs** | Minimal | Monolith with clear modules |
| **4-10 devs** | Moderate | Modular Monolith, clear boundaries |
| **10-30 devs** | Significant | Service-Oriented, domain teams |
| **30+ devs** | Complex | Microservices (if justified) |

**Decision Matrix:**

```
         Small Team ◀────────────────▶ Large Team
              │                            │
    Simple ───┼────────────────────────────┼─── Complex
    Project   │     ┌─────────────┐        │   Project
              │     │   MODULAR   │        │
              │     │  MONOLITH   │        │
              │     │  (Sweet     │        │
              │     │   Spot)     │        │
              │     └─────────────┘        │
              │                            │
         MONOLITH                    MICROSERVICES
```

### Step 3: Select Architecture Pattern

For detailed diagrams and explanations, see:
- [Architecture Patterns](modules/architecture-patterns.md) - All 7 patterns with visual diagrams

| Pattern | Complexity | Best For |
|---------|------------|----------|
| **Layered** | Simple | CRUD apps, small teams, prototypes |
| **Clean** | Moderate | Complex business logic, testability |
| **Hexagonal** | Moderate | Multiple entry points, swappable deps |
| **Event-Driven** | Complex | Loose coupling, async processing |
| **CQRS** | Complex | Different read/write scaling |
| **Modular Monolith** | Moderate | Medium-large projects (recommended) |
| **Microservices** | Complex | Large distributed teams, polyglot |

### Step 4: Define Directory Structure

#### Feature-Based (Recommended for Medium+)

```
src/
├── features/                    # Domain features
│   ├── users/
│   │   ├── api/                # Route handlers, controllers
│   │   │   ├── users.controller.ts
│   │   │   └── users.routes.ts
│   │   ├── application/        # Use cases, services
│   │   │   ├── create-user.ts
│   │   │   └── get-user.ts
│   │   ├── domain/             # Entities, value objects
│   │   │   ├── user.entity.ts
│   │   │   └── email.value-object.ts
│   │   ├── infrastructure/     # External implementations
│   │   │   └── user.repository.ts
│   │   └── index.ts            # Public API
│   │
│   └── orders/
│       ├── api/
│       ├── application/
│       ├── domain/
│       └── infrastructure/
│
├── shared/                      # Cross-cutting concerns
│   ├── domain/                 # Shared value objects
│   ├── infrastructure/         # Shared adapters
│   └── utils/                  # Pure utility functions
│
└── app/                         # Application bootstrap
    ├── config/
    ├── middleware/
    └── main.ts
```

#### Layer-Based (Simple Apps)

```
src/
├── controllers/                # HTTP layer
│   ├── user.controller.ts
│   └── order.controller.ts
├── services/                   # Business logic
│   ├── user.service.ts
│   └── order.service.ts
├── models/                     # Data models
│   ├── user.model.ts
│   └── order.model.ts
├── repositories/               # Data access
│   ├── user.repository.ts
│   └── order.repository.ts
├── middlewares/                # Express middlewares
├── utils/                      # Helper functions
└── app.ts                      # Entry point
```

### Step 5: Document with ADR

**ADR Template:**

```markdown
# ADR-{NUMBER}: {Title}

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Date
YYYY-MM-DD

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision Drivers
- [Driver 1]
- [Driver 2]
- [Constraint 1]

## Considered Options
1. **Option A**: [Description]
2. **Option B**: [Description]
3. **Option C**: [Description]

## Decision
We chose **Option X** because [reasoning].

## Trade-off Analysis

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| Complexity | Low | Medium | High |
| Scalability | Low | High | High |
| Team familiarity | High | Medium | Low |
| Time to implement | 1 week | 3 weeks | 6 weeks |

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Mitigation strategy]

### Risks
- [Risk 1]: [Mitigation]

## Related Decisions
- ADR-XXX: [Related decision]

## Notes
[Any additional context or references]
```

---

## Advanced Implementation (10+ minutes)

### Architecture Fitness Functions

Automated tests that verify architectural decisions:

```typescript
// No domain depending on infrastructure
describe('Architecture Fitness', () => {
  it('domain should not import infrastructure', () => {
    const domainFiles = glob.sync('src/**/domain/**/*.ts');
    for (const file of domainFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content).not.toMatch(/from ['"].*infrastructure/);
    }
  });

  it('features should not cross-import', () => {
    const usersFiles = glob.sync('src/features/users/**/*.ts');
    for (const file of usersFiles) {
      const content = fs.readFileSync(file, 'utf-8');
      expect(content).not.toMatch(/from ['"].*features\/orders/);
    }
  });
});
```

### Module Dependency Analysis

```bash
# Visualize module dependencies
npx madge --image graph.svg src/

# Detect circular dependencies
npx madge --circular src/
```

---

## Works Well With

Commands:
- `/jikime:1-plan --ultrathink` - Deep architecture planning
- `/jikime:architect` - Architecture review

Skills:
- `jikime-foundation-core` - Core patterns and SPEC workflow
- `jikime-workflow-spec` - SPEC document creation
- `jikime-domain-backend` - Backend implementation patterns
- `jikime-domain-frontend` - Frontend architecture patterns

Agents:
- `architect` - System architecture specialist
- `manager-strategy` - Strategic decision making
- `manager-spec` - Requirements and SPEC creation

---

## Quick Decision Guide

| Scenario | Recommended Pattern |
|----------|---------------------|
| MVP/Prototype | Layered Architecture |
| SaaS product (1-3 devs) | Clean Architecture |
| Growing product (4-10 devs) | Modular Monolith |
| Enterprise (10+ devs, multiple teams) | Microservices (if mature DevOps) |
| High async processing | Event-Driven |
| Complex read/write patterns | CQRS |
| Multiple external integrations | Hexagonal |

---

## Validation Checklist

```
Architecture Validation:
- [ ] Pattern matches project size and complexity
- [ ] Architecture aligns with team skills and experience
- [ ] Current requirements are supported
- [ ] Anticipated growth can be accommodated
- [ ] Dependencies flow inward (core has no external deps)
- [ ] Clear boundaries between modules/layers
- [ ] Testing strategy is feasible with this architecture
- [ ] Trade-offs are documented in ADR
- [ ] Fitness functions defined for critical constraints
```

---

Version: 1.0.0
Last Updated: 2026-01-25
Integration Status: Complete - Full architecture design workflow
