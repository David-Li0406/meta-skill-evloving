# Testing Anti-Patterns

These patterns create false confidence—tests that pass but don't catch bugs.

## Anti-Pattern 1: The Liar (Tests That Can't Fail)

**Problem**: A test that passes regardless of whether the code works. Often written after implementation without verifying it can fail.

**Example**:

```python
# ❌ BAD: "The Liar" - this test always passes
def test_store_report(self):
    mock_client = MagicMock()  # MagicMock() is truthy by default
    service.store_report('NVDA19', 'report text')
    mock_client.execute.assert_called()  # Only checks "was it called?"
    # Missing: What if execute() returned 0 rows? Test still passes!

# ✅ GOOD: Test can actually fail when code is broken
def test_store_report_detects_failure(self):
    mock_client = MagicMock()
    mock_client.execute.return_value = 0  # Simulate FK constraint failure
    result = service.store_report('NVDA19', 'report text')
    assert result is False, "Should return False when INSERT affects 0 rows"
```

**Detection**: After writing a test, intentionally break the code. If the test still passes, it's a Liar.

**Fix**: Assert outcomes, not just execution. Verify return values and state changes.

---

## Anti-Pattern 2: Happy Path Only

**Problem**: Testing only success scenarios, never failures.

**Example**:

```python
# ❌ BAD: Only tests success
def test_fetch_ticker(self):
    mock_yf.download.return_value = sample_dataframe
    result = service.fetch('NVDA')
    assert result is not None

# ✅ GOOD: Tests both success AND failure paths
def test_fetch_ticker_success(self):
    mock_yf.download.return_value = sample_dataframe
    result = service.fetch('NVDA')
    assert len(result) > 0

def test_fetch_ticker_returns_none_on_empty(self):
    mock_yf.download.return_value = pd.DataFrame()  # Empty result
    result = service.fetch('INVALID')
    assert result is None

def test_fetch_ticker_handles_timeout(self):
    mock_yf.download.side_effect = TimeoutError()
    result = service.fetch('NVDA')
    assert result is None  # Graceful degradation
```

**Fix**: Test failure modes, edge cases, and error handling—not just the happy path.

---

## Anti-Pattern 3: Testing Implementation, Not Behavior

**Problem**: Testing *how* code does something rather than *what* it achieves.

**Example**:

```python
# ❌ BAD: Tests implementation details (brittle)
def test_cache_stores_correctly(self):
    service.store_report('NVDA19', 'report')
    # Asserts exact SQL string - breaks on any query change
    mock_client.execute.assert_called_with(
        "INSERT INTO reports (symbol, text) VALUES (%s, %s)",
        ('NVDA19', 'report')
    )

# ✅ GOOD: Tests behavior (survives refactoring)
def test_stored_report_can_be_retrieved(self):
    service.store_report('NVDA19', 'report text')
    result = service.get_report('NVDA19')
    assert result['text'] == 'report text'  # The actual contract
```

**Kent Beck's Rule**: "Tests should be sensitive to behavior changes and insensitive to structure changes."

**Fix**: Test the public contract (what users/consumers experience), not internal implementation.

---

## Anti-Pattern 4: Mock Overload (The Mockery)

**Problem**: So many mocks that you're testing the mocks, not the code.

**Example**:

```python
# ❌ BAD: Testing mocks, not behavior
@patch('service.db_client')
@patch('service.cache')
@patch('service.logger')
@patch('service.metrics')
@patch('service.validator')
def test_process(self, mock_validator, mock_metrics, mock_logger, mock_cache, mock_db):
    mock_validator.validate.return_value = True
    mock_cache.get.return_value = None
    mock_db.query.return_value = [{'id': 1}]
    # ... 20 more lines of mock setup
    # What are we even testing at this point?

# ✅ GOOD: Mock only external boundaries
@patch('service.external_api')  # Only mock what crosses system boundary
def test_process(self, mock_api):
    mock_api.fetch.return_value = {'data': 'value'}
    result = service.process('input')
    assert result['status'] == 'success'
```

**Rule**: If test setup is longer than the test itself, the code needs refactoring, not more mocks.

**Fix**:
- Mock only external boundaries (databases, APIs, file I/O)
- Keep internal logic testable without mocks
- Consider integration tests instead of over-mocking

---

## Anti-Pattern 5: Schema Testing Within Service Boundaries

**The Litmus Test**: "If changing this breaks consumers, it's a contract (test it). If changing this doesn't affect consumers, it's implementation (don't test it)."

**Kent Beck's Rule Clarified**:
> "Tests should be sensitive to behavior changes and insensitive to structure changes."

This appears to conflict with testing data schemas. The resolution:

- **Within a service boundary**: Schema is implementation (SQL table structure, internal class shapes)
- **Across service boundaries**: Schema IS the behavior (the interface contract)

**When Schema Testing IS Appropriate:**
- Producer/consumer architectures (scheduler writes data, UI reads it)
- Event-driven systems (event shape is the contract)
- API versioning (request/response structure is public contract)
- Shared data stores accessed by multiple services

**When Schema Testing is an Anti-Pattern:**
- Internal database table structures (implementation detail)
- Private class attributes (encapsulation)
- Function parameters within same codebase (refactoring breaks tests)

**Example - The Distinction:**

```python
# ❌ ANTI-PATTERN: Testing internal structure
def test_database_columns(self):
    """Don't: SQL schema can change without breaking behavior"""
    cursor.execute("DESCRIBE reports")
    assert 'created_at' in columns  # Breaks on column rename

# ✅ PATTERN: Testing cross-service contract
def test_api_response_schema(self):
    """Do: API contract must remain stable for consumers"""
    response = api.get_report('NVDA19')
    assert 'created_at' in response  # External contract
    assert isinstance(response['price_history'], list)
    assert len(response['price_history']) >= 30
```

**Why This Matters**: When services communicate through shared data, changing the data format in one service can silently break others—even when each service's tests pass in isolation. Schema contract tests catch integration failures that unit tests miss.

---

## Summary: Red Flags

| Red Flag | Likely Anti-Pattern |
|----------|---------------------|
| Test passes even when code is broken | The Liar |
| Only `test_success()` methods, no `test_error()` | Happy Path Only |
| Test breaks when you refactor (but behavior unchanged) | Testing Implementation |
| Test setup longer than test body | Mock Overload |
| Test asserts internal SQL/class structure | Schema Testing (internal) |

## References

- [Software Testing Anti-patterns (Codepipes)](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
- [Unit Testing Anti-Patterns (Yegor Bugayenko)](https://www.yegor256.com/2018/12/11/unit-testing-anti-patterns.html)
- [Learn Go with Tests: Anti-patterns](https://quii.gitbook.io/learn-go-with-tests/meta/anti-patterns)
- See [PATTERNS.md](PATTERNS.md) for correct patterns
- See [DEFENSIVE.md](DEFENSIVE.md) for defensive validation
