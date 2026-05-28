# Architectural Anti-Patterns & Solutions

Common architectural mistakes and how to address them.

---

## Coupling Anti-Patterns

### Distributed Monolith

**Problem:** Microservices that must deploy together, share databases, or have synchronous call chains.

```
┌─────────┐     sync      ┌─────────┐     sync      ┌─────────┐
│Service A│──────────────►│Service B│──────────────►│Service C│
└─────────┘               └─────────┘               └─────────┘
     │                         │                         │
     └─────────────────────────┴─────────────────────────┘
                               │
                        ┌──────▼──────┐
                        │ Shared DB   │  ← All services write here
                        └─────────────┘
```

**Solution:** Event-driven architecture with clear ownership.

```
┌─────────┐   event    ┌─────────┐   event    ┌─────────┐
│Service A│───────────►│  Queue  │───────────►│Service B│
└────┬────┘            └─────────┘            └────┬────┘
     │                                              │
┌────▼────┐                                   ┌────▼────┐
│  DB A   │ ← Owns its data                   │  DB B   │
└─────────┘                                   └─────────┘
```

### Hidden Temporal Coupling

**Problem:** Services assume timing or ordering without explicit contracts.

```typescript
// Service A - assumes Service B processes immediately
async function createOrder(order) {
  await db.insert(order);
  await eventBus.publish('order.created', order);
  // Immediately queries Service B for enriched data
  const enriched = await serviceB.getOrderDetails(order.id);  // Race condition!
}
```

**Solution:** Make dependencies explicit, use correlation IDs.

```typescript
async function createOrder(order) {
  const correlationId = uuid();
  await db.insert({ ...order, correlationId, status: 'pending' });
  await eventBus.publish('order.created', { ...order, correlationId });
  // Don't assume immediate availability - let consumer notify when ready
}

// Service B publishes 'order.enriched' event when done
// Service A listens and updates status
```

### Shared Database Anti-Pattern

**Problem:** Multiple services reading/writing same tables.

```
Service A ────┐
              │
Service B ────┼────► Shared Database
              │        └── users table (all services write!)
Service C ────┘        └── orders table (all services write!)
```

**Risks:**
- Schema changes break multiple services
- No clear ownership of data
- Coupling makes independent deployment impossible

**Solution:** Database per service with APIs or events for data access.

```
Service A ────► DB A (owns users)
    │
    │ API call or event
    ▼
Service B ────► DB B (owns orders, caches user info)
```

---

## Data Anti-Patterns

### Distributed Data Duplication

**Problem:** Same data copied everywhere, no clear source of truth.

```
User Service: { id: 1, name: "Alice", email: "a@x.com" }
Order Service: { userId: 1, userName: "Alice", userEmail: "a@x.com" }  // Stale!
Notification Service: { userId: 1, email: "alice@old.com" }  // Even more stale!
```

**Solution:** Single source of truth with explicit sync mechanism.

```
User Service: owns { id, name, email }  ← Source of truth
    │
    ├─► publishes user.updated events
    │
Order Service: stores { userId } only, fetches user details when needed
    │           OR caches with TTL + invalidation on user.updated
    │
Notification Service: subscribes to user.updated, keeps minimal cache
```

### Schema Drift

**Problem:** Same entity has different schemas in different places.

```typescript
// Service A
interface User {
  id: string;
  fullName: string;  // Combined name
  createdAt: Date;
}

// Service B
interface User {
  id: number;        // Different type!
  firstName: string; // Split name
  lastName: string;
  created_at: string; // Different format!
}
```

**Solution:** Shared schema definitions, schema registry.

```typescript
// Shared package: @company/schemas
export interface UserV1 {
  id: string;
  firstName: string;
  lastName: string;
  createdAt: string; // ISO 8601
}

// Both services import from shared package
import { UserV1 } from '@company/schemas';
```

---

## API Anti-Patterns

### Breaking Changes Without Versioning

**Problem:** API changes that break existing clients.

```typescript
// Version 1 (deployed)
interface OrderResponse {
  id: string;
  total: number;  // Renamed to 'amount' in v2
}

// Version 2 (breaks all clients!)
interface OrderResponse {
  id: string;
  amount: number;  // Clients expecting 'total' fail
}
```

**Solution:** Additive changes, deprecation strategy.

```typescript
// Version 2 (backward compatible)
interface OrderResponse {
  id: string;
  total: number;    // Keep for backward compatibility
  amount: number;   // New field (same value)
  /** @deprecated Use 'amount' instead. Will be removed in v3. */
}

// Or use explicit versioning
// GET /v1/orders/:id → returns { total }
// GET /v2/orders/:id → returns { amount }
```

### N+1 API Calls

**Problem:** Client makes many calls to get related data.

```typescript
// Frontend makes N+1 calls
const orders = await fetch('/api/orders');  // 1 call
for (const order of orders) {
  order.user = await fetch(`/api/users/${order.userId}`);  // N calls!
}
```

**Solution:** Batch endpoints, GraphQL, or include related data.

