---
name: data-infrastructure-at-scale
description: |
  Build data infrastructure that scales from prototype to production. Use when architecting
  data pipelines, choosing data stores, planning for high throughput, or migrating to distributed
  systems. Covers caching, replication, sharding, message queues, and data lake architecture.
---

# Data Infrastructure at Scale

Build data infrastructure that grows from MVP to millions of users without rewrites.

## When to Use

Use this skill when:
- Architecting a new data platform
- Current infrastructure can't handle load (slow queries, timeouts)
- Planning to scale from thousands to millions of records/requests
- Choosing between databases, caches, message queues
- Designing ETL/ELT pipelines
- Building real-time analytics or streaming systems

---

## Scaling Stages

### Stage 1: Prototype (< 10K users)

**Architecture**:
```
┌─────────┐
│   App   │
└────┬────┘
     │
┌────▼────┐
│   DB    │
└─────────┘
```

**Characteristics**:
- Single database server
- No caching
- Synchronous processing
- Simple backups

**When to graduate**: Response time > 200ms, database CPU > 60%

---

### Stage 2: Caching (10K - 100K users)

**Architecture**:
```
┌─────────┐
│   App   │
└─┬────┬──┘
  │    │
  │  ┌─▼──────┐
  │  │ Cache  │
  │  └────────┘
  │
┌─▼────┐
│  DB  │
└──────┘
```

**Add**:
- Redis/Memcached for hot data
- CDN for static assets
- Cache invalidation strategy

**Pattern: Cache-Aside**
```python
def get_user(user_id):
    # Try cache first
    user = cache.get(f"user:{user_id}")
    if user:
        return user

    # Miss: fetch from DB
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)

    # Populate cache
    cache.set(f"user:{user_id}", user, ttl=300)
    return user
```

**When to graduate**: Database read load > 70%, cache hit rate < 80%

---

### Stage 3: Read Replicas (100K - 1M users)

**Architecture**:
```
┌─────────┐
│   App   │
└─┬────┬──┘
  │    │
  │  ┌─▼──────┐
  │  │ Cache  │
  │  └────────┘
  │
  │  ┌─────────┐
  ├──► Primary │ (writes)
  │  └────┬────┘
  │       │ replication
  │  ┌────▼────┐
  └──► Replica │ (reads)
     └─────────┘
```

**Add**:
- Read replicas for read-heavy workloads
- Write to primary, read from replicas
- Replication lag monitoring

**Pattern: Write-Primary, Read-Replica**
```python
def get_user(user_id):
    return db_replica.query("SELECT * FROM users WHERE id = ?", user_id)

def update_user(user_id, data):
    # Must use primary for writes
    db_primary.execute("UPDATE users SET ... WHERE id = ?", data, user_id)
    # Invalidate cache
    cache.delete(f"user:{user_id}")
```

**Gotcha: Replication Lag**
```python
# Problem: Read-your-own-writes fails
def create_post(user_id, content):
    post_id = db_primary.insert("INSERT INTO posts ...", user_id, content)

    # Reads from replica, but replication hasn't caught up yet!
    post = db_replica.query("SELECT * FROM posts WHERE id = ?", post_id)
    # post might be None!

# Fix: Read from primary immediately after write
def create_post(user_id, content):
    post_id = db_primary.insert("INSERT INTO posts ...", user_id, content)
    post = db_primary.query("SELECT * FROM posts WHERE id = ?", post_id)
    return post
```

**When to graduate**: Single database can't handle write load, need horizontal scaling

---

### Stage 4: Sharding (1M - 10M users)

**Architecture**:
```
┌─────────┐
│   App   │
└────┬────┘
     │
┌────▼─────────┐
│ Shard Router │
└─┬──────────┬─┘
  │          │
┌─▼──────┐ ┌─▼──────┐
│Shard 1 │ │Shard 2 │  (each shard has replicas)
│user 0-5M │Shard 5M-10M│
└────────┘ └────────┘
```

