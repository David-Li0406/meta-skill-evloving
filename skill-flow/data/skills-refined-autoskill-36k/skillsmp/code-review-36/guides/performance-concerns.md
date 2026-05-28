# Performance Concerns Guide

Patterns that cause performance degradation, resource exhaustion, or system instability. Catch these during code review before they reach production.

---

## Algorithmic Complexity

### Accidental Quadratic (O(n²))

The most common performance bug. Often hidden behind innocent-looking code.

**Vulnerable:**

```python
def remove_duplicates(items: list[str]) -> list[str]:
    result = []
    for item in items:
        if item not in result:  # O(n) lookup in list
            result.append(item)
    return result
# Total: O(n²)
```

**Efficient:**

```python
def remove_duplicates(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:  # O(1) lookup in set
            seen.add(item)
            result.append(item)
    return result
# Total: O(n)

# Or if order doesn't matter:
def remove_duplicates(items: list[str]) -> list[str]:
    return list(set(items))
```

**Common O(n²) patterns to flag:**

| Pattern | Problem |
|---------|---------|
| `if x in list` inside loop | Use set for membership |
| `list.index(x)` inside loop | Use dict for lookup |
| Nested loops over same collection | Often avoidable |
| String concatenation in loop | Use `''.join()` or list |
| `list.insert(0, x)` in loop | Use `collections.deque` |
| Repeated list slicing | Slice once, iterate |

**String concatenation trap:**

```python
# O(n²) - each += creates new string
def build_report(lines: list[str]) -> str:
    result = ""
    for line in lines:
        result += line + "\n"
    return result

# O(n) - join allocates once
def build_report(lines: list[str]) -> str:
    return "\n".join(lines)
```

### Hidden Complexity in Libraries

**Vulnerable:**

```python
import pandas as pd

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    for idx, row in df.iterrows():  # Already slow
        if row['status'] == 'pending':
            df.loc[idx, 'status'] = 'processed'  # O(n) per assignment
    return df
# Total: O(n²)
```

**Efficient:**

```python
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df['status'] == 'pending', 'status'] = 'processed'
    return df
# Total: O(n)
```

**Review checklist:**
- [ ] No `in` checks against lists inside loops
- [ ] No `list.index()` inside loops
- [ ] No string concatenation with `+=` in loops
- [ ] DataFrame operations vectorised, not row-by-row
- [ ] Regex compiled outside loops (`re.compile`)
- [ ] Sorting not repeated unnecessarily

---

## Resource Leaks

### Unclosed File Handles

**Vulnerable:**

```python
def read_config(path: str) -> dict:
    f = open(path)
    data = json.load(f)
    # f.close() never called if json.load raises
    return data
```

**Secure:**

```python
def read_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
```

### Database Connection Leaks

**Vulnerable:**

```python
def get_users() -> list[User]:
    conn = database.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
    # Connection never returned to pool
```

**Secure:**

```python
def get_users() -> list[User]:
    with database.connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
```

### Memory Leaks

**Vulnerable (circular reference with prevent garbage collection):**

```python
class Node:
    def __init__(self):
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        child.parent = self  # Circular reference
        self.children.append(child)
```

**Secure:**

```python
import weakref

class Node:
    def __init__(self):
        self.children = []
        self._parent = None
    
    @property
    def parent(self):
        return self._parent() if self._parent else None
    
    def add_child(self, child):
        child._parent = weakref.ref(self)  # Weak reference
        self.children.append(child)
```

**Vulnerable (unbounded cache):**

```python
_cache = {}

def expensive_lookup(key: str) -> Result:
    if key not in _cache:
        _cache[key] = compute_expensive_result(key)
    return _cache[key]
# Cache grows without bound
```

**Secure:**

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_lookup(key: str) -> Result:
    return compute_expensive_result(key)
```

**Review checklist:**
- [ ] Files opened with `with` statement
- [ ] Database connections returned to pool
- [ ] Caches have size limits
- [ ] Event listeners removed when objects destroyed
- [ ] Circular references use `weakref`
- [ ] Temporary files cleaned up (`tempfile` module)

---

## Bad Neighbour Problems

Code that affects other processes, services, or users sharing the same resources.

### Unbounded Memory Consumption

**Vulnerable:**

```python
def process_upload(file) -> dict:
    content = file.read()  # Loads entire file into memory
    return parse_large_file(content)

# 10GB upload = 10GB memory consumption = OOM killer visits
```

**Secure:**

```python
def process_upload(file, chunk_size: int = 8192) -> dict:
    result = StreamingParser()
    while chunk := file.read(chunk_size):
        result.feed(chunk)
    return result.finalize()
