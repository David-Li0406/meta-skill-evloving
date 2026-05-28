---
name: wide-event-logging
description:
  Implements high-cardinality, structured logging using the "Wide Events" or
  "Canonical Log Line" pattern. Use when asked to (1) set up or improve
  application observability and logging, (2) implement structured logging in
  backend services, (3) add frontend analytics or telemetry, (4) debug
  production issues via better logging, (5) reduce log volume while improving
  debuggability, or (6) implement OpenTelemetry with business context.
---

# Wide Event Logging

Implement the "Wide Event" or "Canonical Log Line" pattern: emit ONE
context-rich JSON event per request instead of scattered log statements.

## Mental Model Shift

> Log what happened to this request, not what your code is doing.

Traditional logging produces 10-20 lines per request that are impossible to
correlate. Wide events produce ONE line with 30-50+ fields containing everything
needed to debug.

## Core Principles

1. **One Request, One Event**: Emit a single wide event at request end
2. **High Cardinality**: Include user_id, request_id, session_id, trace_id
3. **High Dimensionality**: Include 30-50+ fields covering all context
4. **Business Context**: Add subscription tier, cart value, feature flags
5. **Structured JSON**: Enable SQL-like queries, not grep

## Field Categories

Every wide event SHOULD include fields from these categories:

### Request Context (Required)

```json
{
  "request_id": "req_8bf7ec2d",
  "trace_id": "abc123def456",
  "timestamp": "2025-01-15T10:23:45.612Z",
  "method": "POST",
  "path": "/api/checkout",
  "status_code": 200,
  "duration_ms": 1247
}
```

### User Context (Required for authenticated requests)

```json
{
  "user_id": "user_456",
  "session_id": "sess_abc123",
  "subscription_tier": "premium",
  "account_age_days": 847,
  "lifetime_value_cents": 284700
}
```

### Business Context (Domain-specific)

```json
{
  "cart_id": "cart_xyz",
  "cart_item_count": 3,
  "cart_total_cents": 15999,
  "coupon_applied": "SAVE20",
  "payment_method": "card",
  "payment_provider": "stripe"
}
```

### Infrastructure Context

```json
{
  "service_name": "checkout-service",
  "service_version": "2.4.1",
  "deployment_id": "deploy_789",
  "region": "us-east-1",
  "hostname": "checkout-prod-3"
}
```

### Error Context (When errors occur)

```json
{
  "error_type": "PaymentError",
  "error_code": "card_declined",
  "error_message": "Card declined by issuer",
  "error_retriable": false,
  "stripe_decline_code": "insufficient_funds"
}
```

### Performance Context

```json
{
  "db_query_count": 3,
  "db_total_ms": 145,
  "cache_hit": true,
  "external_call_count": 2,
  "external_total_ms": 890
}
```

### Feature Flags

```json
{
  "feature_flags": {
    "new_checkout_flow": true,
    "express_payment": false
  }
}
```

## Implementation by Context

### Backend Services

See [references/BACKEND.md](references/BACKEND.md) for complete patterns
including:

- Middleware implementation (Express, Hono, Fastify)
- Context enrichment in handlers
- Async context propagation
- Database query tracking

### Frontend Analytics

See [references/FRONTEND.md](references/FRONTEND.md) for patterns including:

- Page view and interaction events
- Performance metrics (Core Web Vitals)
- Error boundary integration
- Session and user context

### Analytics Events

See [references/ANALYTICS.md](references/ANALYTICS.md) for patterns including:

- Product analytics (funnel, conversion)
- A/B test instrumentation
- Business metric tracking
- Event naming conventions

## Quick Start: Backend Middleware

```typescript
export async function wideEventMiddleware(ctx, next) {
  const startTime = Date.now();
  const event: Record<string, unknown> = {
    request_id: ctx.get("requestId") || crypto.randomUUID(),
    timestamp: new Date().toISOString(),
    method: ctx.req.method,
    path: ctx.req.path,
    service: process.env.SERVICE_NAME,
    version: process.env.SERVICE_VERSION,
  };

  ctx.set("wideEvent", event);

  try {
    await next();
    event.status_code = ctx.res.status;
    event.outcome = "success";
  } catch (error) {
    event.status_code = 500;
    event.outcome = "error";
    event.error = {
      type: error.name,
      message: error.message,
      code: error.code,
      retriable: error.retriable ?? false,
    };
    throw error;
  } finally {
    event.duration_ms = Date.now() - startTime;
    if (shouldSample(event)) {
      logger.info(event);
    }
  }
}
```

## Tail Sampling

NEVER use random sampling. Use tail-based sampling that keeps important events:

```typescript
function shouldSample(event: WideEvent): boolean {
  // Always keep errors
  if (event.status_code >= 500) return true;
  if (event.error) return true;

  // Always keep slow requests (above p99)
  if (event.duration_ms > 2000) return true;

  // Always keep VIP users
  if (event.user?.subscription === "enterprise") return true;

  // Always keep feature flag rollouts
  if (event.feature_flags?.new_checkout_flow) return true;

  // Random sample the rest at 5%
  return Math.random() < 0.05;
}
```

## Anti-Patterns to Avoid

**NEVER** scatter logs throughout code:

```typescript
// ❌ Bad: 6 log lines, impossible to correlate
logger.info("Processing checkout");
logger.debug("User loaded", { userId });
logger.info("Cart retrieved", { cartId });
logger.debug("Payment starting");
logger.info("Payment complete");
logger.info("Checkout done");
```

**ALWAYS** build one event and emit at the end:

```typescript
// ✅ Good: 1 event with all context
const event = ctx.get("wideEvent");
event.user = { id: user.id, subscription: user.plan };
event.cart = { id: cart.id, total: cart.total };
event.payment = { method: "card", latency_ms: 145 };
// Middleware emits automatically
```

## Debugging Questions Your Events Should Answer

Test your wide event implementation by asking:

- Why did user X's checkout fail? → Need: user_id, error details
- Are premium users experiencing more errors? → Need: subscription_tier
- Which deployment caused latency regression? → Need: deployment_id
- What's the error rate for the new feature? → Need: feature_flags
- What was the user doing before the error? → Need: session context

If you cannot answer these with a single query, add more fields.
