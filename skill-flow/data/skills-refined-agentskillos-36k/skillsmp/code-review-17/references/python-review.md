# Python Code Review Checklist

## Type Hints

### Required Type Hints

```
□ Function parameters have type hints
□ Function return types specified
□ Class attributes have type hints
□ Generic types properly parameterized (list[str], dict[str, int])
□ Optional types explicit (str | None, not Optional[str])
□ Protocol used for interfaces (not ABC where possible)
```

**Examples:**

```python
# BAD: Missing type hints
def process_user(user, options):
    ...

# GOOD: Complete type hints
def process_user(user: User, options: ProcessOptions) -> ProcessResult:
    ...

# BAD: Old-style Optional
from typing import Optional, List, Dict
def get_user(id: int) -> Optional[User]:
    items: List[str] = []
    mapping: Dict[str, int] = {}

# GOOD: Modern syntax (Python 3.10+)
def get_user(id: int) -> User | None:
    items: list[str] = []
    mapping: dict[str, int] = {}
```

---

## Async/Await Patterns

### Async Best Practices

```
□ async def for I/O-bound operations
□ def for CPU-bound operations
□ await used correctly (not forgotten)
□ No blocking calls in async functions
□ asyncio.gather for concurrent operations
□ Proper timeout handling
```

**Examples:**

```python
# BAD: Blocking call in async function
async def fetch_data():
    response = requests.get(url)  # Blocks event loop!
    return response.json()

# GOOD: Async HTTP client
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# BAD: Sequential async calls
async def process_all(ids: list[str]):
    results = []
    for id in ids:
        result = await fetch_one(id)  # Sequential, slow
        results.append(result)
    return results

# GOOD: Concurrent async calls
async def process_all(ids: list[str]):
    tasks = [fetch_one(id) for id in ids]
    return await asyncio.gather(*tasks)  # Concurrent, fast

# GOOD: With timeout
async def fetch_with_timeout():
    try:
        return await asyncio.wait_for(fetch_data(), timeout=5.0)
    except asyncio.TimeoutError:
        raise ServiceTimeoutError()
```

---

## Error Handling

### Exception Best Practices

```
□ Specific exceptions caught (not bare except)
□ Custom exceptions for domain errors
□ Exception context preserved (raise ... from e)
□ Resources cleaned up (try/finally or context manager)
□ Errors logged appropriately
□ User-friendly error messages
```

**Examples:**

```python
# BAD: Bare except
try:
    result = do_something()
except:  # Catches everything including KeyboardInterrupt!
    pass

# BAD: Too broad
try:
    result = do_something()
except Exception:  # Catches too much
    return None

# GOOD: Specific exceptions
try:
    result = do_something()
except ValueError as e:
    logger.warning(f"Invalid value: {e}")
    raise ValidationError(str(e)) from e
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise ServiceUnavailableError() from e

# BAD: Lost context
try:
    ...
except SomeError:
    raise DifferentError("Something failed")  # Original traceback lost!

# GOOD: Preserved context
try:
    ...
except SomeError as e:
    raise DifferentError("Something failed") from e  # Chain preserved
```

---

## Data Classes

### Dataclass Best Practices

```
□ frozen=True for immutable types
□ slots=True for memory efficiency
□ kw_only=True for clarity (Python 3.10+)
□ Default values use field() for mutable types
□ __post_init__ for validation
```

**Examples:**

```python
# BAD: Mutable dataclass
@dataclass
class Config:
    items: list[str] = []  # Mutable default! Shared between instances!

# GOOD: Proper mutable defaults
@dataclass
class Config:
    items: list[str] = field(default_factory=list)

# GOOD: Immutable Value Object
@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

# GOOD: Entity with explicit keyword args
@dataclass(kw_only=True)
class User:
    id: UserId
    email: Email
    name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
```

---

## Performance Considerations

### Performance Checklist

```
□ No N+1 query problems
□ Proper use of generators for large data
□ Caching where appropriate
□ Lazy loading for expensive operations
□ Connection pooling used
□ Bulk operations where possible
```

**Examples:**

```python
# BAD: N+1 queries
for user in users:
    orders = await order_repo.get_by_user(user.id)  # Query per user!

# GOOD: Eager loading or batch query
orders_by_user = await order_repo.get_by_users([u.id for u in users])

# BAD: Loading all into memory
def process_large_file(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)  # Entire file in memory!

# GOOD: Streaming/generator
def process_large_file(path: str) -> Iterator[dict]:
    with open(path) as f:
        for line in f:
            yield json.loads(line)

# BAD: Creating connection per request
async def fetch_data():
    client = httpx.AsyncClient()  # New connection each time
    response = await client.get(url)
    await client.aclose()

# GOOD: Reusing connections
class DataFetcher:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client  # Injected, reused

    async def fetch(self):
        return await self._client.get(url)
```

