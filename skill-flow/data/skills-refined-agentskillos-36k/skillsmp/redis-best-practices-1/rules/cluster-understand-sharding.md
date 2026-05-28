---
title: Understand Redis Cluster Hash Slots
impact: HIGH
impactDescription: essential for multi-key operations and scaling
tags: cluster, sharding, hash-slots, scaling
---

## Understand Redis Cluster Hash Slots

Understand how Redis Cluster distributes data across nodes using hash slots. Keys are mapped to one of 16,384 slots, and each node owns a subset. This affects which operations are possible and how to design your key strategy.

**How It Works:**
- 16,384 hash slots total
- Key's slot = CRC16(key) mod 16384
- Each master owns a range of slots
- Data moves by reassigning slots between nodes

**Key Design Impact:**
- Multi-key operations require keys on same node
- Use hash tags `{tag}` to force keys to same slot
- Cross-slot operations fail with CROSSSLOT error

**Incorrect (not understanding slot distribution):**

```python
import redis
from redis.cluster import RedisCluster

rc = RedisCluster(host='node1', port=6379)

# Anti-pattern 1: Multi-key operation without hash tags
rc.mget(['user:1', 'user:2', 'user:3'])  # CROSSSLOT error likely!
# Keys hash to different slots

# Anti-pattern 2: Transaction across slots
pipe = rc.pipeline()
pipe.set('order:123', 'data')
pipe.set('inventory:456', 'data')
pipe.execute()  # CROSSSLOT error if different slots!

# Anti-pattern 3: Lua script with keys on different slots
rc.eval("return redis.call('GET', KEYS[1]) + redis.call('GET', KEYS[2])",
        2, 'counter:a', 'counter:b')  # CROSSSLOT error!

# Anti-pattern 4: SCAN expecting all keys
# SCAN only returns keys on connected node
for key in rc.scan_iter(match='user:*'):
    # Only sees subset of keys!
    pass
```

**Correct (proper cluster-aware design):**

```python
from redis.cluster import RedisCluster

rc = RedisCluster(
    host='node1',
    port=6379,
    decode_responses=True
)

# Correct 1: Use hash tags for related keys
# All keys with same {tag} go to same slot
rc.set('{user:123}:profile', 'profile_data')
rc.set('{user:123}:settings', 'settings_data')
rc.set('{user:123}:session', 'session_data')

# Now multi-key operations work!
rc.mget(['{user:123}:profile', '{user:123}:settings'])

# Correct 2: Transactions with hash tags
pipe = rc.pipeline()
pipe.hset('{order:abc}:details', mapping={'item': 'widget'})
pipe.sadd('{order:abc}:items', 'item1', 'item2')
pipe.execute()  # Works - same hash tag

# Correct 3: Design key patterns for cluster
# Pattern: {entity_type:id}:attribute
def user_keys(user_id):
    """Generate related keys with same hash tag"""
    base = f"{{user:{user_id}}}"
    return {
        'profile': f"{base}:profile",
        'settings': f"{base}:settings",
        'cart': f"{base}:cart",
        'sessions': f"{base}:sessions"
    }

keys = user_keys('123')
# {user:123}:profile, {user:123}:settings - all same slot!

# Correct 4: Check which slot a key uses
def get_key_slot(key):
    """Get the hash slot for a key"""
    # Redis Cluster command
    return rc.cluster_keyslot(key)

# Same hash tag = same slot
assert get_key_slot('{user:123}:a') == get_key_slot('{user:123}:b')

# Correct 5: SCAN across entire cluster
def scan_all_cluster(pattern):
    """Scan all nodes in cluster for keys matching pattern"""
    all_keys = set()

    # Get all master nodes
    nodes = rc.get_nodes()

    for node in nodes:
        if node.server_type == 'primary':  # Only masters have data
            node_client = rc.get_redis_connection(node)
            for key in node_client.scan_iter(match=pattern, count=100):
                all_keys.add(key)

    return all_keys

# Correct 6: Handle CROSSSLOT errors gracefully
def safe_multi_get(keys):
    """Get multiple keys, handling cross-slot case"""
    try:
        return rc.mget(keys)
    except redis.exceptions.ResponseError as e:
        if 'CROSSSLOT' in str(e):
            # Fallback: get keys individually
            return [rc.get(k) for k in keys]
        raise
```

```python
# Correct 7: Atomic operations across related keys
def transfer_inventory(from_warehouse, to_warehouse, item, quantity):
    """
    Transfer inventory between warehouses atomically.
    Uses hash tags to ensure same slot.
    """
    # Keys with same hash tag for atomicity
    from_key = f"{{inventory:{item}}}:{from_warehouse}"
    to_key = f"{{inventory:{item}}}:{to_warehouse}"

    # Lua script works because keys are on same slot
    script = """
    local from_qty = tonumber(redis.call('GET', KEYS[1]) or '0')
    local transfer = tonumber(ARGV[1])

    if from_qty >= transfer then
        redis.call('DECRBY', KEYS[1], transfer)
        redis.call('INCRBY', KEYS[2], transfer)
        return 1
    end
    return 0
    """

    return rc.eval(script, 2, from_key, to_key, quantity)

# Correct 8: Understand slot distribution for capacity planning
def get_cluster_slot_distribution():
    """Get slot distribution across nodes"""
    slots_info = rc.cluster_slots()
    distribution = []

    for slot_range in slots_info:
        start_slot, end_slot = slot_range[0], slot_range[1]
        master = slot_range[2]  # [host, port, node_id]

        distribution.append({
            'start': start_slot,
            'end': end_slot,
            'slots': end_slot - start_slot + 1,
            'master': f"{master[0]}:{master[1]}"
        })

    return distribution
```

```javascript
// Node.js - ioredis Cluster
const Redis = require('ioredis');

const cluster = new Redis.Cluster([
    { host: 'node1', port: 6379 },
    { host: 'node2', port: 6379 },
    { host: 'node3', port: 6379 },
]);

// Use hash tags for related keys
await cluster.set('{user:123}:profile', 'data');
await cluster.set('{user:123}:settings', 'data');

// Multi-key with hash tags
const values = await cluster.mget(
    '{user:123}:profile',
    '{user:123}:settings'
);

// Pipeline with hash tags
const results = await cluster.pipeline()
    .set('{order:abc}:status', 'pending')
    .set('{order:abc}:total', '99.99')
    .exec();
```

Reference: [Redis Cluster Specification](https://redis.io/docs/reference/cluster-spec/)