**Sharding Strategies**:

**1. Hash-based** (even distribution):
```python
def get_shard(user_id):
    return user_id % NUM_SHARDS

# User 123 → Shard 3
# User 456 → Shard 0
```
- ✓ Even distribution
- ✗ Range queries hard (need to query all shards)
- ✗ Resharding difficult

**2. Range-based** (logical grouping):
```python
def get_shard(user_id):
    if user_id < 5_000_000:
        return 'shard_1'
    elif user_id < 10_000_000:
        return 'shard_2'
    else:
        return 'shard_3'
```
- ✓ Range queries fast
- ✗ Uneven distribution (newer users more active)
- ✓ Easy to add shards

**3. Geographic** (data locality):
```python
def get_shard(user_region):
    if user_region in ['US', 'CA', 'MX']:
        return 'shard_americas'
    elif user_region in ['UK', 'DE', 'FR']:
        return 'shard_europe'
    else:
        return 'shard_asia'
```
- ✓ Low latency (data near users)
- ✓ Compliance (GDPR data residency)
- ✗ Uneven load

**Challenges**:
- **Cross-shard JOINs**: Avoid or do in application layer
- **Distributed transactions**: Use sagas or eventual consistency
- **Shard key choice**: Hard to change later!

**When to graduate**: Need multi-datacenter, global scale

---

### Stage 5: Distributed (10M+ users)

**Architecture**:
```
┌──────────────────────────────────┐
│       Load Balancer (Global)     │
└────────┬────────────────┬────────┘
         │                │
    ┌────▼────┐      ┌────▼────┐
    │  US-DC  │      │  EU-DC  │
    └────┬────┘      └────┬────┘
         │                │
    ┌────▼────────────────▼────┐
    │   Distributed Database   │
    │  (CockroachDB, Spanner)  │
    └──────────────────────────┘
```

**Add**:
- Multi-region deployment
- Distributed consensus (Raft, Paxos)
- Global load balancing
- Edge caching (Cloudflare, Fastly)

**Databases for this stage**:
- **CockroachDB**: PostgreSQL-compatible, multi-region
- **YugabyteDB**: PostgreSQL-compatible, Cassandra API
- **Google Spanner**: Globally distributed, strong consistency
- **DynamoDB Global Tables**: Multi-region key-value

---

## Data Storage Selection

### Decision Tree

```
Start here:
│
├─ Need ACID transactions?
│  ├─ Yes → SQL (PostgreSQL, MySQL)
│  └─ No → Continue
│
├─ Need complex queries (JOINs, aggregations)?
│  ├─ Yes → SQL
│  └─ No → Continue
│
├─ Need flexible schema?
│  ├─ Yes → Document DB (MongoDB, Firestore)
│  └─ No → Continue
│
├─ Write-heavy, time-series?
│  ├─ Yes → Wide-column (Cassandra, ClickHouse)
│  └─ No → Continue
│
├─ Need ultra-low latency?
│  ├─ Yes → In-memory (Redis, Memcached)
│  └─ No → Key-Value (DynamoDB, RocksDB)
```

### Storage Comparison

| Database | Best For | Throughput | Consistency | Cost |
|----------|----------|------------|-------------|------|
| **PostgreSQL** | Transactional, complex queries | Medium | Strong | Low |
| **MySQL** | Read-heavy, replication | High reads | Strong | Low |
| **MongoDB** | Flexible schema, rapid iteration | Medium | Eventual | Medium |
| **Cassandra** | Write-heavy, multi-DC | Very high writes | Tunable | Medium |
| **Redis** | Caching, sessions, pub/sub | Very high | Eventually | Low (memory) |
| **DynamoDB** | Serverless, predictable latency | High | Strong/Eventual | Pay-per-request |
| **ClickHouse** | Analytics, OLAP | Very high (columnar) | Eventually | Medium |
| **Elasticsearch** | Full-text search, logs | High | Eventually | Medium-High |

---

## Caching Strategies

