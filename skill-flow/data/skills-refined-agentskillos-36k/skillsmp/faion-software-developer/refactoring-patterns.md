---
id: refactoring-patterns
name: "Refactoring Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Refactoring Patterns

## Overview

Refactoring is the process of restructuring existing code without changing its external behavior. It improves code readability, reduces complexity, and makes the codebase easier to maintain and extend.

## When to Use

- Code is working but hard to understand
- Adding new features requires touching many files
- Duplicate code exists across the codebase
- Classes or functions are too large
- Before adding new functionality (preparatory refactoring)

## Key Principles

- **Keep tests green**: Refactor in small steps, run tests frequently
- **One change at a time**: Don't mix refactoring with feature work
- **Preserve behavior**: External behavior must remain identical
- **Improve incrementally**: Perfect is the enemy of good
- **Leave code better**: Boy Scout Rule

## Best Practices

### Extract Method/Function

```python
# BEFORE: Long method with multiple responsibilities
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("Order has no items")
    if not order.customer:
        raise ValueError("Order has no customer")
    for item in order.items:
        if item.quantity <= 0:
            raise ValueError(f"Invalid quantity for {item.name}")

    # Calculate totals
    subtotal = 0
    for item in order.items:
        subtotal += item.price * item.quantity
    tax = subtotal * 0.08
    shipping = 10.00 if subtotal < 50 else 0
    total = subtotal + tax + shipping

    # Process payment
    payment_result = payment_gateway.charge(
        order.customer.card,
        total
    )
    if not payment_result.success:
        raise PaymentError(payment_result.error)

    # Send confirmation
    email_service.send(
        to=order.customer.email,
        subject="Order Confirmation",
        body=f"Thank you for your order. Total: ${total}"
    )

    return {"order_id": order.id, "total": total}


# AFTER: Extracted methods with clear responsibilities
def process_order(order):
    validate_order(order)
    totals = calculate_totals(order)
    process_payment(order.customer, totals.total)
    send_confirmation(order.customer, totals)
    return {"order_id": order.id, "total": totals.total}


def validate_order(order):
    if not order.items:
        raise ValueError("Order has no items")
    if not order.customer:
        raise ValueError("Order has no customer")
    for item in order.items:
        if item.quantity <= 0:
            raise ValueError(f"Invalid quantity for {item.name}")


@dataclass
class OrderTotals:
    subtotal: Decimal
    tax: Decimal
    shipping: Decimal
    total: Decimal


def calculate_totals(order) -> OrderTotals:
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax = subtotal * Decimal("0.08")
    shipping = Decimal("10.00") if subtotal < 50 else Decimal("0")
    return OrderTotals(
        subtotal=subtotal,
        tax=tax,
        shipping=shipping,
        total=subtotal + tax + shipping
    )


def process_payment(customer, amount):
    result = payment_gateway.charge(customer.card, amount)
    if not result.success:
        raise PaymentError(result.error)


def send_confirmation(customer, totals):
    email_service.send(
        to=customer.email,
        subject="Order Confirmation",
        body=f"Thank you for your order. Total: ${totals.total}"
    )
```

### Extract Class

```python
# BEFORE: Class with too many responsibilities
class User:
    def __init__(self, name, email, address, city, state, zip_code):
        self.name = name
        self.email = email
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def get_full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"

    def validate_address(self):
        return bool(self.address and self.city and self.state and self.zip_code)

    def format_for_shipping(self):
        return {
            "line1": self.address,
            "city": self.city,
            "state": self.state,
            "postal_code": self.zip_code
        }


# AFTER: Extracted Address class
@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str

    def get_full_address(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"

    def is_valid(self) -> bool:
        return bool(self.street and self.city and self.state and self.zip_code)

    def to_shipping_format(self) -> dict:
        return {
            "line1": self.street,
            "city": self.city,
            "state": self.state,
            "postal_code": self.zip_code
        }


@dataclass
class User:
    name: str
    email: str
    address: Address

    # User-specific methods only
    def get_display_name(self) -> str:
        return self.name or self.email.split("@")[0]
```

### Replace Conditional with Polymorphism

