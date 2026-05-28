# Reference Guide

## Data Structure Selection

| Need | Data Structure |
|------|----------------|
| Fast lookup by key | Hash map / Dictionary |
| Ordered traversal | Sorted array / Tree |
| Fast min/max extraction | Heap / Priority queue |
| FIFO processing | Queue / Deque |
| LIFO processing | Stack |
| Membership testing | Set |
| Counting occurrences | Counter / Frequency map |
| Disjoint sets / Union-find | Union-Find structure |
| Coordinate storage | Tuple as key in hash map |

### Space-Time Tradeoffs

- **More memory** → precompute lookup tables
- **Less memory** → compute on demand
- **Immutable data** → enables safe memoization

## Optimization Techniques

### Early Termination

- Return as soon as answer found
- Skip unnecessary iterations
- Prune search branches that can't improve result

### Avoid Redundant Work

- Memoize expensive function calls
- Precompute static data outside loops
- Use sets for O(1) membership instead of O(n) list scanning

### Numeric Tricks

- Integer division for "divide and round down"
- Modulo for cyclic patterns
- Bit operations for binary representations
- XOR for parity / toggle operations

## Anti-Patterns to Avoid

### Don't

- **Guess and submit** without testing examples
- **Over-engineer** before having a working solution
- **Copy-paste code** between parts (extract functions instead)
- **Assume input format** without verification
- **Ignore Part 2** implications when designing Part 1
- **Optimize prematurely** before correctness
- **Use mutable global state** (makes debugging hard)

### Do

- **Read the full problem** before coding
- **Start with examples** as test cases
- **Print intermediate state** when debugging
- **Keep solutions simple** until complexity is needed
- **Refactor between parts** if Part 2 requires changes

## Part 2 Survival Guide

### Common Part 2 Patterns

| Pattern | Example | Response |
|---------|---------|----------|
| Scale up | 10 → 1,000,000 | Optimize algorithm |
| Add dimensions | 2D grid → 3D | Generalize coordinates |
| Reverse | "Find X" | "Given X, find Y" |
| Many iterations | 1000 → 1 billion | Cycle detection |
| Add constraints | New rules | Refactor logic |
| Combine operations | Chain transforms | Compose functions |

### Preparation Strategies

- Write Part 1 with extensibility in mind
- Use parameters instead of hardcoded values
- Keep parsing separate from logic
- Don't delete Part 1 code—you may need to reference it

## When Stuck

1. **Re-read the problem**—something is likely misunderstood
2. Check for **off-by-one errors** in ranges/indices
3. Verify **coordinate system consistency**
4. Print state at each step, compare with example walkthrough
5. Try smaller/simpler input to isolate the issue
6. Consider whether algorithm choice is fundamentally wrong

## Workflow Checklist

```
[ ] Parse problem statement carefully
[ ] Identify problem category (graph, DP, simulation, etc.)
[ ] Extract example input/output pairs
[ ] Design solution approach before coding
[ ] Implement with clear, testable functions
[ ] Test against ALL examples
[ ] Debug systematically if tests fail
[ ] Run on actual input
[ ] Verify answer format matches expected type
[ ] Adapt for Part 2
```

## Code Quality Tips

- Descriptive variable names (not single letters except loop indices)
- Functions do one thing
- Comments explain *why*, not *what*
- Assertions document assumptions
- Consistent formatting throughout
