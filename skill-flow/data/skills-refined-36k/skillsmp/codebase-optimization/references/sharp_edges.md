# Codebase Optimization - Sharp Edges

## Premature Optimization

### **Id**
premature-optimization
### **Summary**
Optimizing code before measuring or validating the problem
### **Severity**
critical
### **Situation**
Developer optimizes code that "looks slow" without profiling
### **Why**
  Wastes time, adds complexity, often makes things worse. Intuition about
  bottlenecks is often wrong. Most code doesn't need optimization.
  
### **Solution**
  # OPTIMIZATION PROCESS
  1. MEASURE: Profile the actual system
  2. IDENTIFY: Find the real bottleneck
  3. VALIDATE: Confirm it's worth optimizing
  4. OPTIMIZE: Make targeted change
  5. MEASURE: Verify improvement
  6. MONITOR: Watch for regressions
  
  # Before any optimization, ask:
  - What's the measured problem?
  - How much time/resources does it take?
  - What's the expected improvement?
  - Is it worth the complexity cost?
  
  # RULES
  - Profile before optimizing
  - Target the 20% causing 80% of issues
  - Simple code > clever code
  - Readability > micro-optimization
  
  # WHEN TO OPTIMIZE
  - Measured performance problem
  - User-impacting issue
  - Cost/resource constraint
  - Known algorithmic issue (O(n²) on large n)
  
  # WHEN NOT TO OPTIMIZE
  - "Looks slow"
  - "Could be faster"
  - "Best practice"
  - "I know a better way"
  
### **Symptoms**
  - No profiling data
  - Complex "optimized" code
  - Minimal improvement
  - Regression in readability
### **Detection Pattern**


## Big Bang Rewrite

### **Id**
big-bang-rewrite
### **Summary**
Rewriting large portions of the codebase at once
### **Severity**
critical
### **Situation**
Team decides to rewrite entire system instead of incremental improvement
### **Why**
  High risk, long timeline, often fails or never finishes. Statistics: 70% of
  rewrites fail or are abandoned. Average: 3x longer than estimated. Often
  reintroduce old bugs. Team morale destroyed.
  
### **Solution**
  # STRANGLER FIG PATTERN
  Build new alongside old
  Migrate piece by piece
  Route traffic gradually
  Old system can stay working
  
  # SAFE REWRITE APPROACH
  Week 1: New auth module, behind flag
  Week 2: 1% traffic to new auth
  Week 3: 10% traffic, monitor
  Week 4: 50% traffic
  Week 5: 100% traffic
  Week 6: Remove old auth
  
  # NOT
  Month 1-6: Rewrite everything
  Month 7: Pray it works
  Month 8: Debug production fires
  
  # INCREMENTAL REFACTORING
  Improve as you go
  Boy scout rule
  No big bang
  Continuous improvement
  
  # CLEARLY BOUNDED REWRITES
  One module at a time
  Defined interface
  Ship to production
  Then next module
  
### **Symptoms**
  - Multi-month rewrite projects
  - Original system still in production
  - Feature parity gaps
  - Team exhaustion
### **Detection Pattern**


## Optimization Without Tests

### **Id**
optimization-without-tests
### **Summary**
Refactoring or optimizing without adequate test coverage
### **Severity**
critical
### **Situation**
Developer refactors code without tests as safety net
### **Why**
  No safety net means you don't know what you broke. Edge cases break.
  Customer data corrupted. "But it worked in my testing..."
  
### **Solution**
  # TEST FIRST
  Write tests before refactoring
  Characterization tests capture behavior
  Then refactor with confidence
  
  # CHARACTERIZATION TEST EXAMPLE
  // Before understanding the code
  test('calculatePrice current behavior', () => {
    // Record what it currently does
    expect(calculatePrice(100, 'premium')).toBe(85)
    expect(calculatePrice(100, 'basic')).toBe(100)
    expect(calculatePrice(0, 'premium')).toBe(0)
    expect(calculatePrice(-1, 'basic')).toBe(0) // Edge case!
    // Now you know what to preserve
  })
  
  # GOLDEN MASTER TESTING
  For complex/unknown code:
  1. Record current outputs
  2. Run refactored code
  3. Compare outputs
  4. Any difference = potential bug
  
  # MINIMUM TEST COVERAGE
  - Happy path tested
  - Edge cases covered
  - Error paths verified
  - Performance baseline if relevant
  
  NO TESTS = NO REFACTOR.
  
### **Symptoms**
  - Refactoring untested code
  - Post-deploy bugs
  - Missing edge case coverage
  - It worked locally
### **Detection Pattern**


## Hidden Side Effect

