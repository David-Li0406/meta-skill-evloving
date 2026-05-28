---
title: Handle MOVED and ASK Redirects
impact: MEDIUM-HIGH
impactDescription: required for cluster operations and resharding
tags: cluster, redirects, moved, ask, resharding
---

## Handle MOVED and ASK Redirects

Understand and properly handle MOVED and ASK redirects in Redis Cluster. These redirects tell clients to contact a different node for a key. Most client libraries handle this automatically, but understanding them helps debugging and performance tuning.

**Redirect Types:**
- **MOVED**: Slot permanently moved to another node (update client's slot map)
- **ASK**: Slot being migrated, ask target node once (don't update map)

**When They Occur:**
- MOVED: After resharding completes, client's slot map is stale
- ASK: During active resharding, key being migrated

**Incorrect (not handling redirects):**

```python
import redis

# Anti-pattern 1: Using regular Redis client for cluster
r = redis.Redis(host='node1', port=6379)
r.get('key')  # Gets MOVED error, doesn't know how to handle

# Anti-pattern 2: Not refreshing slot map
# Client has stale slot information
# Gets MOVED errors repeatedly, poor performance

# Anti-pattern 3: Ignoring redirect errors
try:
    r.get('key')
except redis.ResponseError as e:
    pass  # Silently fails, data not retrieved
```

**Correct (proper redirect handling):**

```python
from redis.cluster import RedisCluster

# Correct 1: Use cluster-aware client (handles redirects automatically)
rc = RedisCluster(
    host='node1',
    port=6379,
    decode_responses=True,
    # Automatically handle MOVED/ASK
    skip_full_coverage_check=True,  # For clusters not covering all 16384 slots
)

# Operations just work - client handles redirects
rc.get('key')  # If MOVED, client updates slot map and retries
rc.set('key', 'value')  # Automatic redirect handling

# Correct 2: Monitor redirect frequency (indicates resharding or stale map)
def get_cluster_redirect_stats():
    """Check if there are many redirects (indicates issues)"""
    # Note: This varies by client library
    # redis-py-cluster tracks some stats internally
    nodes = rc.get_nodes()
    stats = []

    for node in nodes:
        try:
            info = rc.get_redis_connection(node).info('stats')
            stats.append({
                'node': f"{node.host}:{node.port}",
                'total_commands': info.get('total_commands_processed', 0),
            })
        except:
            pass

    return stats

# Correct 3: Force slot map refresh after known topology change
def refresh_cluster_slots():
    """Refresh the client's slot mapping"""
    # Most clients do this automatically on MOVED
    rc.cluster_slots()  # Fetches current slot mapping

# Correct 4: Handle resharding gracefully
def get_with_retry(key, max_retries=3):
    """Get with explicit redirect handling for debugging"""
    for attempt in range(max_retries):
        try:
            return rc.get(key)
        except redis.exceptions.ResponseError as e:
            error_msg = str(e)
            if 'MOVED' in error_msg:
                # Slot permanently moved - client should update mapping
                print(f"MOVED redirect (attempt {attempt + 1})")
                # redis-py-cluster handles this automatically
                continue
            elif 'ASK' in error_msg:
                # Slot being migrated - need to ASK target node
                print(f"ASK redirect during migration (attempt {attempt + 1})")
                continue
            elif 'CLUSTERDOWN' in error_msg:
                # Cluster is down or in failed state
                print("Cluster is down!")
                raise
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")
```

```python
# Correct 5: Manual redirect handling (for custom clients)
def handle_redirect_manually(command, *args):
    """
    Example of manual redirect handling.
    Most clients do this automatically.
    """
    import re

    try:
        # Try executing on current node
        return current_node.execute_command(command, *args)

    except redis.ResponseError as e:
        error = str(e)

        # Handle MOVED: -MOVED 3999 127.0.0.1:6381
        if error.startswith('MOVED'):
            match = re.match(r'MOVED (\d+) ([\w.]+):(\d+)', error)
            if match:
                slot, host, port = match.groups()
                # Update slot mapping
                update_slot_map(int(slot), host, int(port))
                # Retry on correct node
                target_node = get_node(host, int(port))
                return target_node.execute_command(command, *args)

        # Handle ASK: -ASK 3999 127.0.0.1:6381
        elif error.startswith('ASK'):
            match = re.match(r'ASK (\d+) ([\w.]+):(\d+)', error)
            if match:
                slot, host, port = match.groups()
                # Don't update slot map (migration in progress)
                target_node = get_node(host, int(port))
                # Must send ASKING before the command
                target_node.execute_command('ASKING')
                return target_node.execute_command(command, *args)

        raise
```

```javascript
// Node.js - ioredis handles redirects automatically
const Redis = require('ioredis');

const cluster = new Redis.Cluster([
    { host: 'node1', port: 6379 }
], {
    // Redirect handling options
    maxRedirections: 16,  // Max redirects before giving up
    retryDelayOnClusterDown: 100,  // Wait before retry when cluster down
    retryDelayOnFailover: 100,  // Wait during failover
    retryDelayOnTryAgain: 100,  // Wait on TRYAGAIN error

    // Refresh slot mapping
    slotsRefreshTimeout: 2000,
    slotsRefreshInterval: 5000,  // Periodic refresh
});

// Events for monitoring
cluster.on('ready', () => console.log('Cluster ready'));
cluster.on('node error', (err, node) => {
    console.log(`Node ${node.options.host}:${node.options.port} error:`, err);
});
cluster.on('refresh', () => console.log('Slot mapping refreshed'));

// Operations automatically follow redirects
await cluster.set('key', 'value');
const value = await cluster.get('key');
```

```python
# Correct 6: Monitor cluster health during resharding
def check_cluster_health():
    """Check if cluster is healthy or resharding"""
    try:
        cluster_info = rc.cluster_info()
        state = cluster_info.get('cluster_state')

        result = {
            'state': state,
            'healthy': state == 'ok',
            'slots_assigned': cluster_info.get('cluster_slots_assigned'),
            'slots_ok': cluster_info.get('cluster_slots_ok'),
            'slots_pfail': cluster_info.get('cluster_slots_pfail'),
            'slots_fail': cluster_info.get('cluster_slots_fail'),
            'known_nodes': cluster_info.get('cluster_known_nodes'),
        }

        # Check for migrating slots (resharding in progress)
        nodes = rc.get_nodes()
        migrating = 0
        importing = 0

        for node in nodes:
            try:
                node_info = rc.get_redis_connection(node).cluster_nodes()
                migrating += node_info.count('migrating')
                importing += node_info.count('importing')
            except:
                pass

        result['resharding_in_progress'] = migrating > 0 or importing > 0

        return result

    except Exception as e:
        return {'healthy': False, 'error': str(e)}
```

Reference: [Redis Cluster Redirections](https://redis.io/docs/reference/cluster-spec/#redirection-and-resharding)
