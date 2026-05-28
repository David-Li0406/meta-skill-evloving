# Interface Comments

Documenting abstractions for users who won't read the implementation.

## Purpose

Interface comments answer: **"How do I use this without reading the code?"**

They define the contract between the code and its users, hiding implementation details behind a clear abstraction.

## Essential Elements

### 1. Purpose (High-Level What)

What does this abstraction do? Not *how* it works, but what it accomplishes:

```python
# Bad: Describes implementation
"""Iterates through the list and finds matching elements."""

# Good: Describes purpose
"""Find all users who can receive promotional emails."""
```

### 2. Parameters (Meaning, Not Just Type)

Types tell the compiler; comments tell humans:

```python
# Bad: Just restates types
"""
Args:
    user_id: int - The user ID
    limit: int - The limit
"""

# Good: Explains meaning and constraints
"""
Args:
    user_id: Unique identifier for the user account
    limit: Maximum results to return (1-100, default 20)
"""
```

### 3. Return Value (What It Represents)

What does the return value *mean*, not just its type:

```python
# Bad: States the type
"""Returns: A dictionary"""

# Good: Explains meaning
"""Returns: Map of product IDs to their current inventory counts,
           or empty dict if warehouse is unavailable"""
```

### 4. Side Effects

State changes, I/O operations, external system interactions:

```python
"""
Sends a confirmation email to the user's registered address.
Updates the user's last_contacted timestamp.
Logs the notification to the audit trail.
"""
```

### 5. Preconditions and Postconditions

What must be true before calling, and what will be true after:

```python
"""
Preconditions:
    - User must be authenticated (checked via current_user)
    - Account must not be suspended

Postconditions:
    - Transaction is committed to database
    - Webhook notifications are queued (not yet sent)
"""
```

### 6. Exceptions and Errors

What can go wrong and under what circumstances:

```python
"""
Raises:
    AuthenticationError: If API key is invalid or expired
    RateLimitError: If request quota exceeded (retry after rate_limit_reset)
    NetworkError: If external service is unreachable
"""
```

## The Vocabulary Rule

**Use different words than appear in the code.**

If your comment uses the same terms as the function name and parameters, it's probably not adding value:

```python
# Bad: Same vocabulary
def get_user_email(user_id):
    """Get the email for a user by their ID."""

# Good: Different vocabulary, higher abstraction
def get_user_email(user_id):
    """Look up the primary contact address for notifications."""
```

```python
# Bad: Restates parameter names
def calculate_tax(amount, rate):
    """Calculate tax from amount and rate."""

# Good: Explains the domain
def calculate_tax(amount, rate):
    """
    Compute sales tax for a transaction.

    Args:
        amount: Pre-tax purchase total in cents
        rate: Jurisdiction tax rate as decimal (e.g., 0.0825 for 8.25%)
    """
```

## Class and Module Documentation

### Class Comments

Describe the abstraction the class represents:

```python
class ConnectionPool:
    """
    Manages a pool of reusable database connections.

    Connections are lazily created up to max_size, then reused via
    checkout/checkin. Idle connections are periodically validated
    and recycled if stale.

    Thread-safe: multiple threads can safely checkout connections
    simultaneously without external synchronization.

    Usage:
        pool = ConnectionPool(db_url, max_size=10)
        with pool.connection() as conn:
            conn.execute(query)
    """
```

### Module Comments

Describe what the module provides and when to use it:

```python
"""
Payment processing integration for Stripe.

Handles payment intent creation, confirmation, and webhook processing.
All amounts are in cents (USD). Idempotency keys are auto-generated
for retryable operations.

For refunds and disputes, see payments.refunds module.
"""
```

## When Interface Comments Are Critical

- **Public APIs** - External users can't read your implementation
- **Library code** - Will be used in contexts you can't predict
- **Team boundaries** - Other teams will use without full context
- **Complex abstractions** - Where the name can't capture full behavior
- **Non-obvious behavior** - Side effects, state changes, constraints

## When Simpler Documentation Suffices

- Internal helpers with obvious behavior
- Thin wrappers around well-documented libraries
- Truly trivial operations (but consider if they need to exist)

## Template

For functions and methods:

```
Brief one-line summary of purpose.

Longer description if needed, explaining behavior, constraints,
or usage patterns that aren't obvious from the summary.

Args:
    param1: What this parameter represents and any constraints
    param2: What this parameter represents

Returns:
    What the return value represents, including edge cases

Raises:
    ExceptionType: When and why this is raised

Example:
    result = function_name(typical_input)
```
