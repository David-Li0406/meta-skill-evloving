# Optima Implementation Phases

Detailed breakdown of the seven implementation phases for building Optima services.

---

## Phase 1: Data Model

**Goal:** Design and implement the database schema before any code.

### Why Data Model First?

| Reason | Benefit |
|--------|---------|
| Schema defines domain | Clear understanding before coding |
| Migrations are sequential | Harder to fix later |
| Contracts depend on schema | Event payloads match data |
| Documentation starts here | CLAUDE.md reflects reality |

### Tasks

#### 1.1 Schema Design

```
[ ] Identify entities and relationships
[ ] Choose appropriate data types (TEXT not VARCHAR!)
[ ] Define primary and foreign keys
[ ] Plan indexes for query patterns
[ ] Consider RLS policies (if user-facing)
```

#### 1.2 Migration Creation

```sql
-- Follow this structure for every migration

-- 1. Create tables with proper types
CREATE TABLE new_entity (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign keys first
  related_id UUID NOT NULL REFERENCES other_table(id),

  -- Business fields (TEXT, DECIMAL, TIMESTAMPTZ, JSONB)
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'PENDING',
  amount DECIMAL(18, 8),
  metadata JSONB,

  -- Timestamps always
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. Create indexes
CREATE INDEX idx_new_entity_related_id ON new_entity(related_id);
CREATE INDEX idx_new_entity_status ON new_entity(status) WHERE status = 'PENDING';

-- 3. Add update trigger
CREATE TRIGGER update_new_entity_updated_at
  BEFORE UPDATE ON new_entity
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### 1.3 Apply Migration

```bash
# Via Supabase Dashboard or CLI
supabase db push

# Or direct SQL
psql $DATABASE_URL < migration.sql
```

#### 1.4 Update Documentation

```markdown
# In CLAUDE.md, add new table:

| Table | Owner Service | Purpose |
|-------|---------------|---------|
| new_entity | new-service | Store X data |
```

#### 1.5 Add DatabaseClient Methods

```typescript
// In database-service handlers

// Query handler
case "new_entity.get":
  return await supabase
    .from("new_entity")
    .select("*")
    .eq("id", params.id)
    .single();

case "new_entity.list":
  return await supabase
    .from("new_entity")
    .select("*")
    .eq("status", params.status ?? "PENDING");

// Command handler
case "new_entity.create":
  return await supabase
    .from("new_entity")
    .insert(params.data)
    .select()
    .single();
```

### Deliverables

- [ ] Migration SQL file created
- [ ] Migration applied to Supabase (dev)
- [ ] database-service handlers added
- [ ] DatabaseClient methods exposed
- [ ] CLAUDE.md updated with new tables

---

## Phase 2: Contracts

**Goal:** Define message bus contracts before implementing services.

### Why Contracts Second?

| Reason | Benefit |
|--------|---------|
| Type safety across services | Compile-time error catching |
| Documentation | Self-documenting API |
| Append-only discipline | No breaking changes |
| Shared understanding | All devs see same contract |

### Tasks

#### 2.1 Define Event Types

```typescript
// In message-bus-contracts/src/queues/index.ts

export const EVENT_TYPES = {
  // ... existing events (DO NOT MODIFY)

  // NEW: Add new event types
  NEW_FEATURE_REQUESTED: "NEW_FEATURE_REQUESTED",
  NEW_FEATURE_STARTED: "NEW_FEATURE_STARTED",
  NEW_FEATURE_COMPLETED: "NEW_FEATURE_COMPLETED",
  NEW_FEATURE_FAILED: "NEW_FEATURE_FAILED",
} as const;

export const QUEUES = {
  // ... existing queues

  // NEW: Add queue bindings
  NEW_SERVICE_FEATURE_REQUESTED: "new-service.feature-requested",
  ORCHESTRATOR_FEATURE_COMPLETED: "orchestrator.feature-completed",
} as const;
```

#### 2.2 Create Zod Schemas

```typescript
// In message-bus-contracts/src/events/new-feature.ts

import { z } from "zod";

