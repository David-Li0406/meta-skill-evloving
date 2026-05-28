# Move Patterns

Patterns for moving code between files and modules.

## Move Method

### When to Use
- Method uses more data from another class
- Method doesn't fit with other methods in class
- Method causes unnecessary coupling

### Process

1. **Identify better home** for the method
2. **Copy method** to new location
3. **Adjust for new context** (self → parameter)
4. **Update callers** to use new location
5. **Remove original** method
6. **Test**

### Example

```python
# BEFORE
class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items

    def get_discount_percentage(self):
        # Uses only customer data!
        if self.customer.loyalty_years > 5:
            return 15
        elif self.customer.loyalty_years > 2:
            return 10
        elif self.customer.total_orders > 10:
            return 5
        return 0

# AFTER
class Customer:
    def get_discount_percentage(self):
        if self.loyalty_years > 5:
            return 15
        elif self.loyalty_years > 2:
            return 10
        elif self.total_orders > 10:
            return 5
        return 0

class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items

    def get_discount_percentage(self):
        # Delegate to customer
        return self.customer.get_discount_percentage()
```

## Move Field

### When to Use
- Field used more by another class
- Field is part of a data clump
- Field causes class to have mixed responsibilities

### Example

```python
# BEFORE
class Employee:
    def __init__(self):
        self.name = ""
        self.department_name = ""      # These belong
        self.department_budget = 0.0    # to Department
        self.department_manager = None

# AFTER
class Department:
    def __init__(self):
        self.name = ""
        self.budget = 0.0
        self.manager = None

class Employee:
    def __init__(self):
        self.name = ""
        self.department = None  # Reference to Department
```

## Move Class to Module

### When to Use
- File is too large
- Class has different concerns than others in file
- Class is reusable independently

### Process

1. **Create new file** for the class
2. **Move class** definition
3. **Update imports** in original file
4. **Update imports** in all dependent files
5. **Test**

### Example

```python
# BEFORE: models.py (large file)
class User:
    pass

class Order:
    pass

class Product:
    pass

class Category:
    pass

# AFTER: Split into modules
# models/
#   __init__.py
#   user.py
#   order.py
#   product.py

# models/user.py
class User:
    pass

# models/order.py
from .product import Product

class Order:
    pass

# models/__init__.py
from .user import User
from .order import Order
from .product import Product

# Callers can still do:
from models import User, Order
```

## Move Function to Module

### When to Use
- Function doesn't belong in current module
- Function is used by multiple modules
- Creating a utility/helper module

### Example

```python
# BEFORE: views.py
def format_currency(amount):
    return f"${amount:,.2f}"

def render_order(order):
    total = format_currency(order.total)
    return f"Order Total: {total}"

# AFTER: Move to utils
# utils/formatting.py
def format_currency(amount):
    return f"${amount:,.2f}"

# views.py
from utils.formatting import format_currency

def render_order(order):
    total = format_currency(order.total)
    return f"Order Total: {total}"
```

## Move to Superclass/Subclass

### Pull Up Method (to Superclass)

```python
# BEFORE: Duplicate in subclasses
class Dog:
    def get_name(self):
        return self.name

class Cat:
    def get_name(self):
        return self.name

# AFTER: Move to superclass
class Animal:
    def get_name(self):
        return self.name

class Dog(Animal):
    pass

class Cat(Animal):
    pass
```

### Push Down Method (to Subclass)

```python
# BEFORE: Method only used by one subclass
class Bird:
    def fly(self):
        # Only some birds fly!
        pass

class Penguin(Bird):
    pass  # Can't fly!

# AFTER: Only in flying birds
class Bird:
    pass

class FlyingBird(Bird):
    def fly(self):
        pass

class Penguin(Bird):
    pass  # No fly method
```

## Cross-Package Moves

### Moving Between Packages

```python
# BEFORE: utils/helpers.py
def process_payment(payment):
    pass

# AFTER: payments/processor.py
def process_payment(payment):
    pass

# Migration steps:
# 1. Create new location with code
# 2. Update imports in dependent code
# 3. Add re-export in old location (temporary)
# 4. Remove re-export after all code updated
```

### Maintaining Backwards Compatibility

```python
# Old location: utils/helpers.py
import warnings
from payments.processor import process_payment  # Re-export

def _deprecated_process_payment(*args, **kwargs):
    warnings.warn(
        "process_payment moved to payments.processor",
        DeprecationWarning
    )
    return process_payment(*args, **kwargs)

# This allows old imports to work during migration
```

## Move Checklist

### Before Move

- [ ] Identify all usages of code to move
- [ ] Check for circular import risks
- [ ] Plan new location
- [ ] Ensure tests exist

### During Move

- [ ] Copy to new location
- [ ] Update internal references
- [ ] Update imports in dependent code
- [ ] Keep old location as alias temporarily
- [ ] Run tests after each file update

### After Move

- [ ] Remove old code
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Update IDE configurations if needed

## Common Issues

### Circular Imports

```python
# PROBLEM: A imports B, B imports A
# a.py
from b import B
class A:
    def method(self, b: B): pass

# b.py
from a import A  # Circular!
class B:
    def method(self, a: A): pass

# SOLUTION: Use TYPE_CHECKING
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from a import A

class B:
    def method(self, a: "A"): pass
```

### Breaking Changes

When moving public API:

```python
# Old location - keep for backwards compatibility
# old_module.py
from new_module import public_function  # Re-export

# Deprecation warning
import warnings
warnings.warn(
    f"Import from new_module instead of old_module",
    DeprecationWarning,
    stacklevel=2
)
```
