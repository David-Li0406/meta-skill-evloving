# Rename Patterns

Safe renaming across codebases.

## Safe Rename Process

### 1. Find All References

```bash
# Find all usages
grep -rn "old_name" --include="*.py" --include="*.ts"

# Find in specific patterns
grep -rn "old_name" --include="*.py" src/ tests/

# Check imports
grep -rn "from.*import.*old_name\|import.*old_name"
```

### 2. Check for Dynamic References

```python
# DANGER: These won't be found by simple search
getattr(obj, "old_name")
obj.__dict__["old_name"]
eval("old_name")
globals()["old_name"]
```

### 3. Rename with Tests

```bash
# 1. Run tests (should pass)
pytest

# 2. Rename using tool or sed
# Using IDE: F2 or Shift+F6
# Using sed:
find . -name "*.py" -exec sed -i 's/old_name/new_name/g' {} +

# 3. Run tests again (should pass)
pytest

# 4. Review changes
git diff
```

## Rename Types

### Variable/Parameter Rename

Low risk - usually local scope.

```python
# BEFORE
def calculate(x, y):
    r = x + y
    return r

# AFTER
def calculate(first_number, second_number):
    result = first_number + second_number
    return result
```

### Function/Method Rename

Medium risk - may have external callers.

```python
# Step 1: Add alias (backwards compatible)
def get_user_name(user):  # New name
    return user.full_name

get_username = get_user_name  # Old name as alias

# Step 2: Update all callers to use new name
# Step 3: Deprecate old name
import warnings

def get_username(user):
    warnings.warn("get_username is deprecated, use get_user_name", DeprecationWarning)
    return get_user_name(user)

# Step 4: After grace period, remove old name
```

### Class Rename

Higher risk - affects imports, type hints, inheritance.

```python
# Step 1: Create alias
class UserAccount:  # New name
    pass

User = UserAccount  # Old name as alias

# Step 2: Update all references
from models import UserAccount  # New
# from models import User      # Old

# Step 3: Remove alias after migration
```

### Module/Package Rename

Highest risk - affects imports everywhere.

```python
# Step 1: Create new module with alias import
# new_name.py
from old_name import *

# Step 2: Update imports in dependent code
# Step 3: Move code to new module
# Step 4: Make old module import from new (reverse alias)

# old_name.py (deprecated)
import warnings
warnings.warn("old_name is deprecated, use new_name", DeprecationWarning)
from new_name import *
```

## Naming Conventions

### Python

```python
# Variables and functions: snake_case
user_name = "Alice"
def calculate_total(): pass

# Classes: PascalCase
class UserAccount: pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3

# Private: leading underscore
_internal_cache = {}
def _helper_function(): pass

# "Really private": double underscore (name mangling)
class MyClass:
    def __init__(self):
        self.__secret = "hidden"
```

### TypeScript/JavaScript

```typescript
// Variables and functions: camelCase
const userName = "Alice";
function calculateTotal() {}

// Classes: PascalCase
class UserAccount {}

// Constants: UPPER_SNAKE_CASE or camelCase
const MAX_RETRY_COUNT = 3;
const maxRetryCount = 3;

// Private: # prefix (ES2022+) or underscore
class MyClass {
    #secret = "hidden";
    private _legacy = "old style";
}

// Interfaces/Types: PascalCase (often with I prefix)
interface IUser {}
type UserRole = "admin" | "user";
```

## Rename Checklist

### Before Rename

- [ ] Run all tests (must pass)
- [ ] Search for all references
- [ ] Check for dynamic/string references
- [ ] Check external dependencies
- [ ] Plan rollback

### During Rename

- [ ] Use IDE rename tool when possible
- [ ] Update in dependency order
- [ ] Update documentation
- [ ] Update configuration files
- [ ] Run tests after each file

### After Rename

- [ ] Run full test suite
- [ ] Check CI/CD passes
- [ ] Review changes
- [ ] Update changelog
- [ ] Notify team of breaking changes

## Common Pitfalls

### 1. String References

```python
# This won't be found by rename tool
config = {
    "handler": "old_handler_name"  # String reference!
}

# Solution: Search for strings too
grep -rn '"old_handler_name"\|'\''old_handler_name'\'''
```

### 2. Serialized Data

```python
# Data stored in database/files with old name
{"old_field": "value"}

# Solution: Migration or alias
@property
def new_field(self):
    return self._data.get("new_field") or self._data.get("old_field")
```

### 3. API Contracts

```python
# External API expects old name
@app.post("/api/users")
def create_user(data: dict):
    # Client sends: {"userName": "Alice"}
    # Can't just rename without breaking clients
```

Solution: Versioned API or field aliases
```python
class CreateUserRequest(BaseModel):
    user_name: str = Field(alias="userName")
```

### 4. Environment Variables

```python
# .env file still has old name
OLD_API_KEY=xxx

# Code uses new name
api_key = os.getenv("NEW_API_KEY")  # Returns None!
```

### 5. Database Columns

```python
# Database has old column name
# ORM model has new name
class User(Base):
    user_name = Column("username", String)  # Map new to old
```

## Gradual Rename Strategy

For high-risk renames:

```python
# Phase 1: Add new name, keep old
def new_name():
    return _implementation()

old_name = new_name  # Alias

# Phase 2: Deprecate old name
def old_name():
    warnings.warn("old_name deprecated, use new_name", DeprecationWarning)
    return new_name()

# Phase 3: Log usage of old name
def old_name():
    logger.warning(f"old_name called from {caller_info()}")
    return new_name()

# Phase 4: Remove old name (in next major version)
```
