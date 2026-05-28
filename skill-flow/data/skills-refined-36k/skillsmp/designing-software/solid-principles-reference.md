# SOLID Principles Reference

Compiled for future skill development. Includes Python-specific nuance and connections to existing skills.

## What is SOLID?

SOLID is a mnemonic for five object-oriented design principles introduced by Robert C. Martin (2000) and named by Michael Feathers (2004). They guide developers toward maintainable, flexible, and testable code.

**In Python**: SOLID applies, but with nuance. Python's duck typing, first-class functions, and dynamic nature mean some principles are "free" while others require discipline rather than enforcement.

---

## S — Single Responsibility Principle (SRP)

> A class/module should have only one reason to change.

### When to Lean On It

**Always.** SRP is the most universally applicable principle and maps directly to the [functionally-ish](../howto-program-functionally-ish/SKILL.md) pattern: separate pure logic from side effects.

- Each function does one thing
- Each class has one responsibility
- Each module serves one purpose

### When to Relax

- **Simple scripts**: A 50-line utility script doesn't need three classes
- **Data classes**: A dataclass holding related fields isn't violating SRP

### Examples

```python
# Good — single responsibility per class
class OrderValidator:
    def validate(self, order: Order) -> list[str]:
        errors = []
        if not order.items:
            errors.append("Order has no items")
        if order.total < 0:
            errors.append("Total cannot be negative")
        return errors


class OrderRepository:
    def save(self, order: Order) -> None:
        self.db.insert("orders", order.to_dict())


class OrderService:
    def __init__(self, validator: OrderValidator, repo: OrderRepository) -> None:
        self.validator = validator
        self.repo = repo

    def place_order(self, order: Order) -> None:
        errors = self.validator.validate(order)
        if errors:
            raise ValidationError(errors)
        self.repo.save(order)
```

```python
# Bad — multiple responsibilities in one class
class Order:
    def validate(self) -> list[str]:
        # Validation logic
        ...

    def save(self) -> None:
        # Database logic
        db.insert("orders", self.to_dict())

    def send_confirmation_email(self) -> None:
        # Email logic
        smtp.send(self.customer.email, "Order confirmed")
```

### Connection to Other Skills

- **Functionally-ish**: SRP at function level = "pure logic OR side effects, not both"
- **C4 Model**: Each Component should have one clear responsibility

---

## O — Open/Closed Principle (OCP)

> Software entities should be open for extension, closed for modification.

### When to Lean On It

- **Stable abstractions**: When you have a well-defined interface that multiple implementations share
- **Plugin systems**: When new behavior types are frequently added
- **Libraries/frameworks**: When you can't modify client code

### When to Relax

- **Python's reality**: Duck typing and monkey patching mean everything is already "open for extension"
- **Early development**: Don't prematurely abstract; wait for patterns to emerge
- **Simple conditionals**: A 3-branch `if/elif/else` doesn't need a strategy pattern

### Examples

```python
# Good — open for extension via Protocol
from typing import Protocol


class PaymentProcessor(Protocol):
    def process(self, amount: float) -> bool: ...


class StripeProcessor:
    def process(self, amount: float) -> bool:
        return stripe.charge(amount)


class PayPalProcessor:
    def process(self, amount: float) -> bool:
        return paypal.send_payment(amount)


# Adding new payment method = new class, no modification to existing code
class CryptoProcessor:
    def process(self, amount: float) -> bool:
        return crypto.transfer(amount)


def checkout(processor: PaymentProcessor, amount: float) -> bool:
    return processor.process(amount)
```

```python
# Acceptable in Python — simple conditional, don't over-engineer
def calculate_discount(customer_tier: str) -> float:
    match customer_tier:
        case "bronze":
            return 0.05
        case "silver":
            return 0.10
        case "gold":
            return 0.15
        case _:
            return 0.0

# Only refactor to OCP pattern if:
# - Discount tiers change frequently
# - External code needs to add new tiers
# - Logic per tier becomes complex
```

### Connection to Other Skills

- **Functionally-ish**: Pure functions are naturally closed (no side effects to modify)
- **C4 Model**: Containers/Components with clear interfaces can be extended without internal changes

