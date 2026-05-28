# Defensive Programming in Tests

**Core Principle**: Fail fast and visibly when something is wrong. Silent failures hide bugs.

## Key Defensive Patterns

### 1. Validate Configuration at Startup

**Principle**: Prevent production surprises by catching configuration issues early.

```python
# ❌ BAD: Fails during test execution
def test_fetch_data(self):
    result = api.fetch(url=os.getenv('API_URL'))  # Fails if not set
    assert result is not None

# ✅ GOOD: Validates at startup
@pytest.fixture(scope='session', autouse=True)
def validate_env():
    """Run once before all tests"""
    required = ['API_URL', 'API_KEY', 'AURORA_HOST']
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        pytest.fail(f"Missing required env vars: {missing}")
```

### 2. Explicit Failure Detection

**Principle**: Check operation outcomes (rowcount, status codes), not just absence of exceptions.

```python
# ❌ BAD: Assumes no exception = success
def test_store_data(self):
    service.store('NVDA19', price=150.25)  # Might silently fail
    # No assertion - if no exception raised, test passes

# ✅ GOOD: Checks operation outcome
def test_store_data(self):
    result = service.store('NVDA19', price=150.25)
    assert result is True, "Store operation should return True on success"

    # Verify data actually stored (round-trip)
    stored = service.get('NVDA19')
    assert stored['price'] == 150.25
```

### 3. Progressive Evidence Strengthening in Tests

Tests should verify through **all evidence layers**, not just surface signals.

**Evidence hierarchy for tests**:
1. **Surface**: Test didn't raise exception (weakest)
2. **Content**: Assertions passed (stronger)
3. **Observability**: No error logs during test (stronger)
4. **Ground truth**: Actual side effects match intent (strongest)

**Example**:
```python
def test_user_creation():
    # Layer 1: Surface (test runs without exception)
    user = create_user("test@example.com")

    # Layer 2: Content (assertions pass)
    assert user.email == "test@example.com"
    assert user.id is not None

    # Layer 3: Observability (no errors logged)
    assert len(caplog.records) == 0

    # Layer 4: Ground truth (database state matches)
    db_user = db.query(User).filter_by(id=user.id).first()
    assert db_user is not None
    assert db_user.email == "test@example.com"
```

**Anti-pattern**: Stopping at surface
```python
def test_save_data():
    save_data(item)
    # Test passes but doesn't verify data actually saved! (only verified no exception)
```

**Correct pattern**: Verify ground truth
```python
def test_save_data():
    save_data(item)
    # Verify database state (ground truth)
    assert db.query(Item).filter_by(id=item.id).first() is not None
```

See CLAUDE.md Principle #2 for the general pattern.

### 4. No Silent Fallbacks

**Principle**: Default values should be explicit, not hidden error recovery.

```python
# ❌ BAD: Silent fallback hides failures
def get_config(key):
    return os.getenv(key) or 'default_value'  # Hides missing env var

def test_uses_config(self):
    result = service.process()  # Uses fallback, test passes
    assert result is not None  # But wrong config!

# ✅ GOOD: Explicit defaults, fail on missing required config
def get_config(key, default=None, required=False):
    value = os.getenv(key)
    if required and not value:
        raise ValueError(f"Required config {key} not set")
    return value or default

def test_requires_config(self):
    with pytest.raises(ValueError, match="Required config"):
        service.process()  # Fails fast - no silent fallback
```

### 4. Test Failure Modes

**Principle**: After writing a test, intentionally break the code to verify the test catches it.

```python
# Step 1: Write the test
def test_validates_input(self):
    with pytest.raises(ValueError, match="Invalid ticker"):
        process_ticker('')

# Step 2: Sabotage code (comment out validation)
def process_ticker(ticker):
    # if not ticker:
    #     raise ValueError("Invalid ticker")
    return analyze(ticker)  # Proceeds with empty string

# Step 3: Run test - should FAIL
# If test still passes, it's not testing what you think it is

# Step 4: Restore code, verify test passes
```

