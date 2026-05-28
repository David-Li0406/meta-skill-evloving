---
name: optima-service-planner
description: Plan and implement microservices for Optima platform. Use when building new services, features, or integrations. Generates phased implementation roadmaps following Optima patterns - Database Gateway, append-only contracts, RabbitMQ messaging, DigitalOcean deployment. Start with data model, then contracts, then services.
---

# Optima Service Planner

Plan and implement production-ready microservices following Optima's proven architectural patterns.

## Overview

This skill generates **phased implementation roadmaps** for building new Optima microservices, ensuring consistency with the established patterns:

- **Database Service Gateway** - All DB access through a single service
- **Append-Only Contracts** - Shared message bus schemas that never break
- **Integration Service Pattern** - One service per external system
- **Event-Driven Architecture** - All inter-service communication via RabbitMQ

## Optima Prime Directives

| # | Directive | Implementation |
|---|-----------|----------------|
| 1 | **Documentation with code** | Update docs alongside every code change |
| 2 | **Data model first** | Start with database schema and migrations |
| 3 | **Message bus communication** | All services talk via RabbitMQ, never direct calls |
| 4 | **One integration service** | One service per external system (DB, CEX, provider) |
| 5 | **API backend via bus** | Website backend talks to services through message bus |
| 6 | **Errors to notifications** | All errors published to notification service |
| 7 | **Credentials in database** | Store secrets in DB, not environment variables |
| 8 | **DigitalOcean deployment** | YAML deployment configs, separate workers/webservices |
| 9 | **Append-only contracts** | Never modify existing schemas, only add new versions |
| 10 | **Stateless services** | State lives in message bus and database only |

## Implementation Phases

Every new service or feature follows this sequence:

```
Phase 1: Data Model
├── Database schema design
├── Migrations (Supabase)
└── Initial CLAUDE.md update

Phase 2: Contracts
├── New event types (append-only)
├── Zod validation schemas
└── Publish to @optima-financial/message-bus-contracts

Phase 3: Core Service
├── Message handlers
├── Business logic
├── Database operations (via DatabaseClient)
└── NotifyingLogger integration

Phase 4: Integration
├── External API clients (if integration service)
├── Credential loading at startup
├── Circuit breakers / retry logic
└── Error notification publishing

Phase 5: Deployment
├── DigitalOcean app.yaml
├── Health check endpoints
├── Environment variable configuration
└── Monitoring / alerting setup

Phase 6: Documentation
├── Update CLAUDE.md (tables, services, commands)
├── Update README.md
├── Create/update service-specific docs
├── Document API endpoints
└── Create operational runbook

Phase 7: Testing
├── Unit tests (business logic, handlers)
├── Integration tests (message bus, database)
├── E2E tests (full workflow execution)
├── Operational tests (health checks, alerts)
└── Manual testing scenarios
```

## Core Architectural Patterns

### Database Service Gateway

```
                   ┌─────────────────────┐
                   │   Database Service  │ ◄── ONLY service with DB access
                   │  (database-service) │
                   └──────────┬──────────┘
                              │
                              ▼
                        PostgreSQL
                        (Supabase)
                              ▲
                              │
┌─────────────┐    ┌─────────────────────┐
│  Service A  │───►│     Message Bus     │ ◄── All services use DatabaseClient
│  Service B  │───►│     (RabbitMQ)      │     to talk to database-service
│  Service C  │───►│                     │
└─────────────┘    └─────────────────────┘
```

**Rule:** Services import `DatabaseClient` from `@cfgi/shared/db-client`, never direct Supabase client.

### Append-Only Contracts

```typescript
// @optima-financial/message-bus-contracts

// NEVER modify existing types
EVENT_TYPES.DATA_INGESTED          // Frozen forever

// ALWAYS add new versions for changes
EVENT_TYPES.DATA_INGESTED_V2       // New version if schema changes

// NEVER remove or rename - would break consumers
```

