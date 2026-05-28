# Example Pattern Descriptions Using Story-Based Framing

This document contains example pattern descriptions using the narrative four-act structure. Each example demonstrates how to apply story-based framing to different code anti-patterns.

## Example 1: The Fake Generic (Union-Polluted Generic)

### Act 1: The Promise

A generic class `TemplateExpander(Generic[T])` promises to preserve type T throughout its operations. The TypeVar is constrained to specific types:

```python
T = TypeVar('T', str, list[str])

class TemplateExpander(Generic[T]):
    """Expands template strings with context-specific values."""
```

### Act 2: The Betrayal

But the constructor accepts `raw_value: ConfigValue` (a union type alias) instead of `raw_value: T`, storing a union type rather than the promised generic parameter:

```python
ConfigValue: TypeAlias = str | list[str]

def __init__(self, raw_value: ConfigValue, config: BuildConfig) -> None:
    self._raw_value = raw_value  # Type: ConfigValue (union), not T
```

The generic parameter T exists but is never actually used.

### Act 3: The Consequences

Methods contain `isinstance()` checks and `# type: ignore` comments to work around the type mismatch:

```python
def expand(self) -> str | list[str]:
    if isinstance(self._raw_value, str):
        return self._expand_string(self._raw_value)  # type: ignore
    else:
        return [self._expand_string(item) for item in self._raw_value]  # type: ignore
```

`@overload` declarations attempt to paper over the union issue, adding complexity without fixing the root cause.

### Act 4: The Source

Values originate from heterogeneous storage where specific type information is lost at the storage boundary:

```python
class BuildConfig:
    _values: dict[str, str | list[str]]  # Union storage loses type info

    def get_expander(self, key: str) -> TemplateExpander[???]:
        value = self._values[key]  # Gets union type
        return TemplateExpander(value, self)  # T becomes indeterminate
```

### The Fix

Use TypeGuard to narrow the union BEFORE instantiation, and change constructor to accept the type parameter directly:

```python
def is_str(value: ConfigValue) -> TypeGuard[str]:
    return isinstance(value, str)

def is_list_str(value: ConfigValue) -> TypeGuard[list[str]]:
    return isinstance(value, list)

class BuildConfig:
    def get_expander(self, key: str) -> TemplateExpander[str] | TemplateExpander[list[str]]:
        value = self._values[key]
        if is_str(value):
            return TemplateExpander(value, self)  # T = str
        else:
            return TemplateExpander(value, self)  # T = list[str]

class TemplateExpander(Generic[T]):
    def __init__(self, raw_value: T, config: BuildConfig) -> None:
        self._raw_value: T = raw_value  # Properly typed as T
```

## Example 2: The Type Eraser (Unnecessary cast() Usage)

### Act 1: The Promise

A function returns a properly typed result from parsing JSON configuration:

```python
def parse_config(raw_json: str) -> AppConfig:
    """Parses JSON and returns strongly-typed configuration object."""
```

### Act 2: The Betrayal

But internally, the function uses `cast()` to force type checker acceptance without actual runtime validation:

```python
def parse_config(raw_json: str) -> AppConfig:
    data = json.loads(raw_json)  # Type: Any
    return cast(AppConfig, data)  # Lies to type checker
```

No validation ensures `data` actually matches `AppConfig` structure.

### Act 3: The Consequences

Downstream code trusts the type and crashes at runtime with `AttributeError` or `KeyError`:

```python
def use_config(config: AppConfig) -> None:
    host = config.database.host  # AttributeError: dict has no attribute 'database'
```

`# type: ignore` comments proliferate as the lie propagates through the codebase.

### Act 4: The Source

The pattern originates from trusting external data sources (APIs, config files, user input) without validation:

```python
# Configuration comes from untrusted external file
with open("config.json") as f:
    config = parse_config(f.read())  # Blindly trusts file format
```

### The Fix

Use runtime validation (TypedDict, Pydantic, dataclasses with validation) instead of cast():

