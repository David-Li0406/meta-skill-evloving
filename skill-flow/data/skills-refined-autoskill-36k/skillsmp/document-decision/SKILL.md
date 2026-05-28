---
name: document-decision
description: Create Architecture Decision Records (ADRs) documenting WHY decisions were made. Uses standard ADR format (Status/Context/Decision/Consequences).
---

# Document Architecture Decision

Use this skill when recording system design decisions for LikeC4-modeled architectures.

## Purpose

Create Architecture Decision Records (ADRs) that explain WHY architectural choices were made in the system diagrams, not HOW the diagrams are built or maintained.

## Scope

- ✅ System design decisions (e.g., why Kong API Gateway vs HAProxy, why MongoDB vs PostgreSQL)
- ✅ Container-level technology choices (e.g., why RabbitMQ for queuing, why MinIO for storage)
- ✅ Component architecture patterns (e.g., why async processing, why microservices)
- ✅ Deployment infrastructure choices (e.g., why 3-node replication, why specific VM sizing)
- ❌ NOT repository structure, tooling, CI/CD setup, or LikeC4 modeling decisions

## Format

1. **Filename:** `ADR/NNNN-decision-title.md` (manually increment NNNN)
2. **Template:** Use `ADR/0000-template.md` as reference
3. **Sections:** Status, Context, Decision, Consequences (Positive/Negative/Neutral)

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

## Integration with LikeC4

- Reference elements from diagrams: "The decision affects `mySystem.apiGateway` (Container_ReverseProxy)"
- Link to views: "See deployment view: `deployment_api_tier`"
- Tag related decisions: Use frontmatter or Notes section to link ADRs
