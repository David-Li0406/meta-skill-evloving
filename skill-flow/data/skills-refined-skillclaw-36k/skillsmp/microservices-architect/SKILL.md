---
name: microservices-architect
description: Design and architect microservices following Chris Richardson's Microservices Patterns. Use when designing services, APIs, data flows, or evaluating architecture decisions. Guides full workflow from feature intake to production-ready design with observability, async patterns, security, testing, and deployment strategies.
---

# Microservices Architect

Design production-ready microservices following Chris Richardson's *Microservices Patterns* with battle-tested principles for observability, reliability, and operability.

## Overview

This skill guides you through microservices design with a focus on:
- **Operability over cleverness** — Systems we can run, trust, and evolve
- **Observability first** — If you can't see it, you can't trust it
- **Async by default** — Pub/sub patterns for resilience
- **Explicit trust** — Security and authorization built-in

## Prime Directives (Non-Negotiables)

These are the rules every microservices design must follow. Exceptions require explicit justification.

| # | Directive | Meaning |
|---|-----------|---------|
| 1 | **Nothing unwatched exists** | Ship observability with every feature. Know before customers. |
| 2 | **Produce it → publish it. Consume it → consume all** | Client-side filtering; wire is a consistent, schema'd data space |
| 3 | **Pub/sub by default** | Prefer event-driven; route through wireline formats quickly |
| 4 | **Async by default; sync only when unavoidable** | Pub/sub default; sync only for ACID/idempotency; isolate with feature flags |
| 5 | **Trust must be explicit, scoped, and observable** | Authenticate everything; authorize narrowly; emit signals on failures |
| 6 | **Customers report it first = failure** | Breaks happen; surprise is the failure. Detect before impact. |
| 7 | **Observability over performance** | Accept 20-30% overhead to eliminate blind spots |
| 8 | **Siloing/bulkheading by design** | Not using bulkheads = deployment choice. Not supporting them = architecture failure |
| 9 | **Explicit Runtime Trust Profile** | Time-bound, observable, revocable trust; policy via profiles, not patches |
| 10 | **Operational knobs must be exposed** | Expose the control, inputs, and effects. Operating > building |

## Design Workflow

For every feature request, produce these outputs:

### 1. Design
- Message flows and sequence diagrams
- Schemas (events, commands, queries)
- Idempotency strategy
- Failure modes and recovery

### 2. Operability
- What to observe (metrics, logs, traces)
- Alerting signals and thresholds
- Operational "knobs" (feature flags, circuit breakers, rate limits)

### 3. Safety
- Containment/bulkheading strategy
- Blast radius analysis
- Rollback plan

### 4. Tests
- Operational tests that validate behavior + observability
- Consumer-driven contract tests
- Component integration tests

### 5. Implementation Plan
- Small, incremental steps
- Strangler fig approach for refactoring
- Emit insight events describing changes

## Operating Stance

When designing microservices, default to:

```
┌─────────────────────────────────────────────────────────────┐
│  Pub/sub by default                                         │
│  Async by default                                           │
│  Sync only when unavoidable → isolate behind interfaces     │
│  "Nothing unwatched exists"                                 │
│  "If customers report it first, we have already failed"    │
│  Bulkheading/siloing must be possible by design             │
│  Security/trust is explicit and scoped                      │
└─────────────────────────────────────────────────────────────┘
```

## Style

- Be direct
- Treat exceptions as exceptions
- If there is ambiguity, choose the safer path and emit insight
- Refactoring steps emit insight events (what changed, what diverged, what decision was taken)

## Supporting Files

- [AXIOMS.md](AXIOMS.md) — Core architectural principles
- [PATTERNS.md](PATTERNS.md) — Detailed Richardson patterns
- [TEMPLATES.md](TEMPLATES.md) — Feature intake and design output templates
- [CHECKLIST.md](CHECKLIST.md) — Quality validation checklist

## Quick Pattern Reference

| Category | Patterns |
|----------|----------|
| **Data & Query** | API Composition, Materialized View, CQRS |
| **External APIs** | API Gateway, Backend-for-Frontend (BFF), Protocol Handler |
| **Testing** | Consumer-Driven Contracts, Component Testing, Operational Testing |
| **Deployment** | Blue-Green, Canary, Strangler Fig, Continuous Delivery |
| **Observability** | Health Checks, Distributed Tracing, Log Aggregation, Alerting |
| **Security** | Zero Trust, Runtime Trust Profile, Trust-as-Actor |
| **Resilience** | Circuit Breaker, Bulkhead, Retry with Backoff |

## Trigger Phrases

This skill activates when you:
- "Design a microservice for..."
- "Architect a service that..."
- "Review this service design"
- "What patterns should I use for..."
- "Help me decompose this monolith"
- "Create an API for..."
- "Design the data flow for..."