---

## L — Liskov Substitution Principle (LSP)

> Subtypes must be substitutable for their base types without altering program correctness.

### When to Lean On It

- **Class hierarchies**: When using inheritance (which should be rare in Python)
- **Protocol implementations**: When multiple classes implement the same Protocol
- **Framework extension points**: When subclassing framework classes

### When to Relax

- **Favor composition**: Python idiom prefers composition over inheritance; LSP matters less when you're not subclassing
- **Duck typing**: If it quacks like a duck, it's a duck — behavioral compatibility is what matters, not inheritance

### Examples

```python
# Good — subtype is fully substitutable
class Bird(Protocol):
    def move(self) -> None: ...


class Sparrow:
    def move(self) -> None:
        print("Flying")


class Penguin:
    def move(self) -> None:
        print("Swimming")


def migrate(birds: list[Bird]) -> None:
    for bird in birds:
        bird.move()  # Works for any Bird
```

```python
# Bad — subtype breaks expected behavior (classic LSP violation)
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    def __init__(self, side: float) -> None:
        super().__init__(side, side)

    # LSP violation: setting width should not affect height in Rectangle
    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value
        self._height = value  # Surprise! This breaks Rectangle's contract


# Better — don't use inheritance here
@dataclass
class Rectangle:
    width: float
    height: float

@dataclass
class Square:
    side: float
```

### Connection to Other Skills

- **Python skill**: Type hints with Protocols enable static checking of LSP
- **C4 Model**: Components implementing the same interface must be interchangeable

---

## I — Interface Segregation Principle (ISP)

> Clients should not be forced to depend on interfaces they don't use.

### When to Lean On It

- **Large Protocol definitions**: If a Protocol has 10 methods but most implementers only need 3
- **Testing**: Smaller interfaces = easier to mock
- **Multiple clients**: When different callers need different subsets of functionality

### When to Relax

- **Python has no interfaces**: Duck typing means you only implement what you use anyway
- **Cohesive functionality**: If methods genuinely belong together, keep them together
- **Don't over-segregate**: 10 single-method Protocols is worse than 2 focused ones

### Examples

```python
# Good — segregated protocols
class Readable(Protocol):
    def read(self) -> bytes: ...


class Writable(Protocol):
    def write(self, data: bytes) -> None: ...


class Seekable(Protocol):
    def seek(self, position: int) -> None: ...


# Compose as needed
class ReadWriteFile:
    def read(self) -> bytes: ...
    def write(self, data: bytes) -> None: ...


class ReadOnlyStream:
    def read(self) -> bytes: ...
    # No write needed


def copy_data(source: Readable, dest: Writable) -> None:
    dest.write(source.read())
```

```python
# Bad — fat interface forces unnecessary implementation
class DataStore(Protocol):
    def read(self, key: str) -> bytes: ...
    def write(self, key: str, data: bytes) -> None: ...
    def delete(self, key: str) -> None: ...
    def list_keys(self) -> list[str]: ...
    def get_metadata(self, key: str) -> dict: ...
    def set_permissions(self, key: str, perms: dict) -> None: ...


# A simple cache only needs read/write but must implement everything
class SimpleCache:
    def read(self, key: str) -> bytes: ...
    def write(self, key: str, data: bytes) -> None: ...
    def delete(self, key: str) -> None:
        raise NotImplementedError  # Code smell!
    def list_keys(self) -> list[str]:
        raise NotImplementedError
    # ...
```

### Connection to Other Skills

- **Functionally-ish**: Functions should accept only the data they need (not a whole database connection)
- **C4 Model**: Component interfaces should be focused on specific client needs

---

## D — Dependency Inversion Principle (DIP)

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

### When to Lean On It

**Often.** DIP maps directly to the [functionally-ish](../howto-program-functionally-ish/SKILL.md) pattern: pass data not connections.

- **Testability**: Inject dependencies to enable testing without real I/O
- **Flexibility**: Swap implementations (e.g., test database vs production)
- **Decoupling**: High-level business logic shouldn't know about low-level details

### When to Relax