### 1. Cache-Aside (Lazy Loading)

**Pattern**: Application manages cache
```python
def get_product(product_id):
    # Check cache
    product = cache.get(f"product:{product_id}")
    if product:
        return product

    # Cache miss: Load from DB
    product = db.query("SELECT * FROM products WHERE id = ?", product_id)

    # Store in cache
    cache.set(f"product:{product_id}", product, ttl=3600)
    return product
```

**Pros**: Simple, cache failures don't break app
**Cons**: Cache miss penalty, stale data possible

### 2. Write-Through

**Pattern**: Update cache and database together
```python
def update_product(product_id, data):
    # Update DB
    db.execute("UPDATE products SET ... WHERE id = ?", data, product_id)

    # Update cache
    cache.set(f"product:{product_id}", data, ttl=3600)
```

**Pros**: Cache always fresh
**Cons**: Write latency (two operations)

### 3. Write-Behind (Write-Back)

**Pattern**: Update cache first, DB asynchronously
```python
def update_product(product_id, data):
    # Update cache immediately
    cache.set(f"product:{product_id}", data)

    # Queue DB update for later
    queue.enqueue('update_product_db', product_id, data)
```

**Pros**: Low write latency
**Cons**: Data loss risk if cache fails before DB write

### 4. Refresh-Ahead

**Pattern**: Refresh cache before expiration
```python
def get_product(product_id):
    product = cache.get(f"product:{product_id}")
    ttl = cache.ttl(f"product:{product_id}")

    # Refresh if TTL < 10% of original
    if ttl < 360:  # 10% of 3600s
        queue.enqueue('refresh_product_cache', product_id)

    return product
```

**Pros**: Reduces cache misses
**Cons**: More complex, refresh overhead

### Cache Invalidation

**Problem**: "There are only two hard things in Computer Science: cache invalidation and naming things."

**Strategies**:

**1. TTL-based** (simplest):
```python
cache.set("user:123", user_data, ttl=300)  # 5 minutes
# Pros: Simple, automatic cleanup
# Cons: May serve stale data for up to 5 minutes
```

**2. Event-based**:
```python
def update_user(user_id, data):
    db.execute("UPDATE users SET ... WHERE id = ?", data, user_id)
    cache.delete(f"user:{user_id}")  # Invalidate immediately

    # Also invalidate derived caches
    cache.delete(f"user:{user_id}:posts")
    cache.delete(f"user:{user_id}:followers")
```

**3. Version-based**:
```python
def get_user(user_id):
    version = db.query("SELECT version FROM users WHERE id = ?", user_id)
    cache_key = f"user:{user_id}:v{version}"

    user = cache.get(cache_key)
    if not user:
        user = db.query("SELECT * FROM users WHERE id = ?", user_id)
        cache.set(cache_key, user, ttl=3600)
    return user

def update_user(user_id, data):
    db.execute("UPDATE users SET version = version + 1, ... WHERE id = ?", data, user_id)
    # Old cache keys naturally expire, no need to delete
```

---

## Message Queues & Async Processing

### When to Use Queues

Use queues for:
- **Decoupling**: Producer and consumer run independently
- **Load leveling**: Handle traffic spikes without overload
- **Reliability**: Retry failed jobs automatically
- **Async processing**: Don't block user requests

### Queue Comparison

| Queue | Best For | Guarantees | Throughput |
|-------|----------|------------|------------|
| **Redis** | Simple queues, fast | At-most-once | Very high |
| **RabbitMQ** | Complex routing, reliability | At-least-once | High |
| **Apache Kafka** | Event streaming, replay | Exactly-once | Very high |
| **AWS SQS** | Serverless, simple | At-least-once | High |
| **Google Pub/Sub** | GCP, fan-out | At-least-once | High |

### Pattern: Task Queue

