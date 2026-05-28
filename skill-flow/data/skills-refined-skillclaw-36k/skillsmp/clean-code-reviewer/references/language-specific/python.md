# Python Clean Code Rules

## Naming Conventions (PEP 8)

### Variables and Functions
- Use snake_case: `get_user_name`, `total_price`
- Boolean variables: use clear predicates: `is_active`, `has_permission`
- Constants: UPPER_SNAKE_CASE: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`
- Private variables/methods: prefix with underscore: `_internal_state`

### Classes
- Use PascalCase: `UserAccount`, `OrderProcessor`

### Common Anti-patterns
- Avoid: `data`, `info`, `obj`, `val`, `temp`, `result` without context
- Avoid: single letters except `i`, `j`, `k` for loops or `_` for unused variables
- Avoid: mixedCase (use snake_case instead)

### Good Examples
```python
# Bad
d = datetime.now()
u = get_u()
flag = True

# Good
created_at = datetime.now()
current_user = get_current_user()
is_authenticated = True
```

## Function Length

**Target: Maximum 20 lines** (excluding blank lines and docstrings)

Functions exceeding 20 lines often indicate:
- Multiple responsibilities
- Complex nested logic
- Need for extraction into helper functions

### Refactoring Example
```python
# Bad: Too long, does too much
def process_order(order):
    # Validate
    if not order.get('items'):
        raise ValueError('Empty order')

    # Calculate total
    total = 0
    for item in order['items']:
        total += item['price'] * item['quantity']

    # Apply discount
    if order.get('coupon'):
        discount = get_discount(order['coupon'])
        total -= total * discount

    # Add shipping
    shipping = calculate_shipping(order['address'])
    total += shipping

    # Save order
    saved_order = db.orders.create(
        items=order['items'],
        total=total,
        status='pending'
    )

    # Send email
    send_email(
        order['email'],
        'Order confirmed',
        generate_email_body(saved_order)
    )

    return saved_order

# Good: Split into focused functions
def process_order(order):
    validate_order(order)
    total = calculate_order_total(order)
    saved_order = save_order(order, total)
    send_order_confirmation(saved_order)
    return saved_order
```

## Comment Guidelines

### Redundant Comments (Remove)
```python
# Set the name - REDUNDANT
user.name = 'John'

# Loop through items - REDUNDANT
for item in items:
    pass

# Increment counter - REDUNDANT
counter += 1

# Return result - REDUNDANT
return result
```

### Valuable Comments (Keep)
```python
# HACK: API returns None instead of empty list for new users
orders = response.get('data') or []

# Using set for O(1) lookup performance instead of list
unique_ids = set(ids)

# FIXME: This breaks with timezones, should use UTC
deadline = datetime(2024, 1, 1)

# Regex matches email format per RFC 5322 simplified
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
```

## Docstrings vs Comments

Use docstrings for:
- Module-level documentation
- Class documentation
- Public function/method documentation

```python
def calculate_total(items: list[dict], discount: float = 0.0) -> float:
    """Calculate total price with optional discount.

    Args:
        items: List of items with 'price' and 'quantity' keys
        discount: Discount percentage (0.0 to 1.0)

    Returns:
        Total price after discount
    """
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    return subtotal * (1 - discount)
```

Use comments for:
- Implementation notes
- Complex algorithm explanations
- TODOs and FIXMEs

## Type Hints

Use type hints for function signatures (Python 3.5+):
```python
# Good
def get_user_by_id(user_id: int) -> User | None:
    return db.users.get(user_id)

# Better clarity than:
def get_user_by_id(user_id):
    return db.users.get(user_id)
```

## List Comprehensions

Prefer list comprehensions for simple transformations, but split complex ones:

```python
# Good: Simple and readable
active_users = [u for u in users if u.is_active]

# Bad: Too complex
result = [
    (user.name, sum(order.total for order in user.orders if order.status == 'completed'))
    for user in users
    if user.is_active and user.created_at > cutoff_date
]

# Good: Break down complex comprehensions
def get_user_totals(users, cutoff_date):
    active_users = [u for u in users if u.is_active and u.created_at > cutoff_date]
    return [(u.name, calculate_completed_total(u)) for u in active_users]
```

## Context Managers

Use context managers for resource management:
```python
# Good
with open('file.txt') as f:
    content = f.read()

# Avoid manual close()
f = open('file.txt')
content = f.read()
f.close()  # Redundant with context manager
```
