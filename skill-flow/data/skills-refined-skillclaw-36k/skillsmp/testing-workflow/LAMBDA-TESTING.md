# Lambda-Specific Testing Patterns

Testing patterns for AWS Lambda functions, Docker containers, and cross-service integration.

## Docker Container Testing

**Problem:** Lambda runs in a different environment than local development. Code that works locally may fail in Lambda due to missing dependencies, system libraries, or Python version differences.

**Solution:** Test imports and execution inside the Lambda Docker container BEFORE deploying to AWS.

### Pattern 1: Import Validation

**Purpose:** Verify all Python imports work in Lambda environment

**Script:** `scripts/test_docker_imports.sh`

```bash
#!/bin/bash
# Test Lambda handler imports inside Docker container

IMAGE_NAME="dr-lambda-import-test"

# Build Lambda Docker image
docker build -t $IMAGE_NAME -f lambda.Dockerfile .

# Test each handler can be imported
test_import() {
    local handler_module=$1
    local handler_name=$2

    echo -n "Testing: $handler_name... "

    if docker run --rm $IMAGE_NAME python3 -c "
from $handler_module import lambda_handler
assert callable(lambda_handler)
" 2>&1; then
        echo "✓ PASS"
    else
        echo "✗ FAIL"
        exit 1
    fi
}

# Test all handlers
test_import "src.scheduler.get_ticker_list_handler" "get_ticker_list"
test_import "src.scheduler.ticker_fetcher_handler" "ticker_fetcher"
```

**What it catches:**
- Missing dependencies in `requirements.txt`
- Import errors (wrong module paths, circular imports)
- Missing system libraries (e.g., libpq for psycopg2)
- Python version incompatibilities

**Example failure:**
```
Testing: get_ticker_list_handler...
❌ Import failed: ModuleNotFoundError: No module named 'pymysql'
```

**Fix:** Add missing dependency to `requirements.txt`

---

### Pattern 2: Local Execution with Mocked AWS

**Purpose:** Execute Lambda handlers inside Docker with mocked AWS services

**Script:** `scripts/test_docker_local.sh`

```bash
#!/bin/bash
# Test Lambda handler execution inside Docker with mocked AWS

# Test get_ticker_list with mocked Aurora
GET_TICKER_TEST=$(cat <<'EOF'
import json
import os
import sys
import unittest.mock as mock

# Mock environment variables
os.environ['AURORA_HOST'] = 'mock-aurora.cluster.amazonaws.com'
os.environ['AURORA_USERNAME'] = 'test_user'
os.environ['AURORA_PASSWORD'] = 'test_password'
os.environ['AURORA_DATABASE'] = 'ticker_data'

# Mock pymysql
sys.modules['pymysql'] = mock.MagicMock()

mock_cursor = mock.MagicMock()
mock_cursor.fetchall.return_value = [('NVDA19',), ('DBS19',)]

mock_conn = mock.MagicMock()
mock_conn.cursor.return_value = mock_cursor

with mock.patch('pymysql.connect', return_value=mock_conn):
    from src.scheduler.get_ticker_list_handler import lambda_handler
    result = lambda_handler({}, None)

    # Verify result structure
    assert 'tickers' in result
    assert result['count'] == 2
    print('✓ Handler executed successfully')
EOF
)

docker run --rm $IMAGE_NAME python3 -c "$GET_TICKER_TEST"
```

**What it catches:**
- Handler execution errors
- Environment variable issues
- Response format problems
- Error handling bugs

**Why this matters:** Catches bugs that unit tests miss (environment-specific issues) without deploying to AWS.

---

### Pattern 3: Critical Dependency Validation

**Purpose:** Verify critical libraries are available and importable

```bash
test_dependency() {
    local package=$1
    local import_name=$2

    echo -n "Testing: $package... "

    if docker run --rm $IMAGE_NAME python3 -c "import $import_name" 2>&1; then
        echo "✓ PASS"
    else
        echo "✗ FAIL"
        exit 1
    fi
}

# Test critical dependencies
test_dependency "pymysql" "pymysql"
test_dependency "boto3" "boto3"
test_dependency "yfinance" "yfinance"
```

