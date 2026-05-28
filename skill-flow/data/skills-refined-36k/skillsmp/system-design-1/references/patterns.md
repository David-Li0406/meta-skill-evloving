# System Design Patterns Reference

## Architectural Patterns

### Layered Architecture

```
┌─────────────────────────┐
│   Presentation Layer    │  UI, API endpoints
├─────────────────────────┤
│    Application Layer    │  Business logic, orchestration
├─────────────────────────┤
│      Domain Layer       │  Core business rules
├─────────────────────────┤
│   Infrastructure Layer  │  Database, external services
└─────────────────────────┘
```

**Rules:**
- Each layer only depends on layers below it
- Never skip layers
- Use interfaces for dependency inversion

### Hexagonal Architecture (Ports & Adapters)

```
                    ┌─────────────┐
    REST API ──────►│             │◄────── Database
                    │    Core     │
    GraphQL ───────►│   Domain    │◄────── Message Queue
                    │             │
    CLI ───────────►│             │◄────── External API
                    └─────────────┘
```

**Ports:** Interfaces defined by the domain
**Adapters:** Implementations that connect to external systems

Benefits:
- Testability (mock adapters)
- Technology independence
- Clear boundaries

### Clean Architecture

Dependency rule: Dependencies point inward

```
┌──────────────────────────────────────┐
│ Frameworks & Drivers (Web, DB, UI)   │
├──────────────────────────────────────┤
│ Interface Adapters (Controllers,     │
│ Gateways, Presenters)                │
├──────────────────────────────────────┤
│ Use Cases (Application Business)     │
├──────────────────────────────────────┤
│ Entities (Enterprise Business Rules) │
└──────────────────────────────────────┘
```

### Domain-Driven Design (DDD)

**Strategic Patterns:**
- Bounded Context - Explicit boundary around a domain model
- Context Map - Relationships between bounded contexts
- Ubiquitous Language - Shared vocabulary

**Tactical Patterns:**
- Entity - Identity-based object
- Value Object - Immutable, equality by value
- Aggregate - Consistency boundary
- Repository - Collection-like interface for aggregates
- Domain Event - Something that happened in the domain
- Domain Service - Stateless operations

## Microservices Patterns

### Service Communication

**Synchronous:**
- REST over HTTP
- gRPC (binary protocol)
- GraphQL Federation

**Asynchronous:**
- Message Queue (RabbitMQ)
- Event Streaming (Kafka)
- Pub/Sub (Google Cloud Pub/Sub, AWS SNS)

### Service Discovery

**Client-side discovery:**
```
Client → Service Registry → Service Instance
```

**Server-side discovery:**
```
Client → Load Balancer → Service Instance
                ↓
        Service Registry
```

Tools: Consul, etcd, Kubernetes DNS, AWS Cloud Map

### API Gateway Pattern

```
                    ┌─────────────┐
Client ────────────►│ API Gateway │
                    └─────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   ┌─────────┐       ┌─────────┐       ┌─────────┐
   │Service A│       │Service B│       │Service C│
   └─────────┘       └─────────┘       └─────────┘
```

Responsibilities:
- Request routing
- Authentication/Authorization
- Rate limiting
- Request/response transformation
- Caching
- Monitoring

Tools: Kong, AWS API Gateway, Nginx, Traefik

### Saga Pattern

For distributed transactions:

**Choreography:**
```
Service A → Event → Service B → Event → Service C
    ↑                                      │
    └──────── Compensating Event ──────────┘
```

**Orchestration:**
```
         ┌───────────────┐
         │   Saga        │
         │ Orchestrator  │
         └───────────────┘
          │     │     │
          ▼     ▼     ▼
        Svc A Svc B Svc C
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing fast
    HALF_OPEN = "half_open"  # Testing recovery

    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.state = self.CLOSED
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = None

    def call(self, func):
        if self.state == self.OPEN:
            if time_since(self.last_failure_time) > self.recovery_timeout:
                self.state = self.HALF_OPEN
            else:
                raise CircuitOpenError()

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
```

Libraries: Hystrix (deprecated), Resilience4j, Polly

### Bulkhead Pattern

Isolate failures to prevent cascade:

```
┌────────────────────────────────────┐
│           Application              │
├──────────┬──────────┬──────────────┤
│ Pool A   │ Pool B   │ Pool C       │
│ (Users)  │ (Orders) │ (Analytics)  │
└──────────┴──────────┴──────────────┘
```

Implementation:
- Thread pools per dependency
- Connection pools per service
- Rate limits per client

## Data Patterns

### CQRS (Command Query Responsibility Segregation)

