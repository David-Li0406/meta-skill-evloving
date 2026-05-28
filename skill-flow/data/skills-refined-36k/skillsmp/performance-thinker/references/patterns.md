# Performance Thinker

## Patterns


---
  #### **Name**
Profile Before You Touch
  #### **Description**
Always measure before optimizing
  #### **When**
Any performance concern
  #### **Example**
    # THE GOLDEN RULE:
    # "Measure, don't guess" - applies everywhere
    
    # STEP 1: Establish baseline
    # What is current performance? Be specific.
    """
    Current: API endpoint /orders responds in 850ms p95
    Target: < 200ms p95
    Gap: ~650ms to eliminate
    """
    
    # STEP 2: Profile to find bottleneck
    # Use appropriate tools for your stack:
    
    # Node.js
    node --prof app.js
    node --prof-process isolate-*.log > profile.txt
    
    # Python
    python -m cProfile -o profile.stats app.py
    # Or: py-spy for production profiling
    
    # Go
    import _ "net/http/pprof"
    go tool pprof http://localhost:6060/debug/pprof/profile
    
    # Chrome DevTools for frontend
    # Performance tab → Record → Reproduce issue → Analyze
    
    # STEP 3: Identify the actual bottleneck
    """
    Profile shows:
    - Database query: 650ms (76%)
    - JSON serialization: 150ms (18%)
    - Everything else: 50ms (6%)
    
    Focus: Database query (not the code you thought!)
    """
    
    # STEP 4: Optimize the bottleneck
    # Only optimize what the profiler identified
    
    # STEP 5: Measure again
    """
    After adding index:
    - Database query: 50ms (was 650ms)
    - Total: 250ms (was 850ms)
    
    Close enough to target? Ship it.
    """
    

---
  #### **Name**
The Performance Pyramid
  #### **Description**
Optimize in order of impact
  #### **When**
Planning performance work
  #### **Example**
    # OPTIMIZE IN THIS ORDER (highest impact first):
    
    ## Level 1: Architecture (10x-1000x impact)
    - Wrong architecture (sync when should be async)
    - Missing caching layer
    - N+1 queries hitting database
    - Single-threaded when parallelizable
    - Wrong database for workload
    
    ## Level 2: Algorithms (10x-100x impact)
    - O(n²) when O(n) is possible
    - Linear search when hash lookup works
    - Repeated computation (cache results)
    - Wrong data structure (list vs set vs map)
    
    ## Level 3: I/O and Data (2x-10x impact)
    - Database query optimization (indexes!)
    - Batch vs individual operations
    - Connection pooling
    - Payload size reduction
    
    ## Level 4: Code (1.1x-2x impact)
    - Loop optimizations
    - Memory allocation reduction
    - Cache-friendly data layout
    - Language-specific tricks
    
    # THE INSIGHT:
    # Most developers jump to Level 4 when Level 1-2 problems exist.
    # Optimizing code is fun; fixing architecture is hard.
    # But a 2x code improvement can't fix a 100x architecture mistake.
    

---
  #### **Name**
The Right Cache Strategy
  #### **Description**
Cache thoughtfully with clear invalidation
  #### **When**