**Repository:** https://github.com/Optima-Financial/message-bus-contracts

### Integration Service Pattern

| External System | Integration Service | Other Services |
|-----------------|---------------------|----------------|
| Supabase/PostgreSQL | `database-service` | Use `DatabaseClient` |
| KuCoin CEX | `trade-execution` | Publish trade intents |
| BitGo Custody | `custody-service` | Publish deposit/withdrawal events |
| CoinGecko | `market-data` | Request prices via events |
| Email (Gmail) | `notifications` | Publish notification events |

**Rule:** Only integration services touch external APIs. Others communicate via message bus.

## Service Architecture Template

Every Optima service follows this structure:

```typescript
// Service initialization pattern
async function start() {
  // 1. Connect to message bus
  const messageBus = getMessageBus({ serviceName: "my-service" });
  await messageBus.connect();

  // 2. Set up notifying logger (REQUIRED)
  const notifyingLogger = wrapWithNotifications(app.log, {
    serviceName: "my-service",
    messageBus,
    environment,
  });

  // 3. Register global error handlers
  registerGlobalErrorHandlers({
    logger: notifyingLogger,
    serviceName: "my-service",
    onFatalError: async () => {
      await messageBus.close();
      await app.close();
    },
  });

  // 4. Initialize DatabaseClient (if needed)
  const db = getDatabaseClient({ serviceName: "my-service" });
  await db.initialize();

  // 5. Load credentials at startup (integration services only)
  if (needsCredentials) {
    await credentialStore.initialize(messageBus);
  }

  // 6. Subscribe to message handlers
  await messageBus.subscribe(EVENT_TYPES.SOME_EVENT, handleSomeEvent);

  // 7. Start server
  await app.listen({ port: PORT, host: "0.0.0.0" });
}
```

## Planning Workflow

When planning a new service or feature:

### 1. Gather Requirements
- What business problem does this solve?
- What existing services does it interact with?
- What external systems does it integrate with?
- What data does it need to store/access?

### 2. Design Data Model
- What tables are needed?
- What are the relationships?
- What indexes are required?
- Follow Optima conventions (TEXT not VARCHAR, etc.)

### 3. Define Contracts
- What events does this service publish?
- What events does this service subscribe to?
- Define Zod schemas for all payloads
- Add to message-bus-contracts (append-only!)

### 4. Design Service
- Message handlers
- Database operations (via DatabaseClient)
- Business logic
- Error handling (via NotifyingLogger)

### 5. Plan Deployment
- DigitalOcean configuration
- Environment variables
- Health checks
- Monitoring

### 6. Update Documentation
- Update CLAUDE.md with new tables and services
- Update README.md with new commands/features
- Create service-specific documentation
- Document all API endpoints
- Create operational runbook

### 7. Plan Testing Strategy
- Unit tests for business logic and handlers
- Integration tests for message bus and database
- E2E tests for full workflow execution
- Operational tests for health checks and alerts
- Manual testing scenarios and verification

## Supporting Files

- [PATTERNS.md](PATTERNS.md) — Detailed Optima architectural patterns
- [TEMPLATES.md](TEMPLATES.md) — Service spec, deployment, contract templates
- [PHASES.md](PHASES.md) — Detailed implementation phases
- [CHECKLIST.md](CHECKLIST.md) — Implementation quality checklist

## Trigger Phrases

This skill activates when you:
- "Plan a new Optima service for..."
- "Design a service that..."
- "What's the implementation plan for..."
- "Add a new feature to Optima..."
- "Create an integration with..."
- "Build a microservice for..."

## Key Technologies

| Component | Technology |
|-----------|------------|
| Message Bus | RabbitMQ (AMQP) |
| Database | PostgreSQL (Supabase) |
| Runtime | Node.js + TypeScript |
| Web Framework | Fastify |
| Validation | Zod |
| Logging | Pino |
| Deployment | DigitalOcean App Platform |
| Package Registry | GitHub Packages |