### **Id**
hidden-side-effect
### **Summary**
Optimization changes behavior in unexpected ways
### **Severity**
critical
### **Situation**
Code behavior changes due to optimization (e.g., sync to async)
### **Why**
  Side effects are everywhere. Order matters more than you think.
  "Equivalent" isn't always equivalent. Logging gone, notifications wrong
  order, analytics broken.
  
### **Solution**
  # ORIGINAL CODE
  function processItems(items) {
    items.forEach(item => {
      process(item)      // Sync, sequential
      logItem(item)      // Logging happens
      notifyWatchers()   // Side effect
    })
  }
  
  # "OPTIMIZED" CODE (BROKEN)
  function processItems(items) {
    await Promise.all(items.map(item =>
      process(item)      // Now parallel!
    ))
    // Logging gone, notifications wrong order
  }
  
  # HIDDEN SIDE EFFECTS
  - Logging and monitoring
  - Analytics and tracking
  - Cache updates
  - Event emissions
  - State mutations
  - Database writes
  - External API calls
  
  # THE FIX
  1. Document side effects
  // SIDE EFFECTS: Updates cache, logs to analytics
  function saveUser(user) { ... }
  
  2. Test for side effects
  test('saveUser logs analytics event', () => {
    saveUser(testUser)
    expect(analytics.track).toHaveBeenCalledWith('user_saved')
  })
  
  3. Check after optimization
  - Same logs generated?
  - Same events emitted?
  - Same external calls made?
  - Same error behavior?
  
### **Symptoms**
  - Missing logs after optimization
  - Analytics discrepancies
  - Event order changes
  - Downstream system breakage
### **Detection Pattern**
Promise\\.all.*forEach|async.*map.*await

## Memory Leak Introduction

### **Id**
memory-leak-introduction
### **Summary**
Optimization introduces memory leaks
### **Severity**
critical
### **Situation**
Caching or optimization causes memory to grow unbounded
### **Why**
  Slow degradation, crashes, hard to diagnose. Runs for 2 weeks then OOM.
  Caches without limits are memory leaks.
  
### **Solution**
  # UNBOUNDED CACHE (WRONG)
  const cache = new Map()
  function getData(id) {
    if (!cache.has(id)) {
      cache.set(id, expensiveQuery(id))
    }
    return cache.get(id)
  }
  // Grows forever, OOM after weeks
  
  # BOUNDED CACHE (RIGHT)
  const cache = new LRUCache({ max: 1000, ttl: 3600000 })
  
  # EVENT LISTENER LEAK
  // WRONG
  window.addEventListener('resize', handler)
  // Component unmounts, handler stays
  
  // RIGHT
  useEffect(() => {
    window.addEventListener('resize', handler)
    return () => window.removeEventListener('resize', handler)
  }, [])
  
  # CLOSURE LEAK
  function setup() {
    const bigData = loadBigData()
    return () => {
      // bigData held in closure forever
    }
  }
  
  # THE FIX
  1. Set cache limits and TTLs
  2. Clean up event listeners
  3. Cancel subscriptions
  4. Clear intervals/timeouts
  5. Profile memory over time
  6. Test for leaks with long runs
  
### **Symptoms**
  - Memory grows over time
  - OOM crashes after days/weeks
  - Unbounded Map/Set/Array growth
  - Missing cleanup functions
### **Detection Pattern**
new Map\\(\\)|new Set\\(\\)|cache\\s*=\\s*\\{\\}

## Dependency Upgrade Disaster

### **Id**
dependency-upgrade-disaster
### **Summary**
Upgrading dependencies without understanding breaking changes
### **Severity**
high
### **Situation**
Mass dependency update without testing or reading changelogs
### **Why**
  Subtle bugs, security issues, production failures. Breaking changes don't
  always fail tests. Even minor versions can break things.
  
### **Solution**
  # UPGRADE PROCESS
  1. ONE AT A TIME
     Upgrade one dependency
     Run full test suite
     Manual testing if needed
     Ship, monitor
     Then next dependency
  
  2. READ CHANGELOGS
     What changed?
     Breaking changes?
     Migration guide?
     Known issues?
  
  3. TEST THOROUGHLY
     - All tests pass
     - Manual smoke test
     - Check specific features
     - Performance comparison
  
  4. HAVE ROLLBACK PLAN
     Lock file in version control
     Know how to downgrade
     Monitor after deploy
  
  # package.json - Lock versions
  "dependencies": {
    "react": "18.2.0",      // Exact version
    "lodash": "~4.17.21",   // Patch only
    "express": "^4.18.0"    // Minor okay
  }
  
  # UPGRADE PRIORITY
  1. Security patches (ASAP)
  2. Bug fixes (soon)
  3. Features (when needed)
  4. Major versions (carefully planned)
  
### **Symptoms**
  - Mass npm update
  - No changelog review
  - Post-upgrade bugs
  - Unexpected behavior changes
