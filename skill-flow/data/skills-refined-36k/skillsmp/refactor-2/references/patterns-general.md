# Refactoring Patterns Reference

Detailed examples and patterns for common refactoring operations.

## Extract Function Pattern

### Before

```python
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Order must have items")
    if order.total < 0:
        raise ValueError("Invalid total")

    # Calculate discounts
    discount = 0
    if order.customer.is_premium:
        discount = order.total * 0.1
    if order.total > 100:
        discount += order.total * 0.05

    # Apply payment
    final_total = order.total - discount
    payment_result = charge_card(order.customer.card, final_total)

    return payment_result
```

### After

```python
def process_order(order):
    validate_order(order)
    discount = calculate_discount(order)
    final_total = order.total - discount
    return charge_card(order.customer.card, final_total)

def validate_order(order):
    if not order.items:
        raise ValueError("Order must have items")
    if order.total < 0:
        raise ValueError("Invalid total")

def calculate_discount(order):
    discount = 0
    if order.customer.is_premium:
        discount = order.total * 0.1
    if order.total > 100:
        discount += order.total * 0.05
    return discount
```

## Guard Clause Pattern

### Before

```python
def get_payment_amount(employee):
    result = 0
    if employee.is_separated:
        result = separated_amount(employee)
    else:
        if employee.is_retired:
            result = retired_amount(employee)
        else:
            result = normal_amount(employee)
    return result
```

### After

```python
def get_payment_amount(employee):
    if employee.is_separated:
        return separated_amount(employee)
    if employee.is_retired:
        return retired_amount(employee)
    return normal_amount(employee)
```

## Replace Temp with Query

### Before

```python
def calculate_total(order):
    base_price = order.quantity * order.item_price
    if base_price > 1000:
        return base_price * 0.95
    else:
        return base_price * 0.98
```

### After

```python
def calculate_total(order):
    if base_price(order) > 1000:
        return base_price(order) * 0.95
    else:
        return base_price(order) * 0.98

def base_price(order):
    return order.quantity * order.item_price
```

## Introduce Parameter Object

### Before

```python
def amount_invoiced(start_date, end_date):
    ...

def amount_received(start_date, end_date):
    ...

def amount_overdue(start_date, end_date):
    ...
```

### After

```python
@dataclass
class DateRange:
    start: date
    end: date

def amount_invoiced(date_range: DateRange):
    ...

def amount_received(date_range: DateRange):
    ...

def amount_overdue(date_range: DateRange):
    ...
```

## Replace Conditional with Polymorphism

### Before

```python
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14159 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    elif shape.type == "triangle":
        return 0.5 * shape.base * shape.height
```

### After

```python
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height
```

## Decompose Conditional

### Before

```python
if date.before(SUMMER_START) or date.after(SUMMER_END):
    charge = quantity * winter_rate + winter_service_charge
else:
    charge = quantity * summer_rate
```

### After

```python
if is_winter(date):
    charge = winter_charge(quantity)
else:
    charge = summer_charge(quantity)

def is_winter(date):
    return date.before(SUMMER_START) or date.after(SUMMER_END)

def winter_charge(quantity):
    return quantity * winter_rate + winter_service_charge

def summer_charge(quantity):
    return quantity * summer_rate
```

## Consolidate Duplicate Conditional Fragments

### Before

```python
if is_special_deal():
    total = price * 0.95
    send_notification()
else:
    total = price * 0.98
    send_notification()
```

### After

```python
if is_special_deal():
    total = price * 0.95
else:
    total = price * 0.98
send_notification()
```

## Split Loop

### Before

```python
total_salary = 0
youngest_age = float('inf')

for person in people:
    total_salary += person.salary
    if person.age < youngest_age:
        youngest_age = person.age
```

### After

```python
total_salary = sum(person.salary for person in people)
youngest_age = min(person.age for person in people)
```

## Replace Magic Number with Symbolic Constant

### Before

```python
def potential_energy(mass, height):
    return mass * 9.81 * height
```

### After

```python
GRAVITATIONAL_ACCELERATION = 9.81

def potential_energy(mass, height):
    return mass * GRAVITATIONAL_ACCELERATION * height
```

## Encapsulate Collection

### Before

```python
class Person:
    def __init__(self):
        self.courses = []

    def get_courses(self):
        return self.courses  # Returns mutable reference
```

### After

```python
class Person:
    def __init__(self):
        self._courses = []

    def get_courses(self):
        return list(self._courses)  # Returns copy

    def add_course(self, course):
        self._courses.append(course)

    def remove_course(self, course):
        self._courses.remove(course)
```

## Functional Refactoring Patterns

### Replace Loop with Pipeline

Before:
```python
result = []
for item in items:
    if item.is_active:
        result.append(item.name.upper())
```

After:
```python
result = [item.name.upper() for item in items if item.is_active]
# Or with map/filter:
result = list(map(lambda x: x.name.upper(), filter(lambda x: x.is_active, items)))
```

### Extract Pure Function

Move side-effect-free logic into pure functions for easier testing and reasoning:

Before:
```python
def process_and_save(data):
    result = data.value * 2 + 10
    if result > 100:
        result = 100
    database.save(result)
    return result
```

After:
```python
def calculate_result(value):
    result = value * 2 + 10
    return min(result, 100)

def process_and_save(data):
    result = calculate_result(data.value)
    database.save(result)
    return result
```
