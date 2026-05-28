---
name: error-handling
description: Error handling patterns for robust applications. Use when implementing error handling, exception management, try-catch blocks, or graceful error recovery.
---

# Error Handling Patterns

Universal error handling patterns for robust applications.

## Core Principles

### 1. Fail Fast
Detect errors early, before they cause more damage.

```
# Bad - Error propagates silently
def process(data):
    result = parse(data)  # Might return None
    return transform(result)  # Crashes later

# Good - Fail immediately
def process(data):
    result = parse(data)
    if result is None:
        raise ValueError("Failed to parse data")
    return transform(result)
```

### 2. Fail Loudly
Make errors visible, don't swallow them.

```
# Bad - Silent failure
try:
    do_something()
except Exception:
    pass  # Error disappears

# Good - Log and handle
try:
    do_something()
except Exception as e:
    logger.error(f"Failed: {e}")
    raise  # Or handle appropriately
```

### 3. Handle at the Right Level
Catch errors where you can meaningfully respond.

## Patterns

### Result Type Pattern
```
def divide(a, b):
    if b == 0:
        return Result.error("Division by zero")
    return Result.ok(a / b)
```

### Guard Clause Pattern
```
def process_order(order):
    if order is None:
        raise ValueError("Order cannot be null")
    if not order.items:
        raise ValueError("Order must have items")

    # Happy path
    return submit_order(order)
```

### Retry Pattern
```
def with_retry(operation, max_attempts=3, delay=1):
    for attempt in range(max_attempts):
        try:
            return operation()
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            sleep(delay * (2 ** attempt))
```

## Error Messages

### For Users
- Clear and actionable
- No technical jargon
- Suggest next steps

### For Developers
- Detailed context
- Stack traces
- Relevant data

## Checklist

- [ ] Expected errors handled explicitly
- [ ] Unexpected errors logged and reported
- [ ] Resources cleaned up in finally/defer
- [ ] User-facing messages are helpful
- [ ] No swallowed exceptions
