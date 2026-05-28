# Functional Patterns: Core

Functional-first building blocks: higher-order functions, purity, comprehensions, generators.

---
## Higher-Order Functions

**Problem**: You need to pass functions as arguments to other functions or return them as values.

**Solution**:
```python
from typing import Callable

def apply_twice(f: Callable[[int], int], x: int) -> int:
    return f(f(x))

def increment(x: int) -> int:
    return x + 1

result = apply_twice(increment, 5)
assert result == 7  # 5 -> 6 -> 7
```

**Tip**: Higher-order functions enable powerful abstractions. Use type hints to make the function signatures clear and catch errors early.

---

## Pure Functions

**Problem**: You want functions that are predictable, testable, and free from side effects.

**Solution**:
```python
# OK Pure: Same input -> Same output, no side effects
def calculate_discount(price: float, rate: float) -> float:
    return price * (1 - rate)

# BAD Impure: Side effects (modifies external state)
total = 0
def add_to_total(amount: float) -> None:
    global total
    total += amount
```

**Tip**: Pure functions are easier to test, reason about, and parallelize. Avoid global state and mutations when possible.

---

## Map, Filter, Reduce

**Problem**: You need to transform, filter, or aggregate collections of data.

**Solution**:
```python
from functools import reduce
from operator import add, mul

numbers = [1, 2, 3, 4, 5]

# Map: Transform each element
doubled = list(map(lambda x: x * 2, numbers))
assert doubled == [2, 4, 6, 8, 10]

# Filter: Keep elements matching predicate
evens = list(filter(lambda x: x % 2 == 0, numbers))
assert evens == [2, 4]

# Reduce: Accumulate to single value
product = reduce(mul, numbers, 1)
assert product == 120

# OK Prefer comprehensions when readable
doubled_comp = [x * 2 for x in numbers]
evens_comp = [x for x in numbers if x % 2 == 0]
```

**Tip**: Comprehensions are often more Pythonic than map/filter. Use reduce for accumulation, but consider built-ins like sum() when available.

---

## List Comprehensions

**Problem**: You need to transform or filter lists concisely.

**Solution**:
```python
# Basic
squares = [x ** 2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Nested comprehension (flatten)
matrix = [[1, 2], [3, 4], [5, 6]]
flattened = [item for row in matrix for item in row]
assert flattened == [1, 2, 3, 4, 5, 6]

# Dictionary comprehension
user_ages = {user["name"]: user["age"] for user in users}

# Set comprehension
unique_lengths = {len(word) for word in ["apple", "pie", "cat"]}
```

**Tip**: Keep comprehensions simple. If logic gets complex, extract it to a named function for readability.

---

## Generator Expressions

**Problem**: You need to process large datasets without loading everything into memory.

**Solution**:
```python
# Generator: Lazy, memory-efficient
squares_gen = (x ** 2 for x in range(10))

# Consume one at a time
assert next(squares_gen) == 0
assert next(squares_gen) == 1

# Memory-efficient for large datasets
large_data = (x ** 2 for x in range(1_000_000))  # No intermediate list
result = sum(large_data)  # Process lazily
```

**Tip**: Use generator expressions (parentheses) instead of list comprehensions (brackets) when you only need to iterate once or when working with large datasets.

---

## Readable Comprehensions

**Problem**: Your comprehensions are becoming too complex and hard to understand.

**Solution**:
```python
# OK Keep simple and readable
good = [x * 2 for x in numbers if x > 5]

# BAD Avoid overly complex
bad = [x * 2 if x > 5 else x for x in numbers]

# Extract to function if complex
def is_valid(item: dict) -> bool:
    return item["age"] >= 18 and item["status"] == "active"

valid_items = [item for item in data if is_valid(item)]
```

**Tip**: If a comprehension has multiple conditions or complex logic, extract the logic into a well-named function.

---