```

### Unbounded Query Results

**Vulnerable:**

```python
@app.route("/api/logs")
def get_logs():
    return LogEntry.query.all()  # Returns millions of rows

# One request exhausts database connection pool and memory
```

**Secure:**

```python
@app.route("/api/logs")
def get_logs():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 100, type=int), 1000)
    return LogEntry.query.paginate(page=page, per_page=per_page)
```

### CPU Monopolisation

**Vulnerable:**

```python
def search(pattern: str, text: str) -> bool:
    # ReDoS: catastrophic backtracking
    return bool(re.match(r'(a+)+$', text))

# Input "aaaaaaaaaaaaaaaaaaaaaaaaaaaaab" hangs for minutes
```

**Secure:**

```python
import re2  # Google's RE2 library - guaranteed linear time

def search(pattern: str, text: str) -> bool:
    return bool(re2.match(r'(a+)+$', text))
```

Or set timeouts:

```python
import signal

def search_with_timeout(pattern: str, text: str, timeout: int = 1) -> bool:
    def handler(signum, frame):
        raise TimeoutError("Regex took too long")
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    try:
        return bool(re.match(pattern, text))
    finally:
        signal.alarm(0)
```

### Blocking the Event Loop

**Vulnerable (Node.js/async Python):**

```javascript
app.get('/api/hash', (req, res) => {
    // Blocks event loop for seconds
    const hash = crypto.pbkdf2Sync(req.body.password, salt, 100000, 64, 'sha512');
    res.json({ hash: hash.toString('hex') });
});
```

**Secure:**

```javascript
app.get('/api/hash', async (req, res) => {
    // Non-blocking
    const hash = await crypto.pbkdf2(req.body.password, salt, 100000, 64, 'sha512');
    res.json({ hash: hash.toString('hex') });
});
```

**Review checklist:**
- [ ] Large data processed in streams/chunks
- [ ] Query results paginated
- [ ] Regex patterns reviewed for catastrophic backtracking
- [ ] CPU-intensive work offloaded to worker threads/processes
- [ ] Timeouts on all external calls
- [ ] Rate limiting on expensive endpoints

---

## Database Performance

### N+1 Queries

**Vulnerable:**

```python
def get_orders_with_items():
    orders = Order.query.all()  # 1 query
    for order in orders:
        items = order.items  # N queries (lazy load)
        yield order, items
```

**Secure:**

```python
def get_orders_with_items():
    orders = Order.query.options(
        joinedload(Order.items)  # Eager load in 1 query
    ).all()
    for order in orders:
        yield order, order.items
```

### Missing Indexes

**Vulnerable:**

```python
# Frequently called with user_id filter
def get_user_orders(user_id: int) -> list[Order]:
    return Order.query.filter_by(user_id=user_id).all()

# Without index: full table scan every time
```

**Check for:**

```sql
-- Does index exist?
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;

-- If "Seq Scan", add index:
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Inefficient Queries

**Vulnerable:**

```python
# Fetches all columns when only one needed
def get_user_emails() -> list[str]:
    users = User.query.all()
    return [u.email for u in users]
```

**Efficient:**

```python
def get_user_emails() -> list[str]:
    return [email for (email,) in db.session.query(User.email).all()]
```

**Review checklist:**
- [ ] Eager loading for known access patterns
- [ ] Queries use only needed columns
- [ ] Filters on indexed columns
- [ ] `EXPLAIN ANALYZE` for complex queries
- [ ] Batch operations instead of row-by-row
- [ ] Connection pooling configured

---

## Network Performance

### Chatty APIs

**Vulnerable:**

```python
def get_dashboard_data(user_id: int) -> dict:
    user = api.get(f"/users/{user_id}")
    orders = api.get(f"/users/{user_id}/orders")
    notifications = api.get(f"/users/{user_id}/notifications")
    recommendations = api.get(f"/users/{user_id}/recommendations")
    # 4 sequential HTTP requests
    return {**user, 'orders': orders, ...}
```

**Efficient:**

```python
import asyncio

async def get_dashboard_data(user_id: int) -> dict:
    user, orders, notifications, recommendations = await asyncio.gather(
        api.get(f"/users/{user_id}"),
        api.get(f"/users/{user_id}/orders"),
        api.get(f"/users/{user_id}/notifications"),
        api.get(f"/users/{user_id}/recommendations"),
    )
    # 4 parallel requests
    return {**user, 'orders': orders, ...}
```

