# Optima Architectural Patterns

Detailed patterns and conventions for building Optima microservices.

---

## Database Service Gateway Pattern

### Overview

The Database Service Gateway is the **ONLY** service with direct database access. All other services communicate with it via RabbitMQ message bus.

### Why This Pattern?

| Benefit | Description |
|---------|-------------|
| **Single point of control** | All DB operations go through one service |
| **Credential isolation** | Only one service needs DB credentials |
| **Audit trail** | Easy to log and monitor all DB access |
| **Schema consistency** | Centralized query/command handling |
| **Easier testing** | Mock DatabaseClient instead of database |

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION LAYER                              │
│                                                                          │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                │
│   │  Service A   │   │  Service B   │   │  Service C   │                │
│   │              │   │              │   │              │                │
│   │ DatabaseClient   │ DatabaseClient   │ DatabaseClient               │
│   └──────┬───────┘   └──────┬───────┘   └──────┬───────┘                │
│          │                  │                  │                         │
│          └──────────────────┼──────────────────┘                         │
│                             │                                            │
│                             ▼                                            │
│                    ┌─────────────────┐                                   │
│                    │   Message Bus   │                                   │
│                    │   (RabbitMQ)    │                                   │
│                    └────────┬────────┘                                   │
│                             │                                            │
└─────────────────────────────┼────────────────────────────────────────────┘
                              │
┌─────────────────────────────┼────────────────────────────────────────────┐
│                             ▼             DATA LAYER                     │
│                    ┌─────────────────┐                                   │
│                    │ Database Service│                                   │
│                    │                 │                                   │
│                    │ Query Handlers  │                                   │
│                    │ Command Handlers│                                   │
│                    └────────┬────────┘                                   │
│                             │                                            │
│                             ▼                                            │
│                    ┌─────────────────┐                                   │
│                    │   PostgreSQL    │                                   │
│                    │   (Supabase)    │                                   │
│                    └─────────────────┘                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Implementation

**Service code (uses DatabaseClient):**
```typescript
import { getDatabaseClient } from "@cfgi/shared/db-client";

const db = getDatabaseClient({ serviceName: "my-service" });
await db.initialize();

// All operations go via message bus to database-service
const strategies = await db.getActiveStrategies();
await db.createIntent(intent);
await db.updateBalance(userId, strategyId, amount);
```

**DatabaseClient methods:**
| Method | Event Type | Description |
|--------|------------|-------------|
| `getActiveStrategies()` | DB_QUERY | Get all active strategies |
| `getStrategy(id)` | DB_QUERY | Get single strategy |
| `createIntent(intent)` | DB_COMMAND | Create trade intent |
| `updateBalance(...)` | DB_COMMAND | Update user balance |
| `getCredentials(type)` | CREDENTIAL_REQUEST | Get encrypted credentials |
| `getConfigValue(key)` | DB_QUERY | Get operational config |

---

## Append-Only Contracts Pattern

### Overview

All message bus event types and schemas are defined in a shared npm package: `@optima-financial/message-bus-contracts`. This package follows **append-only** semantics - existing schemas are never modified.

### Why Append-Only?

| Problem | Solution |
|---------|----------|
| Breaking changes crash consumers | Never modify, only add |
| Version hell across repos | Single source of truth |
| Runtime validation failures | Zod schemas catch issues |
| Unclear event contracts | Type-safe definitions |

### Repository Structure

```
@optima-financial/message-bus-contracts
├── src/
│   ├── queues/
│   │   ├── index.ts      # EVENT_TYPES, QUEUES, EXCHANGES
│   │   └── routing.ts    # eventTypeToRoutingKey()
│   ├── events/
│   │   ├── index.ts      # Zod schemas for all events
│   │   ├── data.ts       # Data ingestion events
│   │   ├── trading.ts    # Trading events
│   │   └── db.ts         # Database events
│   └── types/
│       └── index.ts      # TypeScript type exports
└── package.json
```

### Event Type Conventions

```typescript
// Good: Add new event types
export const EVENT_TYPES = {
  DATA_INGESTED: "DATA_INGESTED",
  EVALUATION_COMPLETE: "EVALUATION_COMPLETE",
  TRADE_EXECUTED: "TRADE_EXECUTED",
  // NEW: Just add at the end
  NEW_FEATURE_EVENT: "NEW_FEATURE_EVENT",
} as const;

// Bad: Never modify or remove existing types
// DATA_INGESTED: "DATA_INGESTED_RENAMED"  // ❌ Breaks consumers
// DATA_INGESTED: removed                   // ❌ Breaks consumers
```