```
        Commands                    Queries
           │                           │
           ▼                           ▼
    ┌─────────────┐            ┌─────────────┐
    │   Write     │            │    Read     │
    │   Model     │───Event───►│    Model    │
    │ (Normalized)│            │(Denormalized)│
    └─────────────┘            └─────────────┘
           │                           │
           ▼                           ▼
    ┌─────────────┐            ┌─────────────┐
    │   Write     │            │    Read     │
    │     DB      │            │     DB      │
    └─────────────┘            └─────────────┘
```

When to use:
- Read/write ratio heavily skewed
- Different scaling requirements
- Complex domain with different read views

### Event Sourcing

Store events instead of current state:

```
Account Events:
1. AccountCreated { id: 1, owner: "Alice" }
2. MoneyDeposited { account: 1, amount: 100 }
3. MoneyWithdrawn { account: 1, amount: 30 }
4. MoneyDeposited { account: 1, amount: 50 }

Current Balance = replay events = 120
```

Benefits:
- Complete audit trail
- Temporal queries
- Event replay for debugging
- Easy to add new projections

Challenges:
- Schema evolution
- Event versioning
- Snapshots for performance
- Eventual consistency

### Database Sharding

**Horizontal partitioning strategies:**

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| Range | user_id 1-1M → shard1 | Simple | Hot spots |
| Hash | hash(user_id) % N | Even distribution | Resharding hard |
| Directory | Lookup table | Flexible | Extra hop |
| Geographic | EU → shard_eu | Data locality | Uneven load |

### Read Replicas

```
       Writes
          │
          ▼
    ┌──────────┐
    │  Primary │
    └──────────┘
          │
    Replication
     ┌────┼────┐
     ▼    ▼    ▼
  ┌────┐┌────┐┌────┐
  │Rep1││Rep2││Rep3│  ← Reads
  └────┘└────┘└────┘
```

Considerations:
- Replication lag
- Read-after-write consistency
- Failover promotion

## Caching Patterns

### Cache-Aside (Lazy Loading)

```
1. Check cache
2. If miss → read from DB → write to cache
3. Return data
```

```python
def get_user(user_id):
    user = cache.get(f"user:{user_id}")
    if user is None:
        user = db.query("SELECT * FROM users WHERE id = ?", user_id)
        cache.set(f"user:{user_id}", user, ttl=3600)
    return user
```

### Write-Through

```
1. Write to cache
2. Cache writes to DB
3. Return success
```

Ensures consistency but adds latency to writes.

### Write-Behind (Write-Back)

```
1. Write to cache
2. Return success immediately
3. Cache asynchronously writes to DB
```

Better write performance but risk of data loss.

### Cache Invalidation Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| TTL | Expire after time | Acceptable staleness |
| Event-based | Invalidate on write | Strong consistency |
| Version tags | Check version on read | Read-heavy |

## Messaging Patterns

### Message Queue vs Event Stream

| Aspect | Message Queue | Event Stream |
|--------|---------------|--------------|
| Consumption | One consumer | Multiple consumers |
| Retention | Until processed | Time-based |
| Ordering | Per-queue | Per-partition |
| Replay | No | Yes |
| Use case | Task distribution | Event sourcing |

### Competing Consumers

```
Producer → Queue → [Consumer 1]
                 → [Consumer 2]
                 → [Consumer 3]
```

For parallel processing, ensure idempotency.

### Publish-Subscribe

```
Publisher → Topic → Subscriber 1
                  → Subscriber 2
                  → Subscriber 3
```

For broadcasting events to multiple interested parties.

### Dead Letter Queue

```
Producer → Main Queue → Consumer
                │
                └──(failures)──→ DLQ → Alert/Manual Processing
```

Handle messages that can't be processed.

## Resilience Patterns

### Retry with Exponential Backoff

```python
def retry_with_backoff(func, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

### Timeout Pattern

Always set timeouts for external calls:
- Connection timeout: 1-5 seconds
- Read timeout: 5-30 seconds depending on operation
- Overall timeout: Include retries

### Fallback Pattern

```python
def get_recommendations(user_id):
    try:
        return recommendation_service.get(user_id)
    except ServiceUnavailable:
        return get_popular_items()  # Fallback to cached popular items
```

### Health Check Pattern

```python
@app.route("/health")
def health():
    checks = {
        "database": check_database(),
        "cache": check_cache(),
        "external_api": check_external_api()
    }

    healthy = all(checks.values())
    status = 200 if healthy else 503

    return jsonify(checks), status
```

Types:
- Liveness: Is the process running?
- Readiness: Can the service handle requests?
- Startup: Has the service initialized?
