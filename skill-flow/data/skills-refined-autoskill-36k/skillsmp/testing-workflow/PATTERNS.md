# Testing Patterns

## Canonical Test Pattern

The standard pattern for writing tests in this project:

```python
class TestComponent:
    def setup_method(self):
        """Initialize component before each test"""
        self.component = Component()

    def test_success(self, mock_ticker_data):  # Use fixture from conftest
        """Test happy path with valid input"""
        result = self.component.process({'ticker': 'NVDA19'})
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        assert result['ticker'] == 'NVDA19'

    def test_error(self):
        """Test error handling with invalid input"""
        with pytest.raises(ValueError, match="Invalid"):
            self.component.process({'ticker': ''})

    @pytest.mark.asyncio
    async def test_async(self):
        """Test async operations with AsyncMock"""
        with patch.object(svc, 'fetch', new_callable=AsyncMock) as m:
            m.return_value = {'data': 1}
            result = await svc.get_data()
        assert result == {'data': 1}
```

**Key Elements:**
- Class-based organization
- `setup_method()` for initialization
- Descriptive test names (`test_behavior_description`)
- Use fixtures from conftest.py
- Assert specific types and values
- Test both success and error paths
- AsyncMock for async methods

## Fixture Usage

### Using Shared Fixtures (from conftest.py)

```python
# conftest.py - Define once
@pytest.fixture
def mock_ticker_data():
    return {
        'ticker': 'NVDA19',
        'price': 150.25,
        'change_pct': 2.5
    }

# test_component.py - Use everywhere
def test_process_ticker(mock_ticker_data):
    result = process(mock_ticker_data)
    assert result['ticker'] == 'NVDA19'
```

**Benefits:**
- Define once, use everywhere
- No duplicate mock data
- Easy to update across all tests

### Test-Specific Fixtures

```python
@pytest.fixture
def temp_file(tmp_path):
    """Create temporary file for this test only"""
    file = tmp_path / "test.json"
    file.write_text('{"key": "value"}')
    return file

def test_read_file(temp_file):
    data = read_json(temp_file)
    assert data['key'] == 'value'
```

## Mocking Patterns

### Patch Where Used (Not Where Defined)

```python
# ❌ BAD: Patch where defined
@patch('yfinance.download')  # Wrong - patches in yfinance module
def test_fetch_ticker(mock_download):
    result = ticker_service.fetch('NVDA')

# ✅ GOOD: Patch where used
@patch('src.data.ticker_service.yf.download')  # Right - patches in your module
def test_fetch_ticker(mock_download):
    mock_download.return_value = sample_dataframe
    result = ticker_service.fetch('NVDA')
    assert len(result) > 0
```

### Async Mocking

```python
# ❌ BAD: Regular Mock for async
with patch.object(svc, 'fetch_data', Mock()) as m:
    result = await svc.get_data()  # Breaks - Mock not awaitable

# ✅ GOOD: AsyncMock for async
with patch.object(svc, 'fetch_data', new_callable=AsyncMock) as m:
    m.return_value = {'data': 1}
    result = await svc.get_data()  # Works - AsyncMock is awaitable
    assert result == {'data': 1}
```

### Async Lambda Invocation Testing

**Pattern:** Testing async Lambda invocations (fire-and-forget triggers)

**Key difference from sync:** Async invocation returns immediately, doesn't wait for response.

```python
@patch('src.scheduler.ticker_fetcher_handler.boto3.client')
def test_async_lambda_trigger(mock_boto_client):
    """Test async Lambda invocation (fire-and-forget pattern)"""
    # Setup
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {'StatusCode': 202}  # Async accepted
    mock_boto_client.return_value = mock_lambda

    # Execute
    result = trigger_precompute(fetch_results, start_time)

    # Verify async invocation type (NOT 'RequestResponse')
    invoke_args = mock_lambda.invoke.call_args
    assert invoke_args.kwargs['InvocationType'] == 'Event', \
        "Must use 'Event' for async invocation"

    # Verify returns immediately (doesn't check response content)
    assert result is True

    # Verify payload structure
    payload = json.loads(invoke_args.kwargs['Payload'])
    assert payload['triggered_by'] == 'scheduler'
    assert 'fetch_summary' in payload
```

**Invocation types:**
- `Event` - Async (fire-and-forget, returns immediately)
- `RequestResponse` - Sync (waits for Lambda to finish)
- `DryRun` - Validation only

**Testing async invocation payload:**
```python
def test_async_payload_structure():
    """Test async Lambda receives correct payload format"""
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {'StatusCode': 202}

    trigger_precompute(fetch_results, start_time)

    # Extract and parse payload
    payload_str = mock_lambda.invoke.call_args.kwargs['Payload']
    payload = json.loads(payload_str)

    # Verify required fields
    assert 'triggered_by' in payload
    assert 'timestamp' in payload

    # Verify timestamp is ISO format
    from datetime import datetime
    datetime.fromisoformat(payload['timestamp'])  # Should not raise
```

**Defensive async error handling:**
```python
def test_async_trigger_handles_failure_gracefully():
    """Test caller handles async trigger failures without crashing"""
    mock_lambda = MagicMock()
    mock_lambda.invoke.side_effect = Exception("Lambda service error")

    # Should catch exception and return False (not raise)
    result = trigger_precompute(fetch_results, start_time)
    assert result is False

    # Main Lambda should still succeed (defensive pattern)
    # Async trigger is a non-critical side effect
```

