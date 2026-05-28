---
title: Track Memory Usage and Trends
impact: HIGH
impactDescription: prevents OOM, enables capacity planning
tags: performance, memory, monitoring, capacity
---

## Track Memory Usage and Trends

Monitor Redis memory usage continuously to prevent OOM situations and plan capacity. Track not just current usage but trends over time to predict when you'll need more capacity.

**Key Metrics to Monitor:**
- `used_memory`: Memory allocated by Redis
- `used_memory_rss`: OS-reported memory (actual memory usage)
- `used_memory_peak`: Historical peak usage
- `maxmemory`: Configured limit
- `mem_fragmentation_ratio`: RSS / used_memory
- `evicted_keys`: Keys removed due to maxmemory

**Incorrect (no memory monitoring):**

```python
# Anti-pattern 1: No memory monitoring
# Only notice memory issues when OOM kills Redis

# Anti-pattern 2: Checking memory only occasionally
def weekly_health_check():
    info = r.info("memory")
    print(f"Memory: {info['used_memory_human']}")
# Too infrequent, can't track trends

# Anti-pattern 3: Only checking used_memory
# Ignoring RSS, fragmentation, and trends
```

**Correct (comprehensive memory monitoring):**

```python
import redis
import time
from datetime import datetime

r = redis.Redis()

# Correct 1: Get comprehensive memory stats
def get_memory_stats():
    """Get all relevant memory statistics"""
    info = r.info("memory")

    stats = {
        # Current usage
        'used_memory': info['used_memory'],
        'used_memory_human': info['used_memory_human'],
        'used_memory_rss': info['used_memory_rss'],
        'used_memory_rss_human': info['used_memory_rss_human'],

        # Peak usage
        'used_memory_peak': info['used_memory_peak'],
        'used_memory_peak_human': info['used_memory_peak_human'],

        # Configuration
        'maxmemory': info.get('maxmemory', 0),
        'maxmemory_human': info.get('maxmemory_human', '0'),
        'maxmemory_policy': info.get('maxmemory_policy', 'noeviction'),

        # Fragmentation
        'mem_fragmentation_ratio': info.get('mem_fragmentation_ratio', 0),
        'mem_fragmentation_bytes': info.get('mem_fragmentation_bytes', 0),

        # Dataset
        'used_memory_dataset': info.get('used_memory_dataset', 0),
        'used_memory_overhead': info.get('used_memory_overhead', 0),

        # Lua
        'used_memory_lua': info.get('used_memory_lua', 0),
        'used_memory_scripts': info.get('used_memory_scripts', 0),
    }

    # Calculate utilization percentage
    if stats['maxmemory'] > 0:
        stats['utilization_pct'] = (stats['used_memory'] / stats['maxmemory']) * 100
    else:
        stats['utilization_pct'] = None

    return stats

# Correct 2: Memory health check with alerts
def check_memory_health():
    """Check memory health and return alerts"""
    stats = get_memory_stats()
    alerts = []

    # Check utilization
    if stats['utilization_pct']:
        if stats['utilization_pct'] > 90:
            alerts.append({
                'severity': 'critical',
                'message': f"Memory at {stats['utilization_pct']:.1f}% - near limit"
            })
        elif stats['utilization_pct'] > 75:
            alerts.append({
                'severity': 'warning',
                'message': f"Memory at {stats['utilization_pct']:.1f}%"
            })
    else:
        alerts.append({
            'severity': 'warning',
            'message': "maxmemory not configured"
        })

    # Check fragmentation
    frag = stats['mem_fragmentation_ratio']
    if frag < 1:
        alerts.append({
            'severity': 'critical',
            'message': f"Fragmentation {frag:.2f} - using swap!"
        })
    elif frag > 1.5:
        alerts.append({
            'severity': 'warning',
            'message': f"High fragmentation: {frag:.2f}"
        })

    return {
        'healthy': len([a for a in alerts if a['severity'] == 'critical']) == 0,
        'alerts': alerts,
        'stats': stats
    }

# Correct 3: Track memory trends over time
class MemoryTrendTracker:
    def __init__(self, redis_client, history_size=1440):
        self.r = redis_client
        self.history = []
        self.history_size = history_size  # 24 hours at 1-minute intervals

    def record(self):
        """Record current memory stats"""
        stats = get_memory_stats()
        self.history.append({
            'timestamp': time.time(),
            'used_memory': stats['used_memory'],
            'used_memory_rss': stats['used_memory_rss'],
            'fragmentation': stats['mem_fragmentation_ratio']
        })

        # Keep bounded history
        if len(self.history) > self.history_size:
            self.history = self.history[-self.history_size:]

    def get_trend(self, minutes=60):
        """Calculate memory growth trend over period"""
        cutoff = time.time() - (minutes * 60)
        recent = [h for h in self.history if h['timestamp'] > cutoff]

        if len(recent) < 2:
            return None

        first = recent[0]['used_memory']
        last = recent[-1]['used_memory']
        duration_hours = (recent[-1]['timestamp'] - recent[0]['timestamp']) / 3600

        growth_rate = (last - first) / duration_hours if duration_hours > 0 else 0

        return {
            'start_memory': first,
            'end_memory': last,
            'growth_bytes': last - first,
            'growth_rate_per_hour': growth_rate,
            'growth_rate_human': f"{growth_rate / 1024 / 1024:.2f} MB/hour"
        }

    def predict_time_to_full(self):
        """Predict when memory will reach maxmemory"""
        stats = get_memory_stats()
        trend = self.get_trend(60)

        if not trend or trend['growth_rate_per_hour'] <= 0:
            return None

        if not stats['maxmemory']:
            return None

        remaining = stats['maxmemory'] - stats['used_memory']
        hours_to_full = remaining / trend['growth_rate_per_hour']

        return {
            'hours_to_full': hours_to_full,
            'estimated_full_time': datetime.fromtimestamp(
                time.time() + hours_to_full * 3600
            ),
            'current_utilization_pct': stats['utilization_pct']
        }
```

