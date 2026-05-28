---
name: domain-cloud-native
description: Use this skill when building cloud-native applications that require adherence to best practices in microservices architecture, including observability, health checks, and graceful shutdowns.
---

# Cloud-Native Domain

> **Layer 3: Domain Constraints**

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| 12-Factor | Config from env | Environment-based config |
| Observability | Metrics + traces | tracing + opentelemetry |
| Health checks | Liveness/readiness | Dedicated endpoints |
| Graceful shutdown | Clean termination | Signal handling |
| Horizontal scale | Stateless design | No local state |
| Container-friendly | Small binaries | Release optimization |

---

## Critical Constraints

### Stateless Design

```
RULE: No local persistent state
WHY: Pods can be killed/rescheduled anytime
RUST: External state (Redis, DB), no static mut
```

### Graceful Shutdown

```
RULE: Handle SIGTERM, drain connections
WHY: Zero-downtime deployments
RUST: tokio::signal + graceful shutdown
```

### Observability

```
RULE: Every request must be traceable
WHY: Debugging distributed systems
RUST: tracing spans, opentelemetry export
```

---

## Trace Down ↓

From constraints to design (Layer 2):

```
"Need distributed tracing"
    ↓ m12-lifecycle: Span lifecycle
    ↓ tracing + opentelemetry

"Need graceful shutdown"
    ↓ m07-concurrency: Signal handling
    ↓ m12-lifecycle: Connection draining

"Need health checks"
    ↓ domain-web: HTTP endpoints
    ↓ m06-error-handling: Health status
```

---

## Key Crates

| Purpose | Crate |
|---------|-------|
| gRPC | tonic |
| Kubernetes | kube, kube-runtime |
| Docker | bollard |
| Tracing | tracing, opentelemetry |
| Metrics | prometheus, metrics |
| Config | config, figment |
| Health | HTTP endpoints |

## Design Patterns

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| gRPC services | Service mesh | tonic + tower |
| K8s operators | Custom resources | kube-runtime Controller |
| Observability | Debugging | tracing + OTEL |
| Health checks | Orchestration | `/health`, `/ready` |
| Config | 12-factor | Env vars + secrets |

## Code Pattern: Graceful Shutdown

```rust
use tokio::signal;

async fn run_server() -> anyhow::Result<()> {
    let app = Router::new()
        .route("/health", get(health))
        .route("/ready", get(ready));
```