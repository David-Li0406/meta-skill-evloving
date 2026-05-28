# Optima Templates

Templates for service specifications, deployment configs, and message contracts.

---

## Service Specification Template

Use this template when planning a new Optima service.

```markdown
# Service Specification: [Service Name]

**Author:** [Name]
**Date:** [YYYY-MM-DD]
**Status:** Draft | In Review | Approved | Implemented

---

## 1. Overview

### Purpose
<!-- What business problem does this service solve? -->

### Service Type
- [ ] Core Service (business logic)
- [ ] Integration Service (external API)
- [ ] Supporting Service (utilities)

### External Dependencies
<!-- List any external systems this service integrates with -->
| System | Purpose | Integration Service? |
|--------|---------|---------------------|
| | | [ ] Yes |

---

## 2. Message Bus Events

### Subscribes To (Consumes)

| Event Type | Source | Handler | Description |
|------------|--------|---------|-------------|
| `EVENT_NAME` | service-name | `handleEventName` | What it does |

### Publishes (Produces)

| Event Type | Trigger | Description |
|------------|---------|-------------|
| `EVENT_NAME` | When X happens | What it contains |

---

## 3. Database Operations

### Via DatabaseClient

| Operation | Method | Description |
|-----------|--------|-------------|
| `db.getSomething(id)` | Query | Get something by ID |
| `db.createSomething(data)` | Command | Create new record |

### New Tables Required

| Table | Purpose | Owner Service |
|-------|---------|---------------|
| `table_name` | Store X data | this-service |

### Schema Definition

```sql
CREATE TABLE table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- Use TEXT not VARCHAR
  name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'PENDING',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX idx_table_name_status ON table_name(status);
```

---

## 4. API Endpoints (if any)

### Health Checks (Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Liveness probe |
| `/health/ready` | GET | Readiness probe |

### Service-Specific Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/something` | POST | Bearer | Do something |

---

## 5. Error Handling

### Error Categories

| Category | Severity | Action |
|----------|----------|--------|
| External API failure | ERROR | Retry with backoff, publish alert |
| Validation failure | WARN | Reject message, log |
| Database timeout | ERROR | Retry, circuit break if persistent |

### Alert Conditions

| Condition | Severity | Notification |
|-----------|----------|--------------|
| Error rate > 10/min | Page | Immediate email |
| Service unreachable | Page | Immediate email |

---

## 6. Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RABBITMQ_URL` | Yes | - | Message bus connection |
| `SERVICE_PORT` | Yes | - | HTTP port |
| `NODE_ENV` | Yes | - | production/development |

### Operational Config (in database)

| Key | Type | Description |
|-----|------|-------------|
| `config_key` | string[] | What it configures |

---

## 7. Implementation Notes

### Dependencies
- `@cfgi/shared` - DatabaseClient, messaging, logger
- `@optima-financial/message-bus-contracts` - Event types

### Critical Paths
<!-- What are the most important flows? -->

### Known Limitations
<!-- Any constraints or future improvements -->
```

---

## DigitalOcean App Platform Template

### Single Service (.do/app.yaml)

```yaml
spec_version: 2
name: optima-[service-name]

services:
  - name: [service-name]
    github:
      repo: Optima-Financial/[repo-name]
      branch: main
      deploy_on_push: true
    dockerfile_path: packages/[service-name]/Dockerfile
    http_port: 300X
    instance_size_slug: basic-xxs
    instance_count: 1

    health_check:
      http_path: /health
      initial_delay_seconds: 10
      period_seconds: 10
      timeout_seconds: 5
      success_threshold: 1
      failure_threshold: 3

    envs:
      - key: NODE_ENV
        value: production
      - key: SERVICE_PORT
        value: "300X"
      - key: RABBITMQ_URL
        scope: RUN_AND_BUILD_TIME
        type: SECRET
        value: "PLACEHOLDER"
      - key: GH_PACKAGES_TOKEN
        scope: RUN_AND_BUILD_TIME
        type: SECRET
        value: "PLACEHOLDER"