### 4a. Test Sabotage Verification (Detailed Methodology)

**Principle**: The only way to know a test actually validates behavior is to break the code and verify the test fails.

**Why this matters**: Tests that pass when code is broken are "liars" - they create false confidence and don't catch regressions.

#### Step-by-Step Sabotage Process

**1. Write the test with specific assertions**

```python
def test_triggers_precompute_on_successful_fetch(self):
    """Test async Lambda invocation with correct payload"""
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {'StatusCode': 202}

    result = trigger_precompute(fetch_results, start_time)

    # Verify Lambda invocation
    mock_lambda.invoke.assert_called_once()

    # Verify invocation parameters
    invoke_args = mock_lambda.invoke.call_args
    assert invoke_args.kwargs['InvocationType'] == 'Event'  # Async

    # Verify payload structure
    payload = json.loads(invoke_args.kwargs['Payload'])
    assert payload['triggered_by'] == 'scheduler'
    assert 'fetch_summary' in payload
    assert payload['fetch_summary']['success_count'] == 47
```

**2. Run test - should PASS ✅**

```bash
$ pytest test_handler.py::test_triggers_precompute_on_successful_fetch
✅ PASSED
```

**3. Sabotage: Break ONE assertion at a time**

**Sabotage A: Wrong invocation type**
```python
def trigger_precompute(fetch_results, start_time):
    response = lambda_client.invoke(
        FunctionName=precompute_arn,
        InvocationType='RequestResponse',  # ← Changed from 'Event'
        Payload=json.dumps(payload)
    )
```

**Run test:**
```bash
$ pytest test_handler.py::test_triggers_precompute_on_successful_fetch
❌ FAILED - AssertionError: assert 'RequestResponse' == 'Event'
```
**Result:** ✅ Test caught the bug!

**Sabotage B: Wrong payload structure**
```python
def trigger_precompute(fetch_results, start_time):
    payload = {
        'triggered_by': 'manual',  # ← Changed from 'scheduler'
        'fetch_summary': {...}
    }
```

**Run test:**
```bash
❌ FAILED - AssertionError: assert 'manual' == 'scheduler'
```
**Result:** ✅ Test caught the bug!

**Sabotage C: Missing field**
```python
def trigger_precompute(fetch_results, start_time):
    payload = {
        'triggered_by': 'scheduler',
        # 'fetch_summary': {...}  # ← Removed this field
    }
```

**Run test:**
```bash
❌ FAILED - KeyError: 'fetch_summary'
```
**Result:** ✅ Test caught the bug!

**4. Restore code, verify test passes again**

```bash
$ pytest test_handler.py::test_triggers_precompute_on_successful_fetch
✅ PASSED
```

#### What to Sabotage

**Critical assertions to verify:**
- Return values (change `True` → `False`)
- Type checks (return wrong type)
- Field presence (remove required fields)
- Value comparisons (change expected values)
- Exception types (raise different exception)
- Invocation calls (skip function call)

**Example checklist for Lambda test:**
```python
# Test: Async Lambda invocation
def test_async_trigger():
    result = trigger_lambda()
    assert result is True  # ← Sabotage: return False
    assert mock.invoke.called  # ← Sabotage: remove invoke() call
    assert kwargs['InvocationType'] == 'Event'  # ← Sabotage: use 'RequestResponse'
    assert payload['ticker'] == 'NVDA19'  # ← Sabotage: use different ticker
```

**For each assertion, ask:**
- "If I break this, will the test fail?"
- "If this assertion is wrong, what bug would slip through?"

#### Red Flags: Tests That Can't Fail

**Warning sign 1: Generic truthy checks**
```python
# ❌ BAD: Test passes even when broken
def test_workflow():
    result = run_workflow()
    assert result  # Empty dict {} is truthy - test passes!
```

