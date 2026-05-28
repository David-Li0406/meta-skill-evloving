# faion-software-architect

Software architecture skill for system design, technology selection, and architecture decision records.

## Overview

| Metric | Value |
|--------|-------|
| Methodologies | 28 |
| Agents | 2 |

## Directory Structure

```
faion-software-architect/
├── SKILL.md                    # Main skill definition
├── CLAUDE.md                   # This file
├── decision-trees.md           # Architecture decision trees
└── patterns.md                 # Design patterns reference
```

## When to Use

| Trigger | Action |
|---------|--------|
| "Design architecture for..." | System design workflow |
| "Should we use X or Y?" | Technology selection |
| "How to scale to...?" | Quality attributes analysis |
| "Document why we chose..." | Create ADR |
| "Review this architecture" | Design review |

## Key Decision Trees

### Architecture Style

```
Small team / MVP → Monolith or Modular Monolith
Large team / Independent deploy → Microservices
Unclear boundaries → Modular Monolith (extract later)
```

### Database Selection

```
Relational data → PostgreSQL / MySQL
Document data → MongoDB / DynamoDB
Key-value → Redis
Time-series → TimescaleDB
Graph → Neo4j
Search → Elasticsearch
```

### Communication Pattern

```
Sync internal → gRPC or REST
Sync external → REST or GraphQL
Async ordered → Kafka
Async unordered → RabbitMQ / SQS
Real-time → WebSockets or SSE
```

## Quality Attributes

| Attribute | Key Question |
|-----------|--------------|
| Scalability | Handle 10x load? |
| Performance | Latency p95 < 200ms? |
| Availability | 99.9% or 99.99%? |
| Security | Threat model done? |
| Maintainability | Deploy daily? |

## ADR Template (Quick)

```markdown
# ADR-NNN: Title
## Status: Proposed/Accepted
## Context: Why is this decision needed?
## Decision: What we decided
## Consequences: Trade-offs
## Alternatives: What else was considered
```

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-software-developer | Implements the architecture |
| faion-devops-engineer | Implements infrastructure |
| faion-product-manager | Provides requirements |

---

*faion-software-architect v1.0*
