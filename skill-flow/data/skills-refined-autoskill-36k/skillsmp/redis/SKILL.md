---
name: redis
description: Redis in-memory data structure store commands including key operations, hashes, pub/sub, streams, and clustering.
---

# Redis — Key Operations

**Basic Commands**
```bash
redis-cli
SET key "value"
GET key
DEL key
EXPIRE key 60  # TTL in seconds
```

**Hashes**
```bash
HSET user:1000 name "John" age 30
HGETALL user:1000
```

**Publish/Subscribe**
```bash
# Terminal 1:
SUBSCRIBE channel

# Terminal 2:
PUBLISH channel "message"
```

## Redis — Advanced Patterns

**Streams**
```bash
# Producer:
XADD mystream * sensor-id 1234 temp 19.8

# Consumer:
XREAD BLOCK 0 STREAMS mystream $
```

**Lua Scripting**
```bash
eval "return redis.call('GET', KEYS[1])..ARGV[1]" 1 mykey _suffix
```

**Cluster Management**
```bash
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001
redis-cli --cluster check 127.0.0.1:7000
```