- **No IoC containers needed**: Python doesn't need Spring-style DI frameworks; constructor injection is enough
- **Simple scripts**: Don't inject dependencies into a 20-line script
- **Stable dependencies**: Standard library modules (json, os.path) don't need abstraction

### Examples

```python
# Good — dependency injected, easy to test
class OrderProcessor:
    def __init__(
        self,
        repository: OrderRepository,
        payment: PaymentProcessor,
        notifier: Notifier,
    ) -> None:
        self.repository = repository
        self.payment = payment
        self.notifier = notifier

    def process(self, order: Order) -> None:
        self.payment.charge(order.total)
        self.repository.save(order)
        self.notifier.send(f"Order {order.id} confirmed")


# In production
processor = OrderProcessor(
    repository=PostgresOrderRepository(),
    payment=StripePaymentProcessor(),
    notifier=EmailNotifier(),
)

# In tests — no mocking frameworks needed
processor = OrderProcessor(
    repository=InMemoryOrderRepository(),
    payment=FakePaymentProcessor(),
    notifier=NullNotifier(),
)
```

```python
# Bad — hardcoded dependencies, impossible to test without mocks
class OrderProcessor:
    def __init__(self) -> None:
        self.db = psycopg2.connect(os.environ["DATABASE_URL"])
        self.stripe = stripe.Client(os.environ["STRIPE_KEY"])
        self.smtp = smtplib.SMTP("mail.example.com")

    def process(self, order: Order) -> None:
        self.stripe.charge(order.total)
        self.db.execute("INSERT INTO orders ...")
        self.smtp.send(...)
```

### Connection to Other Skills

- **Functionally-ish**: "Pass data, not connections" is DIP applied to functions
- **C4 Model**: Components depend on abstractions (other Component interfaces), not concrete implementations

---

## Quick Reference

| Principle | Core Idea | Python Nuance | Lean On | Relax |
|-----------|-----------|---------------|---------|-------|
| **SRP** | One reason to change | Always applicable | Always | Simple scripts, dataclasses |
| **OCP** | Extend, don't modify | Duck typing gives this "for free" | Plugin systems, stable APIs | Early development, simple conditionals |
| **LSP** | Subtypes are substitutable | Favor composition over inheritance | Class hierarchies, Protocols | Duck typing handles most cases |
| **ISP** | Small, focused interfaces | Python has no interfaces | Large Protocols, testing | Cohesive functionality |
| **DIP** | Depend on abstractions | No IoC containers needed | Testability, flexibility | Simple scripts, stable deps |

---

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Abstract everything upfront | Premature abstraction adds complexity | Wait for patterns to emerge, then abstract |
| IoC container in Python | Overkill without static typing | Constructor injection is sufficient |
| Single-method classes everywhere | Over-application of SRP | Functions are fine; classes need state |
| Inheritance for code reuse | Violates LSP, creates coupling | Use composition |
| Protocol with 10 methods | Violates ISP | Segregate into focused Protocols |
| "I'll need this flexibility later" | YAGNI violation | Add abstraction when needed, not before |

---

## Anti-Rationalizations

- "This class is small, it can have two responsibilities" — Size doesn't matter; reasons to change do. Split it.
- "Inheritance is simpler than composition" — Simpler now, painful later. Compose.
- "I don't need dependency injection in Python" — You do for testing. Inject.
- "Let me add a strategy pattern for these 3 cases" — Wait until you have 5+ or they change frequently.
- "Protocols are just Java interfaces in Python" — They're optional and structural; use them for documentation and testing, not enforcement.

---

## Sources

- [SOLID Design Principles Explained | DigitalOcean](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
- [Why SOLID principles are still the foundation | Stack Overflow](https://stackoverflow.blog/2021/11/01/why-solid-principles-are-still-the-foundation-for-modern-software-architecture/)
- [Dynamic Languages and SOLID Principles | Colour Coding](https://colourcoding.net/2009/11/20/dynamic-languages-and-solid-principles/)
- [SOLID Python (PDF) | ResearchGate](https://www.researchgate.net/publication/323935872_SOLID_Python_SOLID_principles_applied_to_a_dynamic_programming_language)
