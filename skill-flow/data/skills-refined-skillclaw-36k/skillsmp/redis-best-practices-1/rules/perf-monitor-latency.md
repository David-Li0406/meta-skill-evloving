---
title: Track and Diagnose Latency Issues
impact: HIGH
impactDescription: identifies latency sources, enables optimization
tags: performance, latency, monitoring, debugging
---

## Track and Diagnose Latency Issues

Monitor and diagnose Redis latency to ensure responsive applications. Latency can come from network, slow commands, persistence operations, or memory issues. Use Redis's built-in latency monitoring tools.

**Common Latency Sources:**
- Network round-trip time
- Slow commands (see SLOWLOG)
- Persistence (BGSAVE, AOF rewrites)
- Memory operations (swapping, fragmentation)
- Cluster redirections
- Client connection issues

**Latency Metrics:**
- P50, P99, P99.9 latencies
- Operations per second
- Command execution time
- Network latency

**Incorrect (ignoring latency issues):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No latency monitoring
def get_data(key):
    return r.get(key)  # No visibility into latency
# Latency issues go undetected until users complain

# Anti-pattern 2: Only checking average latency
def check_latency_bad():
    latencies = [measure_one() for _ in range(10)]
    print(f"Average: {sum(latencies)/len(latencies)}ms")
# Misses P99 spikes that affect user experience

# Anti-pattern 3: Not using Redis latency tools
# Manually timing without SLOWLOG or LATENCY commands
```

**Correct (comprehensive latency monitoring):**

```python
import redis
import time
import statistics

r = redis.Redis()

# Correct 1: Measure round-trip latency
def measure_latency(samples=100):
    """Measure ping latency to Redis"""
    latencies = []

    for _ in range(samples):
        start = time.perf_counter()
        r.ping()
        elapsed = (time.perf_counter() - start) * 1000  # ms
        latencies.append(elapsed)

    latencies.sort()

    return {
        'samples': samples,
        'min_ms': min(latencies),
        'max_ms': max(latencies),
        'avg_ms': statistics.mean(latencies),
        'median_ms': statistics.median(latencies),
        'p95_ms': latencies[int(samples * 0.95)],
        'p99_ms': latencies[int(samples * 0.99)],
        'stddev_ms': statistics.stdev(latencies) if samples > 1 else 0
    }

# Correct 2: Use Redis latency monitoring
def enable_latency_monitor(threshold_ms=100):
    """Enable Redis latency monitor for events exceeding threshold"""
    # Set threshold in milliseconds
    r.config_set('latency-monitor-threshold', threshold_ms)

def get_latency_history():
    """Get latency history for all event types"""
    try:
        # LATENCY HISTORY returns [timestamp, latency_ms] pairs
        events = ['command', 'fast-command', 'fork', 'aof-fsync-always',
                  'aof-write', 'aof-write-pending-fsync', 'rdb-unlink-temp-file']

        history = {}
        for event in events:
            try:
                data = r.execute_command('LATENCY', 'HISTORY', event)
                if data:
                    history[event] = [
                        {'timestamp': ts, 'latency_ms': lat}
                        for ts, lat in data
                    ]
            except:
                pass

        return history
    except:
        return {}

def get_latency_latest():
    """Get latest latency spike for each event type"""
    try:
        data = r.execute_command('LATENCY', 'LATEST')
        results = []
        for entry in data:
            if len(entry) >= 4:
                results.append({
                    'event': entry[0].decode() if isinstance(entry[0], bytes) else entry[0],
                    'timestamp': entry[1],
                    'latest_latency_ms': entry[2],
                    'max_latency_ms': entry[3]
                })
        return results
    except:
        return []

def get_latency_doctor():
    """Get latency doctor analysis"""
    try:
        report = r.execute_command('LATENCY', 'DOCTOR')
        return report.decode() if isinstance(report, bytes) else report
    except:
        return "Latency doctor not available"

