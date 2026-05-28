---
name: redis-expert-best-practices
description: Use this skill for expert-level Redis operations, including caching, data structures, and high-performance key-value management.
---

# Redis Expert Best Practices

Expert guidance for Redis - the in-memory data structure store used as cache, message broker, and database with microsecond latency.

## Core Concepts

### Data Structures
- **Strings**: Binary-safe, up to 512MB, used for simple key-value storage, counters, and caching.
- **Lists**: Linked lists, used for queues and recent items.
- **Sets**: Unordered unique strings, used for unique collections and relationships.
- **Sorted Sets**: Sets ordered by score, used for leaderboards and time-series data.
- **Hashes**: Field-value pairs, more memory-efficient for objects with multiple fields.
- **Streams**: Append-only logs for event streaming and log data.

### Key Features
- In-memory storage with persistence
- Pub/Sub messaging
- Transactions and Lua scripting
- Pipelining for batch operations
- Master-Replica replication for high availability
- Redis Cluster for horizontal scaling

## Best Practices

### Key Naming Conventions
- Use colons as namespace separators.
- Include object type and identifier in key names.
- Keep keys short but descriptive.

```redis
# Good key naming examples
user:1234:profile
order:5678:items
cache:api:products:list
```

### Caching Patterns
- **Cache-Aside Pattern**: Load data into cache only when necessary.
- **Write-Through Pattern**: Update cache immediately after writing to the database.
- **Cache Invalidation**: Use patterns or tags for efficient cache invalidation.

### Expiration and Memory Management
- Always set TTL on cache keys.
- Monitor memory usage and configure max memory policies.

### Transactions and Atomicity
- Use `MULTI/EXEC` for transactions.
- Utilize Lua scripts for complex atomic operations.

### Pub/Sub and Messaging
- Use Redis Pub/Sub for real-time messaging and notifications.

### High Availability
- Implement replication for read scaling.
- Use Redis Sentinel for automatic failover.
- Configure Redis Cluster for horizontal scaling.

### Security
- Require authentication and use TLS for connections.
- Bind to specific interfaces and disable dangerous commands.

## Performance Optimization

### Connection Management
- Use connection pooling and set appropriate timeouts.

### Pipelining
- Use pipelining for batch operations to reduce round trips.

### Avoid KEYS Command
- Use SCAN for large datasets to prevent blocking the server.

## Common Use Cases

### Session Store (Express)
```javascript
import session from 'express-session';
import RedisStore from 'connect-redis';

app.use(
  session({
    store: new RedisStore({ client: redis }),
    secret: 'secret',
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,
      httpOnly: true,
      maxAge: 1000 * 60 * 60 * 24, // 24 hours
    },
  })
);
```

### Job Queue (BullMQ)
```javascript
import { Queue, Worker } from 'bullmq';

const queue = new Queue('emails', { connection: redis });

// Add job
await queue.add('send-email', {
  to: 'user@example.com',
  subject: 'Welcome',
  body: 'Hello!',
});

// Process jobs
const worker = new Worker('emails', async (job) => {
  await sendEmail(job.data);
}, { connection: redis });
```

## Resources
- Redis Documentation: https://redis.io/docs/
- ioredis: https://github.com/redis/ioredis
- Redis University: https://university.redis.com/
- BullMQ: https://docs.bullmq.io/