---
name: performance
description: "Performance analysis and optimization process. Use when code is slow, operations timeout, reviewing for efficiency, optimizing bottlenecks, or designing for high-load scenarios. Also use when users report slowness, someone says 'this should be faster', adding caching, or when code has nested loops. Essential for Big O analysis, N+1 query detection, database indexing, frontend Core Web Vitals, and profiling with language-specific tools."
---

# Performance Skill

## Overview

Premature optimization is the root of all evil. This skill guides systematic performance analysis—measure first, then optimize.

**Core principle:** Never optimize without profiling. Guessing at bottlenecks wastes time and often makes things worse.

## The Performance Process

### Phase 1: Measure First

**Before changing ANY code:**

1. **Define the Problem**
   - What specifically is slow?
   - How slow is it? (numbers, not feelings)
   - What is acceptable performance?

2. **Establish Baseline**
   - Measure current performance
   - Use realistic data sizes
   - Record the numbers

3. **Profile, Don't Guess**
   - Use profiling tools (not intuition)
   - Identify actual bottleneck
   - See `references/algorithm-complexity.md` for patterns

### Phase 2: Analyze

**Find the real bottleneck:**

1. **Check Complexity**
   - What's the Big O of this code?
   - Is there a nested loop making it O(n²)?
   - Is there repeated work that could be cached?

2. **Check I/O**
   - Database queries in loops (N+1)?
   - Network calls that could be batched?
   - File operations that could be buffered?

3. **Check Memory**
   - Loading more data than needed?
   - Creating unnecessary copies?
   - Memory leaks?

### Phase 3: Optimize

**Fix the bottleneck, measure again:**

1. **Target the Bottleneck**
   - Only optimize what profiler identified
   - Don't optimize "while you're in there"

2. **Measure Improvement**
   - Did it actually get faster?
   - By how much?
   - Any regressions elsewhere?

3. **Document the Change**
   - What was the bottleneck?
   - What was the fix?
   - What was the improvement?

## Red Flags - STOP and Profile

### Complexity Red Flags

```
- Nested loops over collections
- .includes() or .indexOf() inside loops
- String concatenation in loops
- Recursive functions without memoization
- Sorting inside loops
```

### Database Red Flags

```
- Query in a loop (N+1 problem)
- SELECT * when only need few columns
- Missing indexes on filtered/sorted columns
- LIKE '%value%' (can't use index)
- Large IN clauses
```

### Memory Red Flags

```
- Loading entire dataset into memory
- Storing derived data that could be computed
- Not using pagination for large results
- Unbounded caches
- Retaining references to unused objects
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "It's obviously slow" | Profile it. Intuition is often wrong. |
| "Let's add caching" | Caching hides problems. Fix the root cause. |
| "We need to rewrite it" | Usually a small fix. Profile first. |
| "Premature optimization is bad" | Measuring isn't optimizing. Always measure. |
| "It's fast enough for now" | Define "enough". Measure against requirement. |
| "The algorithm is optimal" | I/O often dominates. Check database and network. |

## Performance Checklist

Before approving performance-sensitive code:

- [ ] **Measured**: Do we have baseline numbers?
- [ ] **Profiled**: Did we use tools to find bottleneck?
- [ ] **Complexity**: Is algorithmic complexity appropriate?
- [ ] **N+1**: No database queries in loops?
- [ ] **Indexes**: Queries use appropriate indexes?
- [ ] **Pagination**: Large results are paginated?
- [ ] **Verified**: Did we measure improvement?

## Quick Complexity Reference

| Pattern | Complexity | Fix |
|---------|------------|-----|
| Nested loops | O(n²) | Use Map/Set for O(1) lookup |
| Array.includes in loop | O(n²) | Convert to Set first |
| String concat in loop | O(n²) | Use array.join() |
| Recursive without memo | O(2ⁿ) | Add memoization |
| Query per item | O(n) queries | Batch or JOIN |

## Quick Profiling Commands

```bash
# Node.js
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Python
python -m cProfile -s cumtime script.py
py-spy record -o profile.svg -- python script.py

# Go
go test -bench=. -cpuprofile=cpu.prof
go tool pprof cpu.prof

# Browser
# DevTools → Performance tab → Record
```

## Performance Hierarchy

Focus optimization efforts in this order (highest impact first):

```
1. Architecture    - Wrong design = can't optimize later
2. Algorithms      - O(n²) to O(n) = 1000x improvement
3. Database        - Missing index = table scans
4. I/O             - Network, disk, blocking calls
5. Memory          - Leaks, excessive allocation
6. Micro           - Loop unrolling, etc. (rarely needed)
```

## References

Detailed patterns and examples in `references/`:
- `algorithm-complexity.md` - Big O reference and optimization patterns
- `database-performance.md` - Query optimization and indexing
- `caching-strategies.md` - When and how to cache
- `frontend-performance.md` - Bundle size, Core Web Vitals
- `profiling-tools.md` - Language-specific profiling guides