# For background workers (no HTTP)
workers:
  - name: [worker-name]
    github:
      repo: Optima-Financial/[repo-name]
      branch: main
      deploy_on_push: true
    dockerfile_path: packages/[worker-name]/Dockerfile
    instance_size_slug: basic-xxs
    instance_count: 1

    envs:
      - key: NODE_ENV
        value: production
      - key: RABBITMQ_URL
        scope: RUN_AND_BUILD_TIME
        type: SECRET
        value: "PLACEHOLDER"
```

### Multi-Service Monorepo

```yaml
spec_version: 2
name: optima-core-services

services:
  - name: database-service
    github:
      repo: Optima-Financial/optima-core
      branch: main
      deploy_on_push: true
    dockerfile_path: packages/database-service/Dockerfile
    http_port: 3007
    instance_size_slug: basic-xs
    instance_count: 1
    health_check:
      http_path: /health
    envs:
      - key: NODE_ENV
        value: production
      - key: SERVICE_PORT
        value: "3007"
      - key: RABBITMQ_URL
        type: SECRET
      - key: SUPABASE_URL
        type: SECRET
      - key: SUPABASE_ANON_KEY
        type: SECRET

  - name: data-ingestion
    github:
      repo: Optima-Financial/optima-core
      branch: main
    dockerfile_path: packages/data-ingestion/Dockerfile
    http_port: 3001
    instance_size_slug: basic-xxs
    instance_count: 1
    health_check:
      http_path: /health
    envs:
      - key: SERVICE_PORT
        value: "3001"
      - key: RABBITMQ_URL
        type: SECRET

  # Add more services...
```

---

## Dockerfile Template

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# GitHub Packages auth
ARG GH_PACKAGES_TOKEN
ENV GH_PACKAGES_TOKEN=${GH_PACKAGES_TOKEN}

# Copy workspace config
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml .npmrc ./

# Copy packages
COPY packages/shared ./packages/shared
COPY packages/[service-name] ./packages/[service-name]

# Install dependencies
RUN pnpm install --frozen-lockfile

# Build shared first, then service
RUN pnpm --filter @cfgi/shared build
RUN pnpm --filter @cfgi/[service-name] build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

# Copy built artifacts
COPY --from=builder /app/packages/[service-name]/dist ./dist
COPY --from=builder /app/packages/[service-name]/package.json ./
COPY --from=builder /app/node_modules ./node_modules

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD wget --no-verbose --tries=1 --spider http://localhost:${SERVICE_PORT}/health || exit 1

EXPOSE ${SERVICE_PORT}

CMD ["node", "dist/index.js"]
```

---

## Message Contract Template

### Adding New Event Type

```typescript
// packages/contracts/src/queues/index.ts

export const EVENT_TYPES = {
  // Existing events (DO NOT MODIFY)
  DATA_INGESTED: "DATA_INGESTED",
  EVALUATION_COMPLETE: "EVALUATION_COMPLETE",
  // ...

  // NEW: Add at end
  NEW_FEATURE_STARTED: "NEW_FEATURE_STARTED",
  NEW_FEATURE_COMPLETED: "NEW_FEATURE_COMPLETED",
} as const;

export const QUEUES = {
  // Existing queues
  // ...

  // NEW: Add queue binding
  NEW_SERVICE_FEATURE_STARTED: "new-service.feature-started",
} as const;
```

### Adding New Schema

```typescript
// packages/contracts/src/events/new-feature.ts

import { z } from "zod";

/**
 * Payload for NEW_FEATURE_STARTED event
 * @version 1
 */
export const NewFeatureStartedPayloadV1 = z.object({
  // Correlation for request/response
  correlation_id: z.string().uuid(),

  // Timestamp
  timestamp: z.string().datetime(),

  // Business fields
  feature_id: z.string().uuid(),
  initiated_by: z.string(),
  parameters: z.object({
    param1: z.string(),
    param2: z.number().optional(),
  }),
});

export type NewFeatureStartedPayloadV1 = z.infer<typeof NewFeatureStartedPayloadV1>;

/**
 * Payload for NEW_FEATURE_COMPLETED event
 * @version 1
 */
export const NewFeatureCompletedPayloadV1 = z.object({
  correlation_id: z.string().uuid(),
  timestamp: z.string().datetime(),
  feature_id: z.string().uuid(),
  status: z.enum(["SUCCESS", "FAILED"]),
  result: z.unknown().optional(),
  error: z.object({
    code: z.string(),
    message: z.string(),
  }).optional(),
});

export type NewFeatureCompletedPayloadV1 = z.infer<typeof NewFeatureCompletedPayloadV1>;
```