### Schema Versioning

```typescript
// Original schema - FROZEN forever
export const TradeExecutedPayloadV1 = z.object({
  trade_id: z.string().uuid(),
  intent_id: z.string().uuid(),
  status: z.enum(["SUCCESS", "FAILED"]),
});

// New version with additional fields
export const TradeExecutedPayloadV2 = z.object({
  trade_id: z.string().uuid(),
  intent_id: z.string().uuid(),
  status: z.enum(["SUCCESS", "FAILED", "PARTIAL"]),  // Extended enum
  filled_quantity: z.number(),                        // New field
  average_price: z.number(),                          // New field
});

// Backward-compatible union for consumers that support both
export type TradeExecutedPayload =
  | z.infer<typeof TradeExecutedPayloadV1>
  | z.infer<typeof TradeExecutedPayloadV2>;
```

### Version Bumping Rules

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Add new event type | Minor (1.3.0 → 1.4.0) | Added `NEW_EVENT` |
| Add optional field to schema | Patch (1.4.0 → 1.4.1) | Added optional `metadata` |
| Add new schema version | Minor (1.4.0 → 1.5.0) | Added `PayloadV2` |
| Remove/rename event | **NEVER** | Would break consumers |
| Change field type | **NEVER** | Would break consumers |

---

## Integration Service Pattern

### Overview

Each external system has exactly ONE integration service. Other services never touch external APIs directly - they communicate via message bus events.

### Service Mapping

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INTEGRATION SERVICES                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐    │
│  │ database-service│     │ trade-execution │     │ custody-service │    │
│  │                 │     │                 │     │                 │    │
│  │   PostgreSQL    │     │     KuCoin      │     │     BitGo       │    │
│  │   (Supabase)    │     │   Spot/Futures  │     │    Wallets      │    │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘    │
│           │                       │                       │              │
│           └───────────────────────┼───────────────────────┘              │
│                                   │                                      │
│                                   ▼                                      │
│                          ┌─────────────────┐                             │
│                          │   Message Bus   │                             │
│                          └─────────────────┘                             │
│                                   ▲                                      │
│           ┌───────────────────────┼───────────────────────┐              │
│           │                       │                       │              │
│  ┌────────┴────────┐     ┌────────┴────────┐     ┌────────┴────────┐    │
│  │  market-data    │     │  notifications  │     │  data-ingestion │    │
│  │                 │     │                 │     │                 │    │
│  │   CoinGecko     │     │     Gmail       │     │   CFGI API      │    │
│  │   Prices        │     │     SMTP        │     │   Webhooks      │    │
│  └─────────────────┘     └─────────────────┘     └─────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### How Other Services Interact

```typescript
// ❌ WRONG: Direct external API call
const prices = await fetch("https://api.coingecko.com/...");

// ✅ RIGHT: Request via message bus
await messageBus.publish(EVENT_TYPES.PRICE_REQUEST, {
  correlation_id: uuid(),
  assets: ["BTC", "ETH"],
});

// Listen for response
messageBus.subscribe(EVENT_TYPES.PRICE_RESPONSE, async (event) => {
  if (event.correlation_id === myCorrelationId) {
    const prices = event.prices;
  }
});
```

### Credential Management

Integration services load credentials **ONCE at startup** from database-service:

```typescript
class IntegrationService {
  private credentialStore: CredentialStore;

  async initialize(messageBus: MessageBus): Promise<void> {
    // Load credentials at startup (one-time)
    await this.credentialStore.initialize(messageBus);

    // Initialize external client
    const creds = this.credentialStore.getCredentials();
    this.externalClient = new ExternalClient(creds);

    // Subscribe to credential rotation (rare)
    messageBus.subscribe(EVENT_TYPES.CREDENTIAL_ROTATED, async (event) => {
      const newCreds = await this.credentialStore.refresh(messageBus);
      this.externalClient = new ExternalClient(newCreds);
    });
  }
}
```

---

## NotifyingLogger Pattern

### Overview

All Optima services use the NotifyingLogger pattern to automatically publish error alerts to the notification service.

### Implementation

