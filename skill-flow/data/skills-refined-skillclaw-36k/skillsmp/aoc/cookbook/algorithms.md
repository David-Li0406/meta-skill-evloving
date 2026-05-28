# Algorithm Cookbook

Recipes for common AoC algorithm patterns.

---

## BFS: Shortest Path (Unweighted)

**Problem**: Find shortest path in unweighted graph or grid.

**Solution**:
```text
queue = [start]
visited = {start}
distance = {start: 0}

while queue:
    node = queue.pop_front()
    for neighbor in adjacent(node):
        if neighbor not in visited:
            visited.add(neighbor)
            distance[neighbor] = distance[node] + 1
            queue.append(neighbor)
```

**Tip**: For grids, `adjacent(node)` returns 4 or 8 neighbors.

---

## DFS: Exhaustive Search

**Problem**: Find all paths, detect cycles, check reachability.

**Solution**:
```text
def dfs(node, visited):
    if node in visited:
        return
    visited.add(node)
    for neighbor in adjacent(node):
        dfs(neighbor, visited)
```

**Tip**: Use iterative with explicit stack for deep recursion.

---

## Dijkstra: Weighted Shortest Path

**Problem**: Shortest path with non-negative edge weights.

**Solution**:
```text
pq = [(0, start)]  # (distance, node)
dist = {start: 0}

while pq:
    d, node = pop_min(pq)
    if d > dist.get(node, inf):
        continue
    for neighbor, weight in edges(node):
        new_d = d + weight
        if new_d < dist.get(neighbor, inf):
            dist[neighbor] = new_d
            push(pq, (new_d, neighbor))
```

**Tip**: Skip nodes already processed with better distance.

---

## A*: Heuristic Search

**Problem**: Shortest path when you have a good distance estimate.

**Solution**:
```text
pq = [(heuristic(start, goal), 0, start)]  # (f, g, node)
g_scores = {start: 0}

while pq:
    _, g, node = pop_min(pq)
    if node == goal:
        return g
    for neighbor, weight in edges(node):
        new_g = g + weight
        if new_g < g_scores.get(neighbor, inf):
            g_scores[neighbor] = new_g
            f = new_g + heuristic(neighbor, goal)
            push(pq, (f, new_g, neighbor))
```

**Tip**: Use Manhattan distance for grids. Heuristic must never overestimate.

---

## Dynamic Programming: Memoization

**Problem**: "Count ways...", "Find min/max...", overlapping subproblems.

**Solution** (top-down):
```text
memo = {}

def solve(state):
    if state in memo:
        return memo[state]
    if is_base_case(state):
        return base_value(state)

    result = combine(solve(sub) for sub in subproblems(state))
    memo[state] = result
    return result
```

**Solution** (bottom-up):
```text
dp = initialize_base_cases()

for state in topological_order():
    dp[state] = combine(dp[sub] for sub in subproblems(state))

return dp[final_state]
```

**Tip**: State must be hashable (tuples, not lists). Ask: "What info do I need for the next decision?"

---

## Cycle Detection: Skip Huge Iterations

**Problem**: "After N iterations..." where N is astronomically large.

**Solution**:
```text
state = initial
seen = {state: 0}

for step in range(1, max_steps + 1):
    state = transition(state)
    if state in seen:
        cycle_start = seen[state]
        cycle_len = step - cycle_start
        remaining = (target - cycle_start) % cycle_len
        # Look up from stored states
        break
    seen[state] = step
```

**Tip**: Store full state history to retrieve answer after finding cycle.

---

## Binary Search: Find Threshold

**Problem**: "Find minimum X such that..." with monotonic property.

**Solution**:
```text
def binary_search(lo, hi, predicate):
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**Tip**: Works when `predicate` is False for low values, True for high values.

---

## Flood Fill: Connected Regions

**Problem**: Find/count connected regions, calculate areas.

**Solution**:
```text
def flood_fill(grid, start, target):
    if grid[start] != target:
        return set()

    region = {start}
    queue = [start]

    while queue:
        pos = queue.pop()
        for neighbor in adjacent(pos):
            if neighbor not in region and grid.get(neighbor) == target:
                region.add(neighbor)
                queue.append(neighbor)
    return region
```

**Tip**: Use BFS for level-order, DFS for memory efficiency.

---

## GCD/LCM: Cycle Synchronization

**Problem**: Multiple cycles that need to align.

**Solution**:
```text
gcd(a, b) = gcd(b, a % b)  # Euclidean
lcm(a, b) = a * b // gcd(a, b)

# For multiple values:
lcm(a, b, c) = lcm(lcm(a, b), c)
```

**Tip**: Common in problems with multiple repeating patterns.

---

## Modular Arithmetic: Large Numbers

**Problem**: Numbers grow too large, need to keep bounded.

**Solution**:
```text
result = (result + value) % MOD
result = (result * factor) % MOD
```

**Tip**: Apply mod after every operation to prevent overflow.
