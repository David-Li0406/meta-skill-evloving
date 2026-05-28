# Extract Patterns

Patterns for extracting code into reusable components.

## Extract Method

### When to Use
- Method is too long (>20 lines)
- Code block has a clear purpose
- Code is duplicated
- Code needs a comment to explain it

### Process

1. **Identify code to extract**
2. **Check for local variables** used in the code
3. **Create new method** with parameters for inputs
4. **Replace original code** with method call
5. **Test**

### Example

```python
# BEFORE
def generate_report(data):
    # Calculate statistics
    total = sum(d['value'] for d in data)
    average = total / len(data) if data else 0
    max_val = max(d['value'] for d in data) if data else 0
    min_val = min(d['value'] for d in data) if data else 0

    # Format report
    report = f"""
    Report Summary
    ==============
    Total: {total}
    Average: {average:.2f}
    Max: {max_val}
    Min: {min_val}
    """
    return report

# AFTER
def generate_report(data):
    stats = calculate_statistics(data)
    return format_report(stats)

def calculate_statistics(data):
    if not data:
        return {'total': 0, 'average': 0, 'max': 0, 'min': 0}
    values = [d['value'] for d in data]
    return {
        'total': sum(values),
        'average': sum(values) / len(values),
        'max': max(values),
        'min': min(values)
    }

def format_report(stats):
    return f"""
    Report Summary
    ==============
    Total: {stats['total']}
    Average: {stats['average']:.2f}
    Max: {stats['max']}
    Min: {stats['min']}
    """
```

## Extract Class

### When to Use
- Class has too many responsibilities
- Group of fields are always used together
- Methods only use subset of fields
- Class name includes "And" or "Or"

### Process

1. **Identify cohesive group** of fields/methods
2. **Create new class** with these members
3. **Create reference** in original class
4. **Move methods** one at a time
5. **Update callers**
6. **Test after each step**

### Example

```python
# BEFORE
class Employee:
    def __init__(self, name, email, phone,
                 street, city, state, zip_code,
                 salary, department, hire_date):
        self.name = name
        self.email = email
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.salary = salary
        self.department = department
        self.hire_date = hire_date

    def get_address_label(self):
        return f"{self.street}\n{self.city}, {self.state} {self.zip_code}"

    def get_annual_salary(self):
        return self.salary * 12

# AFTER
class Address:
    def __init__(self, street, city, state, zip_code):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def get_label(self):
        return f"{self.street}\n{self.city}, {self.state} {self.zip_code}"

class ContactInfo:
    def __init__(self, email, phone):
        self.email = email
        self.phone = phone

class Employee:
    def __init__(self, name, contact, address, salary, department, hire_date):
        self.name = name
        self.contact = contact
        self.address = address
        self.salary = salary
        self.department = department
        self.hire_date = hire_date

    def get_address_label(self):
        return self.address.get_label()

    def get_annual_salary(self):
        return self.salary * 12
```

## Extract Interface/Protocol

### When to Use
- Multiple classes share same methods
- Want to enable dependency injection
- Testing requires mocking

### Example (Python Protocol)

```python
# BEFORE
class EmailNotifier:
    def send(self, user, message):
        # Send email
        pass

class SMSNotifier:
    def send(self, user, message):
        # Send SMS
        pass

def notify_user(notifier, user, message):
    notifier.send(user, message)  # Duck typing, no type safety

# AFTER
from typing import Protocol

class Notifier(Protocol):
    def send(self, user: User, message: str) -> None: ...

class EmailNotifier:
    def send(self, user: User, message: str) -> None:
        # Send email
        pass

class SMSNotifier:
    def send(self, user: User, message: str) -> None:
        # Send SMS
        pass

def notify_user(notifier: Notifier, user: User, message: str) -> None:
    notifier.send(user, message)  # Type-checked
```

## Extract Module/Package

### When to Use
- File is too large (>500 lines)
- Clear separation of concerns
- Functionality is reusable

### Process

1. **Identify cohesive functionality**
2. **Create new module/file**
3. **Move code** to new module
4. **Update imports** in original and callers
5. **Test**

### Example

```python
# BEFORE: utils.py (500 lines)
def format_date(date): ...
def parse_date(string): ...
def format_currency(amount): ...
def parse_currency(string): ...
def validate_email(email): ...
def validate_phone(phone): ...
# ... more functions

# AFTER: Split into modules
# utils/
#   __init__.py
#   dates.py
#   currency.py
#   validation.py

# utils/dates.py
def format_date(date): ...
def parse_date(string): ...

# utils/currency.py
def format_currency(amount): ...
def parse_currency(string): ...

# utils/validation.py
def validate_email(email): ...
def validate_phone(phone): ...

# utils/__init__.py
from .dates import format_date, parse_date
from .currency import format_currency, parse_currency
from .validation import validate_email, validate_phone
```

## Extract Constant

### When to Use
- Magic numbers in code
- Repeated literal values
- Configuration values

### Example

```python
# BEFORE
def calculate_shipping(weight):
    if weight <= 1:
        return 5.99
    elif weight <= 5:
        return 9.99
    else:
        return weight * 2.50

# AFTER
LIGHT_PACKAGE_THRESHOLD = 1  # kg
MEDIUM_PACKAGE_THRESHOLD = 5  # kg
LIGHT_SHIPPING_RATE = 5.99
MEDIUM_SHIPPING_RATE = 9.99
HEAVY_SHIPPING_RATE_PER_KG = 2.50

def calculate_shipping(weight):
    if weight <= LIGHT_PACKAGE_THRESHOLD:
        return LIGHT_SHIPPING_RATE
    elif weight <= MEDIUM_PACKAGE_THRESHOLD:
        return MEDIUM_SHIPPING_RATE
    else:
        return weight * HEAVY_SHIPPING_RATE_PER_KG
```

## Extract Variable

### When to Use
- Complex expressions
- Expression used multiple times
- Expression needs explanation

### Example

```python
# BEFORE
if user.subscription and user.subscription.end_date > datetime.now() and user.subscription.plan in ['pro', 'enterprise']:
    show_premium_features()

# AFTER
has_active_subscription = (
    user.subscription and
    user.subscription.end_date > datetime.now()
)
is_premium_plan = user.subscription and user.subscription.plan in ['pro', 'enterprise']
should_show_premium = has_active_subscription and is_premium_plan

if should_show_premium:
    show_premium_features()
```
