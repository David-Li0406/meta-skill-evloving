---
name: refactoring
description: Improve existing code structure and quality while preserving functionality through systematic refactoring techniques, code modernization, and technical debt reduction. Use when improving code quality, modernizing legacy code, eliminating code smells, or when user mentions refactoring, code improvement, or technical debt.
---

# Refactoring

A comprehensive refactoring skill that helps improve code structure, readability, and maintainability while preserving existing behavior.

## Quick Start

Basic refactoring workflow:

```
# Ensure tests exist (or create them first)
# Identify code smells and improvement opportunities
# Apply refactoring techniques incrementally
# Run tests after each change
# Commit frequently
```

## Core Capabilities

### 1. Code Smell Detection & Resolution

Identify and fix common issues:

- **Long Method**: Break into smaller methods
- **Large Class**: Split responsibilities
- **Duplicate Code**: Extract common functionality
- **Long Parameter List**: Introduce parameter objects
- **Feature Envy**: Move behavior to appropriate class
- **Data Clumps**: Group related data
- **Primitive Obsession**: Create value objects
- **Switch Statements**: Replace with polymorphism

### 2. Refactoring Techniques

Apply proven refactoring patterns:

- **Extract Method**: Pull code into separate method
- **Rename**: Improve names for clarity
- **Move Method/Field**: Relocate to appropriate class
- **Inline**: Simplify unnecessary abstractions
- **Replace Temp with Query**: Remove temporary variables
- **Introduce Parameter Object**: Group related parameters
- **Replace Conditional with Polymorphism**: Use inheritance
- **Extract Class**: Split large classes

### 3. Design Pattern Implementation

Refactor to design patterns:

- **Strategy**: Replace conditionals with strategies
- **Factory**: Centralize object creation
- **Observer**: Decouple event handling
- **Decorator**: Add behavior without modification
- **Template Method**: Define algorithm skeleton

### 4. Code Modernization

Update to modern practices:

- **Modern Language Features**: Use latest syntax
- **Async/Await**: Replace callback patterns
- **Type Safety**: Add type hints/annotations
- **Functional Patterns**: Pure functions, immutability
- **Dependency Injection**: Improve testability

### 5. Performance Optimization

Improve efficiency while refactoring:

- **Algorithm Optimization**: Better data structures
- **Caching**: Avoid redundant computation
- **Lazy Loading**: Defer expensive operations
- **Batch Operations**: Reduce I/O overhead
- **Database Optimization**: Query improvement

## Refactoring Catalog

### Extract Method

**Before:**
```python
def print_invoice(invoice):
    print("***********************")
    print("**** Invoice ****")
    print("***********************")
    
    # Print details
    print(f"Name: {invoice.customer_name}")
    print(f"Address: {invoice.customer_address}")
    print(f"Total: ${invoice.total}")
```

**After:**
```python
def print_invoice(invoice):
    print_banner()
    print_details(invoice)

def print_banner():
    print("***********************")
    print("**** Invoice ****")
    print("***********************")

def print_details(invoice):
    print(f"Name: {invoice.customer_name}")
    print(f"Address: {invoice.customer_address}")
    print(f"Total: ${invoice.total}")
```

### Replace Conditional with Polymorphism

**Before:**
```python
class Bird:
    def __init__(self, bird_type):
        self.type = bird_type
    
    def fly(self):
        if self.type == "sparrow":
            return "Flying short distances"
        elif self.type == "eagle":
            return "Soaring high"
        elif self.type == "penguin":
            return "Cannot fly"
```

**After:**
```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def fly(self):
        pass

class Sparrow(Bird):
    def fly(self):
        return "Flying short distances"

class Eagle(Bird):
    def fly(self):
        return "Soaring high"

class Penguin(Bird):
    def fly(self):
        return "Cannot fly"
```

### Introduce Parameter Object

**Before:**
```python
def create_order(customer_name, customer_email, customer_address,
                product_id, product_name, quantity, price):
    # Create order with many parameters
    pass
```

