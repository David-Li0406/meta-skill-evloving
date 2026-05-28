---
title: Use redis-benchmark Correctly
impact: MEDIUM
impactDescription: enables proper performance testing and capacity planning
tags: performance, benchmark, testing, capacity
---

## Use redis-benchmark Correctly

Use redis-benchmark properly for performance testing and capacity planning. Incorrect benchmarking leads to wrong conclusions. Understand what the tool measures and how to interpret results.

**What redis-benchmark Measures:**
- Raw Redis throughput (ops/sec)
- Latency distribution
- Best-case performance (pipelining, small payloads)

**What It Doesn't Measure:**
- Real application patterns
- Network across data centers
- Complex queries or Lua scripts
- Mixed workload patterns

**Incorrect (misleading benchmarks):**

```bash
# Anti-pattern 1: Default benchmark without understanding
redis-benchmark
# Uses pipelining, small payloads - not realistic

# Anti-pattern 2: Comparing different configurations unfairly
# Benchmark A: pipelining enabled, single key
# Benchmark B: no pipelining, random keys
# Results are not comparable!

# Anti-pattern 3: Not considering payload size
redis-benchmark -t set,get
# Uses tiny default payloads - not representative if your data is larger

# Anti-pattern 4: Testing on same machine as Redis
redis-benchmark -h localhost
# No network latency - unrealistic for production
```

**Correct (meaningful benchmarks):**

```bash
# Correct 1: Baseline benchmark with common options
redis-benchmark \
    -h redis.example.com \
    -p 6379 \
    -a password \
    -c 50 \         # 50 concurrent connections
    -n 100000 \     # 100K requests
    -d 256 \        # 256 byte payload
    --threads 4 \   # Multi-threaded (Redis 6.0+)
    -q              # Quiet mode (summary only)

# Correct 2: Realistic no-pipelining test
redis-benchmark \
    -h redis.example.com \
    -c 50 \
    -n 100000 \
    -P 1 \          # No pipelining (1 command at a time)
    -d 256 \
    -t set,get,lpush,lpop,hset

# Correct 3: Test specific commands
redis-benchmark -t set -n 100000 -d 1024  # SET with 1KB payload
redis-benchmark -t get -n 100000          # GET
redis-benchmark -t lpush,lpop -n 100000   # List operations
redis-benchmark -t hset -n 100000         # Hash operations
redis-benchmark -t sadd,spop -n 100000    # Set operations
redis-benchmark -t zadd,zrange -n 100000  # Sorted Set operations

# Correct 4: Test with realistic key patterns
redis-benchmark \
    -c 50 \
    -n 100000 \
    -r 100000 \     # Random keys from 100K key space
    -d 512 \
    -t set,get

# Correct 5: Compare with and without pipelining
echo "=== Without pipelining ==="
redis-benchmark -c 50 -n 100000 -P 1 -t set -q

echo "=== With pipelining (10 commands) ==="
redis-benchmark -c 50 -n 100000 -P 10 -t set -q

echo "=== With pipelining (50 commands) ==="
redis-benchmark -c 50 -n 100000 -P 50 -t set -q

# Correct 6: Latency focused test
redis-benchmark \
    -c 1 \          # Single connection
    -n 10000 \
    -P 1 \
    -d 256 \
    --csv           # CSV output for analysis
```

```python
# Correct 7: Application-specific benchmarks
import redis
import time
import statistics
import concurrent.futures

r = redis.Redis(host='redis.example.com', port=6379)

def benchmark_operation(name, func, iterations=10000):
    """Benchmark a specific operation"""
    latencies = []

    start_total = time.perf_counter()
    for i in range(iterations):
        start = time.perf_counter()
        func(i)
        latencies.append((time.perf_counter() - start) * 1000)
    total_time = time.perf_counter() - start_total

    latencies.sort()
    return {
        'name': name,
        'iterations': iterations,
        'total_time_sec': total_time,
        'ops_per_sec': iterations / total_time,
        'avg_ms': statistics.mean(latencies),
        'min_ms': min(latencies),
        'max_ms': max(latencies),
        'p50_ms': latencies[len(latencies) // 2],
        'p95_ms': latencies[int(len(latencies) * 0.95)],
        'p99_ms': latencies[int(len(latencies) * 0.99)],
    }

# Benchmark your actual access patterns
def run_application_benchmark():
    results = []

    # String cache pattern
    results.append(benchmark_operation(
        'cache_set',
        lambda i: r.setex(f'cache:{i}', 3600, 'x' * 256)
    ))

    results.append(benchmark_operation(
        'cache_get',
        lambda i: r.get(f'cache:{i % 1000}')  # Hot keys
    ))

    # Session pattern
    results.append(benchmark_operation(
        'session_hset',
        lambda i: r.hset(f'session:{i}', mapping={'user': 'john', 'token': 'xyz'})
    ))

    results.append(benchmark_operation(
        'session_hgetall',
        lambda i: r.hgetall(f'session:{i % 1000}')
    ))

    # Rate limiter pattern
    results.append(benchmark_operation(
        'rate_limit',
        lambda i: (r.incr(f'ratelimit:{i % 100}'),
                   r.expire(f'ratelimit:{i % 100}', 60))
    ))

    # Pipeline pattern
    def pipeline_ops(i):
        pipe = r.pipeline()
        for j in range(10):
            pipe.get(f'key:{i * 10 + j}')
        pipe.execute()

    results.append(benchmark_operation(
        'pipeline_10_gets',
        pipeline_ops,
        iterations=1000
    ))

    return results

# Correct 8: Concurrent benchmark
def concurrent_benchmark(operations, num_workers=10, per_worker=1000):
    """Run benchmark with concurrent workers"""
    def worker(worker_id):
        results = []
        for i in range(per_worker):
            start = time.perf_counter()
            operations(worker_id * per_worker + i)
            results.append(time.perf_counter() - start)
        return results

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker, i) for i in range(num_workers)]
        all_latencies = []
        for f in concurrent.futures.as_completed(futures):
            all_latencies.extend(f.result())
    total_time = time.perf_counter() - start

    all_latencies = [l * 1000 for l in all_latencies]  # to ms
    all_latencies.sort()

    return {
        'total_ops': len(all_latencies),
        'total_time_sec': total_time,
        'ops_per_sec': len(all_latencies) / total_time,
        'avg_ms': statistics.mean(all_latencies),
        'p99_ms': all_latencies[int(len(all_latencies) * 0.99)],
    }

# Usage
result = concurrent_benchmark(
    lambda i: r.get(f'key:{i % 10000}'),
    num_workers=20,
    per_worker=5000
)
print(f"Concurrent throughput: {result['ops_per_sec']:.0f} ops/sec")
```

```bash
# Correct 9: Interpret benchmark results

# Sample output:
# SET: 125000.00 requests per second, p50=0.199 msec
#
# Interpretation:
# - 125K ops/sec is raw throughput
# - Real application will be lower due to:
#   - Application logic overhead
#   - No pipelining
#   - Larger payloads
#   - Network latency
#   - Connection pool overhead

# Good benchmark checklist:
# [ ] Test from a client machine, not Redis server
# [ ] Use realistic payload sizes
# [ ] Test with expected concurrency
# [ ] Compare with and without pipelining
# [ ] Test your actual command patterns
# [ ] Run multiple times for consistency
# [ ] Consider warm-up period
```

Reference: [redis-benchmark](https://redis.io/docs/management/optimization/benchmarks/)
