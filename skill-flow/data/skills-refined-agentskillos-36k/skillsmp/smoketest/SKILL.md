---
name: smoketest
description: Run the cache server with the benchmark tool to detect issues
---

Run the cache server with the benchmark tool to detect issues.

## Steps

1. **Build the release binaries** (if not already built):
   ```bash
   cargo build --release -p server -p benchmark
   ```

2. **Kill any existing server** to avoid port conflicts:
   ```bash
   pkill -f crucible-server || true
   sleep 1
   ```

3. **Start the server in the background**:
   ```bash
   ./target/release/crucible-server server/config/smoketest.toml 2>&1 &
   SERVER_PID=$!
   sleep 2
   ```

4. **Verify server is listening** on port 6379:
   ```bash
   nc -z 127.0.0.1 6379
   ```
   If this fails, check the server logs and report the error.

5. **Quick sanity check with redis-cli** (always do this first):
   ```bash
   redis-cli -p 6379 PING
   redis-cli -p 6379 SET smoketest_key smoketest_value
   redis-cli -p 6379 GET smoketest_key
   ```
   These basic commands should work. If they fail, the server has a fundamental issue.

6. **Run the benchmark**:
   ```bash
   ./target/release/crucible-benchmark benchmark/config/quick-test.toml --format verbose
   ```
   Capture the output and check for:
   - Connection errors (should be 0)
   - Timeout errors
   - Unexpected latency spikes (p99.9 > 100ms suggests issues)
   - Hit rate (should be > 0 for this test since we do sets before gets)

7. **Stop the server**:
   ```bash
   kill $SERVER_PID 2>/dev/null || pkill -f crucible-server || true
   ```

8. **Report results**:
   - If benchmark completed successfully with reasonable latencies: PASS
   - If any errors occurred: FAIL with details
   - Include throughput (requests/second) and key latency percentiles (p50, p99, p99.9)

## Success Criteria

The smoketest passes if:
- Server starts without errors
- redis-cli basic commands work (PING, SET, GET)
- Benchmark connects successfully (or redis-benchmark on macOS)
- All requests complete without timeouts
- p99.9 latency is under 100ms (for crucible-benchmark)
- No error messages in output

## Failure Modes to Watch For

- Server crash or panic
- Connection refused errors
- Request timeouts
- Memory allocation failures
- Thread panics
- Protocol parse errors

## Platform Notes

- **Linux**: Full support with io_uring or mio backends. Use crucible-benchmark.
- **macOS**: mio backend only. crucible-benchmark works correctly.

## Optional: Test Different Backends

To test specific backends, use different server configs:
- `server/config/slab.toml` - Slab allocator backend
- `server/config/heap.toml` - Heap allocator backend
- `server/config/redis.toml` - Full Redis-compatible config

Adjust benchmark config if testing memcache protocol:
- `benchmark/config/memcache.toml` - Memcache protocol test