**After:**
```python
from dataclasses import dataclass

@dataclass
class Customer:
    name: str
    email: str
    address: str

@dataclass
class OrderItem:
    product_id: int
    product_name: str
    quantity: int
    price: float

def create_order(customer: Customer, item: OrderItem):
    # Much cleaner interface
    pass
```

### Replace Temp with Query

**Before:**
```python
def calculate_total(order):
    base_price = order.quantity * order.item_price
    discount_factor = 0.1 if base_price > 1000 else 0
    return base_price * (1 - discount_factor)
```

**After:**
```python
def calculate_total(order):
    return base_price(order) * (1 - discount_factor(order))

def base_price(order):
    return order.quantity * order.item_price

def discount_factor(order):
    return 0.1 if base_price(order) > 1000 else 0
```

### Extract Class

**Before:**
```python
class Person:
    def __init__(self, name, street, city, state, zip_code):
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
    
    def get_full_address(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"
```

**After:**
```python
class Address:
    def __init__(self, street, city, state, zip_code):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
    
    def get_full_address(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
```

## Refactoring Strategies

### 1. The Boy Scout Rule

Always leave code better than you found it.

```python
# While fixing a bug, also:
# - Improve variable names
# - Extract complex expressions
# - Add missing tests
# - Update documentation
```

### 2. Incremental Refactoring

Make small, safe changes:

1. **One change at a time**: Single refactoring per commit
2. **Run tests frequently**: After each small change
3. **Commit often**: Create restore points
4. **Stop if tests fail**: Fix before continuing

### 3. Strangler Fig Pattern

Gradually replace legacy code:

```
Old System ──┐
             ├──▶ Facade ──▶ New System (grows)
New Code ────┘
```

1. **Create abstraction layer**
2. **Route new features to new system**
3. **Migrate old features incrementally**
4. **Remove old system when complete**

### 4. Branch by Abstraction

Refactor while keeping system working:

1. **Create abstraction**: Interface for current implementation
2. **Implement new version**: Behind same interface
3. **Switch gradually**: Use feature flags
4. **Remove old implementation**: When fully migrated

## Language-Specific Refactoring

### Python Modernization

**Before (Python 2 style):**
```python
def process_data(data):
    result = []
    for item in data:
        if item['value'] > 0:
            result.append(item)
    return result
```

**After (Modern Python):**
```python
def process_data(data: list[dict]) -> list[dict]:
    return [item for item in data if item['value'] > 0]
```

**Advanced:**
```python
from typing import TypedDict

class DataItem(TypedDict):
    value: int
    name: str

def process_data(data: list[DataItem]) -> list[DataItem]:
    """Filter data items with positive values."""
    return [item for item in data if item['value'] > 0]
```

### JavaScript Modernization

**Before (ES5):**
```javascript
var MyComponent = function(name) {
    this.name = name;
};

MyComponent.prototype.greet = function() {
    return 'Hello, ' + this.name;
};
```

**After (Modern JavaScript):**
```javascript
class MyComponent {
    constructor(name) {
        this.name = name;
    }
    
    greet() {
        return `Hello, ${this.name}`;
    }
}
```

**With TypeScript:**
```typescript
class MyComponent {
    constructor(private name: string) {}
    
    greet(): string {
        return `Hello, ${this.name}`;
    }
}
```

### Callback to Async/Await

**Before:**
```javascript
function fetchUserData(userId, callback) {
    fetchUser(userId, function(err, user) {
        if (err) return callback(err);
        
        fetchPosts(user.id, function(err, posts) {
            if (err) return callback(err);
            
            fetchComments(posts, function(err, comments) {
                if (err) return callback(err);
                callback(null, { user, posts, comments });
            });
        });
    });
}
```

**After:**
```javascript
async function fetchUserData(userId) {
    try {
        const user = await fetchUser(userId);
        const posts = await fetchPosts(user.id);
        const comments = await fetchComments(posts);
        return { user, posts, comments };
    } catch (error) {
        throw new Error(`Failed to fetch user data: ${error.message}`);
    }
}
```

## Refactoring Workflow

### Step 1: Understand the Code

- Read the code thoroughly
- Identify entry points and dependencies
- Document current behavior
- Review existing tests