---

## CI Lint & Format (Pre-commit)

### 커밋 전 필수 검증

**CRITICAL**: 코드 작성/수정 후 반드시 로컬에서 lint와 format을 실행하세요.

```bash
# 필수 검증 명령어 (커밋 전 실행)
black --check <path>       # 포맷팅 검증
ruff check <path>          # 린트 검증

# 자동 수정
black <path>               # 포맷팅 자동 적용
ruff check <path> --fix    # 린트 자동 수정
```

### CI에서 검증하는 항목

| Tool | 검증 항목 | 자동 수정 |
|------|----------|----------|
| **Black** | 코드 포맷팅 (줄 길이, 공백, 들여쓰기) | `black <path>` |
| **Ruff** | Unused imports, undefined names, 스타일 | `ruff check --fix` |
| **isort** | Import 정렬 | `isort <path>` |
| **mypy** | 타입 체크 (선택) | N/A |

### 자주 발생하는 Ruff 오류

```python
# F401: Unused import
import pytest  # 사용하지 않으면 제거

# F841: Unused variable
result = do_something()  # 사용하지 않으면 _ 또는 제거

# E501: Line too long (Black이 대부분 처리)
# E711: Comparison to None (use `is None`)
if x == None:  # BAD
if x is None:  # GOOD

# E712: Comparison to True/False
if x == True:   # BAD
if x is True:   # GOOD (또는 그냥 if x:)
```

### Pre-commit Hook 활용

```bash
# .pre-commit-config.yaml이 있는 경우
pre-commit run --all-files
```

---

## Code Style

### Style Guidelines

```
□ Line length ≤ 88 characters (Black default)
□ Imports sorted (isort)
□ No unused imports
□ No unused variables
□ Meaningful variable names
□ Constants in UPPER_CASE
□ Classes in PascalCase
□ Functions/variables in snake_case
```

### Function Design

```
□ Functions do one thing (single responsibility)
□ Functions are small (< 20 lines ideal)
□ No more than 3-4 parameters
□ Early returns for guard clauses
□ No deep nesting (max 3 levels)
```

**Examples:**

```python
# BAD: Long function with many responsibilities
def process_order(order_data: dict) -> Order:
    # Validate (50 lines)
    # Create order (30 lines)
    # Calculate totals (20 lines)
    # Apply discounts (40 lines)
    # Save to database (20 lines)
    # Send notification (30 lines)
    ...

# GOOD: Small, focused functions
def process_order(order_data: dict) -> Order:
    validated = validate_order_data(order_data)
    order = create_order(validated)
    order = apply_discounts(order)
    await save_order(order)
    await send_notification(order)
    return order

# BAD: Deep nesting
def process(items):
    for item in items:
        if item.is_valid:
            if item.type == "A":
                if item.value > 0:
                    # Deep logic here
                    pass

# GOOD: Early returns / guard clauses
def process(items):
    for item in items:
        if not item.is_valid:
            continue
        if item.type != "A":
            continue
        if item.value <= 0:
            continue
        # Flat logic here
```

---

## Testing Patterns

### Test Quality Checklist

```
□ Test names describe behavior (test_user_creation_fails_with_invalid_email)
□ Arrange-Act-Assert pattern used
□ One assertion per test (ideally)
□ Mocks used for external dependencies
□ Edge cases covered
□ No test interdependencies
□ Fixtures reused appropriately
```

**Examples:**

```python
# BAD: Unclear test name
def test_user():
    ...

# GOOD: Descriptive test name
def test_create_user_raises_error_when_email_already_exists():
    ...

# BAD: Multiple assertions, unclear failure
def test_user_creation():
    user = create_user(...)
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active == True
    assert len(user.roles) == 1

# GOOD: Focused assertions (or use pytest.mark.parametrize)
def test_create_user_assigns_unique_id():
    user = create_user(...)
    assert user.id is not None

def test_create_user_sets_email():
    user = create_user(email="test@example.com", ...)
    assert user.email == "test@example.com"

# GOOD: Arrange-Act-Assert
async def test_order_total_includes_tax():
    # Arrange
    order = Order(items=[
        OrderItem(price=100, quantity=2),
    ])
    tax_calculator = TaxCalculator(rate=0.1)

    # Act
    total = tax_calculator.calculate_total(order)

    # Assert
    assert total == 220  # 200 + 10% tax
```