```python
# BEFORE: Complex conditional logic
class PriceCalculator:
    def calculate_price(self, product, customer_type):
        base_price = product.price

        if customer_type == "regular":
            discount = 0
        elif customer_type == "premium":
            discount = 0.1
        elif customer_type == "vip":
            discount = 0.2
        elif customer_type == "wholesale":
            discount = 0.3
            if product.quantity > 100:
                discount = 0.4
        else:
            discount = 0

        return base_price * (1 - discount)


# AFTER: Polymorphic pricing strategies
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, product) -> Decimal:
        pass

    def calculate_price(self, product) -> Decimal:
        discount = self.calculate_discount(product)
        return product.price * (1 - discount)


class RegularPricing(PricingStrategy):
    def calculate_discount(self, product) -> Decimal:
        return Decimal("0")


class PremiumPricing(PricingStrategy):
    def calculate_discount(self, product) -> Decimal:
        return Decimal("0.1")


class VIPPricing(PricingStrategy):
    def calculate_discount(self, product) -> Decimal:
        return Decimal("0.2")


class WholesalePricing(PricingStrategy):
    def calculate_discount(self, product) -> Decimal:
        if product.quantity > 100:
            return Decimal("0.4")
        return Decimal("0.3")


# Factory to get strategy
def get_pricing_strategy(customer_type: str) -> PricingStrategy:
    strategies = {
        "regular": RegularPricing(),
        "premium": PremiumPricing(),
        "vip": VIPPricing(),
        "wholesale": WholesalePricing(),
    }
    return strategies.get(customer_type, RegularPricing())
```

### Introduce Parameter Object

```python
# BEFORE: Too many parameters
def create_user(
    name: str,
    email: str,
    phone: str,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    country: str,
    preferred_language: str,
    timezone: str,
    marketing_consent: bool,
) -> User:
    ...

# Calling code is hard to read
user = create_user(
    "John", "john@example.com", "555-1234",
    "123 Main St", "NYC", "NY", "10001", "US",
    "en", "America/New_York", True
)


# AFTER: Parameter objects
@dataclass
class ContactInfo:
    email: str
    phone: str


@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str


@dataclass
class Preferences:
    language: str = "en"
    timezone: str = "UTC"
    marketing_consent: bool = False


@dataclass
class CreateUserRequest:
    name: str
    contact: ContactInfo
    address: Address
    preferences: Preferences = field(default_factory=Preferences)


def create_user(request: CreateUserRequest) -> User:
    ...

# Clear, self-documenting usage
user = create_user(CreateUserRequest(
    name="John",
    contact=ContactInfo(email="john@example.com", phone="555-1234"),
    address=Address(
        street="123 Main St",
        city="NYC",
        state="NY",
        zip_code="10001",
        country="US"
    ),
    preferences=Preferences(language="en", timezone="America/New_York")
))
```

### Replace Magic Numbers/Strings

```python
# BEFORE: Magic numbers and strings
def process_order(order):
    if order.total > 100:  # What does 100 mean?
        order.shipping = 0
    else:
        order.shipping = 9.99

    if order.status == "P":  # What is "P"?
        ...
    elif order.status == "S":
        ...
    elif order.status == "D":
        ...


# AFTER: Named constants and enums
from enum import Enum

class OrderStatus(Enum):
    PENDING = "P"
    SHIPPED = "S"
    DELIVERED = "D"
    CANCELLED = "C"


class ShippingConfig:
    FREE_SHIPPING_THRESHOLD = Decimal("100.00")
    STANDARD_SHIPPING_COST = Decimal("9.99")


def process_order(order):
    if order.total >= ShippingConfig.FREE_SHIPPING_THRESHOLD:
        order.shipping = Decimal("0")
    else:
        order.shipping = ShippingConfig.STANDARD_SHIPPING_COST

    if order.status == OrderStatus.PENDING:
        ...
    elif order.status == OrderStatus.SHIPPED:
        ...
    elif order.status == OrderStatus.DELIVERED:
        ...
```

### Decompose Conditional