# Correct 3: Continuous latency monitoring
class LatencyMonitor:
    def __init__(self, redis_client, window_size=1000):
        self.r = redis_client
        self.latencies = []
        self.window_size = window_size
        self.alerts = []

    def record_operation(self, operation_func):
        """Measure and record operation latency"""
        start = time.perf_counter()
        result = operation_func()
        latency = (time.perf_counter() - start) * 1000

        self.latencies.append({
            'timestamp': time.time(),
            'latency_ms': latency
        })

        # Keep bounded window
        if len(self.latencies) > self.window_size:
            self.latencies = self.latencies[-self.window_size:]

        # Alert on high latency
        if latency > 100:  # 100ms threshold
            self.alerts.append({
                'timestamp': time.time(),
                'latency_ms': latency
            })

        return result

    def get_stats(self):
        """Get latency statistics"""
        if not self.latencies:
            return None

        lats = [l['latency_ms'] for l in self.latencies]
        lats.sort()

        return {
            'count': len(lats),
            'min': min(lats),
            'max': max(lats),
            'avg': statistics.mean(lats),
            'p50': lats[len(lats) // 2],
            'p95': lats[int(len(lats) * 0.95)],
            'p99': lats[int(len(lats) * 0.99)],
        }

# Correct 4: Diagnose latency sources
def diagnose_latency():
    """Comprehensive latency diagnosis"""
    diagnosis = {
        'issues': [],
        'recommendations': []
    }

    # Check SLOWLOG
    slow_commands = r.slowlog_get(10)
    if slow_commands:
        avg_slow = sum(c['duration'] for c in slow_commands) / len(slow_commands) / 1000
        diagnosis['slow_commands'] = {
            'count': len(slow_commands),
            'avg_duration_ms': avg_slow
        }
        if avg_slow > 100:
            diagnosis['issues'].append(f"Slow commands averaging {avg_slow:.1f}ms")
            diagnosis['recommendations'].append("Review SLOWLOG and optimize slow commands")

    # Check memory
    mem_info = r.info("memory")
    frag = mem_info.get('mem_fragmentation_ratio', 1)
    if frag < 1:
        diagnosis['issues'].append("Memory fragmentation < 1: Using swap!")
        diagnosis['recommendations'].append("Add more memory or reduce dataset")
    elif frag > 1.5:
        diagnosis['issues'].append(f"Memory fragmentation: {frag:.2f}")
        diagnosis['recommendations'].append("Enable active defragmentation")

    # Check persistence
    persistence = r.info("persistence")
    if persistence.get('aof_rewrite_in_progress'):
        diagnosis['issues'].append("AOF rewrite in progress")
    if persistence.get('rdb_bgsave_in_progress'):
        diagnosis['issues'].append("RDB save in progress")

    # Check clients
    clients = r.info("clients")
    blocked = clients.get('blocked_clients', 0)
    if blocked > 10:
        diagnosis['issues'].append(f"{blocked} blocked clients")
        diagnosis['recommendations'].append("Check for blocking operations")

    # Network latency
    latency = measure_latency(10)
    diagnosis['network_latency'] = latency
    if latency['p99_ms'] > 10:
        diagnosis['issues'].append(f"Network P99 latency: {latency['p99_ms']:.1f}ms")

    return diagnosis
```

```bash
# CLI commands for latency monitoring

# Enable latency monitoring (threshold in ms)
redis-cli CONFIG SET latency-monitor-threshold 100

# Get latest latency events
redis-cli LATENCY LATEST

# Get latency history for specific event
redis-cli LATENCY HISTORY command

# Get doctor's analysis
redis-cli LATENCY DOCTOR

# Reset latency data
redis-cli LATENCY RESET

# Intrinsic latency test (run on Redis server)
redis-cli --intrinsic-latency 60  # Test for 60 seconds

# Continuous latency monitor
redis-cli --latency

# Latency distribution
redis-cli --latency-dist

# Latency history
redis-cli --latency-history
```

```python
# Correct 5: Track latency by command type
def benchmark_commands():
    """Measure latency for different command types"""
    results = {}

    # String operations
    results['SET'] = measure_operation(lambda: r.set('bench:key', 'value'))
    results['GET'] = measure_operation(lambda: r.get('bench:key'))

    # Hash operations
    r.hset('bench:hash', mapping={'a': '1', 'b': '2'})
    results['HGET'] = measure_operation(lambda: r.hget('bench:hash', 'a'))
    results['HGETALL'] = measure_operation(lambda: r.hgetall('bench:hash'))

    # List operations
    r.rpush('bench:list', *range(100))
    results['LRANGE'] = measure_operation(lambda: r.lrange('bench:list', 0, -1))

    # Cleanup
    r.delete('bench:key', 'bench:hash', 'bench:list')

    return results

def measure_operation(func, iterations=100):
    """Measure operation latency"""
    latencies = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        latencies.append((time.perf_counter() - start) * 1000)

    latencies.sort()
    return {
        'avg_ms': statistics.mean(latencies),
        'p50_ms': latencies[len(latencies) // 2],
        'p99_ms': latencies[int(len(latencies) * 0.99)]
    }
```

Reference: [Redis Latency Monitoring](https://redis.io/docs/management/optimization/latency-monitor/)
