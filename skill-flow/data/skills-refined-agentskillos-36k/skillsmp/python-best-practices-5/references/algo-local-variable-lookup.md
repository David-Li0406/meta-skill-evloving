---
title: Use Local Variables in Hot Loops
impact: MEDIUM-HIGH
impactDescription: 20-30% faster attribute lookups
tags: algo, local-variables, optimization, hot-path
---

## Use Local Variables in Hot Loops

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
