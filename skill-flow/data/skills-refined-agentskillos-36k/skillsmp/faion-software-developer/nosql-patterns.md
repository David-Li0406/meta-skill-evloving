---
id: nosql-patterns
name: "NoSQL Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# NoSQL Patterns

## Overview

NoSQL databases provide flexible schema design, horizontal scalability, and optimized performance for specific access patterns. This methodology covers data modeling patterns for document stores (MongoDB), key-value stores (Redis), wide-column stores (Cassandra), and graph databases (Neo4j).

## When to Use

- High-volume, high-velocity data with flexible schema requirements
- Hierarchical or nested data structures
- Horizontal scaling requirements beyond traditional RDBMS
- Specific access patterns (time-series, graph traversal, caching)
- Polyglot persistence architectures

## Key Principles

- **Model for queries, not entities**: Design around access patterns
- **Embrace denormalization**: Duplicate data to avoid joins
- **Understand consistency trade-offs**: CAP theorem implications
- **Choose the right tool**: Each NoSQL type excels at different patterns
- **Plan for eventual consistency**: Design idempotent operations

## Best Practices

### MongoDB Document Design

```javascript
// Pattern 1: Embedding for 1:Few relationships
// Good when child data is always accessed with parent
{
  _id: ObjectId("..."),
  name: "John Doe",
  email: "john@example.com",
  addresses: [
    { type: "home", street: "123 Main St", city: "NYC", zip: "10001" },
    { type: "work", street: "456 Office Ave", city: "NYC", zip: "10002" }
  ],
  preferences: {
    theme: "dark",
    notifications: true,
    language: "en"
  }
}

// Pattern 2: Referencing for 1:Many or Many:Many
// Orders collection - reference user, embed items
{
  _id: ObjectId("..."),
  userId: ObjectId("user_id_here"),
  status: "pending",
  items: [
    { productId: ObjectId("..."), name: "Widget", price: 29.99, qty: 2 },
    { productId: ObjectId("..."), name: "Gadget", price: 49.99, qty: 1 }
  ],
  shipping: {
    address: { street: "123 Main St", city: "NYC" },
    method: "express",
    cost: 9.99
  },
  totals: {
    subtotal: 109.97,
    tax: 8.80,
    shipping: 9.99,
    total: 128.76
  },
  createdAt: ISODate("2024-01-15T10:30:00Z")
}

// Pattern 3: Bucket pattern for time-series
// Store multiple measurements in one document
{
  sensorId: "temp-001",
  date: ISODate("2024-01-15"),
  measurements: [
    { ts: ISODate("2024-01-15T00:00:00Z"), value: 22.5 },
    { ts: ISODate("2024-01-15T00:05:00Z"), value: 22.7 },
    // ... up to ~200 measurements per document
  ],
  summary: {
    count: 288,
    min: 21.2,
    max: 24.8,
    avg: 22.9
  }
}
```

### MongoDB Indexing

```javascript
// Compound index for common query pattern
db.orders.createIndex({ userId: 1, createdAt: -1 });

// Partial index for active records only
db.orders.createIndex(
  { createdAt: 1 },
  { partialFilterExpression: { status: "pending" } }
);

// Text index for search
db.products.createIndex({ name: "text", description: "text" });

// TTL index for automatic expiration
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 });

// Wildcard index for flexible schema
db.logs.createIndex({ "metadata.$**": 1 });
```

### Redis Data Structures

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# String - Simple caching
r.setex("user:123:profile", 3600, json.dumps(user_data))
profile = json.loads(r.get("user:123:profile"))

# Hash - Object storage
r.hset("user:123", mapping={
    "name": "John Doe",
    "email": "john@example.com",
    "login_count": 42
})
r.hincrby("user:123", "login_count", 1)

# List - Queue/Stack
r.lpush("task:queue", json.dumps(task))  # Add to queue
task = r.brpop("task:queue", timeout=30)  # Blocking pop

# Set - Unique collections
r.sadd("user:123:tags", "premium", "verified", "beta")
r.sismember("user:123:tags", "premium")  # Check membership
r.sinter("user:123:tags", "user:456:tags")  # Common tags

