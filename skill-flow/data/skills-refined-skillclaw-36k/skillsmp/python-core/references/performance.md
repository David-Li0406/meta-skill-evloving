# Python Performance

## Profiling

```python
import cProfile
import pstats

cProfile.run('my_function()', 'output.prof')
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative').print_stats(10)
```

## Common Optimizations

### List Comprehensions
```python
# Fast
squares = [x**2 for x in range(1000)]

# Slow
squares = []
for x in range(1000):
    squares.append(x**2)
```

### Use Built-ins
```python
# Fast
total = sum(numbers)

# Slow
total = 0
for n in numbers:
    total += n
```

### Generators for Memory
```python
# Memory efficient
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield process(line)
```

## Async for I/O

```python
import asyncio
import httpx

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        return await asyncio.gather(*tasks)
```

## Best Practices

1. Profile before optimizing
2. Use async for I/O-bound work
3. Leverage built-in functions
4. Use generators for large datasets
5. Cache expensive computations
6. Consider PyPy for CPU-bound code
