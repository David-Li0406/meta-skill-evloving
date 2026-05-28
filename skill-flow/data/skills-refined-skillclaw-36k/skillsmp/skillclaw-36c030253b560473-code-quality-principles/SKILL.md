---
name: code-quality-principles
description: Use this skill when you need guidance on fundamental software design principles to reduce complexity, prevent over-engineering, and improve maintainability.
---

# Code Quality Principles

Guidance on KISS, YAGNI, and SOLID principles with language-specific examples.

## KISS (Keep It Simple, Stupid)

**Principle**: Avoid unnecessary complexity. Prefer obvious solutions over clever ones.

### Guidelines

| Prefer              | Avoid                           |
| ------------------- | ------------------------------- |
| Simple conditionals | Complex regex for simple checks |
| Explicit code       | Magic numbers/strings           |
| Standard patterns   | Clever shortcuts                |
| Direct solutions    | Over-abstracted layers          |

### Python Example

```python
# Bad: Overly clever one-liner
users = [u for u in (db.get(id) for id in ids) if u and u.active and not u.banned]

# Good: Clear and readable
users = []
for user_id in ids:
    user = db.get(user_id)
    if user and user.active and not user.banned:
        users.append(user)
```

### Rust Example

```rust
// Bad: Unnecessary complexity
fn process(data: &[u8]) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
    data.iter()
        .map(|&b| b.checked_add(1).ok_or("overflow"))
        .collect::<Result<Vec<_>, _>>()
        .map_err(|e| e.into())
}

// Good: Simple and clear
fn process(data: &[u8]) -> Result<Vec<u8>, &'static str> {
    let mut result = Vec::with_capacity(data.len());
    for &byte in data {
        result.push(byte.checked_add(1).ok_or("overflow")?);
    }
    Ok(result)
}
```

## YAGNI (You Aren't Gonna Need It)

**Principle**: Don't implement features until they are actually needed.

### Guidelines

| Do                            | Don't                              |
| ----------------------------- | ---------------------------------- |
| Solve current problem         | Build for hypothetical futures     |
| Add when 3rd use case appears | Create abstractions for 1 use case |
| Delete dead code              | Keep "just in case" code           |
| Minimal viable solution       | Premature optimization             |

### Python Example

```python
# Bad: Premature abstraction for one use case
class AbstractDataProcessor:
    def process(self, data): ...
    def validate(self, data): ...
    def transform(self, data): ...

class CSVProcessor(AbstractDataProcessor):
    def process(self, data):
        return self.transform(self.validate(data))

# Good: Simple function until more cases appear
def process_csv(data):
    # Implementation here
```