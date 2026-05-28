---
name: redis-expert-best-practices
description: Use this skill when you need expert guidance on Redis for caching, data structures, and high-performance applications, along with best practices for effective usage.
---

# Redis Expert and Best Practices

Expert guidance for Redis - the in-memory data structure store used as cache, message broker, and database with microsecond latency. This skill combines core concepts and best practices for effective Redis usage.

## Core Concepts

### Data Structures
- **Strings**: Binary-safe, up to 512MB, used for simple key-value storage, counters, and caching.
- **Lists**: Linked lists, ideal for queues, recent items, and activity feeds.
- **Sets**: Unordered unique strings, useful for unique collections and relationships.
- **Sorted Sets**: Sets ordered by score, great for leaderboards.
- **Hashes**: Field-value pairs, more memory-efficient for objects with multiple fields.
- **Streams**: Append-only log for real-time data.
- **Bitmaps and HyperLogLog**: For advanced data manipulation.
- **Geospatial indexes**: For location-based queries.

### Key Features
- In-memory storage with persistence
- Pub/Sub messaging
- Transactions
- Lua scripting
- Pipelining
- Master-Replica replication
- Redis Sentinel (high availability)
- Redis Cluster (horizontal scaling)

### Use Cases
- Caching layer
- Session storage
- Real-time analytics
- Message queues
- Rate limiting
- Leaderboards
- Geospatial queries

## Best Practices

### Core Principles
- Use Redis for caching, session storage, real-time analytics, and message queuing.
- Choose appropriate data structures for your use case.
- Implement proper key naming conventions and expiration policies.
- Design for high availability and persistence requirements.
- Monitor memory usage and optimize for performance.

### Key Naming Conventions
- Use colons as namespace separators.
- Include object type and identifier in key names.
- Keep keys short but descriptive.
- Use consistent naming patterns across your application.

#### Good Key Naming Examples
- `user:1234:profile`
- `order:5678:items`
- `cache:api:products:list`
- `queue:email:pending`

## Installation and Configuration

### Docker Setup
```bash
# Development
docker run --name redis -p 6379:6379 -d redis:7-alpine

# Production with persistence
docker run --name redis \
  -p 6379:6379 \
  -v redis-data:/data \
  -d redis:7-alpine \
  redis-server --appendonly yes --requirepass strongpassword

# Redis with config file
docker run --name redis \
  -p 6379:6379 \
  -v ./redis.conf:/usr/local/etc/redis/redis.conf \
  -d redis:7-alpine \
  redis-server /usr/local/etc/redis/redis.conf
```

### Configuration (redis.conf)
```conf
# Network
bind 0.0.0.0
port 6379
protected-mode yes

# Security
requirepass strongpassword

# Memory
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1      # Save after 900s if 1 key changed
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# Replication
replica-read-only yes
```

## Node.js Client (ioredis)

### Basic Operations
```typescript
import Redis from 'ioredis';

const redis = new Redis({
  host: 'localhost',
  port: 6379,
  password: 'strongpassword',
});

// Strings
await redis.set('user:1000:name', 'Alice');
await redis.get('user:1000:name');
```