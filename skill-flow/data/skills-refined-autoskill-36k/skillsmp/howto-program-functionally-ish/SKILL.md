---
name: howto-program-functionally-ish
description: Use when writing or refactoring code. Enforces separation of pure logic from side effects for testability and maintainability.
---

# Separate Pure Logic from Side Effects

## Overview

Code divides into two categories: **pure logic** (calculations, transformations, validations) and **side effects** (I/O, database, network, environment). Mixing them creates code that is hard to test, hard to reason about, and prone to subtle bugs. Separating them makes pure logic trivial to test without mocks and confines unpredictability to a thin coordination layer.

## When to Use

- Writing new functions or modules
- Refactoring existing code
- Reviewing code for testability issues
- Debugging code with tangled I/O and logic

## Core Pattern

All operations follow: **Gather → Process → Persist**

1. **Gather** (side effects): Collect data from external sources
2. **Process** (pure logic): Transform, validate, calculate using only the gathered data
3. **Persist** (side effects): Write results to external destinations

### When Writing Pure Logic

- [ ] Function depends only on its arguments
- [ ] Identical inputs produce identical outputs
- [ ] No file, database, or network operations
- [ ] No environment variable reads
- [ ] No non-deterministic calls (`random()`, `datetime.now()`)
- [ ] No mutation of external state
- [ ] Returns values rather than mutating arguments

### When Writing Side Effect Code

- [ ] Orchestrates I/O only: gather → call pure logic → persist
- [ ] Contains no business rules or complex calculations
- [ ] Handles I/O errors (retries, fallbacks, logging)
- [ ] Keeps coordination logic minimal

### When Reviewing Code

- [ ] Can identify which functions are pure vs side-effecting
- [ ] Pure functions contain no I/O or non-determinism
- [ ] Side effect functions contain no business logic
- [ ] Mixed functions are flagged for refactoring

## Examples

### Separating Logic from I/O

```python
# Good — pure logic, trivial to test
def calculate_discount(
    price: float,
    customer_tier: str,
    is_holiday: bool,
) -> float:
    base_discount = {"bronze": 0.05, "silver": 0.10, "gold": 0.15}
    discount = base_discount.get(customer_tier, 0.0)
    if is_holiday:
        discount += 0.05
    return price * (1 - discount)


# Good — side effects only, thin orchestration
def process_order(order_id: str) -> None:
    order = db.fetch_order(order_id)
    customer = db.fetch_customer(order.customer_id)
    is_holiday = calendar_api.is_holiday(date.today())

    final_price = calculate_discount(
        order.price,
        customer.tier,
        is_holiday,
    )

    db.update_order_price(order_id, final_price)
```

```python
# Bad — mixed logic and I/O, requires mocks to test
def calculate_discount(order_id: str) -> float:
    order = db.fetch_order(order_id)
    customer = db.fetch_customer(order.customer_id)
    is_holiday = calendar_api.is_holiday(date.today())

    base_discount = {"bronze": 0.05, "silver": 0.10, "gold": 0.15}
    discount = base_discount.get(customer.tier, 0.0)
    if is_holiday:
        discount += 0.05

    final_price = order.price * (1 - discount)
    db.update_order_price(order_id, final_price)
    return final_price
```

### Avoiding Non-Determinism

```python
# Good — determinism via parameter
def generate_token(user_id: str, timestamp: datetime, entropy: bytes) -> str:
    return hashlib.sha256(f"{user_id}{timestamp}{entropy}".encode()).hexdigest()


# Good — side effect layer provides non-deterministic values
def create_user_token(user_id: str) -> str:
    return generate_token(
        user_id,
        datetime.now(),
        os.urandom(16),
    )
```

```python
# Bad — non-determinism buried in logic, untestable without mocking time
def generate_token(user_id: str) -> str:
    timestamp = datetime.now()
    entropy = os.urandom(16)
    return hashlib.sha256(f"{user_id}{timestamp}{entropy}".encode()).hexdigest()
```

### Returning Values vs Mutating

```python
# Good — returns new value, no mutation
def add_tax(items: list[LineItem], tax_rate: float) -> list[LineItem]:
    return [
        LineItem(item.name, item.price * (1 + tax_rate))
        for item in items
    ]
```

```python
# Bad — mutates argument, side effect disguised as pure function
def add_tax(items: list[LineItem], tax_rate: float) -> None:
    for item in items:
        item.price *= (1 + tax_rate)
```

### Database as Parameter (Still Impure)

```python
# Good — accept data, not connections
def find_overdue_accounts(
    accounts: list[Account],
    today: date,
) -> list[Account]:
    return [a for a in accounts if a.due_date < today]


# Good — shell gathers data, calls pure logic
def get_overdue_accounts() -> list[Account]:
    accounts = db.fetch_all_accounts()
    return find_overdue_accounts(accounts, date.today())
```

```python
# Bad — database parameter makes function impure despite "passing it in"
def find_overdue_accounts(db: Database, today: date) -> list[Account]:
    accounts = db.fetch_all_accounts()
    return [a for a in accounts if a.due_date < today]
```

### Logger Exception

```python
# Acceptable — loggers are the only permitted side effect in pure logic
def process_batch(
    items: list[Item],
    logger: logging.Logger,
) -> list[Result]:
    logger.info("Processing %d items", len(items))
    results = []
    for item in items:
        result = transform(item)
        if result.has_warnings:
            logger.warning("Item %s has warnings: %s", item.id, result.warnings)
        results.append(result)
    return results


# In tests — pass no-op logger
def test_process_batch() -> None:
    items = [make_test_item()]
    results = process_batch(items, logging.getLogger("null"))
    assert len(results) == 1
```

## Quick Reference

```
Pure Logic (Functional Core):
  - Depends only on arguments
  - Identical inputs → identical outputs
  - No I/O, no env vars, no randomness, no datetime.now()
  - Returns values, does not mutate
  - Exception: loggers are permitted

Side Effects (Imperative Shell):
  - Gather → call pure logic → Persist
  - No business rules or calculations
  - Handles I/O errors
  - Thin coordination only

Flow: GATHER (shell) → PROCESS (core) → PERSIST (shell)
```

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| "Just one database call in the function" | One I/O call makes the entire function impure and mock-dependent | Extract I/O to caller, pass data as argument |
| Database/connection as parameter | Still performs I/O, not pure despite "injection" | Pass the data, not the data source |
| `datetime.now()` in calculations | Non-deterministic, tests become flaky or require freezing time | Accept timestamp as parameter |
| `random()` in business logic | Non-deterministic, can't assert exact outputs | Accept random value as parameter |
| Mutating input arguments | Hidden side effect, caller's data unexpectedly changed | Return new values instead |
| Business logic in I/O orchestration | Logic becomes hard to test without integration setup | Extract pure function, call from shell |
| "I'll refactor later" | Later never comes, complexity compounds | Separate now, it's faster in the long run |

## Anti-Rationalizations

- "It's just one file read" — One I/O operation makes the function impure. Extract it.
- "Passing the database is dependency injection" — Passing a connection still performs I/O inside. Pass the data.
- "Mocking is fine" — Mocking is a symptom of entanglement. Pure functions need no mocks.
- "This is over-engineering" — Separating logic from I/O is the minimum viable architecture. Mixing them is under-engineering.
- "Performance requires reading inside the loop" — Benchmark first. If true, document the exception with measurements.
- "It's a small script" — Small scripts become large systems. The pattern scales; mixing doesn't.
