# Test Isolation Guide
**Version:** {{VERSION}}

Patterns for ensuring tests run independently without affecting each other.

---

## Why Isolation Matters

Tests must be:
- **Independent** - Pass/fail regardless of other tests
- **Repeatable** - Same result every run
- **Self-contained** - Set up and clean up own data

---

## Mocking External Dependencies

### When to Mock
- External APIs (network calls)
- Third-party services
- System clock/time
- Random number generators

### Pattern: Replace with Test Double

```python
# Instead of real API call
def test_user_creation():
    # Mock the email service
    mock_email = Mock()
    user_service = UserService(email_service=mock_email)

    user_service.create_user("test@example.com")

    mock_email.send.assert_called_once()
```

### Key Points
- Mock at boundaries (APIs, databases, file system)
- Inject dependencies to enable mocking
- Verify mock was called correctly

---

## Test Doubles

| Type | Purpose | Use When |
|------|---------|----------|
| **Stub** | Returns fixed data | Need predictable input |
| **Mock** | Verifies interactions | Testing calls were made |
| **Fake** | Simplified implementation | Need working but fast version |
| **Spy** | Records calls to real object | Need real behavior + verification |

### Choosing the Right Double

```
Need predictable data? → Stub
Need to verify calls? → Mock
Need real-ish behavior? → Fake
Need both real + verify? → Spy
```

---

## Database Isolation

### Pattern 1: Transaction Rollback

```python
def setUp(self):
    self.transaction = db.begin()

def tearDown(self):
    self.transaction.rollback()  # Undo all changes
```

**Pros:** Fast, automatic cleanup
**Cons:** Can't test commit behavior

### Pattern 2: Fresh Database Per Test

```python
def setUp(self):
    db.create_all()  # Create tables

def tearDown(self):
    db.drop_all()    # Remove everything
```

**Pros:** Complete isolation
**Cons:** Slower

### Pattern 3: In-Memory Database

```python
# Use SQLite in-memory for tests
TEST_DATABASE_URL = "sqlite:///:memory:"
```

**Pros:** Very fast, no cleanup needed
**Cons:** May differ from production DB

### Key Points
- Never share database state between tests
- Each test creates its own data
- Clean up in tearDown, not setUp

---

## File System Isolation

### Pattern 1: Temporary Directories

```python
import tempfile

def setUp(self):
    self.temp_dir = tempfile.mkdtemp()

def tearDown(self):
    shutil.rmtree(self.temp_dir)
```

### Pattern 2: Mock File Operations

```python
@patch('builtins.open', mock_open(read_data='test content'))
def test_file_reading(self, mock_file):
    result = read_config_file()
    assert result == 'test content'
```

### Key Points
- Never write to real project directories
- Use temp directories or mocks
- Clean up created files in tearDown

---

## State Isolation Checklist

Before each test runs:
- [ ] Database in known state
- [ ] No leftover files
- [ ] Global variables reset
- [ ] Mocks configured fresh
- [ ] Time/random mocked if needed

After each test runs:
- [ ] Database rolled back/cleaned
- [ ] Temp files deleted
- [ ] Mocks reset
- [ ] Resources released

---

## Common Mistakes

- **Shared test data** - Each test should create its own data
- **Forgetting cleanup** - Always clean up in tearDown
- **Order-dependent tests** - Tests must pass in any order

---

## Quick Reference

| What to Isolate | How |
|-----------------|-----|
| External APIs | Mock/Stub |
| Database | Transaction rollback or fresh DB |
| File system | Temp directories or mock |
| Time | Mock datetime/clock |
| Random values | Fixed seed or mock |
| Global state | Reset in setUp/tearDown |
