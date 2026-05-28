# Common Refactorings Catalog
**Version:** {{VERSION}}

Standard refactoring patterns for improving code during the TDD REFACTOR phase.

---

## Extract Method

**When:** Code block does one identifiable thing; function is too long.

**Before:**
```python
def process_order(order):
    # Calculate total
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    total *= (1 - order.discount)

    # Send confirmation
    send_email(order.customer, f"Total: {total}")
```

**After:**
```python
def process_order(order):
    total = calculate_total(order)
    send_confirmation(order.customer, total)

def calculate_total(order):
    subtotal = sum(item.price * item.quantity for item in order.items)
    return subtotal * (1 - order.discount)
```

**Benefits:** Readable, testable, reusable

---

## Rename

**When:** Name doesn't describe purpose; abbreviations confuse.

**Before:**
```python
def proc(d):
    for x in d:
        if x.a > 100:
            x.f = True
```

**After:**
```python
def flag_high_value_transactions(transactions):
    for transaction in transactions:
        if transaction.amount > 100:
            transaction.flagged = True
```

**Rule:** Names should explain what, not how.

---

## Inline

**When:** Method body is as clear as the name; indirection adds no value.

**Before:**
```python
def get_price(item):
    return item.price

total = get_price(item) * quantity
```

**After:**
```python
total = item.price * quantity
```

**Caution:** Don't inline if method has multiple callers or encapsulates logic.

---

## Move

**When:** Method uses more from another class than its own.

**Before:**
```python
class Order:
    def calculate_shipping(self):
        return self.address.distance * self.address.rate
```

**After:**
```python
class Address:
    def calculate_shipping(self):
        return self.distance * self.rate

class Order:
    def calculate_shipping(self):
        return self.address.calculate_shipping()
```

**Signal:** Feature envy - method reaches into another object repeatedly.

---

## Simplify Conditionals

### Replace Nested with Guard Clauses

**Before:**
```python
def get_payment(employee):
    if employee.is_active:
        if employee.is_full_time:
            return employee.salary
        else:
            return employee.hourly_rate * employee.hours
    else:
        return 0
```

**After:**
```python
def get_payment(employee):
    if not employee.is_active:
        return 0
    if employee.is_full_time:
        return employee.salary
    return employee.hourly_rate * employee.hours
```

### Replace Conditional with Polymorphism

**Before:**
```python
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
```

**After:**
```python
class Circle:
    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle:
    def area(self):
        return self.width * self.height
```

---

## Quick Reference

| Smell | Refactoring |
|-------|-------------|
| Long method | Extract Method |
| Unclear name | Rename |
| Trivial delegation | Inline |
| Feature envy | Move Method |
| Deep nesting | Guard Clauses |
| Type checking | Polymorphism |
| Duplicated code | Extract + Reuse |
| Magic numbers | Extract Constant |

---

## Safety Checklist

Before any refactoring:
- [ ] All tests passing
- [ ] Change is behavior-preserving
- [ ] Can verify with existing tests

After refactoring:
- [ ] All tests still passing
- [ ] No new behavior introduced
- [ ] Code is clearer than before