export const NewFeatureRequestedPayloadV1 = z.object({
  correlation_id: z.string().uuid(),
  timestamp: z.string().datetime(),

  // Request fields
  entity_id: z.string().uuid(),
  action: z.enum(["CREATE", "UPDATE", "DELETE"]),
  params: z.record(z.unknown()),
});

export const NewFeatureCompletedPayloadV1 = z.object({
  correlation_id: z.string().uuid(),
  timestamp: z.string().datetime(),

  // Result fields
  entity_id: z.string().uuid(),
  status: z.enum(["SUCCESS", "FAILED"]),
  result: z.unknown().optional(),
  error: z.object({
    code: z.string(),
    message: z.string(),
  }).optional(),
});

export type NewFeatureRequestedPayloadV1 = z.infer<typeof NewFeatureRequestedPayloadV1>;
export type NewFeatureCompletedPayloadV1 = z.infer<typeof NewFeatureCompletedPayloadV1>;
```

#### 2.3 Export and Version Bump

```typescript
// In message-bus-contracts/src/events/index.ts
export * from "./new-feature.js";

// In package.json - bump version
{
  "version": "1.X.0"  // Minor bump for new event types
}
```

#### 2.4 Publish Package

```bash
cd packages/contracts
pnpm build
npm publish
```

#### 2.5 Update Consumers

```bash
# In all repos that use the contracts
pnpm update @optima-financial/message-bus-contracts
```

### Deliverables

- [ ] New EVENT_TYPES defined
- [ ] Zod schemas created
- [ ] Package version bumped
- [ ] Published to GitHub Packages
- [ ] Consumer repos updated

---

## Phase 3: Core Service

**Goal:** Implement the service following Optima patterns.

### Service Structure

```
packages/new-service/
├── src/
│   ├── index.ts           # Entry point
│   ├── handlers/
│   │   ├── index.ts       # Handler exports
│   │   └── feature.ts     # Feature handler
│   ├── services/
│   │   └── feature.ts     # Business logic
│   └── types/
│       └── index.ts       # Local types
├── Dockerfile
├── package.json
└── tsconfig.json
```

### Tasks

#### 3.1 Service Scaffold

```typescript
// src/index.ts

import Fastify from "fastify";
import { getMessageBus } from "@cfgi/shared/messaging";
import { getDatabaseClient } from "@cfgi/shared/db-client";
import { wrapWithNotifications, registerGlobalErrorHandlers } from "@cfgi/shared/logger";
import { EVENT_TYPES } from "@optima-financial/message-bus-contracts/queues";
import { handleFeatureRequested } from "./handlers/feature.js";

const app = Fastify({ logger: true });

async function start() {
  // 1. Message bus
  const messageBus = getMessageBus({
    serviceName: "new-service",
    url: process.env.RABBITMQ_URL!,
  });
  await messageBus.connect();

  // 2. NotifyingLogger
  const environment = process.env.NODE_ENV === "production" ? "production" : "development";
  const logger = wrapWithNotifications(app.log, {
    serviceName: "new-service",
    messageBus,
    environment,
  });

  // 3. Global error handlers
  registerGlobalErrorHandlers({
    logger,
    serviceName: "new-service",
    onFatalError: async () => {
      await messageBus.close();
      await app.close();
    },
  });

  // 4. DatabaseClient
  const db = getDatabaseClient({ serviceName: "new-service" });
  await db.initialize();

  // 5. Health checks
  app.get("/health", async () => ({ status: "ok" }));
  app.get("/health/ready", async () => ({
    status: "ready",
    checks: {
      messageBus: messageBus.isConnected(),
      databaseClient: db.isInitialized(),
    },
  }));

  // 6. Subscribe to events
  await messageBus.subscribe(
    EVENT_TYPES.NEW_FEATURE_REQUESTED,
    (event) => handleFeatureRequested(event, { db, logger, messageBus })
  );

  // 7. Start server
  const port = parseInt(process.env.SERVICE_PORT || "3010");
  await app.listen({ port, host: "0.0.0.0" });
  logger.info({ port }, "Service started");
}