### **Detection Pattern**
npm update|yarn upgrade(?!.*--)

## Premature Abstraction

### **Id**
premature-abstraction
### **Summary**
Creating abstractions before patterns emerge
### **Severity**
high
### **Situation**
Creating generic solution from first use case
### **Why**
  Wrong abstraction is worse than no abstraction. Harder to change later.
  "Duplication is far cheaper than the wrong abstraction." - Sandi Metz
  
### **Solution**
  # RULE OF THREE
  1st occurrence: Just write it
  2nd occurrence: Note the duplication
  3rd occurrence: NOW abstract
  
  # THE FIX
  1. DUPLICATION IS OKAY
     Until you see the pattern
     Copy-paste is fine temporarily
     Wrong abstraction is worse
  
  2. WAIT FOR CLARITY
     What's actually common?
     What varies?
     What's the stable interface?
  
  3. EXTRACT, DON'T PREDICT
     // Bad: Predict future needs
     function createDataFetcher({
       cache, retry, timeout, transform,
       onError, onSuccess, ...maybeMore
     })
  
     // Good: Extract what you need now
     function fetchUserData(userId) {
       // Simple, specific
     }
  
  # SIGNALS OF WRONG ABSTRACTION
  - Options/params growing
  - If/else for different cases
  - Callers working around it
  - Nobody understands it
  
### **Symptoms**
  - Many configuration options
  - Conditionals inside abstraction
  - Workarounds in calling code
  - Overly generic names
### **Detection Pattern**
options\\?:|config\\?:|settings\\?:

## Broken Incremental Migration

### **Id**
broken-incremental-migration
### **Summary**
Starting a migration that never finishes
### **Severity**
high
### **Situation**
Migration paused indefinitely, two systems maintained forever
### **Why**
  Incomplete migrations compound costs. Every day with two systems:
  double maintenance, double bugs, double confusion, double documentation.
  
### **Solution**
  # COMMIT TO COMPLETION
  Migration isn't done until old is gone
  Set deadline, make it real
  No new features on old system
  
  # TIMEBOX STRICTLY
  Max 3 months for any migration
  If not done, evaluate:
  - Finish faster
  - Abandon migration
  - But not "pause indefinitely"
  
  # FEATURE FREEZE OLD SYSTEM
  All new work on new system
  Bug fixes only on old
  Creates pressure to finish
  
  # INCREMENTAL DONE RIGHT
  Week 1: Migrate + remove Module A
  Week 2: Migrate + remove Module B
  Week 3: Migrate + remove Module C
  Week 4: Old system deleted
  
  # NOT
  Month 1: Migrate Module A
  Month 6: Migrate Module B
  Month 12: What were we migrating again?
  
  # TRACK PROGRESS VISIBLY
  Migration: 60% complete
  Deadline: March 15
  Remaining: 4 modules
  Owner: @person
  
### **Symptoms**
  - Two systems running
  - Migration paused months ago
  - New features on old system
  - No migration deadline
### **Detection Pattern**


## Performance Cliff

### **Id**
performance-cliff
### **Summary**
Optimization works until a threshold, then fails catastrophically
### **Severity**
high
### **Situation**
Works in testing, fails at production scale
### **Why**
  Linear testing misses exponential failures. O(n) looks fine at n=100,
  O(n²) explodes at n=10000. Cache hit: 1ms, cache miss: 500ms.
  
### **Solution**
  # COMMON CLIFFS
  ALGORITHMIC: O(n) fine at 100, O(n²) explodes at 10000
  MEMORY: Fits in RAM = fast, swaps to disk = 1000x slower
  CACHE: Hit = 1ms, miss = 500ms
  CONCURRENT: 1 connection works, 100 connections deadlock
  
  # THE FIX
  1. TEST AT SCALE
     Test with production-like data volumes
     Test with production-like traffic
     Test at 10x expected load
  
  2. IDENTIFY CLIFFS
     What happens when cache misses?
     What if this grows 10x?
     What if all requests arrive at once?
  
  3. GRACEFUL DEGRADATION
     // Bad: Works or fails
     return cache.get(key) || loadFromDB(key)
  
     // Better: Degrades gracefully
     try {
       return cache.get(key)
     } catch {
       return fallbackValue  // Fast fallback
     }
  
  4. CIRCUIT BREAKERS
     Fail fast when overwhelmed
     Don't cascade failures
  
  5. LOAD SHEDDING
     When overloaded: reject new requests gracefully
     Instead of trying and failing slowly
  
### **Symptoms**
  - Works in testing, fails in prod
  - Timeout at high load
  - Performance varies wildly
  - Cascading failures
### **Detection Pattern**
O\\(n\\^2\\)|O\\(n\\*n\\)|nested.*forEach