### Step 2: Ensure Test Coverage

**If tests don't exist, create them first:**

```python
# Characterization tests - document current behavior
def test_current_behavior():
    # Even if behavior is wrong, test it first
    result = legacy_function(input_data)
    assert result == expected_output  # Document what it DOES
```

### Step 3: Plan Refactoring

- Identify code smells
- Prioritize improvements
- Choose refactoring techniques
- Plan sequence of changes

### Step 4: Refactor Incrementally

```
for each_refactoring in plan:
    1. Make one small change
    2. Run tests
    3. If tests pass:
        - Commit
        - Continue
    4. If tests fail:
        - Revert
        - Adjust approach
```

### Step 5: Clean Up

- Remove commented code
- Update documentation
- Verify all tests pass
- Review overall improvements

## Refactoring Patterns

### Replace Magic Numbers

**Before:**
```python
if order.total > 1000:
    discount = order.total * 0.1
```

**After:**
```python
BULK_ORDER_THRESHOLD = 1000
BULK_DISCOUNT_RATE = 0.1

if order.total > BULK_ORDER_THRESHOLD:
    discount = order.total * BULK_DISCOUNT_RATE
```

### Introduce Null Object

**Before:**
```python
def get_customer_discount(customer):
    if customer is None:
        return 0
    if customer.is_premium:
        return 0.15
    return 0.05
```

**After:**
```python
class Customer:
    def get_discount(self):
        return 0.15 if self.is_premium else 0.05

class NullCustomer(Customer):
    def get_discount(self):
        return 0

def get_customer_discount(customer):
    return customer.get_discount()
```

### Replace Error Codes with Exceptions

**Before:**
```python
def save_user(user):
    if not user.email:
        return -1  # Error: No email
    if not user.name:
        return -2  # Error: No name
    # Save user
    return 0  # Success
```

**After:**
```python
class ValidationError(Exception):
    pass

def save_user(user):
    if not user.email:
        raise ValidationError("Email is required")
    if not user.name:
        raise ValidationError("Name is required")
    # Save user
```

## Anti-Patterns to Avoid

### 1. Big Rewrite

❌ **Don't:** Rewrite everything from scratch

✅ **Do:** Refactor incrementally

### 2. Refactoring Without Tests

❌ **Don't:** Change code without safety net

✅ **Do:** Create tests first, then refactor

### 3. Premature Optimization

❌ **Don't:** Optimize before measuring

✅ **Do:** Profile first, optimize bottlenecks

### 4. Over-Engineering

❌ **Don't:** Add complexity "just in case"

✅ **Do:** Keep it simple, refactor when needed

## Best Practices

1. **Tests First**: Ensure comprehensive test coverage
2. **Small Steps**: Make tiny, incremental changes
3. **Commit Often**: Create rollback points
4. **Run Tests**: After every change
5. **One Thing at a Time**: Single refactoring per commit
6. **Preserve Behavior**: Don't change functionality
7. **Improve Names**: Clear, descriptive naming
8. **Remove Duplication**: DRY principle
9. **Simplify Logic**: Reduce complexity
10. **Document Decisions**: Explain non-obvious changes

## When to Refactor

✅ **Good Times to Refactor:**
- Before adding new features
- When fixing bugs
- During code reviews
- Scheduled refactoring sprints
- When code is hard to understand

❌ **Bad Times to Refactor:**
- Close to deadline
- Without tests
- Production is down
- You don't understand the code
- Scope is too large

## When to Use This Skill

Use this skill when:
- Improving code quality
- Reducing technical debt
- Modernizing legacy code
- Preparing for new features
- Eliminating code smells
- Implementing design patterns
- Optimizing performance
- Improving testability
- Making code more maintainable
- Cleaning up after rapid development

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete refactoring examples including:
- Legacy code modernization
- Design pattern implementation
- Performance optimization
- Test-driven refactoring
- Large-scale refactoring strategies

For refactoring checklists, see [CHECKLISTS.md](CHECKLISTS.md).

For refactoring scripts, see [scripts/refactor_helpers.py](scripts/refactor_helpers.py).