```python
# Correct 4: Analyze memory by data type
def analyze_memory_by_type():
    """Sample keys to understand memory distribution by type"""
    type_stats = {}
    sample_size = 1000
    count = 0

    for key in r.scan_iter(count=100):
        if count >= sample_size:
            break

        key_type = r.type(key).decode()
        memory = r.memory_usage(key) or 0

        if key_type not in type_stats:
            type_stats[key_type] = {'count': 0, 'memory': 0, 'samples': []}

        type_stats[key_type]['count'] += 1
        type_stats[key_type]['memory'] += memory
        if len(type_stats[key_type]['samples']) < 5:
            type_stats[key_type]['samples'].append({
                'key': key.decode(),
                'memory': memory
            })

        count += 1

    # Calculate percentages
    total_memory = sum(t['memory'] for t in type_stats.values())
    for t in type_stats.values():
        t['percentage'] = (t['memory'] / total_memory * 100) if total_memory > 0 else 0
        t['avg_memory'] = t['memory'] / t['count'] if t['count'] > 0 else 0

    return type_stats

# Correct 5: Find top memory consumers
def find_large_keys(top_n=20, sample_size=10000):
    """Find largest keys by memory usage"""
    large_keys = []
    count = 0

    for key in r.scan_iter(count=100):
        if count >= sample_size:
            break

        memory = r.memory_usage(key)
        if memory:
            large_keys.append({
                'key': key.decode(),
                'memory': memory,
                'type': r.type(key).decode()
            })

        count += 1

    # Sort by memory and return top N
    large_keys.sort(key=lambda x: x['memory'], reverse=True)
    return large_keys[:top_n]
```

```bash
# CLI commands for memory monitoring

# Get memory info
redis-cli INFO memory

# Memory doctor (recommendations)
redis-cli MEMORY DOCTOR

# Memory stats
redis-cli MEMORY STATS

# Memory usage for specific key
redis-cli MEMORY USAGE mykey

# Get key count
redis-cli DBSIZE

# Debug memory for a key (detailed)
redis-cli DEBUG OBJECT mykey
```

```javascript
// Node.js - Memory monitoring
const Redis = require('ioredis');
const redis = new Redis();

async function getMemoryStats() {
    const info = await redis.info('memory');
    const lines = info.split('\r\n');
    const stats = {};

    lines.forEach(line => {
        const [key, value] = line.split(':');
        if (key && value) {
            stats[key] = value;
        }
    });

    return {
        usedMemory: parseInt(stats.used_memory),
        usedMemoryHuman: stats.used_memory_human,
        maxmemory: parseInt(stats.maxmemory || 0),
        fragmentationRatio: parseFloat(stats.mem_fragmentation_ratio),
    };
}
```

Reference: [Redis MEMORY Commands](https://redis.io/commands/memory-usage/)