### Exporting from Index

```typescript
// packages/contracts/src/events/index.ts

export * from "./data.js";
export * from "./trading.js";
export * from "./db.js";
// NEW: Add export
export * from "./new-feature.js";
```

---

## Database Migration Template

```sql
-- Migration: [description]
-- Date: [YYYY-MM-DD]
-- Author: [name]

-- ==============================================================================
-- UP MIGRATION
-- ==============================================================================

-- Create new table
CREATE TABLE IF NOT EXISTS new_table (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign keys
  strategy_id UUID NOT NULL REFERENCES strategies(id),
  user_id UUID REFERENCES auth.users(id),

  -- Business fields (use TEXT, never VARCHAR)
  status TEXT NOT NULL DEFAULT 'PENDING',
  amount DECIMAL(18, 8) NOT NULL,
  metadata JSONB,

  -- Timestamps
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_new_table_strategy_id
  ON new_table(strategy_id);
CREATE INDEX IF NOT EXISTS idx_new_table_status
  ON new_table(status)
  WHERE status = 'PENDING';
CREATE INDEX IF NOT EXISTS idx_new_table_created_at
  ON new_table(created_at DESC);

-- Update trigger for updated_at
CREATE TRIGGER update_new_table_updated_at
  BEFORE UPDATE ON new_table
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- RLS (if user-facing table)
ALTER TABLE new_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own records"
  ON new_table FOR SELECT
  USING (auth.uid() = user_id);

-- ==============================================================================
-- DOWN MIGRATION (for rollback)
-- ==============================================================================

-- DROP TABLE IF EXISTS new_table;
```

---

## Implementation Roadmap Template

```markdown
# Implementation Roadmap: [Feature/Service Name]

## Phase 1: Data Model (Week 1)

### Tasks
- [ ] Design database schema
- [ ] Create migration SQL
- [ ] Apply migration to dev environment
- [ ] Update CLAUDE.md with new tables
- [ ] Add to database-service handlers

### Deliverables
- [ ] Migration applied to Supabase
- [ ] DatabaseClient methods added
- [ ] Documentation updated

---

## Phase 2: Contracts (Week 1)

### Tasks
- [ ] Define new event types
- [ ] Create Zod schemas
- [ ] Add to message-bus-contracts
- [ ] Publish new version
- [ ] Update consumer repos

### Deliverables
- [ ] `@optima-financial/message-bus-contracts` v1.X.0 published
- [ ] All consuming services updated

---

## Phase 3: Service Implementation (Weeks 2-3)

### Tasks
- [ ] Create service scaffold
- [ ] Implement message handlers
- [ ] Add DatabaseClient integration
- [ ] Implement NotifyingLogger
- [ ] Add health check endpoints
- [ ] Write unit tests

### Deliverables
- [ ] Service passing all tests
- [ ] Health checks working
- [ ] Error notifications working

---

## Phase 4: Integration (Week 3)

### Tasks
- [ ] Connect to existing services
- [ ] End-to-end flow testing
- [ ] Load testing (if applicable)
- [ ] Security review

### Deliverables
- [ ] E2E tests passing
- [ ] Integration verified in staging

---

## Phase 5: Deployment (Week 4)

### Tasks
- [ ] Create Dockerfile
- [ ] Create .do/app.yaml
- [ ] Set environment variables in DO
- [ ] Deploy to staging
- [ ] Verify in staging
- [ ] Deploy to production
- [ ] Monitor for 24-48 hours

### Deliverables
- [ ] Service running in production
- [ ] Monitoring dashboards created
- [ ] Runbook documented
```
