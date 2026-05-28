# Technical Debt Fix Patterns

Quick reference for addressing common technical debt issues.

## Security Issues

### Hardcoded Credentials
```python
# ❌ Bad
DB_PASSWORD = "secret123"
api_key = "sk-abc123"

# ✅ Good
import os
DB_PASSWORD = os.environ.get("DB_PASSWORD")
api_key = os.environ.get("API_KEY")

# ✅ Better: Use a secrets manager
from your_secrets_manager import get_secret
DB_PASSWORD = get_secret("db/password")
```

### Shell Injection
```python
# ❌ Bad
subprocess.run(f"ls {user_input}", shell=True)

# ✅ Good
subprocess.run(["ls", user_input], shell=False)
```

### Unsafe Deserialization
```python
# ❌ Bad
data = pickle.loads(untrusted_bytes)

# ✅ Good (for simple data)
data = json.loads(untrusted_string)

# ✅ Good (if pickle needed)
import hmac
if hmac.compare_digest(signature, expected_sig):
    data = pickle.loads(trusted_bytes)
```

## Dependency Issues

### Pinning Strategy
```txt
# requirements.txt

# ❌ Bad - unpinned
requests

# ⚠️ Risky - no upper bound  
requests>=2.0

# ✅ Good - exact pin
requests==2.31.0

# ✅ Good - bounded range
requests>=2.31.0,<3.0
```

### Updating Vulnerable Packages
```bash
# Check current vulnerabilities
pip-audit

# Update specific package
pip install --upgrade <package>

# Update and regenerate requirements
pip install --upgrade <package>
pip freeze > requirements.txt
```

## Testing Gaps

### Creating Test Files
```python
# tests/test_mymodule.py
import pytest
from mypackage import mymodule

class TestMyFunction:
    def test_happy_path(self):
        result = mymodule.my_function(valid_input)
        assert result == expected_output
    
    def test_edge_case(self):
        result = mymodule.my_function(edge_input)
        assert result == edge_expected
    
    def test_error_handling(self):
        with pytest.raises(ValueError):
            mymodule.my_function(invalid_input)
```

### Improving Coverage
Focus on:
1. Error handling paths (try/except branches)
2. Conditional branches (if/else)
3. Loop edge cases (empty, single, many items)
4. Boundary conditions

## Maintainability

### Adding Docstrings
```python
def process_order(order_id: str, items: list[Item], priority: bool = False) -> OrderResult:
    """Process a customer order and return the result.
    
    Args:
        order_id: Unique identifier for the order.
        items: List of items to include in the order.
        priority: If True, process with expedited handling.
    
    Returns:
        OrderResult containing status and tracking info.
    
    Raises:
        InvalidOrderError: If order_id is malformed.
        OutOfStockError: If any item is unavailable.
    """
```

### Adding Type Hints
```python
# Basic types
def greet(name: str) -> str: ...

# Collections
def process(items: list[int]) -> dict[str, int]: ...

# Optional
def find(key: str) -> str | None: ...

# Complex types
from typing import TypedDict, Callable

class Config(TypedDict):
    host: str
    port: int
    
Handler = Callable[[Request], Response]
```

### Reducing Function Arguments
```python
# ❌ Bad - too many args
def create_user(name, email, age, address, phone, department, role, manager_id):
    ...

# ✅ Good - config object
@dataclass
class UserConfig:
    name: str
    email: str
    age: int
    address: str
    phone: str
    department: str
    role: str
    manager_id: str | None = None

def create_user(config: UserConfig):
    ...
```

## Deferred Work

### Handling TODO/FIXME
```python
# ❌ Vague
# TODO: fix this later

# ✅ Actionable with context
# TODO(JIRA-123): Implement retry logic for transient failures
#   Current behavior: fails immediately on network error
#   Needed: exponential backoff with max 3 retries

# ✅ Or convert to issue and reference
# See JIRA-456 for planned caching implementation
```

### Replacing HACK/Workaround
1. Document why hack exists (if not already)
2. Create ticket for proper fix
3. Add ticket reference to comment
4. Prioritize based on risk/impact