```python
from pydantic import BaseModel

class AppConfig(BaseModel):
    database: DatabaseConfig
    server: ServerConfig

def parse_config(raw_json: str) -> AppConfig:
    data = json.loads(raw_json)
    return AppConfig.model_validate(data)  # Runtime validation
```

## Example 3: The Any Spreader (Any Type Propagation)

### Act 1: The Promise

A data processing function promises to transform typed input into typed output:

```python
def process_records(records: list[Record]) -> list[ProcessedRecord]:
    """Transforms records with business logic."""
```

### Act 2: The Betrayal

But the function uses `Any` for intermediate results, losing type information mid-pipeline:

```python
def process_records(records: list[Record]) -> list[ProcessedRecord]:
    intermediate: Any = [transform_step1(r) for r in records]
    validated: Any = [validate(item) for item in intermediate]
    return [finalize(v) for v in validated]  # Type checker can't verify
```

### Act 3: The Consequences

Methods downstream receive `Any` and lose all type safety:

```python
def analyze(processed: list[ProcessedRecord]) -> Report:
    total = sum(item.value for item in processed)  # No attribute checking
    # Type checker can't catch: item.vlaue (typo) or missing attributes
```

### Act 4: The Source

The pattern originates from using untyped libraries or lazy type annotations:

```python
import legacy_library  # No type stubs available

def process_records(records: list[Record]) -> list[ProcessedRecord]:
    intermediate = legacy_library.transform(records)  # Returns Any
    # Any spreads through the pipeline
```

### The Fix

Add explicit type annotations at each step, use `cast()` with runtime validation for library boundaries:

```python
from typing import assert_type

def process_records(records: list[Record]) -> list[ProcessedRecord]:
    intermediate: list[StepOneResult] = [transform_step1(r) for r in records]
    validated: list[ValidatedResult] = [validate(item) for item in intermediate]
    result: list[ProcessedRecord] = [finalize(v) for v in validated]
    return result

# For untyped library boundaries:
def safe_transform(records: list[Record]) -> list[StepOneResult]:
    result = legacy_library.transform(records)
    # Runtime validation before cast
    if not all(hasattr(r, 'expected_attr') for r in result):
        raise ValueError("Library returned unexpected structure")
    return cast(list[StepOneResult], result)
```

## Example 4: The Mutable Default (Mutable Default Argument)

### Act 1: The Promise

A function promises to create a new, independent list for each call:

```python
def add_item(item: str, items: list[str] = []) -> list[str]:
    """Adds item to list, returns the list."""
```

### Act 2: The Betrayal

But the default argument `[]` is evaluated once at function definition, creating a shared mutable object:

```python
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items
    # All callers using default share the SAME list object
```

### Act 3: The Consequences

Callers experience unexpected state pollution across independent calls:

```python
result1 = add_item("first")   # ["first"]
result2 = add_item("second")  # ["first", "second"] - UNEXPECTED!
result3 = add_item("third")   # ["first", "second", "third"] - POLLUTION!
```

### Act 4: The Source

The pattern originates from misunderstanding Python's default argument evaluation timing:

```python
# Default arguments evaluated ONCE at function definition
def my_func(arg: list[str] = []):  # This [] created once
    pass

# Every call without argument uses the SAME list object
```

### The Fix

Use `None` as default and create new mutable object inside function:

```python
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []  # New list for each call
    items.append(item)
    return items
```

## Pattern Template (Copy and Customize)

### Act 1: The Promise

{What the code claims to do or appears to implement correctly}

```python
# Code example showing the declaration
```

### Act 2: The Betrayal

{Where the implementation violates the promise}

```python
# Code example showing the violation
```

### Act 3: The Consequences

{Observable symptoms that result from the violation}

```python
# Code example showing the symptoms
```

### Act 4: The Source

{Why the pattern exists - architectural root cause}

```python
# Code example showing the origin
```

### The Fix

{Brief description of the correct solution}

```python
# Code example showing the resolution
```
