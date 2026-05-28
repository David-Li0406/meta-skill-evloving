# Good vs Bad Comment Examples

Practical examples showing the difference between effective and ineffective comments.

## Function Documentation

### Bad: Restates the Obvious

```python
def get_user(user_id):
    """
    Get a user.

    Args:
        user_id: The user ID.

    Returns:
        The user.
    """
```

**Problems:**
- Restates the function name
- Parameters and returns add no information
- Doesn't explain what "getting a user" means or entails

### Good: Explains the Abstraction

```python
def get_user(user_id):
    """
    Retrieve a user's profile from the database.

    Fetches the complete user record including preferences and permissions.
    Results are cached for 5 minutes; use get_user_fresh() to bypass cache.

    Args:
        user_id: Unique identifier from the users table (UUID format)

    Returns:
        User object with profile data, or None if not found.
        Deactivated users return None (use get_user_including_deactivated
        for admin purposes).

    Raises:
        DatabaseError: If connection fails after 3 retries
    """
```

**Why it works:**
- Explains what "getting" actually involves
- Documents caching behavior (not obvious from code)
- Clarifies edge case handling (deactivated users)
- Mentions related functions for different use cases

---

## Class Documentation

### Bad: Describes the Class Name

```python
class PaymentProcessor:
    """A class that processes payments."""
```

### Good: Describes the Abstraction

```python
class PaymentProcessor:
    """
    Handles payment flow from checkout through settlement.

    Coordinates with Stripe for card payments and PayPal for
    alternative payment methods. Maintains idempotency to safely
    handle retries and webhook replays.

    All monetary amounts are integers in cents (USD).

    Thread-safe: a single instance can process concurrent payments.
    For high-volume scenarios, use PaymentProcessorPool instead.

    Lifecycle:
        processor = PaymentProcessor(api_keys)
        result = processor.charge(amount, payment_method)
        # result.status in ['succeeded', 'pending', 'failed']

    See also:
        RefundProcessor: For handling refunds and chargebacks
        PaymentWebhooks: For processing async status updates
    """
```

---

## Implementation Comments

### Bad: Parrots the Code

```python
# Loop through the items
for item in items:
    # Check if item is valid
    if item.is_valid():
        # Add to results
        results.append(item)
```

### Good: Explains the Why

```python
# Filter to items ready for shipment
# (valid = paid, in stock, and shipping address verified)
for item in items:
    if item.is_valid():
        results.append(item)
```

---

### Bad: States What Code Does

```python
# Set timeout to 30 seconds
timeout = 30
```

### Good: Explains the Decision

```python
# 30s timeout balances user experience against slow network conditions
# Based on p99 latency analysis: 95% of requests complete in <10s,
# but payment processor occasionally takes 20-25s during peak hours
timeout = 30
```

---

## Edge Case Documentation

### Bad: No Explanation

```python
if count == 0:
    return []
```

### Good: Documents the Edge Case

```python
# Return empty list for zero count to maintain consistent return type
# Callers can iterate without null checks
if count == 0:
    return []
```

---

## Algorithm Comments

### Bad: Describes the Code

```python
# Use two pointers
left = 0
right = len(arr) - 1
while left < right:
    if arr[left] + arr[right] == target:
        return (left, right)
    elif arr[left] + arr[right] < target:
        left += 1
    else:
        right -= 1
```

### Good: Explains the Approach

```python
# Two-pointer approach on sorted array: O(n) time vs O(n^2) brute force
# Left pointer finds smaller addend, right finds larger
# Works because array is sorted - if sum too small, need larger number (move left)
# If sum too large, need smaller number (move right)
left = 0
right = len(arr) - 1
while left < right:
    current_sum = arr[left] + arr[right]
    if current_sum == target:
        return (left, right)
    elif current_sum < target:
        left += 1  # Need larger sum
    else:
        right -= 1  # Need smaller sum
```

---

## Workaround Comments

### Bad: No Context

```python
data = data.replace('\x00', '')
```

### Good: Explains the Workaround

```python
# Remove null bytes that PostgreSQL COPY command can't handle
# Source system (legacy Oracle) uses \x00 as empty string placeholder
# TODO: Fix at source when Oracle migration completes (Q3 2024)
data = data.replace('\x00', '')
```

---

## Warning Comments

### Bad: Vague Warning

```python
# Be careful here
delete_user_data(user_id)
```

### Good: Specific Warning

```python
# WARNING: Permanently deletes all user data including backups
# GDPR right-to-erasure requirement - cannot be undone
# Audit log entry created automatically; caller must verify
# user identity before calling
delete_user_data(user_id)
```

---

## Module-Level Comments

### Bad: States the Obvious

```python
"""
This module contains utility functions.
"""
```

### Good: Provides Context

```python
"""
String sanitization utilities for user-generated content.

All functions are Unicode-aware and handle edge cases like
zero-width characters and bidirectional text overrides that
could be used for spoofing or injection attacks.

For HTML output, use html_escape() rather than str.replace()
to handle all entity encodings correctly.

Note: These utilities are for display safety only.
For database storage, use parameterized queries instead.
"""
```

---

## Comment Placement

### Bad: Comment Far from Code

```python
# Validate input is positive

logger.info(f"Processing amount: {amount}")
check_permissions(user)
initialize_transaction()

if amount <= 0:
    raise ValueError("Amount must be positive")
```

### Good: Comment Adjacent to Code

```python
logger.info(f"Processing amount: {amount}")
check_permissions(user)
initialize_transaction()

# Validate after permission check to avoid leaking valid amount ranges
# to unauthorized users via error messages
if amount <= 0:
    raise ValueError("Amount must be positive")
```

---

## Summary: The Transformation

| Bad Comment | Good Comment |
|-------------|--------------|
| Restates code | Explains purpose |
| Uses same words | Uses different vocabulary |
| Describes "what" | Explains "why" |
| Generic/vague | Specific/concrete |
| Could apply anywhere | Specific to this code |
| Tells you nothing new | Provides insight |