start().catch((err) => {
  console.error("Failed to start:", err);
  process.exit(1);
});
```

#### 3.2 Message Handlers

```typescript
// src/handlers/feature.ts

import { EVENT_TYPES } from "@optima-financial/message-bus-contracts/queues";
import { NewFeatureRequestedPayloadV1 } from "@optima-financial/message-bus-contracts/events";
import type { DatabaseClient } from "@cfgi/shared/db-client";
import type { MessageBus } from "@cfgi/shared/messaging";
import type { Logger } from "pino";

interface HandlerContext {
  db: DatabaseClient;
  logger: Logger;
  messageBus: MessageBus;
}

export async function handleFeatureRequested(
  event: NewFeatureRequestedPayloadV1,
  ctx: HandlerContext
): Promise<void> {
  const { db, logger, messageBus } = ctx;

  logger.info({ correlation_id: event.correlation_id }, "Processing feature request");

  try {
    // 1. Validate payload
    const validated = NewFeatureRequestedPayloadV1.parse(event);

    // 2. Perform business logic
    const result = await processFeature(validated, db);

    // 3. Publish success
    await messageBus.publish(EVENT_TYPES.NEW_FEATURE_COMPLETED, {
      correlation_id: event.correlation_id,
      timestamp: new Date().toISOString(),
      entity_id: validated.entity_id,
      status: "SUCCESS",
      result,
    });

  } catch (error) {
    logger.error({ err: error, correlation_id: event.correlation_id }, "Feature request failed");

    // Publish failure
    await messageBus.publish(EVENT_TYPES.NEW_FEATURE_COMPLETED, {
      correlation_id: event.correlation_id,
      timestamp: new Date().toISOString(),
      entity_id: event.entity_id,
      status: "FAILED",
      error: {
        code: "PROCESSING_ERROR",
        message: error instanceof Error ? error.message : "Unknown error",
      },
    });
  }
}
```

#### 3.3 Unit Tests

```typescript
// src/handlers/feature.test.ts

import { describe, it, expect, vi } from "vitest";
import { handleFeatureRequested } from "./feature.js";

describe("handleFeatureRequested", () => {
  it("processes valid request and publishes success", async () => {
    const mockDb = {
      getSomething: vi.fn().mockResolvedValue({ id: "123" }),
    };
    const mockMessageBus = {
      publish: vi.fn(),
    };
    const mockLogger = {
      info: vi.fn(),
      error: vi.fn(),
    };

    const event = {
      correlation_id: "test-123",
      timestamp: new Date().toISOString(),
      entity_id: "entity-456",
      action: "CREATE" as const,
      params: {},
    };

    await handleFeatureRequested(event, {
      db: mockDb as any,
      logger: mockLogger as any,
      messageBus: mockMessageBus as any,
    });

    expect(mockMessageBus.publish).toHaveBeenCalledWith(
      "NEW_FEATURE_COMPLETED",
      expect.objectContaining({
        correlation_id: "test-123",
        status: "SUCCESS",
      })
    );
  });
});
```

### Deliverables

- [ ] Service scaffold created
- [ ] Message handlers implemented
- [ ] NotifyingLogger integrated
- [ ] DatabaseClient connected
- [ ] Health check endpoints working
- [ ] Unit tests passing

---

## Phase 4: Integration

**Goal:** Connect to existing services and validate end-to-end flows.

### Tasks

#### 4.1 Wire Up Existing Services

```typescript
// Update existing service to publish events that new service consumes

// In orchestrator or trigger service:
await messageBus.publish(EVENT_TYPES.NEW_FEATURE_REQUESTED, {
  correlation_id: uuid(),
  timestamp: new Date().toISOString(),
  entity_id: entityId,
  action: "CREATE",
  params: { ... },
});

