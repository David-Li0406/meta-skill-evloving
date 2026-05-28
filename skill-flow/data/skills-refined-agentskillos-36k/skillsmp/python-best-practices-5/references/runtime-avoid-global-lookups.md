---
title: Avoid Repeated Global and Module Lookups
impact: LOW
impactDescription: 10-20% improvement in tight loops
tags: runtime, globals, optimization, micro-optimization
---

## Avoid Repeated Global and Module Lookups

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
