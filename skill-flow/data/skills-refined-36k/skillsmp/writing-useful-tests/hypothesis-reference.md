# Hypothesis Reference (Python)

Library-specific patterns for property-based testing with [Hypothesis](https://hypothesis.readthedocs.io/).

## Quick Start

```python
from hypothesis import given
from hypothesis import strategies as st

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)
```

Run with pytest as usual. Hypothesis generates 100 random inputs by default.

## Common Strategies

| Strategy | Generates | Example |
|----------|-----------|---------|
| `st.integers()` | Integers (any range) | `st.integers(min_value=0, max_value=100)` |
| `st.floats()` | Floats (including edge cases) | `st.floats(allow_nan=False)` |
| `st.text()` | Unicode strings | `st.text(min_size=1, max_size=50)` |
| `st.binary()` | Bytes | `st.binary(min_size=0, max_size=1024)` |
| `st.booleans()` | True/False | |
| `st.none()` | None | |
| `st.lists()` | Lists of elements | `st.lists(st.integers(), min_size=1)` |
| `st.dictionaries()` | Dicts with key/value strategies | `st.dictionaries(st.text(), st.integers())` |
| `st.one_of()` | One of multiple strategies | `st.one_of(st.none(), st.integers())` |
| `st.sampled_from()` | Element from a sequence | `st.sampled_from(["a", "b", "c"])` |

## Constraining Generators

Constrain at the generator level rather than filtering afterward.

```python
# Good — generates only valid inputs
@given(st.integers(min_value=1))
def test_positive_numbers(n):
    assert my_function(n) > 0

# Bad — discards invalid inputs, reducing effective test coverage
@given(st.integers())
def test_positive_numbers(n):
    assume(n > 0)  # Hypothesis may give up if too many are discarded
    assert my_function(n) > 0
```

Use `assume()` sparingly, only when constraints are difficult to express in the generator.

## Composite Strategies

Build custom generators for domain objects.

```python
@st.composite
def orders(draw):
    return Order(
        id=draw(st.uuids()),
        items=draw(st.lists(st.builds(LineItem), min_size=1)),
        customer_id=draw(st.uuids()),
        total=draw(st.decimals(min_value=0, max_value=10000)),
    )

@given(orders())
def test_order_processing(order):
    result = process_order(order)
    assert result.status in ("completed", "pending")
```

## Understanding Shrinking

When a test fails, Hypothesis simplifies the failing input to its minimal form.

```
# Original failure (complex, hard to debug)
Falsifying example: test_sort(xs=[3, 1, 4, 1, 5, 9, 2, 6, 0, -1, 7])

# After shrinking (reveals the actual bug)
Falsifying example: test_sort(xs=[1, 0])
```

The shrunk example shows the bug involves comparison of adjacent elements, not list length.

**Reading shrunk output**: Focus on what's left after shrinking. Hypothesis removes everything non-essential to the failure.

## Settings

Adjust behavior per-test or globally.

```python
from hypothesis import settings, Verbosity

# Increase examples for thorough testing
@settings(max_examples=500)
@given(st.lists(st.integers()))
def test_sort(xs): ...

# Verbose output for debugging
@settings(verbosity=Verbosity.verbose)
@given(st.integers())
def test_something(n): ...

# Longer deadline for slow operations
@settings(deadline=1000)  # milliseconds
@given(st.text())
def test_slow_operation(s): ...
```

### CI Configuration

Use profiles for different environments.

```python
# conftest.py
from hypothesis import settings, Phase

# Fast feedback during development
settings.register_profile("dev", max_examples=10)

# Thorough testing in CI
settings.register_profile("ci", max_examples=200)

# Exhaustive testing for releases
settings.register_profile("release", max_examples=1000)

# Load profile from environment
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "dev"))
```

## Example Database

Hypothesis saves failing examples and replays them on subsequent runs.

- Stored in `.hypothesis/examples` by default
- Commit this directory to version control to share failures across team
- Clear with `hypothesis.database.clear()` if needed

## Stateful Testing

For testing systems with state (APIs, databases), use rule-based state machines.

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

class ShoppingCartMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.cart = ShoppingCart()

    @rule(item=st.sampled_from(["apple", "banana", "orange"]))
    def add_item(self, item):
        self.cart.add(item)

    @rule()
    def clear_cart(self):
        self.cart.clear()

    @invariant()
    def count_is_non_negative(self):
        assert self.cart.count() >= 0

TestShoppingCart = ShoppingCartMachine.TestCase
```

## Other Languages

| Language | Library | Notes |
|----------|---------|-------|
| Python | Hypothesis | Most mature, best shrinking |
| JavaScript/TypeScript | fast-check | Similar API to Hypothesis |
| Rust | proptest | Macro-based, good shrinking |
| Go | rapid | Simple, fast |
| Java | jqwik | JUnit 5 integration |
| Haskell | QuickCheck | The original, inspired all others |

## Sources

- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Hypothesis GitHub](https://github.com/HypothesisWorks/hypothesis)