Or provide a batch endpoint:

```python
# Single request
dashboard = api.get(f"/users/{user_id}/dashboard")
```

### Missing Timeouts

**Vulnerable:**

```python
def fetch_data(url: str) -> dict:
    response = requests.get(url)  # Hangs forever if server unresponsive
    return response.json()
```

**Secure:**

```python
def fetch_data(url: str) -> dict:
    response = requests.get(url, timeout=(3.05, 27))  # (connect, read)
    response.raise_for_status()
    return response.json()
```

**Review checklist:**
- [ ] All HTTP requests have timeouts
- [ ] Parallel requests where possible
- [ ] Retry logic with exponential backoff
- [ ] Circuit breakers for failing dependencies
- [ ] Response size limits

---

## Memory Efficiency

### Unnecessary Copies

**Vulnerable:**

```python
def process_large_list(items: list[int]) -> list[int]:
    # Creates intermediate list
    doubled = [x * 2 for x in items]
    # Creates another intermediate list  
    filtered = [x for x in doubled if x > 100]
    return filtered
```

**Efficient:**

```python
def process_large_list(items: list[int]) -> Iterator[int]:
    # Generator - no intermediate allocations
    return (x * 2 for x in items if x * 2 > 100)
```

### Large Object Retention

**Vulnerable:**

```python
def analyze_logs(log_files: list[str]) -> Report:
    all_logs = []
    for path in log_files:
        with open(path) as f:
            all_logs.extend(json.load(f))  # Accumulates everything
    
    return generate_report(all_logs)
```

**Efficient:**

```python
def analyze_logs(log_files: list[str]) -> Report:
    report = ReportBuilder()
    for path in log_files:
        with open(path) as f:
            for entry in ijson.items(f, 'item'):  # Stream JSON
                report.add_entry(entry)
    return report.build()
```

**Review checklist:**
- [ ] Generators for large sequences
- [ ] Streaming for large files
- [ ] Data discarded after processing
- [ ] `__slots__` for memory-constrained classes
- [ ] NumPy views instead of copies where safe

---

## Concurrency Issues

### Lock Contention

**Vulnerable:**

```python
import threading

lock = threading.Lock()
counter = 0

def increment():
    global counter
    with lock:
        # Lock held during slow I/O
        log_to_remote_server(f"Incrementing from {counter}")
        counter += 1
```

**Efficient:**

```python
def increment():
    global counter
    
    # Do I/O outside lock
    current = None
    with lock:
        current = counter
        counter += 1
    
    log_to_remote_server(f"Incremented from {current}")
```

### Thread Pool Exhaustion

**Vulnerable:**

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)

def handle_request(request):
    # Submits work that submits more work
    future = executor.submit(process, request)
    # process() also calls executor.submit()
    # Deadlock when all workers waiting on pending tasks
```

**Review checklist:**
- [ ] Locks held for minimal duration
- [ ] No I/O while holding locks
- [ ] Thread pools sized appropriately
- [ ] No recursive task submission to bounded pools
- [ ] Async I/O for I/O-bound workloads

---

## Startup & Initialisation

### Eager Loading

**Vulnerable:**

```python
# module.py
import expensive_library  # Loaded on import

PRECOMPUTED_DATA = load_gigabytes_of_data()  # Runs at import time

def rarely_used_function():
    return process(PRECOMPUTED_DATA)
```

**Efficient:**

```python
# Lazy loading
_expensive_library = None
_precomputed_data = None

def _get_library():
    global _expensive_library
    if _expensive_library is None:
        import expensive_library
        _expensive_library = expensive_library
    return _expensive_library

def rarely_used_function():
    global _precomputed_data
    if _precomputed_data is None:
        _precomputed_data = load_gigabytes_of_data()
    return process(_precomputed_data)
```

**Review checklist:**
- [ ] Heavy imports deferred until needed
- [ ] Large data loaded lazily
- [ ] Startup path profiled
- [ ] Health checks don't trigger expensive initialisation

---

## Profiling Commands

When performance issues are suspected, use these to investigate:

```bash
# Python CPU profiling
python -m cProfile -o profile.out script.py
python -m pstats profile.out

# Python memory profiling
pip install memory_profiler
python -m memory_profiler script.py

# Line-by-line profiling
pip install line_profiler
kernprof -l -v script.py

# Rust
cargo flamegraph

# Node.js
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# General system
time command
/usr/bin/time -v command  # Detailed (GNU time)
```
