# Hypothesis Examples

Reference examples demonstrating well-formed hypotheses and falsification plans.

## Example 1: API Timeout

**Symptom**: Intermittent 504 errors on `/api/orders` endpoint during peak hours.

### H1: Database Connection Pool Exhaustion

**Claim**: The connection pool reaches its limit during high load, causing queries to queue beyond the gateway timeout.

**Plausibility**: High — Correlates with traffic patterns; pool size unchanged since last scaling.

**Prediction**: If true, connection pool metrics will show saturation (active = max) during 504 occurrences.

| Step | Action | Expected Negative Result |
|------|--------|--------------------------|
| 1 | Query `pg_stat_activity` during peak, count active connections | Active connections < pool max during 504 window |
| 2 | Cross-reference APM traces for blocked acquisition attempts | No connection acquisition delays in traces |

**Confidence**: Decisive. Pool exhaustion leaves clear metrics; absence disproves.

### H2: Slow Query on Order Lookup

**Claim**: A specific query (`SELECT * FROM orders WHERE user_id = ?`) lacks an index and degrades under load.

**Plausibility**: Medium — Query plan not recently reviewed; table size grew 3x this quarter.

**Prediction**: If true, `EXPLAIN ANALYZE` shows sequential scan with cost proportional to table size.

| Step | Action | Expected Negative Result |
|------|--------|--------------------------|
| 1 | Run `EXPLAIN ANALYZE` on the query with representative user_id | Index scan present, execution time < 50ms |
| 2 | Check `pg_stat_user_tables` for sequential scan count on orders | seq_scan count not increasing during incident window |

**Confidence**: High. Index usage is binary and observable.

---

## Example 2: Flaky Unit Test

**Symptom**: `test_process_payment` fails ~10% of CI runs with assertion error on `status == 'completed'`.

### H1: Race Condition in Async Handler

**Claim**: The test asserts before the async payment callback completes, causing intermittent assertion failure.

**Plausibility**: High — Test uses `asyncio.create_task` without explicit await on callback.

**Prediction**: If true, adding a deterministic wait or mock eliminates flakiness entirely.

| Step | Action | Expected Negative Result |
|------|--------|--------------------------|
| 1 | Instrument test with explicit `await callback_complete` event | Flakiness persists with same failure rate |
| 2 | Replace async call with synchronous mock | Flakiness persists |

**Confidence**: Decisive. Eliminating async timing removes the race condition variable.

### H2: Shared Mutable State Between Tests

**Claim**: A previous test mutates a module-level variable that `test_process_payment` depends on, and test ordering varies.

**Plausibility**: Medium — Test suite uses `pytest-randomly`; no explicit fixtures for state reset.

**Prediction**: If true, running the test in isolation always passes; failure correlates with specific predecessor tests.

| Step | Action | Expected Negative Result |
|------|--------|--------------------------|
| 1 | Run `pytest test_payment.py::test_process_payment -x --count=100` in isolation | At least one failure in isolation |
| 2 | Identify predecessor test from failed CI log, run sequence locally | Sequence passes; no state leakage observable |

**Confidence**: High. Isolation testing is straightforward and deterministic.

---

## Example 3: Memory Leak in Long-Running Service

**Symptom**: Heap usage grows linearly over 72 hours until OOM kill.

### H1: Unbounded Cache Growth

**Claim**: The LRU cache for session tokens has no max size, accumulating entries indefinitely.

**Plausibility**: High — Cache instantiated without `maxsize` parameter; session volume is high.

**Prediction**: If true, cache length correlates with heap growth; setting maxsize arrests growth.

| Step | Action | Expected Negative Result |
|------|--------|--------------------------|
| 1 | Log `len(session_cache)` hourly; correlate with heap metrics | Cache size stable while heap grows |
| 2 | Deploy with `maxsize=10000`; monitor heap over 72h | Heap growth continues at same rate |

**Confidence**: High if correlation is absent. Moderate if maxsize deployment still leaks (other caches may exist).

### H2: Circular References Preventing GC

**Claim**: Objects in the request handler form reference cycles that the garbage collector cannot collect in time.

**Plausibility**: Low — Python's GC handles cycles; would need custom `__del__` or weak reference misuse.

**Prediction**: If true, forcing GC with `gc.collect()` periodically reduces heap growth.

| Step | Action | Expected Negative Result |
|------|--------|--------------------------|
| 1 | Add `gc.collect()` call after each request; monitor heap | Heap growth unchanged |
| 2 | Profile with `objgraph` to identify cycle roots | No unexpected reference cycles found |

**Confidence**: Moderate. Absence of cycles is suggestive but not definitive if cycles are transient.
