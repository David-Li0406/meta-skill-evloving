# Performance Thinker - Sharp Edges

## N+1 Query Problem - Death by a Thousand Queries

### **Id**
n-plus-one-queries
### **Severity**
critical
### **Situation**
  Page loads slowly. You check the database - thousands of queries per request.
  The ORM is fetching related records one at a time in a loop. Each query is fast,
  but together they're killing performance.
  
### **Why**
  ORMs make it easy to traverse relationships: order.customer.name. But each
  traversal might be a separate query. In a loop over 100 orders, that's 100
  extra queries. With nested relationships, it compounds.
  
### **Solution**
  1. Detect N+1 queries:
     - Enable query logging
     - Look for repeating similar queries
     - Use tools: Django Debug Toolbar, Bullet gem, etc.
  
  2. Fix with eager loading:
     ```python
     # Django: select_related for ForeignKey, prefetch_related for M2M
     Order.objects.select_related('customer').all()
  
     # Rails: includes
     Order.includes(:customer, :items).all()
  
     # SQLAlchemy: joinedload
     session.query(Order).options(joinedload(Order.customer))
     ```
  
  3. Monitor query count per request:
     - Alert when query count > threshold
     - Track p95 queries per endpoint
  
### **Symptoms**
  - Slow pages with many similar queries in logs
  - Query count grows with data size
  - Each query is fast but total is slow
  - Performance degrades as database grows
### **Detection Pattern**
for.*in.*query|\.all\(\).*for|loop.*database

## Premature Caching - Complexity Without Measurement

### **Id**
premature-caching
### **Severity**
high
### **Situation**
  Developer adds Redis cache "for performance." Now there's cache warming,
  invalidation bugs, stale data issues, and a new point of failure. The
  original operation took 50ms. Nobody measured if that was a problem.
  
### **Why**
  Caching adds significant complexity: invalidation strategy, consistency issues,
  another system to monitor, cache stampede risk, memory management. If you don't
  need the speedup, you're adding complexity for nothing.
  
### **Solution**
  1. Measure first:
     - What is current latency?
     - What is target latency?
     - Is caching the right solution?
  
  2. Try simpler solutions first:
     - Add database index
     - Optimize query
     - Reduce payload size
  
  3. If you must cache:
     - Plan invalidation upfront
     - Start with short TTL
     - Monitor cache hit rate
     - Prepare for cache failure
  
### **Symptoms**
  - Cache added without baseline measurements
  - No clear invalidation strategy
  - Stale data bugs appearing
  - Original operation wasn't actually slow
### **Detection Pattern**
redis|memcache|cache\.set|cache\.get

## Wrong Profiling Level - Measuring the Wrong Thing

### **Id**
wrong-profiling-level
### **Severity**
high
### **Situation**
  Micro-benchmark shows function is 100x faster after optimization. In production,
  nobody notices any difference. The function runs once per request and took 1ms.
  The database query that takes 500ms wasn't even measured.
  
### **Why**
  Micro-benchmarks isolate components from real context. That 100x improvement
  in a function that's 0.1% of request time is a 0.099% improvement overall.
  End-to-end measurement shows what actually matters to users.
  
### **Solution**
  1. Always measure end-to-end first:
     - What does the user experience?
     - What is the full request latency?
  
  2. Use profiling to find bottlenecks:
     - Profile the whole request, not individual functions
     - Look at percentage of time, not just absolute time
  
  3. Validate improvements end-to-end:
     - Micro-benchmark shows 100x improvement? Great.
     - What's the end-to-end improvement? That's what matters.
  
### **Symptoms**
  - Impressive micro-benchmark improvements
  - No noticeable production improvement
  - Optimizing code that's tiny fraction of total time
  - Missing the real bottleneck
### **Detection Pattern**
benchmark|micro.*benchmark|perf\.measure

## Memory Leak From Optimization - Cache That Grows Forever

