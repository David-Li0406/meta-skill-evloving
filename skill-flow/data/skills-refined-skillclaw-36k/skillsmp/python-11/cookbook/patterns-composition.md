# Functional Patterns: Composition and Immutability

Reduce, partials, dispatch, pipelines, and immutable data techniques.

---
## Reduce for Accumulation

**Problem**: You need to combine all elements of a sequence into a single value using a custom operation.

**Solution**:
```python
from functools import reduce
from operator import add, mul

numbers = [1, 2, 3, 4, 5]
total = reduce(add, numbers)
assert total == 15

product = reduce(mul, numbers)
assert product == 120

# Custom reducer
def concat_strings(acc: str, s: str) -> str:
    return f"{acc},{s}" if acc else s

words = ["apple", "banana", "cherry"]
result = reduce(concat_strings, words, "")
assert result == "apple,banana,cherry"
```

**Tip**: Always provide an initial value to reduce() when possible. Use operator module functions (add, mul) instead of lambdas for better performance.

---

## Partial Application

**Problem**: You need to create specialized versions of functions by fixing some arguments.

**Solution**:
```python
from functools import partial

def power(base: int, exponent: int) -> int:
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

assert square(5) == 25
assert cube(5) == 125

# With positional args
def greet(greeting: str, name: str) -> str:
    return f"{greeting}, {name}!"

say_hello = partial(greet, "Hello")
assert say_hello("Alice") == "Hello, Alice!"
```

**Tip**: Use partial() to create specialized functions without writing wrapper functions. Great for callbacks and configuration.

---

## Memoization

**Problem**: You have expensive function calls that repeat with the same arguments.

**Solution**:
```python
from functools import lru_cache, cached_property

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Without cache: O(2^n), With cache: O(n)
assert fibonacci(100) == 354224848179261915075

print(fibonacci.cache_info())
fibonacci.cache_clear()  # Clear cache

# cached_property for classes
class User:
    def __init__(self, user_id: int):
        self.user_id = user_id

    @cached_property
    def full_name(self) -> str:
        return f"User-{self.user_id}"  # Computed once
```

**Tip**: lru_cache is perfect for recursive functions and expensive computations. Use cached_property for expensive instance computations that only need to run once.

---

## Function Overloading

**Problem**: You want different behavior based on the argument type without manual type checking.

**Solution**:
```python
from functools import singledispatch

@singledispatch
def process(arg: object) -> str:
    return f"Default: {arg}"

@process.register(int)
def _(arg: int) -> str:
    return f"Integer: {arg * 2}"

@process.register(list)
def _(arg: list) -> str:
    return f"List with {len(arg)} items"

assert process(5) == "Integer: 10"
assert process([1, 2, 3]) == "List with 3 items"
assert process("hello") == "Default: hello"
```

**Tip**: singledispatch dispatches on the type of the first argument. Great for creating extensible APIs without complex if/isinstance chains.

---

## Function Composition

**Problem**: You want to combine multiple functions into a single function that applies them in sequence.

**Solution**:
```python
from typing import Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose(f: Callable[[T], U], g: Callable[[U], V]) -> Callable[[T], V]:
    def composed(x: T) -> V:
        return g(f(x))
    return composed

def add_one(x: int) -> int:
    return x + 1

def double(x: int) -> int:
    return x * 2

add_then_double = compose(add_one, double)
assert add_then_double(5) == 12  # (5 + 1) * 2
```

**Tip**: Composition reads right-to-left (mathematical style). For left-to-right, use pipe functions or method chaining.

---

## Pipeline Pattern

**Problem**: You want to chain multiple transformations in a readable left-to-right order.

**Solution**:
```python
from functools import reduce
from typing import Callable, Any

def pipe(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return reduce(lambda f, g: lambda x: g(f(x)), functions, lambda x: x)

def add_one(x: int) -> int:
    return x + 1

def triple(x: int) -> int:
    return x * 3

pipeline = pipe(add_one, triple, lambda x: x - 2)
assert pipeline(5) == 16  # 5 -> 6 -> 18 -> 16
```

**Tip**: Pipelines make data transformations more readable. Each function receives the output of the previous one.

---

## Fluent Pipeline Class

**Problem**: You want method chaining for readable, type-safe data transformations.

**Solution**:
```python
from typing import Generic, TypeVar, Callable

T = TypeVar('T')
U = TypeVar('U')

class Pipeline(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def then(self, func: Callable[[T], U]) -> 'Pipeline[U]':
        return Pipeline(func(self.value))

    def get(self) -> T:
        return self.value

def add_one(x: int) -> int:
    return x + 1

def triple(x: int) -> int:
    return x * 3

result = (
    Pipeline(5)
    .then(add_one)
    .then(triple)
    .then(lambda x: x - 2)
    .get()
)
assert result == 16
```

**Tip**: Fluent interfaces improve readability. This pattern is especially useful for data processing workflows.

---

## Frozen Dataclasses

**Problem**: You want immutable data structures that prevent accidental modification.

**Solution**:
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinates:
    x: float
    y: float

    def move(self, dx: float, dy: float) -> 'Coordinates':
        return Coordinates(self.x + dx, self.y + dy)

c1 = Coordinates(0, 0)
c2 = c1.move(1, 1)

assert c1.x == 0  # Original unchanged
assert c2.x == 1  # New instance
```

**Tip**: Frozen dataclasses are hashable and can be used as dictionary keys. Return new instances instead of mutating for immutability.

---

## NamedTuple for Immutability

**Problem**: You need lightweight, immutable records with named fields.

**Solution**:
```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p1 = Point(0, 0)
x, y = p1  # Unpack
# p1.x = 5  # TypeError - immutable
```

**Tip**: NamedTuples are memory-efficient and faster than dataclasses. Use them for simple immutable records.

---

## Immutable Collections

**Problem**: You need to prevent modifications to dictionaries or expose read-only views.

**Solution**:
```python
from types import MappingProxyType

config = {"api_key": "secret", "timeout": 30}
readonly_config = MappingProxyType(config)
# readonly_config["api_key"] = "new"  # TypeError

# Functional list operations with tuples
def append_immutable(lst: tuple, item) -> tuple:
    return lst + (item,)

numbers = (1, 2, 3)
new_numbers = append_immutable(numbers, 4)
assert numbers == (1, 2, 3)  # Unchanged
assert new_numbers == (1, 2, 3, 4)
```

**Tip**: MappingProxyType creates a read-only view of a dictionary. Use tuples instead of lists for immutable sequences.

---

## Copy-on-Write Pattern

**Problem**: You need to update data structures without mutating the original.

**Solution**:
```python
from copy import copy
from dataclasses import dataclass

@dataclass
class UserProfile:
    name: str
    settings: dict

    def with_setting(self, key: str, value: object) -> 'UserProfile':
        new_settings = copy(self.settings)
        new_settings[key] = value
        return UserProfile(name=self.name, settings=new_settings)

profile1 = UserProfile("Alice", {"theme": "light"})
profile2 = profile1.with_setting("theme", "dark")

assert profile1.settings["theme"] == "light"  # Unchanged
assert profile2.settings["theme"] == "dark"
```

**Tip**: Copy-on-write provides a balance between immutability and performance. Use copy() for shallow copies or deepcopy() for nested structures.

---
