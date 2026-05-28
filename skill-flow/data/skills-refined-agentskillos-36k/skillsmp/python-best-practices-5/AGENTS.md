# Python >=3.11

**Version 0.1.0**  
Python Community  
January 2026

> **Note:**  
> This document is mainly for agents and LLMs to follow when maintaining,  
> generating, or refactoring codebases. Humans may also find it useful,  
> but guidance here is optimized for automation and consistency by AI-assisted workflows.

---

## Abstract

Comprehensive performance optimization guide for Python >=3.11 applications, designed for AI agents and LLMs. Contains 45 rules across 9 categories, prioritized by impact from critical (I/O patterns, async concurrency) to incremental (runtime tuning). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific impact metrics to guide automated refactoring and code generation.

---

## Table of Contents

1. [I/O Patterns](#1-io-patterns) — **CRITICAL**
   - 1.1 [Batch Database Operations to Reduce Round Trips](#11-batch-database-operations-to-reduce-round-trips)
   - 1.2 [Stream Large Files Instead of Loading Into Memory](#12-stream-large-files-instead-of-loading-into-memory)
   - 1.3 [Use Async File I/O for Non-Blocking Operations](#13-use-async-file-io-for-non-blocking-operations)
   - 1.4 [Use Buffered I/O for Frequent Small Writes](#14-use-buffered-io-for-frequent-small-writes)
   - 1.5 [Use Connection Pooling for Database and HTTP Clients](#15-use-connection-pooling-for-database-and-http-clients)
2. [Async Concurrency](#2-async-concurrency) — **CRITICAL**
   - 2.1 [Avoid Async Overhead for CPU-Bound Work](#21-avoid-async-overhead-for-cpu-bound-work)
   - 2.2 [Avoid Blocking Calls in Async Code](#22-avoid-blocking-calls-in-async-code)
   - 2.3 [Store References to Fire-and-Forget Tasks](#23-store-references-to-fire-and-forget-tasks)
   - 2.4 [Use asyncio.gather() for Independent Operations](#24-use-asynciogather-for-independent-operations)
   - 2.5 [Use Semaphores for Concurrency Limiting](#25-use-semaphores-for-concurrency-limiting)
   - 2.6 [Use TaskGroup for Structured Concurrency](#26-use-taskgroup-for-structured-concurrency)
3. [Memory Management](#3-memory-management) — **HIGH**
   - 3.1 [Avoid Intermediate Lists in Pipelines](#31-avoid-intermediate-lists-in-pipelines)
   - 3.2 [Leverage String Interning for Repeated Strings](#32-leverage-string-interning-for-repeated-strings)
   - 3.3 [Preallocate Lists When Size is Known](#33-preallocate-lists-when-size-is-known)
   - 3.4 [Use __slots__ for Memory-Efficient Classes](#34-use-slots-for-memory-efficient-classes)
   - 3.5 [Use Generators for Lazy Evaluation](#35-use-generators-for-lazy-evaluation)
   - 3.6 [Use Weak References for Caches and Observers](#36-use-weak-references-for-caches-and-observers)
4. [Data Structures](#4-data-structures) — **HIGH**
   - 4.1 [Use Counter for Frequency Counting](#41-use-counter-for-frequency-counting)
   - 4.2 [Use deque for O(1) Queue Operations](#42-use-deque-for-o1-queue-operations)
   - 4.3 [Use dict.get() with Default Instead of KeyError Handling](#43-use-dictget-with-default-instead-of-keyerror-handling)
   - 4.4 [Use NamedTuple for Immutable Lightweight Records](#44-use-namedtuple-for-immutable-lightweight-records)
   - 4.5 [Use Set for O(1) Membership Testing](#45-use-set-for-o1-membership-testing)
5. [Algorithm Efficiency](#5-algorithm-efficiency) — **MEDIUM-HIGH**
   - 5.1 [Cache Expensive Computations in Loops](#51-cache-expensive-computations-in-loops)
   - 5.2 [Use Built-in Functions Over Manual Implementation](#52-use-built-in-functions-over-manual-implementation)
   - 5.3 [Use itertools for Efficient Iteration Patterns](#53-use-itertools-for-efficient-iteration-patterns)
   - 5.4 [Use List Comprehensions Over Manual Loops](#54-use-list-comprehensions-over-manual-loops)
   - 5.5 [Use Local Variables in Hot Loops](#55-use-local-variables-in-hot-loops)
   - 5.6 [Use str.join() for String Concatenation](#56-use-strjoin-for-string-concatenation)
6. [Concurrency Model](#6-concurrency-model) — **MEDIUM**
   - 6.1 [Choose the Right Concurrency Model](#61-choose-the-right-concurrency-model)
   - 6.2 [Minimize Lock Contention in Threaded Code](#62-minimize-lock-contention-in-threaded-code)
   - 6.3 [Use asyncio.Queue for Producer-Consumer Patterns](#63-use-asyncioqueue-for-producer-consumer-patterns)
   - 6.4 [Use Chunking for ProcessPoolExecutor](#64-use-chunking-for-processpoolexecutor)
   - 6.5 [Use Thread-Safe Data Structures for Shared State](#65-use-thread-safe-data-structures-for-shared-state)
7. [Serialization](#7-serialization) — **MEDIUM**
   - 7.1 [Avoid Pickle for Untrusted Data](#71-avoid-pickle-for-untrusted-data)
   - 7.2 [Use MessagePack for Compact Binary Serialization](#72-use-messagepack-for-compact-binary-serialization)
   - 7.3 [Use orjson for High-Performance JSON](#73-use-orjson-for-high-performance-json)
   - 7.4 [Use Pydantic for Validated Deserialization](#74-use-pydantic-for-validated-deserialization)
8. [Caching and Memoization](#8-caching-and-memoization) — **LOW-MEDIUM**
   - 8.1 [Avoid Over-Caching Low-Value Operations](#81-avoid-over-caching-low-value-operations)
   - 8.2 [Implement TTL for Time-Sensitive Caches](#82-implement-ttl-for-time-sensitive-caches)
   - 8.3 [Use cached_property for Expensive Computed Attributes](#83-use-cachedproperty-for-expensive-computed-attributes)
   - 8.4 [Use lru_cache for Expensive Pure Functions](#84-use-lrucache-for-expensive-pure-functions)
9. [Runtime Tuning](#9-runtime-tuning) — **LOW**
   - 9.1 [Avoid Repeated Global and Module Lookups](#91-avoid-repeated-global-and-module-lookups)
   - 9.2 [Minimize Exception Handling in Hot Paths](#92-minimize-exception-handling-in-hot-paths)
   - 9.3 [Profile Before Optimizing](#93-profile-before-optimizing)
   - 9.4 [Upgrade to Python 3.11+ for Free Performance](#94-upgrade-to-python-311-for-free-performance)

---

## 1. I/O Patterns

**Impact: CRITICAL**

I/O is the #1 bottleneck for Python services. Blocking I/O serializes otherwise parallelizable work, wasting CPU cycles waiting for network and disk.

### 1.1 Batch Database Operations to Reduce Round Trips

**Impact: CRITICAL (N round trips to 1, 10-100× improvement for bulk operations)**

Each database query incurs network latency. Batching multiple operations into a single query eliminates N-1 round trips and reduces connection overhead.

**Incorrect (N database round trips):**

```python
async def update_user_statuses(user_ids: list[int], status: str):
    for user_id in user_ids:
        await db.execute(
            "UPDATE users SET status = $1 WHERE id = $2",
            status, user_id
        )  # 1000 users = 1000 round trips
```

**Correct (1 database round trip):**

```python
async def update_user_statuses(user_ids: list[int], status: str):
    await db.execute(
        "UPDATE users SET status = $1 WHERE id = ANY($2)",
        status, user_ids
    )  # 1000 users = 1 round trip
```

**Alternative (bulk insert with executemany):**

```python
async def insert_orders(orders: list[Order]):
    await db.executemany(
        "INSERT INTO orders (user_id, total) VALUES ($1, $2)",
        [(o.user_id, o.total) for o in orders]
    )
```

Reference: [asyncpg documentation](https://magicstack.github.io/asyncpg/current/)

### 1.2 Stream Large Files Instead of Loading Into Memory

**Impact: CRITICAL (O(1) memory instead of O(n), prevents OOM errors)**

Loading entire files into memory for processing causes memory spikes and potential OOM errors. Stream files line-by-line or in chunks to maintain constant memory usage.

**Incorrect (loads entire file into memory):**

```python
def process_log_file(filepath: str) -> int:
    with open(filepath, "r") as f:
        lines = f.readlines()  # 10GB file = 10GB+ memory
    return sum(1 for line in lines if "ERROR" in line)
```

**Correct (streams line by line, O(1) memory):**

```python
def process_log_file(filepath: str) -> int:
    error_count = 0
    with open(filepath, "r") as f:
        for line in f:  # File object is an iterator
            if "ERROR" in line:
                error_count += 1
    return error_count
```

**Alternative (chunked binary reading):**

```python
def calculate_checksum(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):  # 8KB chunks
            hasher.update(chunk)
    return hasher.hexdigest()
```

Reference: [Python I/O documentation](https://docs.python.org/3/tutorial/inputoutput.html)

### 1.3 Use Async File I/O for Non-Blocking Operations

**Impact: CRITICAL (eliminates blocking waits, 80% latency reduction)**

Synchronous file operations block the event loop, preventing other coroutines from running. Use `aiofiles` or similar libraries for async file I/O to maintain concurrency.

**Incorrect (blocks event loop during file read):**

```python
async def process_config():
    with open("config.json", "r") as f:
        data = f.read()  # Blocks entire event loop
    return json.loads(data)
```

**Correct (non-blocking file read):**

```python
import aiofiles

async def process_config():
    async with aiofiles.open("config.json", "r") as f:
        data = await f.read()  # Other coroutines can run
    return json.loads(data)
```

**When NOT to use this pattern:**
- Small config files read once at startup (blocking is acceptable)
- Performance-critical paths where `aiofiles` overhead matters (use sync I/O in executor)

Reference: [aiofiles documentation](https://github.com/Tinche/aiofiles)

### 1.4 Use Buffered I/O for Frequent Small Writes

**Impact: CRITICAL (reduces syscalls by 100-1000×, 10× throughput improvement)**

Each unbuffered write triggers a system call with kernel transition overhead. Buffered I/O batches writes, dramatically reducing syscall frequency.

**Incorrect (unbuffered writes, syscall per line):**

```python
def write_metrics(metrics: list[Metric], filepath: str):
    with open(filepath, "w", buffering=1) as f:  # Line buffered
        for metric in metrics:
            f.write(f"{metric.name},{metric.value}\n")
            # 10000 metrics = 10000 syscalls
```

**Correct (buffered writes, batched syscalls):**

```python
def write_metrics(metrics: list[Metric], filepath: str):
    with open(filepath, "w") as f:  # Default buffering ~8KB
        for metric in metrics:
            f.write(f"{metric.name},{metric.value}\n")
        # Writes batched into ~8KB chunks, ~100× fewer syscalls
```

**Alternative (explicit buffer size for large writes):**

```python
def write_large_dataset(records: list[dict], filepath: str):
    with open(filepath, "w", buffering=65536) as f:  # 64KB buffer
        for record in records:
            f.write(json.dumps(record) + "\n")
```

**Note:** Use `buffering=1` (line buffered) only when you need immediate line-by-line visibility, such as log files read by external tools in real-time.

Reference: [Python open() documentation](https://docs.python.org/3/library/functions.html#open)

### 1.5 Use Connection Pooling for Database and HTTP Clients

**Impact: CRITICAL (eliminates connection overhead, 50-200ms per request savings)**

Creating a new connection for each request incurs TCP handshake, TLS negotiation, and authentication overhead. Connection pools reuse established connections.

**Incorrect (new connection per request):**

```python
async def get_user(user_id: int) -> User:
    conn = await asyncpg.connect(DATABASE_URL)  # 50-200ms overhead
    try:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1", user_id
        )
        return User(**row)
    finally:
        await conn.close()
```

**Correct (reuse pooled connection):**

```python
# Create pool once at startup
pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20)

async def get_user(user_id: int) -> User:
    async with pool.acquire() as conn:  # Near-instant connection
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1", user_id
        )
        return User(**row)
```

**For HTTP clients (httpx):**

```python
# Reuse client with connection pooling
client = httpx.AsyncClient(limits=httpx.Limits(max_connections=100))

async def fetch_data(url: str) -> dict:
    response = await client.get(url)
    return response.json()
```

Reference: [asyncpg connection pooling](https://magicstack.github.io/asyncpg/current/api/index.html#connection-pools)

---

## 2. Async Concurrency

**Impact: CRITICAL**

Sequential awaits create waterfalls that multiply latency. Proper async patterns with gather/TaskGroup yield 2-10× improvement for I/O-bound code.

### 2.1 Avoid Async Overhead for CPU-Bound Work

**Impact: CRITICAL (2-8× improvement using multiprocessing for CPU-bound work)**

Async/await adds overhead (~2-5μs per await) for coroutine scheduling. For CPU-bound work, this overhead provides no benefit since the GIL prevents true parallelism. Use multiprocessing instead.

**Incorrect (async overhead with no concurrency benefit):**

```python
async def process_images(images: list[Image]) -> list[Thumbnail]:
    results = []
    for image in images:
        thumbnail = await asyncio.to_thread(resize_image, image)
        results.append(thumbnail)  # Still sequential due to GIL
    return results
```

**Correct (true parallelism with ProcessPoolExecutor):**

```python
from concurrent.futures import ProcessPoolExecutor

def process_images(images: list[Image]) -> list[Thumbnail]:
    with ProcessPoolExecutor() as executor:
        return list(executor.map(resize_image, images))
```

**Alternative (hybrid approach for mixed workloads):**

```python
async def process_mixed_workload(
    images: list[Image],
    urls: list[str],
) -> tuple[list[Thumbnail], list[Response]]:
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as executor:
        # CPU-bound in process pool
        thumbnails = loop.run_in_executor(
            executor, lambda: list(map(resize_image, images))
        )
        # I/O-bound with asyncio
        responses = asyncio.gather(*[fetch_url(url) for url in urls])

        return await asyncio.gather(thumbnails, responses)
```

Reference: [Concurrency in Python](https://docs.python.org/3/library/asyncio-dev.html#concurrency-and-multithreading)

### 2.2 Avoid Blocking Calls in Async Code

**Impact: CRITICAL (prevents event loop starvation, maintains concurrency)**

Blocking calls (CPU-bound work, synchronous I/O, `time.sleep()`) block the entire event loop, preventing all other coroutines from running. Use `run_in_executor()` for unavoidable blocking operations.

**Incorrect (blocks event loop for 5 seconds):**

```python
async def generate_report(data: ReportData) -> Report:
    time.sleep(5)  # Blocks ALL coroutines
    result = compute_heavy_statistics(data)  # CPU-bound, blocks
    return Report(result)
```

**Correct (offload blocking work to thread pool):**

```python
async def generate_report(data: ReportData) -> Report:
    await asyncio.sleep(5)  # Non-blocking sleep
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None,  # Default thread pool
        compute_heavy_statistics,
        data,
    )
    return Report(result)
```

**Alternative (for synchronous libraries):**

```python
async def sync_api_call(endpoint: str) -> dict:
    loop = asyncio.get_running_loop()
    # Wrap synchronous requests in executor
    response = await loop.run_in_executor(
        None,
        lambda: requests.get(endpoint).json()
    )
    return response
```

Reference: [asyncio event loop executors](https://docs.python.org/3/library/asyncio-eventloop.html#executing-code-in-thread-or-process-pools)

### 2.3 Store References to Fire-and-Forget Tasks

**Impact: CRITICAL (prevents silent task cancellation via garbage collection)**

Tasks created with `asyncio.create_task()` can be garbage collected if no reference is kept, causing silent cancellation. Always store task references.

**Incorrect (task may be garbage collected):**

```python
async def handle_request(request: Request) -> Response:
    asyncio.create_task(log_analytics(request))  # May be GC'd
    asyncio.create_task(update_metrics(request))  # May be GC'd
    return await process_request(request)
```

**Correct (store references to prevent GC):**

```python
background_tasks: set[asyncio.Task] = set()

async def handle_request(request: Request) -> Response:
    for coro in [log_analytics(request), update_metrics(request)]:
        task = asyncio.create_task(coro)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

    return await process_request(request)
```

**Alternative (using TaskGroup for managed lifecycle):**

```python
async def run_server():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(start_http_server())
        tg.create_task(start_metrics_reporter())
        # All tasks cleaned up when context exits
```

Reference: [asyncio.create_task documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task)

### 2.4 Use asyncio.gather() for Independent Operations

**Impact: CRITICAL (2-10× improvement, N round trips to 1)**

When async operations have no interdependencies, execute them concurrently using `asyncio.gather()`. Sequential awaits serialize operations that could run in parallel.

**Incorrect (sequential execution, 3 round trips):**

```python
async def fetch_dashboard_data(user_id: int) -> DashboardData:
    user = await fetch_user(user_id)
    orders = await fetch_orders(user_id)
    notifications = await fetch_notifications(user_id)
    # Total time: user + orders + notifications
    return DashboardData(user, orders, notifications)
```

**Correct (parallel execution, 1 round trip):**

```python
async def fetch_dashboard_data(user_id: int) -> DashboardData:
    user, orders, notifications = await asyncio.gather(
        fetch_user(user_id),
        fetch_orders(user_id),
        fetch_notifications(user_id),
    )
    # Total time: max(user, orders, notifications)
    return DashboardData(user, orders, notifications)
```

**Alternative (with error handling):**

```python
results = await asyncio.gather(
    fetch_user(user_id),
    fetch_orders(user_id),
    return_exceptions=True,  # Don't fail fast, collect all results
)
```

Reference: [asyncio.gather documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)

### 2.5 Use Semaphores for Concurrency Limiting

**Impact: CRITICAL (prevents resource exhaustion, controls connection limits)**

Unbounded concurrency can exhaust resources (connections, file descriptors, memory). Use `asyncio.Semaphore` to limit concurrent operations.

**Incorrect (unbounded concurrency, may exhaust connections):**

```python
async def fetch_all_urls(urls: list[str]) -> list[Response]:
    return await asyncio.gather(
        *[fetch_url(url) for url in urls]
    )  # 10000 URLs = 10000 concurrent connections
```

**Correct (bounded concurrency with semaphore):**

```python
async def fetch_all_urls(urls: list[str], max_concurrent: int = 50) -> list[Response]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_with_limit(url: str) -> Response:
        async with semaphore:
            return await fetch_url(url)

    return await asyncio.gather(
        *[fetch_with_limit(url) for url in urls]
    )  # Max 50 concurrent connections
```

**Alternative (bounded semaphore for stricter control):**

```python
# Raises ValueError if released more than acquired
semaphore = asyncio.BoundedSemaphore(max_concurrent)
```

Reference: [asyncio.Semaphore documentation](https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore)

### 2.6 Use TaskGroup for Structured Concurrency

**Impact: CRITICAL (automatic cleanup on failure, prevents orphaned tasks)**

`asyncio.TaskGroup` (Python 3.11+) provides structured concurrency with automatic exception handling and cleanup. Unlike `gather()`, it cancels all tasks when one fails.

**Incorrect (unstructured tasks, potential orphans):**

```python
async def process_batch(items: list[Item]) -> list[Result]:
    tasks = [asyncio.create_task(process_item(item)) for item in items]
    try:
        return await asyncio.gather(*tasks)
    except Exception:
        # Some tasks may continue running as orphans
        for task in tasks:
            task.cancel()
        raise
```

**Correct (structured concurrency, automatic cleanup):**

```python
async def process_batch(items: list[Item]) -> list[Result]:
    results = []
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_item(item)) for item in items]
    # All tasks complete or all cancelled on any exception
    return [task.result() for task in tasks]
```

**Benefits:**
- Automatic cancellation of remaining tasks on exception
- No orphaned tasks or resource leaks
- Clear task lifetime boundaries
- Better exception propagation via ExceptionGroup

Reference: [asyncio.TaskGroup documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup)

---

## 3. Memory Management

**Impact: HIGH**

Memory allocation and object creation overhead compounds in hot paths. Using __slots__, generators, and efficient data structures reduces memory footprint by 30-50%.

### 3.1 Avoid Intermediate Lists in Pipelines

**Impact: HIGH (eliminates N intermediate allocations, O(1) vs O(n) memory)**

Chaining list operations creates intermediate lists at each step. Use generator expressions or `itertools` to process data in a single pass without intermediate allocations.

**Incorrect (creates 3 intermediate lists):**

```python
def process_orders(orders: list[Order]) -> list[str]:
    pending = [o for o in orders if o.status == "pending"]  # List 1
    high_value = [o for o in pending if o.total > 1000]  # List 2
    emails = [o.customer_email for o in high_value]  # List 3
    return emails
```

**Correct (single pass, no intermediate lists):**

```python
def process_orders(orders: Iterable[Order]) -> Iterator[str]:
    return (
        order.customer_email
        for order in orders
        if order.status == "pending" and order.total > 1000
    )
```

**Note:** The return type changes from `list[str]` to `Iterator[str]`. If you need a concrete list, wrap with `list(process_orders(orders))`.

**Alternative (itertools for complex pipelines):**

```python
from itertools import filterfalse, islice

def process_orders(orders: Iterable[Order]) -> Iterator[str]:
    pending = (o for o in orders if o.status == "pending")
    high_value = (o for o in pending if o.total > 1000)
    return (o.customer_email for o in islice(high_value, 100))
```

Reference: [itertools documentation](https://docs.python.org/3/library/itertools.html)

### 3.2 Leverage String Interning for Repeated Strings

**Impact: HIGH (eliminates duplicate string allocations)**

Python automatically interns some strings, but explicit interning with `sys.intern()` ensures repeated strings share the same memory location.

**Incorrect (duplicate strings consume memory):**

```python
def process_events(events: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        event_type = event["type"]  # Each "click" is a new string
        counts[event_type] = counts.get(event_type, 0) + 1
    return counts
    # 1M events with 10 types = 1M string allocations
```

**Correct (interned strings share memory):**

```python
import sys

def process_events(events: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for event in events:
        event_type = sys.intern(event["type"])  # Reuses existing string
        counts[event_type] = counts.get(event_type, 0) + 1
    return counts
    # 1M events with 10 types = 10 string allocations
```

**Alternative (pre-intern known values):**

```python
EVENT_TYPES = {
    sys.intern("click"): 0,
    sys.intern("scroll"): 0,
    sys.intern("submit"): 0,
}
```

**Note:** Python automatically interns string literals and identifiers. Use `sys.intern()` for dynamically created strings that repeat frequently.

Reference: [sys.intern documentation](https://docs.python.org/3/library/sys.html#sys.intern)

### 3.3 Preallocate Lists When Size is Known

**Impact: HIGH (eliminates reallocation overhead, 10-30% faster)**

List append operations trigger periodic reallocations as the list grows. When the final size is known, preallocate to avoid reallocation overhead.

**Incorrect (multiple reallocations during growth):**

```python
def transform_values(source: list[int]) -> list[int]:
    result = []
    for value in source:
        result.append(value * 2)  # Triggers reallocations
    return result
```

**Correct (list comprehension, single allocation):**

```python
def transform_values(source: list[int]) -> list[int]:
    return [value * 2 for value in source]  # Single allocation
```

**Alternative (numpy for numeric data):**

```python
import numpy as np

def transform_values(source: np.ndarray) -> np.ndarray:
    result = np.empty(len(source), dtype=source.dtype)  # Preallocate
    np.multiply(source, 2, out=result)  # In-place operation
    return result
```

**Alternative (preallocate with None):**

```python
def transform_sparse_values(indices: list[int], values: list[int], size: int) -> list[int | None]:
    result = [None] * size  # Single allocation
    for idx, val in zip(indices, values):
        result[idx] = val
    return result
```

Reference: [Python list implementation](https://docs.python.org/3/faq/design.html#how-are-lists-implemented-in-cpython)

### 3.4 Use __slots__ for Memory-Efficient Classes

**Impact: HIGH (30-50% memory reduction per instance)**

By default, Python stores instance attributes in a `__dict__`. Defining `__slots__` eliminates this dict, reducing memory by 30-50% per instance.

**Incorrect (dict overhead per instance):**

```python
@dataclass
class Point:
    x: float
    y: float
    z: float
    # Each instance carries a __dict__ (~100+ bytes overhead)
```

**Correct (slots eliminate dict overhead):**

```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
    z: float
    # No __dict__, ~40% less memory per instance
```

**Alternative (manual slots for pre-3.10):**

```python
class Point:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
```

**When NOT to use slots:**
- Classes requiring dynamic attribute assignment
- Classes using multiple inheritance (slots can conflict)
- Few instances where memory savings are negligible

Reference: [dataclass slots documentation](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass)

### 3.5 Use Generators for Lazy Evaluation

**Impact: HIGH (O(1) memory instead of O(n), processes any size dataset)**

List comprehensions create the entire list in memory. Generator expressions yield items one at a time, using constant memory regardless of dataset size.

**Incorrect (creates entire list in memory):**

```python
def get_active_users(users: list[User]) -> list[User]:
    return [user for user in users if user.is_active]
    # 1M users with 100K active = 100K User objects in memory
```

**Correct (yields one at a time, O(1) memory):**

```python
def get_active_users(users: Iterable[User]) -> Iterator[User]:
    return (user for user in users if user.is_active)
    # Memory: 1 User object at a time

# Or with yield for complex logic
def get_active_users(users: Iterable[User]) -> Iterator[User]:
    for user in users:
        if user.is_active:
            yield user
```

**When to materialize:**

```python
# Only create list when you need random access or length
active_list = list(get_active_users(users))  # Explicit materialization
```

Reference: [Generator expressions](https://docs.python.org/3/howto/functional.html#generator-expressions-and-list-comprehensions)

### 3.6 Use Weak References for Caches and Observers

**Impact: HIGH (prevents memory leaks, allows automatic cleanup)**

Strong references in caches and observer patterns prevent garbage collection, causing memory leaks. Use `weakref` to allow objects to be collected when no longer needed.

**Incorrect (strong references prevent GC):**

```python
class EventEmitter:
    def __init__(self):
        self.listeners: list[Callable] = []

    def subscribe(self, callback: Callable):
        self.listeners.append(callback)  # Strong reference
        # Callback owner cannot be GC'd even when out of scope
```

**Correct (weak references allow GC):**

```python
import weakref

class EventEmitter:
    def __init__(self):
        self.listeners: list[weakref.ref] = []

    def subscribe(self, callback: Callable):
        self.listeners.append(weakref.ref(callback))

    def emit(self, event: Event):
        # Clean up dead references and call live ones
        self.listeners = [ref for ref in self.listeners if ref() is not None]
        for ref in self.listeners:
            if callback := ref():
                callback(event)
```

**Alternative (WeakValueDictionary for caches):**

```python
from weakref import WeakValueDictionary

# Cached objects can be GC'd when no other references exist
_user_cache: WeakValueDictionary[int, User] = WeakValueDictionary()

def get_user(user_id: int) -> User:
    if user_id not in _user_cache:
        _user_cache[user_id] = fetch_user_from_db(user_id)
    return _user_cache[user_id]
```

Reference: [weakref documentation](https://docs.python.org/3/library/weakref.html)

---

## 4. Data Structures

**Impact: HIGH**

Wrong data structure choice leads to O(n) instead of O(1) operations. Sets and dicts provide constant-time lookups; deque beats list for queue operations.

### 4.1 Use Counter for Frequency Counting

**Impact: HIGH (2-3× faster than manual dict counting)**

Manual counting with dictionaries is verbose and slower than `collections.Counter`, which is implemented in C and provides useful methods.

**Incorrect (manual counting):**

```python
def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.split():
        word = word.lower()
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts
```

**Correct (Counter, optimized implementation):**

```python
from collections import Counter

def count_words(text: str) -> Counter[str]:
    return Counter(word.lower() for word in text.split())
```

**Counter provides useful methods:**

```python
word_counts = Counter(words)

# Most common items
top_10 = word_counts.most_common(10)

# Combine counters
total = word_counts + other_counts

# Subtract counts
remaining = word_counts - processed_counts

# Elements iterator (repeat by count)
all_words = list(word_counts.elements())
```

Reference: [Counter documentation](https://docs.python.org/3/library/collections.html#collections.Counter)

### 4.2 Use deque for O(1) Queue Operations

**Impact: HIGH (O(n) to O(1) for left operations)**

List `pop(0)` and `insert(0, x)` are O(n) operations requiring element shifting. `collections.deque` provides O(1) operations on both ends.

**Incorrect (O(n) for left operations):**

```python
def process_queue(tasks: list[Task]) -> None:
    while tasks:
        task = tasks.pop(0)  # O(n) - shifts all elements
        process(task)
        if task.spawn_subtask:
            tasks.insert(0, task.subtask)  # O(n) again
```

**Correct (O(1) for both ends):**

```python
from collections import deque

def process_queue(tasks: list[Task]) -> None:
    queue = deque(tasks)
    while queue:
        task = queue.popleft()  # O(1)
        process(task)
        if task.spawn_subtask:
            queue.appendleft(task.subtask)  # O(1)
```

**Alternative (bounded deque for fixed-size buffers):**

```python
# Automatically discards oldest items when full
recent_events: deque[Event] = deque(maxlen=1000)
recent_events.append(new_event)  # O(1), auto-evicts if full
```

Reference: [deque documentation](https://docs.python.org/3/library/collections.html#collections.deque)

### 4.3 Use dict.get() with Default Instead of KeyError Handling

**Impact: HIGH (cleaner code, avoids exception overhead)**

Exception handling for missing keys is slower and more verbose than using `dict.get()` with a default value.

**Incorrect (exception overhead for missing keys):**

```python
def get_user_setting(user_id: int, settings: dict[int, Settings]) -> Settings:
    try:
        return settings[user_id]
    except KeyError:
        return Settings()  # Default settings
```

**Correct (no exception overhead):**

```python
def get_user_setting(user_id: int, settings: dict[int, Settings]) -> Settings:
    return settings.get(user_id, Settings())
```

**Alternative (setdefault for insert-if-missing):**

```python
def get_or_create_settings(user_id: int, settings: dict[int, Settings]) -> Settings:
    return settings.setdefault(user_id, Settings())
    # Inserts default and returns it if key missing
```

**Alternative (defaultdict for automatic defaults):**

```python
from collections import defaultdict

user_counts: defaultdict[int, int] = defaultdict(int)
user_counts[user_id] += 1  # No KeyError, auto-initializes to 0
```

Reference: [dict.get documentation](https://docs.python.org/3/library/stdtypes.html#dict.get)

### 4.4 Use NamedTuple for Immutable Lightweight Records

**Impact: HIGH (3-10× less memory than dict, attribute access by name)**

Dictionaries storing fixed fields waste memory on hash tables and string keys. `NamedTuple` provides named access with tuple efficiency.

**Incorrect (dict overhead for structured data):**

```python
def fetch_coordinates() -> list[dict[str, float]]:
    return [
        {"latitude": 40.7128, "longitude": -74.0060, "altitude": 10.0},
        {"latitude": 34.0522, "longitude": -118.2437, "altitude": 71.0},
    ]
    # Each dict: ~240 bytes
```

**Correct (NamedTuple, minimal overhead):**

```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    latitude: float
    longitude: float
    altitude: float

def fetch_coordinates() -> list[Coordinate]:
    return [
        Coordinate(40.7128, -74.0060, 10.0),
        Coordinate(34.0522, -118.2437, 71.0),
    ]
    # Each tuple: ~72 bytes
```

**Benefits:**
- Immutable by default (hashable, safe as dict keys)
- Named attribute access (`coord.latitude`)
- Unpacking support (`lat, lon, alt = coord`)
- Memory efficient (no per-instance dict)

Reference: [NamedTuple documentation](https://docs.python.org/3/library/typing.html#typing.NamedTuple)

### 4.5 Use Set for O(1) Membership Testing

**Impact: HIGH (O(n) to O(1) lookups)**

List membership testing (`in`) is O(n). Set membership testing is O(1). Convert lists to sets when performing repeated lookups.

**Incorrect (O(n) per lookup, O(n×m) total):**

```python
def filter_allowed_users(users: list[User], allowed_ids: list[int]) -> list[User]:
    return [user for user in users if user.id in allowed_ids]
    # 10K users × 1K allowed = 10M comparisons
```

**Correct (O(1) per lookup, O(n) total):**

```python
def filter_allowed_users(users: list[User], allowed_ids: list[int]) -> list[User]:
    allowed_set = set(allowed_ids)  # O(m) one-time cost
    return [user for user in users if user.id in allowed_set]
    # 10K users × O(1) = 10K comparisons
```

**Note:** Set creation is O(m). Use sets when lookup count exceeds set size, or when the set can be reused.

Reference: [Time complexity of Python operations](https://wiki.python.org/moin/TimeComplexity)

---

## 5. Algorithm Efficiency

**Impact: MEDIUM-HIGH**

Algorithm complexity dominates at scale. List comprehensions, generator expressions, and built-in functions outperform manual loops by 2-5×.

### 5.1 Cache Expensive Computations in Loops

**Impact: MEDIUM-HIGH (eliminates N redundant calculations)**

Repeated computation inside loops multiplies cost. Hoist invariant calculations outside the loop or cache intermediate results.

**Incorrect (repeated computation inside loop):**

```python
def filter_recent_orders(orders: list[Order], days: int) -> list[Order]:
    return [
        order for order in orders
        if order.created_at > datetime.now() - timedelta(days=days)
        # datetime.now() and timedelta() called for each order
    ]
```

**Correct (computation hoisted outside loop):**

```python
def filter_recent_orders(orders: list[Order], days: int) -> list[Order]:
    cutoff = datetime.now() - timedelta(days=days)  # Computed once
    return [order for order in orders if order.created_at > cutoff]
```

**Alternative (cache attribute access):**

```python
def process_config_items(items: list[Item], config: Config) -> list[Result]:
    # Cache frequently accessed nested attributes
    threshold = config.settings.processing.threshold
    multiplier = config.settings.processing.multiplier

    return [
        Result(item.value * multiplier)
        for item in items
        if item.value > threshold
    ]
```

Reference: [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)

### 5.2 Use Built-in Functions Over Manual Implementation

**Impact: MEDIUM-HIGH (5-20× faster, C-optimized implementations)**

Built-in functions like `sum()`, `max()`, `min()`, `any()`, `all()` are implemented in C and significantly outperform Python loop equivalents.

**Incorrect (manual sum implementation):**

```python
def calculate_total_revenue(orders: list[Order]) -> float:
    total = 0
    for order in orders:
        total += order.total
    return total
```

**Correct (built-in sum):**

```python
def calculate_total_revenue(orders: list[Order]) -> float:
    return sum(order.total for order in orders)
```

**More built-in examples:**

```python
# Max/min with key function
highest_order = max(orders, key=lambda o: o.total)
oldest_user = min(users, key=lambda u: u.created_at)

# any/all for boolean checks (short-circuit)
has_admin = any(user.is_admin for user in users)  # Stops at first True
all_verified = all(user.verified for user in users)  # Stops at first False

# sorted with key
by_date = sorted(orders, key=lambda o: o.created_at, reverse=True)
```

Reference: [Built-in functions](https://docs.python.org/3/library/functions.html)

### 5.3 Use itertools for Efficient Iteration Patterns

**Impact: MEDIUM-HIGH (2-5× faster than Python equivalents)**

The `itertools` module provides C-optimized iterators for common patterns. They're memory-efficient and faster than Python equivalents.

**Incorrect (manual batching):**

```python
def batch_items(items: list[Item], batch_size: int) -> list[list[Item]]:
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches
```

**Correct (itertools.batched, Python 3.12+):**

```python
from itertools import batched

def batch_items(items: Iterable[Item], batch_size: int) -> Iterator[tuple[Item, ...]]:
    return batched(items, batch_size)
```

**Common itertools patterns:**

```python
from itertools import chain, groupby, islice, takewhile

# Flatten nested iterables
all_orders = chain.from_iterable(user.orders for user in users)

# Group by key (requires sorted input)
by_status = groupby(sorted(orders, key=lambda o: o.status), key=lambda o: o.status)

# Take first N items lazily
first_10 = islice(large_iterator, 10)

# Take while condition is true
recent = takewhile(lambda o: o.created_at > cutoff, sorted_orders)
```

Reference: [itertools documentation](https://docs.python.org/3/library/itertools.html)

### 5.4 Use List Comprehensions Over Manual Loops

**Impact: MEDIUM-HIGH (2-3× faster than equivalent for loop)**

List comprehensions are optimized in CPython and run faster than equivalent `for` loops with `append()`. They also produce cleaner, more readable code.

**Incorrect (manual loop with append):**

```python
def get_order_totals(orders: list[Order]) -> list[float]:
    totals = []
    for order in orders:
        totals.append(order.quantity * order.unit_price)
    return totals
```

**Correct (list comprehension):**

```python
def get_order_totals(orders: list[Order]) -> list[float]:
    return [order.quantity * order.unit_price for order in orders]
```

**With conditional filtering:**

```python
def get_high_value_totals(orders: list[Order]) -> list[float]:
    return [
        order.quantity * order.unit_price
        for order in orders
        if order.quantity * order.unit_price > 1000
    ]
```

**When to use a regular loop:**
- Complex logic with multiple statements per iteration
- Need to break early or handle exceptions per item
- Side effects during iteration

Reference: [List comprehension documentation](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)

### 5.5 Use Local Variables in Hot Loops

**Impact: MEDIUM-HIGH (20-30% faster attribute lookups)**

Global and attribute lookups are slower than local variable lookups. In performance-critical loops, assign frequently accessed items to local variables.

**Incorrect (repeated global/attribute lookups):**

```python
import math

def calculate_distances(points: list[Point]) -> list[float]:
    distances = []
    for point in points:
        # math.sqrt looked up each iteration
        distances.append(math.sqrt(point.x ** 2 + point.y ** 2))
    return distances
```

**Correct (local variable for hot path):**

```python
import math

def calculate_distances(points: list[Point]) -> list[float]:
    sqrt = math.sqrt  # Local lookup is faster
    return [sqrt(point.x ** 2 + point.y ** 2) for point in points]
```

**Micro-benchmark context:**

```python
# Global: ~50ns per lookup
# Attribute: ~40ns per lookup
# Local: ~20ns per lookup
# Difference matters when loop runs millions of times
```

**Note:** Only apply this optimization in proven hot paths. Profile first to confirm the loop is a bottleneck.

Reference: [Python Performance Tips - Local Variables](https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Local_Variables)

### 5.6 Use str.join() for String Concatenation

**Impact: MEDIUM-HIGH (O(n) vs O(n²), eliminates quadratic string creation)**

String concatenation with `+=` in loops creates new string objects each iteration, resulting in O(n²) complexity. `str.join()` builds the result in a single pass.

**Incorrect (quadratic string concatenation):**

```python
def build_csv_row(values: list[str]) -> str:
    result = ""
    for i, value in enumerate(values):
        if i > 0:
            result += ","
        result += value  # Creates new string each iteration
    return result
```

**Correct (single-pass join):**

```python
def build_csv_row(values: list[str]) -> str:
    return ",".join(values)
```

**With transformation:**

```python
def build_user_summary(users: list[User]) -> str:
    return "\n".join(f"{user.name}: {user.email}" for user in users)
```

**Alternative (f-strings for fixed small concatenations):**

```python
# For 2-5 known values, f-strings are cleaner and fast
greeting = f"Hello, {first_name} {last_name}!"
```

Reference: [str.join documentation](https://docs.python.org/3/library/stdtypes.html#str.join)

---

## 6. Concurrency Model

**Impact: MEDIUM**

GIL limits threading for CPU-bound work. Choosing the right concurrency model—asyncio, threading, or multiprocessing—determines scalability.

### 6.1 Choose the Right Concurrency Model

**Impact: MEDIUM (2-8× improvement with correct model selection)**

Python offers three concurrency models, each suited for different workloads. Choosing wrong limits scalability or adds unnecessary overhead.

**Decision guide:**

```python
# I/O-bound: asyncio (best) or threading
# CPU-bound: multiprocessing (bypasses GIL)
# Mixed: hybrid approach

# I/O-bound examples: web requests, database queries, file I/O
# CPU-bound examples: image processing, data compression, ML inference
```

**Incorrect (threading for CPU-bound work):**

```python
from concurrent.futures import ThreadPoolExecutor

def process_images(images: list[Image]) -> list[Thumbnail]:
    with ThreadPoolExecutor(max_workers=8) as executor:
        return list(executor.map(resize_image, images))
    # GIL prevents true parallelism - limited to 1 CPU core
```

**Correct (multiprocessing for CPU-bound work):**

```python
from concurrent.futures import ProcessPoolExecutor

def process_images(images: list[Image]) -> list[Thumbnail]:
    with ProcessPoolExecutor(max_workers=8) as executor:
        return list(executor.map(resize_image, images))
    # Each process has its own GIL - true parallelism
```

**Correct (asyncio for I/O-bound work):**

```python
async def fetch_all_pages(urls: list[str]) -> list[Response]:
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[session.get(url) for url in urls]
        )
    # Single thread handles thousands of concurrent connections
```

Reference: [Concurrency in Python](https://docs.python.org/3/library/concurrency.html)

### 6.2 Minimize Lock Contention in Threaded Code

**Impact: MEDIUM (reduces serialization, improves parallel throughput)**

Long-held locks serialize execution, negating concurrency benefits. Keep critical sections minimal and consider lock-free alternatives.

**Incorrect (lock held during I/O):**

```python
import threading

cache_lock = threading.Lock()
cache: dict[str, Data] = {}

def get_data(key: str) -> Data:
    with cache_lock:  # Lock held during slow I/O
        if key not in cache:
            cache[key] = fetch_from_database(key)  # Blocks all threads
        return cache[key]
```

**Correct (minimize critical section):**

```python
import threading

cache_lock = threading.Lock()
cache: dict[str, Data] = {}

def get_data(key: str) -> Data:
    # Check without lock first
    with cache_lock:
        if key in cache:
            return cache[key]

    # Fetch outside lock (may have duplicate fetches, but no blocking)
    data = fetch_from_database(key)

    with cache_lock:
        cache.setdefault(key, data)  # Only insert if still missing
        return cache[key]
```

**Alternative (RLock for reentrant access):**

```python
# Use RLock when same thread may need to acquire lock multiple times
cache_lock = threading.RLock()
```

Reference: [threading.Lock documentation](https://docs.python.org/3/library/threading.html#lock-objects)

### 6.3 Use asyncio.Queue for Producer-Consumer Patterns

**Impact: MEDIUM (enables backpressure and controlled concurrency)**

`asyncio.Queue` provides async-safe producer-consumer coordination with backpressure support, preventing memory exhaustion from fast producers.

**Incorrect (unbounded list accumulation):**

```python
async def process_stream(stream: AsyncIterator[Event]) -> None:
    events = []
    async for event in stream:
        events.append(event)  # Memory grows unbounded

    for event in events:
        await process_event(event)
```

**Correct (bounded queue with backpressure):**

```python
async def process_stream(stream: AsyncIterator[Event]) -> None:
    queue: asyncio.Queue[Event] = asyncio.Queue(maxsize=100)

    async def producer():
        async for event in stream:
            await queue.put(event)  # Blocks when queue full
        await queue.put(None)  # Sentinel to signal completion

    async def consumer():
        while (event := await queue.get()) is not None:
            await process_event(event)
            queue.task_done()

    await asyncio.gather(producer(), consumer())
```

**Multiple consumers:**

```python
async def run_workers(queue: asyncio.Queue, num_workers: int = 5):
    async def worker():
        while True:
            task = await queue.get()
            await process_task(task)
            queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(num_workers)]
    await queue.join()  # Wait for all tasks to complete
```

Reference: [asyncio.Queue documentation](https://docs.python.org/3/library/asyncio-queue.html)

### 6.4 Use Chunking for ProcessPoolExecutor

**Impact: MEDIUM (reduces IPC overhead by 10-100×)**

Each task submitted to ProcessPoolExecutor incurs inter-process communication (IPC) overhead. Batch small tasks into chunks to amortize this cost.

**Incorrect (IPC overhead per item):**

```python
from concurrent.futures import ProcessPoolExecutor

def process_pixels(pixels: list[Pixel]) -> list[Color]:
    with ProcessPoolExecutor() as executor:
        return list(executor.map(transform_pixel, pixels))
    # 1M pixels = 1M IPC round trips
```

**Correct (chunked processing):**

```python
from concurrent.futures import ProcessPoolExecutor

def process_chunk(chunk: list[Pixel]) -> list[Color]:
    return [transform_pixel(pixel) for pixel in chunk]

def process_pixels(pixels: list[Pixel], chunk_size: int = 1000) -> list[Color]:
    chunks = [pixels[i:i + chunk_size] for i in range(0, len(pixels), chunk_size)]

    with ProcessPoolExecutor() as executor:
        results = executor.map(process_chunk, chunks)

    return [color for chunk_result in results for color in chunk_result]
    # 1M pixels = 1K IPC round trips
```

**Alternative (use chunksize parameter):**

```python
with ProcessPoolExecutor() as executor:
    results = list(executor.map(transform_pixel, pixels, chunksize=1000))
```

Reference: [ProcessPoolExecutor documentation](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor)

### 6.5 Use Thread-Safe Data Structures for Shared State

**Impact: MEDIUM (prevents race conditions and data corruption)**

Regular Python data structures are not thread-safe. Use `queue.Queue`, `threading.Lock`, or thread-local storage for shared state.

**Incorrect (race condition on shared list):**

```python
results: list[Result] = []

def worker(task: Task) -> None:
    result = process(task)
    results.append(result)  # Race condition!

with ThreadPoolExecutor() as executor:
    executor.map(worker, tasks)
```

**Correct (thread-safe queue):**

```python
from queue import Queue

results: Queue[Result] = Queue()

def worker(task: Task) -> None:
    result = process(task)
    results.put(result)  # Thread-safe

with ThreadPoolExecutor() as executor:
    executor.map(worker, tasks)

# Collect results
all_results = [results.get() for _ in range(len(tasks))]
```

**Alternative (return values from executor):**

```python
def process_task(task: Task) -> Result:
    return process(task)

with ThreadPoolExecutor() as executor:
    results = list(executor.map(process_task, tasks))
```

Reference: [queue documentation](https://docs.python.org/3/library/queue.html)

---

## 7. Serialization

**Impact: MEDIUM**

JSON/pickle overhead adds up in hot paths. Efficient serialization with orjson, msgpack, or Protocol Buffers reduces CPU and memory pressure.

### 7.1 Avoid Pickle for Untrusted Data

**Impact: MEDIUM (prevents arbitrary code execution vulnerabilities)**

Pickle can execute arbitrary code during deserialization. Never unpickle data from untrusted sources. Use safe alternatives like JSON or MessagePack.

**Incorrect (arbitrary code execution risk):**

```python
import pickle

def load_user_data(data: bytes) -> UserData:
    return pickle.loads(data)  # Can execute arbitrary code!
```

**Correct (safe JSON deserialization):**

```python
import orjson
from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    email: str

def load_user_data(data: bytes) -> UserData:
    return UserData.model_validate(orjson.loads(data))
```

**When pickle is acceptable:**
- Internal caching (e.g., ML model checkpoints)
- IPC between trusted processes
- Data you serialized yourself

**Safer pickle alternative (restricted):**

```python
import pickle

# Restrict unpickling to specific classes
class RestrictedUnpickler(pickle.Unpickler):
    SAFE_CLASSES = {"UserData", "OrderData"}

    def find_class(self, module, name):
        if name in self.SAFE_CLASSES:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"Forbidden class: {name}")
```

Reference: [pickle security warning](https://docs.python.org/3/library/pickle.html#module-pickle)

### 7.2 Use MessagePack for Compact Binary Serialization

**Impact: MEDIUM (30-50% smaller than JSON, faster parsing)**

MessagePack produces smaller payloads than JSON and parses faster, making it ideal for high-volume internal APIs and caching.

**Incorrect (verbose JSON for internal API):**

```python
import json

def cache_set(key: str, value: dict) -> None:
    redis.set(key, json.dumps(value))  # Verbose text format

def cache_get(key: str) -> dict | None:
    if data := redis.get(key):
        return json.loads(data)
    return None
```

**Correct (compact MessagePack):**

```python
import msgpack

def cache_set(key: str, value: dict) -> None:
    redis.set(key, msgpack.packb(value))  # 30-50% smaller

def cache_get(key: str) -> dict | None:
    if data := redis.get(key):
        return msgpack.unpackb(data)
    return None
```

**With custom types:**

```python
import msgpack
from datetime import datetime

def encode_datetime(obj):
    if isinstance(obj, datetime):
        return {"__datetime__": obj.isoformat()}
    return obj

def decode_datetime(obj):
    if "__datetime__" in obj:
        return datetime.fromisoformat(obj["__datetime__"])
    return obj

packed = msgpack.packb(data, default=encode_datetime)
unpacked = msgpack.unpackb(packed, object_hook=decode_datetime)
```

Reference: [msgpack-python documentation](https://github.com/msgpack/msgpack-python)

### 7.3 Use orjson for High-Performance JSON

**Impact: MEDIUM (3-10× faster than stdlib json)**

The `orjson` library is significantly faster than the standard library `json` module and handles common Python types natively.

**Incorrect (stdlib json, slow):**

```python
import json

def serialize_response(data: dict) -> bytes:
    return json.dumps(data).encode("utf-8")

def parse_request(body: bytes) -> dict:
    return json.loads(body.decode("utf-8"))
```

**Correct (orjson, 3-10× faster):**

```python
import orjson

def serialize_response(data: dict) -> bytes:
    return orjson.dumps(data)  # Returns bytes directly

def parse_request(body: bytes) -> dict:
    return orjson.loads(body)  # Accepts bytes directly
```

**orjson handles common types:**

```python
import orjson
from datetime import datetime
from uuid import UUID

data = {
    "timestamp": datetime.now(),  # Auto-serialized to ISO format
    "user_id": UUID("12345678-1234-5678-1234-567812345678"),
    "scores": [1.5, 2.7, 3.9],
}

# No need for custom encoder
result = orjson.dumps(data)
```

Reference: [orjson documentation](https://github.com/ijl/orjson)

### 7.4 Use Pydantic for Validated Deserialization

**Impact: MEDIUM (combines parsing with validation, prevents invalid data)**

Raw JSON parsing provides no validation. Pydantic combines deserialization with type validation, catching errors at the boundary.

**Incorrect (no validation, errors propagate):**

```python
import json

def process_order(data: bytes) -> Order:
    parsed = json.loads(data)
    return Order(
        user_id=parsed["user_id"],  # May be missing
        total=parsed["total"],  # May be wrong type
        items=parsed["items"],  # May be malformed
    )
```

**Correct (validated deserialization):**

```python
from pydantic import BaseModel, Field

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)

class Order(BaseModel):
    user_id: int
    total: float = Field(gt=0)
    items: list[OrderItem] = Field(min_length=1)

def process_order(data: bytes) -> Order:
    return Order.model_validate_json(data)
    # Raises ValidationError with clear messages for invalid data
```

**Benefits:**
- Type coercion (string "123" → int 123)
- Constraint validation (positive numbers, non-empty lists)
- Clear error messages for debugging
- JSON Schema generation for API docs

Reference: [Pydantic documentation](https://docs.pydantic.dev/)

---

## 8. Caching and Memoization

**Impact: LOW-MEDIUM**

functools.lru_cache and manual caching prevent redundant computation but add memory overhead. Use strategically on expensive, frequently-called functions.

### 8.1 Avoid Over-Caching Low-Value Operations

**Impact: LOW-MEDIUM (cache overhead may exceed computation cost)**

Caching adds overhead: hash computation, dictionary lookups, memory usage. Only cache operations where computation cost significantly exceeds cache overhead.

**Incorrect (caching trivial operations):**

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def double(x: int) -> int:
    return x * 2
    # Hash + lookup overhead exceeds multiplication cost

@lru_cache(maxsize=1000)
def format_name(first: str, last: str) -> str:
    return f"{first} {last}"
    # String formatting is fast, caching adds overhead
```

**Correct (cache expensive operations only):**

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def parse_config(config_path: str) -> Config:
    # File I/O + parsing is expensive
    with open(config_path) as f:
        return parse_yaml(f.read())

@lru_cache(maxsize=1000)
def compile_regex(pattern: str) -> re.Pattern:
    # Regex compilation is expensive
    return re.compile(pattern)
```

**Profile before caching:**

```python
import cProfile

# Profile to identify actual bottlenecks
cProfile.run("process_data(large_dataset)")
# Only cache functions that appear in profiler output
```

Reference: [Python profiling documentation](https://docs.python.org/3/library/profile.html)

### 8.2 Implement TTL for Time-Sensitive Caches

**Impact: LOW-MEDIUM (prevents stale data, controls memory growth)**

`lru_cache` has no expiration. For time-sensitive data, use `cachetools.TTLCache` or implement manual expiration to prevent stale results.

**Incorrect (stale data indefinitely):**

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_exchange_rate(currency: str) -> float:
    return fetch_current_rate(currency)
    # Returns stale rate until cache_clear() is called
```

**Correct (TTL-based expiration):**

```python
from cachetools import TTLCache
from cachetools.keys import hashkey

exchange_cache: TTLCache[str, float] = TTLCache(maxsize=1000, ttl=300)  # 5 min TTL

def get_exchange_rate(currency: str) -> float:
    if currency not in exchange_cache:
        exchange_cache[currency] = fetch_current_rate(currency)
    return exchange_cache[currency]
```

**Alternative (decorator with TTL):**

```python
from cachetools import cached, TTLCache

@cached(cache=TTLCache(maxsize=1000, ttl=300))
def get_exchange_rate(currency: str) -> float:
    return fetch_current_rate(currency)
```

Reference: [cachetools documentation](https://cachetools.readthedocs.io/)

### 8.3 Use cached_property for Expensive Computed Attributes

**Impact: LOW-MEDIUM (computes once per instance, O(1) subsequent access)**

`functools.cached_property` computes an attribute value once and caches it on the instance, avoiding repeated computation.

**Incorrect (recomputes on every access):**

```python
class Report:
    def __init__(self, data: list[DataPoint]):
        self.data = data

    @property
    def statistics(self) -> Statistics:
        # Expensive computation runs every time .statistics is accessed
        return compute_statistics(self.data)
```

**Correct (computed once, cached on instance):**

```python
from functools import cached_property

class Report:
    def __init__(self, data: list[DataPoint]):
        self.data = data

    @cached_property
    def statistics(self) -> Statistics:
        # Computed once, stored as instance attribute
        return compute_statistics(self.data)
```

**Invalidating cached value:**

```python
class Report:
    @cached_property
    def statistics(self) -> Statistics:
        return compute_statistics(self.data)

    def update_data(self, new_data: list[DataPoint]) -> None:
        self.data = new_data
        # Invalidate cached value
        if "statistics" in self.__dict__:
            del self.__dict__["statistics"]
```

Reference: [functools.cached_property documentation](https://docs.python.org/3/library/functools.html#functools.cached_property)

### 8.4 Use lru_cache for Expensive Pure Functions

**Impact: LOW-MEDIUM (eliminates redundant computation, O(1) cached lookups)**

`functools.lru_cache` memoizes function results, eliminating redundant computation for repeated calls with the same arguments.

**Incorrect (recomputes every call):**

```python
def calculate_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
    # fib(40) = 2^40 recursive calls
```

**Correct (memoized, linear complexity):**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
    # fib(40) = 40 unique calls
```

**Cache management:**

```python
@lru_cache(maxsize=1000)
def fetch_user_permissions(user_id: int) -> set[str]:
    return set(db.get_permissions(user_id))

# Check cache statistics
print(fetch_user_permissions.cache_info())

# Clear cache when data changes
fetch_user_permissions.cache_clear()
```

**Requirements for caching:**
- Function must be pure (same inputs → same outputs)
- Arguments must be hashable (no lists, dicts)

Reference: [functools.lru_cache documentation](https://docs.python.org/3/library/functools.html#functools.lru_cache)

---

## 9. Runtime Tuning

**Impact: LOW**

Python 3.11+ optimizations, interpreter settings, and micro-optimizations for hot paths provide incremental but measurable gains.

### 9.1 Avoid Repeated Global and Module Lookups

**Impact: LOW (10-20% improvement in tight loops)**

Global variable lookups are slower than local lookups. In performance-critical code, assign globals to locals or use direct imports.

**Incorrect (module lookup each iteration):**

```python
import math

def calculate_hypotenuse(pairs: list[tuple[float, float]]) -> list[float]:
    return [math.sqrt(x*x + y*y) for x, y in pairs]
    # math.sqrt lookup each iteration
```

**Correct (local reference):**

```python
import math

def calculate_hypotenuse(pairs: list[tuple[float, float]]) -> list[float]:
    sqrt = math.sqrt  # Single lookup
    return [sqrt(x*x + y*y) for x, y in pairs]
```

**Alternative (direct import):**

```python
from math import sqrt

def calculate_hypotenuse(pairs: list[tuple[float, float]]) -> list[float]:
    return [sqrt(x*x + y*y) for x, y in pairs]
```

**Note:** This optimization matters only in tight loops with millions of iterations. Profile first to confirm the lookup is a bottleneck.

Reference: [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)

### 9.2 Minimize Exception Handling in Hot Paths

**Impact: LOW (exceptions are 100× slower than conditionals)**

Exception handling is expensive compared to conditionals. In hot paths, use explicit checks instead of try/except for expected conditions.

**Incorrect (exception for expected case):**

```python
def get_value(data: dict, key: str) -> int:
    try:
        return data[key]
    except KeyError:
        return 0
    # KeyError raised and caught for every missing key
```

**Correct (conditional check):**

```python
def get_value(data: dict, key: str) -> int:
    return data.get(key, 0)
    # No exception overhead
```

**Incorrect (exception for type conversion):**

```python
def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None
```

**Correct (pre-validation for expected failures):**

```python
def parse_int(value: str) -> int | None:
    if value.lstrip("-").isdigit():
        return int(value)
    return None
```

**When exceptions are appropriate:**
- Truly exceptional conditions (file not found, network errors)
- Rare error cases where conditional would be complex
- When the check would duplicate the operation's work

Reference: [Python exception handling performance](https://docs.python.org/3/faq/design.html#how-fast-are-exceptions)

### 9.3 Profile Before Optimizing

**Impact: LOW (identifies actual bottlenecks, prevents wasted effort)**

Premature optimization wastes effort on non-bottlenecks. Profile code to identify actual performance issues before applying optimizations.

**Incorrect (optimizing without profiling):**

```python
# Spending hours optimizing a function that takes 0.1% of runtime
def get_user_name(user: User) -> str:
    return user.first_name + " " + user.last_name  # "Optimize" to f-string?
```

**Correct (profile first):**

```python
import cProfile
import pstats

def profile_function(func, *args, **kwargs):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()

    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    stats.print_stats(20)  # Top 20 functions
    return result

# Profile the actual slow operation
profile_function(process_large_dataset, dataset)
```

**Line profiler for detailed analysis:**

```python
# pip install line_profiler
# kernprof -l -v script.py

@profile
def slow_function(data: list[int]) -> int:
    total = 0
    for item in data:  # Line profiler shows time per line
        total += process_item(item)
    return total
```

**Memory profiling:**

```python
# pip install memory_profiler
# python -m memory_profiler script.py

from memory_profiler import profile

@profile
def memory_heavy_function():
    large_list = [i ** 2 for i in range(1000000)]
    return sum(large_list)
```

Reference: [cProfile documentation](https://docs.python.org/3/library/profile.html)

### 9.4 Upgrade to Python 3.11+ for Free Performance

**Impact: LOW (10-60% faster with zero code changes)**

Python 3.11 introduced significant interpreter optimizations. Upgrading provides 10-60% performance improvement with no code changes.

**Incorrect (running on Python 3.10):**

```python
# requirements.txt
python_requires = ">=3.10"

# pyproject.toml
[project]
requires-python = ">=3.10"
# Missing 10-60% free performance from newer interpreter
```

**Correct (targeting Python 3.11+):**

```python
# requirements.txt
python_requires = ">=3.11"

# pyproject.toml
[project]
requires-python = ">=3.11"
# Same code runs 10-60% faster with zero changes
```

**Version performance comparison:**

```python
# Same code, different Python versions:
# Python 3.10: 100ms baseline
# Python 3.11: 75ms (25% faster)
# Python 3.12: 70ms (30% faster)
# Python 3.13: 65ms (35% faster, with JIT potential)
```

**Check current version:**

```python
import sys
print(f"Python {sys.version_info.major}.{sys.version_info.minor}")
```

**Migration checklist:**
- Test with target Python version
- Update deprecated stdlib usage
- Check third-party library compatibility

Reference: [What's New in Python 3.11](https://docs.python.org/3/whatsnew/3.11.html)

---

## References

1. [https://docs.python.org/3/](https://docs.python.org/3/)
2. [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)
3. [https://docs.python.org/3/library/functools.html](https://docs.python.org/3/library/functools.html)
4. [https://docs.python.org/3/library/itertools.html](https://docs.python.org/3/library/itertools.html)
5. [https://docs.python.org/3/library/collections.html](https://docs.python.org/3/library/collections.html)
6. [https://docs.python.org/3/whatsnew/3.11.html](https://docs.python.org/3/whatsnew/3.11.html)
7. [https://docs.python.org/3/whatsnew/3.12.html](https://docs.python.org/3/whatsnew/3.12.html)
8. [https://docs.python.org/3/whatsnew/3.13.html](https://docs.python.org/3/whatsnew/3.13.html)
9. [https://wiki.python.org/moin/PythonSpeed/PerformanceTips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
10. [https://docs.python-guide.org/writing/style/](https://docs.python-guide.org/writing/style/)
11. [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
12. [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
13. [https://github.com/ijl/orjson](https://github.com/ijl/orjson)

---

## Source Files

This document was compiled from individual reference files. For detailed editing or extension:

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and impact ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for creating new rules |
| [SKILL.md](SKILL.md) | Quick reference entry point |
| [metadata.json](metadata.json) | Version and reference URLs |