```typescript
// Option 1: Batch endpoint
const users = await fetch('/api/users?ids=1,2,3');

// Option 2: Include in response
const orders = await fetch('/api/orders?include=user');
// Returns: [{ id: 1, user: { name: 'Alice' } }]

// Option 3: GraphQL
const { orders } = await graphql(`
  query { orders { id user { name } } }
`);
```

---

## Operational Anti-Patterns

### Big Bang Deployment

**Problem:** Large changes deployed all at once.

```
Monday:    Feature complete
Tuesday:   Ship everything to production
Wednesday: Fire drills, rollback attempts
Thursday:  Still fixing production
Friday:    Post-mortem
```

**Solution:** Incremental rollout with feature flags.

```
Week 1: Deploy code behind feature flag (flag off)
Week 2: Enable for internal users (1%)
Week 3: Enable for beta users (10%)
Week 4: Enable for all users (100%)
Week 5: Remove feature flag and old code
```

### Irreversible Migration

**Problem:** Database migration that can't be rolled back.

```sql
-- Migration: Rename column (IRREVERSIBLE!)
ALTER TABLE users RENAME COLUMN full_name TO name;

-- If rollback needed, code expects 'full_name' but column is 'name'
-- App crashes!
```

**Solution:** Multi-phase migration.

```sql
-- Phase 1: Add new column (backward compatible)
ALTER TABLE users ADD COLUMN name VARCHAR(255);
UPDATE users SET name = full_name;

-- Phase 2: Deploy code that reads from both, writes to both
-- Code: user.name ?? user.full_name

-- Phase 3: After all old code is gone, drop old column
ALTER TABLE users DROP COLUMN full_name;
```

### Missing Circuit Breakers

**Problem:** Cascade failures when dependency is slow/down.

```
User Request
    │
    ▼
┌─────────┐      ┌─────────┐
│Service A│─────►│Service B│ ← Slow/Down
└─────────┘      └─────────┘
    │
    ▼
Service A threads exhausted waiting for B
    │
    ▼
Service A becomes unresponsive
    │
    ▼
Upstream services fail
    │
    ▼
Entire system down!
```

**Solution:** Circuit breaker with fallback.

```typescript
const breaker = new CircuitBreaker(serviceB.getData, {
  timeout: 3000,
  errorThreshold: 50,
  resetTimeout: 30000,
});

async function getData(id: string) {
  try {
    return await breaker.fire(id);
  } catch (error) {
    if (error.name === 'CircuitBreakerOpen') {
      // Fallback: return cached data, default, or graceful error
      return getCachedData(id) ?? DEFAULT_DATA;
    }
    throw error;
  }
}
```

---

## Event-Driven Anti-Patterns

### Event Schema Breaking Changes

**Problem:** Adding required fields to events breaks consumers.

```typescript
// Producer publishes new required field
interface OrderCreatedV2 {
  orderId: string;
  customerId: string;
  priority: 'high' | 'low';  // New required field!
}

// Old consumer crashes
function handleOrder(event: OrderCreated) {
  if (event.priority === undefined) {
    // TypeError or unexpected behavior
  }
}
```

**Solution:** Make new fields optional with defaults.

```typescript
interface OrderCreatedV2 {
  orderId: string;
  customerId: string;
  priority?: 'high' | 'low';  // Optional!
}

// Consumer handles missing field
function handleOrder(event: OrderCreated) {
  const priority = event.priority ?? 'low';  // Default value
}
```

### Event Ordering Assumptions

**Problem:** Consumer assumes events arrive in order.

```
Producer sends: OrderCreated → OrderUpdated → OrderShipped

Consumer receives: OrderCreated → OrderShipped → OrderUpdated
                   (Out of order due to parallel processing!)

Result: Order shows "Updated" status instead of "Shipped"
```

**Solution:** Idempotent processing with version/timestamp.

```typescript
interface OrderEvent {
  orderId: string;
  version: number;  // Monotonic version
  timestamp: string;
}

async function handleEvent(event: OrderEvent) {
  const current = await db.orders.findOne({ id: event.orderId });

  // Only process if newer
  if (current && current.version >= event.version) {
    return; // Skip stale event
  }

  await db.orders.update({
    id: event.orderId,
    version: event.version,
    // ... other fields
  });
}
```

---

## Quick Reference: Pattern Detection

| Pattern | Detection Signal | Risk |
|---------|------------------|------|
| Distributed Monolith | Services share DB, deploy together | HIGH |
| Hidden Coupling | Service A queries B after publishing event | MEDIUM |
| Schema Drift | Same entity, different types across services | HIGH |
| N+1 Calls | Loop with API call inside | MEDIUM |
| Breaking API Change | Required field removed/renamed | CRITICAL |
| Irreversible Migration | DROP COLUMN without multi-phase | HIGH |
| Missing Circuit Breaker | Sync call without timeout/fallback | MEDIUM |
| Event Ordering Assumption | Consumer logic depends on order | HIGH |
| Shared Mutable State | Multiple services write same cache key | CRITICAL |
