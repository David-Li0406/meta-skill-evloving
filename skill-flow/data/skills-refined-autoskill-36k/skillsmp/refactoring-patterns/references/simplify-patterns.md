# Simplify Patterns

Patterns for reducing code complexity.

## Simplify Conditionals

### Replace Nested Conditionals with Guard Clauses

```python
# BEFORE: Deep nesting
def get_payment_amount(employee):
    if employee.is_active:
        if employee.is_full_time:
            if employee.years_of_service > 5:
                return employee.salary * 1.1
            else:
                return employee.salary
        else:
            return employee.hourly_rate * employee.hours
    else:
        return 0

# AFTER: Guard clauses
def get_payment_amount(employee):
    if not employee.is_active:
        return 0

    if not employee.is_full_time:
        return employee.hourly_rate * employee.hours

    if employee.years_of_service > 5:
        return employee.salary * 1.1

    return employee.salary
```

### Replace Conditional with Polymorphism

```python
# BEFORE: Type-checking conditional
def calculate_shipping(item):
    if item.type == "book":
        return 2.99
    elif item.type == "electronics":
        return item.weight * 0.5
    elif item.type == "furniture":
        return item.weight * 2.0 + 20
    else:
        return item.weight * 1.0

# AFTER: Polymorphism
class Item:
    def shipping_cost(self):
        return self.weight * 1.0

class Book(Item):
    def shipping_cost(self):
        return 2.99

class Electronics(Item):
    def shipping_cost(self):
        return self.weight * 0.5

class Furniture(Item):
    def shipping_cost(self):
        return self.weight * 2.0 + 20
```

### Consolidate Conditional Expression

```python
# BEFORE: Multiple conditions with same result
def should_notify(user):
    if user.is_admin:
        return True
    if user.is_moderator:
        return True
    if user.notification_preference == "all":
        return True
    return False

# AFTER: Consolidated
def should_notify(user):
    return (
        user.is_admin or
        user.is_moderator or
        user.notification_preference == "all"
    )
```

### Use Dictionary for Multiple Conditions

```python
# BEFORE: Long if-elif chain
def get_status_message(status):
    if status == "pending":
        return "Your order is pending"
    elif status == "processing":
        return "Your order is being processed"
    elif status == "shipped":
        return "Your order has shipped"
    elif status == "delivered":
        return "Your order was delivered"
    else:
        return "Unknown status"

# AFTER: Dictionary lookup
STATUS_MESSAGES = {
    "pending": "Your order is pending",
    "processing": "Your order is being processed",
    "shipped": "Your order has shipped",
    "delivered": "Your order was delivered",
}

def get_status_message(status):
    return STATUS_MESSAGES.get(status, "Unknown status")
```

## Simplify Loops

### Replace Loop with Pipeline

```python
# BEFORE: Imperative loop
def get_active_premium_emails(users):
    emails = []
    for user in users:
        if user.is_active:
            if user.is_premium:
                emails.append(user.email)
    return emails

# AFTER: Functional pipeline
def get_active_premium_emails(users):
    return [
        user.email
        for user in users
        if user.is_active and user.is_premium
    ]

# Or with filter/map
def get_active_premium_emails(users):
    active_premium = filter(
        lambda u: u.is_active and u.is_premium,
        users
    )
    return [u.email for u in active_premium]
```

### Replace Loop with Built-in

```python
# BEFORE: Manual loop
def has_admin(users):
    for user in users:
        if user.is_admin:
            return True
    return False

# AFTER: Built-in
def has_admin(users):
    return any(user.is_admin for user in users)

# More examples:
all(user.is_verified for user in users)  # All verified?
sum(order.total for order in orders)      # Total sum
max(user.score for user in users)         # Highest score
```

## Simplify Expressions

### Introduce Explaining Variable

```python
# BEFORE: Complex expression
if user.age >= 18 and user.country in ALLOWED_COUNTRIES and not user.is_banned and user.email_verified:
    allow_access()

# AFTER: Named conditions
is_adult = user.age >= 18
is_allowed_country = user.country in ALLOWED_COUNTRIES
is_in_good_standing = not user.is_banned
is_verified = user.email_verified

if is_adult and is_allowed_country and is_in_good_standing and is_verified:
    allow_access()
```

### Replace Magic Numbers with Constants

```python
# BEFORE: Magic numbers
def calculate_price(base_price, quantity):
    if quantity > 100:
        return base_price * quantity * 0.8
    elif quantity > 10:
        return base_price * quantity * 0.9
    return base_price * quantity

# AFTER: Named constants
BULK_THRESHOLD = 100
BULK_DISCOUNT = 0.8
VOLUME_THRESHOLD = 10
VOLUME_DISCOUNT = 0.9

def calculate_price(base_price, quantity):
    if quantity > BULK_THRESHOLD:
        return base_price * quantity * BULK_DISCOUNT
    elif quantity > VOLUME_THRESHOLD:
        return base_price * quantity * VOLUME_DISCOUNT
    return base_price * quantity
```

## Simplify Method Calls

### Replace Parameter with Method Call

```python
# BEFORE: Caller calculates value
discount = order.get_discount()
total = order.calculate_total(discount)

# AFTER: Method calculates internally
total = order.calculate_total()  # Gets discount internally

class Order:
    def calculate_total(self):
        discount = self.get_discount()
        return self.subtotal * (1 - discount)
```

### Introduce Parameter Object

```python
# BEFORE: Long parameter list
def create_order(customer_name, customer_email, customer_phone,
                 shipping_street, shipping_city, shipping_state, shipping_zip,
                 items, discount_code):
    pass

# AFTER: Parameter objects
@dataclass
class Customer:
    name: str
    email: str
    phone: str

@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str

def create_order(customer: Customer, shipping: Address, items: list, discount_code: str = None):
    pass
```

### Replace Constructor with Factory Method

```python
# BEFORE: Complex constructor logic
class User:
    def __init__(self, data):
        if isinstance(data, dict):
            self.name = data['name']
            self.email = data['email']
        elif isinstance(data, str):
            # Parse from string
            parts = data.split(',')
            self.name = parts[0]
            self.email = parts[1]

# AFTER: Factory methods
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['email'])

    @classmethod
    def from_csv(cls, csv_string):
        parts = csv_string.split(',')
        return cls(parts[0], parts[1])
```

## Remove Code Smells

### Remove Dead Code

```python
# BEFORE: Unused code
def old_calculate(x, y):  # Never called!
    return x * y

def calculate(x, y):
    return x + y

# AFTER: Remove unused
def calculate(x, y):
    return x + y
```

### Remove Duplicate Code

```python
# BEFORE: Duplicated validation
def create_user(email):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        raise ValueError("Invalid email")
    # Create user

def update_user(user_id, email):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        raise ValueError("Invalid email")
    # Update user

# AFTER: Extract to function
def validate_email(email):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        raise ValueError("Invalid email")

def create_user(email):
    validate_email(email)
    # Create user

def update_user(user_id, email):
    validate_email(email)
    # Update user
```

## Complexity Metrics

### When to Simplify

| Metric | Threshold | Action |
|--------|-----------|--------|
| Method lines | > 20 | Extract methods |
| Cyclomatic complexity | > 10 | Reduce branches |
| Parameters | > 4 | Introduce parameter object |
| Nesting depth | > 3 | Use guard clauses |
| Class methods | > 20 | Extract class |

### Measuring Complexity

```bash
# Python - radon
radon cc -a -s src/

# JavaScript - complexity-report
npx complexity-report --format plain src/
```