**Sabotage verification:**
```python
# Break the code - return empty dict
def run_workflow():
    return {}  # Should fail, but test passes!
```

**Fix:**
```python
# ✅ GOOD: Specific assertions
def test_workflow():
    result = run_workflow()
    assert 'indicators' in result
    assert len(result['indicators']) > 0
    assert result['indicators']['momentum'] > 0
```

**Warning sign 2: Only checking function was called**
```python
# ❌ BAD: Test passes even if function does nothing
def test_store_data():
    service.store('NVDA19', price=150.25)
    mock_db.execute.assert_called()  # Only checks it was called!
```

**Sabotage verification:**
```python
# Break the code - function does nothing
def store(ticker, price):
    # db.execute("INSERT ...")  # ← Comment out actual work
    pass  # Test still passes!
```

**Fix:**
```python
# ✅ GOOD: Check outcome, not just execution
def test_store_data():
    result = service.store('NVDA19', price=150.25)
    assert result is True  # Check return value

    # Verify data actually stored (round-trip)
    stored = service.get('NVDA19')
    assert stored['price'] == 150.25
```

**Warning sign 3: Mock defaults are truthy**
```python
# ❌ BAD: MagicMock returns truthy by default
def test_cache_check():
    mock_cache = MagicMock()  # Returns MagicMock by default (truthy)
    result = service.get_data(cache=mock_cache)
    assert result  # Passes even if service is broken!
```

**Sabotage verification:**
```python
# Break the code - always return None
def get_data(cache):
    return None  # Test still passes because mock is truthy!
```

**Fix:**
```python
# ✅ GOOD: Explicit mock return values
def test_cache_check():
    mock_cache = MagicMock()
    mock_cache.get.return_value = {'data': 'value'}  # Explicit

    result = service.get_data(cache=mock_cache)
    assert result == {'data': 'value'}  # Specific assertion
```

#### Sabotage Checklist

After writing any test, verify these break correctly:

- [ ] Change return value → test fails
- [ ] Remove required field → test fails
- [ ] Change assertion value → test fails
- [ ] Skip critical function call → test fails
- [ ] Return wrong type → test fails
- [ ] Raise different exception → test fails
- [ ] Comment out validation → test fails

**If any sabotage doesn't cause test failure, the test is not testing what you think it is.**

#### Integration with Test-Driven Development (TDD)

**TDD workflow with sabotage verification:**

1. **Red:** Write failing test
2. **Green:** Write minimal code to pass
3. **Sabotage:** Break code, verify test fails ← **ADD THIS STEP**
4. **Restore:** Fix code, verify test passes
5. **Refactor:** Improve code while keeping tests green

**Why add sabotage step:** Ensures "green" isn't a false positive from weak assertions.

#### Real-World Example: Scheduler Tests

From `tests/scheduler/test_ticker_fetcher_handler.py`:

**Test:** Verify precompute payload structure
```python
def test_precompute_payload_includes_failed_tickers():
    """Test payload includes both success and failed ticker lists"""
    mixed_results = {
        'success_count': 45,
        'failed_count': 2,
        'success': [{'ticker': 'NVDA', ...}],
        'failed': [
            {'ticker': 'INVALID1', 'error': 'Not found'},
            {'ticker': 'INVALID2', 'error': 'Timeout'}
        ]
    }

    result = trigger_precompute(mixed_results, start_time)

    payload = json.loads(mock_lambda.invoke.call_args.kwargs['Payload'])

    assert payload['fetch_summary']['failed_count'] == 2
    assert payload['fetch_summary']['failed_tickers'] == mixed_results['failed']
```