```python
# Producer (web app)
@app.post('/orders')
def create_order(order_data):
    # Save to DB
    order_id = db.insert("INSERT INTO orders ...", order_data)

    # Enqueue async tasks
    queue.enqueue('send_confirmation_email', order_id)
    queue.enqueue('update_inventory', order_id)
    queue.enqueue('notify_warehouse', order_id)

    # Return immediately
    return {'order_id': order_id, 'status': 'processing'}

# Consumer (worker)
def send_confirmation_email(order_id):
    order = db.query("SELECT * FROM orders WHERE id = ?", order_id)
    email_service.send(order.email, "Order confirmed", template)
```

**Benefits**:
- User gets instant response
- Email failures don't fail order creation
- Can scale workers independently

### Pattern: Event Bus (Pub/Sub)

```python
# Multiple consumers for same event
event_bus.publish('order.created', {
    'order_id': 123,
    'user_id': 456,
    'total': 99.99
})

# Subscriber 1: Email service
@event_bus.subscribe('order.created')
def send_email(event):
    email_service.send(...)

# Subscriber 2: Analytics
@event_bus.subscribe('order.created')
def track_analytics(event):
    analytics.track('Order Created', event)

# Subscriber 3: Inventory
@event_bus.subscribe('order.created')
def update_inventory(event):
    inventory.decrement(...)
```

