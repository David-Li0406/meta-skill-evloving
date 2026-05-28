# Principle Examples

Concrete before/after examples for each principle.

## DRY Violation

```python
# ❌ Before: Duplicated formatting logic
def get_user_display(user):
    return f"{user.first_name} {user.last_name}".strip()

def format_greeting(user):
    name = f"{user.first_name} {user.last_name}".strip()
    return f"Hello, {name}!"

# ✅ After: Extract shared logic
def get_full_name(user):
    return f"{user.first_name} {user.last_name}".strip()

def get_user_display(user):
    return get_full_name(user)

def format_greeting(user):
    return f"Hello, {get_full_name(user)}!"
```

## KISS Violation

```python
# ❌ Before: Overly clever
def is_even(n): return not n & 1

items = [x for x in (y * 2 for y in range(10) if y % 2 == 0) if x > 4]

# ✅ After: Clear and readable
def is_even(n):
    return n % 2 == 0

even_numbers = [y for y in range(10) if y % 2 == 0]
items = [x * 2 for x in even_numbers if x * 2 > 4]
```

## YAGNI Violation

```python
# ❌ Before: Speculative features
class UserRepository:
    def get_user(self, id): ...
    def get_user_cached(self, id): ...      # Not needed yet
    def get_user_async(self, id): ...       # Not needed yet
    def get_user_with_retry(self, id): ...  # Not needed yet

# ✅ After: Only what's needed now
class UserRepository:
    def get_user(self, id): ...
```

## Fail Fast Violation

```python
# ❌ Before: Error detected late
def process_data(data):
    result = []
    for item in data:
        transformed = expensive_operation(item)
        if item.id is None:  # Checked too late
            raise ValueError("id required")
        result.append(transformed)
    return result

# ✅ After: Validate early
def process_data(data):
    for item in data:
        if item.id is None:
            raise ValueError("id required")
    
    return [expensive_operation(item) for item in data]
```

## Over-Validation

```python
# ❌ Before: Redundant checks throughout call chain
def api_handler(request):
    if request.user is None:
        raise AuthError()
    process_user(request.user)

def process_user(user):
    if user is None:  # Redundant
        raise ValueError()
    save_user(user)

def save_user(user):
    if user is None:  # Redundant
        raise ValueError()
    db.save(user)

# ✅ After: Validate once at boundary
def api_handler(request):
    if request.user is None:
        raise AuthError()
    process_user(request.user)

def process_user(user):
    save_user(user)  # Trust the caller

def save_user(user):
    db.save(user)    # Trust the caller
```

## SRP Violation

```python
# ❌ Before: Multiple responsibilities
def process_order(order):
    # Validation
    if not order.items:
        raise ValueError("Empty order")
    # Calculation
    total = sum(item.price for item in order.items)
    tax = total * 0.1
    # Notification
    send_email(order.customer, f"Total: {total + tax}")
    # Persistence
    db.save(order)
    return total + tax

# ✅ After: Separated responsibilities
def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")

def calculate_total(order):
    subtotal = sum(item.price for item in order.items)
    return subtotal * 1.1  # including tax

def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    send_email(order.customer, f"Total: {total}")
    db.save(order)
    return total
```

## DIP Violation

```typescript
// ❌ Before: Hardcoded dependency
class OrderService {
    private db = new PostgresDatabase();  // Tight coupling
    
    save(order: Order) {
        this.db.insert(order);
    }
}

// ✅ After: Dependency injection
interface Database {
    insert(data: any): void;
}

class OrderService {
    constructor(private db: Database) {}
    
    save(order: Order) {
        this.db.insert(order);
    }
}

// Or functional approach
const createOrderService = (db: Database) => ({
    save: (order: Order) => db.insert(order)
});
```