**Sabotage verification:**
```python
# Sabotage 1: Remove failed_tickers from payload
payload = {
    'fetch_summary': {
        'success_count': 45,
        'failed_count': 2,
        # 'failed_tickers': [...]  # ← Removed
    }
}
# Test result: ❌ FAILED - KeyError: 'failed_tickers' ✅

# Sabotage 2: Wrong failed_count
payload['fetch_summary']['failed_count'] = 0  # ← Wrong value
# Test result: ❌ FAILED - assert 0 == 2 ✅

# Sabotage 3: Empty failed_tickers list
payload['fetch_summary']['failed_tickers'] = []  # ← Wrong data
# Test result: ❌ FAILED - assert [] == [{...}, {...}] ✅
```

**Result:** All sabotage attempts caught by test ✅ - Test is reliable!

### 5. Validate Data Exists Before Dependent Operations

**Principle**: Never assume cache/database is populated. Always verify first.

```python
# ❌ BAD: Assumes data exists
def test_invalidate_cache(self):
    invalidate_cloudfront()  # Assumes cache populated
    # What if cache was empty? Test still passes!

# ✅ GOOD: Validates prerequisite data exists
def test_invalidate_cache(self):
    # Setup: Ensure data exists
    cache_count = check_cache_population()
    assert cache_count > 0, "Cache must be populated before invalidation"

    # Execute
    invalidate_cloudfront()

    # Verify
    # ... assertions
```

### 6. Validate Configuration Before Operations

**Principle**: Run validation tests as gates to distinguish config failures from logic failures.

```python
# ❌ BAD: Config and logic failures mixed
def test_populate_cache(self):
    lambda_client.invoke(...)  # Fails if AURORA_HOST not set
    # Can't tell if failure is config or logic

# ✅ GOOD: Validate config first (separate gate)
@pytest.fixture(scope='session')
def validate_deployment_ready():
    """Gate: Ensures environment is configured"""
    result = subprocess.run(['scripts/validate_deployment_ready.sh'])
    if result.returncode != 0:
        pytest.fail("Configuration validation failed - fix env vars first")

def test_populate_cache(validate_deployment_ready):
    # Now failures are logic/data issues, not config
    lambda_client.invoke(...)
```

### 7. Verify Actual Output Content

**Principle**: Code that executes without exceptions doesn't guarantee correct output.

```python
# ❌ BAD: Checks execution, not output
def test_workflow_executes(self):
    result = run_workflow()  # Returns empty dict {}
    assert result  # Passes (dict is truthy), but wrong!

# ✅ GOOD: Checks actual output content
def test_workflow_produces_data(self):
    result = run_workflow()

    # Verify structure exists
    assert 'user_facing_scores' in result, "Missing required field"

    # Verify content non-empty
    assert len(result['user_facing_scores']) > 0, "Scores should not be empty"

    # Verify expected keys
    assert 'momentum' in result['user_facing_scores']
```

## System Boundary Validation

### Boundary Type Compatibility

**Principle**: Test data type compatibility at every system boundary BEFORE integration.

**System Boundaries:**
- API ↔ Database
- Lambda ↔ JSON
- Python ↔ External API
- Service ↔ External Library

**Pattern**: Round-trip test - data must survive serialization/deserialization across the boundary.

```python
# Example: Aurora → Python → JSON boundary
def test_json_boundary_compatibility(self):
    """Verify data survives JSON serialization (Lambda responses)"""
    result = db.fetch_one("SELECT date FROM ticker_data")

    # BAD: Python date not JSON-serializable
    with pytest.raises(TypeError):
        json.dumps(result)  # ✗ Fails at boundary

    # GOOD: Convert at boundary
    result['date'] = result['date'].isoformat()
    serialized = json.dumps(result)  # ✓ Works

    # Round-trip verification
    deserialized = json.loads(serialized)
    assert deserialized['date'] == result['date']
```

### MySQL ENUM Silent Failures

**Problem**: MySQL ENUMs fail silently on mismatch - no exception, data just doesn't persist.