## Optimization Coupling

### **Id**
optimization-coupling
### **Summary**
Performance optimization tightly couples components
### **Severity**
high
### **Situation**
Breaking module boundaries for performance gains
### **Why**
  Trades future velocity for current speed. Technical debt with interest.
  Harder to change, harder to understand, harder to test.
  
### **Solution**
  # BAD: Bypass for performance
  UserService → Database (direct SQL)
  UserService knows about table structure
  Repository bypassed for "performance"
  
  # BETTER: Optimize within boundaries
  class UserRepository {
    findWithPreload() {
      return this.query()
        .preload('profile')
        .preload('settings')
    }
  }
  
  # COUPLING EXAMPLES TO AVOID
  - Direct DB access bypassing ORM
  - Shared mutable state for speed
  - Inlined code for call reduction
  - Global variables for access
  - Breaking module boundaries
  
  # THE FIX
  1. OPTIMIZE WITHIN BOUNDARIES
     Make Repository faster
     Don't bypass Repository
  
  2. CACHE AT BOUNDARIES
     Cache interface results
     Not internal state
  
  3. MEASURE THE COST
     How much speed gained?
     How much coupling added?
     Is it worth the trade-off?
  
  4. DOCUMENT THE DEBT
     // PERF: Direct SQL for 10x speedup
     // TODO: Refactor when ORM supports batch load
     // Added: 2024-01-15, Owner: @person
  
### **Symptoms**
  - Direct database access
  - Bypassed abstractions
  - Global state for performance
  - Tightly coupled modules
### **Detection Pattern**
db\\.raw|db\\.query|sql`

## Metrics Lie

### **Id**
metrics-lie
### **Summary**
Optimizing for metrics that don't represent real user experience
### **Severity**
high
### **Situation**
Average response time good, but p99 terrible
### **Why**
  Averages hide problems. Outliers matter. "Average 200ms" but 10% of users
  experience 2-second loads.
  
### **Solution**
  # METRICS THAT LIE
  AVERAGE: Hides tail latency
  - One slow request in 100 affects 1% of users
  - p50, p95, p99 tell more
  
  TOTAL TIME: "Page loads in 2s" but interactive in 8s
  
  SYNTHETIC: "Lighthouse 100" but real users see 4s
  
  THROUGHPUT: "1000 req/s" with 20% error rate = 800 success
  
  # THE FIX
  1. USE PERCENTILES
     p50: Typical experience
     p90: Most users
     p99: Worst common case
     p99.9: Your angriest users
  
  2. MEASURE REAL USERS (RUM)
     Not just synthetic tests
  
  3. MEASURE WHAT MATTERS
     Time to interactive
     First contentful paint
     Core Web Vitals
     Not just "load time"
  
  4. MEASURE ERRORS
     Success rate, not just speed
     Errors count as infinite latency
  
  5. SEGMENT DATA
     By device, location, network
     "Fast for desktop, slow for mobile"
     Average hides this
  
### **Symptoms**
  - Reporting averages only
  - Ignoring tail latency
  - Synthetic-only testing
  - Not measuring real users
### **Detection Pattern**
average|mean|avg(?!.*p95|.*percentile)

## Optimization Without Monitoring

### **Id**
optimization-without-monitoring
### **Summary**
Shipping optimizations without visibility into their effect
### **Severity**
high
### **Situation**
Optimization deployed but no metrics to verify it worked
### **Why**
  Can't know if it helped, hurt, or if it regresses later. Unmonitored
  optimizations might not work at all or cause problems elsewhere.
  
### **Solution**
  # MONITORING CHECKLIST
  □ Baseline metrics captured
  □ New metrics tracking change
  □ Dashboard created/updated
  □ Alerts configured
  □ Rollback plan ready
  □ Success criteria defined
  
  # THE FIX
  1. BEFORE/AFTER METRICS
     Baseline before change
     Measure after change
     Compare with statistical rigor
  
  2. DASHBOARDS
     Key performance metrics visible
     Trends over time
     Alerts on regression
  
  3. FEATURE FLAGS
     Deploy behind flag
     Compare flagged vs unflagged
     Gradual rollout
  
  4. A/B TESTING
     "Optimized" vs "original"
     Statistically significant difference?
     Real user impact?
  
  # OPTIMIZATION LOG
  Date: 2024-01-15
  Change: Optimized user query
  Baseline p95: 450ms
  After p95: 120ms
  Improvement: 73%
  Monitoring: dashboard.example/user-query
  Alert: Fires if p95 > 200ms
  
  RULE: No metrics = No optimization
  
### **Symptoms**
  - No before/after comparison
  - No monitoring dashboard
  - No alerts configured
  - No way to verify success
### **Detection Pattern**