```python
# BEFORE: Complex nested conditionals
def calculate_insurance_premium(customer):
    if customer.age >= 18 and customer.age <= 25:
        if customer.accidents == 0:
            if customer.years_licensed >= 2:
                return 200
            else:
                return 300
        else:
            return 500
    elif customer.age > 25 and customer.age <= 65:
        if customer.accidents == 0:
            return 150
        else:
            return 250
    else:
        return 400


# AFTER: Decomposed with explanatory functions
def calculate_insurance_premium(customer) -> int:
    if is_young_driver(customer):
        return calculate_young_driver_premium(customer)
    elif is_standard_age(customer):
        return calculate_standard_premium(customer)
    else:
        return calculate_senior_premium(customer)


def is_young_driver(customer) -> bool:
    return 18 <= customer.age <= 25


def is_standard_age(customer) -> bool:
    return 25 < customer.age <= 65


def calculate_young_driver_premium(customer) -> int:
    if has_clean_record(customer) and is_experienced(customer):
        return 200
    elif has_clean_record(customer):
        return 300
    else:
        return 500


def calculate_standard_premium(customer) -> int:
    return 150 if has_clean_record(customer) else 250


def calculate_senior_premium(customer) -> int:
    return 400


def has_clean_record(customer) -> bool:
    return customer.accidents == 0


def is_experienced(customer) -> bool:
    return customer.years_licensed >= 2
```

### Rename for Clarity

```python
# BEFORE: Unclear names
def calc(d, r):
    return d * r * 0.01

def proc(lst):
    res = []
    for x in lst:
        if x.a > 0:
            res.append(x)
    return res

class Mgr:
    def __init__(self):
        self.lst = []

    def add(self, e):
        self.lst.append(e)


# AFTER: Clear, descriptive names
def calculate_interest(principal: Decimal, annual_rate: Decimal) -> Decimal:
    """Calculate simple interest for one year."""
    return principal * annual_rate * Decimal("0.01")


def filter_positive_balance_accounts(accounts: list[Account]) -> list[Account]:
    """Return accounts with positive balance."""
    return [account for account in accounts if account.balance > 0]


class AccountManager:
    def __init__(self):
        self.accounts: list[Account] = []

    def add_account(self, account: Account) -> None:
        self.accounts.append(account)
```

### Move Method to Appropriate Class

```python
# BEFORE: Method in wrong class (Feature Envy)
class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self.items = items

    def get_customer_discount(self):
        # This method only uses Customer data
        if self.customer.loyalty_years > 5:
            return 0.15
        elif self.customer.loyalty_years > 2:
            return 0.10
        elif self.customer.total_purchases > 1000:
            return 0.05
        return 0


# AFTER: Method moved to Customer
class Customer:
    def __init__(self, loyalty_years, total_purchases):
        self.loyalty_years = loyalty_years
        self.total_purchases = total_purchases

    def get_discount_rate(self) -> Decimal:
        """Calculate discount based on customer loyalty."""
        if self.loyalty_years > 5:
            return Decimal("0.15")
        elif self.loyalty_years > 2:
            return Decimal("0.10")
        elif self.total_purchases > 1000:
            return Decimal("0.05")
        return Decimal("0")


class Order:
    def __init__(self, customer: Customer, items: list[OrderItem]):
        self.customer = customer
        self.items = items

    def calculate_total(self) -> Decimal:
        subtotal = sum(item.price * item.quantity for item in self.items)
        discount = self.customer.get_discount_rate()  # Delegate to Customer
        return subtotal * (1 - discount)
```

### Safe Refactoring Steps

```markdown
## Refactoring Workflow

### 1. Ensure Test Coverage
- Write tests for code to be refactored
- Run tests and verify they pass
- Coverage should be high for affected code

### 2. Small Steps
- Make one small change
- Run tests
- Commit if green
- Repeat

### 3. Use IDE Refactoring Tools
- Extract Method/Variable
- Rename
- Inline
- Move
- Change Signature

### 4. Verify Behavior
- Tests still pass
- No behavior changes
- Same inputs produce same outputs

### 5. Clean Up
- Remove dead code
- Update documentation
- Review diff before committing
```

## Anti-patterns

- **Big bang refactoring**: Changing everything at once
- **Refactoring without tests**: No safety net
- **Mixing with features**: Combining refactoring and new functionality
- **Over-engineering**: Making code more complex "for flexibility"
- **Incomplete refactoring**: Leaving code in worse state
- **Ignoring code smells**: Not refactoring when needed

## References

- [Refactoring by Martin Fowler](https://refactoring.com/)
- [Refactoring Catalog](https://refactoring.com/catalog/)
- [Working Effectively with Legacy Code](https://www.oreilly.com/library/view/working-effectively-with/0131177052/)
- [Clean Code by Robert Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
