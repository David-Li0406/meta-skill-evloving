---
title: Use Sentinel for High Availability
impact: HIGH
impactDescription: automatic failover, prevents single point of failure
tags: cluster, sentinel, high-availability, failover
---

## Use Sentinel for High Availability

Use Redis Sentinel for high availability when you don't need data sharding. Sentinel monitors Redis instances, performs automatic failover, and provides service discovery. It's simpler than Redis Cluster when all data fits on one machine.

**Sentinel vs Cluster:**
- **Sentinel**: HA without sharding, simpler, data fits on one node
- **Cluster**: HA with sharding, more complex, data exceeds one node

**Sentinel Provides:**
- Monitoring: Checks if master and replicas are working
- Notification: Alerts on failures
- Automatic failover: Promotes replica to master
- Service discovery: Clients query Sentinel for current master

**Incorrect (no HA or misconfigured):**

```bash
# Anti-pattern 1: Single Redis instance in production
# No Sentinel, no replicas
# If Redis crashes, complete outage

# Anti-pattern 2: Single Sentinel
sentinel monitor mymaster 127.0.0.1 6379 1
# Single Sentinel can't form quorum if it fails
# Need at least 3 Sentinels

# Anti-pattern 3: Sentinel quorum too low
sentinel monitor mymaster 127.0.0.1 6379 1  # quorum of 1
# Single Sentinel can trigger failover
# Risk of split-brain scenarios
```

```python
# Anti-pattern: Connecting directly to master without Sentinel
import redis
r = redis.Redis(host='redis-master', port=6379)  # Hardcoded master
# If master fails and Sentinel promotes replica, client still points to dead node
```

**Correct (proper Sentinel setup):**

```bash
# Correct 1: Minimum 3 Sentinel nodes for quorum
# sentinel1.conf
sentinel monitor mymaster 192.168.1.10 6379 2  # quorum of 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1

# Sentinel authentication (Redis 6.0+)
sentinel auth-pass mymaster your-redis-password
requirepass your-sentinel-password

# sentinel2.conf and sentinel3.conf - same configuration
```

```bash
# Redis master configuration
# redis-master.conf
port 6379
requirepass your-redis-password
masterauth your-redis-password  # For replica promotion

# Redis replica configuration
# redis-replica.conf
port 6379
replicaof 192.168.1.10 6379
masterauth your-redis-password
requirepass your-redis-password
replica-read-only yes
```

```python
import redis
from redis.sentinel import Sentinel

# Correct 2: Connect through Sentinel for automatic failover
sentinel = Sentinel(
    [
        ('sentinel1.example.com', 26379),
        ('sentinel2.example.com', 26379),
        ('sentinel3.example.com', 26379),
    ],
    socket_timeout=0.5,
    sentinel_kwargs={'password': 'sentinel-password'}  # If Sentinel has auth
)

# Get master connection (auto-discovers current master)
master = sentinel.master_for(
    'mymaster',
    socket_timeout=0.5,
    password='redis-password',
    retry_on_timeout=True
)

# Get replica for read operations
replica = sentinel.slave_for(
    'mymaster',
    socket_timeout=0.5,
    password='redis-password'
)

# Write to master
master.set('key', 'value')

# Read from replica (eventual consistency)
value = replica.get('key')

# Correct 3: Handle failover transparently
def get_with_failover(key):
    """Get value, automatically handling failover"""
    try:
        return master.get(key)
    except redis.ConnectionError:
        # Sentinel will automatically reconnect to new master
        # on next request
        raise

# Correct 4: Check Sentinel status
def check_sentinel_status():
    """Check Sentinel cluster health"""
    for sentinel_host, sentinel_port in sentinel.sentinels:
        try:
            s = redis.Redis(host=sentinel_host, port=sentinel_port)
            info = s.sentinel_master('mymaster')
            print(f"Sentinel {sentinel_host}: Master is {info['ip']}:{info['port']}")
        except Exception as e:
            print(f"Sentinel {sentinel_host} error: {e}")
```

```python
# Correct 5: Full application setup with Sentinel
class RedisSentinelClient:
    def __init__(self, sentinel_hosts, master_name, password=None, sentinel_password=None):
        self.sentinel = Sentinel(
            sentinel_hosts,
            socket_timeout=0.5,
            sentinel_kwargs={'password': sentinel_password} if sentinel_password else {}
        )
        self.master_name = master_name
        self.password = password

    @property
    def master(self):
        """Get master connection for writes"""
        return self.sentinel.master_for(
            self.master_name,
            socket_timeout=0.5,
            password=self.password,
            retry_on_timeout=True,
            max_connections=50
        )

    @property
    def replica(self):
        """Get replica connection for reads"""
        return self.sentinel.slave_for(
            self.master_name,
            socket_timeout=0.5,
            password=self.password,
            max_connections=50
        )

    def get(self, key, use_replica=True):
        """Read operation (from replica by default)"""
        client = self.replica if use_replica else self.master
        return client.get(key)

    def set(self, key, value, **kwargs):
        """Write operation (always to master)"""
        return self.master.set(key, value, **kwargs)

    def get_master_info(self):
        """Get current master info"""
        return self.sentinel.discover_master(self.master_name)

    def get_replica_info(self):
        """Get replica info"""
        return self.sentinel.discover_slaves(self.master_name)

# Usage
client = RedisSentinelClient(
    sentinel_hosts=[
        ('sentinel1', 26379),
        ('sentinel2', 26379),
        ('sentinel3', 26379),
    ],
    master_name='mymaster',
    password='redis-password',
    sentinel_password='sentinel-password'
)

client.set('user:123', 'data')
value = client.get('user:123')
```

```javascript
// Node.js with ioredis Sentinel support
const Redis = require('ioredis');

const redis = new Redis({
    sentinels: [
        { host: 'sentinel1', port: 26379 },
        { host: 'sentinel2', port: 26379 },
        { host: 'sentinel3', port: 26379 },
    ],
    name: 'mymaster',  // Master name
    password: 'redis-password',
    sentinelPassword: 'sentinel-password',
    enableReadyCheck: true,
    maxRetriesPerRequest: 3,
});

redis.on('ready', () => console.log('Connected to master'));
redis.on('+switch-master', () => console.log('Master switched'));
redis.on('error', (err) => console.error('Redis error:', err));

// Use normally - ioredis handles failover
await redis.set('key', 'value');
const value = await redis.get('key');
```

Reference: [Redis Sentinel](https://redis.io/docs/management/sentinel/)
