# Backend Wide Event Patterns

Complete implementation patterns for backend services.

## Table of Contents

- [Middleware Patterns](#middleware-patterns)
- [Context Enrichment](#context-enrichment)
- [Async Context Propagation](#async-context-propagation)
- [Database Query Tracking](#database-query-tracking)
- [External Service Calls](#external-service-calls)
- [Framework Examples](#framework-examples)

## Middleware Patterns

### Express.js

```typescript
import { AsyncLocalStorage } from "async_hooks";

const eventStorage = new AsyncLocalStorage<Record<string, unknown>>();

export function wideEventMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const startTime = Date.now();
  const event: Record<string, unknown> = {
    request_id: req.headers["x-request-id"] || crypto.randomUUID(),
    trace_id: req.headers["x-trace-id"],
    timestamp: new Date().toISOString(),
    method: req.method,
    path: req.path,
    query_params: Object.keys(req.query),
    service: process.env.SERVICE_NAME,
    version: process.env.SERVICE_VERSION,
    deployment_id: process.env.DEPLOYMENT_ID,
    region: process.env.AWS_REGION || process.env.REGION,
    hostname: os.hostname(),
  };

  eventStorage.run(event, () => {
    res.on("finish", () => {
      event.status_code = res.statusCode;
      event.duration_ms = Date.now() - startTime;
      event.response_size_bytes = parseInt(
        res.getHeader("content-length") || "0",
      );
      event.outcome = res.statusCode < 400 ? "success" : "error";

      if (shouldSample(event)) {
        logger.info(event);
      }
    });

    next();
  });
}

export function getWideEvent(): Record<string, unknown> {
  return eventStorage.getStore() || {};
}
```

### Hono

```typescript
import { createMiddleware } from "hono/factory";

export const wideEventMiddleware = createMiddleware(async (c, next) => {
  const startTime = Date.now();
  const event: Record<string, unknown> = {
    request_id: c.req.header("x-request-id") || crypto.randomUUID(),
    trace_id: c.req.header("x-trace-id"),
    timestamp: new Date().toISOString(),
    method: c.req.method,
    path: c.req.path,
    service: c.env?.SERVICE_NAME || process.env.SERVICE_NAME,
    version: c.env?.SERVICE_VERSION || process.env.SERVICE_VERSION,
  };

  c.set("wideEvent", event);

  try {
    await next();
    event.status_code = c.res.status;
    event.outcome = "success";
  } catch (error) {
    event.status_code = 500;
    event.outcome = "error";
    event.error = {
      type: error.name,
      message: error.message,
      code: error.code,
      stack: process.env.NODE_ENV === "development" ? error.stack : undefined,
    };
    throw error;
  } finally {
    event.duration_ms = Date.now() - startTime;
    if (shouldSample(event)) {
      console.log(JSON.stringify(event));
    }
  }
});
```

### Fastify

```typescript
import fp from "fastify-plugin";

export default fp(async function wideEventPlugin(fastify) {
  fastify.decorateRequest("wideEvent", null);

  fastify.addHook("onRequest", async (request) => {
    request.wideEvent = {
      request_id: request.id,
      trace_id: request.headers["x-trace-id"],
      timestamp: new Date().toISOString(),
      method: request.method,
      path: request.url,
      service: process.env.SERVICE_NAME,
      version: process.env.SERVICE_VERSION,
    };
  });

  fastify.addHook("onResponse", async (request, reply) => {
    const event = request.wideEvent;
    event.status_code = reply.statusCode;
    event.duration_ms = reply.elapsedTime;
    event.outcome = reply.statusCode < 400 ? "success" : "error";

    if (shouldSample(event)) {
      request.log.info(event);
    }
  });

  fastify.addHook("onError", async (request, reply, error) => {
    const event = request.wideEvent;
    event.error = {
      type: error.name,
      message: error.message,
      code: error.code,
    };
  });
});
```

### Python (FastAPI)

```python
import time
import uuid
from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

wide_event: ContextVar[dict] = ContextVar("wide_event", default={})

class WideEventMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        event = {
            "request_id": request.headers.get("x-request-id", str(uuid.uuid4())),
            "trace_id": request.headers.get("x-trace-id"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "method": request.method,
            "path": request.url.path,
            "service": os.getenv("SERVICE_NAME"),
            "version": os.getenv("SERVICE_VERSION"),
        }

        token = wide_event.set(event)

        try:
            response = await call_next(request)
            event["status_code"] = response.status_code
            event["outcome"] = "success" if response.status_code < 400 else "error"
            return response
        except Exception as e:
            event["status_code"] = 500
            event["outcome"] = "error"
            event["error"] = {
                "type": type(e).__name__,
                "message": str(e),
            }
            raise
        finally:
            event["duration_ms"] = (time.perf_counter() - start_time) * 1000
            if should_sample(event):
                logger.info(json.dumps(event))
            wide_event.reset(token)

def get_wide_event() -> dict:
    return wide_event.get()
```

### Go (Chi/stdlib)

```go
type contextKey string
const wideEventKey contextKey = "wideEvent"

func WideEventMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        event := map[string]interface{}{
            "request_id":  r.Header.Get("X-Request-ID"),
            "trace_id":    r.Header.Get("X-Trace-ID"),
            "timestamp":   time.Now().UTC().Format(time.RFC3339Nano),
            "method":      r.Method,
            "path":        r.URL.Path,
            "service":     os.Getenv("SERVICE_NAME"),
            "version":     os.Getenv("SERVICE_VERSION"),
        }

        if event["request_id"] == "" {
            event["request_id"] = uuid.New().String()
        }

        ctx := context.WithValue(r.Context(), wideEventKey, event)
        rw := &responseWriter{ResponseWriter: w, statusCode: 200}

        defer func() {
            event["status_code"] = rw.statusCode
            event["duration_ms"] = time.Since(start).Milliseconds()
            event["outcome"] = "success"
            if rw.statusCode >= 400 {
                event["outcome"] = "error"
            }

            if shouldSample(event) {
                jsonBytes, _ := json.Marshal(event)
                log.Println(string(jsonBytes))
            }
        }()

        next.ServeHTTP(rw, r.WithContext(ctx))
    })
}

func GetWideEvent(ctx context.Context) map[string]interface{} {
    if event, ok := ctx.Value(wideEventKey).(map[string]interface{}); ok {
        return event
    }
    return make(map[string]interface{})
}
```

## Context Enrichment

### Adding User Context

```typescript
// After authentication middleware
function addUserContext(req: Request, res: Response, next: NextFunction) {
  const event = getWideEvent();
  const user = req.user; // From auth middleware

  event.user = {
    id: user.id,
    subscription: user.subscriptionTier,
    account_age_days: daysSince(user.createdAt),
    lifetime_value_cents: user.lifetimeValue,
    is_internal: user.email?.endsWith("@company.com"),
    roles: user.roles,
  };

  next();
}
```

### Adding Business Context in Handlers

```typescript
app.post("/checkout", async (req, res) => {
  const event = getWideEvent();

  // Add cart context
  const cart = await getCart(req.user.id);
  event.cart = {
    id: cart.id,
    item_count: cart.items.length,
    total_cents: cart.totalCents,
    has_subscription_items: cart.items.some((i) => i.isSubscription),
    coupon_applied: cart.coupon?.code,
    coupon_discount_cents: cart.coupon?.discountCents,
  };

  // Process payment and add timing
  const paymentStart = Date.now();
  const payment = await processPayment(cart);

  event.payment = {
    method: payment.method,
    provider: payment.provider,
    latency_ms: Date.now() - paymentStart,
    attempt_number: payment.attemptNumber,
    amount_cents: payment.amountCents,
    currency: payment.currency,
  };

  if (payment.error) {
    event.payment.error_code = payment.error.code;
    event.payment.decline_reason = payment.error.declineCode;
  }

  res.json({ orderId: payment.orderId });
});
```

## Async Context Propagation

### Node.js AsyncLocalStorage

```typescript
import { AsyncLocalStorage } from "async_hooks";

const eventStorage = new AsyncLocalStorage<Record<string, unknown>>();

// Helper to run code with event context
export function withWideEvent<T>(
  event: Record<string, unknown>,
  fn: () => T,
): T {
  return eventStorage.run(event, fn);
}

// Get current event anywhere in the call stack
export function getWideEvent(): Record<string, unknown> {
  return eventStorage.getStore() || {};
}

// Usage in nested async functions
async function processOrder(orderId: string) {
  const event = getWideEvent();

  const order = await db.orders.findById(orderId);
  event.order = { id: order.id, status: order.status };

  // Event is available in nested calls
  await chargePayment(order);
  await sendConfirmation(order);
}
```

## Database Query Tracking

### Wrapper Pattern

```typescript
class TrackedDB {
  private queryCount = 0;
  private totalMs = 0;

  async query<T>(sql: string, params?: unknown[]): Promise<T> {
    const start = Date.now();

    try {
      const result = await this.db.query(sql, params);
      return result;
    } finally {
      const duration = Date.now() - start;
      this.queryCount++;
      this.totalMs += duration;

      // Update wide event
      const event = getWideEvent();
      event.db_query_count = this.queryCount;
      event.db_total_ms = this.totalMs;

      // Track slow queries
      if (duration > 100) {
        event.slow_queries = event.slow_queries || [];
        event.slow_queries.push({
          sql: sql.substring(0, 100),
          duration_ms: duration,
          rows: result.rowCount,
        });
      }
    }
  }
}
```

### Prisma Extension

```typescript
const prisma = new PrismaClient().$extends({
  query: {
    async $allOperations({ operation, model, args, query }) {
      const start = Date.now();
      const result = await query(args);
      const duration = Date.now() - start;

      const event = getWideEvent();
      event.db_queries = event.db_queries || [];
      event.db_queries.push({
        model,
        operation,
        duration_ms: duration,
      });

      return result;
    },
  },
});
```

## External Service Calls

### Fetch Wrapper

```typescript
async function trackedFetch(
  url: string,
  options?: RequestInit,
): Promise<Response> {
  const event = getWideEvent();
  const start = Date.now();
  const serviceName = new URL(url).hostname;

  event.external_calls = event.external_calls || [];

  try {
    const response = await fetch(url, options);

    event.external_calls.push({
      service: serviceName,
      method: options?.method || "GET",
      path: new URL(url).pathname,
      status_code: response.status,
      duration_ms: Date.now() - start,
    });

    return response;
  } catch (error) {
    event.external_calls.push({
      service: serviceName,
      method: options?.method || "GET",
      path: new URL(url).pathname,
      error: error.message,
      duration_ms: Date.now() - start,
    });
    throw error;
  }
}
```

## OpenTelemetry Integration

Wide events complement OTel spans. Add the same context to both:

```typescript
import { trace } from "@opentelemetry/api";

app.post("/checkout", async (req, res) => {
  const span = trace.getActiveSpan();
  const event = getWideEvent();

  // Add context to BOTH span and wide event
  const context = {
    "user.id": req.user.id,
    "user.subscription": req.user.plan,
    "cart.item_count": req.body.items.length,
    "cart.total_cents": req.body.total,
  };

  // OTel span attributes
  span?.setAttributes(context);

  // Wide event (use nested structure)
  event.user = { id: req.user.id, subscription: req.user.plan };
  event.cart = {
    item_count: req.body.items.length,
    total_cents: req.body.total,
  };

  // ... handler logic
});
```