```python
def test_enum_boundary(self):
    """Verify ENUM values are valid BEFORE inserting"""
    # Check allowed ENUM values
    result = db.execute("SHOW COLUMNS FROM jobs WHERE Field = 'status'")
    allowed_values = parse_enum_values(result)  # ['pending', 'completed', 'failed']

    # Validate before insert
    status = 'in_progress'  # Invalid ENUM value
    assert status in allowed_values, f"Invalid status: {status}"
```

## AWS Services Success ≠ No Errors

**Principle**: AWS services returning 200 OK doesn't guarantee error-free execution.

### Multi-Layer Verification

Always validate across all layers:

1. **Exit Code/Status**: Did the process complete? (weakest signal)
2. **Logs**: What errors were logged? At what level?
3. **Data State**: What actually changed in databases/files? (strongest signal)

```python
@pytest.mark.integration
def test_lambda_success_with_log_validation(self):
    """Verify Lambda not only returns 200 but has no errors in logs"""
    # Level 1: Status code (weak)
    response = lambda_client.invoke(FunctionName='worker', Payload='{}')
    assert response['StatusCode'] == 200

    # Level 2: Response payload (stronger)
    payload = json.loads(response['Payload'].read())
    assert 'errorMessage' not in payload, f"Lambda error: {payload.get('errorMessage')}"

    # Level 3: CloudWatch logs (strongest)
    logs_client = boto3.client('logs')
    log_events = logs_client.filter_log_events(
        logGroupName=f'/aws/lambda/worker',
        startTime=int((datetime.now() - timedelta(minutes=1)).timestamp() * 1000),
        filterPattern='ERROR'
    )

    assert len(log_events['events']) == 0, \
        f"Found {len(log_events['events'])} errors in Lambda logs"
```

## Silent Failure Detection Patterns

### Database Operations

Database operations often fail without exceptions:

| Failure Mode | Raises Exception? | How to Detect |
|--------------|-------------------|---------------|
| FK constraint (MySQL) | Sometimes | Check rowcount |
| ENUM value mismatch | No | Check rowcount |
| Duplicate key (IGNORE) | No | Check rowcount |
| Write to wrong table | No | Round-trip test |

```python
def test_detects_fk_constraint_failure(self):
    """FK constraint violations should be detectable"""
    mock_client.execute.return_value = 0  # No rows affected

    result = service.store_report('INVALID_TICKER', 'text')

    # Code must check rowcount and return False
    assert result is False, "Should detect FK constraint failure"
```

### Workflow Validation Gates

**Principle**: Before executing a workflow node, validate that all prerequisite data exists.

```python
# ❌ BAD: Assumes upstream nodes succeeded
def test_analyze_technical(self):
    result = analyzer.analyze(state)  # Assumes ticker_data populated
    assert result is not None  # Might be empty dict!

# ✅ GOOD: Validates prerequisites before execution
def test_analyze_technical_validates_prerequisites(self):
    # Empty state (missing ticker_data)
    state = {'ticker': 'NVDA19', 'ticker_data': {}}

    result = analyzer.analyze(state)

    # Should detect missing prerequisite and set error
    assert 'error' in result
    assert 'ticker_data is empty' in result['error']
```

## The Truthy Trap

**Problem**: Empty dicts pass `if result:` checks but fail `if result['key']:` checks.

```python
# ❌ BAD: Truthy check misses empty dict
def test_workflow_produces_data(self):
    result = run_workflow()  # Returns {}
    assert result  # ✓ Passes (dict is truthy), but wrong!
    # Test passes but code is broken

# ✅ GOOD: Check for actual content
def test_workflow_produces_data(self):
    result = run_workflow()

    # Check structure
    assert 'indicators' in result, "Missing indicators"

    # Check content
    assert len(result['indicators']) > 0, "Indicators should not be empty"
```

## References

- **Testing patterns**: See [PATTERNS.md](PATTERNS.md)
- **Anti-patterns**: See [ANTI-PATTERNS.md](ANTI-PATTERNS.md)
- **Project CLAUDE.md**: Defensive Programming Principles section