// Listen for completion
messageBus.subscribe(EVENT_TYPES.NEW_FEATURE_COMPLETED, async (event) => {
  if (event.status === "SUCCESS") {
    // Continue workflow
  } else {
    // Handle failure
  }
});
```

#### 4.2 End-to-End Testing

```typescript
// Integration test
describe("New Feature E2E", () => {
  it("completes full workflow", async () => {
    // 1. Trigger the feature
    const correlationId = uuid();
    await messageBus.publish(EVENT_TYPES.NEW_FEATURE_REQUESTED, {
      correlation_id: correlationId,
      // ...
    });

    // 2. Wait for completion
    const completion = await waitForEvent(
      EVENT_TYPES.NEW_FEATURE_COMPLETED,
      (e) => e.correlation_id === correlationId,
      { timeout: 30000 }
    );

    // 3. Verify
    expect(completion.status).toBe("SUCCESS");

    // 4. Check database state
    const record = await db.getSomething(completion.entity_id);
    expect(record.status).toBe("COMPLETED");
  });
});
```

#### 4.3 Error Notification Testing

```typescript
// Verify errors are published to notification service
it("publishes error alert on failure", async () => {
  // Trigger failure scenario
  // ...

  // Verify NOTIFICATION_ERROR_ALERT was published
  const alert = await waitForEvent(
    EVENT_TYPES.NOTIFICATION_ERROR_ALERT,
    (e) => e.service === "new-service"
  );

  expect(alert.severity).toBe("ERROR");
});
```

### Deliverables

- [ ] Connected to upstream services
- [ ] Connected to downstream services
- [ ] E2E tests passing
- [ ] Error notifications verified
- [ ] Staging environment tested

---

## Phase 5: Deployment

**Goal:** Deploy to DigitalOcean and monitor.

### Tasks

#### 5.1 Create Dockerfile

```dockerfile
# packages/new-service/Dockerfile

FROM node:20-alpine AS builder
WORKDIR /app
RUN npm install -g pnpm

ARG GH_PACKAGES_TOKEN
ENV GH_PACKAGES_TOKEN=${GH_PACKAGES_TOKEN}

COPY package.json pnpm-workspace.yaml pnpm-lock.yaml .npmrc ./
COPY packages/shared ./packages/shared
COPY packages/new-service ./packages/new-service

RUN pnpm install --frozen-lockfile
RUN pnpm --filter @cfgi/shared build
RUN pnpm --filter @cfgi/new-service build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/packages/new-service/dist ./dist
COPY --from=builder /app/packages/new-service/package.json ./
COPY --from=builder /app/node_modules ./node_modules

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD wget --spider http://localhost:${SERVICE_PORT}/health || exit 1

EXPOSE ${SERVICE_PORT}
CMD ["node", "dist/index.js"]
```

#### 5.2 Create DO App Spec

```yaml
# .do/app.yaml

spec_version: 2
name: optima-new-service

services:
  - name: new-service
    github:
      repo: Optima-Financial/optima-core
      branch: main
      deploy_on_push: true
    dockerfile_path: packages/new-service/Dockerfile
    http_port: 3010
    instance_size_slug: basic-xxs
    instance_count: 1

    health_check:
      http_path: /health
      initial_delay_seconds: 15
      period_seconds: 10

    envs:
      - key: NODE_ENV
        value: production
      - key: SERVICE_PORT
        value: "3010"
      - key: RABBITMQ_URL
        scope: RUN_AND_BUILD_TIME
        type: SECRET
        value: "PLACEHOLDER"
      - key: GH_PACKAGES_TOKEN
        scope: RUN_AND_BUILD_TIME
        type: SECRET
        value: "PLACEHOLDER"
```

#### 5.3 Configure Secrets

```bash
# In DigitalOcean App Platform dashboard:
# Settings → Environment Variables

RABBITMQ_URL=amqps://user:pass@rabbitmq-host:5671
GH_PACKAGES_TOKEN=ghp_xxxxxxxxxxxx
```

#### 5.4 Deploy

```bash
# Option 1: Via dashboard
# Push to main branch, auto-deploys

