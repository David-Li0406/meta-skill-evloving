---
title: Use Colon-Separated Key Namespacing
impact: CRITICAL
impactDescription: enables organization, scanning, and multi-tenancy
tags: keys, naming, organization, patterns
---

## Use Colon-Separated Key Namespacing

Use colons (`:`) to create hierarchical key namespaces. This convention enables logical organization, efficient pattern scanning, and clear separation between different data types and entities.

**Naming Convention Pattern:**
```
object-type:id:field
tenant:object-type:id
service:environment:object-type:id
```

**Incorrect (flat or inconsistent naming):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No namespace - collisions likely
r.set("123", "John Doe")  # What is 123? User? Order? Product?
r.set("settings", "{...}")  # Whose settings?

# Anti-pattern 2: Inconsistent separators
r.set("user_123_profile", "{...}")
r.set("user-123-sessions", "{...}")
r.set("user.123.preferences", "{...}")
# Cannot use SCAN patterns effectively

# Anti-pattern 3: Verbose redundant naming
r.set("application_myapp_production_user_data_user_id_123", "{...}")
# Wastes memory, hard to read

# Anti-pattern 4: No object type prefix
r.set("123:profile", "{...}")
r.set("123:orders", "{...}")
# Is 123 a user? customer? merchant?
```

**Correct (consistent colon-separated namespacing):**

```python
import redis
r = redis.Redis()

# Pattern: object-type:id[:field]
r.hset("user:123", mapping={"name": "John", "email": "john@example.com"})
r.set("user:123:session", "session_token_abc")
r.sadd("user:123:roles", "admin", "editor")
r.zadd("user:123:activity", {"login": 1704067200})

# Pattern: object-type:id for relationships
r.sadd("user:123:followers", "user:456", "user:789")
r.sadd("user:123:following", "user:456")

# Multi-tenant pattern: tenant:object-type:id
r.hset("tenant:acme:user:123", mapping={"name": "John"})
r.hset("tenant:globex:user:123", mapping={"name": "Jane"})

# Service/environment pattern
r.set("myapp:prod:config:feature_flags", "{...}")
r.set("myapp:staging:config:feature_flags", "{...}")

# Scan by pattern (find all users)
for key in r.scan_iter(match="user:*", count=100):
    print(key)

# Scan tenant-specific data
for key in r.scan_iter(match="tenant:acme:*", count=100):
    print(key)

# Delete all sessions for a user (carefully!)
for key in r.scan_iter(match="user:123:session:*"):
    r.delete(key)
```

```python
# Real-world examples of good key naming

# E-commerce application
"product:12345"                      # Product hash
"product:12345:inventory"            # Stock count
"product:12345:reviews"              # Review list
"category:electronics:products"       # Set of product IDs
"cart:user:789"                      # Shopping cart hash
"order:abc123"                       # Order hash
"order:abc123:items"                 # Order line items

# Session management
"session:token:xyz789"               # Session data
"session:user:123:tokens"            # Set of user's session tokens

# Caching with versioning
"cache:v1:user:123:profile"          # Versioned cache key
"cache:v2:user:123:profile"          # New cache version

# Rate limiting
"ratelimit:api:user:123"             # Per-user rate limit
"ratelimit:api:ip:192.168.1.1"       # Per-IP rate limit

# Feature flags
"feature:dark_mode:enabled"          # Global feature
"feature:dark_mode:users"            # Set of users with feature
"feature:dark_mode:percentage"       # Rollout percentage

# Queues
"queue:emails:pending"               # Pending email jobs
"queue:emails:processing"            # Jobs being processed
"queue:emails:failed"                # Failed jobs for retry
```

```javascript
// Node.js - Key naming utilities
const redis = require('redis');
const client = redis.createClient();

// Helper function for consistent key generation
function key(...parts) {
    return parts.join(':');
}

// Usage
const userKey = key('user', userId);                    // "user:123"
const sessionKey = key('user', userId, 'session');      // "user:123:session"
const tenantKey = key('tenant', tenantId, 'user', id);  // "tenant:acme:user:123"

await client.hSet(key('user', '123'), { name: 'John' });
await client.set(key('user', '123', 'session'), 'token');
```

Reference: [Redis Key Naming Conventions](https://redis.io/docs/manual/patterns/)
