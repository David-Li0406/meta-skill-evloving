# Observability Patterns

## Structured Logging with Effect.log

Always use `Effect.log` instead of `console.log`:

```typescript
// Basic logging
yield* Effect.log("User created")

// With annotations
yield* Effect.log("User created").pipe(
  Effect.annotateLogs({ userId: user.id, email: user.email })
)

// Log levels
yield* Effect.logDebug("Processing started")
yield* Effect.logInfo("User logged in")
yield* Effect.logWarning("Rate limit approaching")
yield* Effect.logError("Payment failed")
yield* Effect.logFatal("Database connection lost")
```

## Effect.fn for Automatic Tracing

```typescript
class UserService extends Effect.Service<UserService>()("UserService", {
  effect: Effect.gen(function* () {
    return {
      // Automatic span: "UserService.findById"
      findById: Effect.fn("UserService.findById")(
        (id: UserId) => /* ... */
      ),
    }
  }),
}) {}
```

## Span Annotations

Annotate with valuable business context:

```typescript
// GOOD - entity IDs, business values, error context
yield* Effect.annotateCurrentSpan({
  userId: user.id,
  orderId: order.id,
  amount: order.total,
  paymentMethod: order.paymentMethod,
})

// BAD - noise
yield* Effect.annotateCurrentSpan({
  step: "step 3",           // Progress tracking
  item: "processing item",   // Individual items
  internalState: state,      // Internal details
  password: user.password,   // Sensitive data!
})
```

## Metrics

### Counters

```typescript
const ordersProcessed = Metric.counter("orders_processed")
const failedRequests = Metric.counter("requests_failed")

// Increment
yield* Metric.increment(ordersProcessed)

// Increment by value
yield* Metric.incrementBy(ordersProcessed, 5)
```

### Tagged Counters

```typescript
const requestsTotal = Metric.counter("http_requests_total").pipe(
  Metric.tagged("method", "GET"),
  Metric.tagged("status", "200"),
  Metric.tagged("path", "/users"),
)

// Or dynamically
const trackRequest = (method: string, status: number, path: string) =>
  Metric.counter("http_requests_total").pipe(
    Metric.tagged("method", method),
    Metric.tagged("status", String(status)),
    Metric.tagged("path", path),
    Metric.increment,
  )
```

### Gauges

```typescript
const activeConnections = Metric.gauge("active_connections")

// Set value
yield* Metric.set(activeConnections, currentConnections)

// Increment/decrement
yield* Metric.increment(activeConnections)
yield* Metric.decrement(activeConnections)
```

### Histograms

```typescript
const requestDuration = Metric.histogram(
  "http_request_duration_ms",
  Metric.Boundaries.exponential({ start: 1, factor: 2, count: 10 })
)

// Record value
yield* Metric.record(requestDuration, elapsed)

// With Effect.timed
yield* doWork().pipe(
  Effect.timed,
  Effect.tap(([duration]) => Metric.record(requestDuration, Duration.toMillis(duration)))
)
```

## Configuration with Config

```typescript
// Basic config
const port = yield* Config.number("PORT")
const host = yield* Config.string("HOST")

// With defaults
const port = yield* Config.number("PORT").pipe(Config.withDefault(3000))

// With validation
const port = yield* Config.number("PORT").pipe(
  Config.validate({
    message: "Port must be between 1 and 65535",
    validation: (n) => n > 0 && n < 65536,
  })
)

// Secrets (prevents logging)
const apiKey = yield* Config.secret("API_KEY")

// Nested config
const DatabaseConfig = Config.all({
  host: Config.string("DB_HOST"),
  port: Config.number("DB_PORT").pipe(Config.withDefault(5432)),
  name: Config.string("DB_NAME"),
  user: Config.string("DB_USER"),
  password: Config.secret("DB_PASSWORD"),
})
```

## Log Level Configuration

```typescript
// Set log level from environment
const LogLevel = Config.logLevel("LOG_LEVEL").pipe(
  Config.withDefault(LogLevel.Info)
)

// Apply to program
program.pipe(
  Logger.withMinimumLogLevel(yield* LogLevel)
)
```

## Integration Example

```typescript
class PaymentService extends Effect.Service<PaymentService>()("PaymentService", {
  effect: Effect.gen(function* () {
    const paymentsProcessed = Metric.counter("payments_processed")
    const paymentsFailed = Metric.counter("payments_failed")
    const paymentDuration = Metric.histogram("payment_duration_ms", /* ... */)

    return {
      process: Effect.fn("PaymentService.process")(
        (payment: PaymentInput) =>
          Effect.gen(function* () {
            yield* Effect.log("Processing payment").pipe(
              Effect.annotateLogs({ amount: payment.amount, method: payment.method })
            )

            yield* Effect.annotateCurrentSpan({
              paymentId: payment.id,
              amount: payment.amount,
            })

            const start = yield* Clock.currentTimeMillis

            const result = yield* processWithProvider(payment).pipe(
              Effect.tap(() => Metric.increment(paymentsProcessed)),
              Effect.tapError(() => Metric.increment(paymentsFailed))
            )

            const elapsed = (yield* Clock.currentTimeMillis) - start
            yield* Metric.record(paymentDuration, elapsed)

            yield* Effect.log("Payment completed").pipe(
              Effect.annotateLogs({ elapsed, transactionId: result.transactionId })
            )

            return result
          })
      ),
    }
  }),
}) {}
```