**Status code validation:**
```python
def test_async_status_codes():
    """Test async invocation returns 202 Accepted"""
    mock_lambda = MagicMock()

    # Success case
    mock_lambda.invoke.return_value = {'StatusCode': 202}
    assert trigger_precompute(results, time) is True

    # Error case
    mock_lambda.invoke.return_value = {'StatusCode': 500}
    assert trigger_precompute(results, time) is False
```

**For detailed Lambda testing patterns, see [LAMBDA-TESTING.md](LAMBDA-TESTING.md)**

### Mock Return Values vs Side Effects

```python
# Return value (success case)
mock_api.call.return_value = {'status': 'ok'}

# Side effect (exception case)
mock_api.call.side_effect = TimeoutError()

# Side effect (sequence of returns)
mock_api.call.side_effect = [
    {'status': 'pending'},  # First call
    {'status': 'complete'}  # Second call
]
```

## Round-Trip Tests (Persistence)

Test that data can be stored AND retrieved (the actual contract):

```python
def test_cache_roundtrip(self):
    """Store then retrieve - the actual user contract"""
    # Store
    service.store_report(
        symbol='MWG19',
        report_text='Analysis report',
        report_json={'key': 'value'}
    )

    # Retrieve (the behavior that matters)
    result = service.get_cached_report('MWG19')

    # Assert the contract
    assert result is not None, "Stored report should be retrievable"
    assert result['report_text'] == 'Analysis report'
    assert result['report_json']['key'] == 'value'
```

**Why Round-Trip Tests:**
- Tests the actual user workflow (store → retrieve)
- Catches serialization issues
- Verifies foreign keys, constraints work
- More valuable than testing store/retrieve separately

## Boundary Contract Tests

Test data type compatibility at system boundaries (DB ↔ API, Lambda ↔ JSON):

```python
def test_json_serialization_boundary(self):
    """Verify data survives JSON boundary (Lambda response)"""
    # Python dict with date
    result = {
        'ticker': 'NVDA19',
        'date': datetime.now()  # Not JSON-serializable
    }

    # Should fail at boundary
    with pytest.raises(TypeError, match="not JSON serializable"):
        json.dumps(result)

def test_json_serialization_with_conversion(self):
    """Verify proper boundary conversion"""
    result = {
        'ticker': 'NVDA19',
        'date': datetime.now().isoformat()  # Converted for JSON
    }

    # Should succeed at boundary
    serialized = json.dumps(result)
    deserialized = json.loads(serialized)
    assert deserialized['ticker'] == 'NVDA19'
```

**System Boundaries to Test:**
- Aurora → Python → JSON (Lambda responses)
- Python → DynamoDB (type conversion)
- NumPy types → JSON (int64, float64)
- Pandas → JSON (Timestamp, NaT)

## Outcome-Based Testing

Test outcomes, not just execution:

```python
# ❌ Execution test: "Did it run?"
mock_client.execute.assert_called_once()  # Weak

# ✅ Outcome test: "Did it work?"
def test_store_returns_true_on_success(self):
    mock_client.execute.return_value = 1  # 1 row affected
    result = service.store_report('NVDA19', 'text')
    assert result is True  # Verified outcome

def test_store_returns_false_on_failure(self):
    mock_client.execute.return_value = 0  # No rows affected
    result = service.store_report('NVDA19', 'text')
    assert result is False  # Verified outcome
```

## Test Sabotage Verification

After writing a test, verify it can detect failures:

```python
# Step 1: Write the test
def test_store_returns_false_on_failure(self):
    mock_client.execute.return_value = 0
    result = service.store_report('NVDA19', 'text')
    assert result is False

# Step 2: Sabotage - temporarily break the code
def store_report(self, symbol, text):
    self.client.execute(query, params)
    return True  # BUG: Always returns True

# Step 3: Run test - it should FAIL
# If test passes despite sabotage, the test is worthless (The Liar)

# Step 4: Fix code, test should pass again
```

## Parametrized Tests

Test multiple inputs efficiently:

```python
@pytest.mark.parametrize("ticker,expected", [
    ("NVDA19", "NVDA"),
    ("AAPL34", "AAPL"),
    ("MSFT11", "MSFT"),
])
def test_extract_symbol(ticker, expected):
    result = extract_symbol(ticker)
    assert result == expected
```

## Integration Test Pattern

```python
@pytest.mark.integration
class TestAuroraIntegration:
    """Tests that require live Aurora connection"""

    def test_store_and_retrieve_ticker_data(self):
        """Round-trip test with real database"""
        # Store
        ticker_service.store('NVDA19', price=150.25)

        # Retrieve
        result = ticker_service.get('NVDA19')

        # Verify
        assert result['price'] == 150.25
```

## References

- **Anti-patterns**: See [ANTI-PATTERNS.md](ANTI-PATTERNS.md)
- **Defensive programming**: See [DEFENSIVE.md](DEFENSIVE.md)
- **Project testing guide**: `docs/TESTING_GUIDE.md`
