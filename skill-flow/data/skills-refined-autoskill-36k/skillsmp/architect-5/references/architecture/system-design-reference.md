# System Design Reference

## Architecture Styles

### Monolith
Single deployable unit containing all application functionality.

**Use when:**
- Small team (< 10)
- Simple domain
- Fast iteration needed
- Uncertain requirements

**Characteristics:**
- Single codebase
- Shared database
- In-process communication
- Simple deployment

### Microservices
Independently deployable services organized around business capabilities.

**Use when:**
- Large team (> 20)
- Clear bounded contexts
- Different scaling needs
- Technology flexibility needed

**Characteristics:**
- Service per team
- Database per service
- Network communication
- Independent deployment

### Modular Monolith
Monolith with enforced module boundaries.

**Use when:**
- Growing team needing boundaries
- Want monolith simplicity + clear ownership
- Preparing for potential microservices

**Characteristics:**
- Single deployment
- Module-specific schemas
- Internal APIs between modules
- Clear team ownership

### Serverless
Functions executed in response to events.

**Use when:**
- Event-driven workloads
- Variable traffic
- Cost optimization priority
- Quick time to market

**Characteristics:**
- Function-as-a-Service
- Pay per execution
- Auto-scaling
- No server management

## Communication Patterns

### Synchronous
- REST APIs
- GraphQL
- gRPC

**Pros:** Simple, immediate response
**Cons:** Tight coupling, cascade failures

### Asynchronous
- Message queues (RabbitMQ, SQS)
- Event streaming (Kafka)
- Pub/Sub

**Pros:** Loose coupling, resilience
**Cons:** Eventual consistency, complexity

## Data Architecture

### Database per Service
Each service owns its data completely.

**Challenges:**
- Cross-service queries
- Data consistency
- Distributed transactions

**Solutions:**
- Saga pattern for transactions
- Event sourcing for consistency
- CQRS for complex queries

### Event Sourcing
Store events, not current state.

**Benefits:**
- Complete audit trail
- Time travel queries
- Event replay

### CQRS
Separate read and write models.

**Benefits:**
- Optimize reads/writes independently
- Scale reads separately
- Complex query support

## Scalability Patterns

### Horizontal Scaling
Add more instances.

**Requirements:**
- Stateless services
- Shared nothing architecture
- Load balancing

### Vertical Scaling
Add more resources to instance.

**Limits:**
- Hardware constraints
- Single point of failure
- Diminishing returns

### Caching
Reduce load on data stores.

**Levels:**
- Browser cache
- CDN
- Application cache
- Database cache

### Database Scaling
- Read replicas
- Sharding
- Partitioning

## Reliability Patterns

### Circuit Breaker
Prevent cascade failures.

**States:**
1. Closed - Normal operation
2. Open - Fail fast
3. Half-Open - Test recovery

### Retry with Backoff
Handle transient failures.

```
wait_time = base * 2^attempt + jitter
```

### Bulkhead
Isolate failures.

**Approaches:**
- Thread pool isolation
- Process isolation
- Service isolation

### Timeout
Bound wait time.

**Guidelines:**
- Set on all external calls
- Include in SLA budget
- Monitor timeout rates

## Security Architecture

### Defense in Depth
Multiple security layers:
1. Network (firewall, WAF)
2. Transport (TLS)
3. Application (auth, authz)
4. Data (encryption)

### Zero Trust
Never trust, always verify:
- Verify identity for all access
- Least privilege access
- Assume breach
- Encrypt everything

### Authentication Patterns
- OAuth 2.0 / OIDC - Delegated authorization
- JWT - Stateless tokens
- Session - Server-side state
- API Keys - Service auth

### Authorization Patterns
- RBAC - Role-based
- ABAC - Attribute-based
- ReBAC - Relationship-based

## Observability

### Three Pillars

**Metrics:**
- Request rate
- Error rate
- Latency (p50, p95, p99)
- Saturation

**Logs:**
- Structured format
- Correlation IDs
- Log levels
- Centralized aggregation

**Traces:**
- Distributed tracing
- Span context
- Service dependencies
- Latency breakdown

### Alerting
- Alert on symptoms, not causes
- Actionable alerts only
- Clear runbooks
- Escalation paths

## Integration Patterns

### API Gateway
Single entry point for clients.

**Functions:**
- Routing
- Authentication
- Rate limiting
- Request transformation

### Service Mesh
Infrastructure layer for service-to-service.

**Provides:**
- mTLS
- Load balancing
- Observability
- Traffic management

### Backend for Frontend (BFF)
Dedicated backend per client type.

**Benefits:**
- Optimized for client
- Team ownership
- Decoupled evolution

## Quality Attributes

| Attribute | Measures | Trade-offs |
|-----------|----------|------------|
| Scalability | Load handling | Complexity |
| Reliability | Uptime, MTTR | Cost |
| Performance | Latency, throughput | Resource usage |
| Security | Attack resistance | Usability |
| Maintainability | Change ease | Initial effort |
