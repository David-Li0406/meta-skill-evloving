# Debugging Techniques

## Error Categories

| Error Type | Common Causes | First Steps |
|------------|---------------|-------------|
| `TypeError` | Wrong argument type, None access | Check type hints, add guards |
| `AttributeError` | None object, wrong type | Verify object initialization |
| `KeyError` | Missing dict key | Use `.get()` or check existence |
| `ImportError` | Missing package, circular import | Check dependencies, import order |
| `ValueError` | Invalid value for operation | Validate input at boundaries |
| `RuntimeError` | Logic error, invalid state | Review control flow |

## Debugging Workflow

1. **Reproduce** - Create minimal test case
2. **Isolate** - Binary search to find exact location
3. **Inspect** - Check values at failure point
4. **Hypothesize** - Form theory about cause
5. **Test** - Verify hypothesis
6. **Fix** - Implement and test solution

## Using pdb/breakpoint()

```python
def problematic_function(data):
    breakpoint()  # Opens debugger here
    result = process(data)
    return result
```

Common pdb commands:
- `n` (next) - Execute next line
- `s` (step) - Step into function
- `c` (continue) - Continue execution
- `p expr` - Print expression
- `pp expr` - Pretty print
- `l` (list) - Show source code
- `w` (where) - Show stack trace
- `q` (quit) - Exit debugger

## Logging for Debugging

```python
import logging
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

def process_order(order_id: str) -> Order:
    log = logger.bind(order_id=order_id)
    log.info("processing_started")

    try:
        order = fetch_order(order_id)
        log.info("order_fetched", status=order.status)

        result = validate_order(order)
        log.info("order_validated", valid=result.valid)

        return result
    except OrderNotFoundError:
        log.error("order_not_found")
        raise
    except Exception as e:
        log.exception("processing_failed", error=str(e))
        raise
```

## Common Bug Patterns

### Mutable Default Arguments
```python
# Bug
def append_item(item, items=[]):
    items.append(item)
    return items

# Fix
def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Late Binding in Closures
```python
# Bug
funcs = [lambda: i for i in range(3)]
# All return 2

# Fix
funcs = [lambda i=i: i for i in range(3)]
# Returns 0, 1, 2 respectively
```

### Async Context Issues
```python
# Bug - connection closed before use
async def get_data():
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
    return await response.json()  # Error: session closed

# Fix
async def get_data():
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        return await response.json()
```

### Silent Exception Swallowing
```python
# Bug
try:
    result = risky_operation()
except Exception:
    pass  # Silent failure

# Fix
try:
    result = risky_operation()
except SpecificError as e:
    logger.warning("operation_failed", error=str(e))
    result = default_value
```

## Profiling

### Time profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
# ... code to profile ...
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
stats.print_stats(10)
```

### Memory profiling
```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    large_list = [x for x in range(1000000)]
    return sum(large_list)
```

### Line profiling
```python
# pip install line_profiler
from line_profiler import profile

@profile
def slow_function():
    result = []
    for i in range(1000):
        result.append(expensive_operation(i))
    return result
```

## Debugging Async Code

```python
import asyncio

# Enable debug mode
asyncio.run(main(), debug=True)

# Or via environment variable
# PYTHONASYNCIODEBUG=1 python app.py

# Log slow callbacks
logging.getLogger("asyncio").setLevel(logging.DEBUG)
```

## Debugging Tips

1. **Print strategically** - Add prints before/after suspicious code
2. **Simplify** - Remove code until bug disappears, then add back
3. **Check assumptions** - Verify types, values, and states
4. **Read the traceback** - Bottom-up, find your code first
5. **Reproduce consistently** - Write a failing test
6. **Check recent changes** - `git diff`, `git bisect`
7. **Rubber duck** - Explain the problem out loud
