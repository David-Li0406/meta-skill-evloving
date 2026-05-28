---
name: refactor
description: Refactor code to improve quality, apply SOLID principles, remove code smells, and suggest better patterns. Use when improving code structure or modernizing legacy code.
allowed-tools: Read, Write, Grep, Glob
---

# Code Refactoring Skill

Improve code quality through systematic refactoring.

## 1. Extract Method/Function

**Before:**
```python
def process_order(order):
    # Calculate total
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    tax = total * 0.08
    total += tax

    # Send email
    subject = f"Order #{order.id} Confirmation"
    body = f"Your order total is ${total}"
    send_email(order.customer.email, subject, body)
```

**After:**
```python
def process_order(order):
    total = calculate_total_with_tax(order.items)
    send_order_confirmation_email(order, total)

def calculate_total_with_tax(items, tax_rate=0.08):
    subtotal = sum(item.price * item.quantity for item in items)
    return subtotal * (1 + tax_rate)

def send_order_confirmation_email(order, total):
    subject = f"Order #{order.id} Confirmation"
    body = f"Your order total is ${total:.2f}"
    send_email(order.customer.email, subject, body)
```

## 2. Replace Magic Numbers

**Before:**
```javascript
function calculateDiscount(price) {
    if (price > 100) {
        return price * 0.15;
    }
    return price * 0.05;
}
```

**After:**
```javascript
const DISCOUNT_THRESHOLD = 100;
const REGULAR_DISCOUNT_RATE = 0.05;
const PREMIUM_DISCOUNT_RATE = 0.15;

function calculateDiscount(price) {
    const rate = price > DISCOUNT_THRESHOLD
        ? PREMIUM_DISCOUNT_RATE
        : REGULAR_DISCOUNT_RATE;
    return price * rate;
}
```

## 3. Simplify Conditional Logic

**Before:**
```python
def get_user_status(user):
    if user.is_active:
        if user.subscription:
            if user.subscription.is_paid:
                return "premium"
            else:
                return "active"
        else:
            return "active"
    else:
        return "inactive"
```

**After:**
```python
def get_user_status(user):
    if not user.is_active:
        return "inactive"

    if user.subscription and user.subscription.is_paid:
        return "premium"

    return "active"
```

## 4. Replace Nested Conditionals with Guard Clauses

**Before:**
```javascript
function processPayment(payment) {
    if (payment) {
        if (payment.amount > 0) {
            if (payment.method) {
                // Process payment
                return chargeCard(payment);
            } else {
                throw new Error("No payment method");
            }
        } else {
            throw new Error("Invalid amount");
        }
    } else {
        throw new Error("No payment provided");
    }
}
```

**After:**
```javascript
function processPayment(payment) {
    if (!payment) {
        throw new Error("No payment provided");
    }
    if (payment.amount <= 0) {
        throw new Error("Invalid amount");
    }
    if (!payment.method) {
        throw new Error("No payment method");
    }

    return chargeCard(payment);
}
```

## 5. Extract Class

**Before:**
```python
class Order:
    def __init__(self):
        self.items = []
        self.customer_name = ""
        self.customer_email = ""
        self.customer_address = ""
        self.shipping_method = ""
        self.shipping_cost = 0
```

**After:**
```python
class Customer:
    def __init__(self, name, email, address):
        self.name = name
        self.email = email
        self.address = address

class Shipping:
    def __init__(self, method, cost):
        self.method = method
        self.cost = cost

class Order:
    def __init__(self, customer, shipping):
        self.items = []
        self.customer = customer
        self.shipping = shipping
```

## 6. Replace Type Code with Polymorphism

**Before:**
```javascript
class Animal {
    constructor(type) {
        this.type = type;
    }

    makeSound() {
        if (this.type === 'dog') {
            return 'Woof!';
        } else if (this.type === 'cat') {
            return 'Meow!';
        }
    }
}
```

**After:**
```javascript
class Animal {
    makeSound() {
        throw new Error('Must implement makeSound');
    }
}

class Dog extends Animal {
    makeSound() {
        return 'Woof!';
    }
}

class Cat extends Animal {
    makeSound() {
        return 'Meow!';
    }
}
```

## 7. Dependency Injection

**Before:**
```python
class UserService:
    def __init__(self):
        self.db = Database()  # Hard-coded dependency

    def get_user(self, id):
        return self.db.query(f"SELECT * FROM users WHERE id={id}")
```

**After:**
```python
class UserService:
    def __init__(self, database):
        self.db = database  # Injected dependency

    def get_user(self, id):
        return self.db.query_user(id)

# Usage
db = Database()
service = UserService(db)
```

## 8. Remove Duplication

**Before:**
```python
def send_welcome_email(user):
    subject = "Welcome!"
    body = f"Hello {user.name}"
    send_email(user.email, subject, body)

def send_reset_email(user):
    subject = "Password Reset"
    body = f"Hello {user.name}, click here to reset"
    send_email(user.email, subject, body)
```

**After:**
```python
def send_user_email(user, subject, message_template):
    body = message_template.format(name=user.name)
    send_email(user.email, subject, body)

def send_welcome_email(user):
    send_user_email(user, "Welcome!", "Hello {name}")

def send_reset_email(user):
    send_user_email(user, "Password Reset",
                   "Hello {name}, click here to reset")
```

## 9. SOLID Principles

**Single Responsibility:**
```python
# Before: Class does too much
class User:
    def save(self):
        # Database logic
        pass

    def send_email(self):
        # Email logic
        pass

# After: Separate responsibilities
class User:
    pass

class UserRepository:
    def save(self, user):
        pass

class EmailService:
    def send_welcome_email(self, user):
        pass
```

**Open/Closed Principle:**
```python
# Before: Must modify class to add new shapes
class AreaCalculator:
    def calculate(self, shape):
        if shape.type == 'circle':
            return 3.14 * shape.radius ** 2
        elif shape.type == 'square':
            return shape.side ** 2

# After: Open for extension, closed for modification
class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2
```

## 10. Modern Patterns

**Use List Comprehensions:**
```python
# Before
result = []
for item in items:
    if item.is_valid:
        result.append(item.name.upper())

# After
result = [item.name.upper() for item in items if item.is_valid]
```

**Use Destructuring:**
```javascript
// Before
const name = user.name;
const email = user.email;

// After
const { name, email } = user;
```

**Use Arrow Functions:**
```javascript
// Before
users.map(function(user) {
    return user.name;
});

// After
users.map(user => user.name);
```

## When to Use This Skill

Use `/refactor` when:
- Code is difficult to understand
- Functions are too long
- Classes have too many responsibilities
- Code has duplication
- Preparing for new features
- Improving test coverage
- Modernizing legacy code
- Applying design patterns
