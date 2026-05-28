---
title: Profile Before Optimizing
impact: LOW
impactDescription: identifies actual bottlenecks, prevents wasted effort
tags: runtime, profiling, cprofile, optimization
---

## Profile Before Optimizing

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