Adding caching
  #### **Example**
    # BEFORE CACHING, ASK:
    # 1. Can we just make it faster without cache?
    # 2. How often does the data change?
    # 3. What's the cost of stale data?
    # 4. What's the invalidation strategy?
    
    # CACHING PATTERNS:
    
    ## Cache-Aside (most common)
    async function getUser(id) {
      let user = await cache.get(`user:${id}`);
      if (!user) {
        user = await db.findUser(id);
        await cache.set(`user:${id}`, user, { ttl: 3600 });
      }
      return user;
    }
    # Invalidation: Delete key when user updates
    # Risk: Stale reads during TTL
    
    ## Write-Through
    async function updateUser(id, data) {
      const user = await db.updateUser(id, data);
      await cache.set(`user:${id}`, user);  # Update cache immediately
      return user;
    }
    # Pro: Cache always fresh
    # Con: Write latency increases
    
    ## Write-Behind (async write)
    async function updateUser(id, data) {
      await cache.set(`user:${id}`, data);  # Write to cache
      queue.enqueue({ type: 'updateUser', id, data });  # Async DB write
      return data;
    }
    # Pro: Fast writes
    # Con: Data loss risk, complex
    
    # INVALIDATION STRATEGIES:
    
    ## TTL-based (simple, accept staleness)
    cache.set(key, value, { ttl: 300 });  # Stale for up to 5 min
    
    ## Event-based (accurate, complex)
    eventBus.on('user:updated', (id) => cache.delete(`user:${id}`));
    
    ## Versioned keys (for heavy reads)
    const version = await getLatestVersion('users');
    cache.get(`user:${id}:v${version}`);
    

---
  #### **Name**
N+1 Query Detection and Fix
  #### **Description**
Catch and fix the most common database performance killer
  #### **When**
Database-backed applications
  #### **Example**
    # THE N+1 PROBLEM:
    
    # BAD: N+1 queries (1 + N queries)
    orders = db.query("SELECT * FROM orders")  # 1 query
    for order in orders:
        customer = db.query(  # N queries!
            "SELECT * FROM customers WHERE id = ?",
            order.customer_id
        )
        print(order.id, customer.name)
    
    # If 100 orders: 101 queries
    # If 10,000 orders: 10,001 queries (disaster!)
    
    # GOOD: Eager loading (2 queries total)
    orders = db.query("SELECT * FROM orders")  # 1 query
    customer_ids = [o.customer_id for o in orders]
    customers = db.query(  # 1 query
        "SELECT * FROM customers WHERE id IN (?)",
        customer_ids
    )
    customer_map = {c.id: c for c in customers}
    
    for order in orders:
        customer = customer_map[order.customer_id]
        print(order.id, customer.name)
    
    # DETECTION:
    # 1. Enable query logging
    # 2. Look for repeating similar queries
    # 3. Use ORM tools: Django debug toolbar, Bullet gem
    # 4. Monitor query counts per request
    
    # ORM SOLUTIONS:
    
    # Django
    Order.objects.select_related('customer').all()
    
    # Rails
    Order.includes(:customer).all
    
    # SQLAlchemy
    session.query(Order).options(joinedload(Order.customer))
    

---
  #### **Name**
Response Time Breakdown
  #### **Description**
Understand where time goes in a request
  #### **When**
Optimizing API endpoints
  #### **Example**
    # INSTRUMENT EVERYTHING:
    
    async function handleRequest(req) {
      const timing = {};
      const start = performance.now();
    
      // Auth
      const authStart = performance.now();
      const user = await authenticate(req);
      timing.auth = performance.now() - authStart;
    
      // Validation
      const validateStart = performance.now();
      const data = validate(req.body);
      timing.validation = performance.now() - validateStart;
    
      // Database
      const dbStart = performance.now();
      const result = await db.query(...);
      timing.database = performance.now() - dbStart;
    
      // Business logic
      const logicStart = performance.now();
      const processed = processResult(result);
      timing.logic = performance.now() - logicStart;
    
      // Serialization
      const serializeStart = performance.now();
      const response = JSON.stringify(processed);
      timing.serialization = performance.now() - serializeStart;
    
      timing.total = performance.now() - start;
    
      // Log breakdown
      console.log('Timing breakdown:', timing);
      // { auth: 5, validation: 2, database: 450, logic: 10, serialization: 30, total: 497 }
    
      return response;
    }
    
    # NOW YOU KNOW:
    # Database is 90% of time → optimize queries
    # Serialization is 6% → maybe worth looking at if DB is fixed
    # Auth/validation/logic are noise → ignore
    

---
  #### **Name**
Know When to Stop
  #### **Description**
Recognizing "fast enough"
  #### **When**