```typescript
import {
  wrapWithNotifications,
  registerGlobalErrorHandlers,
  type Environment
} from "@cfgi/shared/logger";

async function start() {
  const messageBus = getMessageBus({ serviceName: "my-service" });
  await messageBus.connect();

  // Wrap Fastify logger with notification publishing
  const environment = process.env.NODE_ENV === "production"
    ? "production"
    : "development";

  const notifyingLogger = wrapWithNotifications(app.log, {
    serviceName: "my-service",
    messageBus,
    environment,
  });

  // Register global handlers for uncaught exceptions
  registerGlobalErrorHandlers({
    logger: notifyingLogger,
    serviceName: "my-service",
    onFatalError: async () => {
      await messageBus.close();
      await app.close();
    },
  });

  // Use notifyingLogger throughout service
  notifyingLogger.info("Service starting");
  notifyingLogger.error({ err }, "Something failed"); // → Publishes alert
}
```

### Error Flow

```
Service Error
    │
    ▼
logger.error() / logger.fatal()
    │
    ▼
Publish NOTIFICATION_ERROR_ALERT
    │
    ▼
Notification Service
    │
    ├── Batch errors (15-minute windows)
    ├── Deduplicate by message hash
    └── Send email summary
```

---

## Stateless Service Pattern

### Overview

Optima services are **stateless** - they don't maintain any in-memory state between requests. All state lives in:

1. **Message bus** - In-flight messages and queues
2. **Database** - Persistent state (via database-service)
3. **External systems** - CEX positions, wallet balances

### Why Stateless?

| Benefit | Description |
|---------|-------------|
| **Horizontal scaling** | Add more instances without coordination |
| **Crash recovery** | Restart without losing state |
| **Deployment simplicity** | Rolling updates without draining |
| **Debugging** | State is always queryable from DB |

### What IS Allowed In-Memory

| Allowed | Example |
|---------|---------|
| Credentials (at startup) | KuCoin API keys |
| Configuration | Operational config values |
| Caches with TTL | Price cache (5-minute TTL) |
| Message bus connection | RabbitMQ client |

### What IS NOT Allowed

| Not Allowed | Why |
|-------------|-----|
| User session state | Lost on restart |
| Processing state | Can't recover after crash |
| Counters/metrics | Won't aggregate across instances |
| Workflow state | Use database or message bus |

---

## Request/Response Over Message Bus

### Overview

For operations that need a response (like database queries), Optima uses a correlation ID pattern over the message bus.

### Flow

```
┌────────────────┐                          ┌─────────────────┐
│    Service     │                          │ Database Service│
│                │                          │                 │
│  1. Generate   │                          │                 │
│     correlation│                          │                 │
│     ID         │                          │                 │
│                │                          │                 │
│  2. Subscribe  │                          │                 │
│     to response│                          │                 │
│     queue      │                          │                 │
│                │                          │                 │
│  3. Publish    │─────── DB_QUERY ────────►│  4. Process     │
│     request    │    (correlation_id)      │     query       │
│                │                          │                 │
│  6. Handle     │◄───── DB_RESPONSE ───────│  5. Publish     │
│     response   │    (correlation_id)      │     response    │
│                │                          │                 │
└────────────────┘                          └─────────────────┘
```

### Implementation

```typescript
// Request
const correlationId = uuid();
const responsePromise = messageBus.waitForResponse(
  EVENT_TYPES.DB_RESPONSE,
  correlationId,
  { timeout: 5000 }
);

await messageBus.publish(EVENT_TYPES.DB_QUERY, {
  correlation_id: correlationId,
  operation: "QUERY",
  entity: "strategies",
  action: "list",
  params: { is_active: true },
});

// Wait for response
const response = await responsePromise;
if (response.success) {
  return response.data;
} else {
  throw new Error(response.error.message);
}
```

---

## Health Check Pattern

### Required Endpoints

Every Optima service exposes:

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `/health` | Liveness probe | `{ status: "ok" }` |
| `/health/ready` | Readiness probe | `{ status: "ready", checks: {...} }` |

### Readiness Checks

```typescript
app.get("/health/ready", async (request, reply) => {
  const checks = {
    messageBus: messageBus.isConnected(),
    databaseClient: db.isInitialized(),
    credentials: credentialStore.isLoaded(), // Integration services only
  };

  const allReady = Object.values(checks).every(Boolean);

  return reply
    .code(allReady ? 200 : 503)
    .send({
      status: allReady ? "ready" : "not_ready",
      checks
    });
});
```

### DigitalOcean Health Checks

```yaml
# .do/app.yaml
services:
  - name: my-service
    health_check:
      http_path: /health
      initial_delay_seconds: 10
      period_seconds: 10
      timeout_seconds: 5
      success_threshold: 1
      failure_threshold: 3
```