**Benefits**:
- Loose coupling (services don't know about each other)
- Easy to add new subscribers
- Each service can fail independently

### Retry Strategy

```python
# Exponential backoff with max retries
@queue.job(retry=5, backoff='exponential')
def send_email(order_id):
    # Retry delays: 1s, 2s, 4s, 8s, 16s
    email_service.send(...)

# Dead letter queue for failed jobs
@queue.job(retry=3, on_failure='move_to_dlq')
def process_payment(order_id):
    # After 3 failures, move to DLQ for manual review
    payment_service.charge(...)
```

---

## Data Pipeline Patterns

### ETL (Extract, Transform, Load)

**Use when**: Batch processing, data warehouse

```
┌─────────┐     ┌───────────┐     ┌────────────┐
│ Sources │────►│ Transform │────►│   Target   │
│(DB, API)│     │  (Python) │     │(Warehouse) │
└─────────┘     └───────────┘     └────────────┘
```

**Example: Daily sales report**
```python
# Extract
orders = db.query("SELECT * FROM orders WHERE created_at >= ?", yesterday)
users = db.query("SELECT * FROM users WHERE id IN (?)", order_user_ids)

# Transform
sales_data = []
for order in orders:
    user = users[order.user_id]
    sales_data.append({
        'date': order.created_at.date(),
        'user_region': user.region,
        'total': order.total,
        'category': categorize(order.items)
    })

# Load
warehouse.bulk_insert('daily_sales', sales_data)
```

**Tools**: Apache Airflow, dbt, Luigi

### ELT (Extract, Load, Transform)

**Use when**: Cloud data warehouses with compute power

```
┌─────────┐     ┌────────────┐     ┌───────────┐
│ Sources │────►│   Target   │────►│ Transform │
│(DB, API)│     │(Warehouse) │     │   (SQL)   │
└─────────┘     └────────────┘     └───────────┘
```

**Example**:
```sql
-- 1. Load raw data (just copy)
COPY orders FROM 's3://bucket/orders.csv';

-- 2. Transform in warehouse (fast!)
CREATE TABLE sales_summary AS
SELECT
  DATE(created_at) as date,
  u.region,
  SUM(o.total) as total_sales,
  COUNT(*) as order_count
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE created_at >= CURRENT_DATE - 1
GROUP BY 1, 2;
```

**Benefit**: Leverage warehouse compute, transform at scale

**Tools**: Snowflake, BigQuery, Redshift, dbt

### Streaming (Real-time)

**Use when**: Need low-latency processing

```
┌─────────┐     ┌────────┐     ┌───────────┐
│ Sources │────►│ Kafka  │────►│ Processor │
│(Events) │     │(Buffer)│     │ (Flink)   │
└─────────┘     └────────┘     └───────────┘
```

**Example: Real-time fraud detection**
```python
# Stream processor
stream = kafka.subscribe('transactions')

for transaction in stream:
    # Process each transaction in real-time
    risk_score = fraud_model.predict(transaction)

    if risk_score > 0.8:
        # Flag for review
        alert_service.notify('High risk transaction', transaction)
        db.execute("UPDATE transactions SET status = 'review' WHERE id = ?",
                   transaction.id)
```

**Tools**: Apache Kafka, Flink, Spark Streaming, AWS Kinesis

---

## Monitoring & Observability

### Key Metrics

**Database**:
- **Query latency** (p50, p95, p99)
- **Connection pool utilization**
- **Replication lag** (for replicas)
- **Cache hit rate**
- **Slow query count**

**Queues**:
- **Queue depth** (backlog size)
- **Processing rate** (messages/sec)
- **Error rate**
- **Dead letter queue size**

**Application**:
- **Request throughput** (req/sec)
- **Error rate** (%)
- **Response time** (p95, p99)

### Alerting Thresholds

```yaml
# Example alert rules
alerts:
  - name: HighDatabaseLatency
    condition: db.query.p95 > 200ms for 5 minutes
    severity: warning

  - name: HighReplicationLag
    condition: db.replication_lag > 10s for 2 minutes
    severity: critical

  - name: LowCacheHitRate
    condition: cache.hit_rate < 70% for 10 minutes
    severity: warning

  - name: QueueBacklog
    condition: queue.depth > 10000 for 5 minutes
    severity: warning
```

---

## Migration Strategies

### Database Migration (Zero Downtime)

**1. Dual Writes**:
```python
# Phase 1: Write to both old and new DB
def create_user(data):
    user_id = old_db.insert("INSERT INTO users ...", data)
    new_db.insert("INSERT INTO users ...", data)  # Also write to new
    return user_id

# Phase 2: Backfill historical data
# (Run in background)
for user in old_db.query("SELECT * FROM users"):
    new_db.insert("INSERT INTO users ...", user)

# Phase 3: Read from new DB, verify against old
def get_user(user_id):
    new_user = new_db.query("SELECT * FROM users WHERE id = ?", user_id)
    old_user = old_db.query("SELECT * FROM users WHERE id = ?", user_id)

    if new_user != old_user:
        logger.error("Data mismatch!", user_id=user_id)

    return new_user

# Phase 4: Stop writing to old DB
# Phase 5: Decommission old DB
```

### Resharding

**Problem**: Shard capacity full, need to split

**Strategy: Virtual shards**
```python
# Instead of:
shard = user_id % 4  # Hard to change!

# Use:
virtual_shard = user_id % 1024  # Many virtual shards
physical_shard = shard_map[virtual_shard]  # Map to physical shards

# shard_map initially:
# {0-255: 'shard_1', 256-511: 'shard_2', ...}

# Later, easily rebalance:
# {0-127: 'shard_1', 128-255: 'shard_5', ...}
```

---

## Output Format

When helping with infrastructure scaling:

```
## Current Architecture Analysis

### Bottlenecks Identified
- [Specific bottleneck 1]
- [Specific bottleneck 2]

### Recommended Architecture

[Architecture diagram in text]

### Components to Add
1. [Component]: [Why + how]
2. [Component]: [Why + how]

### Migration Plan

Phase 1: [Description]
- Week 1: [Tasks]
- Week 2: [Tasks]

Phase 2: [Description]
...

### Cost Impact
- Current: $[X]/month
- Projected: $[Y]/month
- ROI: [Justification]

### Risk Mitigation
- Risk 1: [Mitigation]
- Risk 2: [Mitigation]
```

---

## Integration

Works with:
- **scalable-data-schema** - Schema design for scaled infrastructure
- **multi-source-data-conflation** - Merging data from multiple sources
- **data-provenance** - Tracking data lineage in pipelines
- **systems-decompose** - Feature-driven infrastructure planning