# Option 2: Via CLI
doctl apps create --spec .do/app.yaml
```

#### 5.5 Monitor

```
[ ] Check service health in DO dashboard
[ ] Verify logs show successful startup
[ ] Verify message bus connected
[ ] Trigger test event and verify processing
[ ] Monitor for 24-48 hours
[ ] Set up alerts for error rate
```

### Deliverables

- [ ] Dockerfile created and tested
- [ ] DO app spec created
- [ ] Environment variables configured
- [ ] Deployed to staging
- [ ] Deployed to production
- [ ] Monitoring verified

---

## Phase 6: Documentation

**Goal:** Update all documentation to reflect the new service/feature.

### Why Documentation Matters

| Reason | Benefit |
|--------|---------|
| CLAUDE.md is source of truth | AI assistants understand the codebase |
| Onboarding | New developers can ramp up quickly |
| Operational | Runbooks prevent 3am panic |
| Maintenance | Future you will thank present you |

### Tasks

#### 6.1 Update CLAUDE.md

```markdown
# Add to Key Database Tables section:

| Table | Owner Service | Purpose |
|-------|---------------|---------|
| new_entity | new-service | Store X data |

# Add to Services section:

| Service | Port | Status | Responsibility |
|---------|------|--------|----------------|
| new-service | 3010 | ✅ Deployed | Handle new feature |

# Add to Build Commands if needed:

pnpm dev:new-service      # Port 3010

# Add to Environment Variables section:

| Variable | Required | Description |
|----------|----------|-------------|
| NEW_SERVICE_CONFIG | Yes | Configuration for new service |
```

#### 6.2 Update README.md

```markdown
# Add to Services section:

## new-service

Handles new feature functionality.

### Quick Start

\`\`\`bash
pnpm dev:new-service
\`\`\`

### Environment Variables

| Variable | Description |
|----------|-------------|
| SERVICE_PORT | HTTP port (default: 3010) |
```

#### 6.3 Create Service Documentation

Create `docs/new-service.md`:

```markdown
# New Service

## Overview

Brief description of what the service does.

## Events

### Subscribes To

| Event | Handler | Description |
|-------|---------|-------------|
| NEW_FEATURE_REQUESTED | handleFeatureRequested | Process feature requests |

### Publishes

| Event | Trigger | Description |
|-------|---------|-------------|
| NEW_FEATURE_COMPLETED | After processing | Result of feature request |

## Database Operations

| Operation | Description |
|-----------|-------------|
| db.newEntity.get | Get entity by ID |
| db.newEntity.create | Create new entity |

## Configuration

| Key | Type | Description |
|-----|------|-------------|
| config_key | string | What it configures |

## Error Handling

| Error | Severity | Action |
|-------|----------|--------|
| ValidationError | WARN | Reject with error message |
| DatabaseError | ERROR | Retry, then alert |
```

#### 6.4 Document API Endpoints

```markdown
# Add to docs/service-api-endpoints.md:

## new-service (Port 3010)

### Health Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /health | GET | Liveness probe |
| /health/ready | GET | Readiness probe |

### Feature Endpoints (if any)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| /api/v1/feature | POST | Bearer | Trigger feature |
```

#### 6.5 Create Operational Runbook

Create `docs/runbooks/new-service.md`:

```markdown
# New Service Runbook

## Service Information

| Item | Value |
|------|-------|
| Service Name | new-service |
| Port | 3010 |
| Repository | optima-core |
| Dashboard | [DO Dashboard](link) |
| Logs | [DO Logs](link) |

## Health Checks

| Check | Expected | Action if Failed |
|-------|----------|------------------|
| /health | 200 OK | Restart service |
| /health/ready | 200 OK | Check dependencies |

## Common Issues

### Issue: High Latency

**Symptoms:**
- Response time > 1s
- Queue backup

**Diagnosis:**
1. Check database-service health
2. Check RabbitMQ queue depth
3. Check CPU/memory usage

**Resolution:**
1. Scale horizontally if CPU-bound
2. Check for slow database queries
3. Verify message bus connection

### Issue: Service Not Starting

**Symptoms:**
- Container restarts
- Health check failing

**Diagnosis:**
1. Check logs for startup errors
2. Verify environment variables
3. Check RabbitMQ connectivity

**Resolution:**
1. Fix configuration issues
2. Redeploy if code issue
3. Contact platform team if infra issue

## Operational Controls

| Control | How to Activate |
|---------|-----------------|
| Feature flag | Set `feature.enabled` in operational_config |
| Rate limit | Update `feature.rate_limit` in operational_config |

## Escalation

| Level | Contact | When |
|-------|---------|------|
| L1 | On-call | Initial response |
| L2 | Service owner | 30min unresolved |
| L3 | Platform team | Infrastructure issue |
```