**Common issues:**
- NumPy/SciPy require system libraries (`libopenblas`, `libgfortran`)
- Pillow requires image libraries (`libjpeg`, `libpng`)
- psycopg2 requires PostgreSQL client libraries

---

## Contract Testing: Lambda ↔ Step Functions

**Problem:** Lambda output schema must match Step Functions JSONPath expectations. Mismatches cause silent failures (Step Functions can't extract data, workflow fails).

**Solution:** Validate Lambda outputs match Step Functions state machine definition.

### Pattern 4: Output Schema Validation

**Purpose:** Ensure Lambda output has correct structure for Step Functions

```python
def test_output_schema_matches_step_functions():
    """Test Lambda output schema matches $.ticker_list.tickers JSONPath"""
    from src.scheduler.get_ticker_list_handler import lambda_handler

    result = lambda_handler({}, None)

    # Step Functions expects: $.ticker_list.tickers
    # So Lambda must return: {"tickers": [...], "count": N}
    assert 'tickers' in result, "Missing 'tickers' field (required by Step Functions)"
    assert 'count' in result, "Missing 'count' field"

    # Verify types (Step Functions Map state requires list of strings)
    assert isinstance(result['tickers'], list), "tickers must be a list"
    assert all(isinstance(t, str) for t in result['tickers']), \
        "All tickers must be strings for Map state iteration"

    # Verify non-empty tickers
    assert all(len(t) > 0 for t in result['tickers']), \
        "Ticker symbols must not be empty"
```

**What it catches:**
- Missing required fields
- Wrong data types (e.g., dict instead of list)
- Empty values that break iteration
- Non-JSON-serializable types (NumPy, datetime)

---

### Pattern 5: JSONPath Extraction Validation

**Purpose:** Verify Step Functions can extract data using JSONPath

**Script:** `scripts/test_contracts.sh`

```bash
#!/bin/bash
# Test Step Functions JSONPath extraction

TEST_STATE=$(cat <<'EOF'
{
  "ticker_list": {
    "tickers": ["NVDA19", "DBS19", "AAPL19"],
    "count": 3
  }
}
EOF
)

# Test JSONPath: $.ticker_list.tickers (used in Map state ItemsPath)
EXTRACTED_TICKERS=$(echo "$TEST_STATE" | jq -r '.ticker_list.tickers[]' 2>/dev/null)

if [ $? -eq 0 ] && [ -n "$EXTRACTED_TICKERS" ]; then
    TICKER_COUNT=$(echo "$EXTRACTED_TICKERS" | wc -l)
    if [ "$TICKER_COUNT" -eq 3 ]; then
        echo "✓ PASS - JSONPath $.ticker_list.tickers works correctly"
    else
        echo "✗ FAIL - Expected 3 tickers, got $TICKER_COUNT"
        exit 1
    fi
else
    echo "✗ FAIL - JSONPath extraction failed"
    exit 1
fi
```

---

### Pattern 6: Map State Iterator Validation

**Purpose:** Verify Map state can iterate over Lambda output

```python
def test_map_state_iteration():
    """Test Step Functions Map state can iterate over ticker list"""
    from src.scheduler.get_ticker_list_handler import lambda_handler

    result = lambda_handler({}, None)

    # Simulate Step Functions Map state iteration
    state = {"ticker_list": result}

    # Extract tickers (ItemsPath: $.ticker_list.tickers)
    tickers = state["ticker_list"]["tickers"]

    # Simulate Map state iteration
    for ticker in tickers:
        # Each iteration creates this input for SubmitToSQS task
        iteration_input = {
            "ticker": ticker,  # From $$.Map.Item.Value
            "execution_id": "test-exec-123"  # From $$.Execution.Name
        }

        # Verify iteration input is valid
        assert isinstance(iteration_input["ticker"], str)
        assert len(iteration_input["ticker"]) > 0

    print(f"✓ Map iteration works for {len(tickers)} tickers")
```

---

### Pattern 7: JSON Serializability Validation

**Purpose:** Verify Lambda output is JSON-serializable (Lambda requirement)

```python
def test_json_serializability():
    """Test Lambda output survives JSON serialization"""
    import json
    from src.scheduler.get_ticker_list_handler import lambda_handler

    result = lambda_handler({}, None)

    # Attempt JSON serialization (Lambda does this automatically)
    try:
        json_str = json.dumps(result)
        parsed = json.loads(json_str)
    except TypeError as e:
        pytest.fail(f"Output not JSON-serializable: {e}")

    # Verify round-trip produces same result
    assert parsed == result, "Round-trip serialization changed data"
```

**Common JSON serialization issues:**
- NumPy types (`np.int64` → use `int()`)
- Pandas types (`pd.Timestamp` → use `.isoformat()`)
- Datetime objects (use `.isoformat()`)
- Custom classes (use `__dict__` or Pydantic)

---

## Async Lambda Invocation Testing

**Problem:** Testing async Lambda invocations (fire-and-forget) requires different patterns than synchronous invocations.

**Pattern:** Verify async invocation type and payload structure, not response content.

### Pattern 8: Async Invocation Type Validation

**Purpose:** Ensure Lambda is invoked asynchronously (doesn't block caller)

```python
@patch('src.scheduler.ticker_fetcher_handler.boto3.client')
def test_triggers_precompute_asynchronously(mock_boto_client):
    """Test precompute is triggered with async invocation"""
    # Setup
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {'StatusCode': 202}  # Async accepted
    mock_boto_client.return_value = mock_lambda

    # Execute
    result = trigger_precompute(fetch_results, start_time)

    # Verify async invocation type
    invoke_args = mock_lambda.invoke.call_args
    assert invoke_args.kwargs['InvocationType'] == 'Event', \
        "Must use 'Event' for async (not 'RequestResponse')"

    # Verify doesn't wait for response
    assert result is True, "Should return immediately after triggering"
```

**Invocation types:**
- `RequestResponse` - Synchronous (waits for Lambda to finish, returns result)
- `Event` - Asynchronous (fire-and-forget, returns immediately)
- `DryRun` - Validation only (doesn't execute)

---

### Pattern 9: Async Payload Structure Validation

**Purpose:** Verify correct payload structure for async Lambda

```python
def test_async_payload_structure():
    """Test async Lambda receives correct payload format"""
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {'StatusCode': 202}

    trigger_precompute(fetch_results, start_time)

    # Extract payload
    payload_str = mock_lambda.invoke.call_args.kwargs['Payload']
    payload = json.loads(payload_str)

    # Verify required fields
    assert 'triggered_by' in payload
    assert payload['triggered_by'] == 'scheduler'

    # Verify fetch summary
    assert 'fetch_summary' in payload
    assert 'success_count' in payload['fetch_summary']
    assert 'failed_count' in payload['fetch_summary']

    # Verify timestamp
    assert 'timestamp' in payload
    # Should be valid ISO format
    datetime.fromisoformat(payload['timestamp'])
```

---

### Pattern 10: Async Failure Handling

**Purpose:** Ensure caller handles async invocation failures gracefully

```python
def test_async_invocation_handles_failure_gracefully():
    """Test scheduler continues even if async trigger fails"""
    mock_lambda = MagicMock()
    # Lambda invoke raises exception
    mock_lambda.invoke.side_effect = Exception("Lambda service error")

    # Scheduler should catch exception and return False
    result = trigger_precompute(fetch_results, start_time)

    # Scheduler should NOT raise exception (defensive error handling)
    assert result is False, "Should return False when trigger fails"

    # Scheduler itself should still succeed (defensive pattern)
    # The calling code checks result and logs warning, but doesn't fail
```

**Why this matters:** Async triggers are non-critical side effects. Main Lambda shouldn't fail if async trigger fails.

---

### Pattern 11: Status Code Validation

**Purpose:** Verify async invocation returns correct status code

```python
def test_async_status_code():
    """Test async invocation returns 202 Accepted"""
    mock_lambda = MagicMock()
    mock_lambda.invoke.return_value = {'StatusCode': 202}  # Async accepted

    result = trigger_precompute(fetch_results, start_time)
    assert result is True

    # Test unexpected status code
    mock_lambda.invoke.return_value = {'StatusCode': 500}  # Server error
    result = trigger_precompute(fetch_results, start_time)
    assert result is False, "Should return False for non-202 status"
```

**Expected status codes:**
- `202` - Accepted (async invocation queued successfully)
- `200` - OK (sync invocation succeeded)
- `4xx` - Client error (invalid function name, payload too large)
- `5xx` - Server error (Lambda service issue)

---

## Lambda Response Format Validation

### Pattern 12: Lambda Response Structure

**Purpose:** Ensure Lambda returns correct structure for API Gateway/Step Functions

```python
def test_lambda_response_structure():
    """Test Lambda returns correct response format"""
    result = lambda_handler({}, None)

    # Top-level keys
    assert 'statusCode' in result, "Missing statusCode"
    assert 'body' in result, "Missing body"

    # Status code is int
    assert isinstance(result['statusCode'], int)
    assert result['statusCode'] in [200, 400, 500]

    # Body is dict (not JSON string)
    # Lambda serializes to JSON automatically
    assert isinstance(result['body'], dict), \
        "Body should be dict, Lambda serializes it"
```

**Common mistake:** Returning `json.dumps(body)` instead of just `body`
```python
# ❌ BAD: Double-serialized
return {'statusCode': 200, 'body': json.dumps({'data': 'value'})}

# ✅ GOOD: Lambda serializes automatically
return {'statusCode': 200, 'body': {'data': 'value'}}
```

---

## SQS Message Format Validation

### Pattern 13: SQS Message Contract

**Purpose:** Validate SQS messages sent by Step Functions have correct format

```python
def test_sqs_message_format():
    """Test SQS message format for Step Functions → SQS → Lambda"""
    sqs_message = {
        "job_id": "rpt_NVDA19_test-exec-123",
        "ticker": "NVDA19",
        "execution_id": "test-exec-123",
        "source": "step_functions_precompute"
    }

    # Verify required fields
    required = ["job_id", "ticker", "execution_id", "source"]
    for field in required:
        assert field in sqs_message, f"Missing required field: {field}"

    # Verify job_id format: rpt_{ticker}_{execution_id}
    assert sqs_message["job_id"].startswith("rpt_")
    assert sqs_message["ticker"] in sqs_message["job_id"]

    # Verify JSON serializability (SQS requirement)
    json_str = json.dumps(sqs_message)
    assert isinstance(json_str, str)
```

---

## Common Issues and Solutions

### Issue 1: Import Works Locally, Fails in Docker

**Cause:** Different Python path or missing system library

**Solution:**
```dockerfile
# Add to Dockerfile
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# For system libraries
RUN yum install -y postgresql-devel  # For psycopg2
```

---

### Issue 2: NumPy Types Not JSON-Serializable

**Cause:** NumPy returns `np.int64`, `np.float64` instead of native Python types

**Solution:**
```python
# ❌ BAD: Returns NumPy type
return {'count': np.int64(42)}  # Fails JSON serialization

# ✅ GOOD: Convert to native type
return {'count': int(np.int64(42))}  # Works
```

---

### Issue 3: Step Functions Can't Extract Data

**Cause:** Lambda output doesn't match JSONPath in state machine

**Solution:** Read state machine definition, verify Lambda output structure
```json
// State machine expects: $.ticker_list.tickers
{
  "ItemsPath": "$.ticker_list.tickers"
}

// Lambda must return:
{
  "tickers": ["NVDA19", "DBS19"],  // ← Step Functions extracts this
  "count": 2
}
```

---

## Testing Checklist

Before deploying Lambda changes:

- [ ] Unit tests pass (Layer 1)
- [ ] Docker import tests pass (Layer 2)
- [ ] Docker local execution tests pass (Layer 3)
- [ ] Contract tests pass (Layer 4)
- [ ] Response is JSON-serializable
- [ ] All required fields present
- [ ] Types match Step Functions expectations
- [ ] Error handling tested

---

## References

- [Progressive Testing](PROGRESSIVE-TESTING.md) - 7-layer testing strategy
- [Defensive Testing](DEFENSIVE.md) - Validation gates and sabotage verification
- [Testing Patterns](PATTERNS.md) - Canonical test structure
- [AWS Lambda Testing Docs](https://docs.aws.amazon.com/lambda/latest/dg/testing-functions.html)
- [Step Functions JSONPath](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-paths.html)