### **Id**
memory-leak-optimization
### **Severity**
critical
### **Situation**
  Developer adds in-memory cache to speed up repeated lookups. Works great
  for a day. Then memory usage starts growing. A week later, OOM kills start.
  The cache has no size limit or eviction policy.
  
### **Why**
  In-memory caches without bounds grow forever. Each unique key adds an entry.
  Eventually, the cache contains data that will never be accessed again, but
  it's still consuming memory.
  
### **Solution**
  1. Always bound in-memory caches:
     ```javascript
     // Use LRU cache with size limit
     const cache = new LRUCache({ max: 1000 });
  
     // Or use TTL
     const cache = new Map();
     function set(key, value, ttl = 3600000) {
       cache.set(key, { value, expires: Date.now() + ttl });
       setTimeout(() => cache.delete(key), ttl);
     }
     ```
  
  2. Monitor memory usage:
     - Track heap size over time
     - Alert on growth trends
     - Profile memory periodically
  
  3. Prefer external caches for unbounded data:
     - Redis with memory limits
     - Memcached with eviction
  
### **Symptoms**
  - Memory usage grows over time
  - OOM kills after days/weeks of running
  - In-memory cache with no size limit
  - Performance degrades as memory fills
### **Detection Pattern**
new Map\(\)|= \{\}|cache.*=.*\{\}

## Missing Database Index - Full Table Scans

### **Id**
database-index-missing
### **Severity**
critical
### **Situation**
  Query is slow. EXPLAIN shows "Seq Scan" on a million-row table. The WHERE
  clause filters on a column that has no index. Adding an index makes the
  query 1000x faster.
  
### **Why**
  Without an index, the database must scan every row to find matches. With an
  index, it can jump directly to matching rows. This is the difference between
  O(n) and O(log n), but with very large constants.
  
### **Solution**
  1. Check EXPLAIN for your slow queries:
     ```sql
     EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123;
     -- Look for "Seq Scan" on large tables
     ```
  
  2. Add indexes on:
     - Columns in WHERE clauses
     - Columns in JOIN conditions
     - Columns in ORDER BY (if sorting large results)
  
  3. But don't over-index:
     - Each index slows writes
     - Indexes use disk space
     - Only index columns you actually filter on
  
### **Symptoms**
  - Queries slow on large tables
  - EXPLAIN shows sequential scans
  - Performance degrades as table grows
  - Writes are fast, reads are slow
### **Detection Pattern**
SELECT.*FROM.*WHERE|query.*slow|seq scan

## Synchronous Operations That Should Be Async

### **Id**
synchronous-when-async
### **Severity**
high
### **Situation**
  API endpoint takes 5 seconds because it sends an email, generates a PDF,
  and calls three external services - all synchronously. User waits for all
  of it before getting a response.
  
### **Why**
  Not everything needs to happen before responding to the user. Email can be
  queued. PDF can be generated later. External calls that aren't needed for
  the response can happen asynchronously.
  
### **Solution**
  1. Identify what must be synchronous:
     - What does the user need in the response?
     - Everything else can be async
  
  2. Use queues for background work:
     ```python
     # Instead of:
     def create_order(order):
         save_order(order)
         send_confirmation_email(order)  # 1 second
         notify_warehouse(order)  # 2 seconds
         generate_invoice_pdf(order)  # 3 seconds
         return order
  
     # Do this:
     def create_order(order):
         save_order(order)
         queue.enqueue('send_confirmation_email', order.id)
         queue.enqueue('notify_warehouse', order.id)
         queue.enqueue('generate_invoice_pdf', order.id)
         return order  # Immediate response
     ```
  
  3. Use async/await for parallelizable I/O:
     ```javascript
     // Instead of sequential:
     const a = await fetchA();
     const b = await fetchB();
     const c = await fetchC();
  
     // Parallel when possible:
     const [a, b, c] = await Promise.all([
       fetchA(),
       fetchB(),
       fetchC()
     ]);
     ```
  