### Deliverables

- [ ] CLAUDE.md updated with new tables and services
- [ ] README.md updated with service info
- [ ] Service documentation created
- [ ] API endpoints documented
- [ ] Operational runbook created
- [ ] All documentation reviewed for accuracy

---

## Phase 7: Testing

**Goal:** Comprehensive testing at all levels to ensure reliability.

### Testing Pyramid

```
                    ┌───────────┐
                    │   E2E     │  ◄── Full workflow tests
                    │   Tests   │      (fewer, slower)
                    ├───────────┤
                    │Integration│  ◄── Service + dependencies
                    │   Tests   │      (moderate number)
                    ├───────────┤
                    │   Unit    │  ◄── Business logic
                    │   Tests   │      (many, fast)
                    └───────────┘
```

### Tasks

#### 7.1 Unit Tests

Test business logic in isolation with mocked dependencies.

**Location:** Co-located with source files (`*.test.ts`)

```typescript
// src/services/feature.test.ts

import { describe, it, expect, vi, beforeEach } from "vitest";
import { processFeature } from "./feature.js";

describe("processFeature", () => {
  const mockDb = {
    getEntity: vi.fn(),
    createEntity: vi.fn(),
    updateEntity: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("CREATE action", () => {
    it("creates new entity with correct data", async () => {
      mockDb.createEntity.mockResolvedValue({ id: "new-123", status: "CREATED" });

      const result = await processFeature({
        action: "CREATE",
        params: { name: "Test Entity" },
      }, mockDb);

      expect(mockDb.createEntity).toHaveBeenCalledWith({
        name: "Test Entity",
        status: "PENDING",
      });
      expect(result.id).toBe("new-123");
    });

    it("throws validation error for invalid params", async () => {
      await expect(processFeature({
        action: "CREATE",
        params: {}, // Missing required name
      }, mockDb)).rejects.toThrow("name is required");
    });
  });

  describe("UPDATE action", () => {
    it("updates existing entity", async () => {
      mockDb.getEntity.mockResolvedValue({ id: "123", status: "PENDING" });
      mockDb.updateEntity.mockResolvedValue({ id: "123", status: "UPDATED" });

      const result = await processFeature({
        action: "UPDATE",
        entity_id: "123",
        params: { status: "COMPLETED" },
      }, mockDb);

      expect(result.status).toBe("UPDATED");
    });

    it("throws error if entity not found", async () => {
      mockDb.getEntity.mockResolvedValue(null);

      await expect(processFeature({
        action: "UPDATE",
        entity_id: "nonexistent",
        params: {},
      }, mockDb)).rejects.toThrow("Entity not found");
    });
  });
});
```

**Handler tests:**

```typescript
// src/handlers/feature.test.ts

import { describe, it, expect, vi } from "vitest";
import { handleFeatureRequested } from "./feature.js";

describe("handleFeatureRequested", () => {
  const createMocks = () => ({
    db: {
      getEntity: vi.fn(),
      createEntity: vi.fn(),
    },
    logger: {
      info: vi.fn(),
      error: vi.fn(),
      warn: vi.fn(),
    },
    messageBus: {
      publish: vi.fn(),
    },
  });

  it("publishes success event on successful processing", async () => {
    const mocks = createMocks();
    mocks.db.createEntity.mockResolvedValue({ id: "123" });

    await handleFeatureRequested({
      correlation_id: "corr-123",
      timestamp: new Date().toISOString(),
      entity_id: "entity-456",
      action: "CREATE",
      params: { name: "Test" },
    }, mocks);

    expect(mocks.messageBus.publish).toHaveBeenCalledWith(
      "NEW_FEATURE_COMPLETED",
      expect.objectContaining({
        correlation_id: "corr-123",
        status: "SUCCESS",
      })
    );
  });

  it("publishes failure event and logs error on exception", async () => {
    const mocks = createMocks();
    mocks.db.createEntity.mockRejectedValue(new Error("DB connection failed"));

    await handleFeatureRequested({
      correlation_id: "corr-123",
      timestamp: new Date().toISOString(),
      entity_id: "entity-456",
      action: "CREATE",
      params: { name: "Test" },
    }, mocks);

    expect(mocks.logger.error).toHaveBeenCalled();
    expect(mocks.messageBus.publish).toHaveBeenCalledWith(
      "NEW_FEATURE_COMPLETED",
      expect.objectContaining({
        correlation_id: "corr-123",
        status: "FAILED",
        error: expect.objectContaining({
          message: "DB connection failed",
        }),
      })
    );
  });
});
```

