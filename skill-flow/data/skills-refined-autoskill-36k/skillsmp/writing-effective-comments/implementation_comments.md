# Implementation Comments

In-code comments for maintainers who need to understand the implementation.

## Purpose

Implementation comments answer: **"Why does this code work this way?"**

They help future maintainers (including yourself) understand, modify, and debug the code safely.

## When Implementation Comments Are Needed

### 1. Non-Obvious Algorithms

When the approach isn't immediately clear:

```python
# Use binary search on sorted timestamps to find insertion point
# Linear scan was too slow for feeds with 10k+ items
left, right = 0, len(items) - 1
while left < right:
    mid = (left + right) // 2
    if items[mid].timestamp > target:
        right = mid
    else:
        left = mid + 1
```

### 2. Performance Optimizations

When code is written a certain way for speed or memory:

```python
# Pre-allocate result array to avoid repeated resizing
# Benchmarked 3x faster for typical 1000-item batches
results = [None] * len(items)
for i, item in enumerate(items):
    results[i] = transform(item)
```

### 3. Workarounds for External Bugs

When you're compensating for issues outside your control:

```python
# Work around Stripe API bug: webhook signatures fail verification
# if payload contains non-ASCII characters. Normalize before checking.
# See: https://github.com/stripe/stripe-python/issues/1234
payload = payload.encode('utf-8').decode('ascii', errors='replace')
```

### 4. Security-Sensitive Code

When subtle security considerations drive the implementation:

```python
# Use constant-time comparison to prevent timing attacks
# Standard == would leak token length via response time
if not hmac.compare_digest(provided_token, stored_token):
    raise AuthenticationError()
```

### 5. Temporal or Ordering Dependencies

When operations must happen in a specific sequence:

```python
# Must flush cache BEFORE updating database
# Otherwise concurrent readers may get stale cached data
# pointing to rows that no longer exist
cache.invalidate(user_id)
database.update_user(user_id, new_data)
```

### 6. Subtle Edge Cases

When the code handles non-obvious scenarios:

```python
# Handle the case where user timezone offset crosses midnight
# A 10 PM meeting in UTC-8 is actually the next calendar day in UTC
if local_hour < 0:
    local_date += timedelta(days=-1)
    local_hour += 24
```

## Types of Implementation Comments

### High-Level Overview

At the start of a complex function or block, explain the approach:

```python
def reconcile_transactions(local, remote):
    # Three-pass reconciliation:
    # 1. Match transactions by ID (exact matches)
    # 2. Match remaining by amount+date (fuzzy matches)
    # 3. Flag unmatched for manual review
    ...
```

### "Why" Comments

Explain the reasoning behind a decision:

```python
# Using insertion sort here because the list is nearly sorted
# (only new items appended) and n is typically < 20
for i in range(1, len(items)):
    ...
```

### Warning Comments

Alert maintainers to dangerous or subtle code:

```python
# WARNING: This must run in a single transaction
# Partial completion leaves the account in an invalid state
with db.transaction():
    debit_account(source, amount)
    credit_account(dest, amount)
```

### TODO and FIXME

Mark known issues or planned improvements with context:

```python
# TODO(perf): Cache compiled regex patterns
# Current approach recompiles on each call; fine for low volume
# but will need optimization if used in hot path
pattern = re.compile(user_pattern)

# FIXME: Race condition when two requests update simultaneously
# Need to add optimistic locking before enabling bulk updates
# Tracked in issue #4521
```

## Where to Place Comments

### Principle: Keep Comments Close to Code

Comments should be immediately adjacent to the code they describe:

```python
# Good: Comment directly above the relevant code
# Use modular arithmetic to wrap around buffer end
index = (self.head + offset) % self.capacity

# Bad: Comment separated from code
# Use modular arithmetic to wrap around buffer end

validate_offset(offset)
check_bounds(offset)
index = (self.head + offset) % self.capacity
```

### Block-Level vs. Line-Level

Use block comments for multi-line explanations, line comments for brief annotations:

```python
# Block comment: Explains the overall approach
# The retry logic uses exponential backoff with jitter
# to prevent thundering herd when service recovers
for attempt in range(max_retries):
    try:
        return api_call()
    except TransientError:
        delay = base_delay * (2 ** attempt)
        delay += random.uniform(0, delay * 0.1)  # Jitter to spread load
        time.sleep(delay)
```

## What NOT to Comment

### Don't Explain Language Features

```python
# Bad: Explains what Python does
# This is a list comprehension that filters items
active = [u for u in users if u.active]
```

### Don't Restate the Code

```python
# Bad: Just translates code to English
# Increment counter by one
counter += 1
```

### Don't Comment Obvious Logic

```python
# Bad: The code is self-explanatory
# If user is admin, allow access
if user.is_admin:
    allow_access()
```

## Signs You Need a Comment

Ask yourself:
- Would I wonder about this in 6 months?
- Did I consider alternatives? (Document why you chose this one)
- Is there a gotcha that isn't obvious from reading the code?
- Did I spend time figuring out how to make this work?
- Would changing this break something non-obvious?

If yes to any, write a comment explaining what you know that the code doesn't show.
