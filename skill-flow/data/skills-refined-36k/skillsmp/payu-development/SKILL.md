---
name: payu-development
description: High-level development guide for PayU Digital Banking Platform - architecture overview, technology stack, and entry point for specialized skills.
---

# PayU Digital Banking Development (High-Level)

This skill provides the architectural overview and entry points for developing the **PayU Digital Banking Platform**. For specific implementation details, refer to the specialized skills.

## Project Overview

| Attribute | Value |
|-----------|-------|
| **Project Name** | PayU |
| **Type** | Standalone Digital Banking Platform |
| **Platform** | Red Hat OpenShift 4.20+ |
| **Primary Languages** | Java 21 (Core), Python 3.12 (ML) |

### Microservices Map

```
payu/backend/
├── account-service/      # [Spring Boot] User accounts, eKYC
├── auth-service/         # [Spring Boot] Authentication, OAuth2
├── transaction-service/  # [Spring Boot] Transfers, BI-FAST, QRIS
├── wallet-service/       # [Spring Boot] Balance, Ledger (Hexagonal)
├── billing-service/      # [Quarkus]     Bill payments
├── notification-service/ # [Quarkus]     Push, SMS, Email
├── gateway-service/      # [Quarkus]     API Gateway
├── kyc-service/          # [FastAPI]     OCR, Liveness ML
└── analytics-service/    # [FastAPI]     Insights, TimescaleDB
```

## Specialized Skills Map

| Task Category | Use Skill | Description |
|---------------|-----------|-------------|
| **Backend Implementation** | `@backend-engineer` | Frameworks (Spring/Quarkus), DB, API, Kafka patterns |
| **Testing & QA** | `@qa-expert` | TDD workflow, Testcontainers, Integration tests |
| **Security & Compliance** | `@security-specialist` | PCI-DSS, Secure Coding, OJK Compliance, PII |
| **Code Review** | `@code-review` | Code quality checklist, Hygiene, Style guide |
| **Containers** | `@container-specialist` | Dockerfiles, OpenShift, UBI Images |

## Core Architecture Patterns

### 1. Hexagonal Architecture (Core Banking)
Used in Account, Auth, Transaction, Wallet services.
- Decouples domain logic from frameworks.
- Easier to test business rules in isolation.

### 2. Event-Driven Architecture
- **Broker**: AMQ Streams (Kafka).
- **Pattern**: Saga for distributed transactions.
- **Consistency**: Eventual consistency for cross-service operations.

### 3. Polyglot Persistence
- **PostgreSQL**: Primary transactional storage (isolated schemas).
- **Redis**: Caching and distributed locks.
- **TimescaleDB**: Time-series analytics.

### 4. Observability
- **Logs**: LokiStack (JSON Structured).
- **Metrics**: Prometheus/Grafana.
- **Traces**: Jaeger (OpenTelemetry).

---
*ALWAYS use the specialized skills for deeper context when performing specific tasks.*
