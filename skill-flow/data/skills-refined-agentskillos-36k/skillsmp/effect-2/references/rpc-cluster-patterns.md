# RPC & Cluster Patterns

## RpcGroup Organization

```typescript
import { Rpc, RpcGroup } from "@effect/rpc"

// Group related endpoints
const UserRpc = RpcGroup.make("UserRpc", {
  // Queries - read operations
  findById: Rpc.query({
    input: UserId,
    output: User,
    error: UserNotFoundError,
  }),

  findByEmail: Rpc.query({
    input: Schema.String,
    output: Schema.Option(User),
  }),

  // Mutations - write operations
  create: Rpc.mutation({
    input: UserInput,
    output: User,
    error: Schema.Union(ValidationError, EmailTakenError),
  }),

  delete: Rpc.mutation({
    input: UserId,
    output: Schema.Void,
    error: UserNotFoundError,
  }),
})
```

## Error Handling

Always use explicit error unions:

```typescript
// GOOD - explicit error types
const OrderRpc = RpcGroup.make("OrderRpc", {
  create: Rpc.mutation({
    input: OrderInput,
    output: Order,
    error: Schema.Union(
      UserNotFoundError,
      InsufficientStockError,
      PaymentDeclinedError,
    ),
  }),
})

// BAD - generic error
const OrderRpc = RpcGroup.make("OrderRpc", {
  create: Rpc.mutation({
    input: OrderInput,
    output: Order,
    error: Schema.Unknown, // WRONG!
  }),
})
```

## RPC Middleware for Authentication

```typescript
import { RpcMiddleware } from "@effect/rpc"

const AuthMiddleware = RpcMiddleware.make((req) =>
  Effect.gen(function* () {
    const authHeader = req.headers.get("authorization")
    if (!authHeader) {
      return yield* Effect.fail(new UnauthorizedError({ message: "Missing auth header" }))
    }

    const token = authHeader.replace("Bearer ", "")
    const user = yield* AuthService.validateToken(token)

    return yield* Effect.provideService(req.effect, CurrentUser, user)
  })
)

// Apply to group
const ProtectedUserRpc = UserRpc.pipe(RpcGroup.middleware(AuthMiddleware))
```

## Workflow Patterns

```typescript
import { Workflow } from "@effect/workflow"

const OrderWorkflow = Workflow.make("OrderWorkflow", {
  // Idempotency key
  idempotencyKey: (input: OrderInput) => `order-${input.userId}-${input.cartId}`,

  // Workflow definition
  execute: (input: OrderInput) =>
    Effect.gen(function* () {
      // Step 1: Reserve inventory
      const reservation = yield* Activities.reserveInventory(input.items)

      // Step 2: Process payment
      const payment = yield* Activities.processPayment({
        userId: input.userId,
        amount: input.total,
        reservationId: reservation.id,
      })

      // Step 3: Create order
      const order = yield* Activities.createOrder({
        ...input,
        paymentId: payment.id,
        reservationId: reservation.id,
      })

      // Step 4: Send confirmation
      yield* Activities.sendConfirmation(order)

      return order
    }),
})
```

## Activities with Schema

```typescript
const Activities = {
  reserveInventory: Workflow.activity("reserveInventory", {
    input: Schema.Array(OrderItem),
    output: Reservation,
    error: InsufficientStockError,
    execute: (items) =>
      Effect.gen(function* () {
        const inventory = yield* InventoryService
        return yield* inventory.reserve(items)
      }),
  }),

  processPayment: Workflow.activity("processPayment", {
    input: PaymentInput,
    output: Payment,
    error: Schema.Union(PaymentDeclinedError, PaymentServiceError),
    execute: (input) =>
      Effect.gen(function* () {
        const payments = yield* PaymentService
        return yield* payments.charge(input)
      }),
  }),
}
```

## Scheduled Jobs with ClusterCron

```typescript
import { ClusterCron } from "@effect/cluster"

const DailyReport = ClusterCron.make("DailyReport", {
  // Run at midnight UTC every day
  schedule: "0 0 * * *",

  execute: Effect.gen(function* () {
    yield* Effect.log("Generating daily report")

    const stats = yield* ReportService.generateDailyStats()
    yield* EmailService.sendReport({
      to: "team@example.com",
      subject: "Daily Report",
      data: stats,
    })

    yield* Effect.log("Daily report sent")
  }),
})

const HourlyCleanup = ClusterCron.make("HourlyCleanup", {
  schedule: "0 * * * *",

  execute: Effect.gen(function* () {
    yield* CacheService.evictStale()
    yield* TempFileService.cleanup()
  }),
})
```

## Triggering Workflows from HTTP Handlers

```typescript
import { HttpRouter } from "@effect/platform"

const router = HttpRouter.empty.pipe(
  HttpRouter.post("/orders", (req) =>
    Effect.gen(function* () {
      const input = yield* req.json.pipe(
        Effect.flatMap(Schema.decodeUnknown(OrderInput))
      )

      // Start workflow
      const workflowClient = yield* WorkflowClient
      const handle = yield* workflowClient.start(OrderWorkflow, input)

      return HttpResponse.json({
        workflowId: handle.id,
        status: "started",
      })
    })
  ),

  HttpRouter.get("/orders/:workflowId/status", (req) =>
    Effect.gen(function* () {
      const workflowId = req.params.workflowId
      const workflowClient = yield* WorkflowClient
      const status = yield* workflowClient.getStatus(workflowId)

      return HttpResponse.json(status)
    })
  ),
)
```

## RPC Router Setup

```typescript
import { RpcRouter } from "@effect/rpc"

const router = RpcRouter.make(
  UserRpc,
  OrderRpc,
  PaymentRpc,
)

// Serve via HTTP
const httpApp = RpcRouter.toHttpApp(router)

// Or via WebSocket for streaming
const wsApp = RpcRouter.toWebSocketApp(router)
```

## Streaming RPC

```typescript
const StreamingRpc = RpcGroup.make("StreamingRpc", {
  // Server-sent events / streaming response
  watchOrders: Rpc.stream({
    input: UserId,
    output: Order,
    error: UserNotFoundError,
  }),
})

// Implementation
const watchOrders = (userId: UserId) =>
  Effect.gen(function* () {
    const orders = yield* OrderService
    return orders.watchByUser(userId) // Returns Stream<Order>
  })
```