#### 7.2 Integration Tests

Test service with real message bus and database connections.

```typescript
// tests/integration/feature.integration.test.ts

import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { getMessageBus } from "@cfgi/shared/messaging";
import { getDatabaseClient } from "@cfgi/shared/db-client";
import { EVENT_TYPES } from "@optima-financial/message-bus-contracts/queues";
import { v4 as uuid } from "uuid";

describe("Feature Integration", () => {
  let messageBus: MessageBus;
  let db: DatabaseClient;

  beforeAll(async () => {
    messageBus = getMessageBus({
      serviceName: "test-runner",
      url: process.env.RABBITMQ_URL!,
    });
    await messageBus.connect();

    db = getDatabaseClient({ serviceName: "test-runner" });
    await db.initialize();
  });

  afterAll(async () => {
    await messageBus.close();
  });

  it("processes feature request through message bus", async () => {
    const correlationId = uuid();

    // Set up listener for completion
    const completionPromise = new Promise((resolve) => {
      messageBus.subscribe(EVENT_TYPES.NEW_FEATURE_COMPLETED, (event) => {
        if (event.correlation_id === correlationId) {
          resolve(event);
        }
      });
    });

    // Publish request
    await messageBus.publish(EVENT_TYPES.NEW_FEATURE_REQUESTED, {
      correlation_id: correlationId,
      timestamp: new Date().toISOString(),
      entity_id: uuid(),
      action: "CREATE",
      params: { name: "Integration Test Entity" },
    });

    // Wait for completion (with timeout)
    const completion = await Promise.race([
      completionPromise,
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Timeout")), 10000)
      ),
    ]);

    expect(completion.status).toBe("SUCCESS");
  });

  it("stores data correctly in database", async () => {
    // Create via service
    const correlationId = uuid();
    // ... publish and wait for completion ...

    // Verify in database
    const entity = await db.getNewEntity(completion.result.id);
    expect(entity).toBeDefined();
    expect(entity.status).toBe("COMPLETED");
  });
});
```

#### 7.3 E2E / Workflow Tests

Test complete business workflows across multiple services.

```typescript
// tests/e2e/complete-workflow.e2e.test.ts

import { describe, it, expect } from "vitest";

describe("Complete Feature Workflow E2E", () => {
  it("executes full workflow from trigger to completion", async () => {
    // 1. Setup: Create prerequisites
    const prerequisiteData = await setupPrerequisites();

    // 2. Trigger: Start the workflow
    const workflowId = await triggerWorkflow({
      type: "NEW_FEATURE",
      data: prerequisiteData,
    });

    // 3. Wait: Allow workflow to complete
    const result = await waitForWorkflowCompletion(workflowId, {
      timeout: 30000,
      pollInterval: 1000,
    });

    // 4. Verify: Check all expected outcomes
    expect(result.status).toBe("COMPLETED");

    // Verify database state
    const dbState = await verifyDatabaseState(workflowId);
    expect(dbState.entity.status).toBe("PROCESSED");
    expect(dbState.ledgerEntries).toHaveLength(2);

    // Verify events were published
    const events = await getPublishedEvents(workflowId);
    expect(events).toContainEqual(
      expect.objectContaining({ type: "NEW_FEATURE_COMPLETED" })
    );
  });

  it("handles failure and publishes error notification", async () => {
    // Trigger with invalid data to cause failure
    const workflowId = await triggerWorkflow({
      type: "NEW_FEATURE",
      data: { invalid: true },
    });

    const result = await waitForWorkflowCompletion(workflowId);

    expect(result.status).toBe("FAILED");

    // Verify error notification was published
    const alerts = await getErrorAlerts({ service: "new-service" });
    expect(alerts).toContainEqual(
      expect.objectContaining({
        service: "new-service",
        severity: "ERROR",
      })
    );
  });
});
```