Deciding whether to continue optimizing
  #### **Example**
    # THE "FAST ENOUGH" FRAMEWORK:
    
    ## 1. Define your target BEFORE optimizing
    """
    Target: 95th percentile response time < 200ms
    Current: 850ms p95
    After optimization 1: 250ms p95
    After optimization 2: 180ms p95  ← STOP HERE
    """
    
    ## 2. Consider diminishing returns
    """
    Optimization 1: 3 hours work → 600ms improvement
    Optimization 2: 5 hours work → 70ms improvement
    Optimization 3: 20 hours work → 30ms improvement (estimated)
    
    Optimization 3 is probably not worth it.
    """
    
    ## 3. Factor in complexity cost
    """
    Current solution: Simple, maintainable
    Optimized solution: Adds caching layer, invalidation logic,
                        cache warming, monitoring
    
    Is 30ms improvement worth ongoing maintenance?
    """
    
    ## 4. User-perceptible thresholds
    """
    < 100ms: Feels instant
    100-300ms: Feels fast
    300-1000ms: Noticeable delay
    > 1000ms: Feels slow
    
    Going from 150ms to 80ms: Users won't notice
    Going from 1200ms to 400ms: Users will love it
    """
    
    ## 5. Business value check
    """
    Will this performance improvement:
    - Increase conversion? (measure it)
    - Reduce costs? (quantify it)
    - Enable new features? (what specifically?)
    - Prevent outages? (what's the risk?)
    
    If you can't answer these, the optimization might be premature.
    """
    

## Anti-Patterns


---
  #### **Name**
Premature Optimization
  #### **Description**
Optimizing before measuring or before it matters
  #### **Why**
    Knuth's famous quote: "Premature optimization is the root of all evil."
    Optimizing without profiling means you're probably optimizing the wrong thing.
    Optimizing before you have users means you're optimizing for imaginary load.
    
  #### **Instead**
Write clear code first. Measure when it's slow. Optimize the bottleneck.

---
  #### **Name**
Optimizing Without Profiling
  #### **Description**
Guessing where the bottleneck is
  #### **Why**
    Developer intuition about performance is almost always wrong. The bottleneck
    is rarely where you expect. Without profiling, you'll optimize irrelevant code
    while the actual bottleneck remains untouched.
    
  #### **Instead**
Always profile first. Let data guide optimization. Trust the profiler, not your gut.

---
  #### **Name**
Micro-optimization Obsession
  #### **Description**
Spending hours saving microseconds
  #### **Why**
    Saving 10μs in a function that runs once per request is meaningless when
    database queries take 100ms. Micro-optimizations are intellectually satisfying
    but rarely impact real performance.
    
  #### **Instead**
Focus on architectural and algorithmic improvements. Ignore microseconds until you've fixed milliseconds.

---
  #### **Name**
Cache Everything
  #### **Description**
Adding caches without considering invalidation
  #### **Why**
    Caches add complexity, staleness risks, and new failure modes. Cache invalidation
    is genuinely hard. Many caches are added without clear invalidation strategy and
    cause subtle bugs months later.
    
  #### **Instead**
Make the operation fast first. Add cache only when necessary. Plan invalidation upfront.

---
  #### **Name**
Big O Tunnel Vision
  #### **Description**
Choosing algorithms only by complexity class
  #### **Why**
    O(n) with small n often beats O(log n). Constants matter. Cache behavior matters.
    Memory allocation patterns matter. The theoretically optimal algorithm may be
    slower for your actual data.
    
  #### **Instead**
Benchmark with realistic data. Consider constants and practical factors, not just Big O.

---
  #### **Name**
Ignoring Memory
  #### **Description**
Focusing only on CPU while memory bloats
  #### **Why**
    Memory issues cause GC pauses, swapping, and OOM kills. A "fast" algorithm that
    allocates excessively can be slower than a "slow" algorithm that's memory-efficient.
    
  #### **Instead**
Profile memory alongside CPU. Watch for allocation patterns. Consider memory vs speed tradeoffs.