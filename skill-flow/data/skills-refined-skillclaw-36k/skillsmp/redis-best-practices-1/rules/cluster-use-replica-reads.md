---
title: Offload Reads to Replicas
impact: MEDIUM
impactDescription: reduces master load, improves read throughput
tags: cluster, replicas, reads, performance, scaling
---

## Offload Reads to Replicas

Configure reads from replicas to reduce load on masters and improve read throughput. By default, clients read from masters only. Enable replica reads for read-heavy workloads, understanding the eventual consistency trade-off.

**When to Use Replica Reads:**
- Read-heavy workloads (>80% reads)
- Acceptable eventual consistency (milliseconds lag)
- Need to scale read throughput
- Want to reduce master load

**Trade-offs:**
- Eventual consistency: Replicas may be slightly behind
- Stale reads possible during replication lag
- Failover can cause brief unavailability

**Incorrect (all reads from master):**

```python
from redis.cluster import RedisCluster

# Default: all reads go to master
rc = RedisCluster(host='node1', port=6379)

# High read load overwhelms masters
for i in range(100000):
    rc.get(f'key:{i}')  # All hitting masters!
```

```python
# Anti-pattern: Manual replica selection without proper handling
r = redis.Redis(host='replica-host', port=6379)
r.get('key')  # May fail during failover, no automatic discovery
```

**Correct (replica reads with proper configuration):**

```python
from redis.cluster import RedisCluster

# Correct 1: Enable replica reads in cluster
rc = RedisCluster(
    host='node1',
    port=6379,
    decode_responses=True,
    read_from_replicas=True,  # Enable replica reads
)

# Reads automatically distributed to replicas
value = rc.get('key')  # May hit replica

# Correct 2: With Sentinel - separate master/replica clients
from redis.sentinel import Sentinel

sentinel = Sentinel([
    ('sentinel1', 26379),
    ('sentinel2', 26379),
    ('sentinel3', 26379),
])

# Master for writes
master = sentinel.master_for('mymaster', socket_timeout=0.5)

# Replica for reads
replica = sentinel.slave_for('mymaster', socket_timeout=0.5)

def get(key, allow_stale=True):
    """Read with option to use replica"""
    if allow_stale:
        return replica.get(key)
    return master.get(key)

def set(key, value, **kwargs):
    """Writes always go to master"""
    return master.set(key, value, **kwargs)

# Correct 3: Read-your-writes pattern
class ConsistentRedisClient:
    """
    Client that ensures read-your-writes consistency.
    After a write, reads from master briefly.
    """
    def __init__(self, sentinel, master_name):
        self.master = sentinel.master_for(master_name)
        self.replica = sentinel.slave_for(master_name)
        self._recent_writes = {}  # key -> timestamp
        self._consistency_window = 0.1  # 100ms

    def set(self, key, value, **kwargs):
        result = self.master.set(key, value, **kwargs)
        self._recent_writes[key] = time.time()
        return result

    def get(self, key):
        # Check if we recently wrote this key
        write_time = self._recent_writes.get(key, 0)
        if time.time() - write_time < self._consistency_window:
            # Read from master to ensure we see our write
            return self.master.get(key)
        # Safe to read from replica
        return self.replica.get(key)
```

```python
# Correct 4: Monitor replication lag before enabling replica reads
def check_replication_lag(rc):
    """Check replication lag across cluster"""
    nodes = rc.get_nodes()
    lag_info = []

    for node in nodes:
        if node.server_type == 'primary':
            try:
                conn = rc.get_redis_connection(node)
                info = conn.info('replication')

                # Check each replica's lag
                for i in range(info.get('connected_slaves', 0)):
                    replica_info = info.get(f'slave{i}', '')
                    # Parse: ip=x.x.x.x,port=6379,state=online,offset=123,lag=0
                    if 'lag=' in replica_info:
                        lag = int(replica_info.split('lag=')[1].split(',')[0])
                        lag_info.append({
                            'master': f"{node.host}:{node.port}",
                            'replica': i,
                            'lag_seconds': lag
                        })
            except Exception as e:
                pass

    return lag_info

def is_replica_read_safe(max_lag_seconds=1):
    """Check if replica reads are safe (low lag)"""
    lags = check_replication_lag(rc)
    if not lags:
        return False  # No replicas

    max_lag = max(l['lag_seconds'] for l in lags)
    return max_lag <= max_lag_seconds
```

```javascript
// Node.js - ioredis replica reads
const Redis = require('ioredis');

// Cluster with replica reads
const cluster = new Redis.Cluster([
    { host: 'node1', port: 6379 }
], {
    scaleReads: 'slave',  // Read from replicas
    // Or: 'all' to read from both masters and replicas
});

// Reads distributed to replicas
const value = await cluster.get('key');

// Force read from master when needed
const freshValue = await cluster.get('key', (err, result, key, node) => {
    // This callback is called but doesn't help force master
});

// For guaranteed fresh reads, use a separate master-only client
const masterCluster = new Redis.Cluster([
    { host: 'node1', port: 6379 }
], {
    scaleReads: 'master',  // Only read from masters
});

// Sentinel with replica reads
const sentinelRedis = new Redis({
    sentinels: [
        { host: 'sentinel1', port: 26379 }
    ],
    name: 'mymaster',
    role: 'slave',  // Connect to replica
    preferredSlaves: [
        // Prefer specific replicas
        { ip: 'replica1', port: 6379, prio: 1 },
    ]
});
```

```python
# Correct 5: Replica reads with health checking
class HealthAwareReplicaClient:
    """
    Read from replicas only when they're healthy and caught up.
    """
    def __init__(self, sentinel, master_name, max_lag_seconds=1):
        self.sentinel = sentinel
        self.master_name = master_name
        self.max_lag = max_lag_seconds
        self._master = None
        self._replica = None
        self._replica_healthy = True
        self._last_health_check = 0

    @property
    def master(self):
        if not self._master:
            self._master = self.sentinel.master_for(self.master_name)
        return self._master

    @property
    def replica(self):
        if not self._replica:
            self._replica = self.sentinel.slave_for(self.master_name)
        return self._replica

    def _check_replica_health(self):
        """Check if replica is healthy (low lag)"""
        if time.time() - self._last_health_check < 5:  # Cache for 5s
            return self._replica_healthy

        try:
            info = self.master.info('replication')
            for i in range(info.get('connected_slaves', 0)):
                slave_info = info.get(f'slave{i}', '')
                if 'lag=' in slave_info:
                    lag = int(slave_info.split('lag=')[1].split(',')[0])
                    self._replica_healthy = lag <= self.max_lag
                    break
        except:
            self._replica_healthy = False

        self._last_health_check = time.time()
        return self._replica_healthy

    def get(self, key):
        """Read from replica if healthy, else master"""
        if self._check_replica_health():
            try:
                return self.replica.get(key)
            except redis.ConnectionError:
                self._replica_healthy = False
                return self.master.get(key)
        return self.master.get(key)
```

Reference: [Redis Replication](https://redis.io/docs/management/replication/)
