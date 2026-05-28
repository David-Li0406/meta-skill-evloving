# Clean Code Patterns

## Pythonic Patterns

### Use dataclasses for data containers
```python
# Bad
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

# Good
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
```

### Use context managers for resources
```python
# Bad
f = open("file.txt")
data = f.read()
f.close()

# Good
with open("file.txt") as f:
    data = f.read()
```

### Use comprehensions over loops
```python
# Bad
result = []
for item in items:
    if item.active:
        result.append(item.name)

# Good
result = [item.name for item in items if item.active]
```

### Use early returns
```python
# Bad
def process(data):
    if data is not None:
        if data.valid:
            return do_work(data)
        else:
            return None
    else:
        return None

# Good
def process(data):
    if data is None:
        return None
    if not data.valid:
        return None
    return do_work(data)
```

### Use walrus operator for assignment in conditions (Python 3.8+)
```python
# Bad
match = pattern.search(text)
if match:
    process(match.group())

# Good
if match := pattern.search(text):
    process(match.group())
```

### Use structural pattern matching (Python 3.10+)
```python
def handle_response(response: dict):
    match response:
        case {"status": "ok", "data": data}:
            return process(data)
        case {"status": "error", "message": msg}:
            raise APIError(msg)
        case _:
            raise ValueError("Unknown response format")
```

## SOLID Principles

### Single Responsibility
```python
# Bad - class does too much
class UserManager:
    def create_user(self, data): ...
    def send_email(self, user): ...
    def generate_report(self, users): ...

# Good - separate concerns
class UserRepository:
    def create(self, data): ...

class EmailService:
    def send(self, user): ...

class ReportGenerator:
    def generate(self, users): ...
```

### Dependency Injection
```python
# Bad - hard dependency
class UserService:
    def __init__(self):
        self.db = PostgresDatabase()

# Good - inject dependency
class UserService:
    def __init__(self, db: Database):
        self.db = db
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Module | snake_case | `user_service.py` |
| Class | PascalCase | `UserService` |
| Function | snake_case | `get_user_by_id` |
| Constant | UPPER_SNAKE | `MAX_RETRIES` |
| Private | _prefix | `_internal_method` |
| Type variable | Single uppercase or CamelCase | `T`, `UserT` |

## Anti-patterns to Avoid

- **God class**: Split into smaller focused classes
- **Feature envy**: Move method to class it uses most
- **Primitive obsession**: Use value objects
- **Long method**: Extract smaller methods
- **Dead code**: Delete unused code
- **Magic numbers**: Use named constants