### **Symptoms**
  - Slow endpoints doing multiple operations
  - User waiting for non-essential work
  - External API calls blocking responses
  - Obvious parallelization opportunities missed
### **Detection Pattern**
await.*await.*await|sendEmail.*return|notify.*before.*return

## Unbounded Queries - Loading Everything

### **Id**
pagination-without-limits
### **Severity**
high
### **Situation**
  Admin page loads all 500,000 users into memory to display in a table.
  API endpoint returns all matching records with no limit. The system
  worked fine with 100 records, crashes with 100,000.
  
### **Why**
  Code that loads "all" records assumes a small dataset. As data grows,
  memory explodes, queries time out, and responses become enormous.
  What works in development fails in production.
  
### **Solution**
  1. Always paginate:
     ```python
     # Never:
     users = User.objects.all()
  
     # Always:
     users = User.objects.all()[:100]  # Or use proper pagination
     ```
  
  2. Set hard limits on APIs:
     ```javascript
     const limit = Math.min(req.query.limit || 20, 100);
     const results = await db.query(...).limit(limit);
     ```
  
  3. Use cursor pagination for large datasets:
     ```sql
     -- Instead of OFFSET (slow for large offsets):
     SELECT * FROM users WHERE id > last_seen_id ORDER BY id LIMIT 20;
     ```
  
### **Symptoms**
  - Works in dev, crashes in production
  - Out of memory on large datasets
  - Slow queries on tables that grew
  - No LIMIT in queries
### **Detection Pattern**
\.all\(\)|\.find\(\{\}\)|SELECT.*FROM.*(?!LIMIT)

## Serialization Overhead - JSON All The Things

### **Id**
serialization-overhead
### **Severity**
medium
### **Situation**
  API returns a user object. The response includes every field, every related
  object, deeply nested. The JSON is 50KB when the client only needs 500 bytes.
  Serialization takes 100ms.
  
### **Why**
  Serializing large objects is expensive. Sending large payloads is expensive.
  Parsing large payloads on the client is expensive. Most of the data is often
  unused.
  
### **Solution**
  1. Return only what's needed:
     ```python
     # Instead of:
     return user.to_dict()  # Everything
  
     # Use:
     return {
       'id': user.id,
       'name': user.name,
       'email': user.email
     }  # Only what's needed
     ```
  
  2. Implement sparse fieldsets:
     ```
     GET /users/123?fields=id,name,email
     ```
  
  3. Consider binary formats for internal services:
     - Protocol Buffers
     - MessagePack
     - CBOR
  
### **Symptoms**
  - Large JSON responses
  - High serialization CPU usage
  - Slow responses despite fast queries
  - Clients receiving unused data
### **Detection Pattern**
to_json|to_dict|JSON\.stringify|serialize

## Connection Pool Exhaustion - Running Out of Connections

### **Id**
connection-pool-exhaustion
### **Severity**
critical
### **Situation**
  Under load, errors appear: "connection pool exhausted" or "too many connections."
  Each request opens a new database connection. The pool fills up. New requests
  wait or fail.
  
### **Why**
  Database connections are expensive resources. Without pooling, each request
  creates and destroys a connection. With pooling but wrong settings, the pool
  can be exhausted under load.
  
### **Solution**
  1. Use connection pooling:
     ```python
     # SQLAlchemy
     engine = create_engine(url, pool_size=10, max_overflow=20)
  
     # Node.js pg
     const pool = new Pool({ max: 20 });
     ```
  
  2. Size pool appropriately:
     - Too small: Requests wait for connections
     - Too large: Database overloaded
     - Rule of thumb: connections = (cores * 2) + spindles
  
  3. Always return connections:
     ```python
     # Use context managers
     with engine.connect() as conn:
         conn.execute(...)
     # Connection automatically returned
     ```
  
### **Symptoms**
  - "Connection pool exhausted" errors
  - Requests timing out waiting for connections
  - Database showing too many connections
  - Works at low load, fails at high load
### **Detection Pattern**
connection.*pool|pool.*exhausted|too many connections