#### 7.4 Operational Tests

Test that observability and control mechanisms work.

```typescript
// tests/operational/health-and-observability.test.ts

import { describe, it, expect } from "vitest";
import fetch from "node-fetch";

const SERVICE_URL = process.env.SERVICE_URL || "http://localhost:3010";

describe("Operational Tests", () => {
  describe("Health Checks", () => {
    it("returns healthy status from /health", async () => {
      const response = await fetch(`${SERVICE_URL}/health`);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.status).toBe("ok");
    });

    it("returns ready status with dependency checks", async () => {
      const response = await fetch(`${SERVICE_URL}/health/ready`);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.status).toBe("ready");
      expect(data.checks.messageBus).toBe(true);
      expect(data.checks.databaseClient).toBe(true);
    });
  });

  describe("Feature Flags", () => {
    it("respects feature flag when disabled", async () => {
      // Disable feature
      await db.setConfigValue("new_feature.enabled", false);

      // Trigger feature
      const result = await triggerFeature();

      // Should be rejected
      expect(result.status).toBe("REJECTED");
      expect(result.reason).toBe("Feature disabled");

      // Re-enable
      await db.setConfigValue("new_feature.enabled", true);
    });
  });

  describe("Error Notifications", () => {
    it("publishes error alert on service error", async () => {
      // Subscribe to error alerts
      const alertPromise = waitForEvent(
        EVENT_TYPES.NOTIFICATION_ERROR_ALERT,
        (e) => e.service === "new-service"
      );

      // Trigger an error
      await triggerFeature({ causeError: true });

      // Verify alert was published
      const alert = await alertPromise;
      expect(alert.service).toBe("new-service");
      expect(alert.severity).toBe("ERROR");
    });
  });
});
```

#### 7.5 Manual Testing Scenarios

Document manual test cases for QA verification.

```markdown
# Manual Testing Scenarios

## Scenario 1: Happy Path

**Preconditions:**
- Service is deployed and running
- Database has required seed data

**Steps:**
1. Trigger feature request via API/event
2. Wait for processing (max 30s)
3. Verify completion event received

**Expected Results:**
- [ ] Feature completed successfully
- [ ] Database updated correctly
- [ ] No errors in logs

---

## Scenario 2: Error Handling

**Steps:**
1. Trigger feature with invalid data
2. Observe error handling

**Expected Results:**
- [ ] Failure event published
- [ ] Error logged with context
- [ ] Error notification sent
- [ ] Service remains healthy

---

## Scenario 3: Service Restart Recovery

**Steps:**
1. Trigger feature request
2. Restart service mid-processing
3. Observe recovery behavior

**Expected Results:**
- [ ] Service restarts cleanly
- [ ] Unacked messages reprocessed
- [ ] No data loss or corruption
```

### Running Tests

```bash
# All tests
pnpm test

# Unit tests only
pnpm test:unit

# Integration tests (requires running services)
pnpm test:integration

# E2E tests (requires full environment)
pnpm test:e2e

# Single test file
npx vitest run src/handlers/feature.test.ts

# Watch mode
npx vitest watch
```

### Deliverables

- [ ] Unit tests for all business logic
- [ ] Unit tests for all message handlers
- [ ] Integration tests for service + message bus
- [ ] Integration tests for service + database
- [ ] E2E tests for complete workflows
- [ ] Operational tests for health checks
- [ ] Operational tests for feature flags
- [ ] Manual testing scenarios documented
- [ ] All tests passing in CI
- [ ] Test coverage meets threshold (e.g., 80%)
