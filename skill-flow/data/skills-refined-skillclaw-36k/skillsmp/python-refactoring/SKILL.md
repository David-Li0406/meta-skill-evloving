---
name: python-refactoring
description: Python refactoring triggers and guidelines for code size limits
license: MIT
compatibility: opencode
metadata:
    related_coding_principles: For general coding principles, use skill `coding-principles`
    related_python_guidelines: For style and quality standards, use skill `python-guidelines`
---

# Python Refactoring Triggers

## What I Do

Provide guidelines for when to refactor Python code based on size limits and complexity thresholds.

## Size Limits

### Module Size (>250 lines)

```python
# When a single .py file exceeds 250 lines:

# OPTION 1: Split into multiple modules
# module/
#     __init__.py          # Public API
#     core.py              # Core functionality
#     helpers.py           # Helper functions
#     validators.py        # Validation logic

# OPTION 2: Extract functions
# Original module has many related functions
# Extract related functions into separate modules
# Use __init__.py to expose public API
```

### Function Size (>75 lines)

```python
# When a function exceeds 75 lines (declaration + body):

# BEFORE: Monolithic function
def process_data(data):
    # 80+ lines of mixed logic
    validate(data)
    transform(data)
    clean(data)
    aggregate(data)
    export(data)

# AFTER: Decomposed functions
def process_data(data):
    validate(data)
    transformed = transform_data(data)
    cleaned = clean_data(transformed)
    results = aggregate_data(cleaned)
    export_results(results)

def transform_data(data):
    # Single responsibility
    pass

def clean_data(data):
    # Single responsibility
    pass
```

### Class Size (>200 lines)

```python
# When a class exceeds 200 lines:

# BEFORE: God class with many responsibilities
class DataProcessor:
    def validate(self): ...
    def parse(self): ...
    def transform(self): ...
    def export(self): ...
    def log(self): ...
    def cache(self): ...

# AFTER: Split responsibilities
class DataProcessor:
    def __init__(self, validator, parser, transformer, exporter):
        self.validator = validator
        self.parser = parser
        self.transformer = transformer
        self.exporter = exporter

    def process(self, data):
        validated = self.validator.validate(data)
        parsed = self.parser.parse(validated)
        return self.transformer.transform(parsed)
```

## Refactoring Principles

### Single Responsibility

```python
# BAD: Multiple responsibilities
class UserService:
    def authenticate(self): ...      # Auth logic
    def send_email(self): ...        # Email logic
    def cache_data(self): ...        # Caching logic
    def generate_report(self): ...   # Reporting logic

# GOOD: Split by responsibility
class AuthService: ...
class EmailService: ...
class CacheService: ...
class ReportService: ...
```

### Composition over Inheritance

```python
# When class has too many attributes/dependencies:
# Use composition instead of inheritance

class DataProcessor:
    def __init__(self, validator, parser, transformer):
        # Inject dependencies
        self.validator = validator
        self.parser = parser
        self.transformer = transformer
```

## When to Use Me

Use this skill when:

- Code exceeds size thresholds
- Classes have too many methods
- Functions are too complex
- Refactoring decisions needed

## Key Rules

1. **Modules > 250 lines** - Split into multiple modules
2. **Functions > 75 lines** - Decompose into smaller functions
3. **Classes > 200 lines** - Apply SRP, consider composition
4. **Too many methods** - Split into smaller classes
5. **Too many dependencies** - Use dependency injection
