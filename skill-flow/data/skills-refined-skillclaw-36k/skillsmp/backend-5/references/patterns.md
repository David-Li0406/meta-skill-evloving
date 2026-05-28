# Backend Engineering

## Patterns


---
  #### **Name**
Repository Pattern
  #### **Description**
Abstract data access behind interfaces to separate business logic from database implementation
  #### **When**
Testing business logic, switching databases, adding caching, reusing queries
  #### **Example**
    interface UserRepository {
      findById(id: string): Promise<User | null>
      create(data: CreateUserData): Promise<User>
    }
    
    class PrismaUserRepository implements UserRepository {
      async findById(id: string) {
        return this.prisma.user.findUnique({ where: { id } })
      }
    }
    
    // In tests - mock repository
    const mockRepo: UserRepository = {
      findById: jest.fn().mockResolvedValue({ id: '1', name: 'Test' })
    }
    

---
  #### **Name**
Service Layer Pattern
  #### **Description**
Organize business logic into service classes that orchestrate repositories and handle domain rules
  #### **When**
Complex business logic, operations spanning multiple entities, transaction coordination
  #### **Example**
    class OrderService {
      constructor(
        private orders: OrderRepository,
        private products: ProductRepository,
        private payments: PaymentService
      ) {}
    
      async createOrder(userId: string, items: OrderItem[]) {
        // Validate inventory
        for (const item of items) {
          const product = await this.products.findById(item.productId)
          if (product.stock < item.quantity) {
            throw new ValidationError(`Insufficient stock`)
          }
        }
        // Create order, process payment...
      }
    }
    

---
  #### **Name**
Event-Driven Pattern
  #### **Description**
Decouple components by communicating through events rather than direct calls
  #### **When**
Actions trigger multiple side effects, loose coupling needed, async operations
  #### **Example**
    eventBus.emit('order.placed', { order })
    
    // Separate handlers subscribe
    eventBus.on('order.placed', async ({ order }) => {
      await sendOrderConfirmationEmail(order)
    })
    
    eventBus.on('order.placed', async ({ order }) => {
      await reserveInventory(order.items)
    })
    

---
  #### **Name**
Circuit Breaker Pattern
  #### **Description**
Prevent cascading failures by failing fast when a dependency is down
  #### **When**
Calling external services, preventing cascade failures, enabling graceful degradation
  #### **Example**
    const paymentCircuit = new CircuitBreaker({
      failureThreshold: 5,
      resetTimeout: 30000
    })
    
    async charge(amount: number) {
      try {
        return await paymentCircuit.execute(() =>
          this.stripeClient.charges.create({ amount })
        )
      } catch (error) {
        if (error instanceof CircuitOpenError) {
          return this.queueForLaterProcessing(amount)
        }
        throw error
      }
    }
    

---
  #### **Name**
Saga Pattern
  #### **Description**
Coordinate distributed transactions through sequence of local transactions with compensating actions
  #### **When**
Transactions span multiple services, need reversible operations, eventual consistency
  #### **Example**
    class OrderSaga {
      steps = [
        { execute: reserveInventory, compensate: releaseInventory },
        { execute: processPayment, compensate: refundPayment },
        { execute: createShipment, compensate: cancelShipment }
      ]
    
      async execute(data) {
        for (const step of this.steps) {
          try {
            await step.execute(data)
            this.executedSteps.push(step)
          } catch (error) {
            await this.rollback(data)
            throw error
          }
        }
      }
    }
    

---
  #### **Name**
Outbox Pattern
  #### **Description**
Ensure reliable event publishing by storing events in same transaction as business operation
  #### **When**
Need exactly-once event delivery, database and message queue must stay in sync
  #### **Example**
    await db.$transaction(async (tx) => {
      const order = await tx.orders.create({ data })
    
      // Store event in outbox (same transaction)
      await tx.outboxEvents.create({
        data: { type: 'order.created', payload: JSON.stringify(order) }
      })
    
      return order
    })
    // Background worker publishes events from outbox
    

---
  #### **Name**
Retry with Backoff
  #### **Description**
Automatically retry failed operations with increasing delays between attempts
  #### **When**
Calling external services, handling transient failures, self-healing behavior
  #### **Example**
    async function withRetry<T>(fn: () => Promise<T>, options: RetryOptions) {
      let delay = options.initialDelay
      for (let attempt = 1; attempt <= options.maxAttempts; attempt++) {
        try {
          return await fn()
        } catch (error) {
          if (attempt === options.maxAttempts) throw error
          await sleep(delay + Math.random() * 0.3 * delay) // jitter
          delay = Math.min(delay * options.factor, options.maxDelay)
        }
      }
    }
    

---
  #### **Name**
API Versioning
  #### **Description**
Manage breaking changes while maintaining backward compatibility
  #### **When**
External consumers, breaking changes needed, controlled deprecation
  #### **Example**
    app.use('/api/v1', v1Router)
    app.use('/api/v2', v2Router)
    
    // Deprecation headers
    app.use('/api/v1', (req, res, next) => {
      res.set('Deprecation', 'true')
      res.set('Sunset', 'Sat, 1 Jan 2025 00:00:00 GMT')
      next()
    })
    

## Anti-Patterns


---
  #### **Name**
N+1 Queries
  #### **Description**
Firing one query per item in a loop instead of batching
  #### **Why**
Works with 10 items, kills database with 1,000. Response times grow linearly with data size.
  #### **Instead**
Use eager loading (include), JOINs, or batch queries with IN clause

---
  #### **Name**
External Calls in Transactions
  #### **Description**
Calling external APIs inside database transactions
  #### **Why**
Slow external calls hold database locks. Connection pool exhausts. Everything freezes.
  #### **Instead**
External calls outside transactions. Use pending states and update after.

---
  #### **Name**
Check-Then-Act Without Locking
  #### **Description**
Reading a value, checking it, then updating based on the check
  #### **Why**
Race conditions. Two requests both see balance of $100, both deduct $80, balance goes negative.
  #### **Instead**
Atomic updates with WHERE condition, or pessimistic locking (SELECT FOR UPDATE)

---
  #### **Name**
Missing Idempotency
  #### **Description**
Operations that can be safely called once but break when called twice
  #### **Why**
Network retries, user double-clicks, webhook retries all cause duplicate operations.
  #### **Instead**
Idempotency keys for mutations. Check before processing. Return cached response.

---
  #### **Name**
Unbounded Queries
  #### **Description**
Queries without LIMIT that can return millions of rows
  #### **Why**
Works in dev, crashes in production. Memory exhaustion. Client timeouts.
  #### **Instead**
Always paginate. Cursor-based for large datasets. Max limit on user input.

---
  #### **Name**
Fire-and-Forget Async
  #### **Description**
Starting async operations without awaiting or handling errors
  #### **Why**
Errors silently swallowed. Data inconsistency discovered days later.
  #### **Instead**
Await and handle errors. Use job queues for background work.