# Sorted Set - Leaderboards, time-series
r.zadd("leaderboard", {"player1": 1500, "player2": 1200})
r.zincrby("leaderboard", 50, "player1")  # Add points
top_10 = r.zrevrange("leaderboard", 0, 9, withscores=True)

# Sorted Set - Rate limiting
def is_rate_limited(user_id: str, limit: int = 100, window: int = 60) -> bool:
    key = f"ratelimit:{user_id}"
    now = time.time()

    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, now - window)
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, window)
    results = pipe.execute()

    return results[2] > limit
```

### Redis Pub/Sub and Streams

```python
# Pub/Sub for real-time messaging
def publisher():
    r.publish("notifications", json.dumps({
        "type": "order_update",
        "order_id": "123",
        "status": "shipped"
    }))

def subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe("notifications")
    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            handle_notification(data)

# Streams for event sourcing
# Add event to stream
r.xadd("orders:events", {
    "type": "order_created",
    "order_id": "123",
    "user_id": "456",
    "total": "99.99"
})

# Consumer group for distributed processing
r.xgroup_create("orders:events", "order-processors", id="0", mkstream=True)

# Read as consumer
events = r.xreadgroup(
    groupname="order-processors",
    consumername="worker-1",
    streams={"orders:events": ">"},
    count=10,
    block=5000
)
```

### Cassandra Wide-Column Patterns

```cql
-- Time-series with partition key strategy
CREATE TABLE sensor_readings (
    sensor_id text,
    date date,
    timestamp timestamp,
    value double,
    PRIMARY KEY ((sensor_id, date), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

-- Query: Get latest readings for sensor on specific date
SELECT * FROM sensor_readings
WHERE sensor_id = 'temp-001' AND date = '2024-01-15'
LIMIT 100;

-- User activity with time-bucketed partitions
CREATE TABLE user_activity (
    user_id uuid,
    year_month text,  -- '2024-01'
    activity_time timestamp,
    activity_type text,
    details map<text, text>,
    PRIMARY KEY ((user_id, year_month), activity_time)
) WITH CLUSTERING ORDER BY (activity_time DESC);

-- Materialized view for different access pattern
CREATE MATERIALIZED VIEW activity_by_type AS
    SELECT * FROM user_activity
    WHERE activity_type IS NOT NULL
    PRIMARY KEY ((activity_type, year_month), activity_time, user_id);
```

### Graph Database (Neo4j) Patterns

```cypher
// Create nodes and relationships
CREATE (u:User {id: '123', name: 'John', email: 'john@example.com'})
CREATE (p:Product {id: 'prod-1', name: 'Widget', price: 29.99})
CREATE (u)-[:PURCHASED {date: date('2024-01-15'), quantity: 2}]->(p)

// Find products purchased by user's friends
MATCH (user:User {id: '123'})-[:FRIEND]->(friend:User)-[:PURCHASED]->(product:Product)
WHERE NOT (user)-[:PURCHASED]->(product)
RETURN DISTINCT product.name, COUNT(friend) as friend_count
ORDER BY friend_count DESC
LIMIT 10

// Recommendation engine: Users who bought X also bought Y
MATCH (u:User)-[:PURCHASED]->(p1:Product {id: 'prod-1'})
MATCH (u)-[:PURCHASED]->(p2:Product)
WHERE p1 <> p2
RETURN p2.name, COUNT(*) as co_purchases
ORDER BY co_purchases DESC
LIMIT 5

// Shortest path between users
MATCH path = shortestPath(
    (a:User {id: '123'})-[:FRIEND*..6]-(b:User {id: '456'})
)
RETURN path
```

## Anti-patterns

- **Using NoSQL as relational**: Forcing joins and normalization
- **Unbounded arrays**: Documents growing indefinitely
- **Missing indexes on query fields**: Causes collection scans
- **Hot partitions**: Poor partition key selection in Cassandra
- **Ignoring consistency requirements**: Using eventual consistency for critical data
- **Over-embedding**: Creating massive documents that exceed size limits
- **Not planning for schema evolution**: No versioning strategy

## References

- [MongoDB Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)
- [Redis Data Types](https://redis.io/docs/data-types/)
- [Cassandra Data Modeling](https://cassandra.apache.org/doc/latest/cassandra/data_modeling/)
- [Neo4j Graph Patterns](https://neo4j.com/docs/getting-started/data-modeling/)
