---
title: Use INFO Command for Comprehensive Stats
impact: MEDIUM
impactDescription: single source for all Redis metrics
tags: performance, monitoring, info, metrics
---

## Use INFO Command for Comprehensive Stats

Use the INFO command to gather comprehensive statistics about Redis server state. INFO provides data on memory, clients, replication, CPU, keyspace, and more - essential for monitoring and debugging.

**INFO Sections:**
- `server`: General server info (version, uptime, etc.)
- `clients`: Connected clients info
- `memory`: Memory usage and stats
- `persistence`: RDB/AOF status
- `stats`: General statistics (ops/sec, etc.)
- `replication`: Master/replica info
- `cpu`: CPU consumption
- `cluster`: Cluster state
- `keyspace`: Database statistics

**Incorrect (not using INFO effectively):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No monitoring at all
# Running Redis with no visibility into metrics

# Anti-pattern 2: Only checking PING
def health_check_bad():
    return r.ping()  # Tells you nothing about memory, clients, etc.

# Anti-pattern 3: Manual queries for stats
def get_stats_bad():
    # Querying multiple sources instead of INFO
    key_count = r.dbsize()
    # Missing memory, ops/sec, replication status, etc.
    return {"keys": key_count}
```

**Correct (using INFO effectively):**

```python
import redis
r = redis.Redis()

# Correct 1: Get all INFO sections
def get_all_info():
    """Get complete INFO output"""
    return r.info()

# Correct 2: Get specific section
def get_memory_info():
    return r.info("memory")

def get_stats_info():
    return r.info("stats")

def get_replication_info():
    return r.info("replication")

# Correct 3: Build a comprehensive dashboard
def get_redis_dashboard():
    """Get key metrics for monitoring dashboard"""
    server = r.info("server")
    clients = r.info("clients")
    memory = r.info("memory")
    stats = r.info("stats")
    replication = r.info("replication")
    persistence = r.info("persistence")

    return {
        # Server
        'version': server.get('redis_version'),
        'uptime_days': server.get('uptime_in_days'),
        'uptime_seconds': server.get('uptime_in_seconds'),

        # Clients
        'connected_clients': clients.get('connected_clients'),
        'blocked_clients': clients.get('blocked_clients'),
        'max_clients': clients.get('maxclients'),

        # Memory
        'used_memory_human': memory.get('used_memory_human'),
        'used_memory_peak_human': memory.get('used_memory_peak_human'),
        'maxmemory_human': memory.get('maxmemory_human'),
        'mem_fragmentation_ratio': memory.get('mem_fragmentation_ratio'),

        # Operations
        'total_commands_processed': stats.get('total_commands_processed'),
        'instantaneous_ops_per_sec': stats.get('instantaneous_ops_per_sec'),
        'total_connections_received': stats.get('total_connections_received'),

        # Cache performance
        'keyspace_hits': stats.get('keyspace_hits'),
        'keyspace_misses': stats.get('keyspace_misses'),
        'hit_rate': calculate_hit_rate(stats),

        # Replication
        'role': replication.get('role'),
        'connected_slaves': replication.get('connected_slaves'),
        'master_link_status': replication.get('master_link_status'),

        # Persistence
        'rdb_last_save_time': persistence.get('rdb_last_save_time'),
        'rdb_last_bgsave_status': persistence.get('rdb_last_bgsave_status'),
        'aof_enabled': persistence.get('aof_enabled'),
        'aof_last_write_status': persistence.get('aof_last_write_status'),

        # Eviction
        'evicted_keys': stats.get('evicted_keys'),
        'expired_keys': stats.get('expired_keys'),
    }

def calculate_hit_rate(stats):
    """Calculate cache hit rate"""
    hits = stats.get('keyspace_hits', 0)
    misses = stats.get('keyspace_misses', 0)
    total = hits + misses
    return (hits / total * 100) if total > 0 else 0

# Correct 4: Monitor ops/sec over time
class OpsMonitor:
    def __init__(self, redis_client):
        self.r = redis_client
        self.last_total = None
        self.last_time = None

    def get_ops_per_sec(self):
        """Calculate actual ops/sec between calls"""
        stats = self.r.info("stats")
        current_total = stats.get('total_commands_processed', 0)
        current_time = time.time()

        if self.last_total is None:
            self.last_total = current_total
            self.last_time = current_time
            return stats.get('instantaneous_ops_per_sec', 0)

        elapsed = current_time - self.last_time
        ops = current_total - self.last_total

        self.last_total = current_total
        self.last_time = current_time

        return ops / elapsed if elapsed > 0 else 0

# Correct 5: Check replication health
def check_replication_health():
    """Check replication status and lag"""
    info = r.info("replication")
    role = info.get('role')

    if role == 'master':
        slaves = info.get('connected_slaves', 0)
        slave_info = []
        for i in range(slaves):
            slave_data = info.get(f'slave{i}', '')
            # Parse: ip=x.x.x.x,port=6379,state=online,offset=123,lag=0
            if slave_data:
                parts = dict(p.split('=') for p in slave_data.split(','))
                slave_info.append(parts)

        return {
            'role': 'master',
            'connected_slaves': slaves,
            'slaves': slave_info
        }
    else:
        return {
            'role': 'replica',
            'master_host': info.get('master_host'),
            'master_port': info.get('master_port'),
            'master_link_status': info.get('master_link_status'),
            'master_last_io_seconds_ago': info.get('master_last_io_seconds_ago'),
            'slave_read_repl_offset': info.get('slave_read_repl_offset'),
        }

# Correct 6: Get keyspace statistics
def get_keyspace_stats():
    """Get per-database key counts and expiry info"""
    info = r.info("keyspace")
    databases = {}

    for db, data in info.items():
        # data is like: {'keys': 1234, 'expires': 100, 'avg_ttl': 3600000}
        databases[db] = {
            'keys': data.get('keys', 0),
            'expires': data.get('expires', 0),
            'avg_ttl_ms': data.get('avg_ttl', 0),
            'pct_with_expiry': (data.get('expires', 0) / data.get('keys', 1)) * 100
        }

    return databases
```

```bash
# CLI commands for INFO

# Full info
redis-cli INFO

# Specific section
redis-cli INFO memory
redis-cli INFO stats
redis-cli INFO replication
redis-cli INFO clients

# One-liner metrics
redis-cli INFO stats | grep instantaneous_ops
redis-cli INFO memory | grep used_memory_human
redis-cli INFO clients | grep connected_clients

# Watch ops/sec in real-time
watch -n 1 'redis-cli INFO stats | grep instantaneous_ops'
```

```python
# Correct 7: Export metrics to monitoring system
def export_prometheus_metrics():
    """Format metrics for Prometheus scraping"""
    dashboard = get_redis_dashboard()

    metrics = [
        f'redis_connected_clients {dashboard["connected_clients"]}',
        f'redis_blocked_clients {dashboard["blocked_clients"]}',
        f'redis_used_memory_bytes {r.info("memory")["used_memory"]}',
        f'redis_ops_per_sec {dashboard["instantaneous_ops_per_sec"]}',
        f'redis_keyspace_hits_total {dashboard["keyspace_hits"]}',
        f'redis_keyspace_misses_total {dashboard["keyspace_misses"]}',
        f'redis_evicted_keys_total {dashboard["evicted_keys"]}',
        f'redis_expired_keys_total {dashboard["expired_keys"]}',
        f'redis_mem_fragmentation_ratio {dashboard["mem_fragmentation_ratio"]}',
    ]

    return '\n'.join(metrics)
```

Reference: [Redis INFO Command](https://redis.io/commands/